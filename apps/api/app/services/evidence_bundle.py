from dataclasses import dataclass, field

from sqlmodel import Session, select

from app.models.application import ApplicationProfile
from app.models.dependency import Dependency
from app.models.finding import Finding


@dataclass
class EvidenceBundle:
    """Structured, DB-sourced context passed to any LLMProvider. Only real fields may be cited."""

    application: dict
    dependencies: list[dict] = field(default_factory=list)
    findings: list[dict] = field(default_factory=list)

    def available_fields(self) -> set[str]:
        """Citation keys that are valid because they trace back to real data."""
        fields = {f"application.{key}" for key in self.application}
        for i, dep in enumerate(self.dependencies):
            fields.update(f"dependencies[{i}].{key}" for key in dep)
        for i, finding in enumerate(self.findings):
            fields.update(f"findings[{i}].{key}" for key in finding)
        return fields


def build_evidence_bundle(session: Session, application: ApplicationProfile) -> EvidenceBundle:
    dependencies = session.exec(
        select(Dependency).where(Dependency.application_id == application.id)
    ).all()
    findings = session.exec(select(Finding).where(Finding.application_id == application.id)).all()

    return EvidenceBundle(
        application={
            "name": application.name,
            "description": application.description,
            "business_owner": application.business_owner,
            "criticality": application.criticality,
        },
        dependencies=[
            {"name": d.name, "dependency_type": d.dependency_type, "criticality": d.criticality}
            for d in dependencies
        ],
        findings=[
            {"rule_id": f.rule_id, "severity": f.severity, "message": f.message} for f in findings
        ],
    )
