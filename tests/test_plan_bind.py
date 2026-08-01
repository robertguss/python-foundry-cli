"""Optional --plan bind API shape without stage writes (python-foundry-cli-0q3)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from python_foundry.catalog import load_default_catalog
from python_foundry.plan import (
    PlanBindError,
    bind_plan,
    construct,
    rebuild_plan,
)
from python_foundry.spec import load_spec

REPO = Path(__file__).resolve().parents[1]
MINIMAL = REPO / "examples" / "minimal-cli.toml"
VECTOR_VERSION = "0.1.0-vector"


def test_bind_match_succeeds(tmp_path: Path) -> None:
    cat = load_default_catalog()
    spec = load_spec(MINIMAL)
    plan = construct(spec, cat, foundry_version=VECTOR_VERSION)
    artifact = tmp_path / "plan.json"
    artifact.write_text(json.dumps({"ok": True, "plan": plan.body}), encoding="utf-8")

    bound = bind_plan(
        spec=spec,
        catalog=cat,
        plan_artifact=artifact,
        foundry_version=VECTOR_VERSION,
    )
    assert bound.plan_sha256 == plan.plan_sha256
    assert bound.catalog_digest == plan.catalog_digest
    assert bound.foundry_version == plan.foundry_version


def test_bit_flipped_plan_sha256_fails_plan_bind(tmp_path: Path) -> None:
    cat = load_default_catalog()
    spec = load_spec(MINIMAL)
    plan = construct(spec, cat, foundry_version=VECTOR_VERSION)
    body = dict(plan.body)
    # Flip one hex nibble of plan_sha256.
    sha = body["plan_sha256"]
    flipped = ("0" if sha[0] != "0" else "1") + sha[1:]
    body["plan_sha256"] = flipped
    artifact = tmp_path / "bad.json"
    artifact.write_text(json.dumps(body), encoding="utf-8")

    with pytest.raises(PlanBindError) as excinfo:
        bind_plan(
            spec=spec,
            catalog=cat,
            plan_artifact=artifact,
            foundry_version=VECTOR_VERSION,
        )
    assert excinfo.value.error_class == "plan_bind"
    assert excinfo.value.code == "plan_bind.mismatch"
    assert "plan_sha256" in excinfo.value.message


def test_catalog_digest_mismatch_fails(tmp_path: Path) -> None:
    cat = load_default_catalog()
    spec = load_spec(MINIMAL)
    plan = construct(spec, cat, foundry_version=VECTOR_VERSION)
    body = dict(plan.body)
    body["catalog_digest"] = "0" * 64
    artifact = tmp_path / "digest.json"
    artifact.write_text(json.dumps(body), encoding="utf-8")

    with pytest.raises(PlanBindError) as excinfo:
        bind_plan(
            spec=spec,
            catalog=cat,
            plan_artifact=artifact,
            foundry_version=VECTOR_VERSION,
        )
    assert "catalog_digest" in excinfo.value.message


def test_foundry_version_mismatch_fails(tmp_path: Path) -> None:
    cat = load_default_catalog()
    spec = load_spec(MINIMAL)
    plan = construct(spec, cat, foundry_version=VECTOR_VERSION)
    body = dict(plan.body)
    body["foundry"] = {"version": "9.9.9-evil"}
    artifact = tmp_path / "ver.json"
    artifact.write_text(json.dumps(body), encoding="utf-8")

    with pytest.raises(PlanBindError) as excinfo:
        bind_plan(
            spec=spec,
            catalog=cat,
            plan_artifact=artifact,
            foundry_version=VECTOR_VERSION,
        )
    assert "foundry.version" in excinfo.value.message


def test_mismatch_creates_no_stage_directories(tmp_path: Path) -> None:
    """Bind failure must not invoke any write/stage API (no stage dirs)."""
    cat = load_default_catalog()
    spec = load_spec(MINIMAL)
    plan = construct(spec, cat, foundry_version=VECTOR_VERSION)
    body = dict(plan.body)
    body["plan_sha256"] = "deadbeef" * 8
    artifact = tmp_path / "plan.json"
    artifact.write_text(json.dumps(body), encoding="utf-8")

    before = {p.name for p in tmp_path.iterdir()}
    with pytest.raises(PlanBindError):
        bind_plan(
            spec=spec,
            catalog=cat,
            plan_artifact=artifact,
            foundry_version=VECTOR_VERSION,
        )
    after = {p.name for p in tmp_path.iterdir()}
    assert before == after
    assert not any(n.startswith(".foundry-stage") for n in after)


def test_rebuild_unbound_path() -> None:
    cat = load_default_catalog()
    spec = load_spec(MINIMAL)
    a = rebuild_plan(spec=spec, catalog=cat, foundry_version=VECTOR_VERSION)
    b = construct(spec, cat, foundry_version=VECTOR_VERSION)
    assert a.plan_sha256 == b.plan_sha256
