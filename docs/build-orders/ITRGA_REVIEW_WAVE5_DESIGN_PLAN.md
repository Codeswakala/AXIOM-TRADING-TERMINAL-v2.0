# ITRGA CONSTITUTIONAL REVIEW — WAVE 5 DESIGN PLAN

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Wave | **5 — Human-AI Collaboration** |
| Under review | `WAVE5_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` (544 lines) |
| Request/standard | `docs/ITRGA_REQUEST_WAVE5_DESIGN_PLAN.md` (guardrails GR-1…GR-11, pre-registered) |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ ACCEPTED WITH REFINEMENTS (R5-1 … R5-8).** W5-U01 Build Order may issue on operator authorization once refinements are bound; no other Wave-5 unit before its own Build Order |
| Confidence | **HIGH** — measured against a standard fixed before the design existed; the two new hazard classes are met head-on |

> **We don't guess. We prove.** The riskiest wave arrives with the strongest plan: a non-actuating assistant proven safe *because no action tool exists*, and plan/journal schemas that are inert by construction. A short list of "shall" tightenings binds before construction.

---

## 1. Bottom line

This is an excellent, security-first plan that meets all eleven pre-registered guardrails and confronts the two
new hazard classes directly:
- **The AI assistant is non-actuating by ARCHITECTURE** (§4.2): "no assistant output can call an action tool
  because no such tool exists" — the strongest possible form of GR-10, plus a provider-neutral `AssistantPort`
  with a deterministic `RuleBasedGroundedAssistant/NullAssistant` **first** (no external LLM, no secrets, no
  unspiked deps in the safety slice), grounding-with-provenance, and named prompt-injection refusal tests.
- **The trade plan/journal are inert by SCHEMA** (§5): explicit **forbidden-field lists**
  (order_payload/side/quantity/lot_size/position_size/stop_loss/take_profit/broker_account_id/account_id/
  position_id/execution_status) — the W4-U04/U05 keystone standard applied to the two riskiest-named surfaces.
- Sequencing puts the **safety foundation first** (W5-U01), features after (W3-U01/W4-U01 precedent).

**ITRGA ACCEPTS the plan WITH REFINEMENTS R5-1…R5-8.** These are bindings, not rewrites — the plan's shape
stands. On their adoption, ITRGA issues `BUILD_ORDER_W5-U01.md` on operator authorization.

---

## 2. Guardrail compliance assessment (GR-1…GR-11)

| GR | Plan response | ITRGA finding |
|---|---|---|
| GR-1 Gate CLOSED | §0, §2, §3.2 (External Integration "no runtime dependency") | ✅ Compliant |
| GR-2 Advisory/decision-support only | §1, §2, §4.5 disclaimer | ✅ Compliant |
| GR-3 No exec/order/sizing/broker/account | §2, §3.2, §5.1 forbidden fields | ✅ Compliant |
| GR-4 Explainable/auditable/traceable | §4.3 response record (provenance/source ids/policy version/audit) | ✅ Strong |
| GR-5 Evidence mandatory | §2 GR-5 row; §10 per-unit evidence | ✅ Compliant |
| GR-6 Standing controls | §6/§8 (spike for any LLM/compiled dep; persistence-capture per artifact) | ✅ Compliant — see R5-2 |
| GR-7 Statistical/economic honesty | §2 GR-7; §6.2 no predictive guarantee | ✅ Compliant |
| GR-8 Presentation-only UX | §6 surfaces; §2 GR-8 | ✅ Compliant |
| **GR-9 Plan/journal inert** | §5.1/§5.2 explicit forbidden-field lists; §6.3/§6.4 no order-ticket patterns | ✅ Strong — see R5-4 |
| **GR-10 Assistant non-actuating/grounded/anti-injection** | §4.2 no action tools ("because no such tool exists"), §4.3 grounding, §4.4 injection defenses + 6 named negative tests, §4.5 disclaimer | ✅ Strong — see R5-1/R5-3 |
| **GR-11 No leakage** | §2 GR-11; §4.4 secret-exfiltration refusal test; §6.1 no secret display | ✅ Compliant — see R5-3 |

No guardrail is violated. No constitutional conflict (10_CONSTITUTIONAL_HIERARCHY) — Wave 5 sits under
canonical 05 v2.0 without amending any higher-tier doc; **D-W2-001 Option A stands.**

---

## 3. Binding refinements (R5-1 … R5-8) — adopt in the relevant unit

- **R5-1 — Non-actuation must be proven STRUCTURALLY, not just by test (W5-U01).** Beyond the named negative
  tests, W5-U01 **shall** prove the assistant has **no action/mutating tool in its allowlist by construction**:
  a test asserting the tool registry contains only read + own-audited-artifact-write tools, plus a wave-wide
  grep that the assistant module has no order/Gate/model-mutation/broker call path. "No such tool exists" is
  the right design — prove the registry enforces it.
- **R5-2 — The `RuleBasedGroundedAssistant`/`NullAssistant` foundation uses NO new compiled/LLM dependency
  (W5-U01); any future LLM is a HARD-GATED separate unit.** W5-U01 **shall** add no external LLM/API and no
  unspiked dep (per §8.1). Any later LLM provider is its **own** Build Order requiring the full §4.1/§8.2 pack
  (dependency/API spike, §77 secret handling, provider privacy/terms review, injection tests, output-redaction
  tests, no-action tool proof) — and **shall not** ship inside a feature unit.
- **R5-3 — Prompt-injection & secret-exfiltration refusal are MANDATORY NAMED TESTS with audited refusal
  (W5-U01), and re-run every assistant-touching unit.** The six §4.4 tests (refuses order/Gate-open/secret-
  exfiltration/unbounded-tool; grounding-or-refuses; write-limited-to-own-audited-artifact) **shall** pass by
  name, each refusal **shall** emit an **audit event**, and a **sampled-output secret-marker check** (GR-11)
  **shall** be shown. These re-run for W5-U02+ (any unit that adds assistant capability or an LLM).
- **R5-4 — Plan/journal inertness proven three ways per introducing unit (W5-U06/U07, contracts at W5-U01).**
  As W4-U04/U05: (a) **inert schema** (`\d` shows none of the forbidden fields), (b) a **named test** that the
  contract rejects order/sizing/account fields, and (c) a **grep** where those terms appear only as the
  forbidden-key list. Plus a named "**a plan/journal triggers/executes nothing / is never read by an exec
  path**" test.
- **R5-5 — Grounding is REQUIRED-or-REFUSE, and provenance is shown (every assistant unit).** An assistant
  response **shall** either cite persisted source_artifact_ids (grounding) **or refuse** — it **shall not**
  emit an ungrounded claim; hallucinated signals/prices/outcomes are a FAIL. Prove by named test
  (`assistant_response_has_grounding_or_refuses`) + the provenance rendered in any UI (browser).
- **R5-6 — Every AI-generated output carries the disclaimer, proven in the BROWSER (any assistant UI unit).**
  The §4.5 disclaimer ("AI-generated… not financial advice, not an instruction, may be wrong… AXIOM does not
  act") **shall** appear on every assistant reply/annotation surface — proven by component test **and** browser
  screenshot (W3-U05/W0-U06 UI-in-browser precedent). "Decision explanations" **shall** explain **persisted,
  governed** research only (GR-4), never fabricated rationale.
- **R5-7 — Persistence-capture (inline raw SELECT + no-orphan audit) for every new collaboration table (each
  introducing unit).** `assistant_research_responses`, `chart_research_annotations`, `chart_research_drawings`,
  `trade_plan_notes`, `manual_trade_journal_entries`, `decision_explanation_records`, and any grounding-source
  table each owe, on FIRST submission: Alembic head advance + committing script + **raw `psql SELECT ≥1 row`**
  on the correct table + **no-orphan audit JOIN** (W4-U03…U08 standard, delivered inline).
- **R5-8 — Wave-wide bright-line grep on EVERY unit + CI via the documented Git-Bash path.** The standing
  execution/mutation grep (extended with planning/journal/assistant action verbs:
  `place_order|order_payload|order_intent|side|quantity|lot_size|position_size|stop_loss|take_profit|
  broker_account|account_id|position_id|execution_status|gate_open|allow_execution|emit_signal|model\.status\s*=|
  advisory_status\s*=`) **shall** be run per unit (command + output; residuals limited to forbidden-key lists/
  benign seams). CI **shall** run via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` →
  `LOCAL_CI_EXIT_CODE: 0` (the W4-U03 WSL-artifact lesson).

---

## 4. Commendations (what the plan got right)

- **Assistant non-actuation by design** (§4.2) — "no such tool exists" is the strongest GR-10 posture; the
  provider-neutral port + rule-based/null first defers all LLM/secret/dependency risk out of the safety slice.
- **Inert plan/journal by explicit forbidden-field lists** (§5) — the two riskiest-named surfaces are
  structurally prevented from becoming order tickets.
- **Grounding-or-refuse + provenance** (§4.3/§4.4) directly kills the hallucinated-instruction hazard.
- **Honest risk register** (§9) names the three Criticals (injection→action, secret leak, plan-as-order-ticket)
  with structural mitigations + named tests.
- **Sequencing** (safety foundation W5-U01 first) and **non-self-authorization** (§0, §13) are correct.

---

## 5. Findings ledger

| ID | Type | Disposition |
|---|---|---|
| GR-1…GR-11 | Compliance | ✅ all met; no violation; no constitutional conflict; Option A stands |
| R5-1…R5-8 | Binding refinement | Adopt in the relevant unit's Build Order (R5-1/R5-2/R5-3/R5-8 at W5-U01; R5-4/R5-7 at each artifact unit; R5-5/R5-6 at each assistant/UI unit) |

**No CRITICAL/HIGH design defects.** Accepted; refinements bind.

---

## 6. Disposition & next step

- **Wave-5 Design Plan — ✅ ACCEPTED WITH REFINEMENTS (R5-1…R5-8).**
- On **operator authorization**, ITRGA issues **`BUILD_ORDER_W5-U01.md`** = *Collaboration Safety Foundation:
  Assistant Boundary + Inert Planning/Journal Contracts*, with R5-1 (structural non-actuation), R5-2
  (no LLM/unspiked dep this slice), R5-3 (named injection/secret refusal tests + audited refusal), R5-8
  (bright-line grep + Git-Bash CI) as binding acceptance criteria, and the plan/journal inert contracts (R5-4).
- Subsequent units (W5-U02…U08) each require their **own** Build Order carrying their named refinements; the
  DA does not build ahead of the issued Build Order, ship an external LLM inside a feature unit, add
  execution/order/sizing/account linkage, add an actuating assistant tool, or open the Gate.

Send **"authorized"** to have ITRGA issue the W5-U01 Build Order.

> **We don't guess. We prove.** — ITRGA
