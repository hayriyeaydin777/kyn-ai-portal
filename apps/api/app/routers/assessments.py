import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.clients.policy_client import PolicyClient, PolicyServiceError
from app.db import get_session
from app.errors import problem
from app.models.application import ApplicationProfile
from app.models.dependency import Dependency
from app.models.finding import Finding
from app.schemas.finding import FindingRead

router = APIRouter(prefix="/v1/applications/{application_id}/assessments", tags=["assessments"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _get_application_or_404(session: Session, application_id: uuid.UUID) -> ApplicationProfile:
    profile = session.get(ApplicationProfile, application_id)
    if profile is None:
        raise problem(404, "Not Found", f"Application {application_id} not found")
    return profile


def _finding_to_read(finding: Finding) -> FindingRead:
    return FindingRead(
        id=finding.id,
        application_id=finding.application_id,
        rule_id=finding.rule_id,
        severity=finding.severity,
        message=finding.message,
        evidence_fields=finding.evidence_fields.split(",") if finding.evidence_fields else [],
        created_at=finding.created_at,
    )


@router.get("", response_model=list[FindingRead])
def list_findings(
    application_id: uuid.UUID, session: Session = Depends(get_session)
) -> list[FindingRead]:
    _get_application_or_404(session, application_id)
    statement = select(Finding).where(Finding.application_id == application_id)
    findings = session.exec(statement).all()
    return [_finding_to_read(f) for f in findings]


@router.post("", response_model=list[FindingRead], status_code=201)
def evaluate_application(
    application_id: uuid.UUID,
    request: Request,
    session: Session = Depends(get_session),
    policy_client: PolicyClient = Depends(PolicyClient),
) -> list[FindingRead]:
    profile = _get_application_or_404(session, application_id)
    dependencies = session.exec(
        select(Dependency).where(Dependency.application_id == application_id)
    ).all()

    payload = {
        "applicationName": profile.name,
        "criticality": profile.criticality,
        "dependencies": [
            {"name": d.name, "dependencyType": d.dependency_type, "criticality": d.criticality}
            for d in dependencies
        ],
    }

    try:
        result = policy_client.evaluate(payload)
    except PolicyServiceError as exc:
        raise problem(503, "Policy Service Unavailable", str(exc)) from exc

    findings: list[Finding] = []
    for item in result.get("findings", []):
        finding = Finding(
            application_id=application_id,
            rule_id=item["ruleId"],
            severity=item["severity"],
            message=item["message"],
            evidence_fields=",".join(item.get("evidenceFields", [])),
        )
        session.add(finding)
        findings.append(finding)

    record_audit_event(
        session,
        entity_type="ApplicationProfile",
        entity_id=application_id,
        action="evaluate",
        correlation_id=_correlation_id(request),
        detail=f"{len(findings)} findings",
    )
    session.commit()
    for finding in findings:
        session.refresh(finding)

    return [_finding_to_read(f) for f in findings]
