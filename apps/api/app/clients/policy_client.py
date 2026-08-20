from typing import Any

import httpx

from app.config import settings


class PolicyServiceError(Exception):
    """Raised when the policy service is unreachable or returns an error."""


class PolicyClient:
    def __init__(self, base_url: str | None = None, timeout: float = 5.0) -> None:
        self._base_url = base_url or settings.policy_service_url
        self._timeout = timeout

    def evaluate(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            response = httpx.post(
                f"{self._base_url}/v1/assessments/evaluate",
                json=payload,
                timeout=self._timeout,
            )
        except httpx.RequestError as exc:
            raise PolicyServiceError(f"Policy service unreachable: {exc}") from exc

        if response.status_code >= 500:
            raise PolicyServiceError(f"Policy service returned {response.status_code}")
        if response.status_code >= 400:
            raise PolicyServiceError(f"Policy service rejected request: {response.text}")

        return response.json()
