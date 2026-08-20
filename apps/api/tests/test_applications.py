from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models.audit import AuditEvent


def test_create_application_returns_201(client: TestClient):
    response = client.post(
        "/v1/applications",
        json={"name": "Northstar Claims Service", "criticality": "high"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Northstar Claims Service"
    assert body["criticality"] == "high"


def test_create_duplicate_application_returns_409(client: TestClient):
    payload = {"name": "Aurora Customer Portal"}
    first = client.post("/v1/applications", json=payload)
    assert first.status_code == 201

    second = client.post("/v1/applications", json=payload)
    assert second.status_code == 409
    assert second.json()["detail"]["title"] == "Conflict"


def test_get_missing_application_returns_404(client: TestClient):
    response = client.get("/v1/applications/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_applications_returns_created_entries(client: TestClient):
    client.post("/v1/applications", json={"name": "Atlas Messaging Service"})
    response = client.get("/v1/applications")
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert "Atlas Messaging Service" in names


def test_update_application_bumps_updated_at(client: TestClient):
    created = client.post("/v1/applications", json={"name": "Synthetic Identity Provider"})
    app_id = created.json()["id"]

    updated = client.patch(f"/v1/applications/{app_id}", json={"criticality": "critical"})
    assert updated.status_code == 200
    assert updated.json()["criticality"] == "critical"


def test_create_application_writes_audit_event(client: TestClient, session: Session):
    response = client.post("/v1/applications", json={"name": "Northstar Claims Service"})
    app_id = response.json()["id"]

    events = session.exec(select(AuditEvent).where(AuditEvent.entity_type == "ApplicationProfile")).all()
    assert any(str(e.entity_id) == app_id and e.action == "create" for e in events)


def test_invalid_criticality_rejected(client: TestClient):
    response = client.post(
        "/v1/applications", json={"name": "Bad Criticality Corp", "criticality": "not-a-level"}
    )
    assert response.status_code == 422
