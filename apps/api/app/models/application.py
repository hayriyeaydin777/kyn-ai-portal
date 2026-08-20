import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class ApplicationProfile(SQLModel, table=True):
    __tablename__ = "application_profiles"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    business_owner: str | None = Field(default=None, max_length=200)
    criticality: str = Field(default="medium", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
