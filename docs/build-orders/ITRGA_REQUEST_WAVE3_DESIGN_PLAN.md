# ITRGA → DEVELOPMENT AUTHORITY — Request for Wave 3 Engineering Design & Implementation Plan

**Document:** ITRGA-REQ-WAVE3-DESIGN
**From:** ITRGA (Independent Technical Review & Governance Authority)
**To:** Development Authority (DA)
**Date:** 2026-07-15
**Status:** ACTION REQUIRED — produce the plan; **do not begin construction** until ITRGA reviews it.
**Governing baseline (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this request (Tier 8).
**Predecessor milestone:** **Wave 2 "Research Framework Complete" CONFIRMED (2026-07-15)** — Platform v0.22.0.
**Motto:** *We don't guess. We prove.*

---

## 0. Instruction & why this gate exists

Wave 3 (Live Research Advisor) is authorized **to scope/plan.** Per the process that served Wave 2 well, the
DA shall **first produce a Wave 3 Engineering Design & Implementation Plan** for ITRGA review. **No live
inference, signal, alert, dashboard, or endpoint is to be built until ITRGA reviews and accepts the plan and
issues `BUILD_ORDER_W3-U01`.**

**Wave 3 is the highest-risk transition in the engagement so far:** for the first time, AXIOM will produce
**operator-facing signals** — it will *speak to a human about markets in something close to real time*. That
is a materially larger risk envelope than Wave 2's research-only, persisted reports. The plan will be held to
that stakes level.

---

## 1. The constitutional frame Wave 3 must prove it understands (non-negotiable)

1. **Advisory ONLY — recommendations to a human, never actions.** Per `05 v2.0` §15 the *only* approved flow
   is **Professional Recommendation → Operator Decision → (Constitutional Governance Gate) → Future Broker
   Execution**, and *"every recommendation shall remain explainable."* Wave 3 delivers **the recommendation
   and stops at the operator.** **No execution, no orders, no positions, no paper trading, no broker
   connection** — those are **Wave 6**, behind the gate, which stays **CLOSED** throughout Wave 3.
2. **Trading Intelligence System owns signals** (`05 v2.0` §6/§13): signal generation, validation,
   probabilistic analysis, confidence estimation, risk evaluation, execution *recommendations* — and it
   *"does not directly interact with brokers during the current constitutional phase."* Keep signal logic in
   its bounded context; the UX/Chart layer stays presentation-only (§30/§11.1).
3. **Deterministic inference** (`05 v2.0` §42): the same inputs + model version must yield the same signal.
   Live inference is *deterministic scoring of a governed model*, not a new training loop.
4. **Only governed models may go live.** A signal may only come from a model that is **pre-registered
   (W2-U05), validated with uncertainty (W2-U07), calibrated (W2-U08), economically stress-tested (W2-U09),
   and generalization/domain-fenced (W2-U10)** — with **research→(some new gate)→advisory** status. A model
   that has not passed the Wave-2 gauntlet cannot emit a live signal. **Deployment policy** (`07_ML_SPEC`
   §Deployment Policy): validation + documentation + review + governance approval + registration + rollback.
5. **Operating-domain guardrail at signal time** (W2-U10): a live signal must not be emitted for a
   market/timeframe/regime outside the model's validated operating domain — it must **withhold or warn**,
   not guess.
6. **Confidence honesty carries to the UI** (W2-U08): displayed confidence must be the **calibrated**
   confidence; a poorly-calibrated model's signal must be shown as such, never laundered into false
   certainty.
7. **No drift-triggered auto-anything** (W2-U10): drift/health monitoring **alerts the operator**; it never
   auto-retrains and never auto-acts.
8. **Full research audit trail** (`04_PROJECT_ROADMAP` Wave 3): every emitted signal is persisted +
   auditable (which model version, inputs/as-of, confidence, domain, the validation lineage) — the
   persisted-artifact **committing-proof-first-submission** control from Wave 2 applies to signals, signal
   history, and alerts.

---

## 2. Required contents of the Wave 3 Design & Implementation Plan

### 2.1 Architecture & bounded context
- Placement of the **Live Inference Engine** and **Trading Intelligence** signal path in `05 v2.0`; the
  interfaces used to obtain live market data (via the existing Market Intelligence / query seam — no
  reach-around) and governed models (via the W2 model registry). UX/Chart stays presentation-only.
- The end-to-end **signal flow diagram** ending at **Operator Decision** and the **CLOSED Governance Gate**
  — with an explicit "STOP: no execution beyond this point (Wave 6)" boundary drawn.

### 2.2 Live inference engine (deterministic, governed)
- How a **governed, registered model** is loaded and scored deterministically on live/near-real-time inputs;
  input as-of discipline (no look-ahead at inference; the chronology guard's spirit applies live);
  reproducibility (same input+version → same signal).
- **Model-eligibility gate:** only a model with complete W2-U05..U10 lineage + an explicit **advisory
  deployment status** may serve; ineligible model → **refused** (negative test).

### 2.3 Signal generation, validation & confidence
- Signal generation + validation (Trading Intelligence §6); **calibrated confidence** surfaced (W2-U08);
  **operating-domain guardrail** enforced at emit time (W2-U10) — out-of-domain → withhold/warn.
- **Explainability:** every signal carries a human-readable rationale + its provenance (model version,
  as-of, confidence, domain, validation/economic lineage) — *"every recommendation shall remain
  explainable"* (§15).

### 2.4 Market / health / drift monitoring & operator alerts
- Live **market monitoring**, **health monitoring**, and **drift monitoring** (design matured from W2-U10)
  that **alert the operator** — **never auto-retrain, never auto-act.** Alert = information to a human.

### 2.5 Governance dashboard, signal history, research audit trail, operator workspace
- The **governance dashboard** (surfacing model status, domain, calibration, economic verdict, drift, health
  — the "is this signal trustworthy?" view), **signal history**, **research audit trail** (every signal
  persisted + auditable), and **operator workspace** — all read/advisory surfaces.
- **Performance analytics + confidence visualization** presenting *research/advisory* performance, with
  uncertainty (no false precision), clearly labelled as advisory not guaranteed.

### 2.6 The bright-line boundary (draw it explicitly)
- A dedicated section stating **exactly where Wave 3 stops**: recommendation + operator decision surface;
  **no order/execution/broker/paper-trading path exists**, the **Governance Gate stays CLOSED**, and any
  future execution is Wave 6. Include the **negative controls** you will prove (no execution route, gate
  closed, no auto-act).

### 2.7 Unit breakdown & sequencing
- Map Wave 3 into discrete, independently-reviewable units (W3-U01, U02, …), each Level-I provable on target.
  Recommend the **first unit be the smallest safe advisory slice** — e.g. **Live Inference Engine +
  model-eligibility gate (deterministic scoring of a governed model, no UI/alerts yet)** — so the
  governed-model-only + deterministic + no-execution guarantees are proven before any signal reaches an
  operator surface. Show dependencies; mark which units first touch the operator-facing surface (higher
  scrutiny).

### 2.8 Target-platform & dependencies
- Windows/PowerShell + PostgreSQL 18 + Python 3.14.6 realism; the **wheel-compat spike** is owed by the
  first unit adopting a compiled ML/serving dependency (still owed from Wave 2). WebSocket/real-time path
  reuse (W0/W1 live seam) rather than reinvention.

### 2.9 Governance, risk, ADRs, registers
- New risks pre-listed (premature-execution, out-of-domain signal, miscalibrated-confidence-shown, drift-
  auto-act, signal-not-audited, ineligible-model-served); ADRs planned (live inference, signal contract,
  governance dashboard). Which Tier-7 registers each unit touches. Carry the Wave-2 residuals (persistence-
  capture control — now HIGH-on-recurrence; remote CI; wheel spike; OBS-1 chronology at live data).

---

## 3. What ITRGA will check the plan against (self-check first)

- **Advisory-only / no-execution**: the flow ends at Operator Decision; gate CLOSED; no order/broker path;
  negative controls defined. (R17 — the brightest line.)
- **Governed-model-only + deterministic inference**: only W2-U05..U10-complete, advisory-status models serve;
  ineligible → refused; same input+version → same signal.
- **Operating-domain guardrail + calibrated confidence at emit time** (W2-U10/U08 carried to live).
- **No auto-retrain / no auto-act** on drift/health (alerts only).
- **Every signal audited/persisted** (committing-proof-first-submission control).
- **Bounded contexts** (Trading Intelligence owns signals; UX presentation-only; no DB reach-around).
- **Target-platform realism**; unit granularity small enough for Level-I proof; first unit is the safe slice.
- **Completeness vs. roadmap Wave-3** (live inference, market/health/drift monitoring, signal generation,
  governance dashboard, performance analytics, confidence viz, operator alerts, research audit trail, signal
  history, operator workspace).

**A complete, conformant plan → ITRGA issues `BUILD_ORDER_W3-U01`. A plan with a constitutional conflict
(esp. any execution/gate ambiguity) or a missing safety control → returned with itemized corrections before
any Build Order.**

---

## 4. Process & boundaries

1. DA submits the **Wave 3 Engineering Design & Implementation Plan** (§2).
2. ITRGA reviews it against §3 + the constitution (esp. `05 v2.0` §15 flow + §6 Trading Intelligence + §42
   deterministic inference) + the Wave-2 outputs (governed-model lineage).
3. On acceptance → ITRGA authors **`BUILD_ORDER_W3-U01`** to the full operator-run (Windows + PostgreSQL)
   evidence standard, incl. the persisted-artifact committing proof and the no-execution negative controls.
4. **Hard boundaries throughout Wave 3:** advisory signals only; **no execution/orders/broker/paper trading
   (Wave 6)**; **Constitutional Governance Gate stays CLOSED**; only governed models serve; deterministic
   inference; operating-domain + calibrated-confidence honesty; drift/health **alert only**; every signal
   audited.
5. The DA **does not self-approve the plan, does not self-authorize W3-U01, does not emit a live signal
   outside a governed unit, and does not open the broker gate.** The plan is a hypothesis until ITRGA
   accepts it.

---

*ITRGA — Wave 3 is where AXIOM first speaks to an operator, so we plan it before we build it. Bring us the
blueprint: a live inference engine that only ever scores a fully-governed model, deterministically; signals
that carry their calibrated confidence, their operating domain, and their reasoning; monitoring that alerts a
human and never acts on its own; and a bright line — drawn and negatively-tested — where the recommendation
ends and the closed Governance Gate begins. The platform may advise; it may not act. We don't guess. We
prove.*
