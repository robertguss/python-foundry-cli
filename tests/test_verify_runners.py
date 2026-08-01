"""Verify runners precedence and none mode (python-foundry-cli-9tz)."""

from __future__ import annotations

from pathlib import Path

from python_foundry.verify import NETWORK_DISCLOSURE, run_verify


def test_network_disclosure_mentions_uv(tmp_path: Path) -> None:
    assert "uv" in NETWORK_DISCLOSURE
    assert "network" in NETWORK_DISCLOSURE.lower()


def test_verify_none_skips_with_warning(tmp_path: Path) -> None:
    result = run_verify(tmp_path, "none")
    assert result.skipped is True
    assert result.steps_run == ()
    assert result.warning is not None
    assert "none" in result.warning
