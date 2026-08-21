import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class ArchitectureDecision(SQLModel, table=True):
    __tablename__ = "architecture_decisions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=200)
    context: str = Field(sa_column=Column(Text, nullable=False))
    drivers: str = Field(sa_column=Column(Text, nullable=False))
    alternatives: str = Field(sa_column=Column(Text, nullable=False))
    decision: str = Field(sa_column=Column(Text, nullable=False))
    consequences: str = Field(sa_column=Column(Text, nullable=False))
    status: str = Field(default="draft", max_length=20)
    version: int = Field(default=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
