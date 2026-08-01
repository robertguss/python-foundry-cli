"""Archetype + profile set composition (pure; no filesystem writes)."""

from __future__ import annotations

from python_foundry.resolve.compose import HOOKS_HK_REPLACES, resolve
from python_foundry.resolve.errors import ResolveError
from python_foundry.resolve.models import PlannedFile, ResolvedProject
from python_foundry.resolve.verify import (
    DEFAULT_VERIFY_MODE,
    EffectiveVerify,
    VerifySource,
    resolve_effective_verify,
)

__all__ = [
    "DEFAULT_VERIFY_MODE",
    "HOOKS_HK_REPLACES",
    "EffectiveVerify",
    "PlannedFile",
    "ResolveError",
    "ResolvedProject",
    "VerifySource",
    "resolve",
    "resolve_effective_verify",
]
