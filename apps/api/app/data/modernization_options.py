from dataclasses import dataclass


@dataclass(frozen=True)
class ModernizationOption:
    option_id: str
    name: str
    description: str
    tradeoffs: str
    addresses_rule_ids: tuple[str, ...]


# Versioned, reviewable catalog — not AI-generated. Bump CATALOG_VERSION on any change.
CATALOG_VERSION = "1.0"

MODERNIZATION_OPTIONS: tuple[ModernizationOption, ...] = (
    ModernizationOption(
        option_id="O001",
        name="Automate CI/CD pipeline",
        description="Replace manual release steps with an automated build/test/deploy pipeline.",
        tradeoffs="Upfront pipeline investment; requires test coverage to be trustworthy.",
        addresses_rule_ids=("M001", "M003"),
    ),
    ModernizationOption(
        option_id="O002",
        name="Migrate to cloud-hosted infrastructure",
        description="Move from on-premises hosting to a cloud provider for elastic scale.",
        tradeoffs="Migration effort and cost; requires network/security re-architecture.",
        addresses_rule_ids=("M002",),
    ),
    ModernizationOption(
        option_id="O003",
        name="Introduce observability and incident response tooling",
        description="Add monitoring, alerting, and runbooks to reduce outage duration and frequency.",
        tradeoffs="Ongoing tooling cost; requires team process changes.",
        addresses_rule_ids=("M004",),
    ),
)


def match_options(rule_ids: list[str]) -> list[ModernizationOption]:
    """Deterministic lookup — no AI. Returns catalog options addressing any of the given rule ids."""
    matched = [
        option for option in MODERNIZATION_OPTIONS if any(rid in option.addresses_rule_ids for rid in rule_ids)
    ]
    return matched
