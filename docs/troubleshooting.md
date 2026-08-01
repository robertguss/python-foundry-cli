# Troubleshooting

## `foundry validate` fails

### Unknown key

```text
error_class=spec_validation
```

Only the documented Project Spec fields are allowed. Check the [Project Spec Reference](spec-reference.md) for the allowed keys.

### Unknown archetype or profile

```text
error_class=resolution
```

`archetype` must be one of `cli`, `scripts`, or `data-etl`. Profile ids must come from the closed catalog. Run:

```bash
foundry catalog list
```

### Duplicate profile

`profiles` is treated as a set. Remove duplicates.

## `foundry generate` fails to place

### Destination already exists

`foundry` refuses to overwrite a non-empty destination. Move or remove the directory first, or choose a different `destination`.

### Verify failure

If you see a verify-step failure in the JSON report, inspect the stage path in the report:

```json
{
  "ok": false,
  "stage_path": "/absolute/path/to/.foundry-stage-..."
}
```

Navigate to that directory and run the failing command manually. Common causes:

- `uv sync --locked` failed because `uv.lock` is stale. Remove the stage and re-run `generate`.
- `ruff check .` or `ruff format --check .` failed because rendered files do not match expectations. Report this as a bug.
- `ty check` failed because of type errors in generated code.

## Plan bind mismatch

When using `--plan plan.json`, `generate` recomputes the plan and compares `plan_sha256`, catalog digest, and foundry version. If any changed, you will see:

```text
error_class=plan_bind
```

Regenerate the plan:

```bash
foundry plan --spec my.toml --json > plan.json
# review the new plan
foundry generate --spec my.toml --plan plan.json --dest ./out
```

## Network issues during generate

`generate` runs `uv lock` and, for `default`/`strict` verify, `uv sync --locked`. These may need network access to PyPI. If you are offline, ensure you have a warm uv cache or use `--verify none` and run the lock step later:

```bash
foundry generate --spec my.toml --dest ./out --verify none
```

Note that `--verify none` still attempts lock production. It only skips the post-lock tooling checks.

## `foundry` not found

After installation, make sure the tool binary directory is on your PATH. With uv:

```bash
uv tool update-shell
```

Or run via the package:

```bash
uv run --with python-foundry foundry version
```

## Getting help

Run `foundry --help` and `foundry <command> --help` for the most current option reference.
