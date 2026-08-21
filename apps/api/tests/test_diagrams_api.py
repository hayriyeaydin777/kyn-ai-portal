from fastapi.testclient import TestClient


def test_create_diagram_returns_201(client: TestClient):
    response = client.post(
        "/v1/diagrams",
        json={
            "title": "System context diagram",
            "description": "Fictional high-level context diagram.",
            "scope": "whole-system",
            "linked_decision_ids": ["11111111-1111-1111-1111-111111111111"],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["version"] == 1
    assert body["linked_decision_ids"] == ["11111111-1111-1111-1111-111111111111"]


def test_get_missing_diagram_returns_404(client: TestClient):
    response = client.get("/v1/diagrams/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_diagrams_returns_created_diagram(client: TestClient):
    client.post(
        "/v1/diagrams",
        json={"title": "Diagram", "description": "Desc", "scope": "module", "linked_decision_ids": []},
    )

    response = client.get("/v1/diagrams")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["linked_decision_ids"] == []
