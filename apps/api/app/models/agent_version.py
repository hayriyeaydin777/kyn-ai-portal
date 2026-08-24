import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class AgentVersion(SQLModel, table=True):
    __tablename__ = "agent_versions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    agent_id: uuid.UUID = Field(foreign_key="agent_definitions.id", index=True)
    version: int = Field(default=1)
    prompt_version: str = Field(max_length=50)
    input_schema: str = Field(sa_column=Column(Text, nullable=False))
    output_schema: str = Field(sa_column=Column(Text, nullable=False))
    allowed_tools: str = Field(sa_column=Column(Text, nullable=False))
    status: str = Field(default="draft", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
