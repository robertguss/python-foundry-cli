"""SPK-002: frozen practical Core ty config in generated projects."""

from __future__ import annotations

from pathlib import Path

from python_foundry.generate import generate


def test_spk002_ty_config_present_in_core_emit(tmp_path: Path) -> None:
    dest = tmp_path / "ty-cli"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "ty-cli"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    generate(spec_path=spec, destination=dest, run_verify_tools=False, run_lock=True)
    pyproject = (dest / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.ty.environment]" in pyproject
    assert 'python-version = "3.13"' in pyproject
    # No dotenv secrets patterns.
    assert "dotenv" not in pyproject.lower()
    agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
    assert "fnox" in agents.lower() or "quality" in agents.lower()
    skill = dest / ".agents/skills/quality-gates/SKILL.md"
    assert skill.is_file()
    assert "ty check" in skill.read_text(encoding="utf-8")


def test_spk002_fnox_toml_present_and_dod_stated(tmp_path: Path) -> None:
    """REQ-058 fnox.toml present + gitignored keys; REQ-074 DoD language."""
    dest = tmp_path / "fnox-cli"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "fnox-cli"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    generate(spec_path=spec, destination=dest, run_verify_tools=False, run_lock=True)

    fnox_toml = dest / "fnox.toml"
    assert fnox_toml.is_file()
    fnox_text = fnox_toml.read_text(encoding="utf-8")
    assert "[providers.age]" in fnox_text
    assert 'type = "age"' in fnox_text
    assert "load_dotenv" not in fnox_text

    gitignore = (dest / ".gitignore").read_text(encoding="utf-8")
    assert "age.txt" in gitignore or ".age/" in gitignore

    agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
    assert "definition of done" in agents.lower()
    assert "0 tests collected is not success" in agents

    skill = (dest / ".agents/skills/quality-gates/SKILL.md").read_text(encoding="utf-8")
    assert "definition of done" in skill.lower()
    assert "0 tests collected is not success" in skill
