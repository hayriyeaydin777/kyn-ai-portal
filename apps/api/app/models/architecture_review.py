import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class ArchitectureReview(SQLModel, table=True):
    __tablename__ = "architecture_reviews"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    decision_id: uuid.UUID = Field(foreign_key="architecture_decisions.id", index=True)
    business_alignment: int
    security: int
    privacy: int
    reliability: int
    performance: int
    testability: int
    operability: int
    integration: int
    data: int
    cost: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
