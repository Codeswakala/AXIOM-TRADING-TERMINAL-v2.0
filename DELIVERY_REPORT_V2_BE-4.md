# DELIVERY REPORT — AXIOM V2 BE-4: Market Context, Chart Intelligence, Research Read Models

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-4-DR-001 |
| Build Order | BO-V2-BE-4-001 (issued per AXIOM-V2-OD-BE-4-008) |
| Governing plan | AXIOM-V2-BE-4-DA-PLAN-001 v1.0.0 (APPROVED WITH OBSERVATIONS — ITRGA-REV-V2-BE-4-PLAN-001; R-1…R-5 binding) |
| Date | 2026-08-31 |
| Author | Development Authority (DA) |
| Status | **SUBMITTED FOR ITRGA SOURCE/EVIDENCE REVIEW** |
| Baseline in | head `20260829_0042` · 750 tests · drift = the 9 inherited V1 tokens |
| Baseline out | migration `20260831_0043` (test chains only — **no working-database modification**, BO §9) · **789 tests** · drift unchanged |

**Standing discipline: we don't guess. We prove.**

---

## 1. Executive Summary

BE-4 is implemented per the approved plan with all five binding refinements
R-1…R-5 satisfied. DA verification: **789 tests executed, 789 passed, 0
failed** = 750 baseline + **39 new BE-4 tests** (all green; itemization §4).
Zero V1 diffs; the BE-3 P2 in-force state untouched and proven untouched;
zero network attempts (socket guard on every BE-4 test); lint clean.

**Validation-tier declaration (BO §6.12, SD-1 = A): pipeline-validation.**
Every result in this band is produced on labelled synthetic input
(`live:simulated` via the BE-2 model). The evidence proves the pipeline —
determinism, temporal integrity, lineage, typing. **It substantiates no
market conclusion.** "BE-4 read models produce correct market analysis"
remains NOT PROVEN and is not claimed.

**Browser evidence (BO §6.12, SD-2 = A): RECORDED RESIDUAL** — carried
here for the determination; to be verified at the FE band / X-01 joint gate.

## 2. Deliverables vs BO §4

| Deliverable | State |
|---|---|
| D-1 Migration `20260831_0043_v2_be4_research_read_models` | Implemented: 3 tables (uuid4 `TEXT(36)` PKs); determinism anchor `UNIQUE(instrument_id, input_content_hash, engine_versions_hash)`; `engine_versions_hash` per the OBS-3 pin (SHA-256 over JSON, keys sorted, no whitespace — asserted byte-exact by test); 6 R-2 guard triggers with the exact pinned names/messages; revision-local seeds (3 computation versions with source hashes recorded at seed time; 5 permission rows); symmetric downgrade; guard-presence verification |
| D-2 MCE module set | `app/v2/research/{versioning,typing,market_context}.py` — all ten §14 families on the reused V1 surface; deterministic ids; single typing gate |
| D-3 CIE module set | `app/v2/research/chart_intelligence.py` — annotations (fact/derived only) vs interpretations (contextual, non-empty basis enforced); zero predictions |
| D-4 Endpoints | 4 GET + the single `POST /market-context/compute` (R-1), mounted on the V2 aggregate router; V2 envelope on every response |
| D-5 Tests | **39 tests** in `tests/test_v2_be4_{research,migration,api}.py` — nine plan §11 groups (§4 itemization); content-based comparisons only |
| D-6 DR + transcripts | This report; `docs/evidence/V2_BE-4_SOURCE_TRANSCRIPT.md` (REM-001, 15 files literal); `docs/evidence/V2_BE-4_API_TRANSCRIPT.txt` (Level I) |
| D-7 Register sync | `V2_CURRENT_STATE.md` v19.0.0; risk/debt registers synchronized (OBS-2) |

## 3. Binding refinements — satisfaction evidence

**R-1 (governed writer).** `POST /market-context/compute` is the only
non-GET endpoint (Level I: the executed API transcript exercises the full
surface; the route table contains exactly 4 GET + 1 POST). RBAC-gated by
`v2.research.market_context.compute` (admin-only; operator role receives
read permissions only — the `denied` test proves default-deny with the
generic public message). Mode-enforced server-side. Fully audited
(`research.market_context.computed`, `research.chart_intelligence.computed`,
`…compute.reused`, `…compute.unknown`). Idempotent by the determinism
anchor — executed proof: repeat POST returned `reused_existing: true`,
same report id, report count still 1, reuse audited.

**R-2 (DB-level immutability).** Six triggers created with the exact
pinned names; all six guard messages asserted **verbatim** by test
(`test_guard_messages_verbatim`). v2 trigger count after 0043 = **18**
(12 + 6) — the planning-level expectation is now Level II (executed test)
on test chains. Original 12 triggers proven unchanged (no-touch group).
Downgrade drops exactly the six. Repository layer is append-only
(no UPDATE/DELETE surface) as defense-in-depth.

**R-3 (endpoint-path pin).** Level I executed API transcript
(`V2_BE-4_API_TRANSCRIPT.txt`): the final path is
**`/api/v1/v2/market-context/*`** (V1 app prefix `/api/v1` + V2 aggregate
router `/v2` + band sub-router `/market-context`). This **closes the BE-0
route-table reference discrepancy**: the BE-0 reference
`/api/v2/market-context/` is a naming-era artifact; the physical mount
follows the accepted single-application topology (ARCH-001 §1.2). No route
migration performed.

**R-4 (timeframe_relationships rule table).** The fixed rule table, pinned
in code (`app/v2/research/typing.py::TIMEFRAME_RELATIONSHIP_RULES`) and
asserted by tests:

| Relationship class | Layer | Claim type | Rationale |
|---|---|---|---|
| `trend_alignment` | derived | derived_observation | Same-family state compared across two timeframes — computed relationship |
| `momentum_alignment` | derived | derived_observation | As above |
| `volatility_alignment` | derived | derived_observation | As above |
| `higher_tf_context` | contextual | contextual_interpretation | Reads higher-TF state as context for lower — interpretation by construction |
| `structure_nesting` | contextual | contextual_interpretation | As above |

Refusal cases tested at every class boundary: unpermitted class
(`order_flow_inference`) refused; derived-class emitted as contextual
refused; contextual-class emitted as derived refused; single-timeframe
relationship refused; cross-timeframe `fact`/`observed` refused
(`test_r4_rule_table_every_permitted_class`,
`test_r4_refusal_cases_per_class_boundary`,
`test_cross_timeframe_fact_refused`).

**R-5 (precedent citations).**
- *BE-2 governed-writer precedent:* W-1 catalog refresh
  (`app/v2/marketdata/api/writers.py::catalog_refresh`, accepted under
  ITRGA-DET-V2-BE-2-001) — the accepted pattern of a single authenticated,
  mode-gated, audited, idempotent mutation path; BE-4's compute writer
  follows it.
- *DEL-004 permission-seed lesson:* BE-1 correction DEL-004 (accepted in
  the BE-1 band record) — migration permission seeds must be
  revision-local literal rows, never imported from the live permission
  module; migration 0043 seeds its 5 rows as literals.

## 4. Test evidence (789 = 750 + 39, itemized; no double counting)

| Module | Count | Plan §11 groups |
|---|---|---|
| `test_v2_be4_research.py` | 22 | 1 determinism (4) · 2 temporal (2) · 3 lineage-engine (2) · 4 typing/R-4 (9) · 5 typed outcomes (3) · 6 band controls/disclosures (2) |
| `test_v2_be4_migration.py` | 5 | migration content+seeds+triggers (1) · guard messages verbatim (1) · no-touch across 0043 (1) · downgrade→re-upgrade cycle (1) · drift gate (1) |
| `test_v2_be4_api.py` | 12 | R-1 writer+audit+lineage DB walk (2) · API typing evidence (1) · six BE-1 states: available/degraded/unavailable/stale/unknown/denied (6) · validation: future as_of, unknown instrument, version-hash mismatch refusal (3) |
| **Total new** | **39** | Full suite: **789 passed, 0 failed** (V1 552 green — BG-9) |

All six BE-1 states individually proven: `available`, `degraded` (typed
`insufficient_data` entries), `unavailable` (empty series), `stale`
(declared bound = 3 timeframe periods; disclosure stored in the artifact),
`unknown` (version resolution impossible → nothing persisted, audited),
`denied` (default-deny; generic message; refusal path). Socket guard on
every BE-4 test — zero network attempts. Wall-clock/randomness
construction-token scan on the deterministic core (no `now()`, no
`random.`, no `uuid4(` — ids are deterministic sequences, making report
bodies byte-identically reproducible).

## 5. BO §6 evidence checklist

| # | Requirement | Evidence |
|---|---|---|
| 1 | Single transcript; MD5/SHA self-check | Source + API transcripts; SHA-256 manifest recomputed against the working tree |
| 2 | REM-001 literal transcript | `V2_BE-4_SOURCE_TRANSCRIPT.md` — 12 new + 3 modified files, literal |
| 3 | Full SHA-256 of the reused V1 surface | In transcript §1: `indicators.py` `af661b52…fa9e0`, `market_structure.py` `bd83c672…a74b`, `indicator_registry.py` `02d2e981…8c87` (closes OBS-1) |
| 4 | Level I API transcript (R-3) | `V2_BE-4_API_TRANSCRIPT.txt` — path pinned; claim_type separation shown verbatim (fact / derived_observation / contextual_interpretation; predictions = 0) |
| 5 | R-4 rule table | §3 above + code pin + tests |
| 6 | R-5 citations | §3 above |
| 7 | Test delta vs 750 | §4: 750 + 39 = **789**, itemized per group |
| 8 | Drift gate at 0043 | Executed (test + direct run): exactly the inherited 9-token set (1 add_table `audit_write_failure_records` + 2 add_index + 6 remove_index); **zero** BE-4 tokens |
| 9 | No-touch evidence | Executed test: provider row + history rows content-identical across 0043; trigger set 12→18 with the original 12 unchanged; `persistence_permitted` = false throughout; provider guard re-proven post-0043 |
| 10 | upgrade→downgrade→upgrade cycle | Executed test, content-based comparison (components, hashes, permissions, provider state) |
| 11 | Credential scan | CLEAN on every artifact; Four Secrets untouched; no credential read/set/use anywhere in the band |
| 12 | Validation tier + browser residual | §1 declarations |
| 13 | Known limitations | §6 below |

## 6. Known limitations / open items (honest; unknown is an allowed state)

1. **Test-chain note (disclosed):** fresh BE-4 test chains pass through
   revision 0042, whose authority gate refuses by design. The BE-4
   migration test harness sets `AXIOM_TD_TRANSITION_AUTHORITY_REF` for its
   own dedicated test databases only — the same accepted pattern as the
   transition band's own tests. This does not re-execute the transition
   act anywhere governed: the working database is untouched (BO §9), and
   the act's authority string is consumed only in the governed record, not
   in test sandboxes.
2. **0043 working-DB application NOT performed** — a separate, later-
   governed act (new Operator decision, sanctioned pack, backup anchor,
   verify act — the BE-3 P2 apply-act pattern; BO §9).
3. `stale` bound (3 timeframe periods) is a band-level declared bound; a
   different governed bound can replace it in a future band without schema
   change (the disclosure carries the bound used).
4. Family-level statement vocabularies (e.g. trend = up/down/flat) are
   v1-scope deterministic reductions; richer vocabularies are future
   plan-stage work, versioned via the `market_context_engine` component.
5. `structure_nesting` (R-4 table) is a permitted class with no v1 emitter
   — the rule + refusal boundary are pinned and tested now; emission
   arrives with a future MCE version bump.
6. Browser evidence residual (SD-2 = A) and real-data research validation
   (SD-1 = A) remain recorded residuals — out of this band by decision.
7. Inherited V1 lint/drift debt unchanged (carried; not BE-4's to resolve).

## 7. Security & constitutional attestation

No actuation surface. No external AI. Zero provider network calls (socket
guard, Level II). No credential in any artifact (scans CLEAN). RBAC
default-deny; 3 additive permissions; compute admin-only (SAL-3); sensitive
denial generic. Mode RESEARCH/SIMULATION enforced server-side. V1
byte-untouched (BG-9); the BE-3 P2 in-force state untouched and guarded
(BG-3). No Git operation (custody deferred — OD-008). No working-database
modification (BO §9).

## 8. Handover

| Item | State |
|---|---|
| Evidence | `docs/evidence/V2_BE-4_SOURCE_TRANSCRIPT.md` · `docs/evidence/V2_BE-4_API_TRANSCRIPT.txt` |
| State docs | `V2_CURRENT_STATE.md` v19.0.0; registers synchronized |
| Next | (1) ITRGA source/evidence review + verification pack (standing battery); (2) ITRGA determination closes the band; (3) 0043 working-DB application = separate governed act; (4) BE-5 requires a new Operator directive |

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-4-DR-001**
