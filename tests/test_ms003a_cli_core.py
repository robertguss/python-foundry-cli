"""MS-003a full-Core cli golden emit + forbidden-path suite."""

from __future__ import annotations

from pathlib import Path

from python_foundry.generate import generate


def test_ms003a_cli_core_emit_surface(tmp_path: Path) -> None:
    dest = tmp_path / "core-cli"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "core-cli"
description = "MS-003a full Core cli"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = generate(spec_path=spec, destination=dest)
    assert result.placed
    assert result.verify_mode == "default"

    # Core toolchain surface
    assert (dest / "pyproject.toml").is_file()
    assert (dest / "uv.lock").is_file()
    assert (dest / "AGENTS.md").is_file()
    assert (dest / ".python-version").is_file()
    assert (dest / ".pre-commit-config.yaml").is_file()
    assert (dest / ".github/workflows/ci.yml").is_file()
    assert (dest / ".agents/skills/quality-gates/SKILL.md").is_file()
    assert (dest / ".agents/skills/secrets-fnox/SKILL.md").is_file()
    assert (dest / ".agents/skills/add-cli-command/SKILL.md").is_file()
    assert (dest / "src/core_cli/cli.py").is_file()

    pyproject = (dest / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.ty.environment]" in pyproject
    assert "ty" in pyproject

    secrets = (dest / ".agents/skills/secrets-fnox/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "fnox" in secrets.lower()
    assert "dotenv" not in secrets.lower() or "not" in secrets.lower()

    # Forbidden-path assertions for the cli archetype now live in
    # tests/test_forbidden_paths.py to avoid duplication with SPK-102 coverage.
