import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class AgentDefinition(SQLModel, table=True):
    __tablename__ = "agent_definitions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=200)
    purpose: str = Field(sa_column=Column(Text, nullable=False))
    owner: str = Field(max_length=200)
    security_tier: str = Field(max_length=20)
    approval_required: bool = Field(default=True)
    lifecycle_status: str = Field(default="draft", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
