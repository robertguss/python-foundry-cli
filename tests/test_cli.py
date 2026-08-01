"""CLI wiring tests for validate/plan/catalog/version (python-foundry-cli-ofq)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from python_foundry import __version__
from python_foundry.catalog import load_default_catalog
from python_foundry.cli.main import app
from python_foundry.generate import GenerateError
from python_foundry.plan import construct
from python_foundry.spec import load_spec


def test_version_prints_package_and_catalog_digest(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert f"foundry {__version__}" in result.stdout
    digest = load_default_catalog().digest
    assert f"catalog_digest {digest}" in result.stdout


def test_validate_minimal_cli(
    cli_runner: CliRunner, minimal_spec_path: Path
) -> None:
    result = cli_runner.invoke(app, ["validate", "--spec", str(minimal_spec_path)])
    assert result.exit_code == 0
    assert "foundry validate: ok" in result.stdout
    assert "example-cli" in result.stdout


def test_validate_json_success(
    cli_runner: CliRunner, minimal_spec_path: Path
) -> None:
    ok = cli_runner.invoke(
        app, ["validate", "--spec", str(minimal_spec_path), "--json"]
    )
    assert ok.exit_code == 0
    body = json.loads(ok.stdout)
    assert body["ok"] is True


def test_validate_json_missing_spec_fails(cli_runner: CliRunner) -> None:
    missing = cli_runner.invoke(
        app, ["validate", "--spec", "/no/such/spec.toml", "--json"]
    )
    assert missing.exit_code != 0
    fail = json.loads(missing.stdout)
    assert fail["ok"] is False
    assert fail["error_class"] == "validation"


def test_plan_minimal_cli_text(
    cli_runner: CliRunner, minimal_spec_path: Path
) -> None:
    text = cli_runner.invoke(app, ["plan", "--spec", str(minimal_spec_path)])
    assert text.exit_code == 0
    assert "foundry plan" in text.stdout
    assert "plan_sha256:" in text.stdout


def test_plan_minimal_cli_json(
    cli_runner: CliRunner, minimal_spec_path: Path
) -> None:
    js = cli_runner.invoke(
        app, ["plan", "--spec", str(minimal_spec_path), "--json"]
    )
    assert js.exit_code == 0
    body = json.loads(js.stdout)
    assert body["ok"] is True
    assert "plan_sha256" in body["plan"]
    assert len(body["plan"]["plan_sha256"]) == 64


def test_plan_verify_cli_override(
    cli_runner: CliRunner, minimal_spec_path: Path
) -> None:
    result = cli_runner.invoke(
        app,
        ["plan", "--spec", str(minimal_spec_path), "--verify", "strict", "--json"],
    )
    assert result.exit_code == 0
    body = json.loads(result.stdout)
    assert body["plan"]["verify_mode"] == "strict"
    assert body["plan"]["verify_source"] == "cli"


def test_validate_plan_leave_destination_untouched(
    tmp_path: Path, cli_runner: CliRunner
) -> None:
    dest = tmp_path / "example-cli"
    dest.mkdir()
    marker = dest / "keep-me.txt"
    marker.write_text("safe\n", encoding="utf-8")
    before = {p.name: p.read_bytes() for p in dest.iterdir()}
    mtime_before = {p.name: p.stat().st_mtime_ns for p in dest.iterdir()}

    # Spec destination points at a path under tmp; validate/plan must not touch it.
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "example-cli"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    v = cli_runner.invoke(app, ["validate", "--spec", str(spec)])
    p = cli_runner.invoke(app, ["plan", "--spec", str(spec)])
    assert v.exit_code == 0
    assert p.exit_code == 0
    after = {p.name: p.read_bytes() for p in dest.iterdir()}
    mtime_after = {p.name: p.stat().st_mtime_ns for p in dest.iterdir()}
    assert before == after
    assert mtime_before == mtime_after
    # No stage dirs created next to dest.
    siblings = {c.name for c in tmp_path.iterdir()}
    assert not any(n.startswith(".foundry-stage") for n in siblings)


def test_catalog_list_kind_qualified(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["catalog", "list"])
    assert result.exit_code == 0
    assert "archetype/cli" in result.stdout
    assert "archetype/data-etl" in result.stdout
    assert "profile/data-etl" in result.stdout
    assert "core/core" in result.stdout


def test_catalog_show_distinguishes_data_etl(cli_runner: CliRunner) -> None:
    a = cli_runner.invoke(app, ["catalog", "show", "archetype/data-etl"])
    b = cli_runner.invoke(app, ["catalog", "show", "profile/data-etl"])
    assert a.exit_code == 0
    assert b.exit_code == 0
    assert a.stdout != b.stdout
    assert "archetype/data-etl" in a.stdout
    assert "profile/data-etl" in b.stdout


def test_catalog_show_unknown_unit_fails(cli_runner: CliRunner) -> None:
    missing = cli_runner.invoke(app, ["catalog", "show", "archetype/nope"])
    assert missing.exit_code != 0


def test_real_uv_run_foundry_version(repo_root: Path) -> None:
    """Drive the real console script path twice for consistency."""
    for _ in range(2):
        proc = subprocess.run(
            ["uv", "run", "foundry", "version"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr
        assert f"foundry {__version__}" in proc.stdout
        assert "catalog_digest" in proc.stdout


def test_real_uv_run_foundry_validate(
    repo_root: Path, minimal_spec_path: Path
) -> None:
    proc = subprocess.run(
        ["uv", "run", "foundry", "validate", "--spec", str(minimal_spec_path)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "foundry validate: ok" in proc.stdout


def test_real_uv_run_foundry_plan_json(
    repo_root: Path, minimal_spec_path: Path
) -> None:
    proc = subprocess.run(
        [
            "uv",
            "run",
            "foundry",
            "plan",
            "--spec",
            str(minimal_spec_path),
            "--json",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    body = json.loads(proc.stdout)
    assert body["ok"] is True


def test_catalog_list_json_output(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["catalog", "list", "--json"])
    assert result.exit_code == 0
    body = json.loads(result.stdout)
    assert body["ok"] is True
    refs = {u["ref"] for u in body["units"]}
    assert "archetype/cli" in refs
    assert "profile/data-etl" in refs


def test_catalog_show_json_success(cli_runner: CliRunner) -> None:
    ok = cli_runner.invoke(app, ["catalog", "show", "archetype/data-etl", "--json"])
    assert ok.exit_code == 0
    body = json.loads(ok.stdout)
    assert body["ok"] is True
    assert body["unit"]["id"] == "data-etl"
    assert body["unit"]["kind"] == "archetype"


def test_catalog_show_json_unknown_fails(cli_runner: CliRunner) -> None:
    bad = cli_runner.invoke(app, ["catalog", "show", "archetype/nope", "--json"])
    assert bad.exit_code != 0
    fail = json.loads(bad.stdout)
    assert fail["ok"] is False
    assert fail["error_class"] == "resolve"
    assert fail["code"] == "catalog.unknown_unit"


def test_generate_json_success(tmp_path: Path, cli_runner: CliRunner) -> None:
    dest = tmp_path / "out"
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "json-cli"
archetype = "cli"
destination = "{dest}"
profiles = []
verify = "none"
''',
        encoding="utf-8",
    )
    result = cli_runner.invoke(
        app, ["generate", "--spec", str(spec_path), "--dest", str(dest), "--json"]
    )
    assert result.exit_code == 0, result.output
    body = json.loads(result.stdout)
    assert body["ok"] is True
    assert body["destination"] == str(dest.resolve())
    assert "plan_sha256" in body
    assert body["verify_mode"] == "none"
    assert body["verify_source"] == "toml"
    assert "network_disclosure" in body
    assert body["verify_warning"] is not None


def test_generate_json_validation_failure(
    tmp_path: Path, cli_runner: CliRunner
) -> None:
    missing = tmp_path / "missing.toml"
    result = cli_runner.invoke(
        app,
        ["generate", "--spec", str(missing), "--dest", str(tmp_path / "out"), "--json"],
    )
    assert result.exit_code != 0
    body = json.loads(result.stdout)
    assert body["ok"] is False
    assert body["error_class"] == "validation"
    assert body["code"] == "spec.read"


def test_generate_json_plan_bind_failure(
    tmp_path: Path,
    cli_runner: CliRunner,
    minimal_spec_path: Path,
) -> None:
    spec = load_spec(minimal_spec_path)
    plan = construct(spec, load_default_catalog())
    bad_plan = dict(plan.body)
    bad_plan["plan_sha256"] = "0" * 64
    plan_path = tmp_path / "bad-plan.json"
    plan_path.write_text(json.dumps(bad_plan), encoding="utf-8")
    dest = tmp_path / "out"
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "bind-cli"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = cli_runner.invoke(
        app,
        [
            "generate",
            "--spec",
            str(spec_path),
            "--dest",
            str(dest),
            "--plan",
            str(plan_path),
            "--json",
        ],
    )
    assert result.exit_code != 0
    body = json.loads(result.stdout)
    assert body["ok"] is False
    assert body["error_class"] == "plan_bind"
    assert body["code"] == "plan_bind.mismatch"


def test_generate_json_place_failure(tmp_path: Path, cli_runner: CliRunner) -> None:
    dest = tmp_path / "out"
    dest.mkdir()
    (dest / "existing.txt").write_text("keep\n", encoding="utf-8")
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "place-cli"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = cli_runner.invoke(
        app, ["generate", "--spec", str(spec_path), "--dest", str(dest), "--json"]
    )
    assert result.exit_code != 0
    body = json.loads(result.stdout)
    assert body["ok"] is False
    assert body["error_class"] == "place"


@pytest.mark.parametrize(
    "error_class, code",
    [
        ("render", "render.error"),
        ("lock", "lock.failed"),
        ("verify", "verify.ruff_check"),
        ("internal", "generate.internal"),
    ],
)
def test_generate_json_failure_schema(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    cli_runner: CliRunner,
    error_class: str,
    code: str,
) -> None:
    stage_path = str(tmp_path / "stage")
    plan_sha256 = "a" * 64

    def _fake_generate(**kwargs: object) -> None:
        raise GenerateError(
            "injected",
            error_class=error_class,
            code=code,
            stage_path=stage_path,
            verify_mode="default",
            plan_sha256=plan_sha256,
        )

    monkeypatch.setattr("python_foundry.generate.generate", _fake_generate)
    spec_path = tmp_path / "cell.toml"
    spec_path.write_text(
        f'''
schema = 1
name = "schema-cli"
archetype = "cli"
destination = "{tmp_path / "out"}"
profiles = []
''',
        encoding="utf-8",
    )
    result = cli_runner.invoke(
        app,
        [
            "generate",
            "--spec",
            str(spec_path),
            "--dest",
            str(tmp_path / "out"),
            "--json",
        ],
    )
    assert result.exit_code != 0
    body = json.loads(result.stdout)
    assert body["ok"] is False
    assert body["error_class"] == error_class
    assert body["code"] == code
    assert body["stage_path"] == stage_path
    assert body["verify_mode"] == "default"
    assert body["plan_sha256"] == plan_sha256
