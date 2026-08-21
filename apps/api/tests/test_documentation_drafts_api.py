from fastapi.testclient import TestClient


def test_create_documentation_draft_returns_201(client: TestClient):
    response = client.post(
        "/v1/documentation-drafts",
        json={"source_snippet": 'def add(a, b):\n    """Adds."""\n    return a + b\n'},
    )
    assert response.status_code == 201
    body = response.json()
    assert "Adds." in body["draft_text"]
    assert body["version"] == 1


def test_get_missing_documentation_draft_returns_404(client: TestClient):
    response = client.get("/v1/documentation-drafts/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_documentation_drafts_returns_created_draft(client: TestClient):
    client.post("/v1/documentation-drafts", json={"source_snippet": "def f():\n    pass\n"})

    response = client.get("/v1/documentation-drafts")
    assert response.status_code == 200
    assert len(response.json()) == 1
