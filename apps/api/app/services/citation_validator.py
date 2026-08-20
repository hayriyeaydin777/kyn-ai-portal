class UnsupportedClaimError(Exception):
    """Raised when a brief cites a field not present in its evidence bundle."""


def validate_citations(citations: list[str], available_fields: set[str]) -> None:
    unsupported = [c for c in citations if c not in available_fields]
    if unsupported:
        raise UnsupportedClaimError(f"Unsupported citation(s): {', '.join(unsupported)}")
