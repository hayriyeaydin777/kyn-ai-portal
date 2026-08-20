import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DependencyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    dependency_type: str = Field(min_length=1, max_length=50)
    criticality: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    notes: str | None = Field(default=None, max_length=2000)


class DependencyRead(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    name: str
    dependency_type: str
    criticality: str
    notes: str | None
    created_at: datetime
