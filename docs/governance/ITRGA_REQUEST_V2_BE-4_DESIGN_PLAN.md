# ITRGA REQUEST FOR BE-4 ENGINEERING DESIGN PLAN — "MARKET CONTEXT, CHART INTELLIGENCE, RESEARCH READ MODELS"

| Field | Value |
|---|---|
| Request ID | `ITRGA-REQ-V2-BE-4-001` |
| From | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| To | Development Authority (DA), via Operator |
| Document type | Pre-workstream Design Plan Request + Pre-registered Band Guardrails |
| Date | 2026-08-31 |
| Programme / band | AXIOM V2 · **Band BE-4 — Market Context, Chart Intelligence, and Research Read Models** (`AXIOM-V2-BE-ROADMAP-001`) |
| Authority | `AXIOM-V2-OD-BE-4-007` (Operator direction; SD-1 = A, SD-2 = A); `AXIOM-V2-OD-BE-4-006` (chain opened); `ITRGA-ASS-V2-BE-4-SCOPE-001` (§6 governing requirements) |
| Platform baseline | working DB `backend\axiom_dev.db` · Alembic head **`20260829_0042`** · **750 tests** (552 V1 + 78 BE-1 + 45 BE-2 + 33 P1 + 25 P2 + 17 transition) · provider `twelvedata` **`contract_tested` in force** (`verified` / persistence `false`) · drift = exactly the inherited V1 9-token set · Gate CLOSED · FE bands blocked (sequencing directive) |
| Governing docs (collective, in precedence) | `AXIOM-V2-GOV-CHARTER-001` (APPROVED) → `AXIOM-V2-BE-ROADMAP-001` Band BE-4 → `AXIOM V2 — PRODUCT & ARCHITECTURE SPECIFICATION` §14/§15/§16 → `ITRGA-ASS-V2-BE-4-SCOPE-001` (with OD-007 decisions) → V1 preservation instruments (charter §3) |
| Motto | *We don't guess. We prove.* |

---

## 0. Status & instruction

Per the roadmap §3 delivery model and the pre-work pattern established for this programme (plan reviewed **before** any Build Order), **no BE-4 Build Order will be issued until the DA delivers a BE-4 Engineering Design Plan and ITRGA has reviewed and accepted it.**

OD-007 directs the DA to produce the plan. The two scope decisions are **fixed parameters of the plan** (not open questions):

- **SD-1 = A:** labelled-synthetic data basis (BE-2 normalized model fed by the V1 simulator adapter; pipeline-validation tier); `persistence_permitted` remains `false`; no provider network call in tests; real-data research validation is a separate, later-governed act.
- **SD-2 = A:** API-level evidence closure; browser evidence a **recorded residual** (verified at the FE band / X-01 joint gate).

The DA shall treat every guardrail in §1 as a **first-class acceptance criterion**, and every item in §2 as **required plan content**.

---

## 1. PRE-REGISTERED BE-4 GUARDRAILS (binding acceptance criteria)

**Constitutional (charter §7 + roadmap §2 invariants):**
- **BG-1 — No actuation.** No order, execution, broker, account, position, P&L, or gate-opening capability, path, or state. Execution stays default-deny.
- **BG-2 — Read models, server-side.** All authoritative computation is server-side; the band exposes **read-only** governed endpoints; the terminal never computes authoritative analytical state (charter invariant 3).
- **BG-3 — No-touch on in-force state.** `v2_md_provider` and `v2_md_provider_status_history` remain immutable (guards enforce in-DB; the plan must also exclude them at design level). No new provider status, no history append, no write to the BE-3 P2 audit domain. No `integrated` or higher ladder step.
- **BG-4 — Data basis (OD-007 SD-1 = A).** Labelled synthetic input via the BE-2 simulator adapter; validation tier declared per roadmap §0.2; **no provider network call in any test**; no credential read/set/use; `persistence_permitted` stays `false`; no persistence act inside this band.
- **BG-5 — Typed outcomes.** Facts / derived observations / contextual interpretations / predictions remain **separately typed at schema level**; insufficient data is a **typed outcome** mapped onto the BE-1 status model (`available`, `unavailable`, `stale`, `degraded`, `unknown`, `denied`); unknown is an allowed state.
- **BG-6 — Determinism & temporal integrity.** Reproducible, versioned computation; as-of-bounded; no future data; the deterministic core does not depend on wall-clock or uncontrolled randomness (seeded/fixed where determinism is asserted).
- **BG-7 — Lineage.** Every output is traceable to its source snapshot and computation version (BE-1 audit/lineage contract; charter invariant 9).
- **BG-8 — Dialect & migrations.** DA workspace **SQLite-only** (`AXIOM-V2-BE-1-PG-EXCEPTION-001`); new alembic revision(s) after `20260829_0042`; `alembic check` baseline = **exactly** the inherited V1 9-token set (zero BE-4 tokens); new tables follow the accepted PK convention (uuid4 `TEXT(36)`); rollback/rollback-evidence plan required.
- **BG-9 — V1 preservation.** V1 code paths are extended, never rewritten; the V1 552-test regression set stays green; V1 historical evidence is immutable (charter §3).
- **BG-10 — Exit evidence (OD-007 SD-2 = A).** API-level evidence closure; **browser evidence declared as a recorded residual** in the plan and the eventual determination.
- **BG-11 — Boundaries.** No frontend band (sequencing directive); no external AI (BE-11); no Git/GitHub operation (Operator custody, deferred); the Four Secrets remain untouched.
- **BG-12 — Evidence discipline.** Single transcript per run; `-File` execution; MD5 self-check on the machine; credential scan CLEAN before every archive; test delta against the **750** baseline reported explicitly.

---

## 2. What the design plan must contain

The DA shall deliver a **single** document (suggested ID `AXIOM-V2-BE-4-DA-PLAN-001`, mirroring the format of the accepted V2 design plans, e.g. `AXIOM-V2-BE-3-P2-DA-PLAN-001`) with a header block (document ID, version, date, author DA, source request `ITRGA-REQ-V2-BE-4-001`, governing roadmap band, status *SUBMITTED FOR ITRGA PLAN REVIEW*) and content addressing, at minimum, the twelve governing requirements of `ITRGA-ASS-V2-BE-4-SCOPE-001` §6:

1. **Reuse and versioning** — the V1 deterministic structure/indicator surface to be reused, established with **Level II evidence in the plan** (inventory: modules, entry points, versions); the computation-versioning contract (registered versions; immutable inputs; independent versioning per spec §53).
2. **Multi-timeframe model** — spec §15: the four-layer typing (directly observed / derived / contextual / statistical) as **typed schema fields, not prose**; the no-unsupported-cross-timeframe-conclusion rule, enforced and tested.
3. **Market-context output model** — spec §14: the ten observation families (prevailing trend; structural state; protected swing; structural break; liquidity context; key levels; session context; volatility state; momentum state; timeframe relationships); every output traceable to its contributing observations, with computation version, as-of time, and explicit mode.
4. **Chart-intelligence model** — spec §16 pipeline (deterministic detection → market context → chart intelligence → annotations + interpretation); facts vs interpretations vs predictions enforced at schema level.
5. **Research read-model expansion** — new tables for market-context and chart-intelligence reports (BE-0 architecture-reference names `v2_market_context_reports`, `v2_chart_intelligence_reports`; final naming is the plan's); report/artifact model on the BE-1 audit/lineage contract; immutable inputs and computation versions.
6. **Typed outcomes** — insufficient data as a typed outcome (band control), mapped onto the BE-1 status model (BG-5).
7. **Endpoints** — read-only, under `/api/v2/market-context/` (BE-0 route table); response contracts carrying the typed status/failure model and explicit mode; no client-side authoritative computation (BG-2).
8. **Data basis** — per OD-007 SD-1 = A (BG-4): labelled synthetic fixtures via the BE-2 simulator adapter; validation tier declared; no provider network call.
9. **Migrations** — revision plan (revision IDs, up/down, ordering after `20260829_0042`); `alembic check` baseline = exactly the inherited V1 9-token set; rollback evidence; PK convention (BG-8).
10. **No-touch list** — the guarded tables and the BE-3 P2 in-force state (BG-3); V1 code paths (BG-9); explicit statement of what the band does **not** change.
11. **Test strategy** — deterministic/reproducibility tests; temporal-integrity tests (as-of bounded, no future data); lineage tests (output → source snapshot + computation version); typed-failure tests (insufficient data; each BE-1 status state); no-touch/guard tests; **no position-based row assertions** (PGF-012 lesson — content-based comparison); test delta against the 750 baseline stated.
12. **Evidence plan + exit-evidence mapping** — each roadmap exit-evidence item mapped to a specific test/evidence artifact; SD-2 residual declared (BG-10); single transcript, `-File`, MD5 self-check, credential scan (BG-12).

Plus, in the plan's own words: **explicit exclusions** (per `ITRGA-ASS-V2-BE-4-SCOPE-001` §5) and **known limitations / open items** (honest; unknown is an allowed state — charter invariant 8).

---

## 3. Process from here

1. **DA → Operator → ITRGA:** deliver the BE-4 Engineering Design Plan (single document; no repository changes — the plan is a document, and OD-007 authorizes no repository change).
2. **ITRGA:** line-by-line plan review across all guardrails (§1) and required content (§2) → `ITRGA_REVIEW_V2_BE-4_DESIGN_PLAN.md` with verdict **APPROVED / APPROVED WITH OBSERVATIONS / RETURN FOR REVISION / REJECTED** (binding refinements, if any, pre-registered in the review).
3. **On an approved plan + Operator authorization:** Build Order (stage 6) — **only an Approved determination authorizes progression** (roadmap §3).
4. **Then:** DA implementation + tests + direct evidence (single transcript) → ITRGA source/evidence review + ITRGA verification pack under the standing battery (ASCII audit, brace audit, AST parse, faithful-schema dry run, MD5 self-check) → ITRGA determination (band closure).

Custody throughout: no Git operations; DA work in the DA workspace; repository publication remains the Operator's custody action.

---

## 4. Reviewer posture reminder

- A violation of any pre-registered guardrail (BG-1…BG-12) ⇒ **REJECTED**, or **RETURN FOR REVISION** for a fixable gap.
- Technical claims in the plan (V1 surface inventory, reuse feasibility, test sufficiency) must carry **Level I/II evidence classification**; an unsupported claim is Level IV and will not be accepted — *we don't guess, we prove*.
- The plan **authorizes nothing**: implementation authority arises only from the Build Order after an approved plan and Operator authorization.
- The exit-evidence mapping must be complete item-for-item, including the SD-2 residual; a mapping gap is a review defect.
- ITRGA issues **corrective observations, not architectural redesign**, unless a constitutional violation requires broader intervention.

---

*We don't guess. We prove.*
**— AXIOM ITRGA, 2026-08-31**
