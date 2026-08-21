from fastapi.testclient import TestClient


def test_create_code_review_returns_201(client: TestClient):
    response = client.post(
        "/v1/code-reviews",
        json={"source_snippet": "def add(a, b):\n    return a + b\n"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["provider"] == "fake"
    assert body["status"] == "draft"


def test_get_missing_code_review_returns_404(client: TestClient):
    response = client.get("/v1/code-reviews/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_code_reviews_returns_created_run(client: TestClient):
    client.post("/v1/code-reviews", json={"source_snippet": "def f():\n    pass\n"})

    response = client.get("/v1/code-reviews")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_clean_source_produces_no_findings(client: TestClient):
    response = client.post(
        "/v1/code-reviews",
        json={"source_snippet": 'def f():\n    """Docstring."""\n    return 1\n'},
    )
    assert response.json()["findings"] == []
