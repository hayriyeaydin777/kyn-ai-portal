from unittest.mock import patch

from fastapi.testclient import TestClient

from app.clients.policy_client import PolicyServiceError


def _create_application(client: TestClient, name: str = "Northstar Claims Service") -> str:
    response = client.post("/v1/applications", json={"name": name, "criticality": "high"})
    return response.json()["id"]


def test_evaluate_persists_findings_and_audit_event(client: TestClient):
    app_id = _create_application(client)

    fake_response = {
        "findings": [
            {
                "ruleId": "R002",
                "severity": "High",
                "message": "No failover documented.",
                "evidenceFields": ["Criticality"],
            }
        ]
    }
    with patch("app.routers.assessments.PolicyClient.evaluate", return_value=fake_response):
        response = client.post(f"/v1/applications/{app_id}/assessments")

    assert response.status_code == 201
    body = response.json()
    assert len(body) == 1
    assert body[0]["rule_id"] == "R002"
    assert body[0]["severity"] == "High"
    assert body[0]["evidence_fields"] == ["Criticality"]

    listed = client.get(f"/v1/applications/{app_id}/assessments")
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_evaluate_missing_application_returns_404(client: TestClient):
    response = client.post("/v1/applications/00000000-0000-0000-0000-000000000000/assessments")
    assert response.status_code == 404


def test_evaluate_policy_service_down_returns_503(client: TestClient):
    app_id = _create_application(client)

    with patch(
        "app.routers.assessments.PolicyClient.evaluate",
        side_effect=PolicyServiceError("connection refused"),
    ):
        response = client.post(f"/v1/applications/{app_id}/assessments")

    assert response.status_code == 503
    assert response.json()["detail"]["title"] == "Policy Service Unavailable"


def test_list_findings_missing_application_returns_404(client: TestClient):
    response = client.get("/v1/applications/00000000-0000-0000-0000-000000000000/assessments")
    assert response.status_code == 404
