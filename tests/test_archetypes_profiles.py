"""scripts/data-etl archetypes + profile composition emit tests."""

from __future__ import annotations

from pathlib import Path

from python_foundry.catalog import load_default_catalog
from python_foundry.generate import generate
from python_foundry.plan import construct
from python_foundry.spec import parse_spec_text


def test_scripts_archetype_emit(tmp_path: Path) -> None:
    dest = tmp_path / "scripts-app"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "scripts-app"
archetype = "scripts"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    # scripts may not need full ty on empty packages — still run generate
    result = generate(spec_path=spec, destination=dest)
    assert result.placed
    assert (dest / "scripts/hello.py").is_file()
    assert (dest / "tests/test_hello_script.py").is_file()
    assert (dest / ".agents/skills/add-script/SKILL.md").is_file()
    assert not (dest / "src").exists() or not any((dest / "src").rglob("*.py"))


def test_data_etl_archetype_emit(tmp_path: Path) -> None:
    dest = tmp_path / "etl-app"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "etl-app"
archetype = "data-etl"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = generate(spec_path=spec, destination=dest)
    assert result.placed
    assert (dest / "src/etl_app/pipeline.py").is_file()
    assert (dest / "tests/test_pipeline.py").is_file()
    skill = (dest / ".agents/skills/add-script/SKILL.md").read_text(encoding="utf-8")
    assert "archetype/data-etl" in skill or "data-etl" in skill


def test_profile_http_composition_plan() -> None:
    cat = load_default_catalog()
    plan = construct(
        parse_spec_text(
            'schema=1\nname="h"\narchetype="cli"\ndestination="./h"\n'
            'profiles=["http"]\n'
        ),
        cat,
    )
    paths = {f["path"] for f in plan.body["files"]}
    assert any("http_client" in p for p in paths)


def test_hooks_hk_replaces_precommit_in_plan() -> None:
    cat = load_default_catalog()
    plan = construct(
        parse_spec_text(
            'schema=1\nname="h"\narchetype="cli"\ndestination="./h"\n'
            'profiles=["hooks-hk"]\n'
        ),
        cat,
    )
    # hooks-hk override should win for .pre-commit-config.yaml
    owners = {
        f["path"]: f["owner"]
        for f in plan.body["files"]
        if f["path"] == ".pre-commit-config.yaml"
    }
    assert owners.get(".pre-commit-config.yaml", {}).get("id") == "hooks-hk"
