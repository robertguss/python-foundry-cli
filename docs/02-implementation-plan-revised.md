# Final Revised Implementation Plan — python-foundry

- **Artifact type:** Final revised implementation plan
- **Program:** python-foundry
- **Status:** Accepted — delivery authority
- **Version:** 0.2
- **Plan date (base):** 2026-08-01
- **Actual revision date:** 2026-08-01
- **Last updated:** 2026-08-01
- **Delivery status:** Delivery sequence authority (how to build) after human
  stage acceptance; **not** product law
- **Implementation authority (product law):**
  `docs/specifications/02-definitive-specification-revised.md` v0.2
  (accepted; commit `faffbdc`)
- **Base plan:** `docs/plans/01-implementation-plan.md` v0.1 (proposed; stage
  accepted `ab72895`; **not** delivery authority)
- **Accepted review:** `docs/reviews/02-implementation-plan-adversarial-review.md`
  v0.1 (`7032972`); findings FND-200..FND-205; gate was Conditional
- **Commissioning prompt:** `docs/prompts/09-implementation-plan-revision-prompt.md`
- **Stage:** `plan-revision` (human-accepted 2026-08-01; see `research-program.toml` `accepted_commit`)
- **Depends on:** Accepted `plan-review`
- **Phase range used:** PHASE-01..PHASE-06 (continuity with revised-spec §31)
- **Milestone range used:** MS-001, MS-002, MS-003a, MS-003b, MS-DF0, MS-004,
  MS-005, MS-006
- **Finding dispositions:** FND-200..FND-205 (see §R2)
- **This artifact does not supersede** Blueprint locks, Charter methodology, or
  revised-spec REQs

> Translates the accepted revised specification into a **safe delivery sequence**.
> Defines **how to build**, not what the architecture should become.
> **Phases and milestones only** — no coding backlog, sprint tickets, or agent
> task packets. Contract: `program/contracts/implementation-plan.md`.
> High plan-review findings are resolved; artifact status is honest delivery
> authority pending human stage acceptance.

---

## R1. Revision Summary

This revision elevates the proposed implementation plan to **delivery sequence
authority** by disposing plan-review findings FND-200..FND-205 and integrating
sequencing corrections into the body (not ledger-only):

1. **FND-200 (High):** Catalog freeze is no longer irreversible before dogfood
   can falsify Core. Early **foundry Core tooling smoke (MS-DF0)** is a hard
   prerequisite to multi-archetype freeze (MS-003b). PHASE-04 exit is
   **content-complete for the closed catalog**, not an irreversible public
   freeze. When dogfood falsifies Core, the plan **re-gates MS-003a/MS-003b**
   (honest reopen of freeze claims) — no post-exit “still PHASE-04” fiction.
2. **FND-201 (High):** PHASE-04 progressive integration via **MS-003a**
   (full-Core `cli`) then **MS-003b** (all three archetypes + profiles + agent
   surface claims). Continuous CI of earlier goldens is mandatory.
3. **FND-202 (Medium):** Dual-gate ty: MS-002 proves **runner wiring + green on
   minimal cell** with **provisional** ty config; **SPK-002** freezes practical
   Core ty defaults before MS-003a. ty remains Required in default verify.
4. **FND-203 (Medium):** **MS-005 (dogfood) before MS-004 (hybrid public claim)**.
5. **FND-204 (Medium):** MS-005 acceptance is **observable only** (CI + surface
   separation + checked-in dogfood record). Owner attestation is non-gating.
6. **FND-205 (Medium):** Explicit **residual policy table** — residual-accept
   cannot substitute for forbidden-path green, dotenv/Claude absence, or
   ty/fnox demotion (DEC only).

**Status:** All High findings resolved; no Critical plan findings; no remaining
implementation-blocking plan finding → artifact status **`Accepted — delivery
authority`**. Human must still accept the stage and record `accepted_commit`
before treating the program graph as complete for product implementation under
this plan.

---

## R2. Finding Disposition Ledger

| FND | Severity | Disposition | Integration summary |
| --- | -------- | ----------- | ------------------- |
| **FND-200** | High | **Accepted with modification** | Early dogfood smoke as **MS-DF0** (hard prereq to MS-003b multi-archetype freeze) **and** provisional/content-complete PHASE-04 language (not irreversible public freeze) **and** honest re-gate of MS-003a/b when dogfood falsifies Core. Prefer simplification: no new phase; MS-DF0 is a named milestone inside PHASE-04. |
| **FND-201** | High | **Accepted** | Progressive integration: **MS-003a** full-Core `cli` before **MS-003b** three-archetype freeze; ordered PHASE-04 exit bullets; continuous CI of landed goldens. |
| **FND-202** | Medium | **Accepted with modification** | Dual-gate: MS-002 = ty **runner wired + green on minimal cell**, config **provisional**; SPK-002 = practical ty config **freeze** before MS-003a. No SPK-002-lite ID invented; evidence is MS-002 acceptance language + SPK-002 gate. ty not demoted from default verify. |
| **FND-203** | Medium | **Accepted** | Directed dependency **MS-005 → MS-004** for public hybrid claim; PHASE-05 exit ordered dogfood → snapshot → release notes. |
| **FND-204** | Medium | **Accepted** | MS-005 acceptance = product CI + AGENTS/surface-separation evidence + checked-in dogfood record; owner attestation demoted to optional non-gating note. |
| **FND-205** | Medium | **Accepted** | Residual policy table (§16) binds which spikes are hard for which Must outcomes; residual-accept cannot green forbidden paths or demote ty/fnox without DEC. |

**Silent finding loss:** none. All FND-200..205 dispositioned exactly once.

---

## R3. Integrated Correction Ledger

| Theme | Proposed plan (v0.1) | Revised plan (v0.2) |
| ----- | -------------------- | ------------------- |
| Catalog freeze durability | MS-003 all-at-once; dogfood only PHASE-05; rollback “fix in PHASE-04 scope” after exit | MS-003a → MS-DF0 → MS-003b; PHASE-04 exit = content-complete; dogfood falsify → re-gate MS-003a/b |
| PHASE-04 progressive integration | Single MS-003 | MS-003a (cli Core) + MS-003b (full closed catalog) |
| ty timing | ty green at MS-002; SPK-002 only PHASE-04 freeze | Dual-gate: provisional config at MS-002; freeze at SPK-002 before MS-003a |
| Hybrid vs dogfood | MS-004 ∥ MS-005 unordered | MS-005 prerequisite of MS-004 |
| MS-005 evidence | Included owner attestation | Observable CI + surface separation + dogfood record only |
| Residual-accept | Soft “complete or residual-accepted” on spikes | Hard residual policy matrix; Must-red returns to owning phase |
| Rollback reopen fiction | “fix catalog in PHASE-04 scope” after exit | Re-open freeze claims by re-gating named milestones |

---

## R4. Preserved Strengths

From accepted plan-review §3 — preserved in this revision:

- Continuity with revised-spec PHASE-01..06 (no phase invent/merge)
- Thin E2E at PHASE-03 / MS-002 before full catalog breadth
- Spike gates SPK-100..103, SPK-002/050/052, SPK-001 placement intent
- Must REQ traceability table
- Explicit residual risk sequencing (ty, fnox, lock, `--plan`)
- No coding backlog; phases/milestones only
- Subordination language to revised specification v0.2
- Linear dependency graph (no circular `depends_on`)
- Product locks not reversed (ty, fnox+age, AGENTS-only, no Claude, exclusive
  place, custom engine, closed catalog, generate-time lock, verify precedence,
  optional `--plan` bind)

---

## 1. Artifact Metadata

| Field | Value |
| ----- | ----- |
| Program ID | python-foundry |
| Plan ID | `docs/plans/02-implementation-plan-revised.md` |
| Plan version | 0.2 |
| Actual revision date | 2026-08-01 |
| Status | **Accepted — delivery authority** |
| Rigor tier | standard |
| Host OS targets | macOS + Linux only |
| Provisional CLI name | `foundry` (OQ-105 branding; package `python-foundry`) |
| Operator | robertguss |
| Upstream authority commit (revised spec) | `faffbdc` |
| Base plan commit | `ab72895` |
| Plan-review commit | `7032972` |
| Plan HEAD at write time | see Git when committed |

---

## 2. Implementation Authority

| Authority | Role |
| --------- | ---- |
| Accepted `DEC-###` | Highest; none present under `decisions/` at revision time |
| `docs/00-program-blueprint.md` | Locked scope, non-goals, success criteria |
| `docs/01-research-charter.md` | Evidence and methodology rules |
| **`docs/specifications/02-definitive-specification-revised.md` v0.2** | **Product law / implementation authority** |
| **This plan (v0.2)** | **Delivery sequence authority** after human stage acceptance |
| Proposed plan v0.1 | Provenance / base text only |
| Plan-review FND-200..205 | Disposed; not automatic product law |

**Subordination rule:** This plan MUST NOT change architecture, REQ semantics,
locks, or non-goals. If sequencing appears to require a product change, record an
open question or rollback trigger — do not silently amend REQs.

**Starting phase model:** revised-spec §30.3 phase gates and §31 PHASE-01..06.
No merge or split of phases. Refinements are executable entry/exit criteria,
progressive milestones inside PHASE-04/05, residual policy, and freeze durability
language only.

---

## 3. Objectives

Deliver python-foundry **v1** under the revised specification by sequencing work so that:

1. **Load-bearing unknowns** (ty, fnox, lock network cost, plan bind) are gated
   by spikes before they harden wrong defaults.
2. **Thin end-to-end capability** appears early: pure Construct → stage →
   lock → default verify → exclusive place for a minimal `cli` cell, before full
   catalog content breadth.
3. **Continuous integration** of pure pipeline, filesystem, generate, and catalog
   emit — progressive gates inside PHASE-04; not a big-bang late integration.
4. **Early dogfood smoke** of foundry product Core tooling alignment **before**
   multi-archetype catalog freeze; **full dogfood** before public hybrid claim.
5. **Hybrid surface** lands as a CI-frozen GitHub template snapshot from the
   catalog SoT (frozen cell: archetype `cli`, `profiles=[]`, …) only after
   dogfood-informed Core stability.
6. Every **Must REQ** maps to at least one phase with observable exit evidence.
7. Residual risks (§30.4: ty, fnox/dotenv, lock cost, agents skip `--plan`,
   provisional CLI name) are explicitly sequenced with an honest residual policy.

Success aligns with revised-spec §29.2 product v1 DoD and Blueprint §8 success
criteria — without reopening non-goals.

---

## 4. Non-Goals

### Plan non-goals (this artifact)

- Granular coding backlog, sprint tickets, or coding-agent task packets
- Changing REQs, architecture, or tool selections
- Product implementation as the main deliverable of the research stage
- Inventing formal `DEC-###` records without human process

### Product non-goals (inherited — MUST NOT become v1 scope without DEC / Blueprint amendment)

From Blueprint §6 and revised-spec §5.2 / §27:

- Windows support
- Notebooks, GUI apps, mobile
- Framework zoo / multi-stack marketplace
- Remote/plugin catalogs or template marketplace
- dotenv / `.env` as secret storage
- Claude adapters / `CLAUDE.md` / `.claude/` Core emit
- Default MCP kitchen-sink catalogs
- Copier/Cookiecutter as the foundry runtime engine
- Existing-project update/merge in v1
- Demoting **ty** or **fnox** from Core without DEC
- Treating default verify success as pytest DoD (pytest remains agent DoD / strict)

---

## 5. Assumptions

1. Revised specification v0.2 remains implementation authority for the duration
   of delivery unless superseded by an accepted DEC or a later accepted
   specification revision.
2. Product implementation may live in this repository or a linked product tree;
   phase acceptance is defined by **observable behavior and tests**, not by which
   monorepo path holds code.
3. Operator environment has **uv**, network (for lock/sync where required), and
   ability to run **ruff**, **ty**, **pytest** as specified for verify tiers.
4. Host OS for development and CI: **Linux required**; macOS optional (OQ-005).
5. CLI binary name remains provisional `foundry` until owner DEC (OQ-105);
   package identity `python-foundry` is stable.
6. Closed catalog units for v1 are exactly those in revised-spec §11.3
   (core; archetypes `cli`|`scripts`|`data-etl`; profiles `http`|`hooks-hk`|`data-etl`).
7. go-foundry is prior art only (REQ-083 / §9.10); stage-root confinement is
   sufficient for v1 (no FD-level openat parity required to exit PHASE-02).
8. No accepted DECs exist at plan time that alter locks.
9. Greenfield product: no production user migration (see §12).

---

## 6. Dependency Graph

```text
PHASE-01 Pure pipeline
    │
    ▼
PHASE-02 Filesystem (stage + exclusive place)
    │
    ▼
PHASE-03 Generate + verify + lock  ◄── thin E2E (minimal catalog cell)
    │                               ◄── ty runner green; config provisional
    ▼
PHASE-04 Catalog content + emit
    │  MS-003a full-Core cli (+ SPK-002/052 freeze gates)
    │  MS-DF0  foundry Core tooling smoke
    │  MS-003b all archetypes + profiles + SPK-102/050
    │  (PHASE-04 exit = content-complete; not public hybrid freeze)
    ▼
PHASE-05 Hybrid template + dogfood + docs
    │  MS-005 full dogfood  ──►  MS-004 hybrid snapshot claim
    ▼
PHASE-06 Harden + residual risk acceptance
```

| From | To | Dependency kind |
| ---- | -- | --------------- |
| PHASE-01 | PHASE-02 | Construct + plan bind API shape stable enough to drive stage inputs |
| PHASE-02 | PHASE-03 | Stage/place primitives callable from generate orchestration |
| PHASE-03 | PHASE-04 | Generate lifecycle green on minimal cell; lock+verify semantics proven; ty config provisional |
| MS-003a | MS-DF0 | Full-Core `cli` emit available as dogfood reference (MS-DF0 may start scaffolding earlier; smoke **acceptance** needs MS-003a green or equivalent Core cell) |
| MS-DF0 | MS-003b | Early dogfood smoke before multi-archetype freeze claim |
| MS-003b | PHASE-05 entry | Content-complete closed catalog + residual policy satisfied |
| MS-005 | MS-004 | Dogfood before public hybrid claim |
| PHASE-05 | PHASE-06 | Hybrid CI + dogfood evidence; release path exercised at least once |
| SPK-100 | PHASE-01 exit | Pure plan golden for minimal CLI |
| SPK-101 | PHASE-02 exit | Stage + exclusive place |
| SPK-103 | PHASE-03 exit | Default verify cost / network disclosure acceptable |
| SPK-002 | MS-003a | Practical ty config freeze before full-Core `cli` freeze |
| SPK-052 | MS-003a / secrets skill freeze | fnox+age smoke before secrets emit freeze |
| SPK-102, SPK-050 | MS-003b | Forbidden paths + multi-agent surface before full catalog freeze |
| SPK-001 | Before heavy template reliance in PHASE-04 | uv+ruff+ty+pytest smoke on sample trees |

**No circular phase dependencies.** Later phases must not redefine earlier exit
criteria. Freeze **claims** may be re-gated when later evidence falsifies them
(§19); that re-gates named milestones — it does not invent a post-exit PHASE-04
holding pattern.

---

## 7. Phase Overview

| Phase | Name | Depends on | User-visible outcome |
| ----- | ---- | ---------- | -------------------- |
| **PHASE-01** | Pure pipeline | None | `validate` / `plan` produce deterministic Construct; kind-qualified resolve; verify fields + `plan_sha256` + `error_class`; `--plan` bind API shape testable without writes |
| **PHASE-02** | Filesystem | PHASE-01 | Sibling unique stage; path confinement; exclusive place; fail non-empty dest; failures emit absolute `stage_path` |
| **PHASE-03** | Generate + verify + lock | PHASE-02 | First real `generate` to empty dest: lock production, default/strict/none, optional plan bind e2e, place only on success; ty runner green, config provisional |
| **PHASE-04** | Catalog content + emit | PHASE-03 | Progressive: full-Core `cli` → dogfood smoke → all archetypes/profiles/AI-native; content-complete closed catalog |
| **PHASE-05** | Hybrid + dogfood | PHASE-04 | Full dogfood then frozen public template CI green; editor docs; release packaging path |
| **PHASE-06** | Harden | PHASE-05 | Residual risks accepted or mitigated per policy; admission discipline; performance/ops polish; v1 readiness evidence |

---

## 8. Phases

## PHASE-01 — Pure pipeline

- **Status:** Planned
- **Objective:** Implement the write-free pipeline: parse/validate Project Spec,
  load closed catalog, resolve archetype + profiles (set membership; catalog apply
  order), resolve effective verify fields, Construct Generation Plan with
  `plan_sha256` and machine-readable `error_class` taxonomy; expose optional
  `--plan` bind **API shape** (match/mismatch) without performing stage writes.
- **User-visible outcome:** Operator/agent can run `foundry validate` and
  `foundry plan` (text/JSON) on a TOML spec and get a stable, hashable plan for
  the minimal `cli` cell; catalog list/show kind-qualified.
- **Depends on:** None
- **Requirements:** REQ-010 (partial: validate/plan), REQ-011, REQ-013,
  REQ-020..026, REQ-040..043, REQ-041, REQ-082 (purity), REQ-084 (plan fields),
  REQ-086 (bind shape), REQ-087 (kind in plan/catalog), REQ-091; REQ-001/003/083
  discipline
- **Milestones:** MS-001
- **Primary risks:** RSK-100 (non-determinism), RSK-109 (dual-id confusion),
  RSK-108 (bind path education later)

### Entry Criteria

- Revised specification v0.2 accepted as implementation authority.
- This revised plan accepted as delivery authority (or owner proceeds under
  residual risk with this plan as guidance).
- Empty or scaffold product package able to host pure modules per revised-spec §10.1.

### Scope

- Package layout skeleton respecting purity: `spec`, `catalog`, `resolve`,
  `plan`, `report`; CLI wiring for `validate`, `plan`, `catalog list|show`,
  `version` (stub generate OK).
- TOML schema = 1 validation; unknown keys/profiles hard-fail; no secrets fields.
- Profile set semantics + catalog total apply order (FND-002).
- Effective verify resolution recorded on plan: `verify_mode`, `verify_source`
  (CLI > TOML > `default`) even though runners are later (FND-001).
- Plan-as-contract fields (§9.3); canonicalization + fixed `plan_sha256` test
  vector (FND-009).
- JSON error_class closed set for validation/resolve/plan_bind/internal (§12.1.1).
- Optional `--plan` load + recompute + hard-fail on digest/version/catalog
  mismatch **before** any write API is invoked (FND-004 shape).
- Kind-qualified catalog list/show and plan unit references (FND-007).
- Minimal catalog manifests sufficient for resolve (may use stub file inventories).

### Explicit Non-Goals

- Stage, place, render-to-disk, lock, or verify runners.
- Full template body content for all archetypes.
- GitHub template hybrid, dogfood, PyPI publish.
- Copier/Cookiecutter engine.

### Architecture and Components

- Follow revised-spec §10.1 map; enforce `plan` does not import `fsx` /
  `generate` / `cli` (REQ-082).
- Catalog as package data; digest in every plan (REQ-041).

### Integrations

- None external required (no network for validate/plan by default).

### Data or Migration Work

- N/A (greenfield). Schema version fixed at `1`.

### Evidence Spikes

| ID | Intent | Gate |
| -- | ------ | ---- |
| **SPK-100** | Pure plan golden for minimal CLI Construct | **PHASE-01 exit** |

### Testing and Verification

- Unit tests: pure packages only; no FS side effects for validate/plan.
- Golden: plan JSON (and text if applicable) for minimal `cli` + empty profiles.
- Fixture matrix: verify_source cli/toml/default; profile membership order
  independence; duplicate profiles fail; plan_sha256 vector; bind match/mismatch.
- Architecture test: import boundary purity.

### Security and Reliability

- Reject secret material in Project Spec (REQ-022).
- Deterministic plan body: no wall-clock/random in contract fields (RSK-100).

### Dogfooding or Operational Validation

- Not yet (dogfood smoke is MS-DF0 in PHASE-04; full dogfood MS-005 in PHASE-05).
  Operators may exercise CLI manually.

### Rollback and Reconsideration Triggers

- Cannot produce stable `plan_sha256` across platforms → stop; fix
  canonicalization before PHASE-02.
- Purity boundary violated (plan imports write path) → reconsider layout before
  filesystem work.

### Exit Criteria

Observable evidence **all** true:

1. SPK-100 complete: checked-in golden plan for minimal `cli` matches
   recomputed Construct.
2. Fixed `plan_sha256` test vector passes.
3. Profile apply order fixtures: reordered TOML arrays with same membership
   yield identical plan body (excluding non-contract noise).
4. Verify fields present on plan; precedence matrix tests pass (REQ-084).
5. Kind-qualified catalog list/show distinguishes archetype/profile `data-etl`.
6. `--plan` bind mismatch fails with `error_class=plan_bind` without creating
   stage directories.
7. `validate` and `plan` leave destination tree untouched (property or e2e check).
8. MS-001 acceptance evidence recorded.

---

## PHASE-02 — Filesystem

- **Status:** Planned
- **Objective:** Implement fail-closed write primitives: unique sibling stage
  identity, path confinement under stage root, exclusive place to empty
  destination, preserve stage and emit absolute `stage_path` on failure.
- **User-visible outcome:** Generate orchestration can stage files and either
  atomically place a complete tree or leave the destination untouched with a
  recoverable stage path (still may use stub render content).
- **Depends on:** PHASE-01
- **Requirements:** REQ-012 (partial), REQ-030..032, REQ-090; REQ-083 (no
  blocking on FD openat); supports later REQ-031 place semantics
- **Milestones:** supports MS-002 (does not complete it alone)
- **Primary risks:** RSK-101 (leftover stages), RSK-105 (over-copy go-foundry FD)

### Entry Criteria

- PHASE-01 exit criteria met.
- Plan Construct available to name planned paths for stage writes (even if
  content is fixture bytes).

### Scope

- Stage naming: `.foundry-stage-<dest-basename>-<unique>`; collision allocates new
  name; never deletes prior failed stages (FND-011 / REQ-090).
- Fail if destination exists and is non-empty (REQ-030).
- Path confinement: no escape outside stage root (REQ-032).
- Exclusive place stage → destination; destination untouched on failure.
- Error/JSON reports include absolute `stage_path` after stage creation.
- Prefer same-filesystem parent for rename place (ops guidance §15).

### Explicit Non-Goals

- Full verify runners and lock production (PHASE-03).
- Full catalog emit content (PHASE-04).
- Existing-project merge/update (forbidden v1).
- FD-level openat transaction parity.

### Architecture and Components

- `fsx` module only for stage/place; no plan content invention (§10.2).
- `generate` may be thin driver for tests; full verify lifecycle is PHASE-03.

### Integrations

- OS filesystem only; Linux CI required.

### Data or Migration Work

- N/A. Failed stages are operator-deletable artifacts, not migrated data.

### Evidence Spikes

| ID | Intent | Gate |
| -- | ------ | ---- |
| **SPK-101** | Stage + exclusive place; fail non-empty dest | **PHASE-02 exit** |

### Testing and Verification

- e2e: empty dest place succeeds; non-empty dest fails; two consecutive failures
  leave two stages; `stage_path` parseable from JSON stderr report.
- Confinement tests: reject `..` / symlink escape attempts in planned paths.
- No destination mutation on mid-stage failure injection.

### Security and Reliability

- Fail-closed destination (partial generation never leaves half-written dest).
- Stage retention on failure for agent recovery (RSK-101 mitigated by clear
  `stage_path` messaging).

### Dogfooding or Operational Validation

- Manual failure injection acceptable; not product dogfood yet.

### Rollback and Reconsideration Triggers

- Cannot achieve exclusive place without dest corruption on Linux CI → block
  PHASE-03.
- Temptation to implement in-place merge for “convenience” → reject; requires
  DEC + spec change (REQ-033).

### Exit Criteria

1. SPK-101 complete with automated e2e.
2. REQ-030, REQ-031 (stage+place portion), REQ-032, REQ-090 acceptance evidence
   from revised-spec satisfied.
3. Documented stage naming and failure recovery notes for agents (can be brief
   in product AGENTS later expanded PHASE-04/05).
4. Ready to call fsx from generate orchestration in PHASE-03.

---

## PHASE-03 — Generate + verify + lock

- **Status:** Planned
- **Objective:** Complete the generate lifecycle on a **minimal catalog cell**
  (at least `cli` + core stub sufficient for lock+verify): optional plan bind
  e2e, render into stage, generate-time `uv.lock` produce/refresh, verify tiers
  default/strict/none with CLI>TOML>default precedence, exclusive place only on
  success; network disclosure for lock/sync.
- **User-visible outcome:** First successful `foundry generate --spec …` into an
  empty destination with **default verify** producing a tooling-sync-green tree
  (sync + ruff + ty — **not** pytest as default success).
- **Depends on:** PHASE-02
- **Requirements:** REQ-010..013, REQ-024 (bind execute), REQ-080, REQ-084,
  REQ-085, REQ-086 (e2e), REQ-091; partial REQ-052 lock behavior
- **Milestones:** MS-002
- **Primary risks:** RSK-102, RSK-107 (network/cost), RSK-001 (uv churn),
  RSK-100, RSK-108, RSK-002 (ty maturity — provisional at this phase)

### Entry Criteria

- PHASE-02 exit criteria met.
- PHASE-01 plan bind shape and verify field recording available.
- Operator tools installed for default verify: uv, ruff, ty.

### Scope

- `generate` orchestration: bind-or-rebuild → stage → lock → verify → place.
- Lock production before default/strict verify (FND-003 / REQ-085).
- Verify tiers per §9.5; strict = default + pytest; **no** pre-commit pre-place
  (FND-006).
- `--verify none`: loud warning; best-effort lock rules per spec; still no silent
  stale lock on successful place.
- Network need disclosed in docs/CLI help/warnings.
- Minimal emit content: enough pyproject + sources for ruff/ty/sync (full Core
  inventory is PHASE-04 / MS-003a).
- JSON reports with `error_class` in {`render`,`lock`,`verify`,`place`,…}.
- **ty dual-gate (FND-202):** default verify **includes** real `uv run ty check`
  on the minimal cell. MS-002 proves **runner wiring + green on minimal cell**.
  Template ty configuration remains **provisional** until SPK-002 (PHASE-04 /
  MS-003a). Do not freeze Core ty defaults at MS-002.

### Explicit Non-Goals

- Completing all three archetypes and all profiles (PHASE-04 / MS-003b).
- Freezing practical ty template defaults (SPK-002 / MS-003a).
- Hybrid GitHub template CI (PHASE-05).
- Claiming multi-agent skill surface completeness (SPK-050 in PHASE-04).
- Pytest as default verify success.
- Full foundry-repo dogfood (MS-DF0 / MS-005).

### Architecture and Components

- `render`, `generate`, `verify` modules; tool runners sandboxable in tests.
- Custom engine only (REQ engine lock).

### Integrations

- uv lock/sync (network); ruff; ty; pytest (strict).

### Data or Migration Work

- N/A.

### Evidence Spikes

| ID | Intent | Gate |
| -- | ------ | ---- |
| **SPK-103** | Default verify cost/time and network disclosure acceptable for owner CI | **PHASE-03 exit** |
| SPK-001 (partial) | uv+ruff+ty+pytest smoke on generated minimal tree | Before expanding templates in PHASE-04 |

### Testing and Verification

- e2e matrix: default / strict / none; CLI vs TOML verify disagreement.
- Bind e2e: matching plan places; bit-flipped plan fails before stage writes with
  `plan_bind`.
- Lock matrix (minimal): default python pin; optional alternate pin if already
  supported; failure of lock aborts place.
- Verify failure aborts place; dest empty/untouched.
- Mock/sandbox runners where full tool cost is excessive; at least one real-tool
  e2e on Linux CI including **real ty check** on minimal cell.
- Record provisional ty config path used for MS-002 (file path + pin notes).

### Security and Reliability

- Fail-closed place; disclose network (RSK-102/107).
- No secrets in spec; no dotenv introduction in minimal templates.

### Dogfooding or Operational Validation

- Owner runs one real generate outside CI (optional but recommended).
- Foundry-repo Core tooling smoke is **MS-DF0** (PHASE-04), not this phase.

### Rollback and Reconsideration Triggers

- Default verify cost unacceptable after SPK-103 → options: document `none` for
  offline, optimize runners, or owner DEC to adjust **only** via formal process
  (must not silently drop ty from default).
- Cannot produce honest locks on CI → block PHASE-04 content work.
- Agents systematically skip `--plan` (observed later) → strengthen docs/skills
  in PHASE-04/05 (RSK-108); not an architecture reopen.
- Minimal-cell ty green but config clearly unusable for expansion → proceed to
  PHASE-04 with provisional label; **do not** claim SPK-002 complete.

### Exit Criteria

1. MS-002 acceptance evidence: documented command path yields successful generate
   to empty dest with default verify.
2. SPK-103 recorded (cost notes + disclosure present in user-facing help/docs).
3. Precedence matrix and bind e2e green.
4. Default success definition documented as tooling-sync green (not pytest).
5. Lock production path exercised; `uv sync --locked` used in default/strict.
6. **ty dual-gate record:** real ty check green on minimal cell; config labeled
   **provisional** (not Core-defaults-frozen).

---

## PHASE-04 — Catalog content + emit

- **Status:** Planned
- **Objective:** Flesh the closed catalog to full v1 Core, archetypes, profiles,
  and AI-native emit contracts with **progressive integration gates**;
  kind-qualified UX complete; forbidden-path conformance; scripts archetype
  inventory (REQ-088); lock matrix across pins/profiles; gate on ty/fnox/
  agent-surface spikes before freeze claims; early foundry Core tooling smoke
  before multi-archetype freeze.
- **User-visible outcome:** Generating any of `cli` | `scripts` | `data-etl`
  with allowed profiles yields projects that match normative inventories,
  pass default verify, include AGENTS.md + closed skills only, and never emit
  dotenv secrets or Claude adapters. Foundry product CI already runs Core-aligned
  tooling gates (MS-DF0).
- **Depends on:** PHASE-03
- **Requirements:** REQ-040, REQ-044 (admission process start), REQ-050..078
  (except REQ-077 → PHASE-05), REQ-087, REQ-088; REQ-052..063, REQ-070..076,
  REQ-078; supports REQ-001 hybrid prep
- **Milestones:** MS-003a, MS-DF0, MS-003b
- **Primary risks:** RSK-002 (ty), RSK-007/050 (fnox/dotenv), RSK-051, RSK-053,
  RSK-054, RSK-055, RSK-104, RSK-109

### Entry Criteria

- PHASE-03 exit criteria met (thin E2E generate path works; ty provisional).
- SPK-001 smoke green enough to author templates confidently.

### Scope

**Progressive order (FND-201 + FND-200):**

1. **MS-003a — full-Core `cli`:** Core toolchain emit (uv, ruff, ty, pytest,
   pre-commit Default, fnox+age, GHA); archetype `cli` (Typer Default); empty
   profiles golden; default verify e2e; forbidden-path suite on that cell;
   AI-native baseline for cli (AGENTS.md + required skills paths); **SPK-002**
   freezes practical ty config; **SPK-052** before secrets skill freeze.
2. **MS-DF0 — foundry Core tooling smoke:** product CI locked uv sync + ruff +
   ty + pytest green; product AGENTS (or product rules) present; research-only
   skills **not** emitted into Generated Project templates (inventory/test
   check). Hard prerequisite to MS-003b multi-archetype freeze claim.
3. **MS-003b — full closed catalog:** archetypes `scripts` (REQ-088) and
   `data-etl`; profiles `http`, `hooks-hk`, `data-etl` composition; generate-time
   lock matrix; kind-qualified catalog UX complete; **SPK-102** forbidden-path
   suite across goldens; **SPK-050** before multi-agent emit completeness claims.

Also:

- Catalog tree per §9.6 / §11.3 with versions lock.
- Catalog admission notes for future units (REQ-044) — process, not open catalog.
- Continuous integration: earlier goldens remain green as later archetypes land
  (do not delete or skip MS-003a goldens to “move fast”).

### Explicit Non-Goals

- Public GitHub template repo publish / hybrid “done” claim (PHASE-05 / MS-004).
- Full foundry product dogfood completeness (MS-005 — PHASE-05); MS-DF0 is smoke
  only.
- Editor integration docs (REQ-077 → PHASE-05).
- Renaming profile `data-etl` (OQ-106 deferred).
- Promoting hk to Core (requires DEC).
- MCP opt-in profile.
- Irreversible public freeze language at PHASE-04 exit.

### Architecture and Components

- Catalog authoring tree packaged as data; custom renderer only.
- Foundry vs Generated agent surfaces separated (REQ-076): research skills do not
  ship into Generated Projects.

### Integrations

- GitHub Actions templates for Generated Projects.
- fnox + age local key workflow (documented).

### Data or Migration Work

- N/A for users. Catalog versioning via foundry version + catalog digest only.

### Evidence Spikes

| ID | Intent | Gate |
| -- | ------ | ---- |
| **SPK-002** | ty sample CLI tree + CI; freeze practical ty config | **Before MS-003a** (ty defaults frozen) |
| **SPK-052** | fnox exec + age smoke | **Before secrets skill freeze / MS-003a secrets claim** |
| **SPK-050** | AGENTS.md + `.agents/skills` operable on target agents | **Before MS-003b multi-agent completeness claims** |
| **SPK-102** | Catalog expand + forbidden paths | **MS-003b / PHASE-04 exit** |
| SPK-003 | hk vs pre-commit latency | **Only if** promoting hk (out of default path) |

### Testing and Verification

- Golden plans per progressive landing: first `cli` Core; then scripts/data-etl
  × representative profile subsets.
- Conformance inventories: required paths present; forbidden absent.
- scripts archetype inventory tests (REQ-088) at MS-003b.
- e2e generate: `cli` at MS-003a; all three archetypes at MS-003b with default
  verify.
- Forbidden-path suite (RSK-104) — hard; not residual-softened (§16).
- Dual-id docs/examples review (RSK-109).
- Continuous CI: MS-003a goldens stay green through MS-003b work.

### Security and Reliability

- fnox+age only for secrets; skills teach `fnox exec`; age keys out of git.
- No dotenv secret storage (RSK-007/050).
- Path confinement remains enforced on full file sets.

### Dogfooding or Operational Validation

- **MS-DF0 (required):** foundry product Core tooling smoke before MS-003b.
- Optional: agent session tries add-cli-command / add-script skills (SPK-050).
- Full foundry-repo dogfood conversion remains **MS-005** (PHASE-05).

### Rollback and Reconsideration Triggers

- SPK-002 shows ty unusable on Core sample → **do not demote ty silently**;
  escalate residual RSK-002 with owner DEC options (pin, config change, or formal
  exception path already required by REQ-055 risk linkage). See residual policy.
- SPK-052 fails → block secrets skill freeze; do not introduce dotenv fallback.
- Forbidden-path suite fails → block MS-003b / PHASE-04 exit (no residual-accept).
- Catalog sprawl pressure → enforce REQ-044 admission; no open catalog.
- MS-DF0 fails → **block MS-003b freeze claim** until smoke green or owner DEC
  documents why foundry product cannot share Core tooling gates (still must not
  invent a second Core for Generated Projects).
- Later dogfood (MS-005) falsifies Core → **re-gate MS-003a and/or MS-003b**
  (invalidate freeze claims; rework catalog/goldens; re-run affected spikes).
  Do **not** treat prior PHASE-04 exit as durable if freeze evidence is falsified.
  Do not invent a second Core for foundry-only convenience.

### Exit Criteria

Observable evidence **all** true:

1. **MS-003a** acceptance evidence recorded (full-Core `cli` + SPK-002/052 as
   required by residual policy).
2. **MS-DF0** acceptance evidence recorded (foundry Core tooling smoke green).
3. **MS-003b** acceptance evidence recorded (all three archetypes + profiles +
   SPK-102; SPK-050 for multi-agent claims).
4. Residual policy table (§16) satisfied for all PHASE-04 spikes — no forbidden
   residual-accept of Must outcomes.
5. scripts inventory conformance passes (REQ-088).
6. Forbidden paths absent across goldens.
7. Kind-qualified catalog UX goldens stable.
8. Agent DoD docs emit honestly (pytest after place; default ≠ pytest).
9. PHASE-04 exit documented as **content-complete for closed catalog** — **not**
   as public hybrid freeze or irreversible freeze. Public hybrid claim is MS-004
   after MS-005.

---

## PHASE-05 — Hybrid template + dogfood

- **Status:** Planned
- **Objective:** Complete full foundry product dogfood on Core conventions
  (**MS-005 first**); then ship hybrid GitHub template as CI-generated snapshot
  of frozen public template Project Spec cell (**MS-004**); editor documentation;
  release packaging path; polish operator docs including plan-bind workflow
  (RSK-108).
- **User-visible outcome:** Foundry itself develops under Core-like conventions;
  public template path and CLI path stay single-SoT with dogfood-informed Core
  stability; release/tag story clear.
- **Depends on:** PHASE-04 (content-complete)
- **Requirements:** REQ-001, REQ-077, REQ-081, REQ-089; release aspects of
  REQ-010 `version`; Blueprint hybrid L1
- **Milestones:** MS-005 (first), MS-004 (after MS-005)
- **Primary risks:** RSK-103 (template drift), RSK-108, RSK-005 (macOS CI cost),
  OQ-105 branding

### Entry Criteria

- PHASE-04 exit criteria met (MS-003a, MS-DF0, MS-003b).
- Frozen cell fields available as checked-in template Project Spec (§9.9 /
  REQ-089).

### Scope

**Ordered (FND-203):**

1. **MS-005 — full dogfood:** foundry product repository adopts Core conventions
   appropriate to an application-shaped uv project (tooling, AGENTS.md discipline,
   quality gates) without violating research-program vs product surface rules
   (REQ-076). Observable evidence only (FND-204).
2. **MS-004 — hybrid snapshot:** checked-in frozen public template Project Spec
   (`archetype=cli`, `profiles=[]`, name `python-foundry-template`, python 3.13
   default per REQ-089); CI job generates snapshot from catalog SoT and fails on
   drift (REQ-081); process docs forbid hand-editing template as second catalog.
3. Editor documentation only (REQ-077) — no mandatory `.cursor/rules` emit.
4. Release: version command reports foundry version + catalog digest; uv/PyPI
   install path decision recorded in ops notes (choose **uv-native publish**
   path; exact registry steps are milestone evidence, not a backlog).
5. Teach validate → plan → `generate --plan` in Generated Project and foundry
   AGENTS/skills (RSK-108).

### Explicit Non-Goals

- Marketplace distribution.
- Dual-maintaining template content by hand.
- Windows CI.
- Closing all residual ecosystem risks (PHASE-06).
- Claiming hybrid “done” before MS-005.

### Architecture and Components

- Template repo or published snapshot artifact is **output** of generate, not SoT.
- Catalog remains SoT inside foundry product package.

### Integrations

- GitHub Actions (foundry CI + template drift job).
- Optional macOS CI (not required for exit).

### Data or Migration Work

- N/A. Snapshot regeneration replaces prior snapshot wholly.

### Evidence Spikes

- None new required; carry residual SPK outcomes into dogfood validation.

### Testing and Verification

- Dogfood: foundry CI runs locked uv sync, ruff, ty, pytest on the product itself
  (extends MS-DF0 to full dogfood record).
- CI generate+diff for frozen cell (after MS-005).
- Golden alignment: template snapshot matches catalog goldens for that cell.
- Surface separation: research skills not in Generated emit path (test/inventory).
- Docs lint/link checks as practical.

### Security and Reliability

- Release artifacts free of secrets; age keys never published.
- Template snapshot contains no secret material.

### Dogfooding or Operational Validation

- **Primary full dogfood gate:** MS-005 — before public hybrid claim.
- Owner generates a real project from CLI and from template path once (after
  MS-004 CI exists; first CLI generate can be earlier).

### Rollback and Reconsideration Triggers

- Template drift CI flaky due to non-determinism → reopen PHASE-01/03
  determinism before release.
- Dogfood reveals Core emit unusable for foundry itself → **re-gate MS-003a
  and/or MS-003b** (catalog/golden rework); **block MS-004** until re-gated
  freeze evidence is green again. Do not invent a second Core. Do not claim
  “still in PHASE-04 after exit” without re-gating the named freeze milestones.
- CLI rename (OQ-105) if required → branding-only change set; must not rewrite
  architecture.

### Exit Criteria

1. **MS-005** acceptance evidence recorded (observable only).
2. **MS-004** acceptance evidence recorded; MS-005 is prerequisite.
3. REQ-081/089 acceptance evidence present.
4. REQ-077 editor docs published at agreed doc path.
5. Plan-bind workflow documented for agents (mitigate RSK-108).
6. Version + catalog digest reported by CLI.
7. Hybrid “done” implies dogfood-informed Core stability for the frozen cell.

---

## PHASE-06 — Harden

- **Status:** Planned
- **Objective:** Accept or mitigate residual delivery risks **per residual
  policy**; performance and ops polish; catalog admission discipline proven;
  optional strict-tuning notes; declare v1 implementation readiness against
  revised-spec §29.2.
- **User-visible outcome:** Stable v1 suitable for owner daily use; known
  limitations documented; no open Must REQ without evidence or residual policy
  row allowing documented residual.
- **Depends on:** PHASE-05
- **Requirements:** residual of REQ-002, REQ-003, REQ-033, REQ-044, REQ-083;
  performance expectations §19; ops §15–17
- **Milestones:** MS-006
- **Primary risks:** RSK-001, RSK-002 residual, RSK-055, RSK-107 residual,
  RSK-006 methodology (no new load-bearing claims)

### Entry Criteria

- PHASE-05 exit criteria met (MS-005 then MS-004).

### Scope

- Performance spot-checks against §19 expectations (plan pure speed; generate
  cost already informed by SPK-103).
- Residual risk register review: each High/Medium delivery risk either mitigated
  with evidence or owner-accepted **only if residual policy allows** (§16).
- Catalog admission dry-run: process for adding a unit is documented; no actual
  marketplace.
- Strict verify tuning notes (still no pre-commit pre-place).
- Offline/generate `none` documentation hardened.
- Final conformance sweep: Must REQs traceability checklist complete.
- OQ-105 resolved by owner decision or explicitly left provisional in release
  notes.

### Explicit Non-Goals

- Post-v1 deferred work (§26): update/merge, remote catalogs, MCP profile,
  monorepo workspaces, etc.
- Reopening rejected work (§27).
- Building a coding backlog for v2.

### Architecture and Components

- No architecture changes; harden tests, docs, CI only unless a blocking defect
  forces a fix within existing REQs.

### Integrations

- Release pipeline stabilization (tag ↔ version command).

### Data or Migration Work

- N/A.

### Evidence Spikes

- Only reopen SPK-002/052 if residual regressions appear.

### Testing and Verification

- Full regression: unit + golden + conformance + e2e generate matrix.
- Negative tests: non-goals still rejected (Windows paths not supported;
  unknown profiles fail; non-empty dest fails).

### Security and Reliability

- Final forbidden-path and secrets protocol audit.
- Stage hygiene docs for agents (RSK-101).

### Dogfooding or Operational Validation

- Continued dogfood; at least one full owner project generated post-harden
  candidate.

### Rollback and Reconsideration Triggers

- Must REQ still red with no residual-policy-allowed acceptance → not v1; return
  to owning phase / re-gate owning milestone.
- Pressure to add Windows/marketplace/dotenv → refuse without Blueprint/DEC.

### Exit Criteria

1. MS-006 acceptance evidence (v1 readiness).
2. Must REQ traceability table marked satisfied or residual-accepted **only where
   residual policy allows**.
3. Delivery risk register (§17) reviewed; each High/Medium item mitigated or
   policy-allowed owner-accepted.
4. No Critical open delivery defects against revised-spec v0.2.
5. Release notes list known limitations (ty residual, network for lock, provisional
   CLI name if still provisional).

---

## 9. Milestones

### MS-001 — `foundry plan` golden stable for cli

- **Phase:** PHASE-01
- **Outcome:** Deterministic plan Construct for minimal `cli` archetype is golden
  and hash-stable.
- **Prerequisites:** Spec/catalog/resolve/plan modules; SPK-100.
- **Acceptance evidence:**
  - Checked-in golden plan JSON for minimal `cli` + `profiles=[]`.
  - `plan_sha256` fixed test vector passes on Linux CI.
  - Reordered profile membership fixtures (when profiles present) do not change
    apply order relative to catalog.
  - Kind-qualified unit references present in plan output.
- **Blocks:** PHASE-02 start as *accepted* program gate; PHASE-03 bind e2e.

### MS-002 — First successful `generate` to empty dest with default verify

- **Phase:** PHASE-03
- **Outcome:** Thin end-to-end generate works.
- **Prerequisites:** MS-001; PHASE-02 (SPK-101); lock + default verify runners.
- **Acceptance evidence:**
  - Automated e2e: empty destination; `generate` with effective `default`; exit 0;
    dest contains project; stage not left behind on success.
  - Default verify ran tooling-sync steps (sync --locked, ruff, **ty**) — not
    pytest as the success criterion.
  - **ty dual-gate (FND-202):** real `ty check` green on minimal cell; ty template
    config recorded as **provisional** (not Core-defaults-frozen; SPK-002 still
    open).
  - Failure injection: verify fail → dest untouched + `stage_path` reported.
  - Optional `--plan` match succeeds; mismatch → `error_class=plan_bind` before
    stage writes.
- **Blocks:** PHASE-04 full-Core freeze (MS-003a); does **not** freeze ty defaults.
- **Does not prove:** practical ty config maturity for full Core (that is SPK-002).

### MS-003a — Full-Core `cli` golden emit

- **Phase:** PHASE-04
- **Outcome:** Full Core toolchain + `cli` archetype emit contract is complete and
  tested; progressive integration gate before multi-archetype breadth.
- **Prerequisites:** MS-002; SPK-002 (ty config freeze); SPK-052 (before secrets
  skill freeze); SPK-001 smoke sufficient.
- **Acceptance evidence:**
  - Golden plan + conformance inventory for `cli` + Core + empty profiles.
  - Default verify e2e green for `cli` at default python pin.
  - Forbidden-path suite green on the `cli` Core cell (no dotenv secret storage,
    no Claude adapters, MCP default none).
  - AI-native paths present for cli: AGENTS.md + required skills only.
  - SPK-002 complete: practical ty config frozen for Core templates.
  - SPK-052 complete before secrets skill freeze claim.
- **Blocks:** MS-DF0 acceptance as dogfood-reference completeness; MS-003b.
- **Continuous CI:** MS-003a goldens must remain green while MS-003b work proceeds.

### MS-DF0 — Foundry Core tooling smoke

- **Phase:** PHASE-04
- **Outcome:** Foundry product repository runs Core-aligned tooling gates and
  agent surface discipline **before** multi-archetype catalog freeze
  (FND-200 early dogfood smoke).
- **Prerequisites:** MS-002 at minimum for tooling philosophy; **MS-003a** for
  smoke acceptance against a real full-Core `cli` reference (product CI may be
  scaffolded earlier).
- **Acceptance evidence (observable only):**
  - Product CI: locked `uv sync` + ruff + ty + pytest green on foundry itself.
  - Product AGENTS.md (or product rules) exists.
  - Research-only skills are **not** present in Generated Project emit inventories
    (test or inventory check — REQ-076 separation).
  - Checked-in smoke record (dated commands/results or CI job IDs) in-repo.
- **Non-gating:** owner narrative notes.
- **Blocks:** MS-003b multi-archetype freeze claim.
- **Does not complete:** full MS-005 dogfood (deeper alignment + daily-dev
  record still PHASE-05).

### MS-003b — All three archetypes golden emit (content-complete freeze)

- **Phase:** PHASE-04
- **Outcome:** `cli`, `scripts`, and `data-etl` emit contracts are complete and
  tested; closed catalog is **content-complete**.
- **Prerequisites:** MS-003a; MS-DF0; SPK-102; SPK-050 (for multi-agent
  completeness claims); profile matrix and lock matrix ready.
- **Acceptance evidence:**
  - Golden plan + conformance inventory per archetype.
  - scripts inventory satisfies REQ-088.
  - Default verify e2e green for each archetype at default python pin.
  - Forbidden-path suite green across goldens (hard — §16).
  - AI-native paths present: AGENTS.md + required skills only.
  - SPK-050 complete or residual-allowed narrow agent list per §16 (cannot claim
    full multi-agent DoD if residual).
  - MS-003a goldens still green (continuous integration).
- **Blocks:** PHASE-05 entry; MS-005 / MS-004.
- **Freeze durability:** content-complete for closed catalog only. **Not** public
  hybrid freeze. Falsification by MS-005 dogfood **re-gates** this milestone
  (and/or MS-003a).

### MS-005 — Dogfood: foundry repo uses Core conventions

- **Phase:** PHASE-05
- **Outcome:** Foundry product is developed under Core-aligned tooling and agent
  surface discipline (full dogfood).
- **Prerequisites:** MS-003b; product CI capable of ruff/ty/pytest (MS-DF0 base).
- **Acceptance evidence (observable only — FND-204):**
  - Product CI runs locked uv sync + ruff + ty + pytest on foundry itself.
  - Product AGENTS.md (or equivalent product rules) exists without shipping
    research-only skills into Generated Project templates (test/inventory).
  - Checked-in dogfood record in-repo (dated commands/results, CI links, and
    Core-alignment notes for the frozen cell). **Necessary and sufficient**
    together with CI + surface separation.
- **Non-gating note:** owner may add a brief narrative that daily development
  uses the Core command surface — **not** acceptance evidence alone.
- **Blocks:** MS-004 public hybrid claim; MS-006 readiness claim.

### MS-004 — Template snapshot CI green (public hybrid claim)

- **Phase:** PHASE-05
- **Outcome:** Hybrid GitHub template is a generated snapshot of the frozen cell,
  dogfood-informed.
- **Prerequisites:** **MS-005**; MS-003b; checked-in frozen public template
  Project Spec.
- **Acceptance evidence:**
  - Frozen spec file matches REQ-089 field set.
  - CI job regenerates snapshot and fails on drift vs catalog goldens for that cell.
  - Process doc forbids hand-edit as second SoT.
  - MS-005 recorded before claiming hybrid “done.”
- **Blocks:** public hybrid claim; MS-006 hybrid portion.

### MS-006 — v1 delivery readiness

- **Phase:** PHASE-06
- **Outcome:** Implementation is ready for owner v1 use under revised-spec §29.2.
- **Prerequisites:** MS-004, MS-005; residual risk review per §16.
- **Acceptance evidence:**
  - Must REQ traceability complete (satisfied or residual-accepted **only where
    residual policy allows**).
  - Regression suite green on Linux.
  - Release notes list limitations (RSK-002/107/108, OQ-105 as applicable).
  - No open Critical defects against implementation authority.
- **Blocks:** Formal “v1 shipped” declaration (owner).

---

## 10. Cross-Phase Integration

| Integration seam | Phases | Strategy |
| ---------------- | ------ | -------- |
| Plan → Generate bind | 01→03 | Shape in 01; e2e in 03; teach in 04–05 |
| Construct → Stage paths | 01→02→03 | Plan file list drives render; confinement tests span 02–04 |
| Verify fields → Runners | 01→03 | Record early; execute later; single precedence implementation |
| ty runner → ty config freeze | 03→04 | MS-002 provisional; SPK-002 freezes before MS-003a |
| Minimal cell → Full-Core cli | 03→04 | MS-002 lifecycle; MS-003a Core content |
| Full-Core cli → Full catalog | 04 | MS-003a → MS-DF0 → MS-003b; continuous CI of earlier goldens |
| Catalog content → Dogfood smoke | 04 | MS-DF0 before multi-archetype freeze |
| Catalog SoT → Template snapshot | 04→05 | Generate-only snapshot; CI drift gate; **after MS-005** |
| Generated Core → Foundry dogfood | 04→05 | MS-DF0 smoke then MS-005 full; keep research skills out of emit |
| Error taxonomy | 01–03 | Extend coverage as new failure classes become reachable |
| Kind-qualified IDs | 01→04 | Plan/catalog in 01; full UX + docs in 04 |

**Continuous integration rule:** Each phase adds automated tests that remain green
in later phases (no deleting goldens to “move fast”). Progressive PHASE-04
goldens integrate as they land.

**Thin E2E rule:** PHASE-03 must produce a usable generate path before PHASE-04
breadth; avoid multi-phase infrastructure with no user-visible generate.

**Freeze durability rule (FND-200):** PHASE-04 exit is content-complete, not
public hybrid freeze. Public hybrid = MS-004 after MS-005. Dogfood falsification
re-gates MS-003a/MS-003b.

---

## 11. Data or Migration Sequencing

| Topic | Plan |
| ----- | ---- |
| User data migration | **N/A** — greenfield generator; no existing-project update (REQ-033) |
| Schema evolution | Project Spec `schema = 1` only in v1; bump requires explicit support |
| Catalog evolution | Closed admission (REQ-044); digest changes invalidate unbound assumptions; bind path detects digest mismatch |
| Failed stages | Not migrated; operator deletes; unique names prevent clobber |
| Template snapshots | Full regenerate/replace, not merge; only after dogfood-informed freeze |
| Secrets | Never migrate plaintext; fnox ciphertext only if present |
| Freeze re-gate | Catalog/golden changes after re-gate are deliberate rework, not silent migration |

---

## 12. Testing Strategy by Phase

| Phase | Unit | Golden | Conformance | e2e | Spikes |
| ----- | ---- | ------ | ----------- | --- | ------ |
| PHASE-01 | spec/resolve/plan pure | plan JSON cli | kind-qualified catalog | write-free CLI | SPK-100 |
| PHASE-02 | fsx helpers | — | path confinement | stage/place/fail | SPK-101 |
| PHASE-03 | verify orchestration | minimal generate tree | — | generate default/strict/none + bind + real ty | SPK-103 |
| PHASE-04 | render edge cases | progressive: cli Core then all archetypes | inventories + forbidden | generate cli then ×3 archetypes; product CI smoke | SPK-002/050/052/102 |
| PHASE-05 | — | frozen cell snapshot | template=catalog | dogfood CI; then CI drift job | — |
| PHASE-06 | regression | full golden suite | full forbidden | full matrix | residual only |

**Foundry product tests** follow revised-spec §16.1. **Generated Project tests**
are emitted content (§16.2) validated via conformance and strict verify.

---

## 13. Security Activities by Phase

| Phase | Activities |
| ----- | ---------- |
| PHASE-01 | Reject secrets in Project Spec; deterministic plans; no network by default for plan |
| PHASE-02 | Path confinement; fail-closed destination; stage path disclosure without leaking secrets |
| PHASE-03 | Network disclosure for lock/sync; no place on verify fail; avoid embedding secrets in errors |
| PHASE-04 | fnox+age templates + skills; forbidden dotenv/Claude/MCP kitchen-sink; SPK-052; hard forbidden-path gate |
| PHASE-05 | Release/template snapshot secret hygiene; dogfood without committing age private keys |
| PHASE-06 | Final forbidden-path audit; residual RSK-050/051/104 review |

---

## 14. Operations and Release Readiness

| Concern | When | Policy |
| ------- | ---- | ------ |
| Linux CI | PHASE-01 onward | Required: uv locked sync, ruff, ty, pytest as product hardens |
| Foundry product CI smoke | PHASE-04 / MS-DF0 | Locked sync + ruff + ty + pytest on foundry |
| macOS CI | optional | OQ-005; not an exit gate |
| Catalog validation in CI | PHASE-01/04 | Validate catalog + golden plans |
| Template drift CI | PHASE-05 after MS-005 | Generate+diff frozen cell |
| Versioning | PHASE-05 | `foundry version` ↔ release tag; catalog digest reported |
| Publish | PHASE-05/06 | uv-native package publish path documented; PyPI optional per owner |
| Offline ops | PHASE-03+ | Document `--verify none` + cached uv limitations |
| Stage cleanup | PHASE-02+ | Docs for leftover stages (RSK-101) |
| Incident/rollback | all | Destination never half-written; rerun generate on empty dest |
| Freeze re-gate | PHASE-04/05 | Dogfood falsify → re-gate MS-003a/b; block MS-004 |

Release readiness for owner v1 = MS-006 + PHASE-06 exit, not merely MS-002.

---

## 15. Dogfooding

| Stage | Dogfood activity |
| ----- | ---------------- |
| PHASE-01–02 | Optional manual CLI only |
| PHASE-03 | Owner runs one real minimal generate |
| PHASE-04 | **MS-DF0:** foundry product Core tooling smoke (hard gate before MS-003b); use generated fixtures as samples; agent skill trials (SPK-050) |
| PHASE-05 | **MS-005:** full foundry product dogfood (before MS-004 hybrid claim) |
| PHASE-06 | Generate at least one real personal project from release candidate |

**Rules:**

1. Dogfood **smoke** before multi-archetype freeze (MS-DF0 → MS-003b).
2. Full dogfood before public hybrid claim (MS-005 → MS-004).
3. Do not add new archetypes/profiles during dogfood to “make dogfood work”
   without REQ-044 admission and spec authority.
4. Do not demote ty/fnox or introduce dotenv to “make dogfood work.”

**Hybrid dogfood:** Template path and CLI path must produce the same frozen cell
bytes (modulo documented non-goals), after dogfood-informed Core stability.

---

## 16. Residual Policy Table (FND-205)

Phase exits and MS-006 residual-accept **must** follow this matrix. Residual
acceptance requires written limitation text naming which REQs remain fully green.

| Spike / risk | Hard gate for | Residual-allowed without DEC? | Requires DEC if failing |
| ------------ | ------------- | ----------------------------- | ----------------------- |
| **SPK-002** | ty config freeze / MS-003a Core ty defaults | Limitations on **config keys / pin notes** only; default verify still includes ty | Demoting ty from Core / default verify |
| **SPK-052** | secrets skill freeze | Delay freeze (hold MS-003a secrets claim) | dotenv fallback; demote fnox |
| **SPK-102** | MS-003b / forbidden paths / PHASE-04 exit | **No** | Emitting forbidden paths; shipping dotenv secrets or Claude adapters |
| **SPK-050** | multi-agent completeness claims at MS-003b | Narrow documented agent list + docs; cannot claim full multi-agent DoD | Claiming full multi-agent DoD while agents red |
| **SPK-103** | PHASE-03 exit cost disclosure | Document offline `none` limitations | Dropping ty from default for cost |
| **SPK-100/101** | PHASE-01/02 exit | **No** (hard technical gates) | Changing exclusive-place or purity locks |
| **MS-DF0** | MS-003b freeze claim | **No** for skipping smoke; DEC only if foundry cannot share Core tooling gates without inventing second Core | Inventing second Core; dropping product ty/ruff gates silently |
| **Forbidden-path suite** | MS-003a cell; MS-003b full | **No** | Emitting forbidden content |
| **RSK-108** agents skip `--plan` | Docs/skills teach bind | Strengthen docs; not architecture residual | Making bind mandatory via silent product-law change without DEC |

**MS-006 rule:** residual-accept only for rows marked residual-allowed; Must red
otherwise returns to owning phase / re-gates owning milestone.

---

## 17. Risk Register

Delivery-focused register (product risks from revised-spec §24 carried forward
with sequencing). Severity is residual **during delivery**.

| ID | Risk | Sev | Sequencing / mitigation | Phase gate |
| -- | ---- | --- | ----------------------- | ---------- |
| RSK-002 | ty maturity as Core | Med–High | Dual-gate: MS-002 provisional runner green; SPK-002 freeze before MS-003a; pin ty; CI fail-closed; no silent demotion | PHASE-03 provisional; PHASE-04 freeze |
| RSK-007 | fnox Core + no dotenv fallback | Med | Templates + skills; SPK-052 | PHASE-04 / MS-003a |
| RSK-050 | Agents reintroduce dotenv secrets | High | Forbidden paths + secrets skill + reviews | PHASE-04–06 |
| RSK-107 | Generate-time uv lock network/cost | Med | SPK-103; disclose; document offline `none` | PHASE-03 |
| RSK-108 | Agents skip `--plan` bind | Med | AGENTS.md + skills teach bind; docs in PHASE-05 | PHASE-04–05 |
| RSK-100 | Plan/generate non-determinism | High if present | Canonical JSON; goldens; ban time/random | PHASE-01–03 |
| RSK-101 | Leftover stage confuses agents | Med | `stage_path` mandatory; docs | PHASE-02 |
| RSK-102 | Verify needs network | Med | Disclose; `none` mode | PHASE-03 |
| RSK-103 | Template snapshot drift | Med | CI regenerate+diff after dogfood-informed freeze | PHASE-05 |
| RSK-104 | Catalog reintroduces dotenv/Claude | High | Forbidden-path tests SPK-102 (hard) | PHASE-04 |
| RSK-001 | uv pre-1.0 churn | Med | Pin uv; lockfiles | PHASE-03–06 |
| RSK-051 | Claude adapters reintroduced | Med | Forbidden paths | PHASE-04 |
| RSK-053 | MCP kitchen-sink creep | Med | REQ-072 emit none | PHASE-04 |
| RSK-054 | Agents use Pyright, ignore ty | Med | DoD + CI ty | PHASE-04–05 |
| RSK-055 | Skill catalog sprawl | Med | Closed set; admission | PHASE-04–06 |
| RSK-105 | Over-copy go-foundry FD complexity | Med | Stage-root first; stop condition | PHASE-02 |
| RSK-109 | data-etl dual-id confusion | Low | Kind-qualified UX | PHASE-01–04 |
| RSK-005 | macOS CI cost | Low | Optional macOS | PHASE-05 |
| RSK-200 | False freeze before dogfood | Med | MS-DF0 before MS-003b; MS-005 before MS-004; re-gate freeze | PHASE-04–05 |
| OQ-105 | CLI name provisional | Branding | Owner DEC anytime; non-blocking | PHASE-05–06 |

---

## 18. Open Questions

Delivery / sequencing questions only. Product OQs resolved in the revised spec
are **not** reopened here.

| ID | Topic | Blocking? | Notes |
| -- | ----- | --------- | ----- |
| OQ-105 | Final CLI binary name | No | Provisional `foundry`; rename is branding |
| OQ-002 | SPK-002 exact calendar timing | No | Must complete before MS-003a ty freeze |
| OQ-054 | Foundry product closed skill set beyond research | Partial | Product implementation concern; not Generated Core |
| OQ-PLAN-01 | Product code in this repo vs separate implementation repo | No | Phase evidence is behavioral; owner chooses layout |
| OQ-PLAN-02 | PyPI publish vs uv private/index only for v1 | No | Decide by PHASE-05 release notes |
| OQ-106 | Rename profile `data-etl` | No | Deferred; kind-qualified UX first |

If a sequencing conflict appears to require REQ change → escalate as DEC; do not
edit REQs from this plan.

---

## 19. Rollback and Reconsideration Triggers

| Trigger | Action |
| ------- | ------ |
| Stable `plan_sha256` impossible across CI | Halt before PHASE-02; fix canonicalization |
| Exclusive place corrupts dest on failure | Halt before PHASE-03; fix fsx |
| Default verify cost impossible after SPK-103 | Owner options within REQ-080; no silent ty drop |
| SPK-002 ty failure | Residual RSK-002 process per §16; **no** demotion without DEC |
| SPK-052 fnox failure | Block secrets freeze; **no** dotenv fallback |
| Forbidden-path failures | Block MS-003a/MS-003b / release; **no** residual-accept |
| MS-DF0 smoke fails | Block MS-003b freeze claim |
| Dogfood (MS-005) falsifies Core | **Re-gate MS-003a and/or MS-003b**; block or invalidate MS-004 until freeze evidence green again |
| Template drift non-determinism | Return to plan determinism + lock honesty |
| Demand for Windows / marketplace / update-merge | Refuse; Blueprint/DEC only |
| Demand to demote ty or fnox | Refuse without DEC |
| Agents ignore `--plan` in dogfood | Strengthen docs/skills; consider UX warnings; not architecture rewrite |
| Must REQ red at PHASE-06 without policy-allowed residual | Not v1; return to owning phase / re-gate milestone |

**Reversibility preference:** Prefer catalog content and docs changes over
lifecycle redesign once PHASE-03 has exited.

**No post-exit fiction:** There is no “still PHASE-04 after PHASE-04 exit.”
Invalidated freeze claims are **re-gated milestones**, not a hidden holding phase.

---

## 20. Requirement-to-Phase Traceability

Must-priority and normative REQs mapped to **primary** delivery phases.
Cross-cutting REQs list all phases that provide evidence. Cite only; do not
renumber REQs.

| REQ | Priority (spec) | Phase(s) | Milestone / evidence notes |
| --- | --------------- | -------- | -------------------------- |
| REQ-001 | Must | PHASE-01..05 | Hybrid complete at MS-004 **after** MS-005 |
| REQ-002 | Must | All | macOS/Linux only; enforced by CI targets |
| REQ-003 | Must | All | Non-goals tests / review gates |
| REQ-010 | Must | PHASE-01..03 | Commands online by MS-002 |
| REQ-011 | Must | PHASE-01 | Write-free validate/plan |
| REQ-012 | Must | PHASE-02..03 | Sole dest mutator |
| REQ-013 | Must | PHASE-01 | Non-interactive first |
| REQ-020 | Must | PHASE-01 | Schema 1 parse |
| REQ-021 | Must | PHASE-01 | Unknown keys/profiles fail |
| REQ-022 | Must | PHASE-01 | No secrets in spec |
| REQ-023 | Must | PHASE-01 | Path + stdin |
| REQ-024 | Must | PHASE-01..03 | Plan-as-contract + bind |
| REQ-025 | Must | PHASE-01 | Plan encoding |
| REQ-026 | Must | PHASE-01 | plan_sha256 |
| REQ-030 | Must | PHASE-02 | Non-empty dest fail |
| REQ-031 | Must | PHASE-02 | Stage + exclusive place |
| REQ-032 | Must | PHASE-02 | Path confinement |
| REQ-033 | Must | All | No update/merge |
| REQ-040 | Must | PHASE-01..04 | Closed catalog; content-complete at MS-003b |
| REQ-041 | Must | PHASE-01 | Catalog digest in plan |
| REQ-042 | Must | PHASE-01 | Exactly one archetype |
| REQ-043 | Must | PHASE-01 | Profile composition |
| REQ-044 | Must | PHASE-04+ | Admission discipline |
| REQ-050 | Must | PHASE-04 | Core toolchain invariants (MS-003a) |
| REQ-051 | Must | PHASE-04 | Python version policy |
| REQ-052 | Must | PHASE-03..04 | uv + lock commit behavior |
| REQ-053 | Must | PHASE-04 | Layout by archetype (MS-003a/b) |
| REQ-054 | Must | PHASE-04 | Ruff |
| REQ-055 | Must | PHASE-03..04 | ty Required (runner MS-002; freeze SPK-002/MS-003a) |
| REQ-056 | Must | PHASE-04 | pytest Required emit |
| REQ-057 | Must | PHASE-04 | Hooks Default pre-commit |
| REQ-058 | Must | PHASE-04 | fnox+age; no dotenv secrets (SPK-052) |
| REQ-059 | Must | PHASE-04 | HTTP profile (MS-003b) |
| REQ-060 | Must | PHASE-04 | Typer Default CLI (MS-003a) |
| REQ-061 | Must | PHASE-04 | data-etl profile defaults (MS-003b) |
| REQ-062 | Must | PHASE-04 | GHA Core CI |
| REQ-063 | Must | PHASE-04 | Command surface docs |
| REQ-070 | Must | PHASE-04 | AGENTS.md only |
| REQ-071 | Must | PHASE-04 | Skills under `.agents/skills` |
| REQ-072 | Must | PHASE-04 | MCP default none |
| REQ-073 | Must | PHASE-04 | Agent secrets protocol |
| REQ-074 | Must | PHASE-04 | Definition of done |
| REQ-075 | Must | PHASE-04 | Fresh-session packaging |
| REQ-076 | Must | PHASE-04..05 | Foundry vs Generated surfaces (MS-DF0, MS-005) |
| REQ-077 | Should | PHASE-05 | Editor documentation |
| REQ-078 | Must | PHASE-04 | AI-native anti-patterns |
| REQ-080 | Must | PHASE-03 | Default verify mode |
| REQ-081 | Must | PHASE-05 | Template snapshot SoT (MS-004 after MS-005) |
| REQ-082 | Should | PHASE-01..03 | Module layout / purity |
| REQ-083 | Must | All | go-foundry transfer discipline |
| REQ-084 | Must | PHASE-01,03 | Effective verify resolution |
| REQ-085 | Must | PHASE-03,04 | Generate-time uv.lock |
| REQ-086 | Must | PHASE-01..03 | Optional `--plan` bind |
| REQ-087 | Must | PHASE-01,04 | Kind-qualified catalog identity |
| REQ-088 | Must | PHASE-04 | scripts archetype contract (MS-003b) |
| REQ-089 | Must | PHASE-05 | Frozen public template cell (MS-004) |
| REQ-090 | Must | PHASE-02 | Stage identity + failure path |
| REQ-091 | Must | PHASE-01..03 | JSON error_class taxonomy |

---

## 21. Final Implementation Handoff

Per `program/operator/completion-criteria.md`:

| Handoff field | Value |
| ------------- | ----- |
| **Authoritative specification** | `docs/specifications/02-definitive-specification-revised.md` v0.2 (`faffbdc`) — **product law** |
| **Authoritative plan** | This document `docs/plans/02-implementation-plan-revised.md` v0.2 — **delivery sequence authority** after human stage acceptance |
| **Whether implementation may begin** | **Yes**, after human accepts stage `plan-revision` and records `accepted_commit`, under revised-spec product law + this plan. Owner residual risk remains if starting PHASE-01 before that formal accept. |
| **First safe implementation phase** | **PHASE-01** (pure pipeline). PHASE-01/02 may proceed under owner risk with this plan as guidance even before formal stage accept. |
| **Required pre-implementation spikes** | None blocking PHASE-01 start. SPK-100 is the PHASE-01 exit spike. Later: SPK-101 (PHASE-02), SPK-103 (PHASE-03), SPK-002/052 (before MS-003a), SPK-050/102 (before MS-003b), MS-DF0 before MS-003b. |
| **Phase dependencies** | Linear PHASE-01→06; progressive MS-003a → MS-DF0 → MS-003b; MS-005 → MS-004. See §6. |
| **Earliest usable vertical slice** | **MS-002** (PHASE-03): first successful `generate` to empty dest with default verify (thin E2E). |
| **Earliest dogfooding milestone** | **MS-DF0** (PHASE-04 smoke); full dogfood **MS-005** (PHASE-05). |
| **Validation / evidence at boundaries** | Phase exit criteria and milestone acceptance evidence in §8–§9; residual policy §16; Linux CI required. |
| **Risks that must remain visible** | RSK-002 (ty), RSK-007/050 (fnox/dotenv), RSK-107 (lock network), RSK-108 (`--plan` skip), RSK-104 (forbidden paths), RSK-200 (false freeze) — §17. |
| **Decisions that must remain reversible** | Catalog content and docs preferred over lifecycle redesign after PHASE-03; freeze claims re-gatable; CLI name provisional (OQ-105); no silent lock demotion. |
| **Remaining blockers** | **None plan-blocking.** Program stage still needs human accept + commit for formal delivery-authority unlock in the manifest. Product residual risks (ty ecosystem, etc.) are sequenced, not blockers to starting PHASE-01. |
| **Required read set for implementation agents** | This plan; revised-spec v0.2; Blueprint; Charter; AGENTS.md. |
| **Supporting evidence only (not authority)** | Focused reports `docs/reports/01`–`03`; proposed plan `01-implementation-plan.md`; plan-review; research-program.toml (index only); chat history (never authority). |

### Stop line

Do **not** begin substantive product implementation while this revised plan remains
stage-unaccepted if the owner requires formal delivery authority. Do **not**
decompose this plan into hundreds of coding-agent task packets inside the
research program.

---

## 22. Definition of Plan Completion

This **revised implementation plan artifact** is complete when:

1. All sections required by `program/contracts/implementation-plan.md` and the
   revision prompt are present and non-placeholder.
2. Every FND-200..205 is dispositioned with exactly one allowed disposition.
3. Accepted corrections are integrated in the body (phases, milestones, dogfood,
   residual policy, rollback).
4. Artifact status is honest: **`Accepted — delivery authority`** (High findings
   resolved; no implementation-blocking plan finding remains).
5. Phases PHASE-01..06 and milestones MS-001, MS-002, MS-003a, MS-DF0, MS-003b,
   MS-004, MS-005, MS-006 have executable entry/exit or acceptance evidence.
6. Must REQs are traced; residual risks sequenced; residual policy present.
7. No coding backlog is included.
8. Independent `research-validate` passes mechanical checks.
9. Human accepts the stage and records `accepted_commit` in
   `research-program.toml` (human-owned; not claimed by this writing session).

This plan is **not** product v1 completion. Product v1 completion is MS-006 /
PHASE-06 against revised-spec §29.2.

---

## 23. Completion Checklist

- [x] All required plan sections present and non-placeholder
- [x] Actual revision date recorded (2026-08-01)
- [x] Every FND-200..205 dispositioned (exactly one allowed disposition each)
- [x] No silent finding loss
- [x] Accepted corrections integrated in body (not ledger-only)
- [x] Contradictory proposed-plan language removed or reconciled
- [x] Subordinate to revised-spec v0.2 (no REQ/architecture contradictions)
- [x] Phases/milestones only — **no** coding backlog or task packets
- [x] Executable entry/exit criteria (observable evidence)
- [x] Early thin end-to-end path preserved (PHASE-03 / MS-002)
- [x] Spikes scheduled as gates
- [x] Dogfooding and hybrid sequencing corrected (MS-DF0 before MS-003b; MS-005 before MS-004)
- [x] Residual risk / residual-accept policy honest and executable (§16)
- [x] Security, testing, ops addressed by phase
- [x] Rollback/reconsideration triggers present (no post-exit fiction)
- [x] Must REQ traceability present
- [x] Final Implementation Handoff complete per completion-criteria
- [x] Blueprint non-goals preserved
- [x] Product locks preserved
- [x] Strengths preserved
- [x] Honest artifact status: **Accepted — delivery authority**
- [x] Standalone: implementable without chat history
- [x] Allowed file scope only (revised plan path; validation report separate)
- [x] No product implementation started as main work
- [x] Proposed plan (`01-…`) and review not modified
- [x] Independent validation passed (`docs/validations/02-implementation-plan-revised-validation.md`)
- [x] Human approval obtained (2026-08-01)
- [x] `accepted_commit` recorded in manifest (see `research-program.toml` stage `plan-revision`)

---

*End of final revised implementation plan v0.2 — delivery sequence authority
pending human stage acceptance. Product law remains revised specification v0.2.
Provenance: proposed plan v0.1; plan-review FND-200..205 disposed.*
