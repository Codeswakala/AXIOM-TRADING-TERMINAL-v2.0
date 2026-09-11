# AXIOM BUILD ORDER — W3-U05

## Live Research Advisor: Operator Advisory Dashboard / Signal Workspace (FIRST operator-facing UI)

**Build Order ID:** W3-U05
**Wave:** 3 — Live Research Advisor · **Unit:** 05 (first operator-facing UI)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-15
**Authorized By:** ITRGA, following **W3-U04 APPROVED WITH OBSERVATIONS** (Platform v0.26.0; live inference
adapter) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001).
**Builds on:** W3-U01 (eligibility) + W3-U02 (signal contract + read-only history API) + W3-U03 (emit-time
guardrails + staleness) + W3-U04 (live inference).
**Carries:** design-plan **R-3** (advisory-not-instruction; disclaimer; no execution controls) + **F-1**
(stabilize flaky frontend test → green CI).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Operator Advisory Dashboard / Signal Workspace** — the **first operator-facing UI** in AXIOM,
where governed advisory signals reach a human's screen for the first time. It **reads** the W3-U02 read-only
signal-history API and **displays** each signal's direction/state, **calibrated** confidence, rationale/
explainability, operating-domain warning, validation lineage, economic verdict, and freshness — with
**guardrail outcomes (`warning`/`withheld`/`expired`) visibly NOT clean recommendations.**

Per `07_UI_UX_SPEC` + `05 v2.0` §30/§11.1 (UX/Chart presentation-only, no analytical computation) and the
accepted Wave-3 plan §10.4/§3.4: the workspace shows **advisory signals and reasons, not action buttons.**
The single brightest constraint (design-plan R-3): the UI **presents a recommendation, never an
instruction**, carries an explicit **research-advisory disclaimer**, and contains **no execution controls**
of any kind.

This unit is **display-only**: it computes no inference/signal/economic logic client-side, emits no signal,
and adds **no execution/order/broker/paper-trading control.** It also **closes F-1** (the flaky frontend
test that reddened CI at W3-U04).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution controls in the UI (R-3; plan §10.4 forbidden list).** No buy/sell button, order ticket,
  quantity/SL/TP field, position manager, broker-connect control, or paper-trade button — anywhere on the
  surface. **This is the brightest line of the first UI** — any such control is an automatic FAIL. Prove by
  shown grep + browser screenshot.
- ❌ **No advisory-as-instruction framing.** The UI must present signals as **research recommendations**, with
  an explicit visible disclaimer (e.g. "Research advisory — not an order, not financial advice; operator
  decides"). A signal must never be worded/styled as a command to trade. Prove by screenshot.
- ❌ **No client-side computation of inference/signal/economic/indicator-analytics** (§30/§11.1/§3.4). The UI
  **reads** the API and **displays** — it must not recompute a score, re-derive a signal rule, or run
  economic validation client-side. Prove structurally.
- ❌ **Guardrail outcomes shown honestly.** `warning` / `withheld` / `expired` signals must be **visibly
  distinguished** from a clean `emitted` recommendation (not rendered as confident advice); **calibrated**
  confidence shown (never raw score); poor-calibration / economically-unusable / stale states surfaced.
  Prove by screenshot.
- ❌ **No unauthenticated access.** The dashboard route is **protected** (operator auth); unauthenticated
  access redirects/401s. Prove by browser + transcript (the W0-U06/U07 logged-out precedent).
- ❌ **No new signal write/emit surface.** The UI consumes the **read-only** history API only; it must not
  add a POST/emit path (W3-U02 405 stands). No live signal push/stream added in this unit (that is W3-U06).
- ❌ **No secrets/PII in the frontend or logs** (§77); no token leakage into markup/console.
- ❌ **No regression** (Wave-0/1 + W2 + W3-U01..U04). Full suite + **green frontend CI (F-1 closed)** + parity
  smoke; broker gate + prior gates green.
- ✅ **Preserve:** advisory/research-first, UX presentation-only, tz-UTC display, all prior hardening. Sandbox
  preview caveat (external CDN/fonts degrade in-app) does not apply — this is the real app.

---

## 3. Scope — Components A–F

### Component A — Advisory dashboard / signal workspace UI (read-only) (plan §10; `07_UI_UX_SPEC`)
- A protected operator view that lists advisory signals from the W3-U02 history API with filters (market/
  symbol/timeframe/state), and a detail view per signal. **Presentation-only** — no client-side inference/
  signal/economic computation.

### Component B — Honest signal presentation (R-3 + guardrail visibility)
- Each signal displays: direction/**state** (emitted/warning/withheld/expired — visibly distinct),
  **calibrated confidence** (+ uncertainty/calibration state; never raw score), **rationale/explainability**,
  operating-domain status/warning, economic verdict, freshness/expiry, and validation lineage (model version,
  experiment, reports). `warning`/`withheld`/`expired` are **not** styled as clean recommendations.

### Component C — Advisory framing + disclaimer + NO execution controls (R-3 — the bright line)
- Explicit, visible **research-advisory disclaimer** ("not an order / not financial advice; operator
  decides"). **No execution controls** anywhere (plan §10.4 forbidden list). The surface presents a
  recommendation to inform an operator decision — the flow still ends at the operator (§15).

### Component D — Auth-protected route
- The dashboard route requires operator auth; unauthenticated access is redirected/blocked (consistent with
  the W1-U01 endpoint-auth + W0-U07/U08 logged-out redirect behavior).

### Component E — F-1 closure + governance
- **Close F-1:** stabilize the flaky `LivePriceTable` frontend test (raise `testTimeout` / fix the render-
  wait) and show **`local_ci.sh` green (`exit 0`)** — the frontend CI must be reliably green (esp. now that
  the UI grows). **ADR:** *Advisory Dashboard UX*. **Registers:** operator-overtrust risk mitigated
  (disclaimer + guardrail visibility + no execution controls); update `PROJECT_STATE`/`CHANGELOG`; note
  W3-U06 (alerts) deferral.

### Component F — Verification & Delivery
- Full suite green (backend **183** / frontend **16 + new UI tests**) — 0 failed, **green CI (F-1 closed)**,
  no regression — **plus** UI tests: renders emitted/warning/withheld/expired distinctly; shows calibrated
  confidence (not raw score) + rationale + domain/economic/freshness; **no execution control present**
  (test + grep); protected route (unauth blocked); reads history API only (no emit path).
- **Browser evidence (MANDATORY — the W0-U06 precedent):** real browser screenshots of the dashboard
  (signal list + detail with rationale/confidence/warnings), the **disclaimer visible**, a `warning`/
  `withheld`/`expired` signal shown as **not a clean recommendation**, **no execution controls on screen**,
  and the **logged-out route redirect/blocked**.
- Delivery Report per §5.

### Explicitly OUT of scope (later Wave-3 / Wave 6)
Alerts + live WS signal push to the operator (W3-U06); performance analytics/confidence-viz depth (W3-U07);
any execution/order/broker/paper trading control (Wave 6 — and forbidden by R-3 regardless). **No alerts, no
live push, no execution controls in W3-U05.**

---

## 4. Success Criteria (Definition of Done)

- [ ] Protected operator dashboard reads the W3-U02 read-only history API and displays signals
      (presentation-only; no client-side inference/signal/economic computation).
- [ ] **No execution controls** anywhere (R-3 / §10.4) — proven by grep + test + **browser screenshot.**
- [ ] **Advisory framing + visible disclaimer** ("not an order / not financial advice") — screenshot.
- [ ] Guardrail outcomes (`warning`/`withheld`/`expired`) **visibly distinct** from clean `emitted`;
      **calibrated** confidence shown (not raw); rationale + domain + economic + freshness surfaced.
- [ ] Route auth-protected; unauthenticated access redirected/blocked — browser + transcript.
- [ ] **F-1 CLOSED:** flaky frontend test stabilized; `local_ci.sh` green (`exit 0`).
- [ ] No new signal write/emit surface (history API stays read-only; 405 on POST).
- [ ] ADR + registers synced; full suite green (183 backend / 16+new frontend); no regression; prior gates
      green; conforms to `07_UI_UX_SPEC` + 05 v2.0 (§30/§11.1/§15/§77) + D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** + **browser** evidence:
1. **Operator test console** (raw, `collected N`): backend `pytest` **183, 0 failed**; frontend `vitest`
   **16 + new UI tests, 0 failed**; `ruff` clean; `tsc`/build clean.
2. **F-1 evidence:** the previously-flaky `LivePriceTable` test now green; **`local_ci.sh` green (`exit 0`)**
   with the completion marker.
3. **Browser evidence (MANDATORY):** screenshots of — (a) the signal list + a signal detail (rationale +
   calibrated confidence + domain/economic/freshness + lineage); (b) the **visible research-advisory
   disclaimer**; (c) a `warning`/`withheld`/`expired` signal shown **not** as a clean recommendation;
   (d) **no execution controls** anywhere on the surface; (e) **logged-out route redirect/blocked.**
4. **No-execution-control evidence:** shown grep (R7) over the frontend for
   `buy|sell|order|place_order|execute|position|broker|paper.?trade` (execution-control patterns) → empty
   (excluding the benign `order=asc/desc` candle sort) + a UI test asserting no execution control renders.
5. **Presentation-only evidence:** structural/test that the UI computes no inference/signal/economic logic
   (reads API only).
6. **Read-only API preserved:** history API 401/200/405 still holds; no emit path added.
7. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
8. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**
   **(Note: per the W0-U06 defective-review precedent, a UI unit is NOT approvable on report-claims or
   sandbox-only evidence — real browser screenshots are mandatory.)**

---

## 6. Standards & Constraints
UX presentation-only (§30/§11.1/§3.4; `07_UI_UX_SPEC`); **advisory-not-instruction + visible disclaimer + NO
execution controls** (R-3; plan §10.4 — the bright line for the first UI); guardrail outcomes shown honestly;
**calibrated confidence not raw**; auth-protected route; read-only history API (no emit); no client-side
inference/signal/economic computation; no secrets in frontend/logs (§77); **browser evidence mandatory**
(W0-U06 precedent); F-1 green CI. Every change in the registers (R20). Cross-platform.

---

## 7. Process
Implement → internal verify (suite + UI tests + no-execution grep/test + F-1 green CI) → doc sync
(PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence (operator-run, **browser screenshots**,
green CI, no execution controls, disclaimer visible, guardrail outcomes honest) → **submit to ITRGA** →
independent review → corrections if required → approval → next Build Order (W3-U06). The DA does not
self-approve, self-authorize the next unit, add execution controls, push a live signal, or open the broker
gate.

---

## 8. Priority Guidance (if staged)
**A (read-only dashboard) → B (honest signal presentation + guardrail visibility) → C (advisory framing +
disclaimer + NO execution controls) → D (auth-protected route) → E (F-1 close + ADR/registers) →
F (verify + BROWSER evidence).** Highest-value/highest-risk: **no execution controls + advisory-not-
instruction framing** (this is the first screen a human sees — it must be unmistakably an advisory, never a
trade button) and **browser evidence** (the W0-U06 lesson: a UI unit is proven by what's on screen, not by a
report claim). *Prove there is no buy/sell/order control anywhere and the disclaimer is visible.*

---

## 8b. Gate status
Research/advisory only — the operator now **sees** advisory signals, but the surface offers **no action**:
no execution controls (R-3), no live push/alerts (W3-U06), no execution (Wave 6), broker gate CLOSED. The
flow still ends at **Operator Decision** (§15). W3-U06 (Monitoring/Drift/Health Alerts) is the recommended
next unit and needs its own Build Order.

---

*ITRGA — The first screen a human sees must be unmistakably an advisor, never a trader: signals with their
reasons and their calibrated confidence, warnings and withholds and expiries shown for exactly what they are,
a plain disclaimer that this is research and the operator decides — and not one buy, sell, or order control
anywhere. Prove it on screen, not in prose, and make the pipeline green again. The platform now speaks to the
operator; it still does not act. We don't guess. We prove.*
