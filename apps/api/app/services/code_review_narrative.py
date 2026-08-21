from app.config import settings
from app.services.code_review_checks import CodeFinding


def available_fields(findings: list[CodeFinding]) -> set[str]:
    return {f"findings[{i}].message" for i in range(len(findings))}


def generate_summary(findings: list[CodeFinding]) -> tuple[str, list[str], str]:
    """Returns (summary_text, citations, provider_name). Deterministic, zero tokens by default."""
    if settings.ai_provider == "claude":
        raise NotImplementedError(
            "AI_PROVIDER=claude requires the Claude provider adapter (deferred, see S4-10)."
        )
    if settings.ai_provider != "fake":
        raise ValueError(f"Unknown AI_PROVIDER: {settings.ai_provider}")

    if not findings:
        return "No issues found by the deterministic checks.", [], "fake"

    lines = [f"{len(findings)} finding(s) identified:"]
    citations: list[str] = []
    for i, finding in enumerate(findings):
        lines.append(f"- [{finding.rule_id}] ({finding.severity}) {finding.message}")
        citations.append(f"findings[{i}].message")

    return "\n".join(lines), citations, "fake"
