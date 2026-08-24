import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AgentDefinitionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    purpose: str = Field(min_length=1, max_length=2000)
    owner: str = Field(min_length=1, max_length=200)
    security_tier: str = Field(pattern="^(low|medium|high|critical)$")
    approval_required: bool = True


class AgentDefinitionRead(BaseModel):
    id: uuid.UUID
    name: str
    purpose: str
    owner: str
    security_tier: str
    approval_required: bool
    lifecycle_status: str
    created_at: datetime
