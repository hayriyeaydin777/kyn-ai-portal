import json
import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.code_review import CodeReviewRun
from app.schemas.code_review import CodeReviewCreate, CodeReviewRead
from app.services.citation_validator import UnsupportedClaimError, validate_citations
from app.services.code_review_checks import run_all_checks
from app.services.code_review_narrative import available_fields, generate_summary

router = APIRouter(prefix="/v1/code-reviews", tags=["code-reviews"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _run_to_read(run: CodeReviewRun) -> CodeReviewRead:
    return CodeReviewRead(
        id=run.id,
        source_snippet=run.source_snippet,
        language=run.language,
        findings=json.loads(run.findings),
        provider=run.provider,
        summary=run.summary,
        citations=run.citations.split(",") if run.citations else [],
        status=run.status,
        created_at=run.created_at,
    )


@router.get("", response_model=list[CodeReviewRead])
def list_code_reviews(session: Session = Depends(get_session)) -> list[CodeReviewRead]:
    runs = session.exec(select(CodeReviewRun)).all()
    return [_run_to_read(r) for r in runs]


@router.post("", response_model=CodeReviewRead, status_code=201)
def create_code_review(
    payload: CodeReviewCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> CodeReviewRead:
    findings = run_all_checks(payload.source_snippet)

    try:
        summary, citations, provider_name = generate_summary(findings)
    except NotImplementedError as exc:
        raise problem(501, "Not Implemented", str(exc)) from exc

    try:
        validate_citations(citations, available_fields(findings))
    except UnsupportedClaimError as exc:
        raise problem(422, "Unsupported Claim", str(exc)) from exc

    run = CodeReviewRun(
        source_snippet=payload.source_snippet,
        language=payload.language,
        findings=json.dumps(
            [{"rule_id": f.rule_id, "severity": f.severity, "message": f.message, "line": f.line} for f in findings]
        ),
        provider=provider_name,
        summary=summary,
        citations=",".join(citations),
        status="draft",
    )
    session.add(run)
    session.flush()

    record_audit_event(
        session,
        entity_type="CodeReviewRun",
        entity_id=run.id,
        action="create",
        correlation_id=_correlation_id(request),
        detail=f"{len(findings)} findings",
    )
    session.commit()
    session.refresh(run)
    return _run_to_read(run)


@router.get("/{review_id}", response_model=CodeReviewRead)
def get_code_review(review_id: uuid.UUID, session: Session = Depends(get_session)) -> CodeReviewRead:
    run = session.get(CodeReviewRun, review_id)
    if run is None:
        raise problem(404, "Not Found", f"Code review {review_id} not found")
    return _run_to_read(run)
