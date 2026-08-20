from fastapi.testclient import TestClient


def _create_application(client: TestClient, name: str = "Northstar Claims Service") -> str:
    response = client.post("/v1/applications", json={"name": name, "criticality": "high"})
    return response.json()["id"]


def test_generate_brief_uses_fake_provider_by_default(client: TestClient):
    app_id = _create_application(client)

    response = client.post(f"/v1/applications/{app_id}/briefs")

    assert response.status_code == 201
    body = response.json()
    assert body["provider"] == "fake"
    assert body["status"] == "draft"
    assert "Northstar Claims Service" in body["text"]
    assert len(body["citations"]) > 0


def test_generate_brief_missing_application_returns_404(client: TestClient):
    response = client.post("/v1/applications/00000000-0000-0000-0000-000000000000/briefs")
    assert response.status_code == 404


def test_list_briefs_returns_generated_brief(client: TestClient):
    app_id = _create_application(client)
    client.post(f"/v1/applications/{app_id}/briefs")

    response = client.get(f"/v1/applications/{app_id}/briefs")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_approve_brief_changes_status(client: TestClient):
    app_id = _create_application(client)
    brief = client.post(f"/v1/applications/{app_id}/briefs").json()

    response = client.post(
        f"/v1/applications/{app_id}/briefs/{brief['id']}/approvals", json={"decision": "approve"}
    )

    assert response.status_code == 201
    assert response.json()["status"] == "approved"


def test_reject_brief_changes_status(client: TestClient):
    app_id = _create_application(client)
    brief = client.post(f"/v1/applications/{app_id}/briefs").json()

    response = client.post(
        f"/v1/applications/{app_id}/briefs/{brief['id']}/approvals", json={"decision": "reject"}
    )

    assert response.status_code == 201
    assert response.json()["status"] == "rejected"


def test_approve_missing_brief_returns_404(client: TestClient):
    app_id = _create_application(client)

    response = client.post(
        f"/v1/applications/{app_id}/briefs/00000000-0000-0000-0000-000000000000/approvals",
        json={"decision": "approve"},
    )

    assert response.status_code == 404


def test_invalid_decision_rejected(client: TestClient):
    app_id = _create_application(client)
    brief = client.post(f"/v1/applications/{app_id}/briefs").json()

    response = client.post(
        f"/v1/applications/{app_id}/briefs/{brief['id']}/approvals", json={"decision": "maybe"}
    )

    assert response.status_code == 422
