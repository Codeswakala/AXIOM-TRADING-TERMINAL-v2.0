# AXIOM BUILD ORDER — W5-U03

## Human-AI Collaboration: Chart Research Annotations & Drawing Tools (inert, presentation-only, no execution — BROWSER EVIDENCE MANDATORY)

**Build Order ID:** W5-U03
**Wave:** 5 — Human-AI Collaboration · **Unit:** 03 (first Wave-5 operator UI)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W5-U02 APPROVED — CLEAN** (Platform v0.40.0; audited assistant responses) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → **`07/08_UI_UX_SPEC`** → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-5 guardrails **GR-1…GR-11**; this UI unit carries
**R5-4, R5-6, R5-7, R5-8** (+ **R5-3/R5-5** IF annotations are AI-assisted) (`ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md`).
**Governing plan:** `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §6.2 (chart annotations), §7
(`chart_research_annotations`/`chart_research_drawings`), §10 (W5-U03).
**Builds on:** W0-U07 chart foundation + W5-U01/U02 collaboration context/audit + W4/W3 read-only artifacts.
**Baseline to meet/exceed:** backend **257** / frontend **12 files · 29 tests**; Platform **v0.40.0**; head
**20260717_0024**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver **chart research annotations & drawing tools** — operator-authored (and, optionally, AI-assisted)
**inert research markups** on the chart, **linked to persisted source artifacts**, persisted and auditable,
displayed **presentation-only**. An annotation/drawing is a **research note on a chart — never an order ticket,
signal, price target for execution, or instruction** (plan §6.2). Because this is UI, **browser evidence is
mandatory** (R5-6, W3-U05/W0-U06 precedent).

If any annotation is **AI-assisted**, the assistant remains **non-actuating, grounded-or-refuses, disclaimed,
and audited** (R5-1/R5-3/R5-5 carried from W5-U01/U02); still **no external LLM** (R5-2).

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **Annotations/drawings are INERT (R5-4/GR-9). MANDATORY.** No annotation/drawing may carry an order/sizing/
  execution/account/position/signal payload or be an instruction. Prove: **inert schema** (`\d` shows none of
  order_payload/side/quantity/position_size/stop_loss/take_profit/broker_account_id/account_id/position_id/
  execution_status), a **named test** the contract rejects those fields, and a **named "triggers-nothing"**
  test (persisting/viewing an annotation executes/emits nothing).
- ❌ **BROWSER EVIDENCE MANDATORY (R5-6).** From a reachable served session: annotations/drawings rendered on
  the chart, **research/not-instruction disclaimer** visible, **no execution/order controls anywhere**, and
  **logged-out block** on the route. MISSING/unreachable screenshots ⇒ WITHHELD (W3-U05/W0-U06).
- ❌ **Presentation-only — no client-side authoritative recompute (GR-8).** The surface **displays** persisted
  annotations/chart context + read-only artifacts; it must not recompute inference/analytics/signals
  authoritatively in the browser. Prove structurally (grep) + test.
- ❌ **No predictive guarantee / no raw score.** Annotations carry research text + source ids + uncertainty/
  provenance where relevant; **no guaranteed/predicted outcome**, no raw model score rendered. Prove by test +
  screenshot.
- ❌ **No un-audited persisted artifact (R5-7 — INLINE).** New `chart_research_annotations` (and
  `chart_research_drawings` if separate) table(s) trigger the persistence-capture control: Alembic head advance
  + committing script + **raw `psql SELECT ≥1 row`** on the correct table + **no-orphan audit JOIN**
  (`chart_research_annotation.created`; `orphan_count 0`) — inline. `research_status` mandatory; source
  artifact ids in lineage.
- ❌ **AI-assisted path (if present) stays safe (R5-3/R5-5/R5-1).** Any AI-generated annotation is grounded-or-
  refuses, carries the disclaimer, is audited, and the assistant remains non-actuating; refusals audited. If no
  AI in this unit, state so.
- ❌ **No external LLM / new compiled or LLM dependency (R5-2).** Existing stack only.
- ❌ **No execution / order / broker / account / Gate path** (GR-1/GR-3). **R5-8 wave-wide grep** (command +
  output, extended verbs) — residuals limited to forbidden-key lists/refusal codes/benign seams, disclosed.
- ❌ **Authenticated; logged-out blocked; read-only API** for reads (unauth 401 / auth 200; annotation
  create/update is operator-authored via an audited write confined to the annotation store — no execution/
  signal write). **No D-W2-001 breach.**
- ❌ **No regression** (Wave-0…W5-U02). Full suite green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript W5-U03).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic, all prior hardening,
  npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** Inert annotations (R5-4) + browser proof (R5-6) are the keystones.

---

## 3. Scope (Components A–D)

### A. Annotation/drawing persistence (backend, `collaboration`)
- `chart_research_annotations` (+ `chart_research_drawings` if separate) + Alembic migration + committing
  repository. Fields per §6.2/§7 common contract: `id, created_at(UTC), operator_id/actor, artifact_type,
  chart_context (symbol/timeframe/anchor), content (research text/shape), source_artifact_ids, provenance,
  uncertainty (where relevant), disclaimer, research_status, audit_correlation_id`. **No order/sizing/account/
  execution/signal field.** Immutable audit event on create; no orphan.

### B. Read-only reads + audited operator-authored write
- `GET /api/v1/collaboration/chart-annotations` (list) + detail — authenticated, read-only for reads.
- Operator-authored create is an **audited write to the annotation store only** (no execution/signal write);
  unauth blocked. No mutating tool beyond the annotation store.

### C. Presentation-only chart UI (browser-proven)
- Render annotations/drawings on the chart (presentation-only, no client recompute), with disclaimer + source
  linkage; **no execution/order controls; no raw score**. Drawing tools produce inert research markups only.

### D. Tests + registers
- Named: R5-4 inert-schema + reject-forbidden-fields + triggers-nothing; R5-7 persistence/no-orphan;
  presentation-only (no recompute); disclaimer present; no-execution-controls; read-only reads 401/200; (if AI)
  grounding-or-refuse + refusal audited. Update RISK, CHANGELOG → **v0.41.0**, PROJECT_STATE, ADR,
  GOVERNANCE_AMENDMENTS (Option A/Gate CLOSED).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL + BROWSER)

Report `DELIVERY_REPORT_W5-U03.md` + raw `operator results.md` + **browser screenshots**. **Build identity
first.**

1. **Build identity** — new files/ADR; v0.41.0; `git log -1 --oneline`.
2. **BROWSER (MANDATORY, R5-6)** — reachable served session: (a) annotations/drawings rendered on the chart;
   (b) research/not-instruction disclaimer; (c) **no execution/order controls** anywhere; (d) **logged-out
   block** on the route. No `ERR_CONNECTION_REFUSED`.
3. **R5-4 inert** — inert `\d chart_research_annotations` (no forbidden fields) + named reject-forbidden-fields
   test + triggers-nothing test.
4. **R5-7 persistence (inline)** — Alembic head advance + `alembic current`; committing script; **raw
   `psql SELECT ≥1 row`** on `chart_research_annotations`; **no-orphan audit JOIN** (`orphan_count 0`).
5. **Presentation-only** — grep no authoritative recompute in the annotation page; named test.
6. **No raw score / no guarantee** — test + screenshot.
7. **AI path (if present)** — grounding-or-refuse + disclaimer + audited refusal; else state "no AI this unit."
8. **API** — read endpoints unauth **401** / auth **200**; no execution/signal write endpoint.
9. **R5-2** no LLM/dep grep; **R5-8** wave-wide grep (command+output, benign); Gate CLOSED.
10. **Full regression** — backend `pytest` **≥ (257 + new)**, 0 failed; frontend **≥ (12·29 + new UI/tests)**;
    ruff/tsc/build clean; npm audit 0.
11. **CI** — Git-Bash → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U03).
    **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.41.0.
- [ ] **BROWSER (R5-6):** annotations rendered on served chart; disclaimer; **no execution controls**;
      logged-out block. (No unreachable/missing shots.)
- [ ] **R5-4:** inert `\d` (no order/sizing/account/execution/signal cols) + reject-forbidden-fields test +
      triggers-nothing test.
- [ ] **R5-7:** `chart_research_annotations` Alembic head advanced; committing script + **raw SELECT ≥1 row** +
      no-orphan audit JOIN (`orphan_count 0`) — inline.
- [ ] Presentation-only (grep + test); no raw score; no guaranteed/predicted framing.
- [ ] AI path (if present) grounding-or-refuse + disclaimer + audited refusal; else "no AI this unit" stated.
- [ ] Read-only reads 401/200; no execution/signal write endpoint; **R5-2** no LLM/dep; **R5-8** grep benign;
      Gate CLOSED; no D-W2-001 breach.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke.
- [ ] DA does not self-approve, self-advance, build W5-U04+, ship an LLM, add an actuating tool/execution/
      order/account linkage, or open the Gate.

**A single CRITICAL, unmet mandatory evidence (incl. MISSING/UN-REACHABLE browser screenshots), or a red gate
⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA approves W5-U03, advances to **v0.41.0**, and (on operator
authorization) issues `BUILD_ORDER_W5-U04.md` (Signal Investigation Workspace).

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Signal investigation / scenario comparison / trade plan / journal / closeout (W5-U04…U08, each own Build Order).
- Any external LLM/API or new compiled/LLM dependency (future gated unit).
- Any actuating tool; any execution/order/sizing/broker/account/position path; opening the Gate.
- Annotations as order tickets / instructions / price targets for execution; raw-score display; guaranteed
  outcomes; client-side authoritative recompute.
- Any Wave-6 work.

---

## 7. Notes to the Development Authority

First Wave-5 UI — so it is **judged in the browser** (R5-6): a correct implementation still FAILS if the
screenshots are missing, sandbox-only, or show an unreachable page. Show annotations rendered on a served
chart, the research/not-instruction disclaimer, **no execution controls anywhere**, and the logged-out block.
Keep annotations **inert** (reject order/sizing/account fields; trigger nothing) and **presentation-only** (no
client recompute; no raw score). Deliver the **raw SELECT + no-orphan audit inline** (R5-7). If any annotation
is AI-assisted, the assistant stays non-actuating/grounded/disclaimed/audited; still no external LLM (R5-2).
Run CI via the documented Git-Bash path for a clean exit 0. Prove build identity first; disclose grep residuals
with output.

DA does not self-approve, self-advance the version, build W5-U04+, ship an external LLM, add an actuating tool
or any execution/order/account linkage, or open the Gate. The next unit follows ITRGA's verdict + a new Build
Order + operator authorization.

> **We don't guess. We prove.** — ITRGA
