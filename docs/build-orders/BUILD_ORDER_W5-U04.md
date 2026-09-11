# AXIOM BUILD ORDER — W5-U04

## Human-AI Collaboration: Signal Investigation Workspace (read-only, explains lineage/guardrails, NO signal mutation — BROWSER EVIDENCE MANDATORY)

**Build Order ID:** W5-U04
**Wave:** 5 — Human-AI Collaboration · **Unit:** 04
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-17
**Authorized By:** ITRGA, following **W5-U03 APPROVED — CLEAN** (Platform v0.41.0; inert chart annotations) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → **`07/08_UI_UX_SPEC`** → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-5 guardrails **GR-1…GR-11**; this UI unit carries
**R5-6, R5-8** + **no-signal-mutation keystone** (+ **R5-1/R5-3/R5-5/R5-7** IF the assistant summarizes)
(`ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md`).
**Governing plan:** `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §6.5 (signal investigation view), §10
(W5-U04).
**Builds on:** W3-U02+ advisory signals/guardrails/rationale/lineage + W4 intelligence reports (read-only) +
W5-U01/U02 assistant boundary/audit (if used).
**Baseline to meet/exceed:** backend **264** / frontend **13 files · 33 tests**; Platform **v0.41.0**; head
**20260717_0025**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver a **Signal Investigation Workspace** — a read-only operator surface to **explore an advisory signal's
rationale, guardrail states, lineage, and linked intelligence reports** (plan §6.5). It **reads existing
signal/intelligence artifacts and explains them** — it **mutates no signal**, emits nothing, and adds no
execution/action controls. If the assistant is used to **summarize**, it may summarize **only grounded
artifacts** (carried GR-10: non-actuating, grounding-or-refuse, disclaimer, audited); still **no external LLM**
(R5-2). Because this is UI, **browser evidence is mandatory** (R5-6).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **NO signal mutation (KEYSTONE). MANDATORY NAMED TEST + GREP.** Investigating a signal changes/mutates/
  re-emits/re-grades nothing (no `advisory_status =`, `model.status =`, signal edit, re-run, or guardrail
  override). Prove by a named "**investigation triggers/mutates nothing**" test (W3-U06 changes-nothing
  keystone) + grep (`advisory_status\s*=|model\.status\s*=|emit_signal|place_order|update.*signal`) benign.
- ❌ **Read-only over existing artifacts (GR-8 presentation-only).** The workspace **reads** persisted signals/
  guardrails/rationale/lineage/intelligence reports via read-only APIs and **displays/explains** them; it
  recomputes no inference/analytics/guardrail authoritatively client-side. Prove structurally (grep) + test.
- ❌ **No execution / order / broker / account / Gate / action control** (GR-1/GR-3/R-3). No buy/sell/order/
  broker/size/execute/act control anywhere; **R5-8 wave-wide grep** (command + output). Gate CLOSED.
- ❌ **BROWSER EVIDENCE MANDATORY (R5-6).** Reachable served session: the investigation view rendering a
  signal's rationale + guardrail states + lineage/linked reports; **research/not-instruction framing**;
  **calibrated confidence (no raw score)**; **no action controls anywhere**; **logged-out block** on the route.
  MISSING/unreachable ⇒ WITHHELD (W3-U05/W0-U06).
- ❌ **No raw model score rendered.** Confidence shown calibrated (W3-U07/W4-U06/W5-U02 standard). Prove by
  test + screenshot.
- ❌ **Assistant-summary path (IF present) stays safe.** Any assistant summary is **grounded-or-refuses (R5-5)**,
  **non-actuating (R5-1)**, carries the **disclaimer**, and is **audited (R5-3)** with refusals recorded; still
  **no external LLM / new dep (R5-2)**. If a summary record is persisted → **persistence-capture inline (R5-7)**
  (raw SELECT + no-orphan audit). If no assistant summary this unit, **state so explicitly.**
- ❌ **No new report type / no signal write endpoint.** Reads only; no new persisted analytical/signal artifact
  (a new table only if an assistant-summary record is added, with R5-7). No migration expected — state if none.
- ❌ **No D-W2-001 breach; no unspiked/LLM dependency.**
- ❌ **No regression** (Wave-0…W5-U03). Full suite green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript W5-U04).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic, all prior hardening,
  npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** No-signal-mutation + browser proof (R5-6) are the keystones.

---

## 3. Scope (Components A–C)

### A. Signal investigation surface (frontend + read-only backing)
- A view (e.g. `/investigate` or embedded) that, for a selected signal, displays: **rationale, guardrail
  states (domain/calibration/economic/freshness), advisory-status lifecycle, lineage (model/experiment/
  feature-set/report ids), linked intelligence reports** — read-only, presentation-only.
- Uses existing read-only APIs (signals history/detail, alerts, analytics, intelligence reports). If a thin
  read-only aggregation endpoint is needed it is read-only (401/200, POST 405/404), no new artifact.

### B. (Optional) assistant summary
- If the assistant summarizes the investigation: grounded-or-refuse, non-actuating, disclaimer, audited
  (persisted via W5-U02 `assistant_research_responses` — R5-7 inline). If not, state "no assistant summary this
  unit."

### C. Tests + registers
- Named: no-signal-mutation / triggers-nothing; presentation-only (no recompute); no-action-controls; no raw
  score; read-only reads 401/200; (if assistant) grounding-or-refuse + audited. Update RISK, CHANGELOG →
  **v0.42.0**, PROJECT_STATE, ADR, GOVERNANCE_AMENDMENTS (Option A/Gate CLOSED).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL + BROWSER)

Report `DELIVERY_REPORT_W5-U04.md` + raw `operator results.md` + **browser screenshots**. **Build identity
first.**

1. **Build identity** — new files/ADR; v0.42.0; `git log -1 --oneline`.
2. **BROWSER (MANDATORY, R5-6)** — reachable served session: investigation view rendering rationale + guardrail
   states + lineage/linked reports; research/not-instruction framing; **calibrated confidence, no raw score**;
   **no action controls anywhere**; **logged-out block**. No `ERR_CONNECTION_REFUSED`.
3. **No-signal-mutation** — named "investigation mutates/triggers nothing" test + grep
   (`advisory_status =|model.status =|emit_signal|place_order|update.*signal`) benign; optionally show a
   `SELECT` that the investigated signal's row is unchanged after investigation.
4. **Presentation-only** — grep no authoritative recompute in the investigation page; named test.
5. **No raw score** — test + screenshot (calibrated only).
6. **API** — read endpoints unauth **401** / auth **200**; any added aggregation POST → **405/404**; no signal
   write endpoint.
7. **Assistant path (if present)** — grounding-or-refuse + disclaimer + audited refusal; if summary persisted →
   raw SELECT + no-orphan audit (R5-7). Else state "no assistant summary this unit."
8. **R5-2** no LLM/dep grep; **R5-8** wave-wide grep (command+output, benign); Gate CLOSED.
9. **Full regression** — backend `pytest` **≥ (264 + new)**, 0 failed; frontend **≥ (13·33 + new)**;
   ruff/tsc/build clean; npm audit 0; no new migration (or justified + R5-7 proof).
10. **CI** — Git-Bash → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U04).
    **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.42.0.
- [ ] **No-signal-mutation (keystone):** named triggers-nothing test + benign grep (+ optional unchanged-row
      SELECT).
- [ ] **BROWSER (R5-6):** investigation view rendered on served session (rationale + guardrails + lineage);
      research framing; **calibrated confidence, no raw score**; **no action controls**; logged-out block.
- [ ] Presentation-only (grep + test); read-only reads 401/200; no signal write endpoint.
- [ ] Assistant path (if present) grounding-or-refuse + disclaimer + audited + R5-7 if persisted; else stated.
- [ ] **R5-2** no LLM/dep; **R5-8** grep benign; Gate CLOSED; no D-W2-001 breach; no new report type.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke.
- [ ] DA does not self-approve, self-advance, build W5-U05+, ship an LLM, add an actuating tool/execution/
      order/account linkage, mutate a signal, or open the Gate.

**A single CRITICAL, unmet mandatory evidence (incl. MISSING/UN-REACHABLE browser screenshots), or a red gate
⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA approves W5-U04, advances to **v0.42.0**, and (on operator
authorization) issues `BUILD_ORDER_W5-U05.md` (Scenario Comparison Workspace).

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Scenario comparison / trade plan / journal / closeout (W5-U05…U08, each own Build Order).
- Any signal mutation / re-emission / guardrail override / re-grade.
- Any external LLM/API or new compiled/LLM dependency (future gated unit).
- Any actuating tool; any execution/order/sizing/broker/account/position path; opening the Gate.
- Raw-score display; guaranteed/predicted framing; client-side authoritative recompute; new report type.
- Any Wave-6 work.

---

## 7. Notes to the Development Authority

This surface **explains signals; it must never touch them.** The keystone is **no-signal-mutation** — prove by
a named triggers-nothing test + a benign mutation grep (and, ideally, an unchanged-row SELECT after
investigation). Keep it **read-only / presentation-only** (no client recompute), show **calibrated confidence,
never raw score**, and — as a UI unit — **prove it in the browser** (rendered view + framing + no action
controls + logged-out block); missing/unreachable shots ⇒ WITHHELD. If the assistant summarizes, it stays
grounded/non-actuating/disclaimed/audited and LLM-free (R5-2); persist any summary with R5-7 inline. Run CI via
the documented Git-Bash path for a clean exit 0. Prove build identity first; disclose grep residuals with
output.

DA does not self-approve, self-advance the version, build W5-U05+, ship an external LLM, add an actuating tool
or any execution/order/account linkage, mutate a signal, or open the Gate. The next unit follows ITRGA's
verdict + a new Build Order + operator authorization.

> **We don't guess. We prove.** — ITRGA
