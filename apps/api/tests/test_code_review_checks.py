from app.services.code_review_checks import run_all_checks


def test_long_line_triggers_c001():
    source = "x = 1  # " + ("a" * 100)
    findings = run_all_checks(source)
    assert any(f.rule_id == "C001" for f in findings)


def test_bare_except_triggers_c002():
    source = "def f():\n    try:\n        pass\n    except:\n        pass\n"
    findings = run_all_checks(source)
    assert any(f.rule_id == "C002" for f in findings)


def test_todo_marker_triggers_c003():
    source = "x = 1  # TODO: fix this\n"
    findings = run_all_checks(source)
    assert any(f.rule_id == "C003" for f in findings)


def test_secret_like_assignment_triggers_c004():
    source = 'api_key = "sk-fake-demo-value-not-real"\n'
    findings = run_all_checks(source)
    assert any(f.rule_id == "C004" for f in findings)


def test_missing_docstring_on_public_function_triggers_c006():
    source = "def public_function():\n    pass\n"
    findings = run_all_checks(source)
    assert any(f.rule_id == "C006" and "public_function" in f.message for f in findings)


def test_private_function_without_docstring_is_not_flagged():
    source = "def _private_helper():\n    pass\n"
    findings = run_all_checks(source)
    assert not any(f.rule_id == "C006" for f in findings)


def test_function_with_docstring_is_not_flagged():
    source = 'def documented():\n    """Does something."""\n    pass\n'
    findings = run_all_checks(source)
    assert not any(f.rule_id == "C006" for f in findings)


def test_syntax_error_returns_c005_and_stops_other_checks():
    source = "def broken(:\n    pass\n"
    findings = run_all_checks(source)
    assert len(findings) == 1
    assert findings[0].rule_id == "C005"


def test_clean_source_has_no_findings():
    source = 'def documented():\n    """Docstring."""\n    return 1\n'
    findings = run_all_checks(source)
    assert findings == []


def test_is_deterministic():
    source = "def public_function():\n    pass\n"
    first = run_all_checks(source)
    second = run_all_checks(source)
    assert first == second
