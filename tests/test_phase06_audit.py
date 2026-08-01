"""PHASE-06 regression + forbidden-path + non-goals audit."""

from __future__ import annotations

from pathlib import Path

from python_foundry.catalog import load_default_catalog
from python_foundry.plan import construct
from python_foundry.spec import load_spec

REPO = Path(__file__).resolve().parents[1]


def test_frozen_public_template_spec_fields() -> None:
    path = REPO / "examples" / "python-foundry-template.toml"
    assert path.is_file()
    spec = load_spec(path)
    assert spec.schema == 1
    assert spec.name == "python-foundry-template"
    assert spec.archetype == "cli"
    assert spec.profiles == ()
    assert spec.python_version == "3.13"
    assert spec.verify is None


def test_product_ci_and_dogfood_artifacts_exist() -> None:
    assert (REPO / ".github/workflows/ci.yml").is_file()
    assert (REPO / ".github/workflows/hybrid-template.yml").is_file()
    assert (REPO / "docs/evidence/MS-005-dogfood.md").is_file()
    assert (REPO / "docs/evidence/MS-004-hybrid.md").is_file()
    assert (REPO / "docs/evidence/MS-006-residual-risk.md").is_file()
    assert (REPO / "docs/catalog-admission.md").is_file()
    assert (REPO / "docs/editor-support.md").is_file()


def test_no_windows_support_claim_in_readme() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8").lower()
    assert "no windows" in readme


def test_plan_bind_docs_present() -> None:
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "generate --plan" in agents
    assert "two-phase" in agents.lower() or "plan_bind" in agents or "FND-004" in agents


def test_catalog_closed_set_complete() -> None:
    cat = load_default_catalog()
    refs = {u.ref for u in cat.units}
    assert refs >= {
        "core/core",
        "archetype/cli",
        "archetype/scripts",
        "archetype/data-etl",
        "profile/http",
        "profile/hooks-hk",
        "profile/data-etl",
    }
    plan = construct(load_spec(REPO / "examples" / "minimal-cli.toml"), cat)
    assert plan.plan_sha256
