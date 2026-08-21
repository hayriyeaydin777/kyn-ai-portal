import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DocumentationDraftCreate(BaseModel):
    source_snippet: str = Field(min_length=1, max_length=8000)


class DocumentationDraftRead(BaseModel):
    id: uuid.UUID
    source_snippet: str
    draft_text: str
    version: int
    status: str
    created_at: datetime
