# ITRGA_PRV_V2_BE-6_PLAN_001 — Full-depth plan review + scope assessment verdict: `AXIOM-V2-BE-6-DA-PLAN-001` v1.0.0

| Item | Value |
|---|---|
| Date | 2026-09-03 |
| Reviewed artifact | `AXIOM-V2-BE-6-DA-PLAN-001` v1.0.0, 2026-09-03 (303 lines; received via Operator custody) |
| Review contract | `ITRGA-REQ-V2-BE-6-PLAN-001` REQ §1.1–§1.11; Pins P-1…P-5 (carried) + P-6/P-7 (BE-6); roadmap `AXIOM-V2-BE-ROADMAP-001` Band BE-6 contract |
| Review depth | **Full-depth** — every DDL line, contract, mechanism, test budget, evidence plan, boundary, and register impact checked against the governed corpus, not skimmed |

## 1. Independent corroborations performed (not trusted — proven)

| Check | Method | Result |
|---|---|---|
| §0 roadmap quote fidelity | Extracted Band BE-6 section from in-repo `uploads/V2_BACKEND_ROADMAP.md` (lines 254–280) and compared item-by-item: objective, 4 scope bullets, 2 exclusions, 4 exit-evidence items | **BYTE-SUBSTANTIVE VERBATIM — zero divergence** |
| Roadmap file existence (plan's "repo-resident" claim) | `find` across workspace | TRUE: `AXIOM-TRADING-TERMINAL-v2.0/uploads/V2_BACKEND_ROADMAP.md` (clone-custody copy; verified the §0 source against it) |
| V1 reuse inventory (4 files) | Recomputed SHA-256-16 on the frozen clone | **all four byte-match the plan's pins**: risk `6940509097b65e6f`, analytics `b2fe2fdb06e49ca7`, ledger `6ec97a72aea910bf`, simulation `f163e610ba1a6215` — the V1 execution-research surface is frozen and identical between DA tree and review reference |
| Cited config | `grep confidence_level app/ml/validation/service.py` | `= 0.95` exists at line 35 — citation target is real |
| Chain-state arithmetic | Cross-check vs verified records (`ITRGA-DET-V2-0045-APPLY-001`) | head `20260902_0045` ✓; 28+4=32 triggers ✓; 35+6=41 permissions ✓; 5+1=6 compver ✓; 856+50=906 floor ✓; all internally consistent in the plan |

## 2. REQ-item verdicts

| REQ | Plan cites | Verdict |
|---|---|---|
| 1.1 decomposition/DDL/guards/seeds/totals/drift | Part 1 (U-1…U-4; two tables; 4 guards w/ exact messages; 6-grant seeds; downgrade symmetric; 32/41/6 pinned; unchanged drift) | **COMPLIANT** |
| 1.2 hypothetical-only versioning | §1.2 (`record_seq`+`supersedes`; `UNIQUE(portfolio_id, record_seq)`; single-value `basis` CHECK; weights contract 1.0±1e-9/≥0, long-only disclosed) | **COMPLIANT** |
| 1.3 metric contract / determinism / citation law | Part 2 (full contract per metric; pure functions; chi-square CI citing existing `confidence_level=0.95`; both VaR methods reported separately, never merged; grouping-not-regression declared) | **COMPLIANT** |
| 1.4 scenarios | Part 2 (declared deterministic shocks; realism limitation mandatory; empty-with-reason allowed) | **COMPLIANT** |
| 1.5 artifact immutability/anchor/idempotency/P-4/as_of | §1.2 (`uq_v2_pfrisk_determinism_anchor`; reuse-return; `engine_versions(_hash)`; as_of no-future; compver `pre-1.0.0` + C-2 instrument re-pin disclosure) | **COMPLIANT** |
| 1.6 hypothetical-vs-account proof | Part 3 (basis CHECK, basis_label, forbidden-marker guard, V1 ledger read-only-labelled) | **COMPLIANT** |
| 1.7 data honesty tiers | Part 3 (6-class both tables; first-landing synthetic/simulated; refusal w/ typed reasons; V2-TD-18 continuity; tier declarations Part 10) | **COMPLIANT** |
| 1.8 mode/audit/security | Part 4 (BE-1 columns; 5 domain audit events + RBAC denial; lineage fields exact; no credentials; redaction untouched) | **COMPLIANT** |
| 1.9 test plan | Part 5 (10+22+16+2=50; floor ≥906; guard/CHECK/versioning/idempotency/states/forbidden-token/socket; worked-annex fixtures) | **COMPLIANT** |
| 1.10 independent recomputation | Part 2 worked-sample annex (pinned portfolio + pinned series + expected values to stated precision) | **COMPLIANT** |
| 1.11 boundaries | Part 8 table (BE-7 / BE-8…10 / BE-11 / corpus / preview-export excluded / future extensions debt-registered) | **COMPLIANT** |

Pins: **P-1…P-5 satisfied by construction** (the plan applies the BE-5 lineage correctly, incl. post-C-1 `supersedes` vocabulary); **P-6 satisfied by design** (exclusions are CHECK/marker structural, not verbal); **P-7 satisfiable at delivery** via the annex design (requirement carried into the BO).

## 3. Scope assessment (charter/mandate)

In-mandate throughout: new surfaces are `v2_`-prefixed tables under the governed migration chain (continuing at 0046, correct down_revision), a new package under `app/v2/portfolio_research/`, and three enumerated additive-only modifications (`app/v2/api/router.py`, `app/v2/rbac/permissions.py`, `app/db/models/__init__.py` — OBS-1-enumerated up front). Forbidden domains untouched by schema, vocabulary, and marker-guard construction. V1 code read-only reference, pins proven frozen. No working-DB application in-band (separate sanctioned act, as established). **Scope: WITHIN MANDATE.**

## 4. Findings

- **Correction items: NONE.** No roadmap divergence, no design-convention violation, no invention detected; the honest disclosures (long-only scope; grouping-not-regression; parametric-normality assumption; pipeline-validation tier; preview/export exclusion; sequencing inversion) are of the class the programme rewards, and sequencing concern is resolved by the REQ being issued as the DR's review contract.
- **Observations (non-blocking):** O-1: the DR requirement map must answer REQ-1.1…1.11 **item-for-item** plus roadmap §0 and P-1…P-7. O-2: the declared symmetric-downgrade for 0046 must be content-proven in test evidence (already budgeted at U-1). O-3: V1 table-name inventory (`portfolio_risk_reports` etc.) was not re-verifiable from the clone's differing migration layout — immaterial: those tables are read-only lineage references, and the file-level pins that DO matter proved byte-identical.

## 5. Verdict

**PLAN ACCEPTED — full-depth verified, zero corrections.** Authorization chain satisfied for Build Order issuance: `ITRGA-CN-V2-BE-6-001` (Operator authorization 2026-09-03) → this verified plan. The ITRGA proceeds to issue **BO-V2-BE-6-001**.

**ISCRIVED as `ITRGA-PRV-V2-BE-6-PLAN-001`.**
