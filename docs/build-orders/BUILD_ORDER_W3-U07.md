# AXIOM BUILD ORDER — W3-U07

## Live Research Advisor: Performance Analytics + Confidence Visualization (advisory, uncertainty-mandatory)

**Build Order ID:** W3-U07
**Wave:** 3 — Live Research Advisor · **Unit:** 07
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-15
**Authorized By:** ITRGA, following **W3-U06 APPROVED** (Platform v0.28.0; alerts inform-never-act) +
operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001).
**Builds on:** W2-U07 (statistical validation — uncertainty mandatory) + W2-U08 (calibration) + W3-U02/U03
(signals + guardrail states) + W3-U05 (advisory UI) + W3-U06 (alerts).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver **advisory performance analytics + confidence visualization** — an operator-facing view of how the
advisory has performed and how trustworthy its confidence is, **as research, with uncertainty, never as a
guarantee.** Per the accepted Wave-3 plan §9.4/§7.2 and the W2-U07 statistical discipline: every reported
performance number carries **uncertainty (CI / bands / bins) — no point estimate, no false precision** — and
the surface is **explicitly labelled advisory-research, not guaranteed/expected returns.**

Confidence visualization (§7.2) shows **calibrated** confidence, confidence band/uncertainty, calibration
status, base-rate/economic context, and an explicit **warning when confidence is unreliable** (poorly
calibrated). This is **presentation-only** (UX/Chart, §30/§11.1/§3.4): it reads persisted signals/validation/
calibration artifacts and **displays** them — it recomputes no inference/signal/economic/statistical logic
client-side, emits nothing, and adds **no execution controls (R-3).**

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No false precision / no point-estimate-only performance.** Every performance metric shown **must
  carry uncertainty** (confidence interval / band / bin support / sample count) — a bare number implying
  certainty is non-conformant (W2-U07). Prove by test + browser screenshot.
- ❌ **No performance shown as guaranteed / expected / promised returns.** The surface is **explicitly
  labelled research/advisory** ("past/backtested research performance, not a guarantee; not financial
  advice") — consistent with W3-U05 R-3. No language/styling implying assured profit. Prove by screenshot.
- ❌ **No raw-score-as-confidence.** Confidence viz shows **calibrated** confidence + band + calibration
  status; a poorly-calibrated model's confidence is shown **with an explicit unreliability warning** (§7.2),
  never as certainty. Prove by test/screenshot.
- ❌ **No client-side computation of inference/signal/economic/statistical analytics** (§30/§11.1/§3.4). The
  view **reads** persisted W2-U07/U08 + W3-U02/U03 artifacts (via read-only API) and **presents** them — it
  must not recompute a metric/CI/calibration authoritatively in the browser. Prove structurally.
- ❌ **No execution controls (R-3).** No buy/sell/order/position/broker/paper-trade control anywhere on the
  analytics surface. Prove by grep + screenshot.
- ❌ **No cherry-picking / no misleading aggregation.** Analytics report against the pre-registered/persisted
  results honestly (R18); no selective window/metric that flatters. Recall the W2-U07 lesson: a strong number
  gets a leakage/base-rate sanity check — do not present a suspiciously-good stat as skill without context.
- ❌ **No unauthenticated access; no secrets/PII** (§77); read-only API only (no emit/write).
- ❌ **No regression** (Wave-0/1 + W2 + W3-U01..U06). Full suite + **green CI (capture `exit 0` echo — the
  standing LOW)** + parity smoke; prior gates green.
- ✅ **Preserve:** advisory/research-first, UX presentation-only, tz-UTC display, all prior hardening,
  no-execution/no-auto-action. **Browser evidence mandatory** (W0-U06 precedent — UI unit). **Persisted-
  artifact committing proof (both forms) first submission** if any new persisted analytics artifact is added.

---

## 3. Scope — Components A–F

### Component A — Advisory performance analytics (read-only, uncertainty-mandatory) (plan §9.4; W2-U07)
- An operator view aggregating **advisory research performance** from persisted signals + W2-U07 validation
  (e.g. hit-rate/accuracy over emitted advisories, per market/timeframe/state) — **each metric with
  uncertainty** (CI/bootstrap band / sample count). Presentation-only; reads via read-only API.

### Component B — Confidence visualization (§7.2)
- Show, per signal/model: **calibrated confidence + confidence band/uncertainty**, **calibration status**,
  base-rate/economic context, and an explicit **"confidence unreliable" warning** when poorly calibrated.
  Confidence **history** where available (from persisted signals). No raw score as confidence.

### Component C — Advisory-not-guaranteed framing (R-3 continued)
- Explicit, visible labelling that this is **backtested/research advisory performance, not a guarantee, not
  financial advice, not expected future returns**; uncertainty shown alongside every headline number. No
  execution controls.

### Component D — Presentation-only integrity + read-only API
- The analytics view **computes no inference/signal/economic/statistical logic client-side** — it reads
  persisted artifacts and formats. Any new backend aggregation endpoint is **read-only + authenticated**
  (no emit/write/execute). Prove structurally + API 401/200 (405 on write if applicable).

### Component E — Governance, registers, ADR
- **ADR:** *Performance Analytics + Confidence Visualization*. **Registers:** false-precision / performance-
  as-guarantee / raw-confidence-shown / overtrust risks mitigated; update `PROJECT_STATE`/`CHANGELOG`; note
  W3-U08 (closeout) deferral.
- **Persisted proof (both forms) first submission** — only if a new persisted analytics artifact is added
  (else state none added; read-only aggregation over existing artifacts).

### Component F — Verification & Delivery
- Full suite green (backend **188** / frontend **20 + new UI tests**) — 0 failed, **green CI (`exit 0`
  echoed)**, no regression — **plus** tests: every performance metric carries uncertainty (**a
  point-estimate-only render is rejected/flagged**); calibrated confidence + band + calibration-status shown
  (not raw); **advisory-not-guaranteed label present**; **no execution controls** (test + grep);
  presentation-only (no client-side recompute); read-only API (401/200); prior gates (W3-U01..U06 + broker)
  green.
- **Browser evidence (MANDATORY — W0-U06):** screenshots of the analytics view (metrics **with uncertainty/
  bands**, calibrated confidence + calibration status, base-rate/economic context), the **advisory-not-
  guaranteed disclaimer**, a **poorly-calibrated → unreliability warning**, and **no execution controls** on
  screen; logged-out route blocked.
- Delivery Report per §5.

### Explicitly OUT of scope (later / Wave 6)
Wave-3 closeout & hardening (W3-U08); any execution/order/broker/paper trading (Wave 6 — forbidden by R-3
regardless); external notification; alert auto-action (W3-U06 rule stands). **No execution controls, no
guaranteed-returns framing, no client-side authoritative recomputation.**

---

## 4. Success Criteria (Definition of Done)

- [ ] Advisory performance analytics (per market/timeframe/state) with **uncertainty on every metric** (no
      point estimate / no false precision) — proven by test + screenshot.
- [ ] Confidence viz: **calibrated** confidence + band + calibration status + base-rate/economic context +
      **unreliability warning when poorly calibrated** (not raw score).
- [ ] **Advisory-not-guaranteed framing** visible (research/backtested, not a guarantee, not financial
      advice); **no execution controls** (grep + test + screenshot).
- [ ] Presentation-only (no client-side inference/signal/economic/statistical recompute); read-only
      authenticated API (401/200; no emit/write/execute).
- [ ] Honest aggregation (no cherry-picking); strong metrics contextualized (base-rate/leakage sanity per
      W2-U07).
- [ ] No regression; **green CI (`LOCAL_CI_EXIT_CODE: 0` echoed)**; browser evidence delivered; persisted
      proof (both forms) if any new persisted artifact.
- [ ] ADR + registers synced; full suite green (188 backend / 20+new frontend); prior gates green; conforms
      to `07_UI_UX_SPEC` + `07_ML_SPEC` §Statistical Validation + 05 v2.0 (§30/§11.1/§15/§77) + R-3/D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** + **browser** evidence:
1. **Operator test console** (raw, `collected N`): backend `pytest` **188 + new, 0 failed**; frontend
   `vitest` **20 + new, 0 failed**; `ruff` clean; `tsc`/build clean.
2. **Migration evidence** (only if a new persisted analytics artifact added): clean `alembic upgrade head`
   on `PostgresqlImpl`, new head; else state none.
3. **Uncertainty-mandatory evidence (captured `-vv`):** a performance metric with CI/band/sample count;
   **a point-estimate-only render rejected/flagged.**
4. **Confidence-viz evidence:** calibrated confidence + band + calibration status; **poorly-calibrated →
   unreliability warning** (not raw score).
5. **Advisory-not-guaranteed + no-execution-controls evidence:** grep (R7, word-boundary) empty for
   execution controls; UI test asserts none; **browser screenshots** (metrics-with-uncertainty, disclaimer,
   unreliability warning, no execution controls, logged-out blocked).
6. **Presentation-only + read-only API:** structural (no client-side recompute); API 401/200 (405 on write).
7. **Persisted-PG proof (both forms) first submission** — if any new persisted artifact; else N/A stated.
8. **CI green on PostgreSQL** through completion, **`LOCAL_CI_EXIT_CODE: 0` echoed inline** (standing LOW).
9. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
10. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages** (and metrics
    stated **with uncertainty, honestly**).
    **(W0-U06: a UI unit is not approvable on report-claims/sandbox-only — browser screenshots mandatory.)**

---

## 6. Standards & Constraints
UX presentation-only (§30/§11.1/§3.4; `07_UI_UX_SPEC`); **uncertainty mandatory, no false precision, no
guaranteed-returns framing** (W2-U07; plan §7.2/§9.4); **calibrated confidence + unreliability warning, not
raw** (W2-U08); no client-side authoritative recompute; **no execution controls** (R-3); read-only
authenticated API; honest aggregation (R18); no secrets (§77); **browser evidence mandatory** (W0-U06); green
CI with `exit 0` echo; persisted proof both forms if new artifact. Every change in the registers (R20).
Cross-platform.

---

## 7. Process
Implement → internal verify (suite + uncertainty-mandatory + confidence-viz + no-execution + presentation-
only + CI exit-0) → doc sync (PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence (operator-
run, **browser screenshots**, green CI exit-0, uncertainty shown, no guaranteed framing, no execution
controls) → **submit to ITRGA** → independent review → corrections if required → approval → next Build Order
(W3-U08, Wave-3 closeout). The DA does not self-approve, self-authorize the next unit, add execution
controls, or open the broker gate.

---

## 8. Priority Guidance (if staged)
**A (performance analytics w/ uncertainty) → B (confidence viz + unreliability warning) → C (advisory-not-
guaranteed framing + no execution controls) → D (presentation-only + read-only API) → E (ADR/registers) →
F (verify + BROWSER evidence + CI exit-0).** Highest-value/highest-risk: **uncertainty-mandatory / no false
precision** and **advisory-not-guaranteed framing** — an analytics screen that shows a bare hit-rate or
implies guaranteed returns is exactly the operator-overtrust harm this wave defends against. *Prove every
number carries its uncertainty and the screen never promises a return — on screen, not in prose.*

---

## 8b. Gate status
Research/advisory only — analytics **inform** with honest uncertainty; **no execution controls (R-3), no
auto-action (W3-U06), no execution (Wave 6), broker gate CLOSED**; flow ends at Operator Decision (§15).
**W3-U08 (Wave-3 Closeout & Hardening) is the LAST Wave-3 unit → then "Professional Advisor Platform
Complete" milestone comes into reach** (ITRGA-declared, on approval). It needs its own Build Order.

---

*ITRGA — Show the operator how the advisory has done and how far to trust its confidence — but never as a
promise: every number wearing its uncertainty, every confidence calibrated and flagged when unreliable, the
screen plainly labelled research not guarantee, and not one control to act. A bare hit-rate or a whisper of
"expected returns" is exactly the overtrust we guard against. Prove the uncertainty is shown and no return is
promised — on screen. The platform informs; it still does not act. We don't guess. We prove.*
