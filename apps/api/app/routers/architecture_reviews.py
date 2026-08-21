import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.architecture_decision import ArchitectureDecision
from app.models.architecture_review import ArchitectureReview
from app.schemas.architecture_decision import ArchitectureDecisionRead
from app.schemas.architecture_review import ArchitectureReviewCreate, ArchitectureReviewRead

router = APIRouter(prefix="/v1/architecture-decisions/{decision_id}", tags=["architecture-reviews"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _get_decision_or_404(session: Session, decision_id: uuid.UUID) -> ArchitectureDecision:
    decision = session.get(ArchitectureDecision, decision_id)
    if decision is None:
        raise problem(404, "Not Found", f"Architecture decision {decision_id} not found")
    return decision


@router.get("/reviews", response_model=list[ArchitectureReviewRead])
def list_reviews(decision_id: uuid.UUID, session: Session = Depends(get_session)) -> list[ArchitectureReview]:
    _get_decision_or_404(session, decision_id)
    statement = select(ArchitectureReview).where(ArchitectureReview.decision_id == decision_id)
    return list(session.exec(statement).all())


@router.post("/reviews", response_model=ArchitectureReviewRead, status_code=201)
def create_review(
    decision_id: uuid.UUID,
    payload: ArchitectureReviewCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> ArchitectureReview:
    _get_decision_or_404(session, decision_id)

    review = ArchitectureReview(decision_id=decision_id, **payload.model_dump())
    session.add(review)
    session.flush()

    record_audit_event(
        session,
        entity_type="ArchitectureReview",
        entity_id=review.id,
        action="create",
        correlation_id=_correlation_id(request),
        detail=f"decision_id={decision_id}",
    )
    session.commit()
    session.refresh(review)
    return review


@router.post("/accept", response_model=ArchitectureDecisionRead)
def accept_decision(
    decision_id: uuid.UUID, request: Request, session: Session = Depends(get_session)
) -> ArchitectureDecision:
    decision = _get_decision_or_404(session, decision_id)
    if decision.status != "proposed":
        raise problem(409, "Conflict", f"Cannot accept a decision in status '{decision.status}'.")

    decision.status = "accepted"
    session.add(decision)
    record_audit_event(
        session,
        entity_type="ArchitectureDecision",
        entity_id=decision.id,
        action="accept",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(decision)
    return decision


@router.post("/reject", response_model=ArchitectureDecisionRead)
def reject_decision(
    decision_id: uuid.UUID, request: Request, session: Session = Depends(get_session)
) -> ArchitectureDecision:
    decision = _get_decision_or_404(session, decision_id)
    if decision.status != "proposed":
        raise problem(409, "Conflict", f"Cannot reject a decision in status '{decision.status}'.")

    decision.status = "rejected"
    session.add(decision)
    record_audit_event(
        session,
        entity_type="ArchitectureDecision",
        entity_id=decision.id,
        action="reject",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(decision)
    return decision
