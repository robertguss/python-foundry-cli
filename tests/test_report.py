"""Report text/JSON + error_class taxonomy (python-foundry-cli-s19)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from python_foundry.catalog import load_default_catalog
from python_foundry.plan import construct
from python_foundry.report import (
    ERROR_CLASSES,
    ReportError,
    encode_failure,
    failure_json,
    failure_text,
    plan_json,
    plan_text,
    validate_json,
    validate_text,
)
from python_foundry.spec import load_spec


def test_error_class_closed_set() -> None:
    assert ERROR_CLASSES == frozenset(
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


def test_encode_failure_phase01_classes() -> None:
    for cls in ("validation", "resolve", "plan_bind", "internal"):
        body = encode_failure(error_class=cls, message="boom")
        assert body["ok"] is False
        assert body["error_class"] == cls
        assert body["message"] == "boom"


@pytest.mark.parametrize(
    "error_class",
    sorted(ERROR_CLASSES),
)
def test_encode_failure_round_trips_all_classes(error_class: str) -> None:
    body = encode_failure(
        error_class=error_class,
        message="boom",
        code=f"{error_class}.test",
        stage_path="/tmp/stage",
        verify_mode="default",
        plan_sha256="a" * 64,
    )
    assert body["ok"] is False
    assert body["error_class"] == error_class
    assert body["code"] == f"{error_class}.test"
    assert body["stage_path"] == "/tmp/stage"
    assert body["verify_mode"] == "default"
    assert body["plan_sha256"] == "a" * 64

    raw_json = failure_json(
        error_class=body["error_class"],
        message=body["message"],
        code=body["code"],
        stage_path=body["stage_path"],
        verify_mode=body["verify_mode"],
        plan_sha256=body["plan_sha256"],
    )
    decoded = json.loads(raw_json)
    assert decoded["error_class"] == error_class
    assert decoded["code"] == f"{error_class}.test"

    text = failure_text(
        error_class=body["error_class"],
        message=body["message"],
        code=body["code"],
    )
    assert error_class in text
    assert "boom" in text


def test_unknown_error_class_rejected() -> None:
    with pytest.raises(ReportError) as excinfo:
        encode_failure(error_class="whoops", message="x")
    assert "unknown error_class" in str(excinfo.value)
    with pytest.raises(ReportError):
        failure_json(error_class="invented", message="x")
    with pytest.raises(ReportError):
        failure_text(error_class="invented", message="x")


def test_failure_json_optional_fields() -> None:
    raw = failure_json(
        error_class="plan_bind",
        message="digest mismatch",
        plan_sha256="abc",
        verify_mode="default",
        stage_path="/tmp/stage",
        code="plan_bind.mismatch",
    )
    body = json.loads(raw)
    assert body["ok"] is False
    assert body["error_class"] == "plan_bind"
    assert body["plan_sha256"] == "abc"
    assert body["verify_mode"] == "default"
    assert body["stage_path"] == "/tmp/stage"
    assert body["code"] == "plan_bind.mismatch"


def test_plan_text_readable(minimal_spec_path: Path) -> None:
    plan = construct(load_spec(minimal_spec_path), load_default_catalog())
    text = plan_text(plan)
    assert "foundry plan" in text
    assert plan.plan_sha256 in text
    assert "archetype: archetype/cli" in text
    assert "verify: default" in text
    assert "files:" in text


def test_plan_json_success(minimal_spec_path: Path) -> None:
    plan = construct(load_spec(minimal_spec_path), load_default_catalog())
    body = json.loads(plan_json(plan))
    assert body["ok"] is True
    assert body["plan"]["plan_sha256"] == plan.plan_sha256


def test_validate_text_and_json(minimal_spec_path: Path) -> None:
    spec = load_spec(minimal_spec_path)
    text = validate_text(spec)
    assert "foundry validate: ok" in text
    assert "example-cli" in text
    body = json.loads(validate_json(spec))
    assert body["ok"] is True
    assert body["spec"]["name"] == "example-cli"
