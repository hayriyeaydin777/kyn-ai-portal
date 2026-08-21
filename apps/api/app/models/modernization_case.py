import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class ModernizationCase(SQLModel, table=True):
    __tablename__ = "modernization_cases"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    application_id: uuid.UUID = Field(foreign_key="application_profiles.id", index=True)
    technology_stack: str = Field(max_length=200)
    hosting: str = Field(max_length=100)
    release_process: str = Field(max_length=100)
    scale: str = Field(max_length=50)
    pain_points: str = Field(max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
