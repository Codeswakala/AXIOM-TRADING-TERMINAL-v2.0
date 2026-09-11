# AXIOM BUILD ORDER — W4-U07

## Institutional Intelligence: Dashboard / Chart Context (presentation-only, research-framed, no execution controls — BROWSER EVIDENCE MANDATORY)

**Build Order ID:** W4-U07
**Wave:** 4 — Institutional Intelligence · **Unit:** 07 (first Wave-4 operator UI)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W4-U06 APPROVED — CLEAN** (Platform v0.36.0; signal validation) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → **`07/08_UI_UX_SPEC`** → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-4 guardrails **GR-1…GR-8**; this UI unit carries
**R-3** (advisory-not-instruction / no-execution-controls) + **GR-8** (presentation-only) + **browser-evidence
mandate** (W3-U05/W0-U06 UI precedent).
**Governing plan:** `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §7 (UX surfaces), §9 (W4-U07).
**Builds on:** W4-U02…U06 read-only APIs (correlation / regime / scenario / portfolio-risk / signal-validation
reports) + W3-U05/U07 presentation-only UI precedent.
**Baseline to meet/exceed:** backend **233** / frontend **11 files · 25 tests**; Platform **v0.36.0**; head
**20260716_0023**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Institutional Intelligence Dashboard** — the first Wave-4 operator-facing surface that
**displays the persisted Wave-4 research reports** (correlation, regime, scenario, portfolio-risk,
signal-validation) as **read-only research context**, each shown **with its uncertainty and its
research/not-guaranteed framing.** It is **presentation-only** (05 v2.0 §30/§11.1, GR-8): it reads the
existing read-only intelligence APIs and **displays** them — it recomputes no correlation/regime/scenario/
risk/validation metric client-side, emits nothing, and adds **no execution controls (R-3).**

Because this is UI, **browser evidence is mandatory** (W3-U05/W0-U06 precedent — a UI is never approved on
report-claims or sandbox-only; it must be shown rendered in a reachable, served session).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution controls anywhere (R-3 — KEYSTONE).** No buy/sell/order/position/broker/paper-trade/
  sizing/execute control on any dashboard surface or nav. Prove by **grep + test + browser screenshot**.
- ❌ **Presentation-only — no client-side authoritative recompute (GR-8/§30/§11.1).** The dashboard **reads**
  the W4 read-only APIs and **formats** them; it must not recompute a correlation/regime/scenario/risk/
  validation metric, CI, or calibration authoritatively in the browser. Prove structurally (grep: no
  `pearson|regime|scenario|drawdown|wilson|fit(|predict(|score(` compute in the page) + test.
- ❌ **No metric shown without its uncertainty / no false precision (GR-7).** Every displayed research metric
  shows its **uncertainty + sample_count** (as persisted). A bare number implying precision is non-conformant.
  Prove by test + screenshot.
- ❌ **No research shown as guaranteed/expected/predicted (R-3 framing).** Each surface carries the
  research/advisory disclaimer (not financial advice, not a guarantee, not a prediction/instruction — and
  correlation≠causation / scenario=hypothetical where shown). No language/styling implying assured profit.
  Prove by screenshot.
- ❌ **No raw model score displayed.** Confidence/validation surfaces show **calibrated** metrics only; raw
  score is not rendered (W3-U07/W4-U06 standard). Prove structurally + screenshot.
- ❌ **Authenticated; logged-out blocked.** The dashboard route requires operator auth; a logged-out attempt is
  refused (redirect/401), not rendered. It reads the W4 read-only APIs only (401 unauth / 200 auth). Prove by
  screenshot (logged-out block) + the API auth behavior.
- ❌ **No execution / broker / gate path** (GR-1/GR-3). Gate CLOSED. **R-3 wave-wide grep** (command + output),
  residuals disclosed + benign.
- ❌ **No new backend analytical capability / no new report type.** This unit is a **view** over existing W4
  APIs; if a thin read-only aggregation endpoint is genuinely needed it must be read-only (401/200, POST
  405/404) and add no new persisted artifact (no migration expected). State explicitly if none added.
- ❌ **No unspiked compiled dependency; no D-W2-001 breach.**
- ❌ **No regression** (Wave-0…W4-U06). Full suite green + frontend green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript labelled W4-U07).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic, all prior hardening,
  npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** The R-3 no-execution-controls + presentation-only proofs, shown **in the
browser**, are the keystones.

---

## 3. Scope (Components A–C)

### A. Dashboard UI (frontend, presentation-only)
- A new authenticated dashboard view (e.g. `/intelligence`) nested under the existing terminal route guard,
  reachable from nav.
- Displays the persisted W4 reports via the existing read-only APIs
  (`/api/v1/intelligence/correlation-reports`, `…/regime-reports`, `…/scenario-reports`,
  `…/portfolio-risk-reports`, `…/signal-validation-reports`) — list/summary + detail as appropriate.
- Each metric/artifact renders **with uncertainty + sample_count**, **research/advisory disclaimer**,
  method/lineage where relevant, and appropriate framing (correlation≠causation; scenario=hypothetical;
  risk=not-a-real-portfolio; validation=historical/not-guaranteed). **Calibrated only — no raw score.**
- **No execution/order/broker/sizing controls; no signal/action affordance.** Formats API payloads only.

### B. (If needed) thin read-only aggregation endpoint
- Only if genuinely required to back the dashboard; **read-only** (401/200, POST 405/404), **no new persisted
  artifact / no migration.** State explicitly if none is added.

### C. Tests + registers
- Frontend tests: renders reports with uncertainty; renders research/not-guaranteed disclaimer; **does not
  render execution/transaction controls (R-3)**; does not render raw score; presentation-only (no client
  recompute). Backend test if an endpoint is added (auth/read-only).
- Update registers/docs: RISK (dashboard rows per plan §8), CHANGELOG → **v0.37.0**, PROJECT_STATE, ADR,
  GOVERNANCE_AMENDMENTS (Option A stands, Gate CLOSED).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL + BROWSER)

Report `DELIVERY_REPORT_W4-U07.md` + raw `operator results.md` + **browser screenshots**. **Prove build
identity first.**

1. **Build identity** — new files/ADR exist; v0.37.0; `git log -1 --oneline`.
2. **BROWSER SCREENSHOTS (MANDATORY)** — from a single reachable served session (`127.0.0.1:…`):
   (a) login + the dashboard rendered; (b) a W4 report shown **with uncertainty + sample_count**; (c) the
   **research/not-guaranteed disclaimer** visible; (d) **no execution/order/broker controls** anywhere (nav +
   surface); (e) **logged-out** attempt on the dashboard route **blocked** (redirect/login, not rendered).
   Every screenshot must show a served page (no `ERR_CONNECTION_REFUSED`).
3. **R-3 no-execution grep** — over `frontend/src` (command + output), no buy/sell/order/position/broker/
   paper-trade/sizing control; plus a named frontend test "does not render transaction/execution controls".
4. **Presentation-only grep** — over the dashboard page(s): no `pearson|regime|scenario|drawdown|wilson|
   fit(|predict(|score(|raw_score` authoritative compute; reads API + formats only.
5. **API auth** (backing reads) — unauth **401** / auth **200** on the W4 read endpoints the dashboard uses;
   any added aggregation endpoint POST → **405/404**.
6. **Frontend gates** — `vitest` (new higher total, 0 failed, named R-3 test present), `tsc` clean, `build` ✓,
   npm audit 0.
7. **Full backend regression** — `pytest` **≥233**, 0 failed (unchanged if no backend change); ruff clean;
   no new migration (head `20260716_0023`) unless a justified read-only endpoint required one (it shouldn't).
8. **R-3 wave-wide grep** + Gate CLOSED (broker gate tests).
9. **CI** — documented Git-Bash invocation → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`**
   (transcript labelled W4-U07). **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.37.0.
- [ ] **BROWSER EVIDENCE (mandatory):** dashboard rendered on a reachable served session; report with
      uncertainty + sample_count; research/not-guaranteed disclaimer; **no execution controls anywhere**;
      logged-out route blocked. (No `ERR_CONNECTION_REFUSED`.)
- [ ] **R-3 keystone:** no-execution grep empty (command+output) + named frontend test "no transaction/
      execution controls".
- [ ] **GR-8 presentation-only:** no client-side authoritative recompute (grep + test); reads API + formats.
- [ ] Every displayed metric shows uncertainty + sample_count; no raw score; research framing throughout.
- [ ] Dashboard route authenticated; logged-out blocked; backing W4 APIs 401/200 (added endpoint POST 405/404).
- [ ] Frontend green (new higher vitest total, named R-3 test), tsc/build clean, npm audit 0; backend ≥233
      unchanged; no new migration (or justified read-only one).
- [ ] **R-3** wave-wide grep empty/benign; Gate CLOSED; no execution/broker path.
- [ ] No regression; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke.
- [ ] DA does not self-approve, self-advance, build W4-U08, adopt an unspiked dep, or open the Gate.

**A single CRITICAL, unmet mandatory evidence (incl. MISSING/UN-REACHABLE browser screenshots), or a red gate
⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA approves W4-U07, advances to **v0.37.0**, and (on operator
authorization) issues `BUILD_ORDER_W4-U08.md` (Wave-4 Closeout & Hardening — the LAST Wave-4 unit).

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Wave-4 closeout (W4-U08, own Build Order).
- Any execution/order/broker/account/position/sizing control or path; opening the Gate.
- Any new backend analytical capability / new persisted report type / new learned model.
- Any client-side authoritative recompute of a metric/CI/calibration.
- Raw-score display; guaranteed/expected/predicted framing.
- Any Wave-5/6 work.

---

## 7. Notes to the Development Authority

This is a **UI unit**, so the standard is different in one decisive way: **it is judged in the browser.** A
correct implementation still FAILS review if the screenshots are missing, sandbox-only, or show an unreachable
page (W3-U05/W0-U06 precedent). Show, in a reachable served session: the dashboard rendered; a report **with
its uncertainty**; the **research/not-guaranteed disclaimer**; **no execution controls anywhere**; and a
**logged-out block**. Keep it **presentation-only** — read the W4 APIs and format; recompute nothing; render no
raw score. Run CI via the **documented Git-Bash path** for a clean exit 0 (transcript W4-U07). Prove build
identity first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W4-U08, adopt an unspiked dependency, add
execution/broker, or open the Gate. The final Wave-4 unit follows ITRGA's verdict + a new Build Order +
operator authorization.

> **We don't guess. We prove.** — ITRGA
