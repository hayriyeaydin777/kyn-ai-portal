from fastapi.testclient import TestClient


def _create_decision(client: TestClient) -> str:
    response = client.post(
        "/v1/architecture-decisions",
        json={
            "title": "Adopt event-driven messaging",
            "context": "Fictional context.",
            "drivers": "Fictional drivers.",
            "decision": "Fictional decision.",
            "consequences": "Fictional consequences.",
        },
    )
    return response.json()["id"]


def test_create_decision_returns_201_with_generated_alternatives(client: TestClient):
    response = client.post(
        "/v1/architecture-decisions",
        json={
            "title": "x",
            "context": "y",
            "drivers": "z",
            "decision": "d",
            "consequences": "",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "draft"
    assert "Alternatives:" in body["alternatives"]


def test_update_while_draft_is_allowed(client: TestClient):
    decision_id = _create_decision(client)

    response = client.patch(f"/v1/architecture-decisions/{decision_id}", json={"consequences": "Updated."})
    assert response.status_code == 200
    assert response.json()["consequences"] == "Updated."


def test_edit_after_accepted_returns_409(client: TestClient):
    decision_id = _create_decision(client)
    client.post(f"/v1/architecture-decisions/{decision_id}/propose")
    client.post(f"/v1/architecture-decisions/{decision_id}/accept")

    response = client.patch(f"/v1/architecture-decisions/{decision_id}", json={"consequences": "Nope."})
    assert response.status_code == 409


def test_propose_from_wrong_status_returns_409(client: TestClient):
    decision_id = _create_decision(client)
    client.post(f"/v1/architecture-decisions/{decision_id}/propose")

    response = client.post(f"/v1/architecture-decisions/{decision_id}/propose")
    assert response.status_code == 409


def test_accept_requires_proposed_status(client: TestClient):
    decision_id = _create_decision(client)

    response = client.post(f"/v1/architecture-decisions/{decision_id}/accept")
    assert response.status_code == 409


def test_reject_changes_status(client: TestClient):
    decision_id = _create_decision(client)
    client.post(f"/v1/architecture-decisions/{decision_id}/propose")

    response = client.post(f"/v1/architecture-decisions/{decision_id}/reject")
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"


def test_create_review_with_valid_scores(client: TestClient):
    decision_id = _create_decision(client)
    payload = {
        "business_alignment": 4,
        "security": 3,
        "privacy": 4,
        "reliability": 3,
        "performance": 4,
        "testability": 4,
        "operability": 3,
        "integration": 4,
        "data": 4,
        "cost": 3,
    }

    response = client.post(f"/v1/architecture-decisions/{decision_id}/reviews", json=payload)
    assert response.status_code == 201
    assert response.json()["security"] == 3


def test_create_review_rejects_out_of_range_score(client: TestClient):
    decision_id = _create_decision(client)
    payload = {
        "business_alignment": 6,
        "security": 3,
        "privacy": 4,
        "reliability": 3,
        "performance": 4,
        "testability": 4,
        "operability": 3,
        "integration": 4,
        "data": 4,
        "cost": 3,
    }

    response = client.post(f"/v1/architecture-decisions/{decision_id}/reviews", json=payload)
    assert response.status_code == 422


def test_review_missing_decision_returns_404(client: TestClient):
    response = client.get("/v1/architecture-decisions/00000000-0000-0000-0000-000000000000/reviews")
    assert response.status_code == 404
