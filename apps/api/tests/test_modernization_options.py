from app.data.modernization_options import match_options


def test_match_options_returns_ci_cd_for_manual_release_rule():
    options = match_options(["M001"])

    assert any(o.option_id == "O001" for o in options)


def test_match_options_returns_cloud_migration_for_onprem_rule():
    options = match_options(["M002"])

    assert any(o.option_id == "O002" for o in options)


def test_match_options_deduplicates_when_multiple_rules_hit_same_option():
    options = match_options(["M001", "M003"])

    matching = [o for o in options if o.option_id == "O001"]
    assert len(matching) == 1


def test_match_options_returns_empty_for_unknown_rule():
    options = match_options(["UNKNOWN"])

    assert options == []
