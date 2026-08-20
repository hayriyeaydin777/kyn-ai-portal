import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class EvidenceArtifactCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    source: str = Field(min_length=1, max_length=200)
    reference: str | None = Field(default=None, max_length=500)


class EvidenceArtifactRead(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    title: str
    source: str
    reference: str | None
    created_at: datetime
