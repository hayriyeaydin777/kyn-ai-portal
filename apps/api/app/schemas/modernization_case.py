import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ModernizationCaseCreate(BaseModel):
    technology_stack: str = Field(min_length=1, max_length=200)
    hosting: str = Field(min_length=1, max_length=100)
    release_process: str = Field(min_length=1, max_length=100)
    scale: str = Field(min_length=1, max_length=50)
    pain_points: str = Field(default="", max_length=2000)


class ModernizationCaseRead(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    technology_stack: str
    hosting: str
    release_process: str
    scale: str
    pain_points: str
    created_at: datetime
