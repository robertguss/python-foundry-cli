"""Smoke tests for the scaffold CLI."""

from typer.testing import CliRunner

from python_foundry.cli.main import app


def test_version_prints_package_version(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "foundry" in result.stdout
    assert "0.1.0" in result.stdout
