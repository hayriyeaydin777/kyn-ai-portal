from fastapi.testclient import TestClient


def _create_application(client: TestClient, name: str = "Northstar Claims Service") -> str:
    response = client.post("/v1/applications", json={"name": name})
    return response.json()["id"]


def test_create_dependency_returns_201(client: TestClient):
    app_id = _create_application(client)
    response = client.post(
        f"/v1/applications/{app_id}/dependencies",
        json={"name": "Synthetic Identity Provider", "dependency_type": "auth"},
    )
    assert response.status_code == 201
    assert response.json()["application_id"] == app_id


def test_create_dependency_for_missing_application_returns_404(client: TestClient):
    response = client.post(
        "/v1/applications/00000000-0000-0000-0000-000000000000/dependencies",
        json={"name": "x", "dependency_type": "y"},
    )
    assert response.status_code == 404


def test_create_evidence_returns_201(client: TestClient):
    app_id = _create_application(client)
    response = client.post(
        f"/v1/applications/{app_id}/evidence",
        json={"title": "Synthetic architecture diagram", "source": "demo-doc"},
    )
    assert response.status_code == 201
    assert response.json()["application_id"] == app_id


def test_list_dependencies_for_missing_application_returns_404(client: TestClient):
    response = client.get("/v1/applications/00000000-0000-0000-0000-000000000000/dependencies")
    assert response.status_code == 404
