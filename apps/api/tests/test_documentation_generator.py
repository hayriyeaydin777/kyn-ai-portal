from app.services.documentation_generator import generate_documentation


def test_documents_public_function_with_existing_docstring():
    source = 'def add(a, b):\n    """Adds two numbers."""\n    return a + b\n'
    doc = generate_documentation(source)

    assert "## add(a, b)" in doc
    assert "Adds two numbers." in doc


def test_function_without_docstring_shows_placeholder_not_fabricated_text():
    source = "def add(a, b):\n    return a + b\n"
    doc = generate_documentation(source)

    assert "_No docstring provided in source._" in doc


def test_documents_public_class():
    source = 'class Widget:\n    """A widget."""\n    pass\n'
    doc = generate_documentation(source)

    assert "## class Widget" in doc
    assert "A widget." in doc


def test_skips_private_functions():
    source = "def _helper():\n    pass\n"
    doc = generate_documentation(source)

    assert "_helper" not in doc
    assert "No public top-level functions or classes found" in doc


def test_syntax_error_returns_message_not_exception():
    source = "def broken(:\n"
    doc = generate_documentation(source)

    assert "Could not parse source" in doc


def test_is_deterministic():
    source = "def f(x):\n    return x\n"
    assert generate_documentation(source) == generate_documentation(source)
