import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.generated_test_suite import GeneratedTestSuite
from app.schemas.test_generation import GeneratedTestCreate, GeneratedTestRead
from app.services.test_skeleton_generator import generate_test_skeleton

router = APIRouter(prefix="/v1/test-generations", tags=["test-generations"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


@router.get("", response_model=list[GeneratedTestRead])
def list_test_generations(session: Session = Depends(get_session)) -> list[GeneratedTestSuite]:
    return list(session.exec(select(GeneratedTestSuite)).all())


@router.post("", response_model=GeneratedTestRead, status_code=201)
def create_test_generation(
    payload: GeneratedTestCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> GeneratedTestSuite:
    generated = generate_test_skeleton(payload.source_snippet)

    suite = GeneratedTestSuite(
        source_snippet=payload.source_snippet,
        generated_tests=generated,
        status="draft",
    )
    session.add(suite)
    session.flush()

    record_audit_event(
        session,
        entity_type="GeneratedTestSuite",
        entity_id=suite.id,
        action="create",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(suite)
    return suite


@router.get("/{suite_id}", response_model=GeneratedTestRead)
def get_test_generation(suite_id: uuid.UUID, session: Session = Depends(get_session)) -> GeneratedTestSuite:
    suite = session.get(GeneratedTestSuite, suite_id)
    if suite is None:
        raise problem(404, "Not Found", f"Generated test suite {suite_id} not found")
    return suite
