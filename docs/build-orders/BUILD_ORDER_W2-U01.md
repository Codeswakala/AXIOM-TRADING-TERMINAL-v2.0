# AXIOM BUILD ORDER — W2-U01

## ML Research: Canonical Dataset Architecture + Chronology & Data-Integrity Guard

**Build Order ID:** W2-U01
**Wave:** 2 — Machine Learning Research Framework · **Unit:** 01 (first Wave-2 unit)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-13
**Authorized By:** ITRGA, following **Wave 2 Design Plan ACCEPTED** (`docs/ITRGA_REVIEW_WAVE2_DESIGN_PLAN.md`)
+ operator Wave-2 authorization + **LOCKED DECISION D-W2-001 (Option A)**.

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Build the **foundation layer of the ML Research Framework**: (a) a **Canonical Dataset Architecture**
(immutable, versioned, provenance-tracked, reproducible dataset snapshots that can *never* be anonymous),
and (b) a **Chronology & Data-Integrity Guard** enforced as a **testable contract** that refuses
forward-dated / leaked / out-of-order / synthetic records from authoritative training data.

Per operator directive and the accepted design plan, these two layers are the **hard gate** before any
model work: **no model training or evaluation unit is reviewable until W2-U01 (and U02–U05) are Level-I
proven on the target.** This unit contains **no model, no features-for-training beyond schema/contracts,
and no execution** — it is pure data-integrity infrastructure.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No model, no training, no inference, no prediction.** This is dataset + chronology infrastructure.
- ❌ **No execution / broker / order path.** W1-U03 Constitutional Governance Gate stays **CLOSED**; the
  External Integration System is not used (05 v2.0 §15; roadmap Wave-6 gate).
- ❌ **No symbol identity as a learned feature** (D-W2-001 / `07_ML_SPEC` §Market-Agnostic Learning).
  Symbol/provider/market are **metadata for governance/evaluation partitions only** — never ordinary
  predictive identity. (Enforcement matures in W2-U03; W2-U01 must not introduce a contrary pattern.)
- ❌ **No direct DB reach-around.** ML consumes market data via an approved query contract
  (`MarketDataQueryPort`-style), not ad-hoc ORM scattered through ML modules (05 v2.0 §16; plan §3.3).
- ❌ **No anonymous dataset.** Every snapshot carries the full `07_ML_SPEC` §Dataset Governance field set.
- ❌ **No silent data mutation.** Bad records are **quarantined with a reason**, never silently dropped;
  out-of-order records in an authoritative series are **not silently re-sorted** (see R-1).
- ❌ **No secrets/PII in logs/telemetry/dataset dumps** (05 v2.0 §77; W1-U02 redaction standard).
- ❌ **No regression** of any approved capability (Wave-0/1). Prove via full suite + parity smoke.
- ✅ **Preserve:** advisory/research-first, single-uvicorn, canonical v2.0 boundaries, tz-aware UTC,
  observability (structured logs + correlation + redaction + metrics), and all prior hardening.

---

## 3. Scope — Components A–F

### Component A — Canonical Dataset Architecture (`07_ML_SPEC` §Dataset Governance / §Data Pipeline)
- Alembic-migrated PostgreSQL tables per the design plan §5.2 (conceptually `dataset_snapshots`,
  `dataset_series_members`, `dataset_lineage_records`, `dataset_quarantine_records`) — final names/columns
  at DA discretion, but every snapshot **must carry the 8 mandatory fields**: dataset identifier, market,
  timeframe, date range, source, feature version, creation timestamp, quality score. **"No anonymous
  dataset may enter production research."**
- **Immutability + versioning:** deterministic ordering `(market_class, provider, symbol, timeframe,
  open_time, source, id)`; canonical serialization; **SHA-256 `content_hash`** over membership + feature
  version; status `draft → frozen` only after chronology/quality gates pass; **a frozen snapshot is
  immutable — any change creates a new version, never mutates.**
- **Provenance/lineage:** bidirectional (source candle → normalized → feature row → snapshot row →
  experiment input, and back). Every membership row traceable to source candle(s) + feature-def version.

### Component B — Chronology & Data-Integrity Guard (operator directive §1; plan §6)
Deliver the guard as a **formal, testable contract**, running at **all four stages** (ingestion, dataset
construction, training-set generation, experiment execution). Minimum rule set:
- tz-aware UTC on all dataset/feature timestamps;
- **monotonic non-decreasing `open_time`** within each `(market_class, provider, symbol, timeframe)` series
  after dedup;
- **no future record** (`open_time <= as_of_time` and `<= ingestion_finished_at` where applicable);
- **`source=seed:synthetic` excluded** from authoritative training sets; **forward-dated
  `source=live:simulated` excluded/quarantined** (OBS-1);
- **temporal splits only** — random row splits rejected;
- duplicate policy by natural key `(market_class+provider+symbol+timeframe+open_time+source)`;
- source authority classification (authoritative / simulated / synthetic / unknown).
- **Quarantine, don't drop:** bad records recorded with source id, series key, timestamp, reason code,
  detected stage, detail. Reason codes at least: `FUTURE_OPEN_TIME`, `OUT_OF_ORDER_TIME`,
  `DUPLICATE_NATURAL_KEY`, `SYNTHETIC_SOURCE_NOT_AUTHORITATIVE`, `SIMULATED_FORWARD_DATED`,
  `NAIVE_TIMESTAMP`, `SPLIT_LEAKAGE`, `UNKNOWN_SOURCE_AUTHORITY`, **`LABEL_HORIZON_LEAKAGE`** (R-2).

### Component C — REQUIRED REFINEMENTS from plan review (mandatory)
- **R-1 (HIGH) — no silent re-sorting.** Out-of-order records in an **authoritative** series **default to
  quarantine**. Re-sorting is permitted **only** under a named, per-source policy flag, and when permitted
  it must be **explicit, logged, and recorded in lineage** — never silent. **Test:** an out-of-order record
  in an authoritative series is **quarantined, not reordered.**
- **R-2 (HIGH) — label-horizon / embargo (purge) guard.** Even though W2-U01 trains nothing, the guard +
  split contract must encode the **label-horizon leakage** rule now: no (future) training label's forward
  horizon may overlap the validation/test window; provide an **embargo/purge** parameter. **Test:** a label
  whose horizon crosses the split boundary is rejected (`LABEL_HORIZON_LEAKAGE`). (Split *engine* is
  W2-U04; W2-U01 lands the contract + reason code + a unit-level test of the rule.)
- **R-3 (MEDIUM) — trustworthy time anchors.** `as_of_time` / `ingestion_finished_at` must be **immutable,
  recorded at ingestion, and never derived from query-time wall-clock.** **Test:** a record cannot pass the
  "no future record" check by presenting a self-declared future-safe timestamp; the anchor is authoritative.

### Component D — Approved market-data query contract (05 v2.0 §16; plan §3.3)
- Introduce/adopt a small explicit **`MarketDataQueryPort`**-style contract
  (`list_series` / `get_candles` / `get_source_metadata`) backed by existing candle repositories. ML code
  depends on the port, not scattered ORM. No new top-level market; **Deriv Synthetic Indices modelled as a
  provider adapter under the Synthetic class** (§7.1) — do not create a new market class.

### Component E — Governance, registers, ADRs, residuals
- **ADRs:** *Dataset Snapshot Architecture* and *Chronology Guard Contract* (plan §11.3).
- **`RISK_REGISTER`:** land the pre-listed Wave-2 risks that this unit mitigates — data-leakage/look-ahead
  (Critical → mitigated by guard/split/negative-tests), synthetic-as-real (High → source authority +
  quarantine + OBS-1 closed-forward), dataset-not-reproducible (High → content hash), and add
  label-horizon-leakage.
- **`TECHNICAL_DEBT_REGISTER` / `PROJECT_STATE` / `CHANGELOG`:** record deferrals (features/model → later
  units) and this unit's status.
- **Close LOW Wave-1 residuals opportunistically:** **R-CI-01** (a real remote CI run) and
  **CI-pytest-on-PG alignment** — add a PostgreSQL integration tier now that ML schema arrives (plan §11.4).
- **OBS-1:** with the guard live, OBS-1 transitions from "carried note" to **"enforced by contract"** —
  record the transition.

### Component F — Verification & Delivery
- Full existing suite green (backend baseline **88** / frontend **16**) — 0 failed, no regression — **plus**
  new tests for A–D and the **R-1/R-2/R-3 negative tests**.
- Delivery Report per §5.

### Explicitly OUT of scope (defer to later Wave-2 units)
Feature computation for training (W2-U03), the reproducible snapshot *builder* + split *engine* (W2-U04),
experiment registry (W2-U05), any model (W2-U06+), calibration/economic/statistical validation
(W2-U07/08/09), generalization/drift (W2-U10). No numpy/pandas/scikit-learn adoption in this unit — keep to
stdlib + existing FastAPI/Pydantic/SQLAlchemy/Alembic/PostgreSQL stack (plan §4.3).

---

## 4. Success Criteria (Definition of Done)

- [ ] Canonical dataset schema migrated on **PostgreSQL**; every snapshot carries the 8 `07_ML_SPEC` fields;
      **no anonymous dataset** possible.
- [ ] Frozen snapshot is **immutable + content-hashed**; rebuild yields identical hash under unchanged
      inputs; bidirectional lineage present.
- [ ] Chronology guard runs at all four stages as a **testable contract**; bad records **quarantined with
      reason**, not dropped.
- [ ] **Negative tests pass (the core proof):** forward-dated → quarantined; out-of-order in authoritative
      series → **quarantined not re-sorted (R-1)**; `seed:synthetic` → excluded; forward `live:simulated` →
      excluded; random split → rejected; naive timestamp → rejected; **label horizon crossing split →
      rejected (R-2)**; spoofed future-safe timestamp cannot bypass the anchor **(R-3)**.
- [ ] Market data consumed via an **approved query port** (no DB reach-around); **Deriv = provider adapter
      under Synthetic** (no new top-level market).
- [ ] No model/training/inference; no execution; broker gate CLOSED; no symbol identity as learned feature;
      no secrets in logs/dumps.
- [ ] ADRs + registers synced; R-CI-01 + CI-pytest-on-PG addressed; OBS-1 transition recorded.
- [ ] Full suite green (88/16 + new tests); no regression; conforms to 05 v2.0 (§16/§77) + `07_ML_SPEC`
      (§Dataset Governance / §Data Pipeline / §Research Integrity).

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Per the reinforced standard (sandbox-green ≠ target-proven; a failing test/leaked record in evidence is a
finding, not a footnote). Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **Operator test console** (raw, `collected N`): backend `pytest` **≥88 + new tests, 0 failed**;
   frontend `vitest 16`; `ruff` clean; `tsc`/build clean.
2. **Migration evidence:** clean `DROP SCHEMA` → `alembic upgrade head` on `PostgresqlImpl` including the
   new dataset tables (new head id shown).
3. **Chronology negative-test evidence (the headline):** the `-vv` run showing each guard negative test
   PASS — especially **R-1 (quarantine-not-resort), R-2 (label-horizon-leakage rejected), R-3 (spoofed
   timestamp cannot bypass)** — plus a **quarantine-table row** written with a reason code for a bad record.
4. **Reproducibility evidence:** build/freeze a snapshot twice → identical `content_hash`; show a frozen
   snapshot rejecting mutation (new version created instead).
5. **No-anonymous-dataset evidence:** an attempt to create a dataset missing a mandatory field is rejected.
6. **Port/containment evidence:** market data obtained via the query port; a grep-style check (R7: show
   command + output) that ML modules do not scatter raw ORM / do not introduce a new top-level market /
   do not emit symbol identity as a feature.
7. **CI evidence:** the pipeline green (ideally the owed **remote** run — R-CI-01) incl. the new PG
   integration tier; fail-closed.
8. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
9. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Clean architecture / bounded context / single ownership (ML Research System owns ML tables); dependency-
inward, interface-based (query port), no business logic in infra (05 v2.0 §16); **no secrets in
telemetry** (§77); tz-aware UTC everywhere; **scientific integrity** — leakage/look-ahead/synthetic-as-real
prohibited and **proven prohibited by negative tests** (`07_ML_SPEC` §Research Integrity; R18); every change
in the registers (R20); cross-platform (Windows + docker/PostgreSQL).

---

## 7. Process
Implement → internal verify (suite + negative tests + reproducibility) → doc sync (PROJECT_STATE +
registers + 2 ADRs) → Delivery Report with §5 evidence (operator-run, green, bad-records-refused, no failing
tests) → **submit to ITRGA** → independent review → corrections if required → approval → next Build Order
(W2-U02). The DA does not self-approve, does not self-authorize the next unit, and does not open the gate.

---

## 8. Priority Guidance (if staged)
**A (dataset schema + governance fields) → B (chronology guard contract + quarantine) → C (R-1/R-2/R-3
refinements + their negative tests) → D (query port) → E (registers/ADRs + residuals) → F (verify).**
The chronology guard and its **negative tests are the highest-value, highest-risk deliverable** — the unit
succeeds only if a bad record is *proven* to be refused (the ML analogue of the W1-U03 gate refusal).
Never let "fix by reordering" or "drop silently" become a default path.

---

*ITRGA — First the vault, then the ledger, then the lock you can watch turn away a forged entry. Datasets
that can't be anonymous, chronology enforced as a contract, and — above all — a leaked or forward-dated
record proven to fail. Get W2-U01 right and every model that follows inherits clean, reproducible,
leak-free data. We don't guess. We prove.*
