"""Effective verify resolution for plan fields (FND-001 / REQ-084).

Runners land in PHASE-03; this module only records ``verify_mode`` and
``verify_source`` with precedence CLI > TOML > default.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, cast

from python_foundry.resolve.errors import ResolveError
from python_foundry.spec.models import VERIFY_MODES, VerifyMode

VerifySource = Literal["cli", "toml", "default"]
DEFAULT_VERIFY_MODE: VerifyMode = "default"


@dataclass(frozen=True, slots=True)
class EffectiveVerify:
    """Plan-facing verify fields (effective mode + provenance)."""

    mode: VerifyMode
    source: VerifySource


def resolve_effective_verify(
    *,
    cli_verify: str | None = None,
    toml_verify: str | None = None,
) -> EffectiveVerify:
    """Resolve effective verify mode and source (CLI > TOML > default).

    Args:
        cli_verify: Value of CLI ``--verify`` when the flag is present.
            ``None`` means the flag was omitted (not the mode named ``none``).
        toml_verify: Project Spec ``verify`` when set; ``None`` if omitted.

    Returns:
        EffectiveVerify with mode ∈ {default, strict, none} and
        source ∈ {cli, toml, default}.
    """
    if cli_verify is not None:
        return EffectiveVerify(
            mode=_coerce_mode(cli_verify, origin="cli --verify"),
            source="cli",
        )
    if toml_verify is not None:
        return EffectiveVerify(
            mode=_coerce_mode(toml_verify, origin="spec verify"),
            source="toml",
        )
    return EffectiveVerify(mode=DEFAULT_VERIFY_MODE, source="default")


def _coerce_mode(value: str, *, origin: str) -> VerifyMode:
    if value not in VERIFY_MODES:
        allowed = ", ".join(sorted(VERIFY_MODES))
        raise ResolveError(
            f"invalid verify mode {value!r} from {origin}; must be one of: {allowed}",
            code="resolve.invalid_verify",
        )
    return cast(VerifyMode, value)
