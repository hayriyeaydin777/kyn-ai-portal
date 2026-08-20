from app.config import settings
from app.providers.base import LLMProvider
from app.providers.fake import FakeProvider


def get_provider() -> LLMProvider:
    if settings.ai_provider == "fake":
        return FakeProvider()
    if settings.ai_provider == "claude":
        raise NotImplementedError(
            "AI_PROVIDER=claude requires the Claude provider adapter (deferred, see S4-10)."
        )
    raise ValueError(f"Unknown AI_PROVIDER: {settings.ai_provider}")
