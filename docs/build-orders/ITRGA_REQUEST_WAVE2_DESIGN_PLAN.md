# ITRGA → DEVELOPMENT AUTHORITY — Request for Wave 2 Engineering Design & Implementation Plan

**Document:** ITRGA-REQ-WAVE2-DESIGN
**From:** ITRGA (Independent Technical Review & Governance Authority)
**To:** Development Authority (DA)
**Date:** 2026-07-13
**Status:** ACTION REQUIRED — produce the plan; **do not begin construction** until ITRGA reviews it
**Governing baseline (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)** →
**`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this request (Tier 8).
**Binding prior decision:** **`docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` — LOCKED DECISION D-W2-001
(Option A: generalized, market-agnostic model).**
**Motto:** *We don't guess. We prove.*

---

## 0. Instruction

Wave 2 (ML Research Framework) is authorized **to plan**. Per the operator's standing process and
`10_CONSTITUTIONAL_HIERARCHY` §Conflict Resolution ("no implementation shall proceed until the conflict is
resolved" — now resolved), the DA shall **first produce a Wave 2 Engineering Design & Implementation Plan**
and submit it to ITRGA for review. **No code, schema, pipeline, or model is to be built until ITRGA has
reviewed and accepted the plan and issued `BUILD_ORDER_W2-U01`.**

This document tells you exactly what the plan must contain so it is reviewable on the first pass. It is a
**design plan**, not a delivery — evidence obligations attach later, per unit. But the plan will be held to
the constitution: anything that contradicts a higher tier is a plan-level finding.

---

## 1. What the plan must prove it understands (the non-negotiable frame)

1. **Research/advisory ONLY.** The ML framework produces research, not trades. **No execution, no broker
   connection, no order path** — the W1-U03 Constitutional Governance Gate stays CLOSED throughout Wave 2
   (05 v2.0 §15; roadmap Wave-6 gate). Live operator-facing signals are **Wave 3**, not Wave 2.
2. **Bounded context.** ML Research lives in the **ML Research System** (05 v2.0), dependency-inward,
   interface-based, **no business logic in infrastructure**, no shared mutable state. Data comes *from*
   Market Intelligence through approved interfaces; the ML system does not reach into other subsystems'
   internals.
3. **Generalized, market-agnostic model (D-W2-001 / `07_ML_SPEC` §Market-Agnostic Learning).** The learned
   model **must not encode symbol identity**; it learns **generalized market behaviour on normalized
   features** (transferable intelligence). Per-market **evaluation, registries/versioning, and
   operating-domain guardrails are retained and required**; per-market **specialized learned models are
   NOT the default** and may not appear without a formal `07_ML_SPEC` amendment. State this explicitly in
   the plan and show how the architecture enforces it.
4. **Dataset & chronology before models.** No model training/evaluation is designed to run — or will be
   reviewable — until the dataset + chronology-integrity layers are built and Level-I proven on the
   target. Sequence this hard gate into the plan.
5. **Scientific integrity is mandatory (`07_ML_SPEC` §Research Integrity; R18).** No data leakage,
   look-ahead, survivorship, p-hacking, post-hoc hypothesis changes, selective reporting, or hidden
   experiments. Every experiment **pre-registered** (§Experiment Governance).

---

## 2. Required contents of the Design & Implementation Plan

### 2.1 Architecture & context
- Placement of the ML Research System in 05 v2.0; its bounded context, owned responsibilities, and the
  **exact interfaces** it uses to obtain market data (no direct DB reach-around; consume via approved
  contracts).
- A data-flow diagram matching **`07_ML_SPEC` §Data Pipeline** end-to-end: Raw → Cleaning → Normalization
  → Validation → Feature Engineering → Feature Store → Training/Validation/Testing datasets → (later)
  Training → Evaluation → Monitoring → Retraining. Show where **chronology validation runs at each stage**.
- **Technology choices** (libraries/frameworks) with versions, and how they run on the **target platform
  (Windows/PowerShell + PostgreSQL 18, Python 3.14.6)** — call out any package that is problematic on
  Windows/Py3.14 *now*, not after a failed operator run (the W1-U01 lesson).

### 2.2 Canonical dataset architecture (the first unit's core)
- The dataset model must satisfy **`07_ML_SPEC` §Dataset Governance** verbatim: every dataset carries
  **dataset identifier, market, timeframe, date range, source, feature version, creation timestamp, quality
  score** — *"No anonymous dataset may enter production research."*
- **Immutability & versioning:** content-hash or immutable version id per dataset snapshot; how snapshots
  are frozen and referenced by experiments.
- **Provenance/lineage:** raw candle → cleaned → normalized → feature record → training snapshot, traceable
  both directions. Storage design (PostgreSQL tables + any artifact store), with an Alembic migration plan.
- **Reproducible training snapshots:** how "rebuild dataset vX" yields a bit-for-bit identical artifact.

### 2.3 Chronology & data-integrity guard (elevated to architecture per operator §1)
- Define the guard as a **testable contract**, not prose. At minimum: monotonic non-decreasing `open_time`
  within a series; **no record whose `open_time` exceeds the as-of/ingestion time**; explicit **quarantine
  of `source=seed:synthetic` and any forward-dated `live:simulated` candle from authoritative training
  sets** (OBS-1); temporal-only train/val/test splits (never random).
- Specify **where** the guard runs: ingestion, dataset construction, training-set generation, and
  experiment execution (all four, per operator directive §1).
- **Required negative test (design it now):** a test that a leaked / forward-dated / out-of-order record is
  **rejected or quarantined** — the ML analogue of the W1-U03 gate-refusal and W1-U02 redaction tests.
  "Chronology guarded" is proven by a record that *fails* to get through, not by prose.

### 2.4 Multi-market ingestion (market-agnostic)
- How the pipeline ingests the canonical §5 market classes (Synthetic, Forex, Crypto, Stocks, Indices,
  ETFs, Commodities, Futures) through a **market-agnostic contract**; **Deriv Synthetic Indices is a
  *provider adapter* under the Synthetic class** (External Integration isolation, 05 v2.0 §16) — not a new
  top-level market. Duplicate detection, timestamp-ordering validation, market metadata, ingestion
  validation.

### 2.5 Feature engineering + feature store (`07_ML_SPEC` §Feature Engineering / §Feature Store)
- Feature **engineering** as an explicit, versioned discipline producing **normalized** features (no symbol
  identity) — the generalized-behaviour features named in the spec (trend persistence, volatility
  expansion, mean reversion, momentum, liquidity imbalance, breakout, regimes, distributions).
- **Feature store** design: feature versioning, quality checks (§Feature Quality), and how features are
  bound to a dataset snapshot for reproducibility.

### 2.6 Experiment, validation & registry design (later units — design now, build later)
- **Experiment governance (`07_ML_SPEC` §Experiment Governance):** every experiment **pre-registered** with
  purpose, hypothesis, datasets, features, model, evaluation plan, approval timestamp, version. *"No
  undocumented experiment exists."*
- **Statistical validation (§Statistical Validation):** design for **walk-forward validation,
  out-of-sample, cross-validation, calibration, confidence intervals, bootstrap, effect size, statistical
  significance** — results must carry **uncertainty, not just point estimates.**
- **Economic validation (§Economic Validation):** **spread, commission, slippage, latency, liquidity,
  transaction costs** — *"a model may be statistically significant yet economically unusable; both
  conclusions reported independently."* **Do not omit this** — it and calibration were the two roadmap
  items missing from the operator's 10-step sequence.
- **Multi-market evaluation & generalization framework (§Multi-Market Evaluation / §Generalization
  Assessment):** per market / timeframe / regime / cross-market; the framework answering *"trained on
  markets X, does it hold on Y?"*
- **Model registry (§Model Registry):** per-market/per-timeframe registries + the mandated registry fields;
  drift monitoring (§Drift Monitoring); deployment policy (§Deployment Policy) — noting deployment here
  means *research* deployment, not execution.

### 2.7 Unit breakdown & sequencing
- Map the operator's 10-step intent to **discrete, independently-reviewable Wave-2 units (W2-U01, U02, …)**,
  each small enough to prove on target. The recommended first unit is **W2-U01 = Canonical Dataset
  Architecture + Chronology & Data-Integrity Guard** (the two layers behind the hard gate). Show
  dependencies and which units are pure-infrastructure vs. which first touch a model (gated).
- For each unit: scope, the 05 v2.0 / `07_ML_SPEC` sections it satisfies, and the **operator-run evidence**
  it will owe.

### 2.8 Governance, risk & docs
- Which Tier-7 registers each unit touches; new risks (e.g. leakage risk, dataset-drift risk) pre-listed in
  `RISK_REGISTER`; ADRs planned (dataset architecture, chronology guard, feature store).
- Confirm the LOW Wave-1 residuals (**R-CI-01** remote CI run; **CI-pytest-on-PG alignment**) will be
  closed opportunistically in the first Wave-2 CI-touching unit.

---

## 3. What ITRGA will check the plan against (so you can self-check first)

- **Constitutional conformance:** no clause contradicts Tier 3–6; D-W2-001 (Option A) honoured; execution
  gate stays CLOSED; research/advisory only.
- **Completeness vs. roadmap Wave-2:** all named components present — **including Calibration and Economic
  Viability Analysis** (the previously-omitted two).
- **Chronology guard is a *testable contract with a negative test*,** not a paragraph.
- **Dataset governance fields + immutability + provenance + reproducibility** are concrete mechanisms.
- **Market-agnostic** learning is architecturally enforced (no symbol identity), with per-market
  eval/registries/guardrails retained.
- **Target-platform realism** (Windows/PG/Py3.14) addressed up front.
- **Unit granularity** small enough that each is Level-I provable on the operator's machine.

**A plan that is complete and conformant → ITRGA issues `BUILD_ORDER_W2-U01`. A plan with a constitutional
conflict or a missing mandatory layer → ITRGA returns it with itemized corrections before any Build Order.**

---

## 4. Process & boundaries (restated)

1. DA submits the **Wave 2 Engineering Design & Implementation Plan** (this document's §2).
2. ITRGA reviews it against §3 + `ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` + `07_ML_SPEC`.
3. On acceptance → ITRGA authors **`BUILD_ORDER_W2-U01`** to the full operator-run (Windows + PostgreSQL)
   evidence standard.
4. **Hard gate:** no model training/evaluation is reviewable until dataset + chronology layers are Level-I
   proven on the target.
5. The DA **does not self-approve the plan, does not self-authorize W2-U01, and does not open the broker
   gate.** The plan is a hypothesis until ITRGA accepts it; a delivery report remains the lowest evidence
   tier when construction later begins.

---

*ITRGA — Bring us the blueprint before the first brick: the data pipeline drawn to the spec, chronology as
a lock we can watch refuse a bad record, datasets that can never be anonymous, and a model that learns
markets in general — not one symbol by name. Get the plan right and the units will fly. We don't guess. We
prove.*
