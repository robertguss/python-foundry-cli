"""Text/JSON report encoding and closed error_class taxonomy."""

from __future__ import annotations

from python_foundry.report.encode import (
    encode_failure,
    failure_json,
    failure_text,
    plan_json,
    plan_text,
    validate_json,
    validate_text,
)
from python_foundry.report.errors import ERROR_CLASSES, ErrorClass, ReportError

__all__ = [
    "ERROR_CLASSES",
    "ErrorClass",
    "ReportError",
    "encode_failure",
    "failure_json",
    "failure_text",
    "plan_json",
    "plan_text",
    "validate_json",
    "validate_text",
]
