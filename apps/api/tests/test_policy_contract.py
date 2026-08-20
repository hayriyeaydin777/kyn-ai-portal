"""Contract tests for the FastAPI <-> policy-service integration boundary.

These tests pin the exact JSON shape both sides agree on (PolicyRequestV1 /
PolicyResponseV1 in services/policy-service/Contracts) without requiring the
.NET service to be running.
"""

import httpx
import pytest

from app.clients.policy_client import PolicyClient, PolicyServiceError


class _FakeResponse:
    def __init__(self, status_code: int, json_body: dict | None = None, text: str = ""):
        self.status_code = status_code
        self._json_body = json_body or {}
        self.text = text

    def json(self):
        return self._json_body


def test_evaluate_sends_expected_request_shape(monkeypatch: pytest.MonkeyPatch):
    captured = {}

    def fake_post(url, json, timeout):
        captured["url"] = url
        captured["json"] = json
        return _FakeResponse(200, {"findings": []})

    monkeypatch.setattr(httpx, "post", fake_post)

    client = PolicyClient(base_url="http://policy-service")
    payload = {
        "applicationName": "Northstar Claims Service",
        "criticality": "high",
        "dependencies": [
            {"name": "Synthetic Identity Provider", "dependencyType": "auth", "criticality": "medium"}
        ],
    }
    client.evaluate(payload)

    assert captured["url"] == "http://policy-service/v1/assessments/evaluate"
    assert set(captured["json"].keys()) == {"applicationName", "criticality", "dependencies"}
    dependency = captured["json"]["dependencies"][0]
    assert set(dependency.keys()) == {"name", "dependencyType", "criticality"}


def test_evaluate_parses_expected_response_shape(monkeypatch: pytest.MonkeyPatch):
    response_body = {
        "findings": [
            {
                "ruleId": "R002",
                "severity": "High",
                "message": "Application criticality is 'high' but no failover dependency is documented.",
                "evidenceFields": ["Criticality", "Dependencies"],
            }
        ]
    }

    monkeypatch.setattr(httpx, "post", lambda url, json, timeout: _FakeResponse(200, response_body))

    client = PolicyClient(base_url="http://policy-service")
    result = client.evaluate({"applicationName": "x", "criticality": "high", "dependencies": []})

    assert result == response_body
    finding = result["findings"][0]
    assert set(finding.keys()) == {"ruleId", "severity", "message", "evidenceFields"}


def test_evaluate_raises_on_unreachable_service(monkeypatch: pytest.MonkeyPatch):
    def fake_post(url, json, timeout):
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(httpx, "post", fake_post)

    client = PolicyClient(base_url="http://policy-service")
    with pytest.raises(PolicyServiceError):
        client.evaluate({"applicationName": "x", "criticality": "low", "dependencies": []})


def test_evaluate_raises_on_server_error(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        httpx, "post", lambda url, json, timeout: _FakeResponse(500, text="internal error")
    )

    client = PolicyClient(base_url="http://policy-service")
    with pytest.raises(PolicyServiceError):
        client.evaluate({"applicationName": "x", "criticality": "low", "dependencies": []})
