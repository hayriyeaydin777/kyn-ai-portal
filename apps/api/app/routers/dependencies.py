import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.application import ApplicationProfile
from app.models.dependency import Dependency
from app.schemas.dependency import DependencyCreate, DependencyRead

router = APIRouter(prefix="/v1/applications/{application_id}/dependencies", tags=["dependencies"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _get_application_or_404(session: Session, application_id: uuid.UUID) -> ApplicationProfile:
    profile = session.get(ApplicationProfile, application_id)
    if profile is None:
        raise problem(404, "Not Found", f"Application {application_id} not found")
    return profile


@router.get("", response_model=list[DependencyRead])
def list_dependencies(
    application_id: uuid.UUID, session: Session = Depends(get_session)
) -> list[Dependency]:
    _get_application_or_404(session, application_id)
    statement = select(Dependency).where(Dependency.application_id == application_id)
    return list(session.exec(statement).all())


@router.post("", response_model=DependencyRead, status_code=201)
def create_dependency(
    application_id: uuid.UUID,
    payload: DependencyCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> Dependency:
    _get_application_or_404(session, application_id)
    dependency = Dependency(application_id=application_id, **payload.model_dump())
    session.add(dependency)
    session.flush()

    record_audit_event(
        session,
        entity_type="Dependency",
        entity_id=dependency.id,
        action="create",
        correlation_id=_correlation_id(request),
        detail=f"application_id={application_id}",
    )
    session.commit()
    session.refresh(dependency)
    return dependency
