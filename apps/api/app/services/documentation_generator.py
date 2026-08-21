import ast


def generate_documentation(source: str) -> str:
    """Restates only real parsed structure (names, args, existing docstrings) — never fabricates behavior."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return "# Could not parse source (syntax error) — no documentation generated.\n"

    top_level = [
        node
        for node in ast.iter_child_nodes(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ]

    if not top_level:
        return "# No public top-level functions or classes found.\n"

    lines = ["# Module Documentation (draft)", ""]
    for node in top_level:
        docstring = ast.get_docstring(node)
        if isinstance(node, ast.ClassDef):
            lines.append(f"## class {node.name}")
        else:
            args = ", ".join(a.arg for a in node.args.args)
            lines.append(f"## {node.name}({args})")
        lines.append(docstring if docstring else "_No docstring provided in source._")
        lines.append("")

    return "\n".join(lines)
