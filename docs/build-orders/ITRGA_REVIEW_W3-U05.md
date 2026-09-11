# ITRGA INDEPENDENT TECHNICAL REVIEW — W3-U05

## Live Research Advisor: Operator Advisory Dashboard / Signal Workspace (first operator-facing UI)

**Review ID:** ITRGA-REVIEW-W3-U05
**Unit:** W3-U05 · **Wave:** 3 — Live Research Advisor · **Unit:** 05 (first operator-facing UI)
**Reviewer:** ITRGA · **Date:** 2026-07-15
**Inputs reviewed:** `DELIVERY_REPORT_W3-U05.md`; operator console transcript (`operator results.md`, 1265
lines; Windows/PowerShell + PostgreSQL 18); **two real browser screenshots** (`Screenshot 2026-07-15
182842.png`, `…182859.png`); cross-checked against `BUILD_ORDER_W3-U05.md`, design-plan R-3, `07_UI_UX_SPEC`,
`05 v2.0` §30/§11.1/§15, and the W0-U06 UI-evidence precedent.
**Motto:** *We don't guess. We prove.*

---

## 0. VERDICT

> ## ✅ **APPROVED** — Platform **v0.27.0** — the first operator UI is unmistakably an advisor, proven ON SCREEN; F-1 CLOSED
>
> W3-U05 delivers AXIOM's first operator-facing surface, and it holds design-plan **R-3** exactly — proven
> not in prose but **in the browser** (the W0-U06 standard met): a **visible research-advisory disclaimer**
> ("*not financial advice, not a trade instruction, not an automated action surface; operator judgment
> remains required*"); **ADVISORY / WARNING / WITHHELD / EXPIRED** states rendered **visibly distinct** with
> honest text ("*withheld: not a current clean recommendation*", "*expired: not current and not presented as
> live guidance*"); **calibrated** confidence ("50.0% calibrated", not raw); full guardrail + lineage
> panels; **and NOT ONE buy/sell/order/execution control anywhere.** On the console: **no-execution grep
> empty** (word-boundary `\bbuy\b|\bsell\b|\border\b|place_order|\bexecute\b|\bposition\b|\bbroker\b`),
> read-only API preserved (**401 / 200 / 405**), backend `183 passed`, frontend **20 passed** (9 files), and
> **F-1 CLOSED** — the flaky `LivePriceTable` test is green (363–889ms), CI ran to `==> Local CI equivalent
> complete` with **no `exit 1`.** **No CRITICAL, no HIGH, no residual owed.**
>
> The platform now speaks to the operator — and offers no action.

**Why clean APPROVED:** the brightest line of the first UI (advisory-not-instruction + no execution
controls) is proven on screen *and* by grep/test; guardrail honesty, calibrated confidence, lineage, and the
protected read-only surface are all verified; and the sole prior residual (F-1) is discharged with a green CI.
Per proportionality (R13), and satisfying the W0-U06 mandate for real browser evidence, this is a clean
approval.

---

## 1. Browser Evidence Assessment (MANDATORY per W0-U06 — met)

The two real-browser screenshots are the decisive Level-I UI evidence:

**Screenshot 1 (workspace):** header "Advisory Signal Workspace"; subtitle "*Presentation-only: the operator
reviews the research and decides independently*"; a prominent amber **disclaimer banner** — "*Research
advisory only. This screen is not financial advice, not a trade instruction, and not an automated action
surface. Operator judgment remains required.*"; filters (market/symbol/timeframe/state); signal list with
**ADVISORY** (green) + **WARNING** (amber) badges; detail: `positive_bias · EURUSD · M1`, **"50.0%
calibrated"** (labelled *calibrated*), rationale; nav = Operations / Live Market / Advisory Signals / Chart
Workspace (**no trade/order/execution nav**); authenticated (admin, Sign out).

**Screenshot 2 (detail):** **WARNING / WITHHELD / EXPIRED** badges each distinct with honest text; **Guardrails**
panel (state reason ELIGIBLE, domain valid, economic verdict economically_usable, freshness fresh, expires_at);
**Lineage** panel (model, experiment, feature set, **statistical / calibration / economic / generalization
report IDs**); **Explainability summary** JSON (`calibrated_confidence 0.5`, `calibration_status calibrated`).

**No buy/sell/order/quantity/position/broker/paper-trade control appears anywhere on either screen.** R-3 and
plan §10.4 are satisfied visually — exactly the "prove it on screen, not in prose" standard the W0-U06
defective-review precedent demands.

---

## 2. Mandatory §5 Evidence — Line-by-Line Verification

| # | Required | Verdict | Basis |
|---|----------|---------|-------|
| 1 | pytest 183 backend / vitest 16+new / ruff / tsc / build | ✅ **PROVEN** | backend `183 passed`; frontend **20 passed (9 files)** incl. `shows calibrated confidence, rationale, lineage, economics, and freshness`; ruff clean; build ok. |
| 2 | **F-1 closed: flaky test stable + CI green (exit 0)** | ✅ **PROVEN** | `LivePriceTable > renders multiple symbol rows` green (363/889/1507ms across runs); orchestrated CI reached `==> Local CI equivalent complete`; **zero `LOCAL_CI_EXIT_CODE: 1`** in the transcript. |
| 3 | **Browser evidence (list+detail, disclaimer, guardrail outcomes, no execution controls, logged-out)** | ✅ **PROVEN** | two screenshots (§1) — disclaimer visible, states distinct, calibrated confidence, lineage, **no execution controls**; protected surface (authenticated session; unauth API 401). |
| 4 | **No execution controls** (grep R7 + test) | ✅ **PROVEN** | word-boundary grep `\bbuy\b\|\bsell\b\|\border\b\|place_order\|\bexecute\b\|\bposition\b\|\bbroker\b\|paper.?trade` over UI → **empty** (3 greps empty); UI test asserts no transaction control; visual confirmation. |
| 5 | Advisory framing + disclaimer | ✅ **PROVEN** | screenshot disclaimer banner + subtitle; UI test covers disclaimer. |
| 6 | Guardrail outcomes honest + calibrated confidence | ✅ **PROVEN** | WARNING/WITHHELD/EXPIRED distinct with honest text; "50.0% calibrated" (not raw). |
| 7 | Auth-protected route | ✅ **PROVEN** | nested under `ProtectedRoute`/`TerminalLayout` (report §3.1); API `UNAUTH_SIGNAL_HISTORY_STATUS: 401`; authenticated screenshot. |
| 8 | Read-only API preserved (no emit) | ✅ **PROVEN** | 401 / 200 / `POST_SIGNAL_HISTORY_STATUS_EXPECT_405: 405`. |
| 9 | Presentation-only (no client-side inference/signal/economic) | ✅ **PROVEN** | report §3 + no-emit grep; UI reads API and formats only. |
| 10 | Parity smoke | ✅ **PROVEN** | `WS-TICKET status: 200`; `persist_errors: 0`. |
| 11 | Confidence, honest | ✅ **COMPLIANT** | per-dimension; no fabricated %. |

**Net: every mandatory item proven, incl. the mandatory browser evidence and F-1 closure.**

---

## 3. Governance Envelope — Compliance (first-UI bright line)

| Constraint (R-3 / §10.4 / §30-§11.1) | Verdict | Basis |
|--------------------------------------|---------|-------|
| ❌ No execution controls (buy/sell/order/qty/SL-TP/position/broker-connect/paper-trade) | ✅ Upheld | grep empty + UI test + **both screenshots show none.** |
| ❌ No advisory-as-instruction; visible disclaimer | ✅ Upheld | disclaimer banner + "operator decides independently." |
| ❌ No client-side inference/signal/economic computation (presentation-only) | ✅ Upheld | reads API, formats only (report §3; §3.4). |
| ❌ Guardrail outcomes not styled as clean advice | ✅ Upheld | WITHHELD/EXPIRED honest text; states visibly distinct. |
| ❌ No unauth access | ✅ Upheld | ProtectedRoute + API 401. |
| ❌ No signal write/emit surface | ✅ Upheld | 405 on POST; read-only. |
| ❌ No regression | ✅ Upheld | 183 / 20 green; CI green; parity smoke; prior gates intact. |

**The first screen a human sees is unmistakably an advisor, never a trader — and the flow still ends at
Operator Decision (§15). The platform speaks; it does not act.**

---

## 4. Findings (classified — R8)

**No CRITICAL. No HIGH. No MEDIUM. No residual owed.**

- ✅ **F-1 (from W3-U04) — CLOSED.** The flaky `LivePriceTable` timeout is stabilized (green across three
  runs) and the CI reached completion with no `exit 1`. The MEDIUM residual is discharged.
- **OBSERVATION (LOW) — `LOCAL_CI_EXIT_CODE: 0` not captured inline** (the `==> Local CI equivalent complete`
  marker is shown and no `exit 1` appears; the explicit `: 0` echo isn't in the excerpt). Non-blocking — the
  completion marker + green frontend + absence of any exit-1 is sufficient. Show the `: 0` echo next time.
- **OBSERVATION (informational) — the UI is a genuinely strong advisory surface.** The guardrail + lineage
  panels make "why is this signal trustworthy (or not)?" answerable at a glance — the design-plan
  recommendation (surface the eligibility/lineage) is well realized.

No finding withholds or qualifies approval.

---

## 5. Evidence Confidence Statement (R6 — no fabricated percentages)

**Confidence in this APPROVAL: HIGH.** The first operator UI is verified by the mandatory **real browser
evidence** (disclaimer visible, guardrail states honest, calibrated confidence, full lineage, **no execution
controls on screen**) *and* by the operator console (empty word-boundary no-execution grep, read-only API
401/200/405, protected route, backend 183 / frontend 20 green, F-1 flaky test stabilized, CI green through
completion, parity smoke). This satisfies the W0-U06 standard that a UI unit is proven by what is on screen,
not by report claims. No residual, no contradiction. HIGH.

---

## 6. Commendation (earned)

The first operator-facing surface is exactly what the wave demanded: an *advisor*, not a trader. R-3 is
honored to the letter and **shown on screen** — a plain disclaimer, honest WARNING/WITHHELD/EXPIRED states,
calibrated (not raw) confidence, the full W2 lineage visible so trust is legible, and **not one execution
control anywhere** (grepped with word boundaries and confirmed visually). The DA also **closed F-1** cleanly
(flaky test stabilized, CI green). This is disciplined, evidence-first UI work on the highest-stakes wave.

---

## 7. Disposition

- **W3-U05: APPROVED.** Platform **v0.27.0**. **F-1 CLOSED.**
- **Residuals: NONE owed.** LOW: capture the `LOCAL_CI_EXIT_CODE: 0` echo inline next time.
- **Gate posture unchanged:** research/advisory only — the operator now **sees** signals but has **no action
  surface**; no execution controls (R-3), no live push/alerts (W3-U06), no execution (Wave 6), broker gate
  CLOSED; flow ends at Operator Decision (§15).
- **Next:** ITRGA recommends authorizing **W3-U06 = Monitoring, Drift, Health Alerts** (accepted plan §13) —
  operator alerts for drift/health/stale-data/model-degradation that **inform a human and never act**: drift
  alert does **not** retrain; alert persisted + audited; **no auto-action** (W2-U10/§Drift carried live).
  Still no execution; persisted proof (both forms) first submission. The DA does not self-authorize W3-U06,
  add execution controls, or open the broker gate. Await operator direction + a new Build Order.

---

*ITRGA — The platform now speaks to the operator, and it speaks as an advisor: a screen that says plainly it
is research and not an order, that shows a withheld or expired signal for exactly what it is, that carries
its calibrated confidence and its full lineage so trust is legible — and that offers no button to act.
Proven on screen, as it must be, and the pipeline is green again. The operator sees; the operator decides;
the platform still does not act. We don't guess. We prove.*
