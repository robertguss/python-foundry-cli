"""Plan Construct + plan_sha256 canonicalization (python-foundry-cli-6tm)."""

from __future__ import annotations

import json
from pathlib import Path

from python_foundry.catalog import load_default_catalog
from python_foundry.plan import (
    GenerationPlan,
    canonical_json_bytes,
    construct,
    sha256_hex,
)
from python_foundry.spec import load_spec, parse_spec_text

REPO_ROOT = Path(__file__).resolve().parents[1]
MINIMAL_CLI = REPO_ROOT / "examples" / "minimal-cli.toml"

# Fixed foundry version pin for the frozen plan_sha256 test vector so package
# version bumps do not silently invalidate the vector.
VECTOR_FOUNDRY_VERSION = "0.1.0-vector"


def test_construct_minimal_cli() -> None:
    spec = load_spec(MINIMAL_CLI)
    plan = construct(
        spec,
        load_default_catalog(),
        foundry_version=VECTOR_FOUNDRY_VERSION,
    )
    assert isinstance(plan, GenerationPlan)
    assert plan.plan_sha256 == plan.body["plan_sha256"]
    assert len(plan.plan_sha256) == 64
    assert plan.body["schema"] == 1
    assert plan.foundry_version == VECTOR_FOUNDRY_VERSION
    assert plan.catalog_digest == load_default_catalog().digest
    assert plan.verify_mode == "default"
    assert plan.verify_source == "default"
    # Kind-qualified unit refs (REQ-087).
    assert plan.body["resolved"]["archetype"] == {"kind": "archetype", "id": "cli"}
    assert plan.body["resolved"]["units"][0] == {"kind": "core", "id": "core"}
    assert all("kind" in u and "id" in u for u in plan.body["resolved"]["units"])
    assert plan.body["files"]
    assert plan.body["lock"]["produce"] is True
    assert "ty_check" in {s["id"] for s in plan.body["external_steps"]}


def test_plan_sha256_matches_preimage() -> None:
    spec = load_spec(MINIMAL_CLI)
    plan = construct(
        spec,
        load_default_catalog(),
        foundry_version=VECTOR_FOUNDRY_VERSION,
    )
    body = dict(plan.body)
    del body["plan_sha256"]
    recomputed = sha256_hex(canonical_json_bytes(body))
    assert recomputed == plan.plan_sha256
    assert plan.preimage == canonical_json_bytes(body)


def test_deterministic_repeated_construct() -> None:
    cat = load_default_catalog()
    spec = load_spec(MINIMAL_CLI)
    a = construct(spec, cat, foundry_version=VECTOR_FOUNDRY_VERSION)
    b = construct(spec, cat, foundry_version=VECTOR_FOUNDRY_VERSION)
    assert a.plan_sha256 == b.plan_sha256
    assert a.body == b.body
    assert a.preimage == b.preimage


def test_profile_order_independent_plan_body() -> None:
    cat = load_default_catalog()
    a = construct(
        parse_spec_text(
            'schema=1\nname="d"\narchetype="cli"\ndestination="./d"\n'
            'profiles=["data-etl","http","hooks-hk"]\n'
        ),
        cat,
        foundry_version=VECTOR_FOUNDRY_VERSION,
    )
    b = construct(
        parse_spec_text(
            'schema=1\nname="d"\narchetype="cli"\ndestination="./d"\n'
            'profiles=["http","hooks-hk","data-etl"]\n'
        ),
        cat,
        foundry_version=VECTOR_FOUNDRY_VERSION,
    )
    assert a.plan_sha256 == b.plan_sha256
    assert a.body["specification"]["profiles"] == ["data-etl", "hooks-hk", "http"]
    assert a.body["resolved"]["profiles"] == b.body["resolved"]["profiles"]
    assert a.body["resolved"]["profiles"] == [
        {"kind": "profile", "id": "http"},
        {"kind": "profile", "id": "hooks-hk"},
        {"kind": "profile", "id": "data-etl"},
    ]


def test_verify_fields_on_plan_from_cli() -> None:
    plan = construct(
        load_spec(MINIMAL_CLI),
        load_default_catalog(),
        cli_verify="strict",
        foundry_version=VECTOR_FOUNDRY_VERSION,
    )
    assert plan.verify_mode == "strict"
    assert plan.verify_source == "cli"
    assert "pytest" in {s["id"] for s in plan.body["external_steps"]}


# Frozen FND-009 vector for minimal-cli + VECTOR_FOUNDRY_VERSION + shipped catalog.
# Update deliberately when Construct shape or catalog stubs change.
FIXED_PLAN_SHA256 = (
    "169be09438fc33c8f2c30d0983e19a23e08f7f3c5005eed854322209bc2d3bbc"
)


def test_fixed_plan_sha256_test_vector() -> None:
    """Frozen vector: minimal-cli cell + pinned foundry version → known hash."""
    plan = construct(
        load_spec(MINIMAL_CLI),
        load_default_catalog(),
        foundry_version=VECTOR_FOUNDRY_VERSION,
    )
    assert plan.plan_sha256 == FIXED_PLAN_SHA256
    vector_path = Path(__file__).with_name("plan_sha256_vector.txt")
    assert vector_path.read_text(encoding="utf-8").strip() == FIXED_PLAN_SHA256
    body = json.loads(canonical_json_bytes(plan.body).decode())
    assert body["plan_sha256"] == FIXED_PLAN_SHA256
