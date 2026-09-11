# AXIOM — BUILD ORDER B-01
## Data Foundation (Pipeline Execution & Validation-Tier Separation)

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-01` |
| Programme | Backend Operationalization (reconciled v2) |
| Authorizing authority | **Operator** (directive of 2026-08-19: "authorized") |
| Predecessor | `BO-B-00` — **APPROVED WITH OBSERVATIONS** (ITRGA_DETERMINATION_B-00_FINAL.md) |
| Governing documents | `BACKEND_ROADMAP_v2.md` §B-01 · `07_ML_SPEC.md` · `05_SYSTEM_ARCHITECTURE.md` (v2.0) · `17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 1. Objective

Make the **data foundation actually run** — not merely exist as code. The W2 dataset/snapshot/split/feature pipeline is written but has never been executed against a corpus: the `dataset_snapshots`, `dataset_split_manifests`, `feature_records`, `feature_definitions`, `feature_quality_reports`, and related tables are **empty**. This order produces governed, as-of-bounded, lineage-bearing data artifacts that B-02 (ML research) will consume.

It also installs, as a **binding rule for the entire programme**, the validation-tier separation mandated by the Operator (v2 roadmap §B-01.1a): synthetic data may prove the pipeline works, but may never silently substantiate a research conclusion.

This order produces **no analytical output** (no models, signals, intelligence). It produces data artifacts and proves the pipeline.

---

## 2. Scope (in scope)

### B-01.1 — Honest historical corpus ingestion
- Ingest a multi-market corpus through the existing ingestion seam (`POST /api/v1/ingestion/sample`, `POST /api/v1/ingestion/csv`, or a governed programmatic path).
- Populate `market_series_metadata`, ingestion runs, quality scores, and provenance for every series.
- **Data class rule (binding):** the corpus may be (a) real historical data, or (b) explicitly-labeled **synthetic** data. Either is acceptable for *this* unit because this unit is **pipeline validation** — but every series must carry a truthful source label (`historical:real` vs `synthetic` vs `simulated`), and no synthetic series may ever be presented or persisted without that label.
- **Corpus sufficiency note:** the current sample corpus (two small H1 CSVs) is minimal. The DA may (and, to make B-01.2/B-01.3 meaningful, should) extend the corpus — e.g. ingest the simulated/seed feed's persisted candles with correct `live:simulated`/`seed:synthetic` provenance, or a larger labeled synthetic corpus. **Whatever is used must be honest and labeled.**

### B-01.1a — Validation-tier separation (binding programme rule)
- Formalize and enforce the four tiers as a documented, referenced rule:
  | Tier | Data required | Purpose |
  |------|---------------|---------|
  | Pipeline validation | Synthetic permitted | Prove the pipeline works |
  | Research validation | Real historical data | Substantive market conclusions |
  | Economic validation | Real historical + realistic cost assumptions | Economic viability |
  | Generalization validation | Real hold-out data | Cross-market robustness |
- Every downstream ML/report unit must declare its tier and data class. A synthetic corpus may **only** close pipeline-validation units. This order is pipeline-validation tier.

### B-01.2 — Dataset snapshots & temporal splits (executed)
- Execute the snapshot builder (`DatasetService.freeze_from_*`) over the ingested corpus → populate `dataset_snapshots`, `dataset_series_members`, `dataset_lineage_records`.
- Execute the temporal split engine (`split()` / `validate_temporal_split()`, `validate_label_horizon()`) → populate `dataset_split_manifests`.
- **Invariants (binding):** random splits rejected; label-horizon leakage rejected; splits are as-of-bounded and no-look-ahead.

### B-01.3 — Feature store population (executed)
- Register built-in feature definitions (`register_builtin_definitions()`).
- Compute and store features (`compute_and_store()`) over the corpus → populate `feature_records` + `feature_quality_reports`.
- **Invariant (binding):** the causal / no-symbol-identity feature boundary holds — no feature may encode symbol identity (ML Spec §Market-Agnostic Learning).

---

## 3. Exclusions (out of scope — do NOT do)

- **No** model training, model artifacts, experiments, or promotion (that is B-02).
- **No** inference, signals, alerts, or intelligence reports (B-03/B-04/B-05).
- **No** assistant work (B-06).
- **No** frontend changes.
- **No** research/economic/generalization **conclusions** — this unit is pipeline validation only; it may not claim market validity for any synthetic series.
- **No** real market-data provider integration (the simulated feed remains simulated).
- **No** gate-opening, actuation, broker/account/trading/execution state.
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model — see §9).
- **No** reopening of previously closed experiments.

---

## 4. Exact deliverables

1. An ingested, provenance-labeled multi-market corpus with `market_series_metadata` + ingestion-run records.
2. The validation-tier separation rule, documented (a short Markdown addition or ADR-style record, e.g. under `backend/docs/`), and referenced by every subsequent unit.
3. Populated `dataset_snapshots` + `dataset_series_members` + `dataset_lineage_records`.
4. Populated `dataset_split_manifests` (temporal, no-look-ahead, leakage-free).
5. Populated `feature_records` + `feature_quality_reports` + registered `feature_definitions`.
6. A **Delivery Report** (see §10), with deviation register.

---

## 5. Dependencies

- **Upstream:** BO-B-00 (closed). The provenance/landing protocol (R1–R6) binds this delivery.
- **Downstream:** B-02 (ML research) consumes the artifacts produced here. B-01.1a's tier rule governs B-02's data requirements.

---

## 6. Allowed files / components

- `backend/app/ml/dataset/*` (service, snapshot builder, split engine, chronology guard, metadata, provider adapters).
- `backend/app/ml/features/*` (store, definitions).
- `backend/app/api/routes/ingestion.py` and `backend/app/ingestion/*` (only if a governed corpus-ingestion path must be added/fixed).
- `backend/app/models/*` and `backend/app/db/models/*` (only for read/write alignment of the above — no new schema migrations unless strictly required and justified).
- `backend/tests/**` (new/churn tests for snapshots, splits, features, and the tier rule).
- `backend/sample_data/**` and `backend/tests/fixtures/**` (corpus data, labeled).
- New documentation file(s) for the tier rule and any ADR.
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security constraints (binding)

- No secrets/credentials in any changed file or report.
- No new network surface; no new endpoints beyond what §6 permits; no weakening of `17_INSTITUTIONAL_SECURITY_STANDARD.md`.
- Any new ingestion path must be operator-authenticated and path-allowlisted (existing `ALLOWED_ROOTS` discipline must be preserved, not loosened).
- Synthetic data must remain labeled end-to-end (persisted `source`/provenance fields; never silently relabeled real).

---

## 8. Acceptance criteria (per sub-unit)

### B-01.1
- [ ] Corpus ingested; every series has a truthful source label and provenance.
- [ ] `market_series_metadata` + ingestion-run rows populated; `ingestion/stats`, `ingestion/runs`, `candle-counts` return non-zero with labels.

### B-01.1a
- [ ] Tier rule documented and stated as binding; each tier's required data class enumerated.
- [ ] This unit is explicitly declared **pipeline-validation** tier with synthetic data permitted (and any synthetic series labeled as such).

### B-01.2
- [ ] `dataset_snapshots` + members + lineage rows populated with content hashes.
- [ ] `dataset_split_manifests` populated; splits temporal, as-of-bounded, no-look-ahead.
- [ ] Evidence that random splits and label-horizon leakage are rejected (guard tests/transcripts).

### B-01.3
- [ ] `feature_definitions` registered; `feature_records` populated with lineage; `feature_quality_reports` present.
- [ ] No symbol-identity feature present (market-agnostic boundary proven).

---

## 9. Evidence requirements (custody model — reconciled per OBS-B00-2)

**Standing evidence model, going forward:** the Operator has ratified the detached-artifact custody model in BO-B-00 (patch artifact + evidence logs relayed through the review channel; no DA commits/pushes; repository is Operator-controlled). This order therefore **replaces BO-B-00 §9's "commit ref + diff" wording** with the ratified model:

> The DA works in its own workspace and submits, through the review channel: (1) a patch artifact (sha256) that applies cleanly to the verified chain via `git apply --check` in a pristine clone, (2) per-file content SHAs, and (3) evidence logs with hashes. **Every hash declared in the Delivery Report must correspond to an artifact actually transmitted** (protocol R3 — no "ATTACHED" claim for an unsent artifact).

The DA must supply:

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed test output (new/changed tests) | Level II | run transcript |
| Ingestion evidence (`ingestion/runs`, `stats`, `candle-counts` with labels) | Level I | API probe output |
| Snapshot/split/feature row-count evidence (DB or read-API) | Level I | query/probe output |
| Tier-rule document content | Level III | document |
| Delivery Report | Level III | §10 structure |

**Transmission completeness (R3) is itself an acceptance criterion:** the DA verifies mechanically that every declared hash resolves to a transmitted artifact before submitting.

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Corpus description and source labels (real vs synthetic vs simulated, per series)
4. Tier declaration for this unit (pipeline validation)
5. Snapshot/split/feature evidence (executed, with row counts)
6. Leakage/random-split rejection evidence
7. No-symbol-identity boundary evidence
8. Test evidence (executed)
9. Deviations register
10. Known limitations / remaining risk
11. Technical-debt entries (if any)

---

## 11. Rollback / containment

- Data artifacts are additive (new rows in existing tables). No schema migration is authorized by default; if one is strictly required it must be flagged and justified in the Delivery Report before ITRGA will consider it in-scope.
- Revert is: stop ingestion, drop/rollback any newly written rows, revert the patch.
- No data produced here affects production (none is produced; Gate CLOSED).

---

## 12. Completion condition

Complete when: all §8 acceptance criteria are met, evidence (§9) is transmitted and verified, the Delivery Report is submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is **not** evidence of completion and does **not** close this unit.

**Next authorization state:** upon ITRGA approval of B-01, the next bounded Build Order (B-02, ML Research Executed) may be issued. Nothing downstream is authorized by this order.

---

**End of Build Order B-01**
