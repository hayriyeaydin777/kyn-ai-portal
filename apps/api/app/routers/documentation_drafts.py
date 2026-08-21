import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.documentation_draft import DocumentationDraft
from app.schemas.documentation_draft import DocumentationDraftCreate, DocumentationDraftRead
from app.services.documentation_generator import generate_documentation

router = APIRouter(prefix="/v1/documentation-drafts", tags=["documentation-drafts"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


@router.get("", response_model=list[DocumentationDraftRead])
def list_documentation_drafts(session: Session = Depends(get_session)) -> list[DocumentationDraft]:
    return list(session.exec(select(DocumentationDraft)).all())


@router.post("", response_model=DocumentationDraftRead, status_code=201)
def create_documentation_draft(
    payload: DocumentationDraftCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> DocumentationDraft:
    draft_text = generate_documentation(payload.source_snippet)

    draft = DocumentationDraft(
        source_snippet=payload.source_snippet,
        draft_text=draft_text,
        version=1,
        status="draft",
    )
    session.add(draft)
    session.flush()

    record_audit_event(
        session,
        entity_type="DocumentationDraft",
        entity_id=draft.id,
        action="create",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(draft)
    return draft


@router.get("/{draft_id}", response_model=DocumentationDraftRead)
def get_documentation_draft(draft_id: uuid.UUID, session: Session = Depends(get_session)) -> DocumentationDraft:
    draft = session.get(DocumentationDraft, draft_id)
    if draft is None:
        raise problem(404, "Not Found", f"Documentation draft {draft_id} not found")
    return draft
