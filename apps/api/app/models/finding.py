import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Finding(SQLModel, table=True):
    __tablename__ = "findings"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    application_id: uuid.UUID = Field(foreign_key="application_profiles.id", index=True)
    rule_id: str = Field(max_length=20)
    severity: str = Field(max_length=20)
    message: str = Field(max_length=2000)
    evidence_fields: str = Field(max_length=1000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
