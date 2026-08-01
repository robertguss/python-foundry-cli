"""Spec parse/validate errors (error_class=validation)."""

from __future__ import annotations


class SpecError(Exception):
    """Base error for Project Spec parse and validation failures."""

    error_class: str = "validation"

    def __init__(self, message: str, *, code: str = "spec.error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return self.message


class SpecParseError(SpecError):
    """TOML could not be decoded or is not a table."""

    def __init__(self, message: str, *, code: str = "spec.parse") -> None:
        super().__init__(message, code=code)


class SpecValidationError(SpecError):
    """Decoded document failed schema / field / policy rules."""

    def __init__(self, message: str, *, code: str = "spec.validation") -> None:
        super().__init__(message, code=code)
