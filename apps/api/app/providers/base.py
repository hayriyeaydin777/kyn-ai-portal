from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.evidence_bundle import EvidenceBundle


@dataclass
class BriefResponse:
    text: str
    citations: list[str] = field(default_factory=list)


class LLMProvider:
    """Seam every provider (fake or real) must implement. No vendor types leak past this interface."""

    name: str = "base"

    def generate(self, prompt: str, evidence: "EvidenceBundle") -> BriefResponse:
        raise NotImplementedError
