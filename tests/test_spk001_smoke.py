"""SPK-001: uv+ruff+ty+pytest smoke on generated minimal trees."""

from __future__ import annotations

import subprocess
from pathlib import Path

from python_foundry.generate import generate

REPO = Path(__file__).resolve().parents[1]


def test_spk001_tools_green_on_generated_minimal(tmp_path: Path) -> None:
    dest = tmp_path / "smoke-cli"
    spec = tmp_path / "cell.toml"
    spec.write_text(
        f'''
schema = 1
name = "smoke-cli"
description = "SPK-001 sample"
archetype = "cli"
destination = "{dest}"
profiles = []
''',
        encoding="utf-8",
    )
    result = generate(spec_path=spec, destination=dest)
    assert result.placed
    assert (dest / "uv.lock").is_file()

    # Explicit second-pass smoke (generate already ran default verify once).
    for argv in (
        ["uv", "sync", "--locked"],
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "ruff", "format", "--check", "."],
        ["uv", "run", "ty", "check"],
        ["uv", "run", "pytest"],
    ):
        proc = subprocess.run(
            argv, cwd=dest, capture_output=True, text=True, check=False
        )
        assert proc.returncode == 0, f"{argv} failed: {proc.stderr or proc.stdout}"
