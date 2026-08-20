import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ApplicationProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    business_owner: str | None = Field(default=None, max_length=200)
    criticality: str = Field(default="medium", pattern="^(low|medium|high|critical)$")


class ApplicationProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    business_owner: str | None = Field(default=None, max_length=200)
    criticality: str | None = Field(default=None, pattern="^(low|medium|high|critical)$")


class ApplicationProfileRead(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    business_owner: str | None
    criticality: str
    created_at: datetime
    updated_at: datetime
