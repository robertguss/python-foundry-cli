"""Regenerate frozen public template cell and fail on golden drift (REQ-081)."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

# Paths / directory names never compared (local tool state, not catalog SoT).
IGNORE_DIR_NAMES = frozenset(
    {
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        ".git",
    }
)


class HybridSnapshotError(Exception):
    """Snapshot generation or drift failure."""

    error_class: str = "internal"

    def __init__(self, message: str, *, code: str = "hybrid.drift") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


def collect_tree(root: Path) -> dict[str, bytes]:
    """Collect relative path → file bytes, skipping ignored dirs."""
    root = root.resolve()
    if not root.is_dir():
        raise HybridSnapshotError(
            f"snapshot root is not a directory: {root}",
            code="hybrid.missing_root",
        )
    out: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in IGNORE_DIR_NAMES for part in rel_parts):
            continue
        rel = path.relative_to(root).as_posix()
        out[rel] = path.read_bytes()
    return out


def write_tree(root: Path, files: dict[str, bytes]) -> None:
    """Write a path→bytes map under *root* (replaces root if present)."""
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for rel, data in sorted(files.items()):
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def compare_trees(
    actual: dict[str, bytes],
    expected: dict[str, bytes],
) -> list[str]:
    """Return human-readable drift findings (empty means match)."""
    findings: list[str] = []
    actual_keys = set(actual)
    expected_keys = set(expected)

    for rel in sorted(expected_keys - actual_keys):
        findings.append(f"missing in generated snapshot: {rel}")
    for rel in sorted(actual_keys - expected_keys):
        findings.append(f"unexpected in generated snapshot: {rel}")
    for rel in sorted(actual_keys & expected_keys):
        if actual[rel] != expected[rel]:
            a = hashlib.sha256(actual[rel]).hexdigest()[:12]
            e = hashlib.sha256(expected[rel]).hexdigest()[:12]
            findings.append(
                f"content drift: {rel} (generated={a} golden={e})"
            )
    return findings


def check_hybrid_snapshot(
    *,
    spec_path: Path,
    golden_dir: Path,
    work_dir: Path,
    run_verify_tools: bool = True,
) -> list[str]:
    """Generate frozen cell into *work_dir* and diff against *golden_dir*.

    Returns findings list (empty on success). Raises HybridSnapshotError only
    for operational failures (missing golden, generate failure). Callers that
    want fail-closed CI should treat non-empty findings as hard failure.
    """
    from python_foundry.generate import GenerateError, generate

    if not golden_dir.is_dir():
        raise HybridSnapshotError(
            f"missing hybrid golden tree: {golden_dir}",
            code="hybrid.missing_golden",
        )
    if not spec_path.is_file():
        raise HybridSnapshotError(
            f"missing frozen public template spec: {spec_path}",
            code="hybrid.missing_spec",
        )

    work_dir.mkdir(parents=True, exist_ok=True)
    dest = work_dir / "python-foundry-template"
    if dest.exists():
        shutil.rmtree(dest)

    try:
        generate(
            spec_path=spec_path,
            destination=dest,
            run_lock=True,
            run_verify_tools=run_verify_tools,
        )
    except GenerateError as exc:
        raise HybridSnapshotError(
            f"hybrid generate failed: {exc.message}",
            code="hybrid.generate",
        ) from exc

    actual = collect_tree(dest)
    expected = collect_tree(golden_dir)
    return compare_trees(actual, expected)


def assert_no_drift(findings: list[str]) -> None:
    if findings:
        body = "\n".join(f"  - {f}" for f in findings)
        raise HybridSnapshotError(
            "hybrid template snapshot drifted from catalog goldens:\n" + body,
            code="hybrid.drift",
        )
