import json
import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.data.agent_tool_catalog import validate_tools
from app.db import get_session
from app.errors import problem
from app.models.agent_definition import AgentDefinition
from app.models.agent_version import AgentVersion
from app.schemas.agent_version import AgentVersionCreate, AgentVersionRead

router = APIRouter(prefix="/v1/agents/{agent_id}/versions", tags=["agent-versions"])

# Allowed forward transitions. Lifecycle is a strict state machine (ADR-011).
_TRANSITIONS = {
    "draft": "evaluation",
    "evaluation": "review",
    "review": "approved",
    "approved": "deprecated",
    "deprecated": "retired",
}


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


def _get_agent_or_404(session: Session, agent_id: uuid.UUID) -> AgentDefinition:
    agent = session.get(AgentDefinition, agent_id)
    if agent is None:
        raise problem(404, "Not Found", f"Agent {agent_id} not found")
    return agent


def _to_read(version: AgentVersion) -> AgentVersionRead:
    return AgentVersionRead(
        id=version.id,
        agent_id=version.agent_id,
        version=version.version,
        prompt_version=version.prompt_version,
        input_schema=version.input_schema,
        output_schema=version.output_schema,
        allowed_tools=json.loads(version.allowed_tools),
        status=version.status,
        created_at=version.created_at,
    )


@router.get("", response_model=list[AgentVersionRead])
def list_versions(agent_id: uuid.UUID, session: Session = Depends(get_session)) -> list[AgentVersionRead]:
    _get_agent_or_404(session, agent_id)
    statement = select(AgentVersion).where(AgentVersion.agent_id == agent_id)
    return [_to_read(v) for v in session.exec(statement).all()]


@router.post("", response_model=AgentVersionRead, status_code=201)
def create_version(
    agent_id: uuid.UUID,
    payload: AgentVersionCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> AgentVersionRead:
    _get_agent_or_404(session, agent_id)

    unknown = validate_tools(payload.allowed_tools)
    if unknown:
        raise problem(422, "Unknown Tool", f"Tool(s) not in allowlist catalog: {', '.join(unknown)}")

    existing_count = len(
        session.exec(select(AgentVersion).where(AgentVersion.agent_id == agent_id)).all()
    )

    version = AgentVersion(
        agent_id=agent_id,
        version=existing_count + 1,
        prompt_version=payload.prompt_version,
        input_schema=payload.input_schema,
        output_schema=payload.output_schema,
        allowed_tools=json.dumps(payload.allowed_tools),
        status="draft",
    )
    session.add(version)
    session.flush()

    record_audit_event(
        session,
        entity_type="AgentVersion",
        entity_id=version.id,
        action="create",
        correlation_id=_correlation_id(request),
        detail=f"agent_id={agent_id}",
    )
    session.commit()
    session.refresh(version)
    return _to_read(version)


@router.post("/{version_id}/advance", response_model=AgentVersionRead)
def advance_version(
    agent_id: uuid.UUID,
    version_id: uuid.UUID,
    request: Request,
    session: Session = Depends(get_session),
) -> AgentVersionRead:
    _get_agent_or_404(session, agent_id)
    version = session.get(AgentVersion, version_id)
    if version is None or version.agent_id != agent_id:
        raise problem(404, "Not Found", f"Agent version {version_id} not found")

    next_status = _TRANSITIONS.get(version.status)
    if next_status is None:
        raise problem(409, "Conflict", f"No forward transition from status '{version.status}'.")

    version.status = next_status
    session.add(version)
    record_audit_event(
        session,
        entity_type="AgentVersion",
        entity_id=version.id,
        action=f"advance_to_{next_status}",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(version)
    return _to_read(version)
