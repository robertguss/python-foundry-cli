"""Archetype + profile set composition (pure; no filesystem writes)."""

from __future__ import annotations

from python_foundry.resolve.compose import HOOKS_HK_REPLACES, resolve
from python_foundry.resolve.errors import ResolveError
from python_foundry.resolve.models import PlannedFile, ResolvedProject

__all__ = [
    "HOOKS_HK_REPLACES",
    "PlannedFile",
    "ResolveError",
    "ResolvedProject",
    "resolve",
]
