import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.application import ApplicationProfile
from app.schemas.application import (
    ApplicationProfileCreate,
    ApplicationProfileRead,
    ApplicationProfileUpdate,
)

router = APIRouter(prefix="/v1/applications", tags=["applications"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


@router.get("", response_model=list[ApplicationProfileRead])
def list_applications(session: Session = Depends(get_session)) -> list[ApplicationProfile]:
    return list(session.exec(select(ApplicationProfile)).all())


@router.post("", response_model=ApplicationProfileRead, status_code=201)
def create_application(
    payload: ApplicationProfileCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> ApplicationProfile:
    profile = ApplicationProfile(**payload.model_dump())
    session.add(profile)
    try:
        session.flush()
    except IntegrityError as exc:
        session.rollback()
        raise problem(409, "Conflict", f"Application '{payload.name}' already exists") from exc

    record_audit_event(
        session,
        entity_type="ApplicationProfile",
        entity_id=profile.id,
        action="create",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(profile)
    return profile


@router.get("/{application_id}", response_model=ApplicationProfileRead)
def get_application(
    application_id: uuid.UUID, session: Session = Depends(get_session)
) -> ApplicationProfile:
    profile = session.get(ApplicationProfile, application_id)
    if profile is None:
        raise problem(404, "Not Found", f"Application {application_id} not found")
    return profile


@router.patch("/{application_id}", response_model=ApplicationProfileRead)
def update_application(
    application_id: uuid.UUID,
    payload: ApplicationProfileUpdate,
    request: Request,
    session: Session = Depends(get_session),
) -> ApplicationProfile:
    profile = session.get(ApplicationProfile, application_id)
    if profile is None:
        raise problem(404, "Not Found", f"Application {application_id} not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(profile, field, value)
    if updates:
        profile.updated_at = datetime.now(timezone.utc)
    session.add(profile)

    try:
        session.flush()
    except IntegrityError as exc:
        session.rollback()
        raise problem(409, "Conflict", "Application name already exists") from exc

    record_audit_event(
        session,
        entity_type="ApplicationProfile",
        entity_id=profile.id,
        action="update",
        correlation_id=_correlation_id(request),
        detail=",".join(updates.keys()) or None,
    )
    session.commit()
    session.refresh(profile)
    return profile
