import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.approval import ApprovalDecision
from app.models.brief import Brief
from app.schemas.approval import ApprovalDecisionCreate
from app.schemas.brief import BriefRead, brief_to_read

router = APIRouter(prefix="/v1/applications/{application_id}/briefs/{brief_id}/approvals", tags=["approvals"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


@router.post("", response_model=BriefRead, status_code=201)
def decide_brief(
    application_id: uuid.UUID,
    brief_id: uuid.UUID,
    payload: ApprovalDecisionCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> BriefRead:
    brief = session.get(Brief, brief_id)
    if brief is None or brief.application_id != application_id:
        raise problem(404, "Not Found", f"Brief {brief_id} not found for application {application_id}")

    brief.status = "approved" if payload.decision == "approve" else "rejected"
    session.add(brief)

    decision = ApprovalDecision(
        entity_type="Brief",
        entity_id=brief_id,
        decision=payload.decision,
        correlation_id=_correlation_id(request),
    )
    session.add(decision)

    record_audit_event(
        session,
        entity_type="Brief",
        entity_id=brief_id,
        action=payload.decision,
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(brief)
    return brief_to_read(brief)
