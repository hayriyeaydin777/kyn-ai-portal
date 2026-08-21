import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class ModernizationRecommendation(SQLModel, table=True):
    __tablename__ = "modernization_recommendations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    application_id: uuid.UUID = Field(foreign_key="application_profiles.id", index=True)
    modernization_case_id: uuid.UUID = Field(foreign_key="modernization_cases.id", index=True)
    complexity_score: int
    risk_signals: str = Field(max_length=2000)
    matched_option_ids: str = Field(max_length=500)
    provider: str = Field(max_length=50)
    narrative: str = Field(max_length=4000)
    citations: str = Field(max_length=2000)
    status: str = Field(default="draft", max_length=20)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
