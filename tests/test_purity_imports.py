"""Architecture: plan package must not import write-path modules."""

from __future__ import annotations

import ast
from pathlib import Path

PLAN_DIR = Path(__file__).resolve().parents[1] / "src" / "python_foundry" / "plan"
FORBIDDEN = frozenset(
    {
        "python_foundry.fsx",
        "python_foundry.generate",
        "python_foundry.cli",
        "fsx",
        "generate",
        "cli",
    }
)


def _imported_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_plan_package_does_not_import_write_path() -> None:
    py_files = list(PLAN_DIR.rglob("*.py"))
    assert py_files, "expected plan package sources"
    for path in py_files:
        imported = _imported_names(path)
        offenders = imported & FORBIDDEN
        assert not offenders, f"{path} imports forbidden modules: {offenders}"
