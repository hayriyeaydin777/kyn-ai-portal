import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ArchitectureDecisionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    context: str = Field(min_length=1, max_length=4000)
    drivers: str = Field(min_length=1, max_length=2000)
    decision: str = Field(min_length=1, max_length=2000)
    consequences: str = Field(default="", max_length=2000)


class ArchitectureDecisionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    context: str | None = Field(default=None, min_length=1, max_length=4000)
    drivers: str | None = Field(default=None, min_length=1, max_length=2000)
    decision: str | None = Field(default=None, min_length=1, max_length=2000)
    consequences: str | None = Field(default=None, max_length=2000)


class ArchitectureDecisionRead(BaseModel):
    id: uuid.UUID
    title: str
    context: str
    drivers: str
    alternatives: str
    decision: str
    consequences: str
    status: str
    version: int
    created_at: datetime
