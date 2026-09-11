# AXIOM BUILD ORDER — W5-U07

## Human-AI Collaboration: Manual Research Journal (operator reflections, NOT a broker record — inert, BROWSER EVIDENCE MANDATORY)

**Build Order ID:** W5-U07
**Wave:** 5 — Human-AI Collaboration · **Unit:** 07
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-17
**Authorized By:** ITRGA, following **W5-U06 APPROVED — CLEAN** (Platform v0.44.0; inert trade planning) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → **`07/08_UI_UX_SPEC`** → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-5 guardrails **GR-1…GR-11** (esp. **GR-9**); this UI unit
carries **R5-4, R5-6, R5-7, R5-8** (+ **R5-1/R5-3/R5-5** IF AI-assisted) (`ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md`).
**Governing plan:** `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §5.2 (manual journal record),
§6.4 (manual journal), §10 (W5-U07).
**Builds on:** W5-U01 inert-contract pattern + W5-U06 `trade_plan_notes` (linkable) + W3/W4 read-only artifacts.
**Baseline to meet/exceed:** backend **282** / frontend **16 files · 48 tests**; Platform **v0.44.0**; head
**20260717_0026**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver a **Manual Research Journal** — persisted, operator-authored **reflection/research-log entries** (title,
reflection text, linked plan/signal/report ids, emotion/process tags, lesson notes) that help a human review
their own reasoning. **A journal entry is a research log — NOT a broker record** (plan §5.2/§6.4): it does not
import, reconcile, or store broker trades, account identifiers, execution ids, fill prices, order quantity/
position size, and **claims no P&L** (no governed outcome/account data exists). It is inert (persisting/viewing
triggers/executes nothing) and never read by any execution path. Because this is UI, **browser evidence is
mandatory** (R5-6). If AI-assisted, the assistant stays non-actuating/grounded/disclaimed/audited; no external
LLM (R5-2).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **Journal INERT / NOT a broker record (R5-4/GR-9 — KEYSTONE). MANDATORY.** `manual_trade_journal_entries`
  **allows only** research-log fields (§5.2: journal_id, created_at UTC, operator_id, title, reflection_text,
  linked_plan_id, linked_signal_ids, linked_report_ids, emotion_tags, process_tags, lesson_notes,
  research_disclaimer, audit_correlation_id) and **rejects (recursively)** broker/account/execution fields:
  broker account identifiers, `account_id`, `broker_account_id`, execution ids/`execution_status`, fill prices
  as broker records, order `quantity`/`lot_size`/`order_size`/`position_size`, order/sizing/stop/target fields,
  and **P&L/realized-return claims** (no governed outcome data exists). Prove: **inert schema** (information_
  schema forbidden-columns → **0 rows**), a **named reject-forbidden-fields test**, a **named "no P&L /
  no-broker-import" test**, and a **named "triggers-nothing / never-read-by-exec" test.**
- ❌ **No broker import / no account linkage / no execution reconciliation (§6.4).** The journal never pulls
  from a broker, reconciles fills, or links a real account/position. Prove by grep + test (+ screenshot — no
  import/broker/account UI affordance).
- ❌ **Research framing.** Entry + UI carry a research/not-instruction disclaimer (manual research reflection,
  not financial advice, not a trade record, AXIOM does not act). No guaranteed/realized-return language. Prove
  by test + screenshot.
- ❌ **No un-audited persisted entry (R5-7 — INLINE).** `manual_trade_journal_entries` triggers the
  persistence-capture control: Alembic head advance + committing script + **raw `psql SELECT ≥1 row`** on the
  table + **no-orphan audit JOIN** (`manual_trade_journal_entry.created`; `orphan_count 0`) — inline.
  `research_status`/disclaimer mandatory. (Operator-authored create is an audited write to the journal store
  only — no execution/order/signal write.)
- ❌ **Read-only reads + audited journal-store write only.** `GET` list/detail authenticated (unauth **401** /
  auth **200**); create/update via the audited journal-store path only; no execution/order/signal endpoint
  (prove absent, 405/404).
- ❌ **AI path (if present) stays safe (R5-1/R5-3/R5-5).** AI-assisted journal draft grounded-or-refuses,
  non-actuating, disclaimed, audited; no external LLM/dep (R5-2). If no AI, **state so.**
- ❌ **No execution / broker / account / Gate path** (GR-1/GR-3). **R5-8 wave-wide grep** (command + output) —
  residuals limited to forbidden-key lists/refusal codes/benign seams, disclosed. Gate CLOSED.
- ❌ **BROWSER EVIDENCE MANDATORY (R5-6).** Reachable served session: journal workspace rendering an entry
  (title/reflection/linked ids/tags/lesson notes) with **research/not-a-trade-record disclaimer**; **no broker-
  import/account/execution/P&L controls or fields**; **logged-out block**. MISSING/unreachable ⇒ WITHHELD.
- ❌ **No D-W2-001 breach; no unspiked/LLM dependency; no client-side authoritative recompute (GR-8).**
- ❌ **No regression** (Wave-0…W5-U06). Full suite green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript W5-U07).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic, all prior hardening,
  npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** Inert/not-a-broker-record (R5-4/GR-9) + browser proof (R5-6) are the
keystones.

---

## 3. Scope (Components A–D)

### A. Journal persistence (backend, `collaboration`)
- `manual_trade_journal_entries` table + Alembic migration + committing repository. Allowed fields per §5.2;
  **forbidden fields rejected recursively** (reuse W5-U01/U06 inert-contract pattern) incl. **P&L/broker/
  account/execution rejection**. Immutable `manual_trade_journal_entry.created` audit event; no orphan.
  `linked_plan_id` references a W5-U06 plan note (research link only). Update path audited, still inert.

### B. Read-only reads + audited journal-store write
- `GET /api/v1/collaboration/journal-entries` (list) + detail — authenticated, read-only. Create/update via
  audited journal-store write only; no execution/order/signal endpoint (prove absent).

### C. Presentation-only journal UI (browser-proven)
- Render/create journal entries (title/reflection/linked plan+signal+report ids/emotion+process tags/lesson
  notes) with the disclaimer; **no broker-import button, no account/execution/P&L fields**, no order/sizing
  controls.

### D. Tests + registers
- Named: R5-4 inert-schema + reject-forbidden-fields + no-P&L/no-broker-import + triggers-nothing/never-read-
  by-exec; R5-7 persistence/no-orphan; no-broker/account/execution UI (frontend); disclaimer present; read-only
  reads 401/200; no exec/order endpoint. Update RISK, CHANGELOG → **v0.45.0**, PROJECT_STATE, ADR,
  GOVERNANCE_AMENDMENTS (Option A/Gate CLOSED).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL + BROWSER)

Report `DELIVERY_REPORT_W5-U07.md` + raw `operator results.md` + **browser screenshots**. **Build identity
first.**

1. **Build identity** — new files/ADR; v0.45.0; `git log -1 --oneline`.
2. **R5-4 inert / not-a-broker-record** — information_schema forbidden-columns → **0 rows** (incl. account/
   execution/fill/quantity/position/P&L) + named reject-forbidden-fields test + named no-P&L/no-broker-import
   test + triggers-nothing/never-read-by-exec test.
3. **R5-7 persistence (inline)** — Alembic head advance + `alembic current`; committing script; **raw
   `psql SELECT ≥1 row` on `manual_trade_journal_entries`**; **no-orphan audit JOIN** (`orphan_count 0`).
4. **No broker/account/execution** — grep no broker/account/execution/P&L on the page + named frontend test.
5. **BROWSER (MANDATORY, R5-6)** — reachable served session: journal workspace rendering an entry + disclaimer;
   **no broker-import/account/execution/P&L controls**; **logged-out block**. No `ERR_CONNECTION_REFUSED`.
6. **API** — read endpoints unauth **401** / auth **200**; execution/order/signal endpoint absent (405/404);
   journal-store write audited.
7. **AI path (if present)** — grounding-or-refuse + disclaimer + audited; else state "no AI this unit."
8. **R5-2** no LLM/dep grep; **R5-8** wave-wide grep (command+output, benign); Gate CLOSED.
9. **Full regression** — backend `pytest` **≥ (282 + new)**, 0 failed; frontend **≥ (16·48 + new)**;
   ruff/tsc/build clean; npm audit 0.
10. **CI** — Git-Bash → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U07).
    **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.45.0.
- [ ] **R5-4/GR-9 (keystone):** inert schema (forbidden columns 0 rows) + reject-forbidden-fields test +
      no-P&L/no-broker-import test + triggers-nothing/never-read-by-exec test.
- [ ] **Not a broker record:** grep + frontend test + browser show no broker-import/account/execution/P&L.
- [ ] Research/not-a-trade-record disclaimer on entry + UI; no guaranteed/realized-return language.
- [ ] **R5-7:** `manual_trade_journal_entries` Alembic head advanced; committing script + **raw SELECT ≥1 row**
      + no-orphan audit JOIN (`orphan_count 0`) — inline.
- [ ] Read-only reads 401/200; execution/order/signal endpoint absent (405/404); journal-store write audited.
- [ ] **BROWSER (R5-6):** journal rendered on served session + disclaimer + no broker/account/execution/P&L
      controls + logged-out block.
- [ ] AI path (if present) grounded/non-actuating/disclaimed/audited; else stated. **R5-2** no LLM/dep;
      **R5-8** grep benign; Gate CLOSED; no D-W2-001 breach.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke.
- [ ] DA does not self-approve, self-advance, build W5-U08, ship an LLM, add an actuating tool/execution/
      order/account linkage, or open the Gate.

**A single CRITICAL, unmet mandatory evidence (incl. MISSING/UN-REACHABLE browser screenshots), or a red gate
⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA approves W5-U07, advances to **v0.45.0**, and (on operator
authorization) issues `BUILD_ORDER_W5-U08.md` (Wave-5 Closeout & Hardening — the LAST Wave-5 unit).

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Closeout (W5-U08, own Build Order).
- Any broker import / account / execution / fill / P&L / order / sizing / position field, control, or path;
  opening the Gate.
- Any external LLM/API or new compiled/LLM dependency (future gated unit).
- Any actuating tool; a journal entry read by an execution path; guaranteed/realized-return framing.
- Any Wave-6 work.

---

## 7. Notes to the Development Authority

The keystone is **a journal is a research log, not a broker record** — no account/execution/fill/quantity/
position fields, no broker import/reconciliation, and **no P&L claim** (no governed outcome data exists). Prove
it: inert schema (forbidden-columns 0 rows) + reject-forbidden-fields + a **named no-P&L/no-broker-import
test** + triggers-nothing/never-read-by-exec. As a UI unit, **prove in the browser** there is no broker-import/
account/execution/P&L affordance, plus the disclaimer and logged-out block; missing/unreachable shots ⇒
WITHHELD. Deliver the **raw SELECT + no-orphan audit inline** (R5-7). If AI-assisted, keep it grounded/non-
actuating/disclaimed/audited and LLM-free (R5-2). Run CI via the documented Git-Bash path for a clean exit 0.
Prove build identity first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W5-U08, ship an external LLM, add an actuating tool
or any broker/account/execution linkage, or open the Gate. The next unit follows ITRGA's verdict + a new Build
Order + operator authorization.

> **We don't guess. We prove.** — ITRGA
