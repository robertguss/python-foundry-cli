"""CLI: ``python -m python_foundry.hybrid`` — regenerate + fail on drift."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from python_foundry.hybrid.snapshot import (
    HybridSnapshotError,
    assert_no_drift,
    check_hybrid_snapshot,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m python_foundry.hybrid",
        description=(
            "Regenerate frozen public template cell and fail if it drifts "
            "from checked-in catalog goldens (REQ-081 / MS-004)."
        ),
    )
    parser.add_argument(
        "--spec",
        type=Path,
        default=Path("examples/python-foundry-template.toml"),
        help="Frozen public template Project Spec (REQ-089).",
    )
    parser.add_argument(
        "--golden",
        type=Path,
        default=Path("tests/goldens/hybrid-python-foundry-template"),
        help="Checked-in golden snapshot tree.",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=None,
        help="Working directory for generate (default: temp dir).",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip default verify runners (still produces uv.lock).",
    )
    args = parser.parse_args(argv)

    work = args.work_dir
    tmp: tempfile.TemporaryDirectory[str] | None = None
    if work is None:
        tmp = tempfile.TemporaryDirectory(prefix="foundry-hybrid-")
        work = Path(tmp.name)

    try:
        findings = check_hybrid_snapshot(
            spec_path=args.spec,
            golden_dir=args.golden,
            work_dir=work,
            run_verify_tools=not args.skip_verify,
        )
        assert_no_drift(findings)
    except HybridSnapshotError as exc:
        print(f"hybrid snapshot check failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if tmp is not None:
            tmp.cleanup()

    print("hybrid snapshot: ok (matches catalog goldens)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
