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
    # REQ-059: http profile MUST actually add httpx as a dependency.
    assert any(dep.startswith("httpx") for dep in plan.body["dependencies"])


def test_no_profiles_adds_no_dependencies() -> None:
    cat = load_default_catalog()
    plan = construct(
        parse_spec_text(
            'schema=1\nname="h"\narchetype="cli"\ndestination="./h"\nprofiles=[]\n'
        ),
        cat,
    )
    assert plan.body["dependencies"] == []


def test_profile_data_etl_composition_plan() -> None:
    cat = load_default_catalog()
    plan = construct(
        parse_spec_text(
            'schema=1\nname="e"\narchetype="cli"\ndestination="./e"\n'
            'profiles=["data-etl"]\n'
        ),
        cat,
    )
    # REQ-061: profile/data-etl default MUST be polars + pyarrow.
    deps = plan.body["dependencies"]
    assert any(dep.startswith("polars") for dep in deps)
    assert any(dep.startswith("pyarrow") for dep in deps)


def test_http_profile_dependency_rendered_into_pyproject(tmp_path: Path) -> None:
    """REQ-059 acceptance: with/without profile inventories differ."""
    dest = tmp_path / "http-app"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "http-app"
archetype = "cli"
destination = "{dest}"
profiles = ["http"]
''',
        encoding="utf-8",
    )
    result = generate(
        spec_path=spec, destination=dest, run_lock=False, run_verify_tools=False
    )
    assert result.placed
    pyproject = (dest / "pyproject.toml").read_text(encoding="utf-8")
    assert "httpx" in pyproject
    client = (dest / "src/http_app/http_client.py").read_text(encoding="utf-8")
    assert "import httpx" in client


def test_data_etl_profile_dependency_rendered_into_pyproject(tmp_path: Path) -> None:
    dest = tmp_path / "etl-profile-app"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "etl-profile-app"
archetype = "cli"
destination = "{dest}"
profiles = ["data-etl"]
''',
        encoding="utf-8",
    )
    result = generate(
        spec_path=spec, destination=dest, run_lock=False, run_verify_tools=False
    )
    assert result.placed
    pyproject = (dest / "pyproject.toml").read_text(encoding="utf-8")
    assert "polars" in pyproject
    assert "pyarrow" in pyproject


def test_no_profile_pyproject_has_empty_dependencies(tmp_path: Path) -> None:
    dest = tmp_path / "plain-app"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "plain-app"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = generate(
        spec_path=spec, destination=dest, run_lock=False, run_verify_tools=False
    )
    assert result.placed
    pyproject = (dest / "pyproject.toml").read_text(encoding="utf-8")
    assert "dependencies = []" in pyproject


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
