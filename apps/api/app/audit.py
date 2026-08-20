import uuid

from sqlmodel import Session

from app.models.audit import AuditEvent


def record_audit_event(
    session: Session,
    *,
    entity_type: str,
    entity_id: uuid.UUID,
    action: str,
    correlation_id: str | None,
    detail: str | None = None,
) -> None:
    event = AuditEvent(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        correlation_id=correlation_id,
        detail=detail,
    )
    session.add(event)
