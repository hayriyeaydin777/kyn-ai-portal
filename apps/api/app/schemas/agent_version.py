import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AgentVersionCreate(BaseModel):
    prompt_version: str = Field(min_length=1, max_length=50)
    input_schema: str = Field(min_length=1, max_length=2000)
    output_schema: str = Field(min_length=1, max_length=2000)
    allowed_tools: list[str] = Field(default_factory=list)


class AgentVersionRead(BaseModel):
    id: uuid.UUID
    agent_id: uuid.UUID
    version: int
    prompt_version: str
    input_schema: str
    output_schema: str
    allowed_tools: list[str]
    status: str
    created_at: datetime
