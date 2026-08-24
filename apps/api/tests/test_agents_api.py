from fastapi.testclient import TestClient


def _create_agent(client: TestClient, name: str = "Modernization Advisor Agent") -> str:
    response = client.post(
        "/v1/agents",
        json={
            "name": name,
            "purpose": "Fictional demo purpose.",
            "owner": "Demo Owner",
            "security_tier": "medium",
        },
    )
    return response.json()["id"]


def test_create_agent_returns_201(client: TestClient):
    response = client.post(
        "/v1/agents",
        json={"name": "x", "purpose": "y", "owner": "z", "security_tier": "low"},
    )
    assert response.status_code == 201
    assert response.json()["lifecycle_status"] == "draft"


def test_get_missing_agent_returns_404(client: TestClient):
    response = client.get("/v1/agents/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_create_version_with_allowlisted_tools_returns_201(client: TestClient):
    agent_id = _create_agent(client)

    response = client.post(
        f"/v1/agents/{agent_id}/versions",
        json={
            "prompt_version": "v1",
            "input_schema": "{}",
            "output_schema": "{}",
            "allowed_tools": ["read_evidence", "run_deterministic_assessment"],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["version"] == 1
    assert body["status"] == "draft"


def test_create_version_with_unknown_tool_returns_422(client: TestClient):
    agent_id = _create_agent(client)

    response = client.post(
        f"/v1/agents/{agent_id}/versions",
        json={
            "prompt_version": "v1",
            "input_schema": "{}",
            "output_schema": "{}",
            "allowed_tools": ["delete_production_database"],
        },
    )
    assert response.status_code == 422


def test_create_version_missing_agent_returns_404(client: TestClient):
    response = client.post(
        "/v1/agents/00000000-0000-0000-0000-000000000000/versions",
        json={"prompt_version": "v1", "input_schema": "{}", "output_schema": "{}", "allowed_tools": []},
    )
    assert response.status_code == 404


def test_advance_moves_through_lifecycle(client: TestClient):
    agent_id = _create_agent(client)
    version = client.post(
        f"/v1/agents/{agent_id}/versions",
        json={"prompt_version": "v1", "input_schema": "{}", "output_schema": "{}", "allowed_tools": []},
    ).json()

    for expected in ["evaluation", "review", "approved", "deprecated", "retired"]:
        response = client.post(f"/v1/agents/{agent_id}/versions/{version['id']}/advance")
        assert response.status_code == 200
        assert response.json()["status"] == expected


def test_advance_from_retired_returns_409(client: TestClient):
    agent_id = _create_agent(client)
    version = client.post(
        f"/v1/agents/{agent_id}/versions",
        json={"prompt_version": "v1", "input_schema": "{}", "output_schema": "{}", "allowed_tools": []},
    ).json()

    for _ in range(5):
        client.post(f"/v1/agents/{agent_id}/versions/{version['id']}/advance")

    response = client.post(f"/v1/agents/{agent_id}/versions/{version['id']}/advance")
    assert response.status_code == 409


def test_list_versions_returns_created_version(client: TestClient):
    agent_id = _create_agent(client)
    client.post(
        f"/v1/agents/{agent_id}/versions",
        json={"prompt_version": "v1", "input_schema": "{}", "output_schema": "{}", "allowed_tools": []},
    )

    response = client.get(f"/v1/agents/{agent_id}/versions")
    assert response.status_code == 200
    assert len(response.json()) == 1
