"""Closed error_class taxonomy (REQ-091 / FND-012)."""

from __future__ import annotations

from typing import Literal

ErrorClass = Literal[
    "validation",
    "resolve",
    "plan_bind",
    "render",
    "lock",
    "verify",
    "place",
    "internal",
]

ERROR_CLASSES: frozenset[str] = frozenset(
    {
        "validation",
        "resolve",
        "plan_bind",
        "render",
        "lock",
        "verify",
        "place",
        "internal",
    }
)


class ReportError(Exception):
    """Raised when a caller supplies an unknown error_class."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
