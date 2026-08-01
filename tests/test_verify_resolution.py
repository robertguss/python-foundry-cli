"""Effective verify resolution matrix (python-foundry-cli-va1 / REQ-084)."""

from __future__ import annotations

import pytest

from python_foundry.resolve import ResolveError, resolve_effective_verify
from python_foundry.spec import parse_spec_text


def _toml_verify(mode: str | None) -> str | None:
    """Build a Project Spec and return its ``verify`` field (or None)."""
    verify_line = f'verify = "{mode}"\n' if mode is not None else ""
    text = f"""
schema = 1
name = "demo"
archetype = "cli"
destination = "./demo"
profiles = []
{verify_line}
"""
    return parse_spec_text(text).verify


@pytest.mark.parametrize(
    ("cli", "toml", "want_mode", "want_source"),
    [
        # Omitted both → default + source=default
        (None, None, "default", "default"),
        # TOML only
        (None, "strict", "strict", "toml"),
        (None, "none", "none", "toml"),
        (None, "default", "default", "toml"),
        # CLI only
        ("strict", None, "strict", "cli"),
        ("none", None, "none", "cli"),
        ("default", None, "default", "cli"),
        # CLI wins over TOML (including disagreement)
        ("strict", "none", "strict", "cli"),
        ("none", "strict", "none", "cli"),
        ("default", "strict", "default", "cli"),
        ("strict", "default", "strict", "cli"),
    ],
)
def test_verify_precedence_matrix(
    cli: str | None,
    toml: str | None,
    want_mode: str,
    want_source: str,
) -> None:
    toml_value = _toml_verify(toml) if toml is not None else None
    if toml is None:
        toml_value = _toml_verify(None)
        assert toml_value is None
    else:
        assert toml_value == toml

    eff = resolve_effective_verify(cli_verify=cli, toml_verify=toml_value)
    assert eff.mode == want_mode
    assert eff.source == want_source


def test_cli_override_wins_when_flag_present() -> None:
    eff = resolve_effective_verify(cli_verify="strict", toml_verify="none")
    assert eff.mode == "strict"
    assert eff.source == "cli"


def test_omitted_both_is_default() -> None:
    eff = resolve_effective_verify()
    assert eff.mode == "default"
    assert eff.source == "default"


def test_invalid_cli_mode_fails() -> None:
    with pytest.raises(ResolveError) as excinfo:
        resolve_effective_verify(cli_verify="turbo")
    assert excinfo.value.code == "resolve.invalid_verify"
    assert excinfo.value.error_class == "resolve"


def test_mode_none_is_not_flag_omission() -> None:
    """Mode ``none`` is an explicit value; distinct from flag absence."""
    eff = resolve_effective_verify(cli_verify="none")
    assert eff.mode == "none"
    assert eff.source == "cli"
