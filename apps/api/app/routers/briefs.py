import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.application import ApplicationProfile
from app.models.brief import Brief
from app.providers.factory import get_provider
from app.schemas.brief import BriefRead, brief_to_read
from app.services.citation_validator import UnsupportedClaimError, validate_citations
from app.services.evidence_bundle import build_evidence_bundle

router = APIRouter(prefix="/v1/applications/{application_id}/briefs", tags=["briefs"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _get_application_or_404(session: Session, application_id: uuid.UUID) -> ApplicationProfile:
    profile = session.get(ApplicationProfile, application_id)
    if profile is None:
        raise problem(404, "Not Found", f"Application {application_id} not found")
    return profile


@router.get("", response_model=list[BriefRead])
def list_briefs(application_id: uuid.UUID, session: Session = Depends(get_session)) -> list[BriefRead]:
    _get_application_or_404(session, application_id)
    statement = select(Brief).where(Brief.application_id == application_id)
    briefs = session.exec(statement).all()
    return [brief_to_read(b) for b in briefs]


@router.post("", response_model=BriefRead, status_code=201)
def generate_brief(
    application_id: uuid.UUID,
    request: Request,
    session: Session = Depends(get_session),
) -> BriefRead:
    profile = _get_application_or_404(session, application_id)
    evidence = build_evidence_bundle(session, profile)
    provider = get_provider()

    response = provider.generate("Summarize resilience posture.", evidence)

    try:
        validate_citations(response.citations, evidence.available_fields())
    except UnsupportedClaimError as exc:
        raise problem(422, "Unsupported Claim", str(exc)) from exc

    brief = Brief(
        application_id=application_id,
        provider=provider.name,
        text=response.text,
        citations=",".join(response.citations),
        status="draft",
    )
    session.add(brief)
    session.flush()

    record_audit_event(
        session,
        entity_type="Brief",
        entity_id=brief.id,
        action="create",
        correlation_id=_correlation_id(request),
        detail=f"application_id={application_id},provider={provider.name}",
    )
    session.commit()
    session.refresh(brief)
    return brief_to_read(brief)
