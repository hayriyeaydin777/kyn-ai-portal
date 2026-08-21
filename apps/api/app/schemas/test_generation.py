import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class GeneratedTestCreate(BaseModel):
    source_snippet: str = Field(min_length=1, max_length=8000)


class GeneratedTestRead(BaseModel):
    id: uuid.UUID
    source_snippet: str
    generated_tests: str
    status: str
    created_at: datetime
