"""Architecture: pure packages must not import write-path modules."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "src" / "python_foundry"

# Imports that would couple a read/pure package to write-path implementation.
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

PURE_PACKAGES = ["plan", "spec", "resolve", "catalog", "report"]


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


@pytest.mark.parametrize("package", PURE_PACKAGES)
def test_pure_package_does_not_import_write_path(package: str) -> None:
    pkg_dir = SRC / package
    py_files = list(pkg_dir.rglob("*.py"))
    assert py_files, f"expected sources in {package}"
    offenders: list[str] = []
    for path in py_files:
        imported = _imported_names(path)
        bad = imported & FORBIDDEN
        if bad:
            offenders.append(f"{path.name} imports {bad}")
    assert not offenders, f"{package}: {offenders}"
