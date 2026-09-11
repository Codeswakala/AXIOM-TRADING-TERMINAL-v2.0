# AXIOM BUILD ORDER — W5-U05

## Human-AI Collaboration: Scenario Comparison Workspace (compare EXISTING persisted scenarios only, read-only, no generation, no guarantee — BROWSER EVIDENCE MANDATORY)

**Build Order ID:** W5-U05
**Wave:** 5 — Human-AI Collaboration · **Unit:** 05
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-17
**Authorized By:** ITRGA, following **W5-U04 APPROVED — CLEAN** (Platform v0.42.0; signal investigation no-mutation) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → **`07/08_UI_UX_SPEC`** → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-5 guardrails **GR-1…GR-11**; this UI unit carries
**R5-6, R5-8** + **no-scenario-generation keystone** + **GR-7 uncertainty/no-guarantee**
(+ **R5-1/R5-3/R5-5/R5-7** IF the assistant summarizes) (`ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md`).
**Governing plan:** `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §6 (UX), §10 (W5-U05).
**Builds on:** W4-U04 `scenario_reports` (read-only) + W5-U01/U02 assistant boundary/audit (if used).
**Baseline to meet/exceed:** backend **268** / frontend **14 files · 38 tests**; Platform **v0.42.0**; head
**20260717_0025**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver a **Scenario Comparison Workspace** — a read-only operator surface to **compare two or more EXISTING
persisted scenario reports** (from W4-U04) **side by side**, showing each scenario's assumptions, hypothetical
result, **uncertainty, provenance, and hypothetical/not-guaranteed framing.** It **reads and displays** the
persisted scenarios — it **generates no new scenario**, computes no new hypothetical outcome, and implies no
guaranteed result (plan §6/§W5-U05). Because this is UI, **browser evidence is mandatory** (R5-6). If the
assistant summarizes a comparison, it stays **grounded/non-actuating/disclaimed/audited** (carried GR-10);
still **no external LLM** (R5-2).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **NO scenario generation / no new hypothetical computation (KEYSTONE). MANDATORY NAMED TEST + GREP.** The
  workspace compares **only existing persisted `scenario_reports`**; it does not create/compute a new scenario,
  outcome, or counterfactual (no call into the W4-U04 scenario **compute/create** path from this surface).
  Prove by: a **named test** that comparison reads persisted rows and **creates no new `scenario_reports` row**
  (before/after row count unchanged), and a **grep** that the comparison surface has no scenario-generation/
  compute call. Any new scenario generation is out of scope (would need separate authorization).
- ❌ **Uncertainty + provenance shown; NO guaranteed/predicted outcome (GR-7).** Every compared scenario shows
  its **uncertainty + assumptions + provenance/source ids**; the comparison never presents a scenario as a
  prediction, guarantee, or trade instruction. `limitations` (hypothetical/not-a-prediction) visible. Prove by
  test + screenshot; grep for guaranteed/expected-return language benign.
- ❌ **Read-only over existing artifacts (GR-8 presentation-only).** Reads persisted scenarios via the existing
  read-only API and **displays/compares** them; recomputes no scenario/analytics authoritatively client-side
  (a purely presentational diff/side-by-side layout is fine; an authoritative recomputation is not). Prove
  structurally (grep) + test.
- ❌ **No execution / order / broker / account / Gate / action control** (GR-1/GR-3/R-3). No buy/sell/order/
  size/execute control anywhere; **R5-8 wave-wide grep** (command + output). Gate CLOSED.
- ❌ **BROWSER EVIDENCE MANDATORY (R5-6).** Reachable served session: the comparison view rendering ≥2 existing
  scenarios side-by-side with **assumptions + uncertainty + provenance + hypothetical/not-guaranteed framing**;
  **no action controls anywhere**; **logged-out block**. MISSING/unreachable ⇒ WITHHELD (W3-U05/W0-U06).
- ❌ **No raw model score rendered.** Prove by test + screenshot.
- ❌ **Assistant-summary path (IF present) stays safe.** Grounded-or-refuses (R5-5), non-actuating (R5-1),
  disclaimer, audited (R5-3); if a summary record is persisted → persistence-capture inline (R5-7). Still no
  external LLM / new dep (R5-2). If no assistant summary, **state so explicitly.**
- ❌ **No new report type / no scenario write endpoint.** Reads only; no new persisted scenario artifact; no
  migration expected (a new table only if an assistant-summary record is added, with R5-7). State if none.
- ❌ **No D-W2-001 breach; no unspiked/LLM dependency.**
- ❌ **No regression** (Wave-0…W5-U04). Full suite green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript W5-U05).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic, all prior hardening,
  npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** No-scenario-generation + browser proof (R5-6) are the keystones.

---

## 3. Scope (Components A–C)

### A. Comparison surface (frontend + read-only backing)
- A view (e.g. `/compare-scenarios` or embedded) that lets the operator select ≥2 existing persisted scenario
  reports and displays them **side by side**: scenario name, assumptions/inputs, hypothetical result,
  uncertainty, economic-usefulness field, provenance/source ids, limitations, `research_status`.
- Uses the existing read-only `GET /api/v1/intelligence/scenario-reports` (list + detail). If a thin read-only
  comparison-bundle endpoint is needed it is read-only (401/200, POST 405/404), no new artifact, no generation.

### B. (Optional) assistant comparison summary
- If the assistant summarizes the comparison: grounded-or-refuse, non-actuating, disclaimer, audited (persisted
  via W5-U02 `assistant_research_responses` — R5-7 inline). If not, state "no assistant summary this unit."

### C. Tests + registers
- Named: no-scenario-generation (no new `scenario_reports` row; no compute call); uncertainty/provenance shown;
  no-guaranteed-outcome; presentation-only (no recompute); no-action-controls; no raw score; read-only reads
  401/200; (if assistant) grounding-or-refuse + audited. Update RISK, CHANGELOG → **v0.43.0**, PROJECT_STATE,
  ADR, GOVERNANCE_AMENDMENTS (Option A/Gate CLOSED).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL + BROWSER)

Report `DELIVERY_REPORT_W5-U05.md` + raw `operator results.md` + **browser screenshots**. **Build identity
first.**

1. **Build identity** — new files/ADR; v0.43.0; `git log -1 --oneline`.
2. **BROWSER (MANDATORY, R5-6)** — reachable served session: ≥2 existing scenarios compared side-by-side with
   assumptions + uncertainty + provenance + hypothetical/not-guaranteed framing; **no action controls**;
   **logged-out block**. No `ERR_CONNECTION_REFUSED`.
3. **No-scenario-generation (keystone)** — named test that comparison reads persisted rows and creates **no new
   `scenario_reports` row** (before/after `SELECT COUNT` unchanged) + grep no scenario-generation/compute call
   on the comparison surface.
4. **Uncertainty/provenance + no-guarantee** — test + screenshot (each scenario shows uncertainty + source ids;
   no guaranteed/predicted framing; grep benign).
5. **Presentation-only** — grep no authoritative recompute; named test.
6. **No raw score** — test + screenshot.
7. **API** — read endpoints unauth **401** / auth **200**; any added comparison endpoint POST → **405/404**;
   no scenario write/generate endpoint.
8. **Assistant path (if present)** — grounding-or-refuse + disclaimer + audited; if persisted → raw SELECT +
   no-orphan audit (R5-7). Else state "no assistant summary this unit."
9. **R5-2** no LLM/dep grep; **R5-8** wave-wide grep (command+output, benign); Gate CLOSED.
10. **Full regression** — backend `pytest` **≥ (268 + new)**, 0 failed; frontend **≥ (14·38 + new)**;
    ruff/tsc/build clean; npm audit 0; no new migration (or justified + R5-7).
11. **CI** — Git-Bash → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U05).
    **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.43.0.
- [ ] **No-scenario-generation (keystone):** named test — no new `scenario_reports` row (before/after count) +
      grep no generation/compute call.
- [ ] **BROWSER (R5-6):** ≥2 scenarios compared side-by-side (assumptions + uncertainty + provenance + not-
      guaranteed framing) on served session; **no action controls**; logged-out block.
- [ ] Uncertainty/provenance shown; **no guaranteed/predicted outcome**; **no raw score**; presentation-only
      (grep + test).
- [ ] Read-only reads 401/200; no scenario write/generate endpoint; comparison POST (if any) 405/404.
- [ ] Assistant path (if present) grounding-or-refuse + disclaimer + audited + R5-7 if persisted; else stated.
- [ ] **R5-2** no LLM/dep; **R5-8** grep benign; Gate CLOSED; no D-W2-001 breach; no new report type.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke.
- [ ] DA does not self-approve, self-advance, build W5-U06+, ship an LLM, add an actuating tool/execution/
      order/account linkage, generate a scenario, or open the Gate.

**A single CRITICAL, unmet mandatory evidence (incl. MISSING/UN-REACHABLE browser screenshots), or a red gate
⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA approves W5-U05, advances to **v0.43.0**, and (on operator
authorization) issues `BUILD_ORDER_W5-U06.md` (Inert Trade Planning Workspace) carrying R5-4/R5-6/R5-7/R5-8.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Trade plan / journal / closeout (W5-U06…U08, each own Build Order).
- **New scenario generation / computation** beyond reading existing persisted scenarios (separate
  authorization required).
- Any external LLM/API or new compiled/LLM dependency (future gated unit).
- Any actuating tool; any execution/order/sizing/broker/account/position path; opening the Gate.
- Raw-score display; guaranteed/predicted framing; client-side authoritative recompute; new report type.
- Any Wave-6 work.

---

## 7. Notes to the Development Authority

The keystone is **no scenario generation** — this surface **compares what already exists**, it does not create.
Prove it: a named test that a comparison creates **no new `scenario_reports` row** (before/after count) + a
grep that the comparison surface has no generation/compute call. Show every compared scenario **with its
uncertainty + provenance + hypothetical/not-guaranteed framing** (never a prediction), **no raw score**, and —
as a UI unit — **prove it in the browser** (≥2 scenarios side-by-side + framing + no action controls +
logged-out block); missing/unreachable shots ⇒ WITHHELD. If the assistant summarizes, keep it grounded/non-
actuating/disclaimed/audited and LLM-free (R5-2); persist with R5-7 inline. Run CI via the documented Git-Bash
path for a clean exit 0. Prove build identity first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W5-U06+, ship an external LLM, add an actuating tool
or any execution/order/account linkage, generate a scenario, or open the Gate. The next unit follows ITRGA's
verdict + a new Build Order + operator authorization.

> **We don't guess. We prove.** — ITRGA
