# Command Reference

The `foundry` CLI is organized as subcommands. Every command supports `--help`.

## Global options

```text
--install-completion   Install shell completion.
--show-completion      Show shell completion script.
--help                 Show help and exit.
```

## `foundry version`

Print the package version and the catalog digest.

```bash
foundry version
```

Example output:

```text
foundry 0.1.0
catalog_digest 5bb52e34952a44b588948aa0ab0413d011b62617975608112d4e13d79f94d06c
```

The catalog digest is part of every Generation Plan, so `version` is useful for debugging mismatches.

## `foundry validate`

Validate a Project Spec without writing anything.

```bash
foundry validate --spec PATH
```

| Option | Description |
| ------ | ----------- |
| `--spec PATH` | Path to the Project Spec, or `-` to read from stdin. Required. |
| `--json` | Emit a machine-readable JSON report. |

Use this to catch spec errors before planning or generating. It returns exit code `0` when the spec is valid and `non-zero` otherwise.

JSON report shape (on success):

```json
{
  "ok": true,
  "spec": { ... }
}
```

## `foundry plan`

Construct a Generation Plan from a spec. This also does not write to the destination.

```bash
foundry plan --spec PATH [--json] [--verify MODE]
```

| Option | Description |
| ------ | ----------- |
| `--spec PATH` | Path to the Project Spec, or `-`. Required. |
| `--json` | Emit the sealed Generation Plan as JSON. |
| `--verify MODE` | Override verify mode: `default`, `strict`, or `none`. |

The plan is a complete contract: it lists every file that will be rendered, the dependencies that will be locked, and the external steps that `generate` will run.

## `foundry generate`

Generate the project: stage, lock, verify, and place.

```bash
foundry generate --spec PATH [--dest PATH] [--plan FILE] [--verify MODE] [--json]
```

| Option | Description |
| ------ | ----------- |
| `--spec PATH` | Path to the Project Spec, or `-`. Required. |
| `--dest PATH` | Override the destination path from the spec. |
| `--plan FILE` | Bind a previously saved Generation Plan. Strongly recommended for two-phase workflows. |
| `--verify MODE` | Override verify mode: `default`, `strict`, or `none`. |
| `--json` | Emit a machine-readable JSON report. |

Behavior:

- The destination must be empty or non-existent. `foundry` never merges into an existing directory.
- Files are rendered into a sibling staging directory first.
- `uv.lock` is refreshed to match the resolved dependencies.
- The selected verify tier runs in the stage.
- On success, the stage is moved to the destination.
- On failure, the stage is preserved and the destination is untouched. The JSON report includes the absolute `stage_path`.

### Plan binding

Review a plan, then bind it to guarantee `generate` runs exactly that plan:

```bash
foundry plan --spec my.toml --json > plan.json
# review plan.json
foundry generate --spec my.toml --plan plan.json --dest ./out
```

If the recomputed plan does not match the saved plan, `generate` fails before writing anything.

## `foundry catalog`

Inspect the closed catalog that ships with `foundry`.

### `foundry catalog list`

List every catalog unit with its kind and id.

```bash
foundry catalog list
foundry catalog list --json
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

### `foundry catalog show`

Show one catalog unit by its kind-qualified reference.

```bash
foundry catalog show archetype/cli
foundry catalog show profile/http --json
```

Refs use the form `{kind}/{id}`, e.g. `archetype/cli`, `profile/http`, `core/core`.

## Exit codes

- `0`: success.
- `non-zero`: failure. JSON mode includes `error_class` when available.
