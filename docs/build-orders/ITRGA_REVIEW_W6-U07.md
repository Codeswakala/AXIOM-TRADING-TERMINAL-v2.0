# ITRGA REVIEW — W6-U07

## Execution Research Workspace UI (first Wave-6 UI)

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W6-U07 (Wave 6) · **Reviewed pack:** `DELIVERY_REPORT_W6-U07.md` + `operator results.md` + 5 screenshots
**Build Order:** `BUILD_ORDER_W6-U07.md`
**Review date:** 2026-07-18
**Platform of record (pre-unit):** v0.52.0 · head `20260717_0033` · backend 345 / frontend 17f·53t
**Verdict:** 🟡 **CONDITIONAL APPROVAL** — UI proven in the browser; two named-evidence gaps (C-1 CI env-flake, C-2 logged-out browser shot). **Version bump to v0.53.0 HELD** until closure.
**Confidence:** HIGH on what was proven; both conditions are evidence-form gaps, not suspected failures.
**Governance Gate:** CLOSED (verified). **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST)

- `DELIVERY_REPORT_W6-U07.md`: Unit W6-U07, cites Build Order + W6-U06 prerequisite; target v0.53.0, head `20260717_0033` unchanged (no migration). ✔
- `operator results.md`: fresh pack opening with W6-U07-specific `Test-Path` (ADR-062, `ExecutionResearchPage.tsx` + `.test.tsx`, `App.tsx` route `/execution-research`). ✔
- 5 screenshots dated 2026-07-18 attached and reviewed inline. ✔

---

## 1. What is PROVEN (Level-I, operator-run + browser)

| # | Requirement | Evidence | Result |
|---|---|---|---|
| b | Frontend named tests | `ExecutionResearchPage.test.tsx` **5/5 PASSED** (SIMULATED label; read-only artifacts; no exec controls; analytics uncertainty; **requires auth / blocks logged-out**) | ✅ |
| — | Frontend suite total | **18 files / 58 tests passed** (was 17/53 → +1 file, +5 tests) | ✅ |
| c | Backend no regression | **345 passed** (unchanged); broker+safety suite **13 passed** | ✅ |
| e | No-actuation grep (frontend) | operator `Select-String buy\|sell\|place_order\|submit.*order\|execute\|go.?live\|connect.?broker\|account_id\|order_ticket` over `ExecutionResearchPage.tsx` → "Expected: no output above" (clean) | ✅ |
| f | No new table / migration | `alembic` head `20260717_0033` unchanged; read-only unit | ✅ |
| g | No barred dependency | barred-list grep → no output | ✅ |
| — | Browser: reachable served session | shots: Ops Dashboard (`W6-U07`, v0.53.0, "Execution remains governance-gated", `live_streams:false`) + `localhost:8000/execution-research` served | ✅ |
| — | Browser: SIMULATED label + not-live disclaimer | workspace banner "SIMULATED execution research only. Not a live order… AXIOM does not act. Governance Gate CLOSED." + every artifact card `SIMULATED`-labelled | ✅ |
| — | Browser: display-only, no execution/actuation controls (GR6-5) | "browser performs no authoritative recomputation"; artifact/detail/analytics surfaces show no buy/sell/execute/submit/go-live/connect-broker/account control | ✅ |
| — | Browser: analytics uncertainty + economic_usefulness (not real-P&L) | analytics card: `uncertainty: per_metric… present`, `economic usefulness: not_assessed`, `limitations: …not_real_p_and_l…` | ✅ |
| i | Gate CLOSED (R6-4) | `test_governance_gate_remains_closed_for_wave6` PASS; broker suite green; UI states Gate CLOSED | ✅ |

**The UI is genuinely proven in the browser** — served session, SIMULATED framing, display-only, no actuation controls, analytics carrying uncertainty and `not_assessed` economic usefulness. Every *risk* item is green.

---

## 2. CONDITIONS (named-evidence gaps — must close before FINAL)

### 🟡 C-1 — CI `LOCAL_CI_EXIT_CODE: 1` from a proven-unrelated offline `npm audit` failure (not a code/test failure).
The Build Order §5(h) named `LOCAL_CI_EXIT_CODE: 0`. The operator CI printed **exit 1**, but the transcript shows the root cause is environmental, not a gate failure:
```
==> npm audit (high/critical gate)
npm warn audit request to https://registry.npmjs.org/... failed, reason: getaddrinfo ENOTFOUND registry.npmjs.org
npm error audit endpoint returned an error
LOCAL_CI_EXIT_CODE: 1
```
The CI reached this only **after** backend **345 passed** and frontend deps installed — i.e. all substantive gates were green; the failure is `npm audit` unable to reach `registry.npmjs.org` (DNS `ENOTFOUND` — the machine was offline). Per the standing rule (W4-U03 lesson), a red exit from a **proven-unrelated env condition is a finding to investigate, not a green to relabel and not a withhold** — I have investigated it and it is not a defect in W6-U07. But the *named* evidence (a clean `LOCAL_CI_EXIT_CODE: 0`) is not yet on record.
**To close C-1:** re-run the documented Git-Bash CI **with network** (or with the audit step reaching the registry) and submit `LOCAL_CI_EXIT_CODE: 0` + `==> Local CI equivalent complete`. (The DR's own online run reported `npm audit: found 0 vulnerabilities`, consistent with the failure being connectivity, not a vulnerability.)

### 🟡 C-2 — Logged-out-block **browser** screenshot for `/execution-research` not delivered.
GR6-10 item 4 (and BO §5(d)(4)) require a **served-session screenshot** showing an unauthenticated user is blocked/redirected at `/execution-research`. The operator **scripted** the capture (`Start-Process /login`; "open incognito → /execution-research → capture `03_logged_out_block.png`") but the delivered set contains the **login page** and three authenticated execution-research surfaces — **not** the `/execution-research`→`/login` logged-out redirect shot. It IS proven at code/test level (operator-run `requires auth via protected route and blocks logged-out access` PASS), but for a UI unit GR6-10 requires the browser shot (W5-U07 CONDITIONAL precedent — a missing logged-out shot).
**To close C-2:** submit the served-session screenshot of `/execution-research` blocked/redirected to `/login` while logged out.

---

## 3. Classification

- **C-1** — LOW (proven-unrelated offline `npm audit` DNS failure; all substantive gates green; owes a clean exit-0 on a networked run).
- **C-2** — MEDIUM (named GR6-10 browser shot missing; proven by auth test, but UI logged-out evidence is judged in the browser — W5-U07 precedent).
- No CRITICAL, no HIGH. No execution/actuation control (browser + grep + test), display-only, SIMULATED framing, Gate CLOSED — all proven. Per proportionality (R13): every *risk* item Level-I proven, two *named* items open ⇒ **CONDITIONAL**, not WITHHELD. **v0.53.0 HELD**; platform stays **v0.52.0**.

---

## 4. Not a finding (disclosed)

- The CI red is **not** relabeled green: it is recorded as a finding (C-1) with its proven offline-`npm audit` root cause; the substantive gates (345 backend, 18/58 frontend, broker 13) are independently green in the transcript.
- `economic usefulness: not_assessed` in the analytics card is **correct** (stat≠economic), not a defect.

---

## 5. Path to FINAL

On receipt of C-1 (Git-Bash CI `LOCAL_CI_EXIT_CODE: 0` on a networked run) and C-2 (the `/execution-research` logged-out-block browser shot), I will write `ITRGA_VERDICT_W6-U07_FINAL.md` superseding this CONDITIONAL, bump to **v0.53.0** (head `20260717_0033` unchanged), update onboarding, and **W6-U08 (Wave-6 closeout → milestone "Execution Research Environment Complete")** — the last unit — becomes authorizable.

---

## 6. Posture note

Strong first Wave-6 UI: served, SIMULATED-framed, display-only, no actuation controls, analytics honest about uncertainty and `not_assessed` economics. The two gaps are pure evidence-form — a networked CI exit-0 and the one logged-out browser shot the standing UI rule requires. Close them and this unit is FINAL. The CI red was investigated and proven to be an offline `npm audit` DNS failure, not a code defect — recorded, not waved away, not relabeled green.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
