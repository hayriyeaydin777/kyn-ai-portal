import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class CodeReviewRun(SQLModel, table=True):
    __tablename__ = "code_review_runs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_snippet: str = Field(sa_column=Column(Text, nullable=False))
    language: str = Field(default="python", max_length=20)
    findings: str = Field(sa_column=Column(Text, nullable=False))
    provider: str = Field(max_length=50)
    summary: str = Field(sa_column=Column(Text, nullable=False))
    citations: str = Field(sa_column=Column(Text, nullable=False))
    status: str = Field(default="draft", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
