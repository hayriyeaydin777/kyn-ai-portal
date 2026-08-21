from app.config import settings

_STANDARD_ALTERNATIVES = [
    (
        "Do nothing (status quo)",
        "No implementation cost, but drivers/pain points remain unaddressed.",
    ),
    (
        "Incremental change within current architecture",
        "Lower risk and cost than a rewrite; may not fully resolve structural drivers.",
    ),
    (
        "Larger structural change (new component/service boundary)",
        "Directly addresses drivers; higher upfront cost and migration risk.",
    ),
]


def available_fields() -> set[str]:
    return {f"alternatives[{i}].name" for i in range(len(_STANDARD_ALTERNATIVES))}


def draft_alternatives(context: str, drivers: str) -> tuple[str, list[str], str]:
    """Deterministic, reviewable alternatives — same 3 generic options every time, not fabricated per input."""
    if settings.ai_provider == "claude":
        raise NotImplementedError(
            "AI_PROVIDER=claude requires the Claude provider adapter (deferred, see S4-10)."
        )
    if settings.ai_provider != "fake":
        raise ValueError(f"Unknown AI_PROVIDER: {settings.ai_provider}")

    lines = [f"Context: {context}", f"Drivers: {drivers}", "", "Alternatives:"]
    citations: list[str] = []
    for i, (name, tradeoff) in enumerate(_STANDARD_ALTERNATIVES):
        lines.append(f"{i + 1}. {name} — {tradeoff}")
        citations.append(f"alternatives[{i}].name")

    return "\n".join(lines), citations, "fake"
