from dataclasses import dataclass, field


@dataclass
class ModernizationInput:
    technology_stack: str
    hosting: str
    release_process: str
    scale: str
    pain_points: str


@dataclass
class RiskSignal:
    rule_id: str
    severity: str
    message: str


@dataclass
class RiskAssessment:
    complexity_score: int
    signals: list[RiskSignal] = field(default_factory=list)


def assess_risk(case: ModernizationInput) -> RiskAssessment:
    """Pure, deterministic scoring — same input always yields the same output. No AI involved."""
    signals: list[RiskSignal] = []
    score = 0

    release = case.release_process.lower()
    hosting = case.hosting.lower()
    scale = case.scale.lower()
    pain_points = case.pain_points.lower()

    if "manual" in release:
        signals.append(
            RiskSignal("M001", "high", "Manual release process increases deployment risk.")
        )
        score += 3

    if "on-prem" in hosting or "on-premises" in hosting:
        signals.append(
            RiskSignal("M002", "medium", "On-premises hosting limits elasticity and scale-out options.")
        )
        score += 2

    if scale == "large" and "manual" in release:
        signals.append(
            RiskSignal("M003", "high", "Large scale combined with manual releases increases coordinated-failure risk.")
        )
        score += 3

    if "outage" in pain_points or "downtime" in pain_points:
        signals.append(
            RiskSignal("M004", "medium", "Reported outages/downtime indicate existing reliability gaps.")
        )
        score += 2

    return RiskAssessment(complexity_score=score, signals=signals)
