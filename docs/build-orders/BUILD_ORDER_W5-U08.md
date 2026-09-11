# AXIOM BUILD ORDER — W5-U08

## Human-AI Collaboration: Wave-5 Closeout & Hardening (the LAST Wave-5 unit — milestone gate)

**Build Order ID:** W5-U08
**Wave:** 5 — Human-AI Collaboration · **Unit:** 08 (FINAL)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-17
**Authorized By:** ITRGA, following **W5-U07 APPROVED — CLEAN** (Platform v0.45.0; inert journal) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-5 guardrails **GR-1…GR-11**; refinements **R5-1…R5-8**.
**Governing plan:** `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §10 (W5-U08 = full-wave no-execution/
no-action proof, assistant prompt-injection proof index, artifact-audit completeness, auth/read-only, browser
E2E, milestone candidate).
**Closes:** Wave 5 (Human-AI Collaboration) — W5-U01…U08.
**Precedent:** W3-U08 / W4-U08 (closeout = proof unit, not new surface).
**Baseline to meet/exceed:** backend **291** / frontend **53 tests**; Platform **v0.45.0**; head
**20260717_0027**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W5-U08 is a **closeout & hardening** unit, not a new feature. Its job is to **prove — end to end, on the
target — that the whole Human-AI Collaboration layer is safe, non-actuating, grounded, audited, and still
advisory-only**, reconcile docs/registers, and leave the codebase clean so ITRGA can declare the **"Human-AI
Collaborative Workspace Complete"** milestone.

Concretely, prove that the assembled collaboration surfaces (assistant boundary, audited assistant responses,
chart annotations/drawings, signal investigation, scenario comparison, trade planning, manual journal) and the
AI assistant together **cannot act, cannot be prompt-injected into acting, cannot open the Gate, cannot emit an
order/signal or touch a broker/account, and never present research as a guarantee**, and that **every
collaboration artifact is audited (no orphan) across all Wave-5 tables.** The **assistant prompt-injection
proof index (GR-10)** is the wave-defining evidence.

**No new user-facing capability is authorized.** Only genuine closeout hardening (each called out with before/
after evidence). No external LLM.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / order / sizing / broker / account / actuation path anywhere across Wave 5.** Keystone
  closeout proof. A **wave-wide structural grep** (backend + frontend) must return **command + benign output**
  (R7), including at minimum:
  `place_order|order_payload|order_intent|side|quantity|lot_size|order_size|position_size|stop_loss|take_profit|broker_account|account_id|position_id|execution_status|emit_signal|live_signal|gate_open|allow_execution|model\.status\s*=|advisory_status\s*=|auto_retrain|openai|anthropic|transformers|langchain|llama`.
  Residuals limited to the collaboration/artifact **forbidden-key lists**, **refusal reason codes**, and
  established benign seams — each disclosed.
- ❌ **Assistant NON-ACTUATING + injection-resistant (GR-10 — KEYSTONE): PROMPT-INJECTION PROOF INDEX.** A
  consolidated index re-running/collating the named refusal proofs — order-instruction, gate-open, secret-
  exfiltration, unbounded-tool, grounding-required — each **PASS + AUDITED** (`assistant.refused` with reason
  code in `audit_events`). The tool registry remains **read + own-audited-write only** (registry test). No
  external LLM (R5-2).
- ❌ **No opening of the Constitutional Governance Gate (05 v2.0 §15).** Gate CLOSED; broker gate tests pass;
  broker-seam grep empty.
- ❌ **No research shown as guaranteed/instruction; no raw score.** Collaboration surfaces keep research/
  not-instruction framing + disclaimers.
- ❌ **Artifact-audit completeness — ALL Wave-5 tables.** Every one of `assistant_research_responses`,
  `chart_research_annotations`, (`chart_research_drawings` if present), `trade_plan_notes`,
  `manual_trade_journal_entries` shows a **no-orphan audit JOIN** (each row ↔ its `*.created` event;
  `orphan_count 0`). Prove by `psql` for **all** tables.
- ❌ **No un-authenticated access; no secrets/PII** (§77). All Wave-5 read endpoints unauth → **401**; write-
  attempt on read-only / execution endpoints → **405/404**; a sampled payload shows no secrets/raw internals.
- ❌ **No new capability / new report type / new external dependency / new LLM.** Only OBS/hardening fixes
  (disclosed with before/after). A schema migration is **not expected**; if a hardening fix needs one, justify
  + persistence-capture proof.
- ❌ **No regression.** FULL suite green (Wave-0…W5-U07) — 0 failed — + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript W5-U08).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic (Option A), all prior
  hardening, npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.**

---

## 3. Scope (Components A–E)

### A. Full-wave no-execution / no-actuation / bright-line proof
- Run the §2 wave-wide grep over all `backend/app` + `frontend/src` (test/type files excluded; state
  exclusions) — command **and** output; residuals limited to forbidden-key lists/refusal codes/benign seams,
  each disclosed.
- Confirm no Wave-5 schema carries order/sizing/account/broker/execution columns (cite the collaboration
  `\d *` / information_schema); Gate remains closed (broker gate tests + broker-seam grep empty).

### B. Assistant prompt-injection proof index (GR-10 — the wave-defining evidence)
- A consolidated `docs/evidence/W5-U08_ASSISTANT_PROMPT_INJECTION_PROOF_INDEX.md` (or equivalent) mapping each
  refusal class to its named test + its audited `assistant.refused` event (reason code). Re-run the safety
  tests; show the refusal events in `audit_events`; sampled assistant output shows no secret markers. Tool
  registry non-actuation re-asserted (read + own-audited-write only).

### C. Artifact-audit completeness (all Wave-5 tables)
- For each Wave-5 collaboration table: a **no-orphan audit JOIN** + `SELECT COUNT` (`orphan_count 0`), using
  existing seeded rows or a fresh seed.

### D. Security & auth
- Auth table: all Wave-5 read endpoints unauth **401** / auth **200**; read-only/write-safe (405/404 on
  execution/order/emit); no secrets/PII sample. Dashboard/workspace logged-out blocks (browser) as applicable.

### E. Documentation, registers & closeout index
- Reconcile: `README.md`, `PROJECT_STATE.md`, `CHANGELOG.md` (→ **v0.46.0**), `04_PROJECT_ROADMAP.md` (Wave-5
  complete), `RISK_REGISTER.md`, `TECHNICAL_DEBT_REGISTER.md` (carry forward any residual honestly; note the
  external-LLM decision remains a future gated unit — R5-2), `GOVERNANCE_AMENDMENTS.md` (no amendment; Option A
  stands; Gate CLOSED — state so). ADR `ADR-054_Wave5_Closeout_and_Hardening.md` + a **Wave-5 Closeout Evidence
  Index** mapping W5-U01…U08 to verdicts + keystone safety proofs (one traceable page for the milestone).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL + BROWSER)

Report `DELIVERY_REPORT_W5-U08.md` + raw `operator results.md` + browser screenshots. **Build identity first.**

1. **Build identity** — closeout files exist; v0.46.0; `git log -1 --oneline`.
2. **Full-wave grep** (§2) — command + output; residuals disclosed + benign.
3. **Prompt-injection proof index (GR-10)** — refusal tests PASS; `SELECT … FROM audit_events WHERE
   resource_type='assistant_response'` shows `assistant.refused` with each reason code; sampled-output secret
   check clean; tool-registry non-actuation test.
4. **Artifact-audit completeness** — no-orphan JOIN + `COUNT` for **all** Wave-5 tables (`orphan 0`).
5. **Auth table** — all Wave-5 read endpoints 401/200; execution/order/emit 405/404; no secrets/PII sample.
6. **Inert-schema / gate-closed** — collaboration tables carry no order/sizing/account/execution columns;
   broker gate tests pass; broker-seam grep empty.
7. **Full regression** — backend `pytest` **≥291 (+ any hardening)**, 0 failed; frontend **≥53**;
   ruff/tsc/build clean; npm audit 0; no new migration (or justified + proof).
8. **CI** — Git-Bash → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U08).
9. **Browser E2E** — collaboration surfaces reachable + research framing + no action controls + logged-out
   block(s), as applicable. **Parity smoke.**
10. **Docs/registers** — diff summary (v0.46.0, Wave-5 complete, Option A/Gate CLOSED, external-LLM future-
    gated) + ADR-054 + Wave-5 Closeout Evidence Index.

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.46.0.
- [ ] **Full-wave bright-line grep** empty/benign (command+output); collaboration schemas inert; Gate CLOSED
      (broker tests + seam grep empty).
- [ ] **Prompt-injection proof index (GR-10):** each refusal class PASS + audited (`assistant.refused` reason
      codes); tool-registry non-actuation; no secret leakage; no external LLM.
- [ ] **Artifact-audit completeness:** all Wave-5 tables no-orphan JOIN (`orphan_count 0`).
- [ ] **Auth:** all Wave-5 endpoints 401/200; execution/order/emit 405/404; no secrets/PII.
- [ ] No new capability/report type/dependency/LLM; no new migration (or justified).
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke; browser
      E2E where applicable.
- [ ] Docs/registers reconciled (v0.46.0, Wave-5 complete, Option A/Gate CLOSED); ADR-054 + Wave-5 Closeout
      Evidence Index present.
- [ ] DA does not self-approve, self-advance, self-declare the milestone, ship an LLM, add an actuating tool/
      execution/order/account linkage, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W5-U08, advances to **v0.46.0**, and declares the **"Human-AI Collaborative Workspace Complete"**
milestone.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Any new collaboration capability / report type / operator feature beyond OBS/hardening.
- Any external LLM/API or new compiled/LLM dependency (future gated unit).
- Any actuating assistant tool; any execution/order/sizing/broker/account/position path; opening the Gate.
- Any Wave-6 work; self-declaring the milestone (ITRGA authority).

---

## 7. Notes to the Development Authority

This is a **proof unit**: the deliverable is incontrovertible evidence that the whole Human-AI Collaboration
layer is safe and non-actuating — the assistant **cannot be prompt-injected into acting** (proof index: each
refusal class PASS + audited), every collaboration artifact is audited across **all** Wave-5 tables (no
orphan), the auth line holds (401/200; execution/emit 405/404), and no external LLM entered. Mirror the
W3-U08/W4-U08 closeout rigor: prove build identity first, run the wave-wide grep with command + output
(residuals = forbidden-key lists/refusal codes/benign seams, disclosed), and reconcile docs honestly. Run CI
via the documented Git-Bash path for a clean exit 0.

DA does not self-approve, self-advance the version, self-declare the milestone, begin any Wave-6 work, ship an
external LLM, add an actuating tool/execution/order/account linkage, or open the Gate. The milestone
declaration follows ITRGA's verdict.

> **We don't guess. We prove.** — ITRGA
