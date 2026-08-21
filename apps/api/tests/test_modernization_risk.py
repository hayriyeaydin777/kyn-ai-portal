from app.services.modernization_risk import ModernizationInput, assess_risk


def _input(**overrides) -> ModernizationInput:
    defaults = dict(
        technology_stack="Fictional monolith",
        hosting="cloud",
        release_process="automated",
        scale="small",
        pain_points="",
    )
    defaults.update(overrides)
    return ModernizationInput(**defaults)


def test_manual_release_triggers_m001():
    result = assess_risk(_input(release_process="manual, quarterly releases"))

    assert any(s.rule_id == "M001" for s in result.signals)
    assert result.complexity_score >= 3


def test_on_prem_hosting_triggers_m002():
    result = assess_risk(_input(hosting="on-premises data center"))

    assert any(s.rule_id == "M002" for s in result.signals)


def test_large_scale_with_manual_release_triggers_m003():
    result = assess_risk(_input(release_process="manual", scale="large"))

    rule_ids = {s.rule_id for s in result.signals}
    assert {"M001", "M003"}.issubset(rule_ids)


def test_outage_pain_point_triggers_m004():
    result = assess_risk(_input(pain_points="Frequent outages during peak load"))

    assert any(s.rule_id == "M004" for s in result.signals)


def test_clean_input_has_no_signals():
    result = assess_risk(_input())

    assert result.signals == []
    assert result.complexity_score == 0


def test_is_deterministic():
    case = _input(release_process="manual", hosting="on-prem", scale="large", pain_points="downtime")

    first = assess_risk(case)
    second = assess_risk(case)

    assert first == second
