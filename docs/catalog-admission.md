# Catalog admission process dry-run (REQ-044)

1. Propose unit under `catalog/` (or package data tree) with manifest `schema=1`, kind, id, files.
2. Run `uv run foundry catalog list` / `catalog show kind/id`.
3. Construct plan for a representative cell; regenerate goldens if digest changes.
4. Forbidden-path suite must stay green.
5. No remote marketplace / plugin discovery in v1.
