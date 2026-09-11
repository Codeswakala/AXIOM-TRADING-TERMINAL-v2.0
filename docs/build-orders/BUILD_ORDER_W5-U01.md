# AXIOM BUILD ORDER — W5-U01

## Human-AI Collaboration: Collaboration Safety Foundation — Assistant Boundary + Inert Planning/Journal Contracts (no LLM, non-actuating, grounded, anti-injection)

**Build Order ID:** W5-U01
**Wave:** 5 — Human-AI Collaboration · **Unit:** 01 (safety foundation; no rich interaction)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **Wave-5 Design Plan ACCEPTED WITH REFINEMENTS (R5-1…R5-8)** + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-5 guardrails **GR-1…GR-11**; this unit carries
**R5-1, R5-2, R5-3, R5-4, R5-8** (`ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md`).
**Governing plan:** `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §3 (context), §4 (assistant
architecture), §5 (plan/journal data model), §10/§11 (W5-U01).
**Builds on:** W4 read-only intelligence APIs + advisory-signal/alert artifacts (grounding sources).
**Baseline to meet/exceed:** backend **233** / frontend **12 files · 29 tests**; Platform **v0.38.0**; head
**20260716_0023**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W5-U01 is the **safety foundation** of Wave 5 — prove the collaboration safety envelope **before** any rich
interaction, and **before** any external LLM. Three jobs only:

1. **Stand up the `collaboration` bounded context** + a **provider-neutral `AssistantPort`** with a
   **deterministic `RuleBasedGroundedAssistant`/`NullAssistant`** (no external LLM, no new/compiled dep) that is
   **structurally non-actuating** (GR-10/R5-1), **grounded-or-refuses** (R5-5), carries the **AI-generated
   research-only disclaimer** (§4.5), and **refuses prompt-injection / secret-exfiltration with audited
   refusal** (R5-3).
2. **Define the INERT trade-plan and journal contracts** (GR-9/R5-4) — schemas/contracts that **reject**
   order/sizing/account fields and trigger/execute nothing.
3. **Prove the bright line** (R5-8) — wave-wide grep, Gate CLOSED, CI via Git-Bash.

**No rich interactive feature, no external LLM, no operator-facing workspace beyond a minimal safety UI (only
if needed for evidence).** This is scaffolding + a proven safety envelope.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **Assistant must be NON-ACTUATING — structurally (R5-1/GR-10). KEYSTONE.** No assistant tool may mutate
  state, place an order, size a position, change model/config/signal/advisory-status, open the Gate, call a
  broker, fetch external data, or write outside its own audited research-artifact store. Prove by: (a) a
  **tool-registry test** asserting the allowlist contains ONLY read + own-audited-artifact-write tools;
  (b) a **grep** that the assistant/collaboration module has no order/Gate/model-mutation/broker/exec path; and
  (c) named negative tests (below). "No such tool exists" is the required design — prove the registry enforces
  it.
- ❌ **No external LLM / no new compiled or LLM/tokenizer dependency (R5-2).** W5-U01 uses the existing stack +
  deterministic local assistant logic. Any external LLM/API or model package is a **future, separately-gated
  Build Order** (spike + §77 secrets + privacy/terms + injection + redaction + no-action proof). An unspiked/
  LLM import here is an automatic FAIL.
- ❌ **Prompt-injection / secret-exfiltration must be REFUSED, with AUDITED refusal (R5-3/GR-11). MANDATORY
  NAMED TESTS.** At minimum (per §4.4): `assistant_refuses_order_instruction`,
  `assistant_refuses_gate_open_instruction`, `assistant_refuses_secret_exfiltration`,
  `assistant_refuses_unbounded_tool_request`, `assistant_response_has_grounding_or_refuses`,
  `assistant_write_limited_to_own_audited_artifact` — all PASS by name; each refusal emits an **audit event**;
  a **sampled-output secret-marker check** shows no secrets/tokens/raw internals.
- ❌ **Ungrounded assistant claim (R5-5).** An assistant response **either** cites persisted source_artifact_ids
  **or refuses** — no hallucinated signals/prices/outcomes. Prove by named test.
- ❌ **No AI output without the disclaimer (§4.5).** Every assistant response carries "AI-generated research
  assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM
  does not act." Prove by test (+ browser if any UI).
- ❌ **Plan/journal NOT inert (R5-4/GR-9). MANDATORY.** The `trade_plan_notes` and `manual_trade_journal_entries`
  contracts (and schema if persisted this unit) **reject** the forbidden fields (order_payload/order_intent/
  side/quantity/lot_size/order_size/position_size/entry_price_order/stop_loss/take_profit/broker_account_id/
  account_id/position_id/execution_status). Prove: inert schema (`\d`) if persisted + a named test that the
  contract rejects those fields + a named "**a plan/journal triggers/executes nothing / is never read by an
  exec path**" test.
- ❌ **No execution / order / broker / account / Gate path** (GR-1/GR-3). **R5-8 wave-wide grep** (command +
  output, extended verbs) — residuals limited to forbidden-key lists/benign seams, disclosed.
- ❌ **No un-audited persisted artifact (R5-7).** If any collaboration table is created this unit (e.g.
  `assistant_research_responses`), it triggers the persistence-capture control: Alembic head advance +
  committing script + **raw `psql SELECT ≥1 row`** on the correct table + **no-orphan audit JOIN** — inline. If
  contracts-only (persistence deferred to later units), **state so explicitly.**
- ❌ **No D-W2-001 breach; no client-side authoritative recompute (GR-8) if any UI.**
- ❌ **No regression** (Wave-0…W4). Full suite green + **CI via `& "C:\Program Files\Git\bin\bash.exe"
  scripts/local_ci.sh` → `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript labelled W5-U01).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic, all prior hardening,
  npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** The structural non-actuation (R5-1) + injection-refusal (R5-3) + inert
plan/journal (R5-4) proofs are the keystones.

---

## 3. Scope (Components A–D)

### A. Collaboration context + assistant boundary (backend, `collaboration`)
- `collaboration` package skeleton (reads governed artifacts; owns no feeds/broker/order/account/auth/Gate).
- `AssistantPort` + `AssistantRequest`/`AssistantResponse`/`GroundingBundle`/`AssistantSafetyPolicy` +
  deterministic `RuleBasedGroundedAssistant`/`NullAssistant`.
- **Tool allowlist:** read governed-artifact summaries + create own audited draft response ONLY (no mutating/
  order/Gate/broker/external tool exists).
- **Safety policy** (system policy not user-overridable; user text is data, not instruction); grounding-or-
  refuse; audited refusal; disclaimer on every response.

### B. Inert plan/journal contracts
- `trade_plan_notes` + `manual_trade_journal_entries` contracts (allowed vs **forbidden** fields per §5), inert
  by construction. Schema now (with R5-7 proof) OR contracts-only with schema deferred — state which.

### C. Tests (the safety proof)
- Named: the six §4.4 assistant negative tests (R5-3) + tool-registry non-actuation test (R5-1) + grounding-or-
  refuse (R5-5) + disclaimer-present + plan/journal reject-forbidden-fields + plan/journal triggers-nothing
  (R5-4). Backend (and frontend if a minimal safety UI is added).

### D. Registers/docs
- RISK (Wave-5 rows per plan §9 that apply to the foundation), CHANGELOG → **v0.39.0**, PROJECT_STATE, ADR,
  GOVERNANCE_AMENDMENTS (no amendment; Option A stands; Gate CLOSED).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W5-U01.md` + raw `operator results.md`. **Prove build identity first.**

1. **Build identity** — new files/ADR exist; v0.39.0; `git log -1 --oneline`.
2. **R5-1 structural non-actuation** — tool-registry test (allowlist = read + own-audited-write only) + grep no
   order/Gate/model-mutation/broker/exec path in the collaboration/assistant module.
3. **R5-3 injection/secret refusal** — the six named tests PASS by name; each refusal emits an audit event
   (show the event); sampled-output secret-marker check (no secrets/tokens/raw internals).
4. **R5-5 grounding-or-refuse** — named test PASSED (ungrounded → refuse).
5. **Disclaimer** — test asserting the §4.5 disclaimer on every assistant response.
6. **R5-4 inert plan/journal** — named test rejecting forbidden fields + triggers-nothing test; inert `\d`
   if persisted.
7. **R5-2 dependency discipline** — no external LLM/API; grep no unspiked/LLM import; existing stack only.
8. **R5-7 persistence** (if any table added) — Alembic head advance + committing script + **raw SELECT ≥1 row**
   + no-orphan audit; else explicit contracts-only statement.
9. **R5-8 wave-wide grep** — command + output; residuals disclosed + benign; Gate CLOSED (broker gate tests).
10. **Full regression** — backend `pytest` **≥ (233 + new)**, 0 failed; frontend green; ruff/tsc/build clean;
    npm audit 0.
11. **CI** — Git-Bash invocation → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript
    W5-U01). **Parity smoke.** Browser screenshots only if a safety UI was added.

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.39.0.
- [ ] **R5-1 (keystone):** tool-registry non-actuation test + grep (no order/Gate/mutation/broker/exec path).
- [ ] **R5-3:** six named injection/secret refusal tests PASS; audited refusal event shown; sampled secret check
      clean.
- [ ] **R5-5:** grounding-or-refuse test PASS; **disclaimer** on every assistant response.
- [ ] **R5-4:** plan/journal contracts reject forbidden fields (test) + triggers-nothing test + inert `\d`
      (if persisted).
- [ ] **R5-2:** no external LLM / no unspiked or LLM dep (grep); existing stack only.
- [ ] **R5-7:** any new collaboration table → raw SELECT ≥1 row + no-orphan audit (or explicit contracts-only).
- [ ] **R5-8:** wave-wide grep empty/benign (command+output); Gate CLOSED.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke; browser
      evidence if UI.
- [ ] DA does not self-approve, self-advance, build W5-U02+, ship an external LLM, add an actuating tool/
      execution/order/sizing/account linkage, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W5-U01, advances to **v0.39.0**, and (on operator authorization) issues `BUILD_ORDER_W5-U02.md`
(Audited Assistant Research Responses) carrying R5-3/R5-5/R5-6/R5-7.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Rich interactive features / chart assistant / annotations / workspaces (W5-U02…U07, each own Build Order).
- Any external LLM/API or new compiled/LLM dependency (future gated unit).
- Any actuating assistant tool; any execution/order/sizing/broker/account/position path; opening the Gate.
- Any plan/journal order/sizing/account field; any autonomous action.
- Any Wave-6 work.

---

## 7. Notes to the Development Authority

This is the wave's safety keystone: prove the assistant **cannot act because no action tool exists** (registry
test + grep, not just behavior tests), that it **grounds-or-refuses** and **refuses injection/secret-exfil with
an audited refusal**, and that the **plan/journal contracts are inert** (reject order/sizing/account fields;
trigger nothing). Keep it **LLM-free and dependency-clean** this slice — the external LLM is a future gated
unit, never inside a feature. Run CI via the documented Git-Bash path for a clean exit 0. Prove build identity
first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W5-U02+, ship an external LLM, add an actuating tool
or any execution/order/sizing/account linkage, or open the Gate. The next unit follows ITRGA's verdict + a new
Build Order + operator authorization.

> **We don't guess. We prove.** — ITRGA
