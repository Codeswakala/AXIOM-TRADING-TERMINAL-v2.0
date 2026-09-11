# BUILD ORDER — W6-U07

## Execution Research Workspace UI (first Wave-6 UI — browser evidence mandatory)

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 6 — Execution Research · **Unit:** W6-U07 · **Policy:** one unit per Build Order
**Date:** 2026-07-17
**Platform of record (pre-unit):** v0.52.0 · Alembic head `20260717_0033` · backend **345 passed** · frontend **17 files / 53 tests**
**Governing docs:** accepted `WAVE6_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §7 UI Plan + §11 W6-U07; `ITRGA_REVIEW_WAVE6_DESIGN_PLAN.md` (esp. **R6-5 display-only, R6-8 write-gate, GR6-5/GR6-10**); `08_UI_UX_SPEC.md`; `05_SYSTEM_ARCHITECTURE.md` v2.0 §30/§11.1 (presentation-only) / §43; `10_CONSTITUTIONAL_HIERARCHY.md`.
**Constitutional posture:** Governance Gate **CLOSED**. A research/simulation **display-only** workspace — no execution/actuation control of any kind.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

The first Wave-6 UI: a browser workspace that **displays** the persisted, server-side simulated execution-research artifacts (runs, fills, paper ledger, risk reports, experiments, analytics/comparison) from W6-U01…U06. It is **research-framed, `SIMULATED`-labelled, and non-actuating** — no buy/sell/submit/execute/go-live/connect-broker/account control exists. UI units are judged **in the browser** (W3-U05/W0-U06 precedent): report-claims/sandbox-only shots are NOT acceptable.

---

## 2. Scope (build exactly this)

1. **Frontend page(s)/route** under the terminal shell — e.g. `frontend/src/pages/ExecutionResearchPage.tsx` (+ any read-only components) — that lists/details the six simulated artifact types via the **existing read-only** W6 APIs.
2. **Display-only over server-persisted simulated reports (R6-5):** every metric/analytic shown is read from a server-persisted, audited simulated artifact; **no client-side recomputation presented as authoritative**.
3. **Mandatory visible framing on every surface (GR6-5/§7):** the label/disclaimer
   `SIMULATED execution research only. Not a live order, not financial advice, not real P&L. AXIOM does not act. Governance Gate CLOSED.`
   and every artifact rendered with its `SIMULATED` marker.
4. **No new table / no migration** — head stays `20260717_0033`. **No backend write path added** (this is display-only).
   - **R6-8 write-gate:** if the DA proposes ANY UI-triggered simulation *write* (e.g. "run replay"), it is a **separate acceptance gate** requiring its own persistence-capture + a bright-line proof the write reaches only simulated persistence. Default for W6-U07 is **read-only**; if no write is added, state so explicitly.
5. **Frontend Vitest** unit tests for the new page(s).

### FORBIDDEN UI affordances (must be ABSENT — prove in tests + browser)
buy · sell · submit order · execute · place order · go live · connect broker · broker credentials · account selector · real balance/margin/capital · position management for real positions · order ticket · any actuation control.

---

## 3. Binding requirements

- **R6-5 display-only:** no client-side authoritative recomputation; render server artifacts.
- **GR6-5 no execution/actuation controls:** the forbidden-affordance list (§2) is absent — proven by a frontend test asserting none of those labels/controls render, AND by browser screenshots.
- **GR6-10 browser evidence (MANDATORY):** served-session screenshots from a reachable session (`admin/admin123`), showing:
  1. an authenticated Execution Research surface rendering ≥1 simulated artifact with its `SIMULATED` label + the not-live disclaimer;
  2. a view proving **no execution/actuation controls** present;
  3. an analytics/report surface showing uncertainty/limitations + `economic_usefulness` framing (not real-P&L);
  4. a **logged-out block** (unauthenticated → redirect/blocked, e.g. `/execution-research` → `/login`).
- **R6-4:** Gate-closed proof line in-pack (backend `test_governance_gate_remains_closed_for_wave6` + broker suite green — unchanged by a UI unit, but confirm no regression).
- **No backend regression:** full backend suite stays green (expected **345**, unchanged — no new backend table/logic unless a write-gate is separately authorized).

---

## 4. Mandatory tests

**Frontend (Vitest), named:**
```
ExecutionResearchPage renders SIMULATED label and not-live disclaimer
ExecutionResearchPage renders persisted simulated artifacts read-only (runs/fills/ledger/risk/experiment/analytics)
ExecutionResearchPage does not render execution/actuation controls (buy/sell/submit/execute/go-live/connect-broker/account)
ExecutionResearchPage renders analytics uncertainty/limitations and economic_usefulness not-real-pnl framing
ExecutionResearchPage requires auth / blocks logged-out access
```
Frontend suite must PASS with the new file count (expected 17 → 18 files; report actual totals).
Backend suite unchanged and green (**345**), broker suite green.

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W6-U07.md` + `operator results.md` (+ **screenshots**) with, **inline**:

**(a) Build identity.** `Test-Path` new frontend file(s) + proof the pack is OF **W6-U07**; version `0.53.0`.
**(b) Frontend test transcript.** Named Vitest tests PASS + file/test totals (e.g. `18 files / N tests`).
**(c) Backend regression.** Full suite still **345 passed**; broker+safety suite green (no regression from the UI unit).
**(d) BROWSER EVIDENCE (MANDATORY — GR6-10).** Attach served-session screenshots for §3 items 1–4 (SIMULATED-labelled artifact; no-actuation-controls view; analytics uncertainty/economic-usefulness; **logged-out block**). Report the served URL/session; sandbox-only or report-claim shots are NOT acceptable ⇒ WITHHELD/CONDITIONAL.
**(e) No-actuation grep (frontend).** `grep -RInE "buy|sell|place_order|submit.*order|execute|go.?live|connect.?broker|account_id|order_ticket"` over the new page(s) → only disclosed benign matches (e.g. a forbidden-terms rejection list / disclaimer text), no actual control.
**(f) No new table / no migration.** `alembic current` = `20260717_0033` unchanged (or, if a write-gate was separately authorized, the persistence-capture for it — otherwise none).
**(g) No barred dependency.** grep empty; state any dep change accurately.
**(h) CI (GR6-11).** Git-Bash path → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.
**(i) Gate-closed proof (R6-4).** Named backend test PASS + broker suite green.

---

## 6. Acceptance criteria

APPROVED requires ALL of (a)–(i); named frontend tests PASS with reported totals; backend 345 unchanged + broker green; **browser screenshots present from a reachable served session** showing SIMULATED labels, no execution/actuation controls, analytics framing, and a logged-out block; no-actuation grep clean; no new table/migration (unless a write-gate separately authorized + its persistence-capture delivered); CI exit 0; Gate CLOSED.

- **Missing/unreachable/sandbox-only browser shots ⇒ WITHHELD or CONDITIONAL** (W3-U05/W0-U06 precedent — UI is judged in the browser).
- A single CRITICAL (any execution/actuation control present, any live/broker/account path, client-side authoritative recomputation presented as real, any Gate mutation) ⇒ **WITHHELD.**
- Every *risk* item proven but a *named* proof (e.g. one of the four shots) missing ⇒ **CONDITIONAL** (→ `_FINAL` on closure).

On approval: platform bump to **v0.53.0**; head `20260717_0033` (unchanged); onboarding updated; **W6-U08 (Wave-6 closeout & hardening → milestone "Execution Research Environment Complete")** becomes next authorizable — the last unit of the wave.

---

## 7. Reminders to DA

- **This unit lives or dies in the browser** — the four served-session screenshots are mandatory; tests alone are not sufficient for a UI unit.
- **No execution/actuation control anywhere** — display-only over server artifacts; every surface `SIMULATED`-labelled with the not-live disclaimer.
- Default read-only; any UI-triggered simulation write is a separate gate (R6-8) — if none, say so.
- No new table/migration expected. Verify the pack is OF W6-U07; attach only this unit's operator pack + shots; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
