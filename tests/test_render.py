"""Render into stage without place (python-foundry-cli-zx0)."""

from __future__ import annotations

from pathlib import Path

from python_foundry.catalog import load_default_catalog
from python_foundry.fsx import create_stage
from python_foundry.plan import construct
from python_foundry.render import render_plan_into_stage, render_template
from python_foundry.spec import load_spec

REPO = Path(__file__).resolve().parents[1]
MINIMAL = REPO / "examples" / "minimal-cli.toml"


def test_render_template_basic() -> None:
    assert render_template("hi {{ name }}!", {"name": "x"}) == "hi x!"


def test_render_plan_into_stage_no_place(tmp_path: Path) -> None:
    dest = tmp_path / "example-cli"
    spec = load_spec(MINIMAL)
    plan = construct(spec, load_default_catalog())
    stage = create_stage(dest)

    written = render_plan_into_stage(plan, spec, stage)
    assert written
    # Stage has content; destination untouched / absent.
    assert not dest.exists()
    assert (stage.path / "pyproject.toml").is_file()
    pyproject = (stage.path / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "example-cli"' in pyproject
    assert (stage.path / "AGENTS.md").is_file()
    pyver = (stage.path / ".python-version").read_text(encoding="utf-8")
    assert pyver.strip() == "3.13"
    assert (stage.path / "src/example_cli/cli.py").is_file()
    assert (stage.path / "src/example_cli/__init__.py").is_file()
    # Place never called — dest still missing.
    assert not dest.exists()
