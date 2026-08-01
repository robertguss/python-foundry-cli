"""SPK-100 / MS-001 PHASE-01 exit: golden plan for minimal cli."""

from __future__ import annotations

import json
from pathlib import Path

from python_foundry.catalog import load_default_catalog
from python_foundry.plan import canonical_json_bytes, construct
from python_foundry.spec import load_spec

REPO = Path(__file__).resolve().parents[1]
MINIMAL = REPO / "examples" / "minimal-cli.toml"
GOLDEN = REPO / "tests" / "goldens" / "spk100_minimal_cli_plan.json"
EVIDENCE = REPO / "docs" / "evidence" / "MS-001-spk100.md"


def test_spk100_golden_matches_recomputed_construct() -> None:
    """Checked-in golden plan body matches pure Construct for minimal-cli."""
    assert GOLDEN.is_file(), f"missing golden {GOLDEN}"
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
    plan = construct(load_spec(MINIMAL), load_default_catalog())
    # Compare sealed bodies as canonical JSON (key order independent).
    assert plan.body == golden
    assert plan.plan_sha256 == golden["plan_sha256"]
    recomputed_bytes = canonical_json_bytes(plan.body)
    golden_bytes = canonical_json_bytes(golden)
    assert recomputed_bytes == golden_bytes


def test_spk100_golden_has_contract_fields() -> None:
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
    for key in (
        "schema",
        "foundry",
        "catalog_digest",
        "specification",
        "resolved",
        "files",
        "lock",
        "external_steps",
        "verify_mode",
        "verify_source",
        "plan_sha256",
        "warnings",
    ):
        assert key in golden, f"missing contract field {key}"
    assert golden["resolved"]["archetype"] == {"kind": "archetype", "id": "cli"}
    assert golden["specification"]["profiles"] == []
    assert golden["verify_mode"] == "default"
    assert golden["verify_source"] == "default"
    assert len(golden["plan_sha256"]) == 64


def test_ms001_evidence_recorded() -> None:
    assert EVIDENCE.is_file()
    text = EVIDENCE.read_text(encoding="utf-8")
    assert "SPK-100" in text
    assert "MS-001" in text
    assert "spk100_minimal_cli_plan.json" in text
