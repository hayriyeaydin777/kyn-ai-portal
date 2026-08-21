import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.diagram_metadata import DiagramMetadata
from app.schemas.diagram_metadata import DiagramMetadataCreate, DiagramMetadataRead

router = APIRouter(prefix="/v1/diagrams", tags=["diagrams"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _to_read(diagram: DiagramMetadata) -> DiagramMetadataRead:
    return DiagramMetadataRead(
        id=diagram.id,
        title=diagram.title,
        description=diagram.description,
        scope=diagram.scope,
        version=diagram.version,
        linked_decision_ids=diagram.linked_decision_ids.split(",") if diagram.linked_decision_ids else [],
        created_at=diagram.created_at,
    )


@router.get("", response_model=list[DiagramMetadataRead])
def list_diagrams(session: Session = Depends(get_session)) -> list[DiagramMetadataRead]:
    diagrams = session.exec(select(DiagramMetadata)).all()
    return [_to_read(d) for d in diagrams]


@router.post("", response_model=DiagramMetadataRead, status_code=201)
def create_diagram(
    payload: DiagramMetadataCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> DiagramMetadataRead:
    diagram = DiagramMetadata(
        title=payload.title,
        description=payload.description,
        scope=payload.scope,
        version=1,
        linked_decision_ids=",".join(payload.linked_decision_ids),
    )
    session.add(diagram)
    session.flush()

    record_audit_event(
        session,
        entity_type="DiagramMetadata",
        entity_id=diagram.id,
        action="create",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(diagram)
    return _to_read(diagram)


@router.get("/{diagram_id}", response_model=DiagramMetadataRead)
def get_diagram(diagram_id: uuid.UUID, session: Session = Depends(get_session)) -> DiagramMetadataRead:
    diagram = session.get(DiagramMetadata, diagram_id)
    if diagram is None:
        raise problem(404, "Not Found", f"Diagram {diagram_id} not found")
    return _to_read(diagram)
