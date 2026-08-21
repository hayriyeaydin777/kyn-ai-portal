import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DiagramMetadataCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=2000)
    scope: str = Field(min_length=1, max_length=200)
    linked_decision_ids: list[str] = Field(default_factory=list)


class DiagramMetadataRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    scope: str
    version: int
    linked_decision_ids: list[str]
    created_at: datetime
