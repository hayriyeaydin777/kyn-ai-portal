from app.providers.base import BriefResponse, LLMProvider
from app.services.evidence_bundle import EvidenceBundle


class FakeProvider(LLMProvider):
    """Deterministic, template-based provider. No network calls, no tokens spent."""

    name = "fake"

    def generate(self, prompt: str, evidence: EvidenceBundle) -> BriefResponse:
        lines: list[str] = []
        citations: list[str] = []

        app = evidence.application
        lines.append(f"Application: {app['name']} (criticality: {app['criticality']}).")
        citations.append("application.name")
        citations.append("application.criticality")

        if app.get("description"):
            lines.append(app["description"])
            citations.append("application.description")

        if evidence.dependencies:
            names = ", ".join(d["name"] for d in evidence.dependencies)
            lines.append(f"Dependencies: {names}.")
            citations.extend(f"dependencies[{i}].name" for i in range(len(evidence.dependencies)))
        else:
            lines.append("No dependencies documented.")

        if evidence.findings:
            for i, finding in enumerate(evidence.findings):
                lines.append(f"Finding {finding['rule_id']} ({finding['severity']}): {finding['message']}")
                citations.append(f"findings[{i}].message")
        else:
            lines.append("No findings recorded yet.")

        return BriefResponse(text="\n".join(lines), citations=citations)
