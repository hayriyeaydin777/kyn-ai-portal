from fastapi.testclient import TestClient


def _create_application(client: TestClient, name: str = "Northstar Claims Service") -> str:
    response = client.post("/v1/applications", json={"name": name, "criticality": "high"})
    return response.json()["id"]


def _create_case(client: TestClient, app_id: str) -> str:
    response = client.post(
        f"/v1/applications/{app_id}/modernization-cases",
        json={
            "technology_stack": "Fictional legacy monolith",
            "hosting": "on-premises data center",
            "release_process": "manual, quarterly releases",
            "scale": "large",
            "pain_points": "Frequent outages during peak load",
        },
    )
    return response.json()["id"]


def test_create_modernization_case_returns_201(client: TestClient):
    app_id = _create_application(client)

    response = client.post(
        f"/v1/applications/{app_id}/modernization-cases",
        json={
            "technology_stack": "Fictional monolith",
            "hosting": "cloud",
            "release_process": "automated",
            "scale": "small",
            "pain_points": "",
        },
    )

    assert response.status_code == 201
    assert response.json()["technology_stack"] == "Fictional monolith"


def test_create_case_missing_application_returns_404(client: TestClient):
    response = client.post(
        "/v1/applications/00000000-0000-0000-0000-000000000000/modernization-cases",
        json={"technology_stack": "x", "hosting": "x", "release_process": "x", "scale": "x", "pain_points": ""},
    )
    assert response.status_code == 404


def test_generate_recommendation_produces_expected_risk_signals(client: TestClient):
    app_id = _create_application(client)
    case_id = _create_case(client, app_id)

    response = client.post(f"/v1/applications/{app_id}/modernization-recommendations?case_id={case_id}")

    assert response.status_code == 201
    body = response.json()
    rule_ids = {s["rule_id"] for s in body["risk_signals"]}
    assert {"M001", "M002", "M003", "M004"}.issubset(rule_ids)
    assert body["provider"] == "fake"
    assert body["status"] == "draft"
    assert len(body["matched_option_ids"]) > 0
    assert len(body["citations"]) > 0


def test_generate_recommendation_missing_case_returns_404(client: TestClient):
    app_id = _create_application(client)

    response = client.post(
        f"/v1/applications/{app_id}/modernization-recommendations?"
        "case_id=00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404


def test_list_recommendations_returns_generated_recommendation(client: TestClient):
    app_id = _create_application(client)
    case_id = _create_case(client, app_id)
    client.post(f"/v1/applications/{app_id}/modernization-recommendations?case_id={case_id}")

    response = client.get(f"/v1/applications/{app_id}/modernization-recommendations")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_clean_input_produces_no_risk_signals(client: TestClient):
    app_id = _create_application(client)
    case_response = client.post(
        f"/v1/applications/{app_id}/modernization-cases",
        json={
            "technology_stack": "Fictional monolith",
            "hosting": "cloud",
            "release_process": "automated",
            "scale": "small",
            "pain_points": "",
        },
    )
    case_id = case_response.json()["id"]

    response = client.post(f"/v1/applications/{app_id}/modernization-recommendations?case_id={case_id}")

    assert response.status_code == 201
    assert response.json()["risk_signals"] == []
    assert response.json()["complexity_score"] == 0
