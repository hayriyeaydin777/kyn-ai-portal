# Deny-by-default: an AgentVersion may only declare tools from this catalog.
# These names map to already-built deterministic capabilities (Stages 3, 5, 6),
# not a live dynamic-dispatch runtime (see DEFERRED-ENHANCEMENTS.md).
ALLOWED_TOOLS = frozenset(
    {
        "read_evidence",
        "run_deterministic_assessment",
        "run_modernization_risk_model",
        "run_code_review_checks",
        "generate_test_skeleton",
        "generate_documentation_draft",
        "generate_fake_brief",
    }
)


def validate_tools(tools: list[str]) -> list[str]:
    """Returns the unknown tool names (empty list means all tools are allowlisted)."""
    return [t for t in tools if t not in ALLOWED_TOOLS]
