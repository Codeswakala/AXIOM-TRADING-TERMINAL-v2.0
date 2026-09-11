# AXIOM V2 — Capability Maturity Registry

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-GOV-MAT-001 |
| Status | Active |
| Version | 1.6.0 |
| Date | 2026-09-07 (BE-11 campaign closeout — ITRGA-CAMPAIGN-BE11-CLOSE-001) |
| Author | Development Authority (DA) |
| Build Order | BO-V2-BE-0-001 |

---

## Maturity States

| State | Definition |
|-------|------------|
| DESIGNED | Design plan, specification, or governance document exists |
| IMPLEMENTED | Code exists and compiles |
| TESTED | Tests pass |
| VERIFIED | Independent verification complete |
| APPROVED | ITRGA approved |
| AUTHORIZED | Operator authorized for use |
| PRODUCTION_CERTIFIED | Production readiness certified |

**Note:** BE-0 is a documentation/governance band. BE-0 artifacts are governance documents, not code. They are classified as **DESIGNED** (document exists and is complete) rather than **IMPLEMENTED** (which requires code). Document completion is tracked in the artifact-status column.

---

## V2 Capability Registry

| Capability | Domain | Band | Maturity | Artifact Status | Notes |
|------------|--------|------|----------|-----------------|-------|
| V2 Governance Framework | Core | BE-0 | DESIGNED | ✅ Complete | Governance document |
| V2 Provenance Tracking | Core | BE-0 | DESIGNED | ✅ Complete | Governance document |
| V2 Amendment Register | Core | BE-0 | DESIGNED | ✅ Complete | Governance document (empty) |
| V2 Architecture Principles | Core | BE-0 | DESIGNED | ✅ Complete | Governance document |
| V2 Risk Register | Core | BE-0 | DESIGNED | ✅ Complete | Governance document |
| V2 Technical Debt Register | Core | BE-0 | DESIGNED | ✅ Complete | Governance document |
| V2 ADR Convention | Core | BE-0 | DESIGNED | ✅ Complete | Governance document |
| V2 Capability Maturity Registry | Core | BE-0 | DESIGNED | ✅ Complete | This document |
| V2 Current State | Core | BE-0 | DESIGNED | ✅ Complete | Governance document |
| V2 Programme Charter | Core | BE-0 | DESIGNED | 📝 Draft | DA draft; Operator approval pending |
| V2 Core Domain Primitives | Core | BE-1 | DESIGNED | — | Not yet designed in detail |
| V2 Audit/Lineage Contract | Core | BE-1 | DESIGNED | — | Not yet designed in detail |
| V2 Mode Framework | Core | BE-1 | DESIGNED | — | Not yet designed in detail |
| V2 Feature Flags | Core | BE-1 | DESIGNED | — | Not yet designed in detail |
| Market Data Abstraction | Market Data | BE-2 | DESIGNED | — | |
| Data Quality Framework | Market Data | BE-2 | DESIGNED | — | |
| Provider Adapter Interface | Market Data | BE-3 | DESIGNED | — | |
| Market Context Engine | Intelligence | BE-4 | **COMPLETE** | ✅ Complete | ITRGA-DET-V2-BE-4-FINAL-001 (2026-09-02); pipeline-validation tier; real-data validation = recorded residual |
| Chart Intelligence | Intelligence | BE-4 | **COMPLETE** | ✅ Complete | ITRGA-DET-V2-BE-4-FINAL-001 (2026-09-02); browser evidence = recorded residual (FE/X-01 gate) |
| ML Research Expansion | ML | BE-5 | **COMPLETE** | ✅ Complete | ITRGA-DET-V2-BE-5-FINAL-001 + ITRGA-DET-V2-0045-APPLY-001; granted by ITRGA-DET-V2-BE-5-ACCEPT-001 §2 (2026-09-02) |
| Signal Architecture V2 | ML | BE-5 | **COMPLETE** | ✅ Complete | same — ACCEPT-001 §2 (2026-09-02) |
| Portfolio Research | Portfolio | BE-6 | **COMPLETE** | ✅ Complete | ITRGA-DET-V2-BE-6-FINAL-001 (verdict C full-verify); granted by ITRGA-DET-V2-BE-6-ACCEPT-001 §2 (2026-09-03) |
| Risk Research | Portfolio | BE-6 | **COMPLETE** | ✅ Complete | same — ACCEPT-001 §2 (2026-09-03) |
| Backtesting Engine | Simulation | BE-7 | **COMPLETE** | ✅ Complete | Granted by ITRGA-ACC-V2-BE-7-001 §4 (2026-09-04); delivery BO-V2-BE-7-001 + AXIOM-V2-BE-7-DR-001 v1.0.1; CR-V2-BE-7-001 closed |
| Historical Replay | Simulation | BE-7 | **COMPLETE** | ✅ Complete | same — ACC-001 §4 (2026-09-04) |
| Research Job Queue | Simulation | BE-7 | **COMPLETE** | ✅ Complete | same — ACC-001 §4 (2026-09-04) |
| Paper Trading Engine | Paper | BE-8 | **COMPLETE** | ✅ Complete | Build phase COMPLETE by ITRGA-ACC-V2-BE-8-INT-001; run/act phase sealed ITRGA-V2-BE8-0048-CLO-SEAL-001 (2026-09-05); 0048 applied & verified |
| Paper Account Model | Paper | BE-8 | **COMPLETE** | ✅ Complete | same — CLO/SEAL 2026-09-05 |
| Pre-Trade Risk Gateway | Paper | BE-8 | **COMPLETE** | ✅ Complete | same — CLO/SEAL 2026-09-05 |
| Broker Adapter | Broker | BE-9 | **COMPLETE — OPERATING** | ✅ Complete | ITRGA-CAMPAIGN-BE9-CLOSE-001 (2026-09-06): fielded head 20260905_0049; compver bre-1.0.0 `b0008cb9…` live on working DB; first routine sync complete under investor posture |
| Broker Reconciliation | Broker | BE-9 | **COMPLETE — OPERATING** | ✅ Complete | same — first-sync reconcile clean; read_only_login_asserted true; F-E1-02 CLOSED |
| Account Context Intelligence | Intelligence | BE-10 | **COMPLETE — OPERATING** | ✅ Complete | ITRGA-CAMPAIGN-BE10-CLOSE-001 (2026-09-06): fielded head 20260908_0050 (sha-after 90660b5d…f9de); ace-1.0.0 `532ef0ce…` verified fielded-live; census 76/65/12; 12 sealed map rows onboard; first-read witness wire==fielded digest; empty matrix = honest flat account |
| Paper-Execution Bridge | Paper | BE-11 | **COMPLETE — OPERATING (SEEDS ARMED)** | ✅ Complete | ITRGA-CAMPAIGN-BE11-CLOSEOUT-001 (2026-09-07): fielded head **20260909_0052**; seeds 5/5 (4× tolerance 125.00 USD + staleness 48h); pbr-1.0.0 `4c243435…178b` byte-still, live==db; census 78/69/13; suite floor 1,163; first-read sworn (401 arm; ledger []; drift refuse-flip armed at 0052; intent 403 mode-arm — RESEARCH deployment); fill-sim absent non-revival; reference prices operator-cited only (D-B11-CITE) |
| Bridge Drift Intelligence | Paper | BE-11 | **COMPLETE — OPERATING (SEEDS ARMED)** | ✅ Complete | same — closeout 2026-09-07; 125/250 USD structural 2× law on 4 compared fields; comparison_state armed at 0052; verdict-iff + guard pair live on the fielded lineage |
| Execution Gateway | Execution | BE-12+ (renumbered per ruling (b), REQ-V2-BE-11-001 header) | DESIGNED | — | roadmap execution family renumbers at its future commissioning |
| Order Management | Execution | BE-12+ | DESIGNED | — | same |
| Position Management | Execution | BE-12+ | DESIGNED | — | same |
| AI Provider Adapter | AI | BE-13 (renumbered per roadmap amendment A-2026-09-06) | DESIGNED | — | |
| AI Safety Framework | AI | BE-13 (same amendment) | DESIGNED | — | |

---

**End of Capability Maturity Registry**
