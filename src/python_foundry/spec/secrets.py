"""Reject secret-looking material in Project Spec values (REQ-022)."""

from __future__ import annotations

import re

# Patterns that strongly indicate secret material in free-text fields.
_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"-----BEGIN[ A-Z0-9]*PRIVATE KEY-----"),
    re.compile(r"-----BEGIN OPENSSH PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    # Explicit assignment shapes agents sometimes paste into description.
    re.compile(
        r"(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*[:=]\s*\S+"
    ),
)


def find_secret_hint(text: str) -> str | None:
    """Return a short reason if *text* looks like it carries a secret."""
    for pattern in _SECRET_PATTERNS:
        if pattern.search(text):
            return f"matches forbidden pattern {pattern.pattern!r}"
    return None
