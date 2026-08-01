# Example Project Specs

These TOML files are ready to use with `foundry validate`, `foundry plan`, and `foundry generate`.

| File                           | Purpose                                                                       |
| ------------------------------ | ----------------------------------------------------------------------------- |
| `minimal-cli.toml`             | Smallest valid `cli` project with no profiles.                                |
| `cli-with-http.toml`           | `cli` project plus the `http` profile (adds `httpx`).                         |
| `cli-with-hooks-hk.toml`       | `cli` project plus the `hooks-hk` profile (uses `hk` instead of pre-commit).  |
| `scripts.toml`                 | `scripts` project using PEP 723 inline metadata and `uv run`.                 |
| `data-etl.toml`                | `data-etl` archetype plus the `data-etl` profile (adds `polars` + `pyarrow`). |
| `python-foundry-template.toml` | Frozen public GitHub template cell (`cli`, no profiles, Python 3.13).         |

## Try one

```bash
uv run foundry validate --spec examples/minimal-cli.toml
uv run foundry plan   --spec examples/minimal-cli.toml --json > plan.json
uv run foundry generate --spec examples/minimal-cli.toml --dest ./out
```

Do not invent fields or profile IDs outside the closed catalog / revised spec.
