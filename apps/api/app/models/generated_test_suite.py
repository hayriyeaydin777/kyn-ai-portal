import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class GeneratedTestSuite(SQLModel, table=True):
    __tablename__ = "generated_test_suites"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source_snippet: str = Field(sa_column=Column(Text, nullable=False))
    generated_tests: str = Field(sa_column=Column(Text, nullable=False))
    status: str = Field(default="draft", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
