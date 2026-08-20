import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.brief import Brief


class BriefRead(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    provider: str
    text: str
    citations: list[str]
    status: str
    created_at: datetime


def brief_to_read(brief: Brief) -> BriefRead:
    return BriefRead(
        id=brief.id,
        application_id=brief.application_id,
        provider=brief.provider,
        text=brief.text,
        citations=brief.citations.split(",") if brief.citations else [],
        status=brief.status,
        created_at=brief.created_at,
    )
