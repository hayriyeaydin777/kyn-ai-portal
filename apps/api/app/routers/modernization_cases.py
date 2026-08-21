import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.application import ApplicationProfile
from app.models.modernization_case import ModernizationCase
from app.schemas.modernization_case import ModernizationCaseCreate, ModernizationCaseRead

router = APIRouter(prefix="/v1/applications/{application_id}/modernization-cases", tags=["modernization"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _get_application_or_404(session: Session, application_id: uuid.UUID) -> ApplicationProfile:
    profile = session.get(ApplicationProfile, application_id)
    if profile is None:
        raise problem(404, "Not Found", f"Application {application_id} not found")
    return profile


@router.get("", response_model=list[ModernizationCaseRead])
def list_modernization_cases(
    application_id: uuid.UUID, session: Session = Depends(get_session)
) -> list[ModernizationCase]:
    _get_application_or_404(session, application_id)
    statement = select(ModernizationCase).where(ModernizationCase.application_id == application_id)
    return list(session.exec(statement).all())


@router.post("", response_model=ModernizationCaseRead, status_code=201)
def create_modernization_case(
    application_id: uuid.UUID,
    payload: ModernizationCaseCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> ModernizationCase:
    _get_application_or_404(session, application_id)
    case = ModernizationCase(application_id=application_id, **payload.model_dump())
    session.add(case)
    session.flush()

    record_audit_event(
        session,
        entity_type="ModernizationCase",
        entity_id=case.id,
        action="create",
        correlation_id=_correlation_id(request),
        detail=f"application_id={application_id}",
    )
    session.commit()
    session.refresh(case)
    return case


@router.get("/{case_id}", response_model=ModernizationCaseRead)
def get_modernization_case(
    application_id: uuid.UUID, case_id: uuid.UUID, session: Session = Depends(get_session)
) -> ModernizationCase:
    _get_application_or_404(session, application_id)
    case = session.get(ModernizationCase, case_id)
    if case is None or case.application_id != application_id:
        raise problem(404, "Not Found", f"Modernization case {case_id} not found")
    return case
