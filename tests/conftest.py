"""Shared pytest fixtures for the foundry test suite."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Repository root (parent of tests/)."""
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def minimal_spec_path(repo_root: Path) -> Path:
    """Path to examples/minimal-cli.toml."""
    return repo_root / "examples" / "minimal-cli.toml"


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fresh Typer CliRunner per test."""
    return CliRunner()
