"""Resolve package errors (error_class=resolve)."""

from __future__ import annotations


class ResolveError(Exception):
    """Base error for composition / resolve failures."""

    error_class: str = "resolve"

    def __init__(self, message: str, *, code: str = "resolve.error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return self.message
