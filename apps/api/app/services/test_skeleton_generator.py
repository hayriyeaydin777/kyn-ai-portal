import ast


def _function_defs(source: str) -> list[ast.FunctionDef]:
    """Parses (never executes) source, returning public top-level function definitions."""
    tree = ast.parse(source)
    return [
        node
        for node in ast.iter_child_nodes(tree)
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    ]


def generate_test_skeleton(source: str) -> str:
    """Deterministic pytest skeleton generator. Parses signatures via ast only, never runs the code."""
    try:
        functions = _function_defs(source)
    except SyntaxError:
        return "# Could not parse source (syntax error) — no tests generated.\n"

    if not functions:
        return "# No public top-level functions found — no tests generated.\n"

    lines = ["import pytest", ""]
    for func in functions:
        param_names = [a.arg for a in func.args.args]

        lines.append(f"def test_{func.name}_happy_path():")
        lines.append(f"    # TODO: call {func.name}({', '.join(param_names)}) with valid inputs and assert result")
        lines.append("    pass")
        lines.append("")

        for param in param_names:
            lines.append(f"def test_{func.name}_with_{param}_boundary():")
            lines.append(f"    # TODO: exercise a boundary/edge value for '{param}'")
            lines.append("    pass")
            lines.append("")

    return "\n".join(lines)
