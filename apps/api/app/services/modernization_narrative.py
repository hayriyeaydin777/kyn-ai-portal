from app.config import settings
from app.data.modernization_options import ModernizationOption
from app.services.modernization_risk import ModernizationInput, RiskAssessment


def available_fields(case: ModernizationInput, risk: RiskAssessment) -> set[str]:
    fields = {f"case.{f}" for f in ("technology_stack", "hosting", "release_process", "scale", "pain_points")}
    fields.update(f"risk_signals[{i}].message" for i in range(len(risk.signals)))
    return fields


def generate_narrative(
    case: ModernizationInput, risk: RiskAssessment, options: list[ModernizationOption]
) -> tuple[str, list[str], str]:
    """Returns (narrative_text, citations, provider_name). Fake provider is deterministic, zero tokens."""
    if settings.ai_provider == "claude":
        raise NotImplementedError(
            "AI_PROVIDER=claude requires the Claude provider adapter (deferred, see S4-10)."
        )
    if settings.ai_provider != "fake":
        raise ValueError(f"Unknown AI_PROVIDER: {settings.ai_provider}")

    lines: list[str] = []
    citations: list[str] = []

    lines.append(f"Current state: {case.technology_stack}, hosted on {case.hosting}.")
    citations.extend(["case.technology_stack", "case.hosting"])

    lines.append(f"Release process: {case.release_process}. Scale: {case.scale}.")
    citations.extend(["case.release_process", "case.scale"])

    if risk.signals:
        for i, signal in enumerate(risk.signals):
            lines.append(f"Risk ({signal.severity}): {signal.message}")
            citations.append(f"risk_signals[{i}].message")
    else:
        lines.append("No deterministic risk signals identified.")

    if options:
        names = ", ".join(o.name for o in options)
        lines.append(f"Recommended target-state options: {names}.")
    else:
        lines.append("No catalog options matched the identified risks.")

    return "\n".join(lines), citations, "fake"
