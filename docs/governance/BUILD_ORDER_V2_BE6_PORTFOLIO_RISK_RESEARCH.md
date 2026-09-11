# BUILD ORDER BO-V2-BE-6-001 — Band BE-6: Portfolio and Risk Research Domain

| Field | Value |
|---|---|
| Document ID | **BO-V2-BE-6-001** |
| Issued by | ITRGA |
| Date | 2026-09-03 |
| Authority | Operator BE-6 authorization of 2026-09-03 (`ITRGA-CN-V2-BE-6-001`: "you can request the design plan and once fully verified you can issue the build order" — plan fully verified: `ITRGA-PRV-V2-BE-6-PLAN-001`, verdict ACCEPTED, zero corrections) |
| Governing plan | `AXIOM-V2-BE-6-DA-PLAN-001` v1.0.0 (2026-09-03) — the authoritative content reference for all DDL, file sets, contracts, and budgets cited below |
| Review contract | `ITRGA-REQ-V2-BE-6-PLAN-001` REQ §1.1–§1.11; Pins **P-1…P-7** |
| Roadmap basis | `AXIOM-V2-BE-ROADMAP-001`, Band BE-6 (contract verbatim-verified at review) |
| Executed by | Development Authority (DA), via Operator custody; **all commits belong strictly to the Operator** |

## 1. Scope authorized

**Single package, four units** (per-operator choice preserved to split per unit before work begins if desired):

- **U-1** — Migration `20260903_0046_v2_be6_portfolio_research` (`down_revision = "20260902_0045"`): tables `v2_portfolio_definition` (versioned-immutable; `record_seq`+`supersedes`; `UNIQUE(portfolio_id, record_seq)`; single-value `basis('hypothetical')` CHECK; allocations JSON with declared weights contract; six-class `data_class`; `assumptions` never-empty rule) + `v2_portfolio_risk_report` (immutable; determinism anchor `UNIQUE(portfolio_definition_id, inputs_hash, engine_versions_hash)`; six-state `status`; single-value `basis_label('hypothetical-research')` CHECK; `engine_versions(_hash)`) + **4 guard triggers** + **6 permission grants** (SAL-aligned: admin read/define/compute family SAL-2/SAL-3; operator read-only) + **1 compver seed** (`portfolio_risk_engine = pre-1.0.0`) — all exactly per plan §1.2.
- **U-2** — Risk engine `app/v2/portfolio_research/{__init__,contracts,metrics,scenarios}.py`: pure deterministic pure-function metrics per plan Part 2 (exposures; HHI + top-N; volatility with chi-square CI at the cited level; max drawdown; historical AND parametric VaR reported separately; grouping-not-regression factor shares; deterministic scenario/stress application) — every metric carrying the full risk-metric contract with method citation and typed `insufficient`.
- **U-3** — API `app/v2/portfolio_research/api.py` + one additive mount in `app/v2/api/router.py` + RBAC module additions + model imports (the three enumerated modified files, additive-only): read-only surface + two governed writers (define-portfolio, compute-risk-report) under `/api/v1/v2/portfolio-research/*`; RESEARCH-mode writers; six BE-1 states incl. `denied`.
- **U-4** — Evidence: Delivery Report with requirement map (REQ §1.1–§1.11 item-for-item + roadmap §0 + Pins P-1…P-7), REM-001-class source transcript, Level I API transcript, raw `pytest -v` transcript, **worked-sample annex**, full MD5+SHA-256 per artifact, credential scans.

**Explicitly NOT authorized:** any working-DB application of 0046 (separate sanctioned act with its own instrument, including the obligation inherited from C-2 practice: engine-file re-pins at the application instrument); report preview/export surfaces; any BE-7/BE-8…BE-11 surface; any commit/push; any use of real/historical data classes.

## 2. Terminal state (T-1…T-12) — required, evidence-backed

1. **T-1** — Chain at `20260903_0046 (head)`, single head, exactly one new revision; upgrade reproducible from `20260902_0045`.
2. **T-2** — Both tables exist with exact DDL pins per plan §1.2: column sets, types, CHECKs (incl. the two single-value CHECKs and the 6-class literals identical to 0044/0045), index/UNIQUE names (`uq_v2_pfdef_id_seq`, `ix_v2_pfrisk_def`, `uq_v2_pfrisk_determinism_anchor`); nothing beyond the enumerated columns.
3. **T-3** — The 4 guard triggers exist and **refuse live** with the exact plan-cited messages; v2 trigger census = **32** (28 + 4), enumerated by name.
4. **T-4** — 6 new permission rows with the exact names and SAL/role alignment per plan; global total **41**; forbidden-permission-marker guard green (no account/order/position vocabulary present).
5. **T-5** — compver total **6**; `portfolio_risk_engine = pre-1.0.0` with source hash over the U-2 files; engine-version pins reproduce.
6. **T-6** — Post-migration `alembic check` drift at the new head = **exactly the 9 inherited V1 tokens, zero BE-6 tokens**, itemized (direct runs at both heads).
7. **T-7** — No-touch across 0046: BE-2/BE-4/BE-5 protected state byte-identical at content level (tables/rows/pins), enumerated.
8. **T-8** — Typed-outcome law executed: six states demonstrable incl. `denied`-by-RBAC; typed `insufficient` metric return; as_of no-future refusal; `historical_real`/`live` refusal with typed reasons; `hypothetical-research` label present on every artifact response.
9. **T-9** — Evidence package: Level I API transcript with endpoint path pinned and inline ASSERTs true; raw `pytest -v`: floor **≥ 906, 0 failed** (856 + declared new budget, sum proven) with V1 552 intact; **worked-sample annex recomputed by the ITRGA and equal to engine output** (P-7 execution); REM-001 transcripts with full hashes and reused-V1 pins; credential scans CLEAN.
10. **T-10** — Register impacts staged honestly: `Portfolio Research` + `Risk Research` → IMPLEMENTED at delivery (COMPLETE only via acceptance); risk +2; debt +2 (long-only scope; grouping-not-regression); serialization per the 30.x convention.
11. **T-11** — Boundaries hold in shipped code: no recommendation/action/hedge/rebalance construction anywhere in band modules (construction-token scan); no preview/export surfaces; RESEARCH-only writers; no network in tests.
12. **T-12** — Custody/oversight: no credentials anywhere (the band prompts for none — stated); no Git operations by DA or ITRGA; review authority is **full-depth**: errors are issued as corrections and the DA answers by corrected plan/report; **anything contrary to the roadmap or overall design is ruled out** until a sufficient corrected plan/report is presented.

## 3. Pins in force (P-1…P-7)

P-1…P-5 as carried from BO-V2-BE-5-001 (versioned-immutable lineage with `supersedes` C-1 vocabulary; determinism anchors on immutable artifacts; typed permanent outcomes + six-class data honesty; computation provenance via compver; structural proof over vocabulary), plus **P-6** (hypothetical-only separation proven structurally — CHECKs/schema/response probes, never assertions) and **P-7** (independent ITRGA recomputation against the worked-sample annex, expected values pinned at stated precision).

## 4. Delivery-report obligations (map)

Every REQ §1.1–§1.11 item, every roadmap §0 contract element, and every Pin P-1…P-7 -> evidence citation; honest disclosures preserved (long-only; grouping-not-regression; normality assumption; pipeline-validation tier; NOT-PROVEN for real-market conclusions); known-limitations and debt rows registered.

**ISCRIVED as BUILD ORDER BO-V2-BE-6-001, Band BE-6 — Portfolio and Risk Research Domain. We don't guess. We prove.**
