# AXIOM BUILD ORDER — W5-U06

## Human-AI Collaboration: Inert Trade Planning Workspace (research notes only, NOT an order ticket — GR-9 keystone, BROWSER EVIDENCE MANDATORY)

**Build Order ID:** W5-U06
**Wave:** 5 — Human-AI Collaboration · **Unit:** 06
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-17
**Authorized By:** ITRGA, following **W5-U05 APPROVED — CLEAN** (Platform v0.43.0; scenario comparison, no-generation) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → **`07/08_UI_UX_SPEC`** → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-5 guardrails **GR-1…GR-11** (esp. **GR-9**); this UI unit
carries **R5-4, R5-6, R5-7, R5-8** (+ **R5-1/R5-3/R5-5** IF AI-assisted) (`ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md`).
**Governing plan:** `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §5.1 (inert trade plan record),
§6.3 (trade planning workspace), §10 (W5-U06).
**Builds on:** W5-U01 inert contract pattern + W3/W4 read-only artifacts (linkable) + W5-U03 annotation/audit
precedent.
**Baseline to meet/exceed:** backend **273** / frontend **15 files · 43 tests**; Platform **v0.43.0**; head
**20260717_0025**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver an **Inert Trade Planning Workspace** — persisted, operator-authored **hypothetical research plan
notes** (title, market context, hypothesis, linked signal/report ids, scenario/risk notes, invalidating
conditions, decision status) that help a human reason about a plan. **A trade plan here is a research note —
NOT an order ticket** (plan §5.1/§6.3). It **carries no order/sizing/quantity/stop/target/broker/account/
position/execution field**, **triggers/executes nothing**, and is **never read by any execution path**. This
is the **GR-9 keystone surface** — the one whose name most invites confusion with execution, so the inert
proof is paramount. Because this is UI, **browser evidence is mandatory** (R5-6), and it must show **no
order-ticket patterns** (no buy/sell buttons, no quantity/SL/TP/position controls).

If AI-assisted (drafting a plan note), the assistant stays **non-actuating, grounded-or-refuses, disclaimed,
audited** (carried GR-10); still **no external LLM** (R5-2).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **Trade plan INERT (R5-4/GR-9 — KEYSTONE). MANDATORY.** `trade_plan_notes` **allows only** research-note
  fields (§5.1: plan_id, created_at/updated_at UTC, operator_id, title, market_context, hypothesis,
  linked_signal_ids, linked_report_ids, scenario_notes, risk_notes, invalidating_conditions_text,
  decision_status ∈ {draft|archived|reviewed}, research_disclaimer, audit_correlation_id) and **rejects
  (recursively)** the forbidden fields (order_payload, order_intent, side, quantity, lot_size, order_size,
  position_size, entry_price_order, stop_loss, take_profit, broker_account_id, account_id, position_id,
  execution_status). Prove: **inert schema** (`\d`/information_schema query showing forbidden columns **0
  rows**), a **named reject-forbidden-fields test**, and a **named "a plan triggers/executes nothing / is
  never read by an exec path" test.**
- ❌ **NOT an order ticket — no order-ticket UI patterns (§6.3).** No buy/sell buttons, no quantity/SL/TP/
  position/size/execute controls, no order-entry affordance anywhere on the workspace. Prove by grep + named
  frontend test + **browser screenshot.**
- ❌ **Hypothetical/research framing.** The plan note + UI carry a research/not-instruction disclaimer
  (hypothetical, not financial advice, not a trade instruction, AXIOM does not act). No guaranteed/expected-
  return language. Prove by test + screenshot.
- ❌ **No un-audited persisted plan (R5-7 — INLINE).** `trade_plan_notes` triggers the persistence-capture
  control: Alembic head advance + committing script + **raw `psql SELECT ≥1 row`** on `trade_plan_notes` +
  **no-orphan audit JOIN** (`trade_plan_note.created`; `orphan_count 0`) — inline. `research_status`/disclaimer
  mandatory. (Operator-authored create is an audited write to the plan store only — no execution/order/signal
  write.)
- ❌ **Read-only reads + audited plan-store write only.** `GET` list/detail authenticated (unauth **401** /
  auth **200**); create/update via the audited plan-store path only; no execution/order/signal endpoint (prove
  absent, e.g. `/execute`/`/submit` → 405/404).
- ❌ **AI path (if present) stays safe (R5-1/R5-3/R5-5).** AI-drafted plan note grounded-or-refuses,
  non-actuating, disclaimed, audited; still no external LLM/dep (R5-2). If no AI, **state so.**
- ❌ **No execution / broker / account / Gate path** (GR-1/GR-3). **R5-8 wave-wide grep** (command + output,
  extended verbs) — residuals limited to forbidden-key lists/refusal codes/benign seams, disclosed. Gate CLOSED.
- ❌ **BROWSER EVIDENCE MANDATORY (R5-6).** Reachable served session: plan workspace rendering a plan note
  (title/hypothesis/linked ids/risk notes) with **hypothetical/not-instruction disclaimer**; **no order-ticket
  patterns / no buy-sell/quantity/SL-TP/execution controls**; **logged-out block**. MISSING/unreachable ⇒
  WITHHELD (W3-U05/W0-U06).
- ❌ **No D-W2-001 breach; no unspiked/LLM dependency; no client-side authoritative recompute (GR-8).**
- ❌ **No regression** (Wave-0…W5-U05). Full suite green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript W5-U06).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic, all prior hardening,
  npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** Inert plan (R5-4/GR-9) + no-order-ticket browser proof (R5-6) are the
keystones.

---

## 3. Scope (Components A–D)

### A. Trade plan persistence (backend, `collaboration`)
- `trade_plan_notes` table + Alembic migration + committing repository. Allowed fields per §5.1; **forbidden
  fields rejected recursively** (reuse the W5-U01/U03 inert-contract pattern). Immutable `trade_plan_note.
  created` audit event on create; no orphan by construction. Update path audited (`…updated`), still inert.

### B. Read-only reads + audited plan-store write
- `GET /api/v1/collaboration/trade-plans` (list) + detail — authenticated, read-only. Create/update via audited
  plan-store write only; no execution/order/signal endpoint (prove absent).

### C. Presentation-only planning UI (browser-proven)
- Render/create plan notes (title/market_context/hypothesis/linked signal+report ids/scenario+risk notes/
  invalidating conditions/decision status) with the disclaimer; **no order-ticket patterns** (no buy/sell,
  quantity, SL/TP, position, execute). Operator may **link** persisted research artifacts and write text only.

### D. Tests + registers
- Named: R5-4 inert-schema + reject-forbidden-fields + triggers-nothing/never-read-by-exec; R5-7 persistence/
  no-orphan; no-order-ticket-controls (frontend); disclaimer present; read-only reads 401/200; no exec/order
  endpoint. Update RISK, CHANGELOG → **v0.44.0**, PROJECT_STATE, ADR, GOVERNANCE_AMENDMENTS (Option A/Gate
  CLOSED).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL + BROWSER)

Report `DELIVERY_REPORT_W5-U06.md` + raw `operator results.md` + **browser screenshots**. **Build identity
first.**

1. **Build identity** — new files/ADR; v0.44.0; `git log -1 --oneline`.
2. **R5-4 inert** — inert schema proof (information_schema forbidden-columns → **0 rows**) + named
   reject-forbidden-fields test + triggers-nothing/never-read-by-exec test.
3. **R5-7 persistence (inline)** — Alembic head advance + `alembic current`; committing script; **raw
   `psql SELECT ≥1 row` on `trade_plan_notes`**; **no-orphan audit JOIN** (`trade_plan_note.created`,
   `orphan_count 0`).
4. **No order-ticket** — grep no buy/sell/order/quantity/SL/TP/position/execute control on the page + named
   frontend test.
5. **BROWSER (MANDATORY, R5-6)** — reachable served session: plan workspace rendering a plan note + disclaimer;
   **no order-ticket patterns / no execution controls**; **logged-out block**. No `ERR_CONNECTION_REFUSED`.
6. **API** — read endpoints unauth **401** / auth **200**; execution/order/signal endpoint absent (405/404);
   plan-store write audited.
7. **AI path (if present)** — grounding-or-refuse + disclaimer + audited; else state "no AI this unit."
8. **R5-2** no LLM/dep grep; **R5-8** wave-wide grep (command+output, benign); Gate CLOSED.
9. **Full regression** — backend `pytest` **≥ (273 + new)**, 0 failed; frontend **≥ (15·43 + new)**;
   ruff/tsc/build clean; npm audit 0.
10. **CI** — Git-Bash → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U06).
    **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.44.0.
- [ ] **R5-4/GR-9 (keystone):** inert schema (forbidden columns 0 rows) + reject-forbidden-fields test +
      triggers-nothing/never-read-by-exec test.
- [ ] **No order-ticket:** grep + frontend test + browser show no buy/sell/quantity/SL/TP/position/execute
      controls.
- [ ] Hypothetical/not-instruction disclaimer on plan note + UI; no guaranteed-return language.
- [ ] **R5-7:** `trade_plan_notes` Alembic head advanced; committing script + **raw SELECT ≥1 row** + no-orphan
      audit JOIN (`orphan_count 0`) — inline.
- [ ] Read-only reads 401/200; execution/order/signal endpoint absent (405/404); plan-store write audited.
- [ ] **BROWSER (R5-6):** plan workspace rendered on served session + disclaimer + no order-ticket/exec
      controls + logged-out block.
- [ ] AI path (if present) grounded/non-actuating/disclaimed/audited; else stated. **R5-2** no LLM/dep;
      **R5-8** grep benign; Gate CLOSED; no D-W2-001 breach.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke.
- [ ] DA does not self-approve, self-advance, build W5-U07+, ship an LLM, add an actuating tool/execution/
      order/sizing/account linkage, or open the Gate.

**A single CRITICAL, unmet mandatory evidence (incl. MISSING/UN-REACHABLE browser screenshots), or a red gate
⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA approves W5-U06, advances to **v0.44.0**, and (on operator
authorization) issues `BUILD_ORDER_W5-U07.md` (Manual Research Journal) carrying R5-4/R5-6/R5-7/R5-8.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Journal / closeout (W5-U07/U08, each own Build Order).
- Any order-ticket / order/sizing/quantity/SL/TP/position/account/broker/execution field, control, or path;
  opening the Gate.
- Any external LLM/API or new compiled/LLM dependency (future gated unit).
- Any actuating tool; a plan note read by an execution path; guaranteed/expected-return framing.
- Any Wave-6 work.

---

## 7. Notes to the Development Authority

This is **the** name that most invites confusion with execution — so the bar is: **a trade plan is a research
note that structurally cannot be an order.** Prove it three ways (inert schema forbidden-columns 0 rows +
reject-forbidden-fields test + triggers-nothing/never-read-by-exec test), reuse the W5-U01/U03 inert-contract
pattern, and — as a UI unit — **prove in the browser there are NO order-ticket patterns** (no buy/sell,
quantity, SL/TP, position, execute) plus the disclaimer and logged-out block; missing/unreachable shots ⇒
WITHHELD. Deliver the **raw SELECT + no-orphan audit inline** (R5-7). If AI-assisted, keep it grounded/non-
actuating/disclaimed/audited and LLM-free (R5-2). Run CI via the documented Git-Bash path for a clean exit 0.
Prove build identity first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W5-U07+, ship an external LLM, add an actuating tool
or any order/execution/account linkage, or open the Gate. The next unit follows ITRGA's verdict + a new Build
Order + operator authorization.

> **We don't guess. We prove.** — ITRGA
