"""Smoke test for python_foundry_template."""

from python_foundry_template import __version__


def test_version() -> None:
    assert __version__ == "0.1.0"
