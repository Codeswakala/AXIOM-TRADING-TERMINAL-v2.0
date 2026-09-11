# ITRGA-PRV-V2-BE-5-PLAN-001 — Plan Review & Scope Assessment: AXIOM-V2-BE-5-DA-PLAN-001

| Item | Value |
|---|---|
| Reviewer | ITRGA (succession ITRGA-REA-V2-SUCCESSION-001) |
| Date | 2026-09-02 (Africa/Nairobi) |
| Instrument under review | `AXIOM-V2-BE-5-DA-PLAN-001` v1.0.0, Development Authority, 2026-09-02 (received via the Operator custody channel, 2026-09-02) |
| Requesting instrument | ITRGA-REQ-V2-BE-5-PLAN-001 |
| Authority | Operator authorization of Band BE-5, 2026-09-02 (OD number to be recorded by the Operator on the determination chain) |
| Chain position | BE-0…BE-4 closed (BE-4 by ITRGA-DET-V2-0043-APPLY-001). Next chain migrations: 0044, 0045 |
| Role of this document | ITRGA plan review **and** scope assessment (analog of `ITRGA_ASSESSMENT_V2_BE-4_SCOPE_V1.md`), feeding the Build Order |
| **Verdict** | **APPROVED FOR BUILD-ORDER PROPOSAL — subject to five Review Pins (P-1…P-5). The pins amend DDL/mechanics; they do not require re-planning. The DA addresses them in the Build Order evidence plan directly.** |

Channel note (recorded): the Operator's relay message called the attachment a "delivery report"; the attached artifact is the DA's DESIGN PLAN (status: SUBMITTED FOR ITRGA PLAN REVIEW). Recorded for chain accuracy; no action.

---

## Part A — Request-checklist compliance (ITRGA-REQ-V2-BE-5-PLAN-001 §1.1–§1.9)

| Checklist item | Plan coverage | Judgment |
|---|---|---|
| §1.1 decomposition/units, exact DDL, guards, seeds, downgrade, drift declaration | Part 1: 6 units; exact DDL for 0044/0045; exact refusal messages; SAL seeds + totals; symmetric downgrades; per-unit drift declarations (9 inherited V1 tokens, zero `v2_*`), models registered same-unit (PG-002 lesson cited) | COMPLIANT (amended by P-1/P-2/P-5 totals) |
| §1.2 contract set (registry evolution; eligibility/calibration/freshness/economic/rollback; shadow/champion/challenger; signal families; withheld/expired/refused; reports/diagnostics) | Parts 2–5, bound section-by-section to `07_ML_SPEC.md` | COMPLIANT (FP-1/FP-2 resolved at Part B; champion scope pinned by P-3) |
| §1.3 hard boundaries | Part 6, items 1–7 verbatim-in-substance; data-class first-landing restriction to `synthetic`/`simulated` with typed refusals for `historical_real`/`live` until corpus track | COMPLIANT — notably disciplined on data honesty |
| §1.4 mode/audit/security | Part 7: BE-1 contract columns, audit event inventory, redaction gate, "no credential" stated | COMPLIANT |
| §1.5 test plan | Part 8: fail-first; floor 789→847 projection (58 tests itemized per unit); no position-based assertions (PGF-012 honored); regression no-touch group over BE-3/BE-4 state | COMPLIANT (budget re-states at ≥ +64 under P-1/P-2/P-5) |
| §1.6 evidence plan | Part 9: content-exact DB/API probes recomputable by ITRGA; RSR-1/RSR-2 formats; REM-001 transcript; hash manifest; credential scan | COMPLIANT (values pinned by P-5) |
| §1.7 register impacts | Part 10: maturity rows, risk additions, three honest tech-debt additions | COMPLIANT |
| §1.8 boundaries vs BE-6/BE-7/corpus track | Part 11: explicit, with deferral mechanics and honest "NOT PROVEN" declaration for real-market claims | COMPLIANT |
| §1.9 package size/review volume | Part 12 | COMPLIANT |

## Part B — Independent verification performed by the ITRGA (not restated from the plan)

| Claim in plan | ITRGA verification | Result |
|---|---|---|
| Reused V1 evaluator services exist | `app/ml/validation/service.py`, `app/ml/calibration/service.py`, `app/ml/economic/service.py` present and hash-stable in tree | VERIFIED |
| Cited spec sections exist | `07_ML_SPEC.md` sections present: Statistical Validation, Economic Validation, Model Registry, Drift Monitoring, Continuous Learning, Deployment Policy, Research Integrity | VERIFIED |
| Redaction + forbidden-marker guards exist | `app/v2/audit/redaction.py` present; `V2_FORBIDDEN_PERMISSION_MARKERS` present (`app/v2/rbac/permissions.py`) | VERIFIED |
| Router mount point | `app/v2/api/router.py` present; additive-mount pattern matches BE-4 | VERIFIED |
| SAL convention | `app/v2/rbac/permissions.py` SAL map confirms read=SAL-2, write/decide=SAL-3 pattern the plan's levels align with | VERIFIED |
| Current totals underpinning plan arithmetic | `v2_permission` total 27 and 18 v2 triggers confirmed on the live operator console (0043 transcripts, ITRGA-DET-V2-0043-APPLY-001) | VERIFIED |
| Lineage model exists | `app/db/models/v2_lineage_record.py` present | VERIFIED |
| Rewrite avoidance | Plan is additive-overlay; V1 tables explicitly not altered | ACCEPTED (matches charter reuse law) |

## Part C — Review Pins (mandatory amendments, embedded in the Build Order)

**P-1 — Governance-record mechanics: FULL IMMUTABILITY + ROW VERSIONING (resolves the DA's FP-1).**
The proposed `v2_ml_governance_record` must be fully immutable, consistent with the V2 immutability law applied uniformly across this band (lifecycle events, signal records, report tables). Amend the 0044 DDL: add `record_seq INTEGER NOT NULL`; replace `UNIQUE (model_artifact_id)` with `UNIQUE (model_artifact_id, record_seq)`; add `superseded_by String(36) NULL` (id of the superseding record row); remove `updated_at_event_id`; "current" governance state of an artifact = row with the greatest `record_seq`. Add trigger `v2_ml_governance_record_immutable_update` with the exact refusal message `V2 ML governance records are immutable; UPDATE prohibited`, alongside the already-planned delete guard. Rationale: a mutable projection was the only mutable domain state proposed in the band; versioning preserves the current-state read shape at a small read cost and eliminates the silent-UPDATE risk class by construction rather than by writer discipline alone.

**P-2 — Diagnostics: DEDICATED ARTIFACT TABLE (resolves FP-2).**
Add `v2_ml_diagnostic_report` to migration **0044** (it belongs to the ML-governance overlay, not to the signal unit): the full 0043 report-table pattern — content-hash determinism anchor, `engine_versions` + `engine_versions_hash`, `created_from_inputs_hash`/`input refs` JSON, mode/actor/correlation/created_at, immutable `update`/`delete` triggers with exact messages `V2 ML diagnostic reports are immutable; UPDATE prohibited` / `…DELETE prohibited`; permission seeds `v2.research.ml_diagnostics.read` for admin and operator. Diagnostics-as-event-payloads-only is rejected: every material result must be an identifiable, immutable artifact with stable id, per the traceability invariant and the BE-4 report architecture. U-5 accordingly becomes services + read projections over this table (its budget shape is unchanged).

**P-3 — Champion scope columns explicit.**
Add `model_type String(64) NOT NULL` and `instrument_class String(64) NOT NULL` to the governance record (the at-most-one-`champion` rule the plan itself introduces otherwise references fields that do not exist). Enforcement mechanics (declared, not ambiguous): writer check + dedicated test over the current-row projection; DB-level partial unique indexes cannot span versioned rows and are NOT part of the mechanism.

**P-4 — Computation-version seeds only for co-delivered engines.**
Mirroring the BE-4 OBS-1 rule: `v2_computation_version` rows are seeded only for engine code delivered in the SAME package as the migration that seeds them. 0044 seeds `ml_governance_engine = mge-1.0.0` (delivered with U-2 in package 1); 0045 seeds `signal_engine = sge-1.0.0` (delivered with U-4 in package 2). Source hashes are pinned at delivery from the implementation transcript; the ITRGA recomputes independently (compver-pin pattern). No compver row may precede or follow the package boundary of its engine.

**P-5 — Post-unit expectation values pinned for the BO evidence plan (supersedes the plan's arithmetic after P-1/P-2/P-4).**

| measure | before | after 0044 | after 0045 |
|---|---|---|---|
| v2 trigger names (exact set enumerated at evidence time) | 18 | **24** | **28** |
| `v2_permission` rows | 27 | **34** | **35** |
| `v2_computation_version` rows | 3 | **4** | **5** |
| `alembic check` drift | 9 inherited V1 tokens | unchanged | unchanged |

New-test budget re-stated at **≥ +64** (floor projection **≥ 853**), reflecting P-1's added version/guard tests, P-2's diagnostic-report tests, and P-3's champion-scope tests. Fail-first and the no-touch regression group remain binding.

## Part D — Accepted without amendment

- Threshold constants (calibration bound, freshness bound) pinned at implementation FROM the V1 service configs with explicit citations into `decision_basis` — the DA correctly refuses to invent numbers in the plan; the Build Order must carry the citations requirement.
- `state_reason`/`uncertainty` conditional-nullability enforced by writer + test (not DDL) — accepted, with the column comments carrying the contract.
- First-landing data-class restriction (`synthetic`/`simulated` only; `historical_real`/`live` refused with typed reasons until the corpus track) — accepted verbatim; this is the band's honesty spine.
- Delivery packaging: the DA's two-package proposal (U-1+U-2, U-3+U-4) plus a closure package (U-5+U-6) is endorsed. One Build Order may cover all units at the Operator's choice; the evidence discipline is identical either way.
- Working-DB application of 0044/0045 expressly out of band scope (separate sanctioned acts under the 0043 precedent) — recorded as the governing posture.

## Part E — Non-blocking observations

- Path precision note: the permission/seed register file is `app/v2/rbac/permissions.py` (the plan writes `rbac/permissions.py` in one place; identity verified).
- OBS-9 (BE-4 record) remains the Operator's administrative item; untouched by BE-5.
- The plan's honest Part 13 limitations are adopted into this review's record (real-market claims NOT PROVEN until the corpus track exists).

## Part F — Next steps

1. Operator approval of this review (or correction items).
2. Build Order issuance (single BO covering U-1…U-6, or per-package — Operator's choice; DA evidence plan must embed P-1…P-5 and the P-5 value table).
3. DA implementation under fail-first discipline → tests + Level-I evidence → Delivery Report with requirement mapping.
4. ITRGA battery/verification of any sanctioned production act in the 0043 pattern if and when the Operator directs working-DB application of 0044/0045.

Standing rules restated: this review authorizes no code change, no repository write, **no commits by anyone but the Operator**, no database write, and no execution.

— ITRGA, 2026-09-02
