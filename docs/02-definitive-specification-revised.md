# Revised Definitive Specification — python-foundry

- **Artifact type:** Revised definitive specification
- **Program:** python-foundry
- **Status:** Accepted — implementation authority
- **Version:** 0.2
- **Created (synthesis base):** 2026-08-01
- **Actual revision date:** 2026-08-01
- **Last updated:** 2026-08-01
- **Base artifact:** `docs/specifications/01-definitive-specification.md` v0.1 (accepted proposed)
- **Accepted review:** `docs/reviews/01-specification-adversarial-review.md` v0.1 (`9d11cd8`)
- **Commissioning prompt:** `docs/prompts/06-specification-revision-prompt.md`
- **Stage:** `spec-revision` (program acceptance pending human + `accepted_commit`)
- **Validation:** Pending independent validation
- **Implementation status:** Not started (research program artifact; this document is product implementation authority once the stage is human-accepted)
- **Depends on:** Accepted Blueprint; Accepted Charter; Accepted reports 01–03; Accepted proposed specification; Accepted adversarial review (FND-001..012)
- **Requirement range:** REQ-001..REQ-083 retained (sparse); **REQ-084..REQ-091** added this revision; REQ-092..REQ-299 reserved
- **Finding dispositions:** FND-001..FND-012 (see §R2)

> Revision integrates accepted adversarial-review corrections into a coherent
> standalone product law. Load-bearing locks (ty, fnox+age, no dotenv secrets,
> AGENTS.md-only, no Claude adapters, exclusive place, closed catalog, custom
> engine) are preserved. Prefer simplification over new machinery.

---

## R1. Revision Summary

This revision elevates the proposed definitive specification to **implementation
authority** by closing control-plane gaps that made agent-facing generate
behavior non-total:

1. **Effective verify resolution** (CLI > TOML > default) with plan recording.
2. **Profile composition order** frozen (catalog order; TOML membership-only).
3. **`uv.lock` lifecycle** at generate (produce/refresh to match resolution).
4. **Plan binding** via optional `generate --plan` with digest hard-fail; honest
   rebuild-only path when unbound.
5. Align **default verify success** language with pytest/DoD (no overclaim).
6. **Strict verify** drops pre-commit pre-place (pytest only beyond default).
7. **data-etl dual IDs** mitigated with kind-qualified catalog/plan UX.
8. **scripts archetype** emit/test/lock contract made normative.
9. **`plan_sha256` canonicalization** algorithm frozen + test-vector requirement.
10. **Public GitHub template** Project Spec cell frozen.
11. **Stage identity** naming, collision, and error path norms.
12. **Machine-readable error taxonomy** for plan/generate JSON failures.

No Critical findings existed. All High findings are **Accepted** or **Accepted
with modification**. Artifact status: **Accepted — implementation authority**.

---

## R2. Finding Disposition Ledger

| FND | Severity | Disposition | Integration |
| --- | -------- | ----------- | ----------- |
| FND-001 | High | **Accepted** | §9.5, §11.1, §13.1, REQ-080, REQ-084 |
| FND-002 | High | **Accepted** | §9.7, §11.1, REQ-043 |
| FND-003 | High | **Accepted with modification** | §11.4, §9.5, REQ-052, REQ-085 (generate-time lock refresh; not closed-matrix-only) |
| FND-004 | High | **Accepted with modification** | §9.2–9.3, §13.1, REQ-024, REQ-086 (optional `--plan` bind; rebuild path honesty) |
| FND-005 | Medium | **Accepted** | §5.1, §9.5, §13.5, REQ-074, REQ-080 |
| FND-006 | Medium | **Accepted** | §9.5, REQ-080 (strict = default + pytest; no pre-commit pre-place) |
| FND-007 | Medium | **Accepted with modification** | §9.6–9.7, §11.3, §12.1, REQ-087 (kind-qualified IDs; keep string ids) |
| FND-008 | Medium | **Accepted** | §12.3, REQ-053, REQ-056, REQ-088 |
| FND-009 | Medium | **Accepted** | §9.3, REQ-026 |
| FND-010 | Medium | **Accepted** | §9.9, REQ-081, REQ-089 |
| FND-011 | Low | **Accepted** | §9.4, §15, REQ-031, REQ-090 |
| FND-012 | Low | **Accepted** | §12.1, REQ-091 |

**Count check:** 12 / 12 dispositioned; none silent.

---

## R3. Integrated Correction Ledger

| Theme | Spec change |
| ----- | ----------- |
| Verify precedence | Effective mode = CLI flag if set, else TOML `verify`, else `default`; plan records `verify_mode` + `verify_source` |
| Profile order | TOML `profiles` is a **set** (duplicates fail); apply order = catalog total order |
| Lockfile | After render, generate MUST produce/refresh `uv.lock` for resolved inputs before default/strict verify; verify uses locked sync |
| Plan bind | `generate --plan FILE` optional; must match recomputed plan_sha256 + catalog digest + foundry version or hard-fail before stage writes; unbound generate rebuilds and docs forbid two-command trust without `--plan` |
| Runnable language | Default verify success = sync+ruff+ty green; **not** pytest; agent DoD still requires pytest after place |
| Strict | default + pytest (+ cov if configured); **not** pre-commit in pre-place verify |
| data-etl dual | Keep ids; catalog list/show and plan use `kind` + `id`; docs/examples disambiguate |
| scripts | Normative inventory: PEP 723 scripts dir, uv project+lock, tests policy, no mandatory src package |
| plan_sha256 | UTF-8 JSON, sorted keys, no insignificant whitespace, SHA-256 hex of preimage |
| Public template | Frozen cell: archetype `cli`, profiles `[]`, python 3.13, name `python-foundry-template` |
| Stage | Naming pattern, collision → new unique name, MUST emit absolute `stage_path` on failure |
| Errors | Closed `error_class` set on JSON failure reports |

---

## R4. Preserved Strengths

- Closed Core + closed agent surface (AGENTS.md + `.agents/skills` only)
- Plan-as-contract purity + exclusive place fail-closed writes
- User decisions honored (ty, fnox+age, no dotenv secrets, no Claude adapters)
- Full REC disposition ledger (carried; no tool re-selection)
- Hybrid GitHub template with single catalog SoT
- Non-interactive first; forbidden-path discipline
- Sparse thematic REQ IDs retained for stable subjects

---

## 1. Artifact Metadata


| Field | Value |
| ----- | ----- |
| Program ID | python-foundry |
| Stage ID | `spec-revision` |
| Product name | **python-foundry** (installable package / repo) |
| Spec version | **0.2** (revised) |
| Base proposed | v0.1 (`01-definitive-specification.md`) |
| CLI binary (provisional) | **`foundry`** (owner may rename via branding; package remains `python-foundry`) |
| Operator | robertguss |
| Rigor | standard |
| Host OS | macOS + Linux only |
| Primary implementers | AI coding agents honoring `AGENTS.md` + `.agents/` |

---

## 2. Executive Decision Summary

**python-foundry** is a personal, open-sourceable **hybrid foundry** for modern
Python projects:

1. A **Python/`uv` CLI** that turns a declarative **TOML Project Spec** into a
   complete repository via **`validate` → `plan` → `generate`**.
2. A **strong default Core** (toolchain, layout, quality gates, secrets, CI,
   agent surface) emitted as **invariants** into every Generated Project.
3. Optional **closed profiles** (`http`, `hooks-hk`, `data-etl`) and exactly one
   **archetype** (`cli` | `scripts` | `data-etl`).
4. A **GitHub template** surface that is a **generated snapshot** of the catalog
   (not a second source of truth).
5. **AI-native** operability: root **`AGENTS.md` only**, skills under
   **`.agents/skills/` only**, MCP default **none**, secrets via **fnox + age**,
   **no** dotenv secret storage, **no** Claude Code adapters.

| Decision area | Spec decision |
| ------------- | ------------- |
| Engine | Custom planner-led renderer (**not** Copier/Cookiecutter runtime) |
| Spec | TOML `schema = 1`; non-interactive; hard-fail unknown keys/profiles |
| Plan | **Plan-as-contract** (immutable Construct; optional `--plan` bind; unbound generate rebuilds) |
| Verify resolution | CLI `--verify` overrides TOML; else TOML; else `default` |
| Lockfile | Generate produces/refreshes `uv.lock` to match resolution before default/strict verify |
| Writes | Sibling stage → tiered verify → **exclusive place**; fail if dest non-empty |
| Core tools | uv, Ruff, **ty**, pytest, pre-commit Default, **fnox+age**, GHA |
| Python | Floor **3.12**; default pin **3.13** |
| Agent surface | AGENTS.md + closed skills; amplify REC-013 command surface |
| go-foundry | Adopt/Adapt/Reject per architecture REC-210 (prior art only) |

**Chief Architect freezes (formerly open):**

| ID | Resolution |
| -- | ---------- |
| OQ-101 | Default verify mode = **`default`** (sync + ruff + ty before place) |
| OQ-100 | Minimum TOML field set frozen in §11; extension only via schema bump |
| OQ-104 | Generated Projects (v1 apps) **MUST commit `uv.lock`** |
| OQ-105 | Provisional CLI name **`foundry`**; package **`python_foundry` / python-foundry** |
| OQ-001 | Documented command **`uv run ty check`**; config under pyproject per ty docs at implement time |
| OQ-003 | **Keep** pre-commit Default; do **not** force hk Core |
| OQ-004 | **Keep** data-etl profile default **polars + pyarrow** |
| OQ-005 | macOS CI **optional** (Linux required) |
| OQ-102 | JSON plan to stdout/file is **Optional** flag; not required on-disk under `.foundry/` by default; `generate --plan` binds a plan artifact when supplied |
| OQ-REV-verify | Effective verify = CLI > TOML > `default` (FND-001) |
| OQ-REV-profiles | Profile apply order = catalog order; TOML array is membership set (FND-002) |
| OQ-103 | data-etl archetype emits **`add-script`** skill (no separate `data-etl-entry` skill in v1 Core) |
| OQ-052 | v1 **does not** emit `.cursor/rules` by default |
| OQ-053 | **No** MCP profile in v1 |
| OQ-055 | Package/CLI templates **MUST** include ≥1 smoke test; “0 tests collected” is not success |

---

## 3. Authority and Intended Use

### 3.1 Precedence (highest first)

1. Accepted `DEC-###` (none at revision time)
2. Program Blueprint (`docs/00-program-blueprint.md`)
3. Research Charter methodology
4. Revision commissioning prompt (`06-specification-revision-prompt.md`)
5. **This revised specification** — **implementation authority** for product v1
   once the `spec-revision` stage is human-accepted in the program manifest
6. Accepted proposed specification v0.1 (historical base; superseded where this
   document differs)
7. Accepted adversarial review (finding provenance; dispositions in §R2)
8. Accepted research reports (evidence + recommendation provenance)
9. Implementation plans (downstream; must not contradict this document)
10. `research-program.toml` (index only)

### 3.2 Intended use

- **Implementation** of the product MUST follow this revised specification and an
  accepted implementation plan (downstream program stage).
- **This research repository** is not the product implementation repo; bounded
  spikes may still live under `docs/evidence/`.
- The proposed specification (`01-…`) remains citable history; **this file wins**
  on conflict after stage acceptance.

### 3.3 Standalone rule

An implementer with this specification plus official tool docs for locked tools
(uv, ruff, ty, pytest, fnox, Typer, GitHub Actions) MUST be able to build v1
without chat history or re-reading research digests alone. Reports remain
citable evidence for *why*.

---

## 4. Problem and Product Definition

### 4.1 Problem

Starting each Python project re-establishes the same packages, layout, quality
tooling, hooks, secrets, CI, and agent-operable structure. That costs time,
produces inconsistent bases, and forces re-explaining conventions to AI coding
agents (primary implementers). One-shot scaffolds do not encode a closed,
research-backed Core plus dry-run generation and AI-native surfaces.

### 4.2 Product

**python-foundry** ships:

| Surface | Description |
| ------- | ----------- |
| Foundry CLI | Installable Python package providing validate/plan/generate/catalog/version |
| Closed catalog | Package data: core + archetypes + profiles + version pins |
| Generated Projects | Repositories produced by generate (or from GitHub template snapshot) |
| GitHub template | Fixed default snapshot generated from catalog (hybrid UX) |

### 4.3 Users

| Role | Relationship |
| ---- | ------------ |
| Primary operator | Owner (robertguss) |
| Primary implementers | AI agents (Grok, Cursor, Codex, and similar) |
| Secondary | Open-source readers (not v1 design focus) |
| Out of scope v1 | Multi-tenant orgs, marketplaces, Windows users, Claude Code as design target |

---

## 5. Goals and Non-Goals

### 5.1 Goals

1. Hybrid foundry: generator CLI + strong Core + GitHub template surface.
2. Evidence-backed modern Python Core for CLI, scripts, and data/ETL (no notebooks).
3. AI-native operability without oral tradition.
4. Adapt go-foundry patterns where they fit Python/uv; reject blind copy.
5. Produce implementation-ready REQs and high-level phases (this document).
6. Fast path: empty directory → validate/plan → generate → **tooling-verified**
   project (default verify: uv sync + ruff + ty). **Pytest green is agent DoD
   after place**, not implied by default generate success (FND-005).

### 5.2 Non-goals (MUST NOT become v1 scope without DEC / Blueprint amendment)

1. Multi-user / org template marketplace.
2. Framework zoo (every web/ML stack).
3. Notebooks, GUI apps, mobile.
4. **Windows** support.
5. Unlimited MCP/skill catalogs.
6. New package managers (uv is assumed).
7. Granular coding backlog as a program output.
8. Full product implementation inside the research program beyond spikes.
9. Existing-project update/merge/sync as a v1 generate path.
10. Claude Code adapters (`CLAUDE.md`, `.claude/`) as Core emit.
11. Dotenv / `.env` as secret storage.
12. Copier or Cookiecutter as the foundry **runtime engine**.

---

## 6. Locked Decisions and Invariants

These are **product invariants**. Generator, catalog, docs, and skills MUST NOT
silently undo them.

### 6.1 Blueprint locks

| ID | Invariant |
| -- | --------- |
| L1 | Hybrid product shape |
| L2 | Foundry is Python/`uv` (dogfood) |
| L3 | macOS + Linux only |
| L4 | Latest practical Python; floor/default per ecosystem |
| L6 | Archetypes CLI + scripts; data/ETL; no notebooks |
| L7 | GitHub Actions in Generated Project Core |
| L8 | uv project + console scripts for v1 |
| L9 | AI-native first; closed agent tooling |
| L10 | go-foundry adapt, do not copy blindly |

### 6.2 Generated Project Core locks

| Layer | Invariant |
| ----- | --------- |
| Python | `requires-python >= 3.12`; default pin **3.13** |
| Tooling | **uv** + committed **`uv.lock`** (v1 Generated Projects) |
| Layout | **src/** packages; tests at top-level `tests/`; scripts PEP 723 + `uv run` |
| Lint/format | **Ruff** check + format |
| Types | **ty** Required (User decision; residual RSK-002) |
| Tests | **pytest** Required; pytest-cov Default |
| Hooks | **pre-commit** Default; **hk** only via `hooks-hk` profile |
| Secrets | **fnox** Required; provider **age**; **no** `.env` secret storage |
| CI | GHA + setup-uv + ruff + ty + pytest; Linux required; macOS optional |
| CLI framework | **Typer** Default for `cli` archetype |
| Commands | REC-013 surface (see §13) |

### 6.3 AI-native locks

| Layer | Invariant |
| ----- | --------- |
| Instructions | Root **`AGENTS.md` only** |
| Skills | **`.agents/skills/<name>/SKILL.md` only** |
| MCP | Default **none** committed |
| Forbidden | `CLAUDE.md`, `.claude/`, kitchen-sink MCP, dotenv secret templates |
| Diagnostics | Ruff + ty LSP for editors; **CLI** for agent DoD |
| Secrets protocol | `fnox exec -- …` |

### 6.4 Architecture locks

| Layer | Invariant |
| ----- | --------- |
| Lifecycle | `validate` / `plan` / `generate` (+ catalog list/show, version) |
| Spec | TOML Project Spec `schema = 1` |
| Plan | Plan-as-contract |
| Writes | Stage → verify → exclusive place |
| Catalog | Closed; no remote/plugin marketplace |
| Engine | Custom planner-led |
| Template | Generated snapshot from catalog SoT |
| Emit | Core + AI-native as **always-on** for successful plans |

---

## 7. Final Technology Stack

### 7.1 Foundry product (dogfood Core)

| Concern | Choice |
| ------- | ------ |
| Language | Python ≥3.12 / pin 3.13 |
| Project tool | uv |
| CLI framework | Typer |
| Lint/format | Ruff |
| Types | ty |
| Tests | pytest (+ cov default) |
| Secrets | fnox + age (where secrets used) |
| Packaging | Installable package `python-foundry`; console script **`foundry`** |

### 7.2 Generated Project Core

Same as §6.2. Profiles add:

| Profile | Stack |
| ------- | ----- |
| `http` | httpx (sync default for CLI/scripts) |
| `hooks-hk` | hk (replaces default pre-commit hook files per catalog rules) |
| `data-etl` | polars + pyarrow; extras duckdb, pandas documented as opt-in |

### 7.3 Explicitly not Core

Poetry/PDM/Hatch as Default; Pyright/mypy as Default typechecker; black/isort/flake8 as Default; dotenv secrets; Windows toolchains; notebook stacks; web frameworks.

---

## 8. System Context

```text
┌─────────────────┐     TOML Project Spec      ┌──────────────────┐
│ Operator/Agent  │ ─────────────────────────► │  foundry CLI     │
└─────────────────┘                            │  validate/plan/  │
                                               │  generate        │
┌─────────────────┐     closed package data    │                  │
│ Catalog (embed) │ ◄─────────────────────────►│  resolve/plan/   │
└─────────────────┘                            │  render/fsx/     │
                                               │  verify          │
┌─────────────────┐     exclusive place        └────────┬─────────┘
│ Generated Repo  │ ◄───────────────────────────────────┘
│ (dest path)     │
└────────┬────────┘
         │ CI / agents
         ▼
   uv / ruff / ty / pytest / fnox / GHA
```

External systems: GitHub (Actions + optional template repo), age key material
(local, never committed private keys), optional future secret providers via fnox
(non-default).

---

## 9. Architecture

### 9.1 Lifecycle

| Command | Writes? | Behavior |
| ------- | ------- | -------- |
| `foundry validate --spec PATH` | No | Pure pipeline; exit 0/≠0; no plan required on stdout |
| `foundry plan --spec PATH` | No | Emit Generation Plan (text default; JSON via flag) |
| `foundry generate --spec PATH [--plan FILE] [--verify MODE]` | Yes | Bind plan if `--plan` given; else rebuild Construct; stage → lock refresh → verify → exclusive place |
| `foundry catalog list` | No | List closed units with **kind** column |
| `foundry catalog show KIND/ID` | No | Unit detail (kind-qualified) |
| `foundry version` | No | Version + catalog digest |

- `validate` and `plan` MUST NOT mutate the destination or require network by default.
- Interactive questionnaires are NOT required for v1 (MAY exist later; never sole path).
- Stdin: `--spec -` MUST be supported.
- **Unbound generate** (no `--plan`) rebuilds from current foundry version + catalog
  + spec. That is **not** a two-phase commit with a previously inspected plan
  (FND-004). Agents that reviewed a plan MUST pass it via `--plan` to bind.

### 9.2 Pure pipeline

```text
read spec → parse/validate schema → load catalog → resolve (archetype+profiles)
  → resolve effective verify (CLI > TOML > default)
  → Construct Generation Plan → (plan: emit | generate: bind-or-rebuild → execute)
```

`validate` and `plan` share Construct. `generate` either:

1. **Bound path:** load `--plan` JSON; recompute Construct from current inputs;
   hard-fail before any stage write if `plan_sha256`, foundry version, or catalog
   digest mismatch; else execute the bound plan; or
2. **Rebuild path:** Construct from current inputs and execute (documented as
   single-step authority).

### 9.3 Plan-as-contract

The Generation Plan is immutable relative to inputs and includes at least:

- foundry version + catalog digest
- normalized spec (including raw `profiles` membership list)
- resolved archetype + **profiles in catalog apply order** (kind-qualified)
- planned files (path, mode, render kind, content digest)
- dependencies / pins / lock production intent
- external steps + **`verify_mode`** + **`verify_source`** (`cli` | `toml` | `default`)
- `plan_sha256` over canonical JSON (excluding that field)
- warnings (non-binding)

Plan construction MUST be free of wall-clock time and randomness in the plan body.

#### 9.3.1 Canonicalization for `plan_sha256` (FND-009)

Preimage for `plan_sha256`:

1. Build a JSON object of all plan fields **except** `plan_sha256`.
2. Serialize as UTF-8 JSON with:
   - object keys sorted lexicographically at every level;
   - no insignificant whitespace (compact separators);
   - no NaN/Infinity;
   - path strings as POSIX relative form as stored in the plan.
3. `plan_sha256` = lowercase hex SHA-256 of those UTF-8 bytes.

Implementations MUST ship a **fixed test vector** (minimal plan → known hash).

### 9.4 Write semantics (generate)

1. Fail if destination exists and is non-empty (no default overwrite/merge).
2. Create sibling staging directory under destination parent with **unique name**:
   `.foundry-stage-<dest-basename>-<unique>` where `<unique>` is enough to avoid
   collision (e.g. short random or monotonic token). If the chosen name exists,
   allocate a new unique name (do not overwrite prior stages) (FND-011).
3. Render all planned files into stage (paths confined under stage root).
4. **Lock production (FND-003):** for resolved pyproject + python pin + profile
   deps, run `uv lock` (or equivalent) **in stage** so `uv.lock` matches metadata
   **before** default/strict verify. Network need MUST be disclosed. On
   `--verify none`, still attempt lock production when network/policy allows;
   if lock cannot be produced, hard-fail unless an explicit documented escape
   is used (v1: no silent stale lock commit).
5. Run selected verify tier **in stage**.
6. On success: exclusive place stage → destination; remove or relocate stage per
   rename semantics (no leftover stage required on success).
7. On failure: **preserve** stage; destination untouched; exit ≠ 0; error report
   MUST include absolute `stage_path`.

v1 MUST NOT implement existing-project update/merge.

### 9.5 Verify tiers (generate)

#### 9.5.1 Effective verify resolution (FND-001)

| Priority | Source |
| -------- | ------ |
| 1 (highest) | CLI `--verify MODE` when the flag is present |
| 2 | Project Spec TOML `verify` when set |
| 3 (lowest) | `default` |

The plan MUST record `verify_mode` (effective) and `verify_source` (`cli`|`toml`|`default`).

#### 9.5.2 Tier steps

| Mode | Steps (in stage, before place) | Success means |
| ---- | ------------------------------ | ------------- |
| `default` (**Default**) | After lock production: `uv sync --locked` + ruff check + ruff format --check + ty check | **Tooling-sync green** — NOT pytest (FND-005) |
| `strict` | default + pytest (+ cov if configured) | Tooling + tests green. **Does not** run pre-commit pre-place (FND-006) |
| `none` | Explicit opt-out; **loud warning**; still emit DoD docs; lock rules per §9.4 | No tool proof; agent must run DoD after place |

Network need for lock + `uv sync` is disclosed. Verify failure MUST abort place.

pre-commit remains **emitted** (unless `hooks-hk`) and is part of **agent DoD**
when configured (§13.5) and optional local/CI use — not a pre-place strict step.

### 9.6 Catalog

Closed, git-visible catalog as package data:

```text
catalog/
  versions.toml
  core/…
  archetypes/{cli,scripts,data-etl}/…
  profiles/{http,hooks-hk,data-etl}/…
```

- No remote catalog fetch, plugin discovery, or user-installed units in v1.
- Unknown unit IDs fail resolution.
- Catalog digest is part of every plan.
- Dev override path MAY load from filesystem for catalog authors only.
- **Kind qualification (FND-007):** the string `data-etl` is both an archetype id
  and a profile id. CLI `catalog list` / `catalog show` and plan JSON MUST always
  present units as `{ "kind": "archetype"|"profile"|"core", "id": "…" }`. Docs and
  examples MUST show both axes when discussing data/ETL. Bare ambiguous tokens in
  a future unified field are forbidden; TOML keeps separate `archetype` vs
  `profiles` keys (already disambiguated by field).

### 9.7 Composition

- Exactly **one** archetype: `cli` | `scripts` | `data-etl`.
- Profiles: subset of `{http, hooks-hk, data-etl}` selected by the TOML
  `profiles` array treated as a **set**:
  - duplicate ids → hard-fail;
  - **array order MUST NOT affect** plan body or file winners (FND-002);
  - **apply order** = catalog-defined total order restricted to the selected set.
- Apply: `core` → archetype → profiles (catalog order among selected).
- Path collisions: later wins only if `override = true`; else fail.
- `hooks-hk` replaces default pre-commit hook files rather than dual-defaulting.

### 9.8 Engine

Custom planner-led renderer. Copier/Cookiecutter MAY inform template ergonomics
as prior art but MUST NOT be the foundry runtime engine for v1.

### 9.9 GitHub template hybrid

- **SoT:** closed catalog in the foundry product repository.
- **Template repo:** CI-generated snapshot from a **frozen public template Project
  Spec** (FND-010 / REQ-089):

  | Field | v1 public template value |
  | ----- | ------------------------ |
  | `schema` | `1` |
  | `name` | `python-foundry-template` |
  | `archetype` | `cli` |
  | `profiles` | `[]` |
  | `python_version` | default pin **3.13** (omit or explicit 3.13) |
  | `verify` | omit (effective `default` at snapshot generate time) |

- Hand-editing the template repo as a second catalog is forbidden.
- CI MUST fail on snapshot drift vs catalog goldens for this cell.
- Profiles beyond this snapshot require the CLI (unchanged hybrid UX).

### 9.10 go-foundry transfer (normative summary)

| Pattern | Disposition |
| ------- | ----------- |
| validate/plan/generate | Adopt |
| TOML spec + schema | Adopt |
| Immutable plan + pure Construct | Adopt |
| Closed core/archetype/profile catalog | Adopt (Python units) |
| versions lock | Adapt (uv/deps/actions) |
| Sibling stage + exclusive place | Adopt |
| FD-level openat transaction | Adapt (stage-root confinement first) |
| Binary embed | Adapt (`importlib.resources`) |
| Tiered verify | Adapt (uv/ruff/ty/pytest) |
| Non-interactive + JSON reports | Adopt/Adapt |
| TUI archetype; Go stacks; remote catalogs; v1 update-sync; Windows; Claude emit | Reject |

---

## 10. Components and Boundaries

### 10.1 Foundry package layout

```text
src/python_foundry/
  cli/          # Typer wiring only
  spec/         # parse + validate (pure)
  catalog/      # load manifests, digests, package data
  resolve/      # archetype/profile resolution (pure)
  plan/         # Construct plan (pure)
  render/       # static + template → bytes
  fsx/          # stage + place
  generate/     # lifecycle orchestration
  verify/       # tool runners
  report/       # text/JSON encoding
catalog/        # authoring tree (packaged as data)
tests/
```

**Purity rule:** `plan` MUST NOT import `fsx`, `generate`, or `cli`.

### 10.2 Boundary table

| Component | May depend on | Must not |
| --------- | ------------- | -------- |
| cli | all orchestration APIs | embed business rules beyond wiring |
| spec, resolve, plan | catalog load (read) | filesystem writes |
| render | plan artifacts | place to final dest |
| fsx | OS paths | invent plan contents |
| verify | stage tree | mutate dest before place success |
| generate | all above | skip plan Construct |

### 10.3 Foundry vs Generated Project agent surfaces

| Surface | Foundry product / research | Generated Project |
| ------- | -------------------------- | ----------------- |
| AGENTS.md | Program/product rules | Project conventions + DoD |
| Skills | Research/foundry skills | Closed Core skills only (§12) |
| MCP | Owner may use research MCP | Default none |

Research-program skills MUST NOT ship into Generated Projects.

---

## 11. Data Model

### 11.1 Project Spec (TOML, schema = 1)

**Normative minimum fields:**

| Field | Required | Rules |
| ----- | -------- | ----- |
| `schema` | Yes | Integer `1` for v1; unsupported → hard fail |
| `name` | Yes | Non-empty project name |
| `description` | No | Free text |
| `archetype` | Yes | Exactly one of `cli` \| `scripts` \| `data-etl` |
| `destination` | Yes | Path; basename SHOULD match `name` |
| `profiles` | Yes key | Array; may be `[]`; each id ∈ closed set; **set semantics** — duplicates hard-fail; **order ignored** for apply (catalog order wins) (FND-002) |
| `python_version` | No | If set, must be ≥ floor and supported; else default 3.13 pin; lock MUST be regenerated to match (FND-003) |
| `verify` | No | `default` \| `strict` \| `none` when set; **effective** mode uses CLI override if present (FND-001) |

- Unknown keys → hard fail.
- Secret material in the spec file → forbidden.
- Profile IDs not in catalog → hard fail.
- Effective verify resolution: see §9.5.1 (CLI > TOML > `default`).

**Illustrative example (non-secret):**

```toml
schema = 1
name = "example-cli"
description = "Example CLI project"
archetype = "cli"
destination = "./example-cli"
profiles = ["http"]
```

### 11.2 Generation Plan

See §9.3. JSON schema for plan encoding is an implementation detail but MUST
preserve contract fields and stable canonicalization for `plan_sha256`.

### 11.3 Catalog entities

| Kind | Id (v1) |
| ---- | ------- |
| core | `core` |
| archetype | `cli`, `scripts`, `data-etl` |
| profile | `http`, `hooks-hk`, `data-etl` |
| lock | `versions.toml` |

File entries: `static` | `template` with explicit path + mode.

### 11.4 Lockfile policy (OQ-104 resolved; FND-003)

- v1 Generated Projects are **application-shaped**: MUST commit **`uv.lock`**.
- **Lifecycle:** catalog templates MAY ship example locks for goldens, but
  **generate MUST produce or refresh `uv.lock` in stage** so the committed lock
  matches resolved `pyproject.toml` + python pin + selected profiles **before**
  default/strict verify (`uv sync --locked`).
- Off-matrix combinations (e.g. non-default `python_version` + profiles) are
  allowed when lock refresh succeeds; failure of `uv lock` / locked sync fails
  generate (fail closed).
- Library-only packaging variants (no lock) are **out of v1** catalog units
  unless later admitted with explicit lock policy docs.
- Workspace monorepos are **out of v1** (deferred).

---

## 12. Interfaces and Integrations

### 12.1 CLI interface

- Entry: console script `foundry`.
- Global: `--help`, version via `foundry version`.
- Machine-readable: plan/generate reports MUST support JSON mode for agents/CI.
- Exit codes: `0` success; non-zero on failure. Distinct numeric codes SHOULD be
  used where practical; **JSON failure objects are normative** (FND-012).

#### 12.1.1 JSON error taxonomy (FND-012)

On non-zero exit for `plan` / `generate` (and `validate` when JSON requested),
the JSON report MUST include:

| Field | Rule |
| ----- | ---- |
| `ok` | `false` |
| `error_class` | One of: `validation`, `resolve`, `plan_bind`, `render`, `lock`, `verify`, `place`, `internal` |
| `message` | Human-readable summary |
| `stage_path` | Absolute path when a stage exists (generate failures after stage create) |
| `verify_mode` | Effective mode when relevant |
| `plan_sha256` | When a plan was constructed or bound |

#### 12.1.2 Catalog UX (FND-007)

- `catalog list` MUST print/kind-encode each unit's **kind** (`core` |
  `archetype` | `profile`) and **id**.
- `catalog show` MUST accept a kind-qualified reference (e.g. `archetype/data-etl`
  and `profile/data-etl` as distinct).

### 12.2 Agent surface emit (Generated Projects)

**MUST emit:**

```text
AGENTS.md
.agents/skills/quality-gates/SKILL.md
.agents/skills/secrets-fnox/SKILL.md
# archetype:
#   cli     → add-cli-command
#   scripts → add-script
#   data-etl → add-script
```

Skills follow agentskills.io: YAML frontmatter `name` + `description`;
directory name matches skill name.

**MUST NOT emit:**

- `CLAUDE.md`, `.claude/`, Claude-only skill forks
- Default committed MCP catalogs / kitchen-sink `.mcp.json`
- `.env` / dotenv secret templates / `.env.example` as secrets training
- Dual full skill trees under product-private roots as Core

**MAY emit later only via admission:** optional Cursor rules profile (not v1 Default).

### 12.3 Core toolchain emit

Every successful plan MUST include Core tooling. **Layout rows differ by
archetype** (FND-008):

| Artifact / config | `cli` / `data-etl` archetypes | `scripts` archetype |
| ----------------- | ---------------------------- | ------------------- |
| `pyproject.toml` | PEP 621; floor 3.12; pin 3.13 default; scripts entry as appropriate | uv project metadata for workspace tools + script dependency policy per catalog |
| `uv.lock` | Committed (generate-refreshed) | Committed (generate-refreshed) |
| Package layout | `src/<package>/` required | **No** mandatory installable package; `scripts/` (or catalog-defined) PEP 723 scripts + `uv run` |
| `tests/` | Top-level; **≥1 smoke test** required | Top-level; **≥1 smoke test** that exercises at least one script entry (collection non-empty) |
| Ruff / ty / pytest | Required | Required |
| pre-commit | Unless `hooks-hk` | Unless `hooks-hk` |
| `fnox.toml` | age skeleton | age skeleton |
| GHA workflow | setup-uv + ruff + ty + pytest | same |
| README.md + AGENTS.md + skills | Per §12.2 | Per §12.2; archetype skill `add-script` |
| Command docs | REC-013 surface | REC-013 + `uv run scripts/…` examples |

Shared: Ruff config; ty config; pytest (+ cov default); no dotenv secret templates;
no Claude adapters.

### 12.4 GitHub Actions (Generated Projects)

- `permissions: contents: read` minimum
- `ubuntu-latest` required; `macos-latest` optional
- `astral-sh/setup-uv` with cache; pin actions by SHA at implementation
- `uv sync --locked`
- ruff check + format check; `uv run ty check`; `uv run pytest`
- No Windows runners
- No reliance on committed `.env` for secrets

### 12.5 Editor integrations (docs only)

Document official Ruff + ty editor extensions / language servers. Do not require
a specific IDE. Agent DoD remains CLI.

---

## 13. User Workflows

### 13.1 Generate a new project (happy path)

1. Author Project Spec TOML (or reuse example).
2. `foundry validate --spec ./project.toml`
3. `foundry plan --spec ./project.toml --json > plan.json` (inspect file list and digests).
4. **Agent-safe bind (recommended):**  
   `foundry generate --spec ./project.toml --plan plan.json`  
   **Or unbound rebuild:** `foundry generate --spec ./project.toml`  
   (optional `--verify strict|none`; CLI overrides TOML verify).
5. On default verify success: tooling is green; **run pytest** before claiming
   agent DoD (FND-005).
6. `cd` destination; develop with command surface below.
7. Secrets-consuming runs: `fnox exec -- uv run …`

**Trust rule (FND-004):** reviewing `plan` output and later running unbound
`generate` is **not** guaranteed to place the reviewed tree if foundry, catalog,
or spec changed. Use `--plan` to bind.

### 13.2 Agent implementer workflow (Generated Project)

1. Read `README.md` + `AGENTS.md` + relevant skills.
2. Implement change.
3. Run quality gates until green.
4. Never introduce dotenv secrets or Claude adapter files.

### 13.3 GitHub template workflow

1. Use GitHub “Use this template” on the published snapshot repo.
2. For profiles beyond snapshot defaults, use the CLI instead.

### 13.4 Command surface (normative names)

```text
uv sync
uv run ruff check .
uv run ruff format .
uv run ruff format --check    # CI / DoD style
uv run ty check
uv run pytest
uv run pre-commit run --all-files   # when pre-commit configured
fnox exec -- uv run <entry>         # when secrets required
```

Optional `just`/`make` wrappers MUST only call the above (no parallel ecosystems).

### 13.5 Definition of done (agents)

**Generate default-verify success ≠ agent DoD** (FND-005). After place (or on an
existing Generated Project), an agent MUST NOT claim work complete until:

1. Ruff check (and format clean / format --check per DoD) passes.
2. `ty check` passes (no exit-zero masking).
3. `pytest` passes; for **cli**, **data-etl**, and **scripts** archetypes,
   **0 tests collected is not success** unless change is explicitly docs-only
   (FND-008).
4. When pre-commit is configured, `pre-commit run --all-files` is green (or CI
   parity). This is **post-place** DoD, not generate `--verify strict` (FND-006).
5. No dotenv secret storage introduced.

---

## 14. Security and Privacy

| Topic | Policy |
| ----- | ------ |
| Secrets storage | fnox + age; ciphertext/structure in `fnox.toml`; no plaintext secrets in git |
| Secrets runtime | `fnox exec -- <command>` injects env for child only |
| Forbidden | `.env` / python-dotenv / committed env files **as secret storage** |
| Keys | Age private keys and local overrides **out of git** |
| Spec file | No secret material |
| MCP configs | No default; if ever opt-in, no plaintext secrets |
| CI | GitHub Actions secrets or fixtures; never committed dotenv secrets |
| Partial generation | Destination never left half-written on failure |
| Path safety | Render paths confined under stage root (no symlink escape) |
| Privacy | Personal tool; no multi-tenant data plane in v1 |

Non-secret configuration MAY use ordinary TOML/YAML/flags — this section is about
**secrets**, not all config.

---

## 15. Reliability and Operations

| Concern | Policy |
| ------- | ------ |
| Fail-closed generate | Verify or place failure leaves destination untouched |
| Stage retention | Preserve stage on failure; unique stage names; **MUST** emit absolute `stage_path` in errors/JSON (FND-011) |
| Offline generate | Use `--verify none` or cached uv; document limitation |
| Same filesystem | Stage parent SHOULD be same filesystem as destination for rename place |
| Catalog integrity | Unknown units / unpinned versions fail validation |
| Template drift | CI fails if GitHub snapshot ≠ catalog goldens |
| Foundry releases | Version command reports foundry version + catalog digest |

---

## 16. Testing and Verification

### 16.1 Foundry product tests

| Layer | Requirement |
| ----- | ----------- |
| Unit | Pure packages (`spec`, `resolve`, `plan`) without FS side effects |
| Golden | Plan JSON/text goldens per archetype × profile subset |
| Conformance | Emit inventories: required paths present; forbidden paths absent |
| e2e | Stage + exclusive place; fail on non-empty dest |
| Verify runners | Mock or sandbox tool runners for default/strict/none |

### 16.2 Generated Project tests

- Templates include smoke tests so `pytest` collects ≥1 test for package/CLI.
- CI runs ruff, ty, pytest on Generated Projects.

### 16.3 Residual spikes (schedule in implementation)

| ID | Intent | Gate |
| -- | ------ | ---- |
| SPK-001 | uv init + ruff + ty + pytest smoke | Before heavy reliance on templates |
| SPK-002 | ty sample CLI tree + CI | Before locking ty template defaults hard |
| SPK-003 | hk vs pre-commit latency | Only if promoting hk |
| SPK-050 | AGENTS.md + `.agents/skills` on target agents | Before claiming multi-agent emit |
| SPK-052 | fnox exec + age smoke | Before secrets skill freeze |
| SPK-100 | Pure plan golden minimal CLI | PHASE-01 |
| SPK-101 | Stage + exclusive place | PHASE-02 |
| SPK-102 | Catalog expand + forbidden paths | PHASE-03/04 |
| SPK-103 | Default verify cost | PHASE-03 |

---

## 17. CI and Release

### 17.1 Foundry product CI

- Linux required; macOS optional.
- uv locked sync; ruff; ty; pytest.
- Catalog validation + golden plan checks.
- Optional: generate template snapshot and diff.

### 17.2 Release

- Tag foundry releases with version matching `foundry version`.
- Publish install path via uv/PyPI as decided in implementation plan (not frozen here beyond uv packaging).
- Template repo update is a release pipeline step from catalog SoT.

---

## 18. Migration

**Greenfield only for v1.**

- No migration from Poetry/PDM projects.
- No in-place upgrade of existing Generated Projects via `foundry generate`.
- Users recreate or manually adopt Core conventions.

---

## 19. Performance Expectations

| Path | Expectation |
| ---- | ----------- |
| validate/plan | Interactive-fast on modest specs; no network by default |
| generate default verify | Dominated by `uv sync` + ruff + ty; acceptable personal-tool latency |
| strict verify | Adds pytest/pre-commit; may be slower; optional |
| Cold cache | May be slow; document; allow `none` with warning |

No multi-tenant scale targets. Optimization must not weaken plan-as-contract or
fail-closed writes.

---

## 20. Internal Contracts

| Contract | Rule |
| -------- | ---- |
| Plan purity | Construct(plan) free of FS writes and network |
| Plan equality | Same inputs → same plan body (canonical) |
| Generate binding | Execute only the Constructed plan for current inputs |
| Catalog closed | Unknown IDs fail |
| Emit invariants | Core + AI-native always present for success plans |
| Forbidden paths | Catalog validation rejects dotenv secret templates and Claude adapters |
| Purity layering | plan ↛ fsx/generate/cli |
| Admission | New catalog units need manifest + pins + goldens + tests |

---

## 21. Dependency Bill of Materials

### 21.1 Foundry runtime (conceptual)

- Python 3.12+ / 3.13 pin
- uv (dev/CI)
- Typer (+ Click as Typer dependency)
- tomllib (stdlib)
- Packaging/resources: importlib.resources
- Test: pytest, ruff, ty

Exact pins live in foundry `versions` / `uv.lock` at implementation.

### 21.2 Generated Project Core (conceptual)

- uv project metadata; ruff; ty; pytest; pytest-cov; pre-commit (default);
  fnox (external CLI tool expectation); GitHub Actions + setup-uv

### 21.3 Profile BOM

- `http`: httpx
- `hooks-hk`: hk
- `data-etl`: polars, pyarrow; extras duckdb, pandas

### 21.4 Operator-installed tools

fnox and age key tooling are **Required** on operator machines for secret-using
workflows; document install in Generated Project AGENTS.md / secrets skill.

---

## 22. Normative Requirements

Requirements use MUST / MUST NOT / SHOULD / MAY. Priority: **Must** | **Should** | **May**.

### 22.1 Product shape and scope

#### REQ-001 — Hybrid product shape

- **Priority:** Must
- **Applies to:** Product
- **Implementation phase:** PHASE-01..05
- **Source decisions:** Blueprint L1; REC-209; REC-212
- **Verification:** Spec inspection; release ships CLI + catalog + template pipeline
- **Risk linkage:** None

##### Requirement

The product MUST provide (1) a generator CLI, (2) a strong default Core via closed
catalog emit, and (3) a GitHub template surface that is a generated snapshot of
the catalog—not a second hand-edited SoT.

##### Rationale

Blueprint hybrid shape; prevents dual-maintenance drift.

##### Acceptance Evidence

CLI entry points exist; catalog packages Core; CI publishes/checks template snapshot.

##### Exceptions

None.

---

#### REQ-002 — Host OS targets

- **Priority:** Must
- **Applies to:** Foundry + Generated Projects
- **Implementation phase:** All
- **Source decisions:** Blueprint L3; REC-212
- **Verification:** CI matrices; docs; no Windows runners
- **Risk linkage:** None

##### Requirement

Supported hosts MUST be macOS and Linux only. The product MUST NOT claim or test
Windows support in v1.

##### Rationale

Blueprint lock.

##### Acceptance Evidence

Docs and CI exclude Windows; no Windows-specific paths in Core templates.

##### Exceptions

None.

---

#### REQ-003 — Non-goals enforcement

- **Priority:** Must
- **Applies to:** Catalog, CLI, docs
- **Implementation phase:** All
- **Source decisions:** Blueprint §6; REC-212
- **Verification:** Catalog admission; forbidden feature tests
- **Risk linkage:** RSK-055, RSK-053

##### Requirement

v1 MUST NOT ship: marketplace/plugin remote catalogs, framework zoo templates,
notebooks/GUI/mobile archetypes, unlimited MCP/skill catalogs, existing-repo
merge/update generate, or Copier/Cookiecutter as runtime engine.

##### Rationale

Scope discipline.

##### Acceptance Evidence

Closed catalog inventory; rejection tests for unknown archetypes/profiles.

##### Exceptions

None without DEC + Blueprint amendment.

---

### 22.2 Foundry CLI lifecycle

#### REQ-010 — CLI commands

- **Priority:** Must
- **Applies to:** Foundry CLI
- **Implementation phase:** PHASE-01..03
- **Source decisions:** REC-200
- **Verification:** CLI tests; `--help`
- **Risk linkage:** None

##### Requirement

The CLI MUST provide: `validate`, `plan`, `generate`, `catalog list`,
`catalog show`, and `version` (names may be namespaced under the `foundry`
entry point). Console script name MUST be `foundry` unless owner DEC renames it
before first release (package name remains python-foundry).

##### Rationale

Agent-scriptable lifecycle.

##### Acceptance Evidence

Commands exist and match §9.1 behaviors.

##### Exceptions

Additional read-only helpers MAY be added if they do not mutate dest.

---

#### REQ-011 — validate and plan are write-free

- **Priority:** Must
- **Applies to:** `validate`, `plan`
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-200, REC-202
- **Verification:** Tests asserting no dest/stage writes
- **Risk linkage:** None

##### Requirement

`validate` and `plan` MUST NOT write the destination tree, create stage
directories, or require network access by default.

##### Rationale

Safe dry-run for agents/CI.

##### Acceptance Evidence

Automated tests; code review of command handlers.

##### Exceptions

Reading the spec file and catalog package data is allowed.

---

#### REQ-012 — generate is the sole dest mutator

- **Priority:** Must
- **Applies to:** `generate`
- **Implementation phase:** PHASE-02..03
- **Source decisions:** REC-200, REC-203
- **Verification:** e2e tests
- **Risk linkage:** RSK-101

##### Requirement

Only `generate` MAY create the stage and place the destination project tree.

##### Rationale

Clear side-effect boundary.

##### Acceptance Evidence

Command matrix tests.

##### Exceptions

None.

---

#### REQ-013 — Non-interactive first

- **Priority:** Must
- **Applies to:** CLI
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-200, REC-201
- **Verification:** CI scripts using only flags/files
- **Risk linkage:** None

##### Requirement

All v1 lifecycle commands MUST be operable without interactive prompts.
Interactive UX MUST NOT be the sole path to generation.

##### Rationale

Agent-first product.

##### Acceptance Evidence

Headless e2e script succeeds.

##### Exceptions

Optional interactive helpers MAY exist later.

---

### 22.3 Project Spec and Plan

#### REQ-020 — TOML Project Spec schema 1

- **Priority:** Must
- **Applies to:** Spec input
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-201; OQ-100 resolution
- **Verification:** Parse tests; invalid suite (SPK-100)
- **Risk linkage:** None

##### Requirement

The sole declarative product intent document MUST be versioned TOML with
`schema = 1` and the minimum fields in §11.1. Unsupported schema versions MUST
hard-fail.

##### Rationale

Agent-editable; tomllib; go-foundry transfer.

##### Acceptance Evidence

Valid/invalid fixture suite.

##### Exceptions

None.

---

#### REQ-021 — Hard-fail unknown keys and profiles

- **Priority:** Must
- **Applies to:** Spec validation
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-201, REC-205
- **Verification:** Negative tests
- **Risk linkage:** None

##### Requirement

Unknown top-level keys, unknown archetype values, and unknown profile IDs MUST
cause validation failure (non-zero exit).

##### Rationale

Closed-set discipline; prevent agent invention.

##### Acceptance Evidence

Negative fixtures.

##### Exceptions

None.

---

#### REQ-022 — No secrets in Project Spec

- **Priority:** Must
- **Applies to:** Spec
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-201; REC-008
- **Verification:** Policy tests/docs; review
- **Risk linkage:** RSK-007

##### Requirement

The Project Spec MUST NOT carry secret material. Templates and docs MUST NOT
encourage putting secrets in the spec file.

##### Rationale

Secrets belong in fnox.

##### Acceptance Evidence

Docs + schema guidance; no secret examples in fixtures.

##### Exceptions

None.

---

#### REQ-023 — Spec path and stdin

- **Priority:** Must
- **Applies to:** CLI
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-201
- **Verification:** Tests for path and `--spec -`
- **Risk linkage:** None

##### Requirement

Commands that take a spec MUST accept an explicit path and MUST support reading
the spec from stdin via `--spec -` (or equivalent documented form).

##### Rationale

Agent/CI piping.

##### Acceptance Evidence

CLI tests.

##### Exceptions

None.

---

#### REQ-024 — Plan-as-contract

- **Priority:** Must
- **Applies to:** plan / generate
- **Implementation phase:** PHASE-01..03
- **Source decisions:** REC-202
- **Verification:** Golden plans; equality tests
- **Risk linkage:** RSK-100

##### Requirement

The Generation Plan MUST be the immutable contract between pure interpretation
and side effects per §9.3. `generate` MUST either: (1) **bind** a plan artifact
via `--plan` and hard-fail before stage writes if recomputed `plan_sha256`,
foundry version, or catalog digest diverge (FND-004); or (2) **rebuild** from
current inputs without claiming two-command trust. Unbound generate MUST NOT be
documented as executing a previously inspected plan.

##### Rationale

Prevent plan/generate skew and false agent dry-run trust.

##### Acceptance Evidence

Goldens; bind mismatch tests; property tests on canonicalization; no timestamps
in plan body.

##### Exceptions

Warnings may be non-binding notes.

---

#### REQ-025 — Plan encoding

- **Priority:** Must
- **Applies to:** `plan` / reports
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-202; OQ-102 resolution
- **Verification:** Snapshot tests
- **Risk linkage:** None

##### Requirement

`plan` MUST emit a human text summary by default and MUST support a JSON encoding
of the full plan (stdout and/or `--json` / `--out` flags). Persisting a plan under
`.foundry/` in the destination is NOT required for v1.

##### Rationale

Agent attachment without mandatory dest writes during plan.

##### Acceptance Evidence

CLI tests for text + JSON modes.

##### Exceptions

MAY add optional on-disk plan later.

---

#### REQ-026 — plan_sha256

- **Priority:** Must
- **Applies to:** Plan JSON
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-202
- **Verification:** Hash stability tests
- **Risk linkage:** RSK-100

##### Requirement

JSON plan encoding MUST include `plan_sha256` as the lowercase hex SHA-256 of the
canonical plan JSON preimage excluding that field, using the algorithm in
§9.3.1 (UTF-8, sorted keys, compact separators) (FND-009).

##### Rationale

Integrity / comparison / portability.

##### Acceptance Evidence

Fixed test vector + unit tests.

##### Exceptions

None.

---

### 22.4 Filesystem semantics

#### REQ-030 — Fail on non-empty destination

- **Priority:** Must
- **Applies to:** `generate`
- **Implementation phase:** PHASE-02
- **Source decisions:** REC-203
- **Verification:** e2e
- **Risk linkage:** None

##### Requirement

If the destination path exists and is non-empty, `generate` MUST fail without
modifying it. Default overwrite and merge are forbidden in v1.

##### Rationale

Fail-closed placement.

##### Acceptance Evidence

e2e tests.

##### Exceptions

None in v1.

---

#### REQ-031 — Sibling stage then exclusive place

- **Priority:** Must
- **Applies to:** `generate`
- **Implementation phase:** PHASE-02
- **Source decisions:** REC-203
- **Verification:** e2e; failure injection
- **Risk linkage:** RSK-101, RSK-105

##### Requirement

`generate` MUST render into a sibling staging directory with a **unique** name
(`.foundry-stage-<dest-basename>-<unique>`; allocate new name on collision),
produce/refresh lock per §9.4/§11.4, run verify in stage, and on success
exclusively place the stage at the destination. On failure it MUST preserve the
stage, leave destination untouched, exit non-zero, and emit absolute
`stage_path` in human and JSON errors (FND-011).

##### Rationale

No partial dest trees; agent-operable failure recovery.

##### Acceptance Evidence

Failure-injection tests; stage path assertions.

##### Exceptions

Same-filesystem parent SHOULD be used; document rename limitations.

---

#### REQ-032 — Path confinement

- **Priority:** Must
- **Applies to:** render / fsx
- **Implementation phase:** PHASE-02
- **Source decisions:** REC-203
- **Verification:** Path traversal tests
- **Risk linkage:** None

##### Requirement

All rendered paths MUST resolve inside the stage root. Symlink/path escape outside
stage MUST fail.

##### Rationale

Safety.

##### Acceptance Evidence

Negative path tests.

##### Exceptions

None.

---

#### REQ-033 — No existing-project update in v1

- **Priority:** Must
- **Applies to:** Product scope
- **Implementation phase:** All
- **Source decisions:** REC-203, REC-210, REC-212
- **Verification:** No update command; docs
- **Risk linkage:** None

##### Requirement

v1 MUST NOT implement existing-project update, sync, or merge generation.

##### Rationale

Complexity deferral; safety.

##### Acceptance Evidence

CLI surface inventory; docs non-goals.

##### Exceptions

Future DEC only.

---

### 22.5 Catalog and composition

#### REQ-040 — Closed catalog

- **Priority:** Must
- **Applies to:** Catalog
- **Implementation phase:** PHASE-01..04
- **Source decisions:** REC-204, REC-212
- **Verification:** Catalog load tests; no network fetch code paths
- **Risk linkage:** None

##### Requirement

v1 MUST ship a closed catalog as package data with `core`, archetypes
`cli|scripts|data-etl`, profiles `http|hooks-hk|data-etl`, and `versions.toml`.
Remote catalog fetch and plugin unit discovery MUST NOT exist in v1.

##### Rationale

Anti-marketplace; G1 Core/profile map.

##### Acceptance Evidence

Packaged data layout; security/architecture review of load paths.

##### Exceptions

Dev-only filesystem override for catalog authors MAY exist and MUST be documented
as non-production.

---

#### REQ-041 — Catalog digest in plan

- **Priority:** Must
- **Applies to:** Plan
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-204, REC-202
- **Verification:** Plan fixtures
- **Risk linkage:** RSK-103

##### Requirement

Every plan MUST include a catalog digest bound into the contract.

##### Rationale

Reproducibility.

##### Acceptance Evidence

Plan goldens.

##### Exceptions

None.

---

#### REQ-042 — Exactly one archetype

- **Priority:** Must
- **Applies to:** Resolve
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-205
- **Verification:** Resolve tests
- **Risk linkage:** None

##### Requirement

Each Project Spec MUST resolve to exactly one archetype in
`{cli, scripts, data-etl}`. Other archetype IDs MUST fail.

##### Rationale

Closed set.

##### Acceptance Evidence

Negative tests for `web`, etc.

##### Exceptions

None.

---

#### REQ-043 — Profile composition rules

- **Priority:** Must
- **Applies to:** Resolve
- **Implementation phase:** PHASE-01
- **Source decisions:** REC-205, REC-014
- **Verification:** Matrix tests (SPK-102)
- **Risk linkage:** None

##### Requirement

Resolution MUST apply `core` then archetype then profiles in **catalog-defined
order**. The TOML `profiles` array is **membership-only** (set semantics;
duplicates hard-fail); **array order MUST NOT** change apply order or plan body
(FND-002). Path collisions without `override = true` MUST fail. `hooks-hk` MUST
replace default pre-commit hook files rather than dual-shipping both as Default.

##### Rationale

Deterministic composition.

##### Acceptance Evidence

Composition fixtures including profile array permutations → identical plans.

##### Exceptions

None.

---

#### REQ-044 — Catalog admission

- **Priority:** Must
- **Applies to:** Process / repo policy
- **Implementation phase:** PHASE-04+
- **Source decisions:** REC-204, REC-212
- **Verification:** PR checklist / CI
- **Risk linkage:** RSK-055

##### Requirement

New catalog units MUST NOT merge without: manifest, version pins, golden plans,
conformance tests, and explicit review. Scope expansions reopening §5.2 non-goals
REQUIRE a DEC or Blueprint amendment.

##### Rationale

Prevent silent Core expansion.

##### Acceptance Evidence

CONTRIBUTING/admission checklist in product repo.

##### Exceptions

None.

---

### 22.6 Core and profile emit

#### REQ-050 — Core toolchain emit invariants

- **Priority:** Must
- **Applies to:** generate / catalog core
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-206; REC-001..014
- **Verification:** Golden inventories
- **Risk linkage:** RSK-002, RSK-007

##### Requirement

Every successful generation for any archetype MUST emit the Core toolchain
artifacts listed in §12.3, including **ty**, **fnox+age**, Ruff, pytest, uv
project metadata, committed `uv.lock`, GHA with ty step, and REC-013 command
documentation. It MUST NOT emit dotenv secret storage patterns or alternate
Default typecheckers.

##### Rationale

Wire accepted ecosystem Core.

##### Acceptance Evidence

Per-archetype golden path inventories + forbidden-path checks.

##### Exceptions

`hooks-hk` may replace pre-commit files per REQ-043.

---

#### REQ-051 — Python version policy

- **Priority:** Must
- **Applies to:** Generated Projects + foundry dogfood
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-001
- **Verification:** pyproject fixtures; CI matrix
- **Risk linkage:** None

##### Requirement

Generated Projects MUST set `requires-python = ">=3.12"` and default pin Python
**3.13** (e.g. `.python-version` / uv pin). Python 3.10 MUST NOT be a new-project
default.

##### Rationale

Support window and uv Tier 1.

##### Acceptance Evidence

Template inspection; CI.

##### Exceptions

Optional newer pin MAY be allowed if ≥ floor and documented.

---

#### REQ-052 — uv Required

- **Priority:** Must
- **Applies to:** Generated Projects + foundry
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-002
- **Verification:** Templates; docs
- **Risk linkage:** RSK-001

##### Requirement

uv MUST be the project/package manager. Templates MUST use PEP 621 metadata (or
scripts-archetype equivalent per REQ-088) and commit `uv.lock` for v1 Generated
Projects. **Generate MUST produce or refresh `uv.lock` in stage** so the lock
matches resolved metadata before default/strict verify with `uv sync --locked`
(FND-003). Docs MUST NOT teach Poetry/PDM/pip-tools as the primary workflow.

##### Rationale

Single agent-simple lifecycle; honest locks.

##### Acceptance Evidence

Templates + command surface; generate e2e with python_version/profile matrix.

##### Exceptions

None for Default path.

---

#### REQ-053 — Layout by archetype

- **Priority:** Must
- **Applies to:** catalog archetypes
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-003
- **Verification:** Goldens
- **Risk linkage:** None

##### Requirement

- `cli` / `data-etl`: `src/<package>/`, `[project.scripts]` as appropriate,
  top-level `tests/`, ≥1 smoke test.
- `scripts` (FND-008 / REQ-088): PEP 723 + `uv run` oriented layout with
  normative inventory in REQ-088 — **not** a mandatory `src/<package>/` tree.
- Prefer src layout over flat for packaged projects (`cli`, `data-etl`).

##### Rationale

Packaging.python.org + uv guidance; scripts archetype clarity.

##### Acceptance Evidence

Archetype goldens for all three.

##### Exceptions

None.

---

#### REQ-054 — Ruff Required

- **Priority:** Must
- **Applies to:** Core
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-004
- **Verification:** Config present; CI steps
- **Risk linkage:** None

##### Requirement

Ruff MUST provide lint and format. black/isort/flake8 MUST NOT be Default Core.

##### Rationale

Single tool; Astral alignment.

##### Acceptance Evidence

pyproject + CI.

##### Exceptions

None.

---

#### REQ-055 — ty Required Core

- **Priority:** Must
- **Applies to:** Core
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-005 (User decision)
- **Verification:** Config + CI `uv run ty check`
- **Risk linkage:** RSK-002

##### Requirement

ty MUST be the Required Core type checker. Command surface and CI MUST invoke
`uv run ty check` (or the project-documented equivalent if ty CLI renames).
Pyright/mypy MUST NOT be dual-Default.

##### Rationale

Owner lock; monostack coherence.

##### Acceptance Evidence

Templates + CI + AGENTS.md.

##### Exceptions

Documented emergency escape hatch MAY exist; MUST NOT be Default emit.

---

#### REQ-056 — pytest Required

- **Priority:** Must
- **Applies to:** Core
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-006; OQ-055
- **Verification:** `uv run pytest` on fresh generate
- **Risk linkage:** None

##### Requirement

pytest MUST be Required Core with top-level `tests/`. pytest-cov is Default.
Templates for **cli**, **data-etl**, and **scripts** MUST ship ≥1 smoke test so
collection is non-empty (FND-008). Default generate verify does **not** run
pytest; agent DoD does (FND-005).

##### Rationale

Standard runner; avoid empty-suite theater.

##### Acceptance Evidence

Generate + pytest e2e per archetype.

##### Exceptions

Docs-only changes on existing repos may skip new tests; greenfield templates may not.

---

#### REQ-057 — Hooks Default pre-commit

- **Priority:** Must
- **Applies to:** Core hooks
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-007; OQ-003
- **Verification:** Files present unless hooks-hk
- **Risk linkage:** RSK-003

##### Requirement

Default Core MUST emit pre-commit configuration. hk MUST be available only via
profile `hooks-hk`, not forced Core.

##### Rationale

Universal default; owner profile for hk.

##### Acceptance Evidence

Goldens with/without profile.

##### Exceptions

None.

---

#### REQ-058 — fnox + age; no dotenv secrets

- **Priority:** Must
- **Applies to:** Core secrets
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-008 (User decision); REC-107
- **Verification:** fnox.toml present; forbidden-path tests
- **Risk linkage:** RSK-007, RSK-050

##### Requirement

fnox MUST be Required Core with default provider **age**. Templates, AGENTS.md,
and skills MUST NOT teach `.env` / python-dotenv / committed env files as secret
storage. Private age keys MUST be gitignored / out of git.

##### Rationale

Owner lock.

##### Acceptance Evidence

Forbidden-path goldens; secrets skill content.

##### Exceptions

Non-secret config files are allowed.

---

#### REQ-059 — HTTP profile

- **Priority:** Must
- **Applies to:** profile `http`
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-009
- **Verification:** Profile golden
- **Risk linkage:** None

##### Requirement

httpx MUST NOT be universal Core. Profile `http` MUST add httpx (sync default
guidance for CLI/scripts).

##### Rationale

Minimal Core.

##### Acceptance Evidence

With/without profile inventories.

##### Exceptions

None.

---

#### REQ-060 — Typer Default for CLI archetype

- **Priority:** Must
- **Applies to:** archetype `cli`
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-010
- **Verification:** CLI template
- **Risk linkage:** None

##### Requirement

CLI archetype Default framework MUST be Typer. argparse MUST NOT be Default.

##### Rationale

Agent-friendly type-hint CLIs.

##### Acceptance Evidence

Template code + deps.

##### Exceptions

Click alternate MAY be a future optional variant; not required in v1.

---

#### REQ-061 — data-etl profile defaults

- **Priority:** Must
- **Applies to:** profile `data-etl`
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-011; OQ-004
- **Verification:** Profile golden
- **Risk linkage:** RSK-004

##### Requirement

No data libraries in universal Core. Profile `data-etl` Default MUST be
**polars + pyarrow**, with duckdb and pandas documented as first-class extras.
Notebooks MUST NOT be emitted.

##### Rationale

Optional heavy deps; modern baseline.

##### Acceptance Evidence

Profile inventory + docs.

##### Exceptions

Owner DEC may swap defaults later.

---

#### REQ-062 — GitHub Actions Core CI

- **Priority:** Must
- **Applies to:** Generated Projects
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-012; OQ-005
- **Verification:** Workflow file golden
- **Risk linkage:** RSK-005

##### Requirement

Core MUST emit a GHA workflow per §12.4: Linux required; macOS optional; setup-uv;
locked sync; ruff; ty; pytest; no Windows; no dotenv secrets reliance.

##### Rationale

Blueprint L7 + Core gates.

##### Acceptance Evidence

Workflow golden + schema checks.

##### Exceptions

None.

---

#### REQ-063 — Command surface documentation

- **Priority:** Must
- **Applies to:** README, AGENTS.md, skills
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-013, REC-106
- **Verification:** Content tests / inspection
- **Risk linkage:** None

##### Requirement

Generated Projects MUST document the closed command surface in §13.4. Docs MUST
NOT present competing primary ecosystems (poetry run, pip+venv primary, dotenv run).

##### Rationale

Decision reduction for agents.

##### Acceptance Evidence

Template content assertions.

##### Exceptions

Thin just/make wrappers that only call the surface are allowed.

---

### 22.7 AI-native emit

#### REQ-070 — AGENTS.md only

- **Priority:** Must
- **Applies to:** Generated Projects
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-100, REC-108; EVD-121
- **Verification:** Forbidden-path tests
- **Risk linkage:** RSK-051

##### Requirement

Generate MUST emit root `AGENTS.md` as the instruction SoT and MUST NOT emit
`CLAUDE.md`, `Claude.md`, `CLAUDE.local.md`, or `.claude/` trees.

##### Rationale

Standards-only; Claude Code not a design target.

##### Acceptance Evidence

Goldens + forbidden paths.

##### Exceptions

None.

---

#### REQ-071 — Skills under `.agents/skills` only

- **Priority:** Must
- **Applies to:** Generated Projects
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-102, REC-103, REC-207; OQ-103
- **Verification:** Path inventory
- **Risk linkage:** RSK-055

##### Requirement

Core skills MUST live at `.agents/skills/<name>/SKILL.md` only. Generate MUST
emit at least: `quality-gates`, `secrets-fnox`, and archetype skill
`add-cli-command` (cli) or `add-script` (scripts and data-etl). MUST NOT emit
`.claude/skills` or dual full skill copies.

##### Rationale

Portable skills layout; closed catalog.

##### Acceptance Evidence

Goldens per archetype.

##### Exceptions

None for v1 Core.

---

#### REQ-072 — MCP default none

- **Priority:** Must
- **Applies to:** Generated Projects
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-104, REC-207; OQ-053
- **Verification:** No default MCP files in goldens
- **Risk linkage:** RSK-053

##### Requirement

Generate MUST NOT commit a default MCP server catalog. v1 MUST NOT include an
MCP profile.

##### Rationale

Context cost; closed set.

##### Acceptance Evidence

Goldens.

##### Exceptions

Operators MAY add MCP manually later.

---

#### REQ-073 — Agent secrets protocol

- **Priority:** Must
- **Applies to:** AGENTS.md + secrets-fnox skill
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-107
- **Verification:** Content inspection
- **Risk linkage:** RSK-050

##### Requirement

Agent docs MUST require `fnox exec -- …` for secret-consuming commands and MUST
forbid dotenv secret storage teaching.

##### Rationale

Relapse surface is agent docs.

##### Acceptance Evidence

Skill + AGENTS.md content tests.

##### Exceptions

None.

---

#### REQ-074 — Definition of done

- **Priority:** Must
- **Applies to:** AGENTS.md + quality-gates skill
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-110
- **Verification:** Content inspection
- **Risk linkage:** RSK-054

##### Requirement

AGENTS.md / quality-gates MUST state the DoD in §13.5, including ty CLI gates,
rejection of empty test collection for cli/data-etl/scripts work, and an explicit
statement that **default generate verify success does not satisfy pytest DoD**
(FND-005). Skills MUST NOT contradict AGENTS.md; on conflict AGENTS.md wins.

##### Rationale

CI parity locally; honest success signals.

##### Acceptance Evidence

Content tests.

##### Exceptions

None.

---

#### REQ-075 — Fresh-session packaging

- **Priority:** Should
- **Applies to:** Generated Project docs
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-109
- **Verification:** Review
- **Risk linkage:** None

##### Requirement

Generated Projects SHOULD be operable from README + AGENTS.md + skills alone
without chat history. Avoid long duplicated prose across README and AGENTS.md.

##### Rationale

Blueprint agent operability.

##### Acceptance Evidence

Human/agent dry-run review.

##### Exceptions

Optional `docs/` when needed.

---

#### REQ-076 — Foundry vs Generated agent surfaces

- **Priority:** Must
- **Applies to:** Emit policy
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-101; OQ-054
- **Verification:** Catalog does not include research skills
- **Risk linkage:** None

##### Requirement

Research-program skills and foundry-meta skills MUST NOT be emitted into
Generated Projects. Foundry product repo agent packaging MAY differ and is
specified at product implementation time.

##### Rationale

Avoid skill bloat and oral tradition.

##### Acceptance Evidence

Catalog inventory review.

##### Exceptions

None.

---

#### REQ-077 — Editor documentation

- **Priority:** Should
- **Applies to:** Docs
- **Implementation phase:** PHASE-05
- **Source decisions:** REC-112, REC-105
- **Verification:** Doc presence
- **Risk linkage:** RSK-054

##### Requirement

Docs SHOULD recommend official Ruff + ty editor integrations and MUST state that
CLI gates remain authoritative for agents.

##### Rationale

Live diagnostics without dual-default typecheckers.

##### Acceptance Evidence

Doc section exists.

##### Exceptions

None.

---

#### REQ-078 — AI-native anti-patterns

- **Priority:** Must
- **Applies to:** Templates, skills, docs
- **Implementation phase:** PHASE-04
- **Source decisions:** REC-111
- **Verification:** Forbidden content tests
- **Risk linkage:** RSK-050, RSK-051, RSK-053

##### Requirement

Templates and skills MUST reject the anti-patterns in REC-111: unlimited
skill/MCP catalogs; Claude adapters; dotenv secret quick starts; five competing
command ecosystems; Windows-only agent paths; silent demotion of ty/fnox;
kitchen-sink MCP; oral-tradition-only conventions.

##### Rationale

Preserve locks under agent pressure.

##### Acceptance Evidence

Content + forbidden-path tests.

##### Exceptions

None.

---

### 22.8 Verification policy and hybrid template

#### REQ-080 — Default verify mode

- **Priority:** Must
- **Applies to:** `generate`
- **Implementation phase:** PHASE-03
- **Source decisions:** REC-211; OQ-101
- **Verification:** CLI default tests
- **Risk linkage:** RSK-102

##### Requirement

Effective verify mode MUST resolve as **CLI `--verify` if present, else TOML
`verify` if set, else `default`** (FND-001). Plan MUST record `verify_mode` and
`verify_source`.

- `default`: after lock production, `uv sync --locked` + ruff check + ruff format
  --check + ty check. Success means **tooling-sync green**, not pytest (FND-005).
- `strict`: default + pytest (+ cov if configured). MUST **not** run pre-commit
  pre-place (FND-006).
- `none`: explicit opt-out; loud warning; still emit DoD docs.

Verify failure MUST abort place. Network for lock/sync MUST be disclosed.

##### Rationale

Honest, total control plane for agents.

##### Acceptance Evidence

CLI matrix tests for precedence; default/strict/none e2e; failure aborts place.

##### Exceptions

Offline users may choose `none` (with warning).

---

#### REQ-081 — GitHub template is generated snapshot

- **Priority:** Must
- **Applies to:** Hybrid release
- **Implementation phase:** PHASE-05
- **Source decisions:** REC-209
- **Verification:** CI drift check
- **Risk linkage:** RSK-103

##### Requirement

The GitHub template repository MUST be produced by generating from the catalog
SoT using the **frozen public template Project Spec** in §9.9 / REQ-089
(FND-010). CI MUST fail if the published snapshot drifts from catalog goldens for
that cell. Hand-editing the template as a second catalog MUST be forbidden in
docs/process.

##### Rationale

Single SoT; stable public baseline.

##### Acceptance Evidence

Checked-in template spec + CI job + process docs.

##### Exceptions

None.

---

#### REQ-082 — Foundry module layout

- **Priority:** Should
- **Applies to:** Foundry product repo
- **Implementation phase:** PHASE-01..03
- **Source decisions:** REC-208
- **Verification:** Package structure inspection
- **Risk linkage:** None

##### Requirement

Foundry implementation SHOULD follow the package map in §10.1 and MUST enforce
the purity rule that `plan` does not import `fsx`/`generate`/`cli`.

##### Rationale

Testable boundaries.

##### Acceptance Evidence

Import linter or architecture tests.

##### Exceptions

Minor renames allowed if boundaries preserved.

---

#### REQ-083 — go-foundry transfer discipline

- **Priority:** Must
- **Applies to:** Design/implementation judgment
- **Implementation phase:** All
- **Source decisions:** REC-210; Blueprint L10
- **Verification:** Review against §9.10
- **Risk linkage:** RSK-105

##### Requirement

Implementers MUST follow the Adopt/Adapt/Reject dispositions in §9.10. go-foundry
MUST NOT be sole authority for Python/uv correctness. FD-level openat complexity
MUST NOT block v1 if stage-root confinement meets REQ-031/032.

##### Rationale

Adapt, do not copy blindly.

##### Acceptance Evidence

Design review; no Windows/TUI/remote catalog imports.

##### Exceptions

None.

---


---

#### REQ-084 — Effective verify resolution

- **Priority:** Must
- **Applies to:** CLI + Project Spec + Plan
- **Implementation phase:** PHASE-01, PHASE-03
- **Source decisions:** FND-001
- **Verification:** Precedence matrix tests
- **Risk linkage:** RSK-102

##### Requirement

Effective verify mode MUST be resolved as CLI `--verify` if the flag is present;
else TOML `verify` if set; else `default`. The plan MUST record `verify_mode` and
`verify_source` ∈ {`cli`,`toml`,`default`}.

##### Rationale

Close dual-surface ambiguity.

##### Acceptance Evidence

Fixture matrix for all combinations including CLI/TOML disagreement.

##### Exceptions

None.

---

#### REQ-085 — Generate-time uv.lock production

- **Priority:** Must
- **Applies to:** `generate` / stage
- **Implementation phase:** PHASE-03, PHASE-04
- **Source decisions:** FND-003; OQ-104
- **Verification:** e2e lock digest vs metadata; `uv sync --locked`
- **Risk linkage:** RSK-001, RSK-102

##### Requirement

Before default or strict verify, `generate` MUST produce or refresh `uv.lock` in
the stage so it matches resolved project metadata (python pin, deps, profiles).
Default/strict verify MUST use locked sync. Generate MUST NOT place a tree whose
committed lock is known-stale relative to rendered metadata.

##### Rationale

Honest committed locks under resolution variance.

##### Acceptance Evidence

Matrix e2e: default pin; alternate `python_version`; with/without `http` profile.

##### Exceptions

`--verify none` still requires best-effort lock production per §9.4; v1 does not
allow silent omission of lock on successful place.

---

#### REQ-086 — Optional generate --plan binding

- **Priority:** Must
- **Applies to:** `generate`
- **Implementation phase:** PHASE-01..03
- **Source decisions:** FND-004
- **Verification:** bind match/mismatch tests
- **Risk linkage:** RSK-100

##### Requirement

`generate` MUST accept optional `--plan PATH` (JSON plan artifact). When
supplied, generate MUST recompute Construct from current inputs and hard-fail
with `error_class=plan_bind` before stage writes if `plan_sha256`, foundry
version, or catalog digest differ. When omitted, generate rebuilds and docs/AGENTS
MUST state that prior `plan` output is not bound.

##### Rationale

Agent-safe dry-run → side-effect path without mandating on-disk `.foundry/`.

##### Acceptance Evidence

CLI tests: match succeeds; bit-flip plan fails; unbound path documented.

##### Exceptions

None.

---

#### REQ-087 — Kind-qualified catalog identity

- **Priority:** Must
- **Applies to:** catalog CLI + plan JSON
- **Implementation phase:** PHASE-01, PHASE-04
- **Source decisions:** FND-007
- **Verification:** catalog list/show tests; plan schema
- **Risk linkage:** None

##### Requirement

Catalog list/show and plan-resolved unit references MUST include unit **kind**
(`core`|`archetype`|`profile`) alongside **id**, so `data-etl` archetype and
`data-etl` profile are never ambiguous in machine output. Human docs MUST show
both axes in data/ETL examples.

##### Rationale

Dual-id confusion mitigation without rename churn.

##### Acceptance Evidence

Golden plan JSON; CLI snapshots.

##### Exceptions

TOML continues to use separate `archetype` and `profiles` keys (already scoped).

---

#### REQ-088 — scripts archetype emit contract

- **Priority:** Must
- **Applies to:** archetype `scripts`
- **Implementation phase:** PHASE-04
- **Source decisions:** FND-008; REC-003
- **Verification:** scripts golden inventory
- **Risk linkage:** None

##### Requirement

The `scripts` archetype MUST emit at least:

- uv project metadata + committed `uv.lock` (generate-refreshed)
- a `scripts/` directory (name may match catalog) containing ≥1 PEP 723 script
  runnable via `uv run`
- top-level `tests/` with ≥1 smoke test invoking a script entry
- Ruff, ty, pytest, pre-commit (unless hooks-hk), fnox.toml, GHA, README,
  AGENTS.md, skills `quality-gates`, `secrets-fnox`, `add-script`

It MUST NOT require an installable `src/<package>/` tree unless catalog later
admits an optional variant.

##### Rationale

Close under-specification vs package archetypes.

##### Acceptance Evidence

Conformance inventory + generate e2e.

##### Exceptions

None.

---

#### REQ-089 — Frozen public template Project Spec

- **Priority:** Must
- **Applies to:** Hybrid GitHub template
- **Implementation phase:** PHASE-05
- **Source decisions:** FND-010; REQ-081
- **Verification:** checked-in spec file + CI
- **Risk linkage:** RSK-103

##### Requirement

v1 public template generation MUST use the frozen field set in §9.9
(`archetype=cli`, `profiles=[]`, name `python-foundry-template`, python 3.13
default). Changes to this cell require release notes and golden updates.

##### Rationale

Stable hybrid showcase.

##### Acceptance Evidence

Repo path for template spec + CI generate+diff.

##### Exceptions

None.

---

#### REQ-090 — Stage identity and failure path

- **Priority:** Must
- **Applies to:** `generate` / fsx
- **Implementation phase:** PHASE-02
- **Source decisions:** FND-011
- **Verification:** failure-injection e2e
- **Risk linkage:** RSK-101

##### Requirement

Stage directories MUST use unique names under the destination parent; collisions
MUST allocate a new name without deleting prior failed stages. Failures after
stage creation MUST report absolute `stage_path` in stderr and JSON.

##### Rationale

Agent recovery and disk hygiene.

##### Acceptance Evidence

Two consecutive failed generates leave two stages; paths parseable from JSON.

##### Exceptions

None.

---

#### REQ-091 — JSON error_class taxonomy

- **Priority:** Must
- **Applies to:** plan/generate/validate JSON reports
- **Implementation phase:** PHASE-01..03
- **Source decisions:** FND-012
- **Verification:** contract tests per fault class
- **Risk linkage:** None

##### Requirement

JSON failure reports MUST include `error_class` from the closed set in §12.1.1
and MUST populate `stage_path` / `verify_mode` / `plan_sha256` when applicable.

##### Rationale

Agent-scriptable failures.

##### Acceptance Evidence

Contract tests for representative faults.

##### Exceptions

None.

---

## 23. Traceability


| REQ | Sources | Phase |
| --- | ------- | ----- |
| REQ-001 | L1; REC-209; REC-212 | PHASE-01..05 |
| REQ-002 | L3; REC-212 | All |
| REQ-003 | Blueprint non-goals; REC-212 | All |
| REQ-010 | REC-200 | PHASE-01..03 |
| REQ-011 | REC-200; REC-202 | PHASE-01 |
| REQ-012 | REC-200; REC-203 | PHASE-02..03 |
| REQ-013 | REC-200; REC-201 | PHASE-01 |
| REQ-020 | REC-201; OQ-100 | PHASE-01 |
| REQ-021 | REC-201; REC-205 | PHASE-01 |
| REQ-022 | REC-201; REC-008 | PHASE-01 |
| REQ-023 | REC-201 | PHASE-01 |
| REQ-024 | REC-202 | PHASE-01..03 |
| REQ-025 | REC-202; OQ-102 | PHASE-01 |
| REQ-026 | REC-202 | PHASE-01 |
| REQ-030 | REC-203 | PHASE-02 |
| REQ-031 | REC-203 | PHASE-02 |
| REQ-032 | REC-203 | PHASE-02 |
| REQ-033 | REC-203; REC-210; REC-212 | All |
| REQ-040 | REC-204; REC-212 | PHASE-01..04 |
| REQ-041 | REC-204; REC-202 | PHASE-01 |
| REQ-042 | REC-205 | PHASE-01 |
| REQ-043 | REC-205; REC-014 | PHASE-01 |
| REQ-044 | REC-204; REC-212 | PHASE-04+ |
| REQ-050 | REC-206; REC-001..014 | PHASE-04 |
| REQ-051 | REC-001 | PHASE-04 |
| REQ-052 | REC-002 | PHASE-04 |
| REQ-053 | REC-003 | PHASE-04 |
| REQ-054 | REC-004 | PHASE-04 |
| REQ-055 | REC-005 | PHASE-04 |
| REQ-056 | REC-006; OQ-055 | PHASE-04 |
| REQ-057 | REC-007; OQ-003 | PHASE-04 |
| REQ-058 | REC-008; REC-107 | PHASE-04 |
| REQ-059 | REC-009 | PHASE-04 |
| REQ-060 | REC-010 | PHASE-04 |
| REQ-061 | REC-011; OQ-004 | PHASE-04 |
| REQ-062 | REC-012; OQ-005 | PHASE-04 |
| REQ-063 | REC-013; REC-106 | PHASE-04 |
| REQ-070 | REC-100; REC-108 | PHASE-04 |
| REQ-071 | REC-102; REC-103; REC-207 | PHASE-04 |
| REQ-072 | REC-104; REC-207 | PHASE-04 |
| REQ-073 | REC-107 | PHASE-04 |
| REQ-074 | REC-110 | PHASE-04 |
| REQ-075 | REC-109 | PHASE-04 |
| REQ-076 | REC-101 | PHASE-04 |
| REQ-077 | REC-112; REC-105 | PHASE-05 |
| REQ-078 | REC-111 | PHASE-04 |
| REQ-080 | REC-211; OQ-101 | PHASE-03 |
| REQ-081 | REC-209 | PHASE-05 |
| REQ-082 | REC-208 | PHASE-01..03 |
| REQ-083 | REC-210; L10 | All |
| REQ-084 | FND-001 | PHASE-01,03 |
| REQ-085 | FND-003; OQ-104 | PHASE-03,04 |
| REQ-086 | FND-004 | PHASE-01..03 |
| REQ-087 | FND-007 | PHASE-01,04 |
| REQ-088 | FND-008; REC-003 | PHASE-04 |
| REQ-089 | FND-010; REQ-081 | PHASE-05 |
| REQ-090 | FND-011 | PHASE-02 |
| REQ-091 | FND-012 | PHASE-01..03 |

---

## 24. Risk Register

| ID | Risk | Severity | Mitigation | Related |
| -- | ---- | -------- | ---------- | ------- |
| RSK-001 | uv pre-1.0 churn | Medium | Pin uv; lockfiles | REQ-052 |
| RSK-002 | ty maturity as Core | Medium–High | Pin ty; SPK-002; Exception path documented; CI fail-closed | REQ-055 |
| RSK-003 | Owner later wants hk Core | Low–Med | Profile available; DEC path | REQ-057 |
| RSK-004 | polars default vs pandas habits | Low | Extras docs | REQ-061 |
| RSK-005 | macOS CI cost | Low | Optional macOS | REQ-062 |
| RSK-006 | Research synthesis overclaim | Medium | Primary citations in reports; this spec avoids new load-bearing web claims | Methodology |
| RSK-007 | fnox Core + no dotenv fallback | Medium | Templates; skills; age key docs | REQ-058 |
| RSK-050 | Agents reintroduce dotenv secrets | High | skills + forbidden paths | REQ-058, REQ-073 |
| RSK-051 | Contributors reintroduce Claude adapters | Med | forbidden paths; REC-100 | REQ-070 |
| RSK-052 | Withdrawn (Claude skills) | — | N/A | — |
| RSK-053 | MCP kitchen-sink creep | Medium | REQ-072 | REQ-072 |
| RSK-054 | Agents use Pyright, ignore ty | Medium | CLI DoD + CI ty | REQ-055, REQ-074 |
| RSK-055 | Skill catalog sprawl | Medium | Closed set; admission | REQ-071, REQ-044 |
| RSK-056 | AGENTS.md vs product rules precedence | Low–Med | No default Cursor rules v1 | OQ-052 |
| RSK-100 | Plan/generate non-determinism | High if present | Canonical JSON; ban time/random | REQ-024 |
| RSK-101 | Leftover stage confuses agents | Medium | Error messages document path | REQ-031 |
| RSK-102 | Verify needs network | Medium | Disclose; `none` mode | REQ-080 |
| RSK-103 | Template snapshot drift | Medium | CI regenerate+diff | REQ-081 |
| RSK-104 | Catalog reintroduces dotenv/Claude | High | Forbidden-path tests | REQ-050, REQ-070 |
| RSK-105 | Over-copy go-foundry FD complexity | Medium | Stage-root first | REQ-083 |
| RSK-106 | Exa overclaim | Medium | Challenged in architecture; locks held | Reports |
| RSK-107 | Generate-time `uv lock` network/cost | Medium | Disclose; `none` still best-effort; SPK-103 | REQ-085, REQ-080 |
| RSK-108 | Agents ignore `--plan` bind path | Medium | AGENTS.md + skills teach bind workflow | REQ-086 |
| RSK-109 | data-etl dual-id residual confusion | Low | Kind-qualified UX; docs | REQ-087 |

---

## 25. Open Questions

| ID | Topic | Status | Blocking? | Notes |
| -- | ----- | ------ | --------- | ----- |
| OQ-001 | Exact ty config keys in templates | **Resolved for REQ** | No | Use `uv run ty check`; freeze config from ty docs + SPK-002 at implement |
| OQ-002 | SPK-002 timing | Open schedule | No | Before heavy codegen (PHASE-04 gate) |
| OQ-003 | Force hk Core | **Resolved: no** | No | pre-commit Default remains |
| OQ-004 | data-etl engine default | **Resolved: polars+pyarrow** | No | Owner DEC may swap later |
| OQ-005 | macOS CI always-on | **Resolved: optional** | No | Linux required |
| OQ-006 | fnox default provider | **Resolved: age** | No | From ecosystem |
| OQ-050/051 | Claude emit | **Cancelled** | No | EVD-121 |
| OQ-052 | Cursor vs AGENTS precedence | **Resolved for v1** | No | Do not emit `.cursor/rules` by default |
| OQ-053 | MCP Core profile | **Resolved: none v1** | No | |
| OQ-054 | Foundry product skill catalog | Deferred | Partial | Product repo implementation; not Generated Project Core |
| OQ-055 | ≥1 test mechanical | **Resolved: yes for templates** | No | REQ-056 |
| OQ-100 | TOML fields | **Resolved** | No | §11.1 |
| OQ-101 | Default verify | **Resolved: default** | No | REQ-080 |
| OQ-102 | JSON plan on disk | **Resolved: optional flag only** | No | REQ-025 |
| OQ-103 | data-etl skill | **Resolved: add-script** | No | REQ-071 |
| OQ-104 | Lockfile policy | **Resolved: commit uv.lock** | No | REQ-052 |
| OQ-105 | CLI name | **Provisional: foundry** | Branding only | Owner may DEC rename |
| OQ-106 | Rename profile `data-etl` | **Deferred** | No | Kind-qualified UX adopted (FND-007); rename only if agents still fail |
| OQ-107 | Default verify includes pytest | **Rejected for v1** | No | Cost; strict available; DoD honesty (FND-005/006) |

---

## 26. Deferred Work

| Item | Why deferred | Earliest |
| ---- | ------------ | -------- |
| Existing-project update/sync | Complexity; safety | Post-v1 DEC |
| Remote/plugin catalogs | Marketplace non-goal | Never without scope change |
| MCP opt-in generator profile | No concrete need | Later admission |
| `.cursor/rules` profile | Avoid dual systems | If Cursor globs proven necessary |
| Click alternate CLI template | Typer Default sufficient | Optional later |
| Library-only (no lock) catalog unit | v1 apps commit lock | Later admission |
| Full FD openat transaction parity | Stage-root enough for v1 | If needed |
| Interactive questionnaire UX | Non-interactive first | Optional later |
| Foundry product closed skill set beyond research | OQ-054 | Product implementation plan |
| PyPI publishing details | Implementation plan | PHASE-05 |
| `data-etl-entry` dedicated skill | Prefer add-script | If agent failures prove need |
| Workspace monorepo Generated Projects | Out of v1 lock model | Post-v1 admission |
| Profile id rename `data-etl` → other | Kind-qualified UX first | If OQ-106 reopened |
| pre-commit inside generate strict | Environment/git hazards (FND-006) | Agent DoD remains |

---

## 27. Rejected Work

| Item | Why rejected | Source |
| ---- | ------------ | ------ |
| Windows support | Blueprint L3 | L3 |
| Notebooks / GUI / mobile | Non-goals | Blueprint |
| Framework zoo | Non-goals | Blueprint |
| Marketplace / remote catalogs | Non-goals | REC-212 |
| dotenv / `.env` secret storage | User decision | REC-008 |
| Claude adapters Core emit | User decision EVD-121 | REC-100 |
| Default MCP kitchen sink | Non-goals + REC-104 | REC-104 |
| Copier/Cookiecutter as engine | Plan purity / catalog control | REC-204, REC-210 |
| Plan-as-preview only | Generate may diverge | REC-202 |
| In-place overwrite/merge v1 | Partial writes | REC-203 |
| Dual-edit GitHub template + catalog | Drift | REC-209 |
| ty demoted from Core | User decision | REC-005 |
| fnox demoted / secrets profile only | User decision | REC-008 |
| httpx in universal Core | Minimal Core | REC-009 |
| hk Required Core (without DEC) | Evidence + simplicity | REC-007 |
| Poetry/PDM/Hatch as Default | uv Core | REC-002 |
| Unlimited skill catalogs | Non-goals | REC-103 |

---

## 28. Recommendation Disposition Ledger

### 28.1 Ecosystem (REC-001..014)

| REC | Disposition | Notes / REQs |
| --- | ----------- | ------------ |
| REC-001 | **Accepted** | REQ-051 |
| REC-002 | **Accepted** | REQ-052 |
| REC-003 | **Accepted** | REQ-053 |
| REC-004 | **Accepted** | REQ-054 |
| REC-005 | **Accepted** | REQ-055; residual RSK-002 |
| REC-006 | **Accepted** | REQ-056 |
| REC-007 | **Accepted** | REQ-057 |
| REC-008 | **Accepted** | REQ-058; dotenv rejected |
| REC-009 | **Accepted** | REQ-059 |
| REC-010 | **Accepted** | REQ-060 |
| REC-011 | **Accepted** | REQ-061 |
| REC-012 | **Accepted** | REQ-062 |
| REC-013 | **Accepted** | REQ-063 |
| REC-014 | **Accepted** | REQ-050, REQ-043 (membership tables) |

### 28.2 AI-native (REC-100..112)

| REC | Disposition | Notes / REQs |
| --- | ----------- | ------------ |
| REC-100 | **Accepted** | REQ-070 |
| REC-101 | **Accepted** | REQ-076 |
| REC-102 | **Accepted** | REQ-071 |
| REC-103 | **Accepted with modification** | REQ-071; v1 uses `add-script` for data-etl (no separate `data-etl-entry` skill) |
| REC-104 | **Accepted** | REQ-072 |
| REC-105 | **Accepted** | REQ-077; CLI gates in REQ-074 |
| REC-106 | **Accepted** | REQ-063 |
| REC-107 | **Accepted** | REQ-073, REQ-058 |
| REC-108 | **Accepted** | REQ-070 |
| REC-109 | **Accepted** | REQ-075 |
| REC-110 | **Accepted** | REQ-074 |
| REC-111 | **Accepted** | REQ-078 |
| REC-112 | **Accepted** | REQ-077 |

### 28.3 Architecture (REC-200..212)

| REC | Disposition | Notes / REQs |
| --- | ----------- | ------------ |
| REC-200 | **Accepted** | REQ-010..013 |
| REC-201 | **Accepted** | REQ-020..023 |
| REC-202 | **Accepted** | REQ-024..026 |
| REC-203 | **Accepted** | REQ-030..033 |
| REC-204 | **Accepted** | REQ-040, REQ-041, REQ-044 |
| REC-205 | **Accepted** | REQ-042, REQ-043 |
| REC-206 | **Accepted** | REQ-050..063 (emit) |
| REC-207 | **Accepted** | REQ-070..078 |
| REC-208 | **Accepted** | REQ-082 |
| REC-209 | **Accepted** | REQ-081, REQ-001 |
| REC-210 | **Accepted** | REQ-083; §9.10 |
| REC-211 | **Accepted** | REQ-080 (default = `default`) |
| REC-212 | **Accepted** | REQ-003, REQ-044 |

**Count check:** 14 + 13 + 13 = **40** RECs dispositioned; none silent.

---

## 29. Definition of Done

### 29.1 This artifact (spec-revision)

- [x] Required sections present (revision front matter through implementation handoff)
- [x] Status: **Accepted — implementation authority**
- [x] Actual revision date recorded
- [x] Every FND-001..012 dispositioned
- [x] Corrections integrated in body (not ledger-only)
- [x] REC ledger carried; REQ-084..091 added; stable REQs retained
- [x] Locks preserved
- [x] High-level phases updated; no granular coding backlog
- [x] Standalone for implementation

### 29.2 Product v1 (future)

Product v1 is done when: pure pipeline + generate fail-closed works; lock
production honest; plan bind works; Core and AI-native emit goldens pass;
default verify produces **tooling-sync-green** projects; agent DoD (incl. pytest)
documented; frozen template snapshot CI green; dogfood foundry itself on Core;
residual spikes for ty/fnox completed or accepted with residual risk.

---

## 30. Updated Implementation Handoff

### 30.1 Implementation authority

After human acceptance of stage `spec-revision`, **this document (v0.2)** is
product implementation authority. The proposed specification v0.1 is historical.

### 30.2 Downstream stage

Next program stage: **`implementation-plan`** — produce
`docs/plans/01-implementation-plan.md` from this revised specification.
Do not invent architecture that contradicts REQs here.

### 30.3 Phase gates (updated)

| Phase | Must incorporate |
| ----- | ---------------- |
| PHASE-01 | FND-002 order fixtures; FND-009 hash vectors; FND-001 verify fields in plan; FND-012 error_class; FND-004 `--plan` bind API shape |
| PHASE-02 | FND-011 stage identity + `stage_path` |
| PHASE-03 | FND-001/003/005/006 verify+lock semantics; FND-004 bind e2e |
| PHASE-04 | FND-007 catalog UX; FND-008 scripts inventory; lock matrix |
| PHASE-05 | FND-010 frozen template cell |

### 30.4 Residual risks to plan for

- RSK-002 ty maturity; RSK-007/050 fnox/dotenv relapse
- RSK-107 lock network cost; RSK-108 agents skip `--plan`
- Provisional CLI name `foundry` (OQ-105)

### 30.5 Explicit non-goals for implementers

Do not reopen Windows, dotenv secrets, Claude adapters, demote ty/fnox, add
marketplace/remote catalogs, or treat generate default success as pytest DoD.

---

## 31. High-Level Implementation Phases

| Phase | Name | Outcomes | Exit gate |
| ----- | ---- | -------- | --------- |
| **PHASE-01** | Pure pipeline | parse/validate; resolve (set profiles); plan Construct; verify resolution fields; plan_sha256 vectors; error_class; `--plan` bind API | SPK-100; REQ-020..026, 040..043, 084, 086, 087, 091 |
| **PHASE-02** | Filesystem | stage identity; path confinement; exclusive place; fail non-empty dest; stage_path errors | SPK-101; REQ-030..032, 090 |
| **PHASE-03** | Generate + verify + lock | lock production; default/strict/none; bind e2e; network disclosure | SPK-103; REQ-010..013, 080, 085, 086 |
| **PHASE-04** | Catalog content + emit | Core + AI-native; profiles; scripts inventory; forbidden paths; kind-qualified catalog | SPK-002, SPK-050, SPK-052, SPK-102; REQ-050..078, 087, 088 |
| **PHASE-05** | Hybrid + dogfood | Frozen template cell CI; foundry dogfood Core; docs polish; release | REQ-001, 081, 089, 077 |
| **PHASE-06** | Harden | Performance; residual OQ; admission; optional strict tuning | Risk residual acceptance |

Milestones (indicative):

| MS | Meaning |
| -- | ------- |
| MS-001 | `foundry plan` golden stable for cli |
| MS-002 | First successful `generate` to empty dest with default verify |
| MS-003 | All three archetypes golden emit |
| MS-004 | Template snapshot CI green |
| MS-005 | Dogfood: foundry repo itself uses Core conventions |

**Not included:** sprint task packets, ticket breakdowns, or coding backlog.

---

## 32. Completion Checklist (spec-revision stage)

- [x] All required sections present and non-placeholder
- [x] Status: **Accepted — implementation authority**
- [x] Actual revision date recorded
- [x] Every FND-001..012 dispositioned (exactly one disposition each)
- [x] No silent finding loss
- [x] Accepted corrections integrated in body
- [x] Stable REQ IDs retained; REQ-084..091 allocated from unused range
- [x] Must REQs have verification paths
- [x] Traceability updated
- [x] REC disposition ledger carried
- [x] Blueprint locks and non-goals preserved
- [x] Ecosystem / AI-native / architecture locks preserved
- [x] Strengths preserved
- [x] High-level phases present; no granular coding backlog
- [x] Standalone character
- [x] Updated implementation handoff complete
- [x] Allowed file scope (revised specification only)
- [x] Proposed spec and review not modified
- [x] No implementation plan as main work

---

*End of revised definitive specification v0.2 — implementation authority (pending human stage acceptance in program manifest).*
