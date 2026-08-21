import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ArchitectureReviewCreate(BaseModel):
    business_alignment: int = Field(ge=1, le=5)
    security: int = Field(ge=1, le=5)
    privacy: int = Field(ge=1, le=5)
    reliability: int = Field(ge=1, le=5)
    performance: int = Field(ge=1, le=5)
    testability: int = Field(ge=1, le=5)
    operability: int = Field(ge=1, le=5)
    integration: int = Field(ge=1, le=5)
    data: int = Field(ge=1, le=5)
    cost: int = Field(ge=1, le=5)


class ArchitectureReviewRead(ArchitectureReviewCreate):
    id: uuid.UUID
    decision_id: uuid.UUID
    created_at: datetime
