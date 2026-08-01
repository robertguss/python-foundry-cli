# Program Blueprint — python-foundry

- **Artifact type:** Program Blueprint
- **Program:** python-foundry
- **Status:** Accepted
- **Version:** 0.1
- **Created:** 2026-07-30
- **Last updated:** 2026-07-31
- **Rigor tier:** standard (approved in discovery framing)

> Discovery framing approved (2026-07-31). Blueprint accepted by human via Git
> commit recorded in `research-program.toml`. This document does **not** conduct
> substantive research; it governs the program.

## 1. Artifact Metadata

| Field      | Value                                              |
| ---------- | -------------------------------------------------- |
| Program ID | python-foundry                                     |
| Owner      | robertguss                                         |
| Repository | https://github.com/robertguss/python-foundry       |
| Role       | Research program repository (methodology + design) |

**Related prior art (transferable reference, not authority here):**

- [go-foundry-research](https://github.com/robertguss/go-foundry-research) — research process this program was abstracted from
- [go-foundry-cli](https://github.com/robertguss/go-foundry-cli) — Go Foundry product patterns to adapt

## 2. Product or Project Vision

**python-foundry** is a personal, open-sourceable, **AI-native hybrid foundry**
for modern Python projects:

1. A **Python/`uv` CLI generator** that turns a declarative project input into a
   complete repository via **validate → plan (dry-run) → generate** (adapted
   from go-foundry, re-researched for Python).
2. A **strong default Core** (toolchain, layout, quality gates, hooks/secrets,
   CI, agent surface) so new work starts fast and consistently.
3. Optional **capability profiles** / archetypes (CLI, scripts, data/ETL) rather
   than a framework zoo.
4. A surface usable as a **GitHub template** for the default path.
5. Generated projects and the foundry itself are **agent-first**: organized,
   documented, and instrumented (skills, curated MCP/LSP, project instructions)
   so AI coding agents can understand and extend them without oral tradition.

This repository is the **research and specification program** for that product.
It stops at a revised definitive specification and a phase/milestone
implementation plan — not a granular coding backlog.

## 3. Problem Statement

The owner repeatedly starts Python projects and re-establishes the same packages,
layout, quality tooling, hooks, secrets handling, CI, and agent-operable
structure. That costs time, produces inconsistent bases, and forces re-explaining
repo conventions to AI coding agents (the primary implementers). Existing one-shot
scaffolds (`uv init`, generic templates) do not encode a closed, research-backed
Core plus a dry-run generation workflow and AI-native agent surface comparable to
the Go Foundry direction.

## 4. Intended Users and Stakeholders

| Role                         | Relationship                                      |
| ---------------------------- | ------------------------------------------------- |
| **Primary operator**         | Owner (robertguss) — directs work, accepts gates  |
| **Primary implementers**     | AI coding agents (Grok, Claude Code, and similar) |
| **Secondary**                | Open-source readers/adopters (not v1 design focus)|
| **Out of scope (v1)**        | Multi-tenant orgs, template marketplaces, unknown teams as primary customers |

## 5. Goals

1. Design a **hybrid foundry**: generator CLI + strong default Core (+ template surface).
2. Establish **evidence-backed** modern Python (2026) practices for Core tooling and layout.
3. Support **CLI** and **scripts** as primary archetypes; **data/ETL** (e.g. DuckDB, pandas) without notebooks.
4. Make **AI-native operability** first-class: agent skills, curated MCP/LSP/agent config, clear docs/structure for both foundry and generated projects.
5. Adapt useful **go-foundry** patterns (spec → plan → generate, Core vs profiles, closed catalogs) without blind copy.
6. Produce an **accepted revised definitive specification** and **revised implementation plan** (phases/milestones) sufficient to build the product later.
7. Keep the owner’s personal defaults honest: **uv**, Astral stack candidates (**ruff**, **ty**), **pytest**, **hk**, **fnox**, **httpx** when networking — subject to research confirmation.

## 6. Non-Goals

1. Multi-user / org template marketplace.
2. Framework zoo (every web/ML stack).
3. Notebooks, GUI apps, mobile.
4. Windows support (ever, for this program’s product targets).
5. Designing primarily for anonymous public consumers over **owner + agents**.
6. Unlimited MCP/skill catalog — **closed, curated** agent tooling only for v1.
7. Replacing packaging ecosystems or inventing a new package manager (**uv** assumed).
8. Granular coding backlog / agent task packets as program outputs.
9. Implementing the product inside this research program beyond optional evidence spikes.

## 7. Locked Constraints

| ID | Constraint |
| -- | ---------- |
| L1 | Product shape: **hybrid** (generator + strong default + GitHub template surface). |
| L2 | Foundry implementation language: **Python** managed with **uv** (dogfood). |
| L3 | Host OS targets: **macOS and Linux only**; never Windows. |
| L4 | Prefer **latest practical Python** versions; exact floor/default pinned in research/spec. |
| L5 | Core toolchain **candidates** (confirm or revise with evidence): `uv`, `ruff`, `ty`, `pytest`, `hk`, `fnox`; `httpx` when networking. |
| L6 | Archetypes: **CLI** + **scripts**; **data/ETL** in scope; **no notebooks**. |
| L7 | CI: **GitHub Actions** in Core. |
| L8 | Packaging: **uv project + console scripts** for v1 (not containers/native binaries as Core). |
| L9 | **AI-native first**: portable agent skills; curated MCP/LSP/agent config; agent-operable layout and docs. |
| L10 | Prior art: go-foundry research/CLI as **strong transferable reference** — adapt, do not copy blindly. |
| L11 | Primary user model: personal tool; agents implement; open-source OK. |
| L12 | Rigor tier: **standard**. |
| L13 | Time posture: research quality over artificial calendar pressure. |
| L14 | This repo is the **research program**; product implementation is downstream of accepted revised spec + plan. |

## 8. Success Criteria

1. **Fast path:** From empty directory, a short validate/plan → generate (or template) flow yields a runnable project with Core tooling wired.
2. **Agent operability:** An AI coding agent can understand layout, conventions, and how to add a CLI command, script, or ETL entry without long oral tradition.
3. **Consistency:** Generated projects share Core conventions across CLI, script, and data/ETL shapes.
4. **Decision reduction:** Owner stops hand-rebuilding the same configs for ordinary new projects.
5. **Program completion:** Accepted revised definitive specification + revised phase/milestone plan that an implementation repo can follow.

**Failure modes:** Scaffold that still needs tribal knowledge; foundry so flexible it reintroduces setup decision fatigue; agent surface as uncurated kitchen sink; Windows or framework-zoo scope creep.

## 9. Rigor Tier

- **Selected:** standard
- **Rationale:** Personal and reversible (not high-assurance), but non-trivial: hybrid generator, 2026 ecosystem survey, AI-native skills/MCP/LSP, multiple archetypes, transfer from go-foundry. Needs full evidence ledgers, bounded spikes, synthesis, and adversarial reviews — more than focused.
- **Approval:** Approved in discovery framing (2026-07-31); confirmed in this Blueprint upon human acceptance.

## 10. Research Graph

| Stage ID | Name | Kind | Depends on | Output | Parallel group |
| -------- | ---- | ---- | ---------- | ------ | -------------- |
| discovery | Project Discovery | discovery | — | `docs/00-program-blueprint.md` | — |
| charter | Research Charter | research-charter | discovery | `docs/01-research-charter.md` | — |
| research-python-ecosystem | Modern Python Ecosystem & Project Standards | foundational (focused research) | charter | `docs/reports/01-modern-python-ecosystem.md` | G1 |
| research-ai-native | AI-Native Repository & Agent Workflow | independent (focused research) | charter | `docs/reports/02-ai-native-agent-workflow.md` | G1 |
| research-foundry-architecture | Foundry Architecture | dependent (focused research) | charter, research-python-ecosystem, research-ai-native | `docs/reports/03-foundry-architecture.md` | — |
| synthesis | Definitive Specification Synthesis | chief-architect-synthesis | research-foundry-architecture | `docs/specifications/01-definitive-specification.md` | — |
| spec-review | Specification Adversarial Review | adversarial-review | synthesis | `docs/reviews/01-specification-adversarial-review.md` | — |
| spec-revision | Revised Definitive Specification | artifact-revision | spec-review | `docs/specifications/02-definitive-specification-revised.md` | — |
| implementation-plan | Implementation Plan | implementation-plan | spec-revision | `docs/plans/01-implementation-plan.md` | — |
| plan-review | Implementation Plan Adversarial Review | adversarial-review | implementation-plan | `docs/reviews/02-implementation-plan-adversarial-review.md` | — |
| plan-revision | Final Revised Implementation Plan | artifact-revision | plan-review | `docs/plans/02-implementation-plan-revised.md` | — |

Prompts for focused and spine stages are created **just in time** from
`program/templates/` (not pre-authored here beyond graph identity).

### Track justification

| Track | Why it exists | Why another cannot absorb it | Decisions it informs | Consumed by |
| ----- | ------------- | ---------------------------- | -------------------- | ----------- |
| research-python-ecosystem | Core tools, layouts, testing, CI, data/ETL libraries must be evidence-backed for 2026 | Architecture assumes a Core set; AI-native assumes a project shape but does not pick ruff vs alternatives | Core vs profile package set; Python floor; layout; pytest/CI conventions | Architecture report; synthesis |
| research-ai-native | Skills, MCP, LSP, agent docs are first-class product requirements | Ecosystem track picks libraries, not agent workflow; architecture wires both | Closed agent toolchain; `AGENTS.md` / skills layout; MCP/LSP defaults | Architecture report; synthesis |
| research-foundry-architecture | Spec → plan → generate, catalog, Core/profiles, CLI shape | Needs ecosystem + AI-native outputs as inputs | Generation model; spec format; parity with go-foundry; module boundaries | Synthesis |

### Omitted tracks (why)

| Omitted | Why unnecessary for this program |
| ------- | -------------------------------- |
| Domain and problem | Personal tooling domain is simple; problem locked in discovery |
| User and workflow | Single primary user; agent-operator model already locked |
| Security and threat model (full) | Personal tool; secrets via fnox — fold light notes into ecosystem/architecture; not a full threat program |
| Data and integration (full) | ETL is an archetype, not multi-enterprise integration fabric |
| Operations / SRE scale | No multi-tenant runtime service as the product |
| Performance and scalability | Not architecture-defining for a project generator |
| Migration and compatibility | Greenfield personal foundry; no legacy user base |
| Legal / compliance (full) | Open-source licensing note in charter/spec later; not regulated product |
| Financial / market | Not a commercial viability study |
| Scientific validation | Engineering convention + bounded spikes suffice |

## 11. Stage Descriptions and Dependencies

### discovery — Project Discovery

- **Primary question:** What problem, outcome, scope, rigor, and graph should govern the program?
- **Output:** this Blueprint
- **Completion:** Framing approved; Blueprint filled; human accepts Blueprint; commit recorded

### charter — Research Charter

- **Primary question:** How will research be conducted (methods, evidence, vocabulary, quality bar)?
- **Prerequisites:** Accepted Blueprint
- **Output:** `docs/01-research-charter.md`
- **Completion:** Charter filled per contract; validated; human accepts; commit recorded

### research-python-ecosystem — Modern Python Ecosystem & Project Standards

- **Kind:** foundational focused research
- **Primary question:** What tooling, libraries, layouts, testing, and CI practices should define Core (and profiles) for CLI, scripts, and data/ETL Python projects in 2026 on macOS/Linux with uv?
- **Scope:** Package/project management; lint/type/test; hooks/secrets; HTTP client norms; data/ETL stack options; GitHub Actions patterns; layout conventions
- **Non-goals:** Designing the generator engine; full agent skill catalog; web framework zoo
- **Inputs:** Accepted Blueprint, Charter; go-foundry as reference only where relevant
- **Output:** `docs/reports/01-modern-python-ecosystem.md`
- **Identifiers:** REC-001..REC-099; RSK/OQ as needed; SPK if load-bearing claims need spikes
- **Spikes:** Expected when version pins or tool choices are contested and testable
- **Replication:** Permitted, not required by default
- **Downstream:** research-foundry-architecture, synthesis

### research-ai-native — AI-Native Repository & Agent Workflow

- **Kind:** independent focused research (parallel with ecosystem after charter)
- **Primary question:** How should the foundry and generated projects be structured, documented, and instrumented so AI coding agents work optimally (skills, MCP, LSP, instructions, checks)?
- **Scope:** Agent instruction files; portable skills; curated MCP/LSP sets; repo boundaries; verification hooks agents can run
- **Non-goals:** Building every MCP server; multi-agent orchestration product; model training
- **Inputs:** Accepted Blueprint, Charter
- **Output:** `docs/reports/02-ai-native-agent-workflow.md`
- **Identifiers:** REC-100..REC-199
- **Spikes:** Optional (e.g. agent task success on sample layout)
- **Replication:** Permitted, not required
- **Downstream:** research-foundry-architecture, synthesis

### research-foundry-architecture — Foundry Architecture

- **Kind:** dependent focused research
- **Primary question:** What architecture implements hybrid generation (spec → plan → generate), Core/profiles/catalog, and AI-native surfaces for a Python/uv foundry CLI, adapting go-foundry where appropriate?
- **Scope:** CLI commands; project spec format; generation plan; filesystem/write semantics; catalog; archetype/profile model; module layout; evidence gates
- **Non-goals:** Full implementation; unbounded profiles
- **Inputs:** Accepted ecosystem + AI-native reports; go-foundry research/spec as transferable reference
- **Output:** `docs/reports/03-foundry-architecture.md`
- **Identifiers:** REC-200..REC-299
- **Spikes:** Expected for load-bearing generation/plan semantics if uncertain
- **Replication:** Risk-triggered
- **Downstream:** synthesis

### Fixed spine (post-research)

| Stage | Completion criteria (summary) |
| ----- | ----------------------------- |
| synthesis | Single coherent definitive specification with REQ-001..REQ-299 as needed; consumes all research reports |
| spec-review | Adversarial findings FND-001..FND-199; no silent omission of load-bearing claims |
| spec-revision | Revised spec is implementation authority candidate; dispositions findings |
| implementation-plan | Phases/milestones only; subordinate to revised spec |
| plan-review | Findings FND-200..FND-399 |
| plan-revision | Final delivery authority plan; human acceptance + commit |

## 12. Parallelism

- **Default:** sequential where dependencies exist.
- **Parallel group G1:** `research-python-ecosystem` and `research-ai-native` may run in parallel after Charter acceptance — they do not require each other’s findings.
- **Sequential:** `research-foundry-architecture` waits for both G1 reports.
- **Justification:** Ecosystem and AI-native concerns are separable; architecture must integrate both.

## 13. Optional Replication Points

- Replication **enabled** at program level; **not required by default**.
- Recommend considering replication if a G1 or architecture report makes a **contested, load-bearing** claim (e.g. “tool X must be Core”) with weak evidence.
- Any replication requires reconciliation per `program/` contracts before synthesis consumes results.

## 14. Artifact Inventory

| Path / area | Purpose |
| ----------- | ------- |
| `docs/00-program-blueprint.md` | This governing Blueprint |
| `docs/01-research-charter.md` | Research methods and quality bar |
| `docs/prompts/` | JIT stage prompts |
| `docs/reports/` | Focused research reports |
| `docs/specifications/` | Definitive and revised specifications |
| `docs/reviews/` | Adversarial reviews |
| `docs/plans/` | Implementation plans |
| `docs/evidence/` | SPK-### spikes |
| `docs/reconciliations/` | Replication reconciliation |
| `docs/validations/` | Validation reports |
| `docs/handoffs/` | Handoff notes |
| `decisions/` | DEC-### records |
| `research-program.toml` | Operational manifest (index only) |
| `program/` | Methodology library (not project conclusions) |

## 15. Identifier Allocations

| Namespace | Range | Notes |
| --------- | ----- | ----- |
| DEC | DEC-001..DEC-999 | Decision records |
| REC | REC-001..REC-099 | Ecosystem track |
| REC | REC-100..REC-199 | AI-native track |
| REC | REC-200..REC-299 | Architecture track |
| REQ | REQ-001..REQ-299 | Specification requirements |
| FND (spec) | FND-001..FND-199 | Spec adversarial review |
| FND (plan) | FND-200..FND-399 | Plan adversarial review |
| RSK | RSK-001..RSK-999 | Risks |
| OQ | OQ-001..OQ-999 | Open questions |
| SPK | SPK-001..SPK-999 | Evidence spikes |
| PHASE | PHASE-01..PHASE-99 | Plan phases |
| MS | MS-001..MS-999 | Plan milestones |

Never reuse IDs. Rejected/superseded IDs remain reserved.

## 16. Authority and Precedence

Follow `program/contracts/authority-and-precedence.md`.

**Project-specific notes:**

1. go-foundry research/CLI artifacts are **prior art**, not governing authority for this program unless explicitly adopted via DEC or accepted research recommendation.
2. Chat history is not authority.
3. After acceptance, precedence is roughly: accepted DEC → this Blueprint → Charter → current stage prompt → revised specification → research reports → reviews → plans → `research-program.toml` (index).

## 17. Human Approval Gates

See `program/operator/approval-gates.md`. Material gates for this program include: framing (done), Blueprint, Charter, each research report, synthesis, spec review/revision, plan review/revision, formal DECs.

## 18. Fresh-Session Policy

Every **substantive** stage runs in a **fresh session** with a self-contained attachment manifest. Preparing prompts, manifests, and mechanical fixes may occur in the current session (`research-stage` skill). Do not execute multiple substantive research stages in one context.

## 19. Validation and Commit Gates

- Independent validation (`research-validate`) before acceptance.
- Validators fix mechanical issues only; no invented research.
- Humans own Git; accepting commit hashes recorded in `research-program.toml`.
- Placeholders never unlock downstream work.

## 20. Amendment Protocol

See `program/reference/amendment-protocol.md`. Material scope/rigor/graph changes require explicit human approval and Blueprint amendment; do not silently edit governing artifacts outside commissioned revision.

## 21. Completion Criteria

See `program/operator/completion-criteria.md`. Program complete when revised definitive specification and revised implementation plan are accepted as implementation and delivery authority, manifest is accurate, and no required stage remains placeholder.

## 22. Implementation Handoff Expectation

- **Implementation authority:** accepted `docs/specifications/02-definitive-specification-revised.md`
- **Delivery authority:** accepted `docs/plans/02-implementation-plan-revised.md` (subordinate to revised spec)
- Handoff targets a separate product/implementation repository (or later branch program) — not ad-hoc coding from chat.
- Final plan stops at **phases and milestones**.

## Principal uncertainties (research must resolve)

1. Exact **Core vs profile** split.
2. **Spec format** and generation engine design (go-foundry parity vs Python-idiomatic).
3. **Best-of-2026** evidence vs current Astral-centric defaults.
4. Minimal closed set of **skills / MCP / LSP**.
5. Layout conventions for CLI, scripts, and ETL without framework zoo.
6. How much of go-foundry’s catalog/plan/transaction model transfers to Python/uv.

## Completion Checklist

- [x] Discovery framing approved by human
- [x] All required sections filled (not placeholder prose)
- [x] Research tracks justified; omitted tracks justified
- [x] Identifier ranges allocated
- [x] Rigor tier approved
- [x] Human accepts Blueprint
- [x] Manifest updated; accepting commit recorded
