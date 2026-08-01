# MS-002 — First successful generate (thin E2E)

- **Phase:** PHASE-03
- **Date:** 2026-08-01
- **Host:** Linux

## Evidence

| Item | Location |
| ---- | -------- |
| Generate lifecycle | `python_foundry.generate.generate` |
| Lock produce/refresh | `python_foundry.generate.produce_uv_lock` |
| Verify runners | `python_foundry.verify.run_verify` |
| Network disclosure | `NETWORK_DISCLOSURE` + generate report |
| Thin e2e | `tests/test_generate.py::test_generate_full_minimal_cli` |
| SPK-103 disclosure | network text on generate output / result |

## Commands

```bash
uv run foundry generate --spec examples/minimal-cli.toml --dest /tmp/foundry-demo
uv run pytest tests/test_generate.py
```

ty remains Required in default verify (not demoted).
