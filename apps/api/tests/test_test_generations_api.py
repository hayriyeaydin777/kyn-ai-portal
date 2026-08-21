from fastapi.testclient import TestClient


def test_create_test_generation_returns_201(client: TestClient):
    response = client.post(
        "/v1/test-generations",
        json={"source_snippet": "def add(a, b):\n    return a + b\n"},
    )
    assert response.status_code == 201
    assert "test_add_happy_path" in response.json()["generated_tests"]


def test_get_missing_test_generation_returns_404(client: TestClient):
    response = client.get("/v1/test-generations/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_test_generations_returns_created_suite(client: TestClient):
    client.post("/v1/test-generations", json={"source_snippet": "def f(x):\n    return x\n"})

    response = client.get("/v1/test-generations")
    assert response.status_code == 200
    assert len(response.json()) == 1
