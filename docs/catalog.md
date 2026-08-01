# Catalog Reference

`foundry` ships with a closed catalog. You cannot add user-defined archetypes or profiles in v1. Use the catalog commands to discover what is available.

## List the catalog

```bash
foundry catalog list
```

Output:

```text
archetype/cli	Conventional CLI project archetype (Typer entrypoint)
archetype/data-etl	Data/ETL project archetype (src package; distinct from profile/data-etl)
archetype/scripts	Scripts-oriented project archetype (PEP 723 + uv run)
core/core	Core toolchain, layout, quality gates, secrets, CI, and AGENTS for every Generated Project
profile/data-etl	Data/ETL tooling profile (polars+pyarrow; distinct from archetype/data-etl)
profile/hooks-hk	hk hooks profile (replaces default pre-commit emit)
profile/http	HTTP client profile (httpx)
```

Use `--json` for machine-readable output.

## Show one unit

```bash
foundry catalog show archetype/cli
foundry catalog show profile/http --json
foundry catalog show core/core
```

Catalog references are **kind-qualified**: `{kind}/{id}`.

| Kind | Meaning |
| ---- | ------- |
| `core` | The Core unit every project receives. |
| `archetype` | A project archetype; exactly one is required. |
| `profile` | An optional capability profile. |

## Why kind-qualified ids?

Some ids exist in more than one kind. For example, `data-etl` is both an archetype and a profile. The CLI always shows `archetype/data-etl` and `profile/data-etl` as separate units so there is no ambiguity.

In a Project Spec, the meaning is already unambiguous because archetypes go in the `archetype` field and profiles go in the `profiles` array:

```toml
archetype = "data-etl"        # this is the archetype
profiles = ["data-etl"]         # this is the profile
```

## Catalog digest

Every Generation Plan records the catalog digest. Run `foundry version` to see the current digest:

```bash
foundry version
```

If a saved plan is bound with `--plan`, `generate` will fail if the catalog digest (or foundry version) changed since the plan was created. This prevents silent behavior drift.
