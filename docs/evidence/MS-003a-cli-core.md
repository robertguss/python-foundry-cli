# MS-003a — full-Core `cli` golden emit

- **Date:** 2026-08-01
- **Test:** `tests/test_ms003a_cli_core.py`
- **Prereqs:** SPK-001, SPK-002, SPK-052 complete

## Surface claims

| Surface | Present |
| ------- | ------- |
| uv + generate-time `uv.lock` | yes |
| ruff / ty / pytest | yes (default verify) |
| pre-commit default | yes |
| GHA CI | yes |
| AGENTS.md | yes |
| skills: quality-gates, secrets-fnox, add-cli-command | yes |
| Forbidden: CLAUDE.md, .claude, dotenv secrets | absent |

Continuous CI must keep this suite green through MS-003b.
