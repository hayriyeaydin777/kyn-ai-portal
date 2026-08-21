import uuid
from datetime import datetime

from pydantic import BaseModel


class ModernizationRecommendationRead(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    modernization_case_id: uuid.UUID
    complexity_score: int
    risk_signals: list[dict]
    matched_option_ids: list[str]
    provider: str
    narrative: str
    citations: list[str]
    status: str
    created_at: datetime
