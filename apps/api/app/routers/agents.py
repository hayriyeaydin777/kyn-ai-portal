import uuid

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.audit import record_audit_event
from app.db import get_session
from app.errors import problem
from app.models.agent_definition import AgentDefinition
from app.schemas.agent_definition import AgentDefinitionCreate, AgentDefinitionRead

router = APIRouter(prefix="/v1/agents", tags=["agents"])


def _correlation_id(request: Request) -> str | None:
    return getattr(request.state, "correlation_id", None)


@router.get("", response_model=list[AgentDefinitionRead])
def list_agents(session: Session = Depends(get_session)) -> list[AgentDefinition]:
    return list(session.exec(select(AgentDefinition)).all())


@router.post("", response_model=AgentDefinitionRead, status_code=201)
def create_agent(
    payload: AgentDefinitionCreate,
    request: Request,
    session: Session = Depends(get_session),
) -> AgentDefinition:
    agent = AgentDefinition(**payload.model_dump())
    session.add(agent)
    session.flush()

    record_audit_event(
        session,
        entity_type="AgentDefinition",
        entity_id=agent.id,
        action="create",
        correlation_id=_correlation_id(request),
    )
    session.commit()
    session.refresh(agent)
    return agent


@router.get("/{agent_id}", response_model=AgentDefinitionRead)
def get_agent(agent_id: uuid.UUID, session: Session = Depends(get_session)) -> AgentDefinition:
    agent = session.get(AgentDefinition, agent_id)
    if agent is None:
        raise problem(404, "Not Found", f"Agent {agent_id} not found")
    return agent
