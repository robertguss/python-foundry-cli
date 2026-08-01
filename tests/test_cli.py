"""CLI wiring tests for validate/plan/catalog/version (python-foundry-cli-ofq)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from python_foundry import __version__
from python_foundry.catalog import load_default_catalog
from python_foundry.cli.main import app

REPO = Path(__file__).resolve().parents[1]
MINIMAL = REPO / "examples" / "minimal-cli.toml"
runner = CliRunner()


def test_version_prints_package_and_catalog_digest() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert f"foundry {__version__}" in result.stdout
    digest = load_default_catalog().digest
    assert f"catalog_digest {digest}" in result.stdout


def test_validate_minimal_cli() -> None:
    result = runner.invoke(app, ["validate", "--spec", str(MINIMAL)])
    assert result.exit_code == 0
    assert "foundry validate: ok" in result.stdout
    assert "example-cli" in result.stdout


def test_validate_json_and_failure() -> None:
    ok = runner.invoke(app, ["validate", "--spec", str(MINIMAL), "--json"])
    assert ok.exit_code == 0
    body = json.loads(ok.stdout)
    assert body["ok"] is True
    bad = runner.invoke(app, ["validate", "--spec", str(MINIMAL), "--json"])
    # Invalid path
    missing = runner.invoke(
        app, ["validate", "--spec", "/no/such/spec.toml", "--json"]
    )
    assert missing.exit_code != 0
    fail = json.loads(missing.stdout)
    assert fail["ok"] is False
    assert fail["error_class"] == "validation"
    del bad


def test_plan_minimal_cli_text_and_json() -> None:
    text = runner.invoke(app, ["plan", "--spec", str(MINIMAL)])
    assert text.exit_code == 0
    assert "foundry plan" in text.stdout
    assert "plan_sha256:" in text.stdout
    js = runner.invoke(app, ["plan", "--spec", str(MINIMAL), "--json"])
    assert js.exit_code == 0
    body = json.loads(js.stdout)
    assert body["ok"] is True
    assert "plan_sha256" in body["plan"]
    assert len(body["plan"]["plan_sha256"]) == 64


def test_plan_verify_cli_override() -> None:
    result = runner.invoke(
        app, ["plan", "--spec", str(MINIMAL), "--verify", "strict", "--json"]
    )
    assert result.exit_code == 0
    body = json.loads(result.stdout)
    assert body["plan"]["verify_mode"] == "strict"
    assert body["plan"]["verify_source"] == "cli"


def test_validate_plan_leave_destination_untouched(tmp_path: Path) -> None:
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
    v = runner.invoke(app, ["validate", "--spec", str(spec)])
    p = runner.invoke(app, ["plan", "--spec", str(spec)])
    assert v.exit_code == 0
    assert p.exit_code == 0
    after = {p.name: p.read_bytes() for p in dest.iterdir()}
    mtime_after = {p.name: p.stat().st_mtime_ns for p in dest.iterdir()}
    assert before == after
    assert mtime_before == mtime_after
    # No stage dirs created next to dest.
    siblings = {c.name for c in tmp_path.iterdir()}
    assert not any(n.startswith(".foundry-stage") for n in siblings)


def test_catalog_list_kind_qualified() -> None:
    result = runner.invoke(app, ["catalog", "list"])
    assert result.exit_code == 0
    assert "archetype/cli" in result.stdout
    assert "archetype/data-etl" in result.stdout
    assert "profile/data-etl" in result.stdout
    assert "core/core" in result.stdout


def test_catalog_show_distinguishes_data_etl() -> None:
    a = runner.invoke(app, ["catalog", "show", "archetype/data-etl"])
    b = runner.invoke(app, ["catalog", "show", "profile/data-etl"])
    assert a.exit_code == 0
    assert b.exit_code == 0
    assert a.stdout != b.stdout
    assert "archetype/data-etl" in a.stdout
    assert "profile/data-etl" in b.stdout
    missing = runner.invoke(app, ["catalog", "show", "archetype/nope"])
    assert missing.exit_code != 0


def test_real_uv_run_foundry_entry() -> None:
    """Drive the real console script path twice for consistency."""
    for _ in range(2):
        proc = subprocess.run(
            ["uv", "run", "foundry", "version"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr
        assert f"foundry {__version__}" in proc.stdout
        assert "catalog_digest" in proc.stdout

    proc = subprocess.run(
        ["uv", "run", "foundry", "validate", "--spec", str(MINIMAL)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "foundry validate: ok" in proc.stdout

    proc = subprocess.run(
        ["uv", "run", "foundry", "plan", "--spec", str(MINIMAL), "--json"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    body = json.loads(proc.stdout)
    assert body["ok"] is True
