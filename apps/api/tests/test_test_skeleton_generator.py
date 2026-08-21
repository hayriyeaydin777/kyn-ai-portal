from app.services.test_skeleton_generator import generate_test_skeleton


def test_generates_happy_path_and_boundary_tests_for_public_function():
    source = "def add(a, b):\n    return a + b\n"
    skeleton = generate_test_skeleton(source)

    assert "def test_add_happy_path():" in skeleton
    assert "def test_add_with_a_boundary():" in skeleton
    assert "def test_add_with_b_boundary():" in skeleton


def test_skips_private_functions():
    source = "def _helper(x):\n    return x\n"
    skeleton = generate_test_skeleton(source)

    assert "test__helper" not in skeleton
    assert "No public top-level functions found" in skeleton


def test_no_functions_returns_message():
    source = "x = 1\n"
    skeleton = generate_test_skeleton(source)

    assert "No public top-level functions found" in skeleton


def test_syntax_error_returns_message_not_exception():
    source = "def broken(:\n"
    skeleton = generate_test_skeleton(source)

    assert "Could not parse source" in skeleton


def test_is_deterministic():
    source = "def multiply(x, y):\n    return x * y\n"
    first = generate_test_skeleton(source)
    second = generate_test_skeleton(source)
    assert first == second


def test_never_executes_submitted_code():
    """A function with a side effect (e.g. raising) must not run during generation."""
    source = "def dangerous():\n    raise RuntimeError('should never run')\n"
    skeleton = generate_test_skeleton(source)
    assert "test_dangerous_happy_path" in skeleton
