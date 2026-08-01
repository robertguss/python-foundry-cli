"""Generate orchestration tests (PHASE-03)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from python_foundry.catalog import load_default_catalog
from python_foundry.cli.main import app
from python_foundry.fsx import create_stage
from python_foundry.generate import GenerateError, generate
from python_foundry.generate.lock import produce_uv_lock
from python_foundry.plan import construct
from python_foundry.render import render_plan_into_stage
from python_foundry.spec import load_spec


def test_render_and_lock_in_stage(
    tmp_path: Path, minimal_spec_path: Path
) -> None:
    dest = tmp_path / "example-cli"
    spec = load_spec(minimal_spec_path)
    plan = construct(spec, load_default_catalog())
    stage = create_stage(dest)
    render_plan_into_stage(plan, spec, stage)
    assert (stage.path / "pyproject.toml").is_file()
    assert (stage.path / "src/example_cli/cli.py").is_file()
    lock = produce_uv_lock(stage.path)
    assert lock.is_file()
    assert not dest.exists()


def test_generate_bind_mismatch_before_stage(
    tmp_path: Path, minimal_spec_path: Path
) -> None:
    dest = tmp_path / "out"
    spec = load_spec(minimal_spec_path)
    plan = construct(spec, load_default_catalog())
    body = dict(plan.body)
    body["plan_sha256"] = "0" * 64
    artifact = tmp_path / "bad-plan.json"
    artifact.write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(GenerateError) as excinfo:
        generate(
            spec_path=minimal_spec_path,
            destination=dest,
            plan_path=artifact,
            run_lock=False,
            run_verify_tools=False,
        )
    assert excinfo.value.error_class == "plan_bind"
    assert excinfo.value.stage_path is None
    # No stage dirs created.
    after_names = {p.name for p in tmp_path.iterdir()}
    assert not any(n.startswith(".foundry-stage") for n in after_names)


def test_generate_full_minimal_cli(tmp_path: Path) -> None:
    """Thin e2e: generate minimal cli with lock + default verify + place."""
    dest = tmp_path / "example-cli"
    # Write a local spec so destination is under tmp_path.
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "example-cli"
description = "e2e cell"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = generate(spec_path=spec_path, destination=dest)
    assert result.placed
    assert dest.is_dir()
    assert (dest / "uv.lock").is_file()
    assert (dest / "pyproject.toml").is_file()
    assert (dest / "src/example_cli/cli.py").is_file()
    assert result.verify_mode == "default"
    disc = result.network_disclosure.lower()
    assert "network" in disc or "uv" in disc


def test_generate_verify_none_surfaces_loud_warning(tmp_path: Path) -> None:
    """REQ-080 §9.5.2: --verify none is a loud, user-visible opt-out."""
    dest = tmp_path / "none-cli"
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "none-cli"
archetype = "cli"
destination = "{dest}"
profiles = []
verify = "none"
''',
        encoding="utf-8",
    )
    result = generate(spec_path=spec_path, destination=dest)
    assert result.placed
    assert result.verify_mode == "none"
    assert result.verify_warning
    assert "no tooling proof" in result.verify_warning.lower()


def test_generate_cmd_verify_none_prints_warning(
    tmp_path: Path, cli_runner: CliRunner
) -> None:
    dest = tmp_path / "none-cli-cmd"
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "none-cli-cmd"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = cli_runner.invoke(
        app, ["generate", "--spec", str(spec_path), "--verify", "none"]
    )
    assert result.exit_code == 0
    assert "WARNING" in result.output


def test_generate_cmd_verify_none_json_includes_warning(
    tmp_path: Path, cli_runner: CliRunner
) -> None:
    dest_json = tmp_path / "none-cli-cmd-json"
    spec_json = tmp_path / "cell-json.toml"
    spec_json.write_text(
        f'''
schema = 1
name = "none-cli-cmd-json"
archetype = "cli"
destination = "{dest_json}"
profiles = []
''',
        encoding="utf-8",
    )
    js = cli_runner.invoke(
        app,
        ["generate", "--spec", str(spec_json), "--verify", "none", "--json"],
    )
    assert js.exit_code == 0
    body = json.loads(js.stdout)
    assert body["verify_warning"]
