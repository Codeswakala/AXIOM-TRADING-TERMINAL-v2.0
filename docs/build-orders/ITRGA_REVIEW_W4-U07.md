# ITRGA INDEPENDENT REVIEW — W4-U07 (Institutional Intelligence Dashboard)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W4-U07** — Institutional Intelligence Dashboard (first Wave-4 UI) |
| Wave | 4 — Institutional Intelligence |
| Build Order | `docs/BUILD_ORDER_W4-U07.md` |
| Evidence | `uploads/DELIVERY_REPORT_W4-U07.md` + `uploads/operator results.md` (894 lines) + 1 browser screenshot |
| DA-claimed platform | 0.37.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **🟡 CONDITIONAL APPROVAL — C-1 (browser: report WITH uncertainty) + C-2 (browser: logged-out block) must be shown. Core UI APPROVED.** |
| Confidence | **HIGH** on implementation correctness; the two conditions are the UI-unit's mandatory browser proofs, partially unmet |

> **We don't guess. We prove.** Three of five mandatory browser shots are proven; two are not — one being the dashboard's whole purpose (a report shown with its uncertainty). For a UI unit that is a condition, not a footnote.

---

## 1. Bottom line

The dashboard is **implemented correctly and safely** — presentation-only, no execution controls, research
disclaimer, no raw score, backed by read-only APIs (401/200/405), all text gates green (233 backend / 12
files·29 frontend / CI exit 0). **But this is a UI unit, and the Build Order made five browser proofs mandatory
and non-waivable** (W3-U05/W0-U06 precedent). Only **one** screenshot was supplied. It proves three of the five;
two remain unmet:
- **C-1:** no browser shot of a **report rendered WITH its uncertainty + sample_count** — the single shot shows
  "Reports loaded: 1" yet both visible cards read **"No reports returned,"** so the dashboard's core function
  (displaying a research metric with uncertainty) is **not shown on screen.**
- **C-2:** no browser shot of the **logged-out block** on `/intelligence`.

Per the standing rule (unmet *mandatory* evidence ⇒ withhold) applied proportionally (R13): the core UI is
approved; the version bump is held until C-1 + C-2 are shown. This is an evidence-completeness hold, **not** a
defect — the component tests indicate the behavior exists; it simply was not proven in the browser.

---

## 2. What is PROVEN ✅

### 2.1 Text/functional gates (all green on target)
- Build identity W4-U07 / v0.37.0; `Test-Path`×N True; no migration (head `20260716_0023`).
- **API auth table (all 5 W4 endpoints):** correlation / regime / scenario / portfolio-risk /
  signal-validation → **unauth 401 / auth 200 / POST 405.** ✅
- **R-3 no-execution grep** empty (command + output) + named frontend test
  `does not render transaction controls PASSED`. ✅
- **GR-8 presentation-only grep** over `InstitutionalIntelligencePage.tsx` for
  `pearson|regime|scenario|drawdown|wilson|fit(|predict(|score(|raw_score` → empty (reads API + formats only).
  ✅
- Frontend **12 files / 29 tests** (incl. `renders research framing and report uncertainty` +
  `does not render transaction controls`); backend **233 passed**; ruff clean; npm audit 0; tsc/build ✓;
  **CI via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `Local CI equivalent complete` +
  `LOCAL_CI_EXIT_CODE: 0`** (transcript W4-U07); parity smoke ws-ticket 200. ✅

### 2.2 Browser shots satisfied by the one screenshot (`/intelligence`, served, logged in, W4-U07)
| Mandatory shot | Status |
|---|---|
| (a) Dashboard rendered on a reachable served session | ✅ `127.0.0.1:8000/intelligence`, no ERR_CONNECTION_REFUSED |
| (c) Research/not-guaranteed disclaimer | ✅ "Research context only. …not financial advice, not a guarantee, not a prediction, and not an instruction. …AXIOM does not act." |
| (d) No execution controls anywhere | ✅ nav = Operations/Live Market/Advisory Signals/Performance Analytics/Institutional Intelligence/Chart Workspace; only "Refresh Research" + "Sign out"; no buy/sell/order/broker |

---

## 3. Conditions to close (browser evidence — no re-implementation)

### C-1 (must close) — a report rendered WITH uncertainty + sample_count, in the browser
The header shows **"Reports loaded: 1"** but the visible cards read **"No reports returned"** — so the shot does
not demonstrate the dashboard's core purpose. Seed/point at existing W4 report data and capture a browser shot
of **at least one report card showing its metric + uncertainty interval + sample_count** on the served page.
(The component test `renders research framing and report uncertainty PASSED` shows the code can render it — but
a UI unit is proven in the browser, not by a fixture-only test; W3-U05/W0-U06.)

### C-2 (must close) — logged-out block on `/intelligence`
Capture a browser shot of an unauthenticated visit to `/intelligence` being **refused/redirected to login**
(not rendered). (`ProtectedRoute` is cited in the report and the API is 401 unauth — but the on-screen block
must be shown, as for every prior operator surface.)

*Cosmetic note (non-blocking):* the "Reports loaded: 1" vs "No reports returned" cards suggest a
counted-but-unbucketed report or an empty-state mismatch; the C-1 re-shot with real data will incidentally
confirm the cards populate correctly.

---

## 4. Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| **C-1** | **MEDIUM** | No browser proof of a report rendered WITH uncertainty + sample_count (the one shot shows empty cards despite "Reports loaded: 1") | **Condition — re-shot with real report data** |
| **C-2** | LOW–MEDIUM | No browser proof of the logged-out block on `/intelligence` | **Condition — re-shot of logged-out redirect** |
| — | — | R-3 no-exec, GR-8 presentation-only, API 401/200/405, disclaimer, no raw score, 233/12·29, CI exit 0 | ✅ proven |

**No CRITICAL. No governance breach. Core UI proven.** Two mandatory UI browser proofs unmet ⇒ **CONDITIONAL
APPROVAL** (not withheld — the risk items and text gates are all proven; the gaps are browser-proof
completeness for a UI unit).

---

## 5. Disposition & next step

- **W4-U07 — 🟡 CONDITIONAL APPROVAL.** Core dashboard (presentation-only, no-execution, research-framed,
  read-only-API-backed) is **APPROVED**. Platform advances to **v0.37.0 on closure of C-1 + C-2** (until then
  v0.36.0 remains the version of record for ITRGA purposes).
- **To close:** a short browser-only re-run supplying (C-1) a report rendered with uncertainty + sample_count
  and (C-2) the logged-out block on `/intelligence`. No re-implementation. On that evidence ITRGA issues the
  FINAL verdict, advances to v0.37.0, and (on operator authorization) issues `BUILD_ORDER_W4-U08.md` (Wave-4
  Closeout — the LAST Wave-4 unit → "Institutional Intelligence Layer Complete" milestone).
- Commendation: the safety posture is exactly right — presentation-only proven by grep + test, no-execution
  proven, disclaimer on screen, all text gates green with CI via the Git-Bash path. The gap is narrow and
  browser-only.
- DA does not self-approve, self-advance the version, self-close the conditions, begin W4-U08, or open the Gate.

> **We don't guess. We prove.** — ITRGA
