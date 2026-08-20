"""Seed synthetic, fictional demo data. Never use real employer/client data here."""

from sqlmodel import Session, select

from app.db import engine
from app.models.application import ApplicationProfile
from app.models.dependency import Dependency
from app.models.evidence import EvidenceArtifact

APPLICATIONS = [
    {
        "name": "Northstar Claims Service",
        "description": "Fictional claims processing platform used for demo purposes.",
        "business_owner": "Demo Product Owner",
        "criticality": "high",
        "dependencies": [
            {"name": "Synthetic Identity Provider", "dependency_type": "auth", "criticality": "high"},
            {"name": "Aurora Message Bus", "dependency_type": "messaging", "criticality": "medium"},
        ],
        "evidence": [
            {"title": "Synthetic architecture diagram", "source": "demo-doc", "reference": "adr-001"},
        ],
    },
    {
        "name": "Aurora Customer Portal",
        "description": "Fictional customer-facing portal used for demo purposes.",
        "business_owner": "Demo Product Owner",
        "criticality": "medium",
        "dependencies": [
            {"name": "Atlas Messaging Service", "dependency_type": "messaging", "criticality": "medium"},
        ],
        "evidence": [
            {"title": "Synthetic release notes", "source": "demo-doc", "reference": None},
        ],
    },
    {
        "name": "Atlas Messaging Service",
        "description": "Fictional internal messaging service used for demo purposes.",
        "business_owner": "Demo Platform Owner",
        "criticality": "medium",
        "dependencies": [],
        "evidence": [],
    },
]


def seed() -> None:
    with Session(engine) as session:
        for app_data in APPLICATIONS:
            existing = session.exec(
                select(ApplicationProfile).where(ApplicationProfile.name == app_data["name"])
            ).first()
            if existing:
                continue
            profile = ApplicationProfile(
                name=app_data["name"],
                description=app_data["description"],
                business_owner=app_data["business_owner"],
                criticality=app_data["criticality"],
            )
            session.add(profile)
            session.flush()

            for dep in app_data["dependencies"]:
                session.add(Dependency(application_id=profile.id, **dep))
            for ev in app_data["evidence"]:
                session.add(EvidenceArtifact(application_id=profile.id, **ev))

        session.commit()
    print("Seed complete.")


if __name__ == "__main__":
    seed()
