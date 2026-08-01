# Agent rules — python-foundry (product)

This is the **product** repository. Research methodology and stage machinery
live in the sibling research repo (`python-foundry`), not here.

## Authority (read before coding)

1. [`docs/02-definitive-specification-revised.md`](docs/02-definitive-specification-revised.md) — **product law**
2. [`docs/02-implementation-plan-revised.md`](docs/02-implementation-plan-revised.md) — **delivery sequence**
3. [`docs/AUTHORITY.md`](docs/AUTHORITY.md) — pinned source commits
4. This file — product workflow only

Do not invent REQs, demote locks, or treat chat history as authority.

## Current delivery position

- **Phase:** PHASE-01 — pure pipeline (write-free)
- **Exit spike:** SPK-100 / milestone **MS-001** (golden plan for minimal `cli`)
- **Not yet:** stage/place (PHASE-02), real `generate` (PHASE-03), full catalog
  content (PHASE-04), hybrid template (PHASE-05)

## Package layout (revised-spec §10.1)

```text
src/python_foundry/
  cli/       # Typer wiring only
  spec/      # parse + validate (pure)
  catalog/   # load manifests, digests
  resolve/   # archetype/profile resolution (pure)
  plan/      # Construct plan (pure)
  report/    # text/JSON encoding
  render/    # later
  fsx/       # later (PHASE-02)
  generate/  # later (PHASE-03)
  verify/    # later (PHASE-03)
catalog/     # authoring tree (packaged as data)
```

**Purity rule:** `plan` MUST NOT import `fsx`, `generate`, or `cli`.

## Product locks (never silently undo)

- ty Required; fnox+age; no dotenv secrets
- AGENTS.md + `.agents/skills/` only for Generated Projects; no Claude adapters
- Exclusive place; custom engine; closed catalog
- Generate-time `uv.lock`; verify CLI > TOML > `default`
- Optional `generate --plan` bind; unbound generate rebuilds honestly
- macOS + Linux only; no Windows

## Foundry vs Generated surfaces

Research-program skills and research `AGENTS.md` rules must **not** ship into
Generated Project emit (REQ-076). Keep product-agent docs and Generated Core
agent surface separate.

## Commands

```bash
uv sync
uv run foundry …
uv run pytest
uv run ruff check .
uv run ty check
```

## Definition of done (local)

- Tests green; no purity violations
- Phase exit criteria from the revised plan before claiming a milestone
- No secret material in Project Specs or goldens

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:970c3bf2 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   bd dolt push
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->

<!-- BEGIN BEADS CODEX SETUP: generated by bd setup codex -->
## Beads Issue Tracker

Use Beads (`bd`) for durable task tracking in repositories that include it. Use the `beads` skill at `.agents/skills/beads/SKILL.md` (project install) or `~/.agents/skills/beads/SKILL.md` (global install) for Beads workflow guidance, then use the `bd` CLI for issue operations.

### Quick Reference

```bash
bd ready                # Find available work
bd show <id>            # View issue details
bd update <id> --claim  # Claim work
bd close <id>           # Complete work
bd prime                # Refresh Beads context
```

### Rules

- Use `bd` for all task tracking; do not create markdown TODO lists.
- Run `bd prime` when Beads context is missing or stale. Codex 0.129.0+ can load Beads context automatically through native hooks; use `/hooks` to inspect or toggle them.
- Keep persistent project memory in Beads via `bd remember`; do not create ad hoc memory files.

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.
<!-- END BEADS CODEX SETUP -->


## Plan bind workflow (FND-004 / RSK-108)

Recommended agent workflow:

1. `foundry validate --spec PATH`
2. `foundry plan --spec PATH --json > plan.json` and review the plan
3. `foundry generate --spec PATH --plan plan.json`

**Trust rule:** reviewing a plan then running unbound `generate` is **not** a
two-phase commit. Only `generate --plan plan.json` binds the reviewed plan
(mismatch fails with `error_class=plan_bind` before stage writes).
