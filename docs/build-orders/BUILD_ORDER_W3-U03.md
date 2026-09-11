# AXIOM BUILD ORDER — W3-U03

## Live Research Advisor: Operating-Domain + Calibration/Economic Guardrails at Emit Time (+ signal staleness)

**Build Order ID:** W3-U03
**Wave:** 3 — Live Research Advisor · **Unit:** 03
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-15
**Authorized By:** ITRGA, following **W3-U02 APPROVED** (Platform v0.24.0; first governed signal) + operator
authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001).
**Builds on:** W3-U01 (eligibility gate + deterministic inference) + W3-U02 (advisory signal contract +
persistence + governed emission/withhold state machine) + Wave-2 U08 (calibration) / U09 (economic) / U10
(operating domain).
**Carries:** accepted Wave-3 plan **R-2** (signal freshness/staleness — withhold/expire stale).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Mature the **emit-time guardrails** that stand between W3-U01 eligibility and a signal being `emitted` — so
that even an *eligible, advisory-approved* model's signal is **withheld or downgraded to `warning`** when the
specific inference is out of operating domain, poorly calibrated, economically unusable, or **stale.** W3-U02
gated emission on eligibility + basic state; this unit hardens the *per-signal* checks and adds the **R-2
freshness/staleness contract.**

Per the accepted Wave-3 plan §8 (operating-domain guardrail), §7 (calibrated confidence / poor-calibration →
withhold/warn), the economic-verdict honesty of W2-U09, and R-2 (a stale advisory must never be shown as
current). This unit remains **advisory-only, backend/API, no UI/alerts/execution.**

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / orders / broker / paper trading; signal stays inert.** W1-U03 Governance Gate CLOSED
  (R17). No order payload introduced; guardrails only *withhold/warn/expire* — they never act. Prove by grep
  + structural.
- ❌ **No emission that violates a guardrail.** An eligible model's signal that is **out-of-domain →
  withheld/warning; poorly-calibrated → warning/withheld; economically-unusable → warning (economic verdict
  shown); stale input/expired → withheld/expired.** No guardrail may be bypassable to force `emitted`. Prove
  each by named test.
- ❌ **No stale signal shown as current (R-2).** Define a concrete **freshness/staleness contract**: a max
  input as-of staleness and a signal validity/expiry. Stale input ⇒ **withheld**; a signal past validity ⇒
  **`expired`**, never presented as live. Prove by test.
- ❌ **No statistical/economic conflation; no raw-score-as-confidence.** Economic verdict (W2-U09) and
  calibrated confidence (W2-U08) are surfaced honestly and independently; economically-unusable is stated,
  not hidden behind a positive score.
- ❌ **No operator UI / alert / live WS signal push this unit** (backend/API history only, per W3-U02).
- ❌ **No chronology/identity violation; no DB reach-around; no secrets** (§16/§77; carried).
- ❌ **No regression** (Wave-0/1 + W2 + W3-U01/U02). Full suite + prior tests + parity smoke; W3-U01 gate +
  W3-U02 signal tests + broker gate still green.
- ✅ **Preserve:** advisory/research-first, tz-UTC, observability, governed emission, inert signal, read-only
  history API, deterministic inference, all prior hardening. **Persisted-artifact committing proof (raw
  `SELECT` + API read-back) first submission** (HIGH-on-recurrence).

---

## 3. Scope — Components A–F

### Component A — Operating-domain guardrail at emit (mature W2-U10 at signal time; plan §8)
- Before emission, check the inference's `(market_class, provider/symbol, timeframe, regime, source
  authority, feature_version)` against the model's **validated operating domain.** Out-of-domain ⇒
  **withheld** or **warning-only** advisory record with `UNSUPPORTED_DOMAIN`; never a normal `emitted`.

### Component B — Calibration guardrail at emit (W2-U08; plan §7)
- If the model's calibration report indicates **poor calibration** (ECE over threshold / `POORLY_CALIBRATED`)
  for the relevant slice, the signal is **`warning`** (or withheld), the **calibration status** is shown, and
  confidence is the **calibrated** value — never false certainty.

### Component C — Economic-verdict guardrail at emit (W2-U09)
- Surface the model's **economic verdict** on the signal; when the model is **economically unusable**
  (statistically-positive-but-economically-negative, per W2-U09), the signal carries the economic warning
  and is **`warning`** (not a clean `emitted` implying usability). Statistical and economic conclusions
  remain independent.

### Component D — Signal freshness / staleness contract (R-2)
- A concrete, configurable contract: **max input as-of staleness** (input too old ⇒ inference/signal
  **withheld**, e.g. `STALE_INPUT`) and **signal validity/expiry** (a signal past its validity ⇒ `expired`,
  and the history API/read never presents an expired signal as current). Deterministic + tz-aware UTC.

### Component E — Governance, registers, ADR
- **ADR:** *Signal Emit-Time Guardrails + Staleness*. **Registers:** out-of-domain-emission / miscalibrated-
  shown / economically-unusable-shown-as-usable / stale-signal risks mitigated; **close design-plan R-2**;
  update `PROJECT_STATE`/`CHANGELOG`.
- **Persisted proof:** guardrail-outcome signal records (withheld/warning/expired) + audit shown on
  PostgreSQL via **committing script → raw `SELECT ≥1 row`** *and* the authenticated history API read-back
  (both, this first submission — closing the W3-U02 LOW note).

### Component F — Verification & Delivery
- Full suite green (baseline **171** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: **out-of-domain → withheld/warning**; **poor-calibration → warning**; **economically-unusable →
  warning (verdict shown)**; **stale input → withheld (`STALE_INPUT`)**; **signal past validity → `expired`
  (not shown current)**; guardrail cannot be bypassed to force emit; inert/no-execution still holds; history
  API still read-only (401/200/405); W3-U01/U02 + broker tests green.
- Delivery Report per §5.

### Explicitly OUT of scope (later Wave-3 / Wave 6)
Live market inference adapter (W3-U04); dashboard/workspace/UI (W3-U05); alerts + live WS signal stream
(W3-U06); analytics (W3-U07); any execution/broker/paper trading (Wave 6). **No UI, no alerts, no live push
in W3-U03.**

---

## 4. Success Criteria (Definition of Done)

- [ ] Emit-time guardrails: out-of-domain, poor-calibration, economically-unusable each **withhold/warn**
      (never a clean `emitted`); guardrail non-bypassable — proven by named tests.
- [ ] **R-2 staleness:** stale input ⇒ withheld (`STALE_INPUT`); signal past validity ⇒ `expired`, never
      presented as current — proven by test.
- [ ] Calibrated confidence + economic verdict surfaced honestly + independently; no raw-score-as-confidence.
- [ ] Signal stays inert (no order payload); gate CLOSED; **no UI/alert/live push this unit**; history API
      read-only (401/200/405).
- [ ] Persisted-PG proof: guardrail-outcome records + audit via **raw `SELECT` + API read-back** (first
      submission).
- [ ] ADR + registers synced (**R-2 closed**); full suite green (171/16 + new tests); no regression; W3-U01/
      U02 + W2 + broker tests still pass; conforms to 05 v2.0 (§6/§15/§16/§77) + `07_ML_SPEC` + D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **(If compiled dep) wheel-spike;** else pure-Python + stated.
2. **Operator test console** (raw, `collected N`): backend `pytest` **≥171 + new tests, 0 failed**; frontend
   `vitest 16`; `ruff` clean; `tsc`/build clean.
3. **Migration evidence** (if schema added, e.g. validity/expiry fields): clean `alembic upgrade head` on
   `PostgresqlImpl`, new head.
4. **Guardrail evidence (captured `-vv`, by name):** out-of-domain → withheld/warning; poor-calibration →
   warning; economically-unusable → warning (verdict shown); each with reason.
5. **Staleness evidence (R-2, captured `-vv`):** stale input → withheld (`STALE_INPUT`); signal past validity
   → `expired` and NOT returned as current by the history API.
6. **Non-bypass evidence:** a guardrail-violating case cannot be forced to `emitted`.
7. **Inert / no-execution + read-only API:** grep (order/broker/execute empty) + structural; history API
   401/200/405.
8. **Persisted-PG proof (first submission):** guardrail-outcome signals + audit via **raw `psql SELECT ≥1
   row` AND authenticated API read-back** (both — closes the W3-U02 LOW note).
9. **CI green on PostgreSQL** through completion (show the completion marker result inline — the W3-U02 LOW).
10. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
11. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Advisory-only, inert signal, no execution (R17; §15 gate CLOSED); **emit-time domain + calibration + economic
guardrails** (W2-U08/U09/U10 at signal time); **statistical/economic independent, calibrated-not-raw**;
**freshness/staleness enforced** (R-2, tz-UTC); no UI/alert/live push this unit; read-only history API;
persisted-artifact committing proof (raw SELECT + API read-back) first submission; no secrets (§77). Every
change in the registers (R20). Cross-platform.

---

## 7. Process
Implement → internal verify (suite + guardrail/staleness by name + non-bypass + inert + persisted-PG) → doc
sync (PROJECT_STATE + registers + ADR; **close R-2**) → Delivery Report with §5 evidence (operator-run, green,
guardrails+staleness proven, persisted proof both forms) → **submit to ITRGA** → independent review →
corrections if required → approval → next Build Order (W3-U04). The DA does not self-approve, self-authorize
the next unit, push a live signal to an operator surface, or open the broker gate.

---

## 8. Priority Guidance (if staged)
**A (domain guardrail) → B (calibration) → C (economic) → D (staleness R-2) → E (ADR/registers, close R-2) →
F (verify, both persisted-proof forms).** Highest-value/highest-risk: the **non-bypassable guardrails** (an
eligible model can still produce an unusable/mis-domained/miscalibrated signal — the emit-time checks are
what stop that reaching a human) and **staleness** (a stale advisory shown as current is a real harm). *Prove
each guardrail withholds/warns and the stale signal expires.*

---

## 8b. Gate status
Research/advisory only — signal stays an **inert record**; **no execution (Wave 6), no operator UI/alert/live
push this unit, broker gate CLOSED.** W3-U04 (Live Market Inference Adapter) is the recommended next unit and
needs its own Build Order.

---

*ITRGA — Eligibility earned the right to speak; the emit-time guardrails decide whether *this* signal should.
Out of its validated domain, poorly calibrated, economically unusable, or stale — the answer is withhold,
warn, or expire, never a clean recommendation implying certainty. Teach the signal to know its own limits and
its own age. The platform speaks only within what it has proven — and still does not act. We don't guess. We
prove.*
