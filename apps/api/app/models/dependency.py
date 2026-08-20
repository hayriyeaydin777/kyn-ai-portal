import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Dependency(SQLModel, table=True):
    __tablename__ = "dependencies"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    application_id: uuid.UUID = Field(foreign_key="application_profiles.id", index=True)
    name: str = Field(max_length=200)
    dependency_type: str = Field(max_length=50)
    criticality: str = Field(default="medium", max_length=20)
    notes: str | None = Field(default=None, max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
