import uuid
from datetime import datetime

from pydantic import BaseModel


class FindingRead(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    rule_id: str
    severity: str
    message: str
    evidence_fields: list[str]
    created_at: datetime
