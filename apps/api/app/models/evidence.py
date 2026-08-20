import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class EvidenceArtifact(SQLModel, table=True):
    __tablename__ = "evidence_artifacts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    application_id: uuid.UUID = Field(foreign_key="application_profiles.id", index=True)
    title: str = Field(max_length=200)
    source: str = Field(max_length=200)
    reference: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
