import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class DiagramMetadata(SQLModel, table=True):
    __tablename__ = "diagram_metadata"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(sa_column=Column(Text, nullable=False))
    scope: str = Field(max_length=200)
    version: int = Field(default=1)
    linked_decision_ids: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
