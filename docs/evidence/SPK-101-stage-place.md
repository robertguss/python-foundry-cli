# SPK-101 — Stage + exclusive place

- **Phase:** PHASE-02
- **Date:** 2026-08-01
- **Host:** Linux

## Evidence

| REQ | Coverage |
| --- | -------- |
| REQ-030 fail non-empty dest | `tests/test_fsx.py`, `tests/test_spk101_e2e.py` |
| REQ-031 sibling stage + exclusive place | `python_foundry.fsx.create_stage` / `exclusive_place` |
| REQ-032 path confinement | `python_foundry.fsx.confine_path` |
| REQ-090 stage identity + absolute `stage_path` | `Stage.absolute_path`; collision allocates new name |

Automated e2e: `uv run pytest tests/test_spk101_e2e.py`.

## Agent recovery notes

On generate failure:

1. Destination is **never** partially written (exclusive place only on success).
2. Inspect absolute `stage_path` in the error report (JSON field / text).
3. Stage directories are named `.foundry-stage-<dest-basename>-<unique>` as
   siblings of the destination under the same parent.
4. Prior failed stages are **not** deleted; each failure allocates a new unique
   name. Operators may remove old stages after investigation.
5. Empty destination directories are placeable; non-empty destinations hard-fail.

## PHASE-03 readiness

`generate` orchestration may call:

```python
from python_foundry.fsx import create_stage, exclusive_place, confine_path
```
