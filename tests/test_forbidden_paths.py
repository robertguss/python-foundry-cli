"""Forbidden-path suite across all shipped archetypes (consolidated from SPK-102)."""

from __future__ import annotations

from pathlib import Path

import pytest

from python_foundry.generate import generate

FORBIDDEN_NAMES = {
    "CLAUDE.md",
    ".claude",
    ".env",
    ".env.example",
    ".cursor",
    ".cursorrules",
    "mcp.json",
    ".mcp.json",
    "python-dotenv",
}

SKIP_DIRS = {".venv", "__pycache__", ".ruff_cache", ".pytest_cache", ".git"}


def _iter_project_files(dest: Path) -> list[Path]:
    out: list[Path] = []
    for path in dest.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            out.append(path)
    return out


def _assert_clean(dest: Path) -> None:
    files = _iter_project_files(dest)
    names = {p.name for p in files}
    for bad in FORBIDDEN_NAMES:
        assert bad not in names, f"forbidden path present: {bad}"
    tree_text = "\n".join(p.as_posix() for p in files)
    assert "CLAUDE.md" not in tree_text
    assert ".claude/" not in tree_text
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
    assert "load_dotenv(" not in text
    assert "import dotenv" not in text
    assert "from dotenv" not in text


@pytest.mark.parametrize("archetype", ["cli", "scripts", "data-etl"])
def test_generated_project_has_no_forbidden_paths(
    tmp_path: Path, archetype: str
) -> None:
    dest = tmp_path / archetype
    spec = tmp_path / f"{archetype}.toml"
    spec.write_text(
        f"""
schema = 1
name = "{archetype}-clean"
archetype = "{archetype}"
destination = "{dest}"
profiles = []
""",
        encoding="utf-8",
    )
    generate(spec_path=spec, destination=dest)
    _assert_clean(dest)
