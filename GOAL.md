# Goal: implement all delivery beads (dependency-ready order)

Use this file as the objective for Grok’s native `/goal` feature:

```text
/goal Implement every open beads issue in this repository until none remain open. Work one bead at a time in dependency-ready order (bd ready), never invent REQs or undo product locks, run full quality gates before each commit, then commit + push + close the bead. Close phase/root epics only after their children are closed. Goal is complete only when bd reports 0 open issues (all 48 closed) with green pytest + ruff + ty on main.
```

---

## Objective (copy into `/goal` if preferred)

Implement the full **python-foundry v1 delivery** bead graph in this product repository (`python-foundry-cli`). Deliver code and evidence until **every beads issue is closed**, including phase epics and the root epic.

**Success evidence (required for goal completion):**

1. `bd stats` (or equivalent) shows **0 open** issues; all delivery beads closed (historically 48; count may grow if follow-ups are filed — still close everything).
2. Root epic `python-foundry-cli-0b8` is closed.
3. On `main` (pushed to `origin`): `uv run pytest`, `uv run ruff check .`, and `uv run ty check` all pass.
4. No product lock silently undone (see Locks below).

Independent verification must be able to reproduce the above without trusting chat claims.

---

## Authority (do not invent product law)

Read and obey, in this precedence order:

1. Accepted `DEC-###` if any under `decisions/`
2. `docs/00-program-blueprint.md` locks and non-goals
3. **`docs/02-definitive-specification-revised.md`** — product law
4. **`docs/02-implementation-plan-revised.md`** — delivery sequence
5. `docs/AUTHORITY.md` — pinned source commits
6. `AGENTS.md` / `CLAUDE.md` — product workflow only

Do **not** invent REQs, demote locks, or treat chat history as authority.

### Product locks (never silently undo)

- ty Required in default verify
- fnox + age for secrets; **no** dotenv secret storage
- Generated Projects: AGENTS.md + `.agents/skills/` only; **no** Claude adapters / `CLAUDE.md` / `.claude/` Core emit
- Exclusive place to empty dest; fail non-empty
- Custom engine (not Copier/Cookiecutter as runtime)
- Closed catalog only
- Generate-time `uv.lock`
- Verify precedence: CLI > TOML > `default`
- Optional `--plan` bind; unbound generate rebuilds honestly
- macOS + Linux only; no Windows
- Purity: `plan` MUST NOT import `fsx`, `generate`, or `cli`

---

## Beads workflow (mandatory)

Use **bd** for all task tracking. Do **not** use TodoWrite, TaskCreate, or markdown TODO lists as the work queue.

```bash
bd prime                 # session context
bd ready                 # unblocked work
bd show <id>             # details + acceptance
bd update <id> --claim   # claim before coding
bd close <id> --reason="…"
bd dolt push             # after git push if Dolt remote is configured
```

Persistent knowledge: `bd remember` / `bd memories` — not ad hoc MEMORY.md files.

---

## Work selection (dependency-ready order)

### What to implement

- Implement **leaf tasks** (and other non-epic work units), **not** epics as coding units.
- **Epics** (`issue_type=epic`) are closed only after all of their children are closed (phase epics, then root).

### How to pick the next bead

Each cycle:

1. Run `bd ready` (and/or list open issues with no active blockers).
2. **Filter out epics** from implementation candidates.
3. Among remaining ready issues, pick **exactly one**:
   - lowest priority number first (P0 before P1 … P4),
   - then stable **id** ascending as tie-break.
4. If the only ready items are epics whose children are all closed → close those epics (childless completion), then re-run selection.
5. If nothing is ready and open work remains → inspect blockers; file residual notes; do not invent REQs. Prefer unblocking via legitimate implementation of dependencies. If stuck with no legal path, leave residual-documented open issues and keep the goal incomplete rather than false-complete.

**Never** start a blocked issue. **Never** implement two beads in the same cycle.

---

## Per-bead cycle (strict)

For the single selected bead:

### 1. Claim and understand

```bash
bd update <id> --claim
bd show <id>
```

Read acceptance/success criteria, REQs, and linked plan/spec sections. Inspect the current codebase.

### 2. Implement

- Meet the bead’s acceptance criteria fully.
- Keep changes scoped to that bead (avoid drive-by refactors).
- Respect package layout and purity rules.
- Add/update tests as required by the bead and phase testing strategy.
- If implementation reveals necessary follow-up that is **not** inventing product law: `bd create` a follow-up and leave it in the graph; do not expand silent scope without a bead.

### 3. Quality gates (required before commit)

From repo root, all must pass:

```bash
uv run pytest
uv run ruff check .
uv run ty check
```

Fix failures before committing. Do not skip gates.

### 4. Commit and push

```bash
git status
git add -A   # stage only intentional project changes; never secrets
git commit -m "$(cat <<'EOF'
<concise why-focused subject for this bead>

Closes bead <id>: <short title>
EOF
)"
git push origin HEAD
bd dolt push   # if Dolt remote configured; resolve/force only if local is known authority
```

- One commit per bead preferred (or a tight series only if hooks force a follow-up export commit).
- Do not force-push `main` unless recovering a known Dolt/git divergence you own and understand.
- No secret material in commits.

### 5. Close the bead

```bash
bd close <id> --reason="Implemented; gates green; pushed to origin."
```

Only close when acceptance criteria are actually met and gates passed.

### 6. Epic cleanup

After closing a task, if a parent epic has **all children closed**, close the epic with a clear reason. Finish with root epic `python-foundry-cli-0b8` when all phase epics are closed.

### 7. Loop

Return to **Work selection** until success evidence holds.

---

## Autonomy and stuck handling

- **Fully autonomous:** do not wait for the human operator between beads.
- **Authority-bound:** if completing a bead requires inventing unspecified product behavior or undoing a lock, **do not invent**. Record residual notes on the bead (`bd update … --notes=…`), file follow-up beads if useful, continue with other ready legal work. Prefer an incomplete honest goal over a false complete.
- Prefer fixing broken tests/code you encounter (project expects green trees) when required for gates.
- Prefer Exa MCP for web research when needed; do not treat research chat as product law.

---

## Phase awareness (guidance only)

Delivery order is enforced by bead dependencies, not by this checklist. Rough map:

| Phase | Focus | Exit signal (examples) |
| ----- | ----- | ---------------------- |
| PHASE-01 | Pure pipeline | MS-001 / SPK-100 |
| PHASE-02 | Stage + exclusive place | SPK-101 |
| PHASE-03 | Generate + lock + verify | MS-002 / SPK-103 |
| PHASE-04 | Catalog content | MS-003a → MS-DF0 → MS-003b |
| PHASE-05 | Dogfood then hybrid | MS-005 → MS-004 |
| PHASE-06 | Harden | MS-006 |

Milestone and spike acceptance text on the beads and plan remain authoritative.

---

## Non-goals for this goal run

- Opening marketplace/remote catalogs
- Windows support
- dotenv / Claude Core emit
- Demoting ty or fnox without DEC
- Closing beads without implementation or without green gates
- Parallel multi-bead coding cycles

---

## Suggested `/goal` invocation

```text
/goal Implement every open beads issue until 0 remain open. One leaf bead at a time from bd ready (exclude epics; pick lowest priority then id). Claim → implement to acceptance → uv run pytest && ruff check . && ty check → commit + push (+ bd dolt push) → bd close. Close epics only after all children are closed. Obey docs/02-definitive-specification-revised.md + docs/02-implementation-plan-revised.md; never invent REQs or undo locks. Complete only when all beads are closed and full gates are green on origin/main.
```

Optional token budget (host-specific):

```text
/goal <objective above> --budget <tokens>
```

---

## Operator controls

```text
/goal status
/goal pause
/goal resume
/goal clear
```
