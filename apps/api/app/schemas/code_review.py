import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CodeReviewCreate(BaseModel):
    source_snippet: str = Field(min_length=1, max_length=8000)
    language: str = Field(default="python", pattern="^(python)$")


class CodeFindingRead(BaseModel):
    rule_id: str
    severity: str
    message: str
    line: int | None = None


class CodeReviewRead(BaseModel):
    id: uuid.UUID
    source_snippet: str
    language: str
    findings: list[CodeFindingRead]
    provider: str
    summary: str
    citations: list[str]
    status: str
    created_at: datetime
