import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class AuditEvent(SQLModel, table=True):
    __tablename__ = "audit_events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    entity_type: str = Field(max_length=100, index=True)
    entity_id: uuid.UUID = Field(index=True)
    action: str = Field(max_length=50)
    correlation_id: str | None = Field(default=None, max_length=100)
    detail: str | None = Field(default=None, max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
