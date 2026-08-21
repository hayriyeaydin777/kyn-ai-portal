import json
import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.data.modernization_options import match_options
from app.db import get_session
from app.errors import problem
from app.models.application import ApplicationProfile
from app.models.modernization_case import ModernizationCase
from app.models.modernization_recommendation import ModernizationRecommendation
from app.schemas.modernization_recommendation import ModernizationRecommendationRead
from app.services.citation_validator import UnsupportedClaimError, validate_citations
from app.services.modernization_narrative import available_fields, generate_narrative
from app.services.modernization_risk import ModernizationInput, assess_risk

router = APIRouter(
    prefix="/v1/applications/{application_id}/modernization-recommendations", tags=["modernization"]
)


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _get_application_or_404(session: Session, application_id: uuid.UUID) -> ApplicationProfile:
    profile = session.get(ApplicationProfile, application_id)
    if profile is None:
        raise problem(404, "Not Found", f"Application {application_id} not found")
    return profile


def _recommendation_to_read(rec: ModernizationRecommendation) -> ModernizationRecommendationRead:
    return ModernizationRecommendationRead(
        id=rec.id,
        application_id=rec.application_id,
        modernization_case_id=rec.modernization_case_id,
        complexity_score=rec.complexity_score,
        risk_signals=json.loads(rec.risk_signals),
        matched_option_ids=rec.matched_option_ids.split(",") if rec.matched_option_ids else [],
        provider=rec.provider,
        narrative=rec.narrative,
        citations=rec.citations.split(",") if rec.citations else [],
        status=rec.status,
        created_at=rec.created_at,
    )


@router.get("", response_model=list[ModernizationRecommendationRead])
def list_recommendations(
    application_id: uuid.UUID, session: Session = Depends(get_session)
) -> list[ModernizationRecommendationRead]:
    _get_application_or_404(session, application_id)
    statement = select(ModernizationRecommendation).where(
        ModernizationRecommendation.application_id == application_id
    )
    recs = session.exec(statement).all()
    return [_recommendation_to_read(r) for r in recs]


@router.post("", response_model=ModernizationRecommendationRead, status_code=201)
def create_recommendation(
    application_id: uuid.UUID,
    case_id: uuid.UUID,
    request: Request,
    session: Session = Depends(get_session),
) -> ModernizationRecommendationRead:
    _get_application_or_404(session, application_id)
    case = session.get(ModernizationCase, case_id)
    if case is None or case.application_id != application_id:
        raise problem(404, "Not Found", f"Modernization case {case_id} not found")

    modernization_input = ModernizationInput(
        technology_stack=case.technology_stack,
        hosting=case.hosting,
        release_process=case.release_process,
        scale=case.scale,
        pain_points=case.pain_points,
    )
    risk = assess_risk(modernization_input)
    options = match_options([s.rule_id for s in risk.signals])

    try:
        narrative, citations, provider_name = generate_narrative(modernization_input, risk, options)
    except NotImplementedError as exc:
        raise problem(501, "Not Implemented", str(exc)) from exc

    try:
        validate_citations(citations, available_fields(modernization_input, risk))
    except UnsupportedClaimError as exc:
        raise problem(422, "Unsupported Claim", str(exc)) from exc

    recommendation = ModernizationRecommendation(
        application_id=application_id,
        modernization_case_id=case_id,
        complexity_score=risk.complexity_score,
        risk_signals=json.dumps([{"rule_id": s.rule_id, "severity": s.severity, "message": s.message} for s in risk.signals]),
        matched_option_ids=",".join(o.option_id for o in options),
        provider=provider_name,
        narrative=narrative,
        citations=",".join(citations),
        status="draft",
    )
    session.add(recommendation)
    session.flush()

    record_audit_event(
        session,
        entity_type="ModernizationRecommendation",
        entity_id=recommendation.id,
        action="create",
        correlation_id=_correlation_id(request),
        detail=f"application_id={application_id},case_id={case_id}",
    )
    session.commit()
    session.refresh(recommendation)
    return _recommendation_to_read(recommendation)
