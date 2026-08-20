import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Brief(SQLModel, table=True):
    __tablename__ = "briefs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    application_id: uuid.UUID = Field(foreign_key="application_profiles.id", index=True)
    provider: str = Field(max_length=50)
    text: str = Field(max_length=4000)
    citations: str = Field(max_length=2000)
    status: str = Field(default="draft", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
