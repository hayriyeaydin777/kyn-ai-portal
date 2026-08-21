import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.architecture_decision import ArchitectureDecision
from app.schemas.architecture_decision import (
    ArchitectureDecisionCreate,
    ArchitectureDecisionRead,
    ArchitectureDecisionUpdate,
)
from app.services.adr_alternatives import draft_alternatives

router = APIRouter(prefix="/v1/architecture-decisions", tags=["architecture-decisions"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _get_or_404(session: Session, decision_id: uuid.UUID) -> ArchitectureDecision:
    decision = session.get(ArchitectureDecision, decision_id)
    if decision is None:
        raise problem(404, "Not Found", f"Architecture decision {decision_id} not found")
    return decision


@router.get("", response_model=list[ArchitectureDecisionRead])
def list_decisions(session: Session = Depends(get_session)) -> list[ArchitectureDecision]:
    return list(session.exec(select(ArchitectureDecision)).all())


@router.post("", response_model=ArchitectureDecisionRead, status_code=201)
def create_decision(
    payload: ArchitectureDecisionCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> ArchitectureDecision:
    alternatives_text, _citations, _provider = draft_alternatives(payload.context, payload.drivers)

    decision = ArchitectureDecision(
        title=payload.title,
        context=payload.context,
        drivers=payload.drivers,
        alternatives=alternatives_text,
        decision=payload.decision,
        consequences=payload.consequences,
        status="draft",
        version=1,
    )
    session.add(decision)
    session.flush()

    record_audit_event(
        session,
        entity_type="ArchitectureDecision",
        entity_id=decision.id,
        action="create",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(decision)
    return decision


@router.get("/{decision_id}", response_model=ArchitectureDecisionRead)
def get_decision(decision_id: uuid.UUID, session: Session = Depends(get_session)) -> ArchitectureDecision:
    return _get_or_404(session, decision_id)


@router.patch("/{decision_id}", response_model=ArchitectureDecisionRead)
def update_decision(
    decision_id: uuid.UUID,
    payload: ArchitectureDecisionUpdate,
    request: Request,
    session: Session = Depends(get_session),
) -> ArchitectureDecision:
    decision = _get_or_404(session, decision_id)

    if decision.status == "accepted":
        raise problem(
            409,
            "Conflict",
            "Accepted architecture decisions are immutable. Create a new version instead.",
        )

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(decision, field, value)
    session.add(decision)

    record_audit_event(
        session,
        entity_type="ArchitectureDecision",
        entity_id=decision.id,
        action="update",
        correlation_id=_correlation_id(request),
        detail=",".join(updates.keys()) or None,
    )
    session.commit()
    session.refresh(decision)
    return decision


@router.post("/{decision_id}/propose", response_model=ArchitectureDecisionRead)
def propose_decision(
    decision_id: uuid.UUID, request: Request, session: Session = Depends(get_session)
) -> ArchitectureDecision:
    decision = _get_or_404(session, decision_id)
    if decision.status != "draft":
        raise problem(409, "Conflict", f"Cannot propose a decision in status '{decision.status}'.")

    decision.status = "proposed"
    session.add(decision)
    record_audit_event(
        session,
        entity_type="ArchitectureDecision",
        entity_id=decision.id,
        action="propose",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(decision)
    return decision
