"""Render into stage without place (python-foundry-cli-zx0)."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from python_foundry.catalog import load_default_catalog
from python_foundry.fsx import create_stage
from python_foundry.plan import construct
from python_foundry.plan.models import GenerationPlan
from python_foundry.render import (
    RenderError,
    load_unit_source,
    render_plan_into_stage,
    render_template,
)
from python_foundry.render.stage_render import _source_for_entry
from python_foundry.spec import load_spec


def test_render_template_basic() -> None:
    assert render_template("hi {{ name }}!", {"name": "x"}) == "hi x!"


def test_render_plan_into_stage_no_place(
    tmp_path: Path, minimal_spec_path: Path
) -> None:
    dest = tmp_path / "example-cli"
    spec = load_spec(minimal_spec_path)
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


def test_render_error_fields() -> None:
    err = RenderError("boom", code="render.test")
    assert err.error_class == "render"
    assert err.message == "boom"
    assert err.code == "render.test"


def test_load_unit_source_rejects_unknown_owner_kind() -> None:
    with pytest.raises(RenderError) as excinfo:
        load_unit_source("unknown", "cli", "x.txt")
    assert excinfo.value.code == "render.owner_kind"
    assert "unknown" in excinfo.value.message


def test_load_unit_source_rejects_missing_source() -> None:
    with pytest.raises(RenderError) as excinfo:
        load_unit_source("core", "core", "no-such-source.static")
    assert excinfo.value.code == "render.missing_source"
    assert "catalog source missing" in excinfo.value.message


def test_source_for_entry_uses_explicit_source() -> None:
    entry = {
        "path": "x.txt",
        "render": "static",
        "owner": {"kind": "core", "id": "core"},
        "source": "files/pyproject.toml.tmpl",
    }
    assert (
        _source_for_entry(cast(GenerationPlan, None), entry)
        == "files/pyproject.toml.tmpl"
    )


def test_source_for_entry_looks_up_source_by_path() -> None:
    entry = {
        "path": "pyproject.toml",
        "render": "template",
        "owner": {"kind": "core", "id": "core"},
    }
    assert (
        _source_for_entry(cast(GenerationPlan, None), entry)
        == "files/pyproject.toml.tmpl"
    )


def test_source_for_entry_fails_when_no_inventory_match() -> None:
    entry = {
        "path": "no-such-file.txt",
        "render": "static",
        "owner": {"kind": "core", "id": "core"},
    }
    with pytest.raises(RenderError) as excinfo:
        _source_for_entry(cast(GenerationPlan, None), entry)
    assert excinfo.value.code == "render.source_lookup"
    assert "no inventory source" in excinfo.value.message


@pytest.mark.parametrize(
    ("template", "context", "expected"),
    [
        ("hi {{ name }}!", {"name": "x"}, "hi x!"),
        ("hi {{ name }}!", {}, "hi {{ name }}!"),
        ("{{ a }}{{ a }}", {"a": "x"}, "xx"),
        ("{{ a }} and {{ b }}", {"a": "1", "b": "2"}, "1 and 2"),
        ("no placeholders", {"a": "x"}, "no placeholders"),
        ("literal {{ braces }}", {}, "literal {{ braces }}"),
    ],
)
def test_render_template_variations(
    template: str, context: dict[str, str], expected: str
) -> None:
    assert render_template(template, context) == expected


def test_render_path_delegates_to_template() -> None:
    from python_foundry.render.engine import render_path

    assert (
        render_path("src/{{ module }}/cli.py", {"module": "foo_bar"})
        == "src/foo_bar/cli.py"
    )
