import ast
import re
from dataclasses import dataclass

MAX_LINE_LENGTH = 100
_SECRET_PATTERN = re.compile(r"(api_key|secret|password|token)\s*=\s*['\"][^'\"]+['\"]", re.IGNORECASE)


@dataclass
class CodeFinding:
    rule_id: str
    severity: str
    message: str
    line: int | None = None


def check_line_length(source: str) -> list[CodeFinding]:
    findings = []
    for i, line in enumerate(source.splitlines(), start=1):
        if len(line) > MAX_LINE_LENGTH:
            findings.append(CodeFinding("C001", "low", f"Line exceeds {MAX_LINE_LENGTH} characters.", i))
    return findings


def check_bare_except(source: str) -> list[CodeFinding]:
    findings = []
    for i, line in enumerate(source.splitlines(), start=1):
        if re.match(r"\s*except\s*:", line):
            findings.append(CodeFinding("C002", "medium", "Bare 'except:' clause swallows all exceptions.", i))
    return findings


def check_todo_markers(source: str) -> list[CodeFinding]:
    findings = []
    for i, line in enumerate(source.splitlines(), start=1):
        if re.search(r"#\s*(TODO|FIXME)", line, re.IGNORECASE):
            findings.append(CodeFinding("C003", "low", "TODO/FIXME marker found.", i))
    return findings


def check_secret_like_assignment(source: str) -> list[CodeFinding]:
    findings = []
    for i, line in enumerate(source.splitlines(), start=1):
        if _SECRET_PATTERN.search(line):
            findings.append(CodeFinding("C004", "high", "Possible hardcoded secret-like assignment.", i))
    return findings


def check_missing_docstrings(source: str) -> list[CodeFinding]:
    """Parses (never executes) the source via ast to find public functions/classes without docstrings."""
    findings: list[CodeFinding] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [CodeFinding("C005", "high", "Source could not be parsed (syntax error).")]

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_"):
                continue
            if ast.get_docstring(node) is None:
                findings.append(
                    CodeFinding("C006", "low", f"Public '{node.name}' is missing a docstring.", node.lineno)
                )
    return findings


def run_all_checks(source: str) -> list[CodeFinding]:
    findings: list[CodeFinding] = []
    findings.extend(check_missing_docstrings(source))
    if not any(f.rule_id == "C005" for f in findings):
        findings.extend(check_line_length(source))
        findings.extend(check_bare_except(source))
        findings.extend(check_todo_markers(source))
        findings.extend(check_secret_like_assignment(source))
    return findings
