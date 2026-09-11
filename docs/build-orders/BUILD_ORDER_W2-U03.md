# AXIOM BUILD ORDER — W2-U03

## ML Research: Feature Definition Framework + Feature Store v1

**Build Order ID:** W2-U03
**Wave:** 2 — Machine Learning Research Framework · **Unit:** 03
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-13
**Authorized By:** ITRGA, following **W2-U02 APPROVED WITH OBSERVATIONS** (Platform v0.14.0) + operator
authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on:** W2-U01 (dataset architecture + chronology guard) + W2-U02 (`MarketDataQueryPort`,
`MarketSeriesKey`, `CanonicalOHLCVRecord`, market metadata).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Feature Definition Framework** and **Feature Store v1** — the layer that turns canonical
market data into **normalized, causal, versioned, market-agnostic features**, stored reproducibly and bound
to dataset snapshots. This is where the D-W2-001 promise first becomes *temptable* (features are exactly
where symbol identity could leak in), so this unit must **enforce, by test, that symbol/provider metadata is
evaluation-readable but feature-excluded**, and that **every feature is causal (no look-ahead)**.

Per `07_ML_SPEC` §Feature Engineering / §Feature Store / §Feature Quality: features emphasize robust market
representations; the store owns versioning/reproducibility/metadata/quality/market-compatibility; **"no
duplicate feature definitions shall exist"**; every feature must satisfy statistical relevance,
reproducibility, **low leakage**, stationarity where appropriate, and cross-market compatibility.

This unit computes **features** (a research artifact) but **no model, no training, no inference, no
execution.** It consumes market data **only** through the W2-U02 query port and respects the W2-U01
chronology guard.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No model / training / inference / prediction / labels-for-training.** Features only. (Label
  construction + splits are W2-U04; the chronology/label-horizon guard contract from W2-U01 stands.)
- ❌ **No execution / broker / provider live connection / credentials.** W1-U03 Constitutional Governance
  Gate stays **CLOSED**; External Integration untouched.
- ❌ **No symbol identity as a feature (D-W2-001) — enforced by test.** No `symbol_id`, one-hot symbol,
  broker/provider instrument code, or provider-specific id emitted into a feature vector. `symbol`,
  `provider`, `market_class` remain **metadata for slicing/evaluation only** — a test must prove the feature
  output **excludes** them even though evaluation code can still read them.
- ❌ **No look-ahead / non-causal features (`07_ML_SPEC` §Feature Quality "low leakage"; R18).** Every
  feature uses **only past/current data within a causal rolling window**; a **negative test must prove a
  forward-looking (peeking) feature is rejected** — the feature-layer analogue of the W1-U03 gate refusal
  and the W2-U01 chronology negative tests.
- ❌ **No DB reach-around.** Feature computation reads market data **only** via `MarketDataQueryPort`
  (05 v2.0 §16). Confirm by shown grep.
- ❌ **No duplicate feature definitions** (`07_ML_SPEC` §Feature Store). Enforce uniqueness of
  `(feature_name, feature_version)`.
- ❌ **No fabricated features.** If an input is unavailable (e.g. real volume/order-flow), the feature is a
  **documented placeholder/omitted — never invented** (continue the W2-U02 honesty precedent).
- ❌ **No secrets/PII in code/config/logs/telemetry** (05 v2.0 §77).
- ❌ **No regression** (Wave-0/1 + W2-U01/U02). Full suite + chronology-guard tests + parity smoke green.
- ✅ **Preserve:** advisory/research-first, single-uvicorn, canonical v2.0, tz-aware UTC, observability,
  dataset architecture + chronology guard + query port, and all prior hardening.

---

## 3. Scope — Components A–F

### Component A — Feature Definition Framework (`07_ML_SPEC` §Feature Engineering)
- A **feature-definition contract**: each feature declares `feature_name`, `feature_version`,
  `formula_spec`/computation, `input_requirements`, **`lookback_window`**, **`causal: true`** (enforced),
  and market-compatibility notes.
- **Uniqueness:** `(feature_name, feature_version)` must be unique — "no duplicate feature definitions."
- Ship an initial set of **normalized, market-agnostic** features from the spec's robust-representation
  families (e.g. returns / rolling returns, ATR-normalized distance, volatility, EMA relationships, RSI/
  MACD/Bollinger statistics, market-structure, time/session features, regime indicators). **Volume/
  order-flow features are placeholders if reliable inputs don't exist — not fabricated** (plan §8.3).

### Component B — Causal computation + look-ahead guard (§Feature Quality; R18)
- All feature computation is **causal by construction** (rolling windows over past/current bars only,
  aligned to `as_of_time`). Integrate with the W2-U01 chronology guard so features can never be computed
  from quarantined/forward-dated/synthetic-as-authoritative records.
- **Negative tests (the headline):** (1) a feature that peeks at future bars is **rejected/flagged**
  (reason e.g. `NON_CAUSAL_FEATURE` / `FEATURE_LOOKAHEAD`); (2) a feature computed over a series containing
  a forward-dated record is **blocked/quarantined upstream** (guard still governs).

### Component C — D-W2-001 feature-exclusion boundary (the required enforcement)
- The feature output vector **structurally excludes** symbol/provider/market_class identity while
  evaluation/slicing code can still read that metadata. **Test:** the emitted feature record contains **no**
  symbol-identity field, AND evaluation code **can** read `market_series_metadata` for the same series —
  proving "metadata is evaluation-readable but feature-excluded." (Extends W2-U02's structural
  no-symbol-identity grep into a *positive/negative pair*.)

### Component D — Feature Store v1 (`07_ML_SPEC` §Feature Store)
- Alembic-migrated tables (plan §8.4), conceptually:
  `feature_definitions` (name, version, formula_spec, input_requirements, lookback_window, causal, created_at);
  `feature_records` (feature_set_version, series_key, as_of_time, feature_values, source_dataset_hash,
  quality_score); `feature_quality_reports` (feature_set_version, missing_rate, drift_summary,
  leakage_checks, stationarity_notes).
- **Reproducibility:** deterministic serialization + a **feature content/version hash** so recomputing a
  feature set over unchanged inputs yields the **identical hash**; feature values bound to a dataset
  snapshot via feature version + source hash. **Test:** compute twice → same hash.
- **Feature quality reporting** (§Feature Quality): missing-rate, low-leakage checks, stationarity notes,
  cross-market compatibility — produced as a report artifact, not fabricated numbers.

### Component E — Governance, registers, ADR, + carried re-captures
- **ADR:** *Feature Store and Feature Versioning* (plan §11.3).
- **Registers:** record feature-leakage risk (mitigated by causal guard + negative tests), feature
  reproducibility (hash), duplicate-definition prevention; update `PROJECT_STATE`/`CHANGELOG`; note
  deferrals (feature *consumption* by models → W2-U06+).
- **Carried re-captures (mandatory this unit):**
  - **G-1 (escalation watch — MUST land here):** run **and capture** `pytest <ml test files> -vv |
    Tee-Object -FilePath <evidence>` (or `-rA`) so **each named ML test PASS is visible** in the operator
    transcript. This has been owed since W2-U01; a third miss escalates to a MEDIUM process finding.
  - **R-CI-01:** capture one CI run (remote preferred; local-orchestration acceptable), fail-closed.

### Component F — Verification & Delivery
- Full suite green (baseline **105** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: feature-definition uniqueness; **causal/look-ahead negative test**; **D-W2-001 feature-exclusion
  positive/negative pair**; feature-store persistence; **reproducible feature-hash (twice→same)**; feature
  quality report shape; port-only access (no ORM reach-around — shown grep); chronology guard still governs
  feature inputs.
- Delivery Report per §5.

### Explicitly OUT of scope (defer)
Labels/target construction + temporal split engine + reproducible snapshot *builder* (W2-U04); experiment
registry (W2-U05); any model/training/inference (W2-U06+); calibration/economic/statistical validation;
live provider connections/credentials; numpy/pandas/scikit-learn adoption **unless** a target-platform
compatibility spike (install/import/smoke on Windows+Py3.14.6) is delivered *and reviewed* per plan §4.2 —
otherwise keep to stdlib + existing stack.

---

## 4. Success Criteria (Definition of Done)

- [ ] Feature-definition framework with unique `(feature_name, feature_version)` (no duplicate definitions),
      `lookback_window` + `causal` declared; initial normalized market-agnostic feature set (placeholders
      where inputs absent — not fabricated).
- [ ] **All features causal; a look-ahead/peeking feature is rejected by test**; features cannot be computed
      from quarantined/forward-dated records (guard still governs).
- [ ] **D-W2-001 enforced by test:** feature output excludes symbol/provider identity **and** evaluation
      code can still read the series metadata (positive/negative pair).
- [ ] Feature Store v1 tables migrated on **PostgreSQL**; **reproducible feature hash (twice → identical)**;
      feature values bound to dataset snapshot; feature quality report produced.
- [ ] Data read **only** via `MarketDataQueryPort` (no ORM reach-around — shown grep); no model/training/
      execution; gate CLOSED; no secrets.
- [ ] ADR + registers synced; **G-1 named-test capture delivered**; R-CI-01 addressed.
- [ ] Full suite green (105/16 + new tests); no regression; W2-U01/U02 tests still pass; conforms to
      05 v2.0 (§16/§77) + `07_ML_SPEC` (§Feature Engineering / §Feature Store / §Feature Quality /
      §Research Integrity).

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **Operator test console** (raw, `collected N`): backend `pytest` **≥105 + new tests, 0 failed**;
   frontend `vitest 16`; `ruff` clean; `tsc`/build clean.
2. **Migration evidence:** clean `alembic upgrade head` on `PostgresqlImpl` incl. the feature-store tables;
   new head id shown.
3. **Causal/look-ahead negative-test evidence:** the run showing a peeking feature is **rejected/flagged**
   (reason code visible), and that guard-quarantined records don't reach feature computation.
4. **D-W2-001 evidence:** the positive/negative pair — feature output has **no** symbol-identity field;
   evaluation code **reads** the series metadata for the same series.
5. **Reproducibility evidence:** compute a feature set twice → **identical feature hash**; show the feature
   quality report.
6. **Port-only evidence:** a **shown grep (R7: command + output)** that feature code uses only the query
   port (no scattered candle ORM), and the no-symbol-identity grep still empty.
7. **G-1 (owed — must land):** `-vv` **captured** run (`| Tee-Object` / `-rA`) showing **each named** ML
   test PASS in the transcript.
8. **R-CI-01 (owed):** a real CI run (remote preferred) or local-orchestration green, fail-closed.
9. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
10. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Clean architecture / bounded context / single ownership (ML Research owns the feature store); dependency-
inward via the query port; **causal-only, low-leakage features** (`07_ML_SPEC` §Feature Quality; R18);
**no duplicate feature definitions**; **reproducible** (feature hash); **no symbol identity as feature**
(D-W2-001, test-enforced); **no fabricated features**; no broker/execution/credentials (§15, gate CLOSED);
no secrets in telemetry (§77); tz-aware UTC. Every change in the registers (R20). Cross-platform
(Windows + docker/PostgreSQL).

---

## 7. Process
Implement → internal verify (suite + causal/look-ahead negative tests + reproducibility + D-W2-001 pair) →
doc sync (PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence (operator-run, green, look-
ahead-refused, G-1 captured, no failing tests) → **submit to ITRGA** → independent review → corrections if
required → approval → next Build Order (W2-U04). The DA does not self-approve, does not self-authorize the
next unit, and does not open the gate.

---

## 8. Priority Guidance (if staged)
**A (feature-definition framework + uniqueness) → B (causal computation + look-ahead guard) → C (D-W2-001
feature-exclusion pair) → D (feature store + reproducible hash + quality report) → E (ADR/registers + G-1/
R-CI-01) → F (verify).** Highest-value / highest-risk: the **causal/look-ahead negative test** and the
**D-W2-001 feature-exclusion test** — features are the exact point where leakage and symbol identity would
enter, so both must be *proven refused*, not assumed. **Land the G-1 named-test capture this unit — it is
on escalation watch.**

---

## 8b. Hard Gate Reminder
**No model unit (W2-U06+) is reviewable until W2-U01–U05 are Level-I proven on the target.** U01 + U02
proven; this is U03. U04 (labels/splits/snapshot builder) + U05 (experiment registry) remain before any
model work. Broker gate CLOSED throughout Wave 2.

---

*ITRGA — Turn candles into features without letting the future — or a symbol's name — sneak in. Every
window causal, every definition unique and versioned, every feature reproducible to the same hash, and the
metadata readable for judging a model yet invisible to it. Prove the peeking feature is refused and the
symbol identity is excluded — and finally show us each test line by name. We don't guess. We prove.*
