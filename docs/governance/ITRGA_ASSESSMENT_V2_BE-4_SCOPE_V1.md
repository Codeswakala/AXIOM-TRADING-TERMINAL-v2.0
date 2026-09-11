# ITRGA ASSESSMENT — BE-4 (Market Context, Chart Intelligence, Research Read Models) · SCOPE (V1)

| Field | Value |
|---|---|
| Assessment ID | `ITRGA-ASS-V2-BE-4-SCOPE-001` |
| Date | 2026-08-31 |
| Authority | `AXIOM-V2-OD-BE-4-006` (OD-006, recorded in `OPERATOR_DECISION_V2_BE-4_START.md`) |
| Chain position | Scope assessment — stage 2 of the BE-4 governance chain (roadmap §3 delivery model) |
| Governing sources | `AXIOM-V2-BE-ROADMAP-001` Band BE-4 (PROPOSED planning document); `AXIOM V2 — PRODUCT & ARCHITECTURE SPECIFICATION` §14/§15/§16; `AXIOM-V2-GOV-CHARTER-001` (APPROVED) §5/§7; `AXIOM-V2-GOV-MAT-001` (BE-4 rows: DESIGNED); `ITRGA-DET-V2-BE-3-P2-TRANS-APPLY-FINAL-001` (programme state) |
| Status | **DECIDED — OD-007 received 2026-08-31: SD-1 = A, SD-2 = A; chain at stage 4 (DA design plan, requested per `ITRGA-REQ-V2-BE-4-001`); see §10 dated note** |

---

## 0. What this document is — and is not

1. This is ITRGA's **scope assessment** for band BE-4, issued under OD-006.
2. It is **not** a design plan (DA-authored, per roadmap §3), **not** a Build Order, **not** a plan determination, and **not** self-authorization. No BE-4 code, table, endpoint, or data change is authorized by this document or by OD-006.
3. **Source authority boundary (stated, not assumed):** `AXIOM-V2-BE-ROADMAP-001` is PROPOSED — "planning only"; "no implementation authority" is conferred by it. The APPROVED charter organizes V2 into backend bands BE-0…BE-11 "as defined in the V2 Backend and Frontend Roadmaps." The **binding** scope of BE-4 is therefore set by the chain: **OD-007 (scope decision) → DA design plan → ITRGA plan review → Build Order.** This assessment identifies what that chain must fix.
4. Nothing is guessed: every current-state fact below is cited to a record; every plan-stage unknown is labeled.

## 1. What OD-006 opens

Verbatim decision (recorded): *"Operator decision: I direct the start of BE-4 (Market Context, Chart Intelligence, Research Read Models). I authorize ITRGA to record OD-006 and open the governed chain: scope assessment, then plan. No repository changes are authorized by this decision."*

Effect of record:
- the BE-4 governance chain is open;
- ITRGA is authorized to issue this scope assessment and, on the Operator's scope decision, to proceed to the plan stage per §7;
- **no repository change** is authorized by OD-006; nothing in the chain to date has modified any file, table, or configuration;
- the sequencing directive remains in force (V2 frontend bands blocked until the V2 backend roadmap is fully cleared);
- credential law: OD-006 text scanned before archiving — **CLEAN**.

## 2. BE-4 scope per the authoritative sources

| # | Scope element | Source | Requirement (summary) |
|---|---|---|---|
| S1 | Objective | Roadmap Band BE-4 | "Evolve V1 deterministic analysis into traceable V2 market-context and chart-intelligence read models." |
| S2 | Deterministic structure/indicator reuse and versioning | Roadmap scope | Reuse the V1 deterministic surface; version computation so inputs/versions are immutable |
| S3 | Multi-timeframe relationship model | Roadmap scope; spec §15 | Four typed layers — directly observed / derived / contextual / statistical; **no unsupported cross-timeframe conclusions** |
| S4 | Market-context outputs | Roadmap scope; spec §14 | Synthesis layer above deterministic indicators: trend, structure, levels, session, volatility, momentum, liquidity, timeframe relationships; **all generated context traceable to contributing observations** |
| S5 | Chart annotations + contextual explanations | Roadmap scope; spec §16 | Pipeline: deterministic detection → market context → chart intelligence → annotations + interpretation; **facts distinguished from interpretations and predictions** |
| S6 | Report/artifact model expansion | Roadmap scope; BE-0 design plan (architecture reference) | New read-model artifacts for market context and chart intelligence (reference names `v2_market_context_reports`, `v2_chart_intelligence_reports`); endpoint reference `/api/v2/market-context/` |
| S7 | Server-side computation | Roadmap scope; charter invariant 3 | Authoritative analytical work is server-side; the terminal consumes governed read models, never computes authoritative state |

**Band controls (roadmap, binding on the design):** facts / derived observations / contextual interpretations / predictions remain **separately typed**; structural outputs **do not imply** institutional order flow or execution readiness; **insufficient data remains a typed outcome**.

**Band exit evidence (roadmap):** deterministic/reproducibility tests; temporal-integrity tests; lineage from output to source snapshot and computation version; direct **API and browser** evidence of facts versus interpretation.

**Maturity:** BE-4 capabilities are `DESIGNED` in the registry (`AXIOM-V2-GOV-MAT-001`, BE-0 delivery) — architecture-level design exists; **the band has not started**. No BE-4 design plan is on record in the ITRGA workspace (verified by absence in the record, 2026-08-31).

## 3. Current-state facts — the ground BE-4 lands on (all Level I, 2026-08-31, unless noted)

| Fact | Value | Evidence |
|---|---|---|
| Working database head | `20260829_0042 (head)` | verify run 1 (2026-08-31 14:40:05 +03:00) |
| Provider state (in force) | `twelvedata`: `contract_tested` / `verified` / **`persistence_permitted = false`** | `ITRGA-DET-V2-BE-3-P2-TRANS-APPLY-FINAL-001` §1 |
| Immutability guards | 4 guard triggers on `v2_md_provider` / status history; 5/5 refusals byte-exact | verify run 1 B7 |
| Drift baseline | `alembic check` = **exactly** the inherited V1 9-token set; zero V2 tokens | verify run 1 B9 |
| Test baseline | **750** (552 V1 + 78 BE-1 + 45 BE-2 + 33 P1 + 25 P2 + 17 transition) | P2 run correlation `a246607c-f0c5-42e9-8f3b-a1e1bd75fa83`; authoritative per final determination |
| Input data available | BE-2 normalized market-data model (bar/quote/tick/event/snapshot contracts, read-only query API, immutable snapshot metadata) with the **V1 simulator adapter maintained as a clearly labelled source** | BE-2 delivery (accepted) |
| Dialect posture | DA workspace **SQLite-only** (`AXIOM-V2-BE-1-PG-EXCEPTION-001`); PostgreSQL gates are deployment-dialect proofs | record of record |
| Frontend | **blocked** — sequencing directive in force | `AXIOM-V2-OD-BE-3-P2-003` §3; OD-005 §5 |
| Protection of in-force state | The BE-3 P2 end state is guarded in-DB: BE-4 **cannot and must not** touch the provider registry or history rows | guards (Level I) |

## 4. Open scope decisions (Operator)

Two decisions are required to open the plan stage. Both are presented with an ITRGA recommendation; the Operator decides (OD-007).

### SD-1 — Data basis for BE-4 computation and evidence

BE-4 read models require market data as input. Current facts constrain the options: `persistence_permitted = false` (in force); enabling persistence is "a separate, later-governed act" (final determination §3); the validation-tier discipline (roadmap §0.2) — synthetic data may prove the pipeline, never silently substantiate market conclusions; no provider network call in tests (credential law; determinism).

| Option | Content | ITRGA assessment |
|---|---|---|
| **A (recommended)** | BE-4 is built and evidenced against the BE-2 normalized model fed by the **V1 simulator adapter (labelled synthetic)** — pipeline-validation tier. All band exit evidence (determinism, temporal integrity, lineage, facts-versus-interpretation) is produced on labelled synthetic input. `persistence_permitted` remains `false`; no provider network call in any test. **Real-data research validation** (real historical data via a permitted, integrated source) is a **separate, later-governed act** and does not block BE-4 closure. | Consistent with every in-force state and with the tier discipline. No new credential, persistence, or provider action; the band closes on provable evidence; the epistemic status stays honest (pipeline proven; market conclusions remain unclaimed). |
| B | BE-4 **presumes a persistence-permitted act first** (a separate OD-gated act permitting Twelve Data payload persistence), then BE-4 is evidenced partly on real historical data. | Adds a dependency ahead of BE-4's own discipline; not required by the band text; defers the band for a step the band does not need. If chosen, ITRGA records the sequence and reviews the persistence act as its own chain. |

### SD-2 — Exit evidence: the "browser evidence" item

The roadmap exit evidence includes "direct API and **browser** evidence of facts versus interpretation." The V2 frontend bands are blocked by the sequencing directive until the V2 backend roadmap is fully cleared. The V1 UI consumes V1 endpoints — it cannot serve as evidence of V2 read models.

| Option | Content | ITRGA assessment |
|---|---|---|
| **A (recommended)** | BE-4 closes on **API-level evidence**: direct API evidence of facts versus interpretation, plus the full determinism/temporal/lineage evidence set. **Browser evidence is recorded as a residual**, to be verified at the FE band / X-01 joint gate. | Respects the sequencing directive with no deviation; the residual is traceable in the determination; no other exit-evidence item is weakened. |
| B | The Operator **unblocks a narrow FE evidence slice** for BE-4 — an explicit, recorded deviation from the sequencing directive (the Operator's own authority), with the slice's boundaries set by the OD. | Available only as an explicit amendment by the Operator; ITRGA would record the deviation with the OD and the boundary, and review the slice as governed FE work. |

**Note:** SD-1 and SD-2 are the only Operator decisions needed to open the plan stage. Phasing, table/endpoint design, and the versioning strategy are **plan-level** (DA design plan) and governed by §6 — they are not Operator decisions.

## 5. Fixed exclusions (invariants — not decisions)

- **No actuation:** no order, execution, broker, account, position, or P&L capability (charter invariant 6; roadmap invariants 1–9).
- **No external AI** (BE-11 territory).
- **No provider network call in tests; no credential read/set/use** (credential law; determinism).
- **No frontend band** (sequencing directive — subject to SD-2).
- **No Git/GitHub operation** (Operator-only custody, deferred clean custody).
- **No change to the BE-3 P2 in-force state:** the guarded tables (`v2_md_provider`, `v2_md_provider_status_history`) remain immutable to BE-4; no new provider status, no history append, no write to the BE-3 P2 audit domain. BE-4 adds its **own** read-model tables via new migrations after `20260829_0042`.
- **No `integrated` or higher ladder step** (separate chain; the transition authority string `BO-V2-BE-3-P2-TRANS-001` was consumed).
- **No persistence permission** (SD-1-governed); the Four Secrets remain untouched.

## 6. Plan-stage requirements (governing input for the DA design plan)

The BE-4 design plan must address, at minimum:

1. **Reuse and versioning** — the V1 deterministic structure/indicator surface to be reused, established with Level II evidence in the plan (inventory, entry points, versions), and the computation-versioning contract (registered versions; immutable inputs; independent versioning per spec §53).
2. **Multi-timeframe model** — spec §15: the four-layer typing (directly observed / derived / contextual / statistical) as **typed schema fields, not prose**; the no-unsupported-cross-timeframe-conclusion rule enforced and tested.
3. **Market-context output model** — spec §14: the ten observation families (prevailing trend; structural state; protected swing; structural break; liquidity context; key levels; session context; volatility state; momentum state; timeframe relationships); every output traceable to its contributing observations (lineage), with computation version, as-of time, and explicit mode.
4. **Chart-intelligence model** — spec §16 pipeline (deterministic detection → market context → chart intelligence → annotations + interpretation); facts vs interpretations vs predictions enforced at schema level.
5. **Research read-model expansion** — new tables for market-context and chart-intelligence reports (BE-0 architecture-reference names `v2_market_context_reports`, `v2_chart_intelligence_reports`; final naming is the plan's); report/artifact model on the BE-1 audit/lineage contract; immutable inputs and computation versions.
6. **Typed outcomes** — insufficient data as a typed outcome (band control), mapped onto the BE-1 status model (`available`, `unavailable`, `stale`, `degraded`, `unknown`, `denied`).
7. **Endpoints** — read-only, under `/api/v2/market-context/` (BE-0 route table); no client-side authoritative computation (charter invariant 3).
8. **Data basis** — per the OD-007 SD-1 outcome: labelled synthetic input via the BE-2 simulator adapter; no provider network call in tests; validation tier declared per roadmap §0.2.
9. **Migrations** — new alembic revision(s) after `20260829_0042`; `alembic check` baseline = **exactly** the inherited V1 9-token set (zero BE-4 tokens); rollback evidence; all new tables follow the accepted PK convention (uuid4 `TEXT(36)`). ITRGA verification will be **content-based row comparison** (PGF-012 lesson) — no position-based assertions in any check or pack.
10. **No-touch list** — the guarded tables and the BE-3 P2 in-force state (§5); V1 code paths preserved (extension, not rewrite); the V1 552-test regression set stays green.
11. **Evidence plan** — single transcript per run; `-File` execution; MD5 self-check on the machine; credential scan CLEAN before every archive; test delta against the 750 baseline reported explicitly.
12. **Exit-evidence mapping** — each roadmap exit-evidence item mapped to a specific test/evidence artifact, including the SD-2 treatment of "browser evidence."

## 7. Governance chain — forward

| Stage | Artifact | Owner | State |
|---|---|---|---|
| 1 | OD-006 (recorded) | Operator → ITRGA record | **DONE — 2026-08-31** |
| 2 | Scope assessment (this document) | ITRGA | **DONE — 2026-08-31** |
| 3 | OD-007 — scope decision (SD-1, SD-2) | Operator | **OPEN — the single next action** |
| 4 | BE-4 design plan (addressing §6) | DA | awaits stage 3 |
| 5 | ITRGA plan review → plan determination | ITRGA | awaits stage 4 |
| 6 | Build Order | chain per lifecycle | awaits stage 5 |
| 7 | DA implementation + tests + direct evidence (single transcript) | DA | awaits stage 6 |
| 8 | ITRGA source/evidence review + verification pack (standing battery: ASCII audit, brace audit, AST parse, faithful-schema dry run, MD5 self-check) | ITRGA | awaits stage 7 |
| 9 | ITRGA determination (band closure) | ITRGA | awaits stage 8 |

Custody throughout: no Git operations; DA work in the DA workspace; repository publication remains the Operator's custody action.

## 8. Evidence status

| Statement | Classification |
|---|---|
| BE-4 band definition, controls, exit evidence | **Verified fact** — `AXIOM-V2-BE-ROADMAP-001` (PROPOSED planning document; confers no authority by itself) |
| Spec §14/§15/§16 requirements as quoted | **Verified fact** — proposed specification text; binding force through the charter and the chain |
| In-force state: head 0042; provider `contract_tested`/`verified`/`false`; guards; drift set; 750-test baseline | **Verified fact** — `ITRGA-DET-V2-BE-3-P2-TRANS-APPLY-FINAL-001` + verify run 1 (Level I, 2026-08-31) |
| No BE-4 design plan on record in the ITRGA workspace | **Verified fact** (absence in the record, 2026-08-31) |
| Exact V1 deterministic-analysis surface (modules, functions, versions) | **UNKNOWN** — plan-stage fact; the DA design plan establishes it with Level II evidence (§6.1) |
| "BE-4 read models work" | **NOT PROVEN** — until the band's evidence exists. Per the tier discipline this is the correct epistemic state: synthetic input proves the pipeline; it does not substantiate market conclusions |

## 9. Single next action

**The Operator issues OD-007 — the BE-4 scope decision (SD-1 and SD-2).**

Minimal acceptable form:

> *Operator decision: for BE-4, I decide **SD-1 = Option A** (labelled-synthetic data basis; persistence remains a separate, later-governed act) and **SD-2 = Option A** (API-level evidence closure; browser evidence a recorded residual). I direct the DA to produce the BE-4 design plan per the requirements of `ITRGA-ASS-V2-BE-4-SCOPE-001` §6. **No repository changes are authorized by this decision.***

(Any A/B combination of SD-1/SD-2 is accepted as recorded; the chain adapts to the decision.)

On receipt: ITRGA records OD-007; §6 becomes the governing plan input; the chain proceeds to stage 4 (DA design plan).

— ITRGA, 2026-08-31

---

## 10. Dated note — OD-007 received (2026-08-31)

- The Operator issued **OD-007** (`AXIOM-V2-OD-BE-4-007`, recorded in `docs/governance/OPERATOR_DECISION_V2_BE-4_SCOPE.md`): **SD-1 = Option A** (labelled-synthetic data basis; persistence remains a separate, later-governed act) and **SD-2 = Option A** (API-level evidence closure; browser evidence a recorded residual). The DA is directed to produce the BE-4 design plan per §6; no repository changes are authorized.
- ITRGA formalized the direction as request **`ITRGA-REQ-V2-BE-4-001`** (`ITRGA_REQUEST_V2_BE-4_DESIGN_PLAN.md`): pre-registered guardrails BG-1…BG-12; required plan content (this document §6, item-for-item); process and reviewer posture.
- **§6 of this assessment is now the governing input for the DA design plan.** The scope-assessment stage is complete; the chain is at **stage 4 (DA design plan — awaiting delivery)**. No Build Order issues before an ITRGA-approved plan (roadmap §3; pre-work pattern).
- Original text of this assessment preserved unedited; this note is an append per the standing correction/closure discipline.

— ITRGA, 2026-08-31
