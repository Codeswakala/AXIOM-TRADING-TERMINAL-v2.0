# ITRGA INDEPENDENT REVIEW — W5-U01 (Collaboration Safety Foundation)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W5-U01** — Collaboration Safety Foundation (Assistant Boundary + Inert Planning/Journal Contracts) |
| Wave | 5 — Human-AI Collaboration (FIRST unit — safety keystone) |
| Build Order | `docs/BUILD_ORDER_W5-U01.md` |
| Evidence | `uploads/DELIVERY_REPORT_W5-U01.md` + `uploads/operator results.md` (1,177 lines) |
| DA-claimed platform | 0.39.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.39.0** |
| Confidence | **HIGH** — the AI assistant is proven non-actuating by construction, grounded-or-refuses, and audits every injection refusal in the database |

> **We don't guess. We prove.** The highest-risk wave's safety keystone is proven: the assistant cannot act because no action tool exists, it refuses every attack class with an audited refusal, and the plan/journal are inert by schema. Approved.

---

## 1. Bottom line

W5-U01 proves the Wave-5 safety envelope **before** any rich interaction or external LLM. The AI assistant is
**non-actuating by construction (R5-1)**, **grounded-or-refuses (R5-5)**, **refuses order/Gate/secret/
unbounded-tool prompts with an AUDITED refusal (R5-3)**, carries the disclaimer, and can only write its own
audited artifact; the **trade-plan/journal contracts are inert (R5-4)**, rejecting all order/sizing/account
fields recursively; **no external LLM / no new dependency (R5-2)**. All 11 named safety tests pass; the refusal/
response events are proven in `audit_events`; full suite 244; CI exit 0 via Git-Bash. **APPROVED, CLEAN, no
residual.**

---

## 2. R5-1 — assistant non-actuating BY CONSTRUCTION (keystone) ✅

- `AssistantToolRegistry` / `DEFAULT_ASSISTANT_TOOL_REGISTRY` allows only modes `read` +
  `own_audited_artifact_write`; only tools `read_governed_artifact_summary` +
  `create_audited_assistant_response_draft`. No action/broker/execution/Gate/model-mutation/external tool
  exists.
- `test_assistant_tool_registry_non_actuating_by_construction PASSED` (structural, not just behavioral) +
  `test_assistant_write_limited_to_own_audited_artifact PASSED`.
- Wave-wide grep: no order/Gate/mutation/broker/exec path constructed in the collaboration module (residuals =
  forbidden-key lists / refusal reason codes / benign, disclosed). "No such tool exists" — enforced by the
  registry. ✅

## 3. R5-3 — injection/secret refusal, AUDITED — proven in the database ✅

Named tests PASS: `test_assistant_refuses_order_instruction_and_audits`,
`..._refuses_gate_open_instruction_and_audits`,
`..._refuses_secret_exfiltration_and_output_has_no_secret_markers`, `..._refuses_unbounded_tool_request`.
**On target, `SELECT … FROM audit_events WHERE resource_type='assistant_response'` shows the refusals with
explicit reason codes:**
- `assistant.refused` · `ORDER_INSTRUCTION_REFUSED`
- `assistant.refused` · `GATE_OPEN_INSTRUCTION_REFUSED`
- `assistant.refused` · `SECRET_EXFILTRATION_REFUSED`
- `assistant.refused` · `UNBOUNDED_TOOL_REQUEST_REFUSED`
- `assistant.refused` · `GROUNDING_REQUIRED`
- `assistant.response_draft_created` (a grounded draft)

Every attack class is refused **and** the refusal is auditable in the DB — the strongest form of GR-10/GR-11.
Sampled-output secret-marker check clean. ✅

## 4. Other controls — PROVEN on target ✅

| Control | Evidence |
|---|---|
| Build identity | `Test-Path`×N True; v0.39.0; `collaboration/{assistant,contracts}.py` |
| **R5-5 grounding-or-refuse** | `test_assistant_response_has_grounding_or_refuses PASSED`; ungrounded → `GROUNDING_REQUIRED` refusal in DB |
| Disclaimer | `test_assistant_response_disclaimer_present PASSED` (§4.5 on every response/refusal) |
| **R5-4 inert plan/journal** | `test_trade_plan_and_journal_contracts_reject_forbidden_fields PASSED` + `test_trade_plan_journal_trigger_nothing_and_are_inert_contracts PASSED`; recursive forbidden-field rejection |
| **R5-2 no LLM/dep** | `test_collaboration_context_has_no_llm_or_unspiked_dependency_or_execution_path PASSED`; grep no `openai\|anthropic\|transformers\|langchain\|llama` import; existing stack only |
| **R5-7 persistence** | Contracts-only this unit — **no new table**, audit via existing `audit_events` (explicitly stated; persistence-capture correctly N/A) |
| **R5-8 bright-line + gate** | wave-wide grep residuals all benign (forbidden-key lists / refusal codes / no-side-effect guards / hardening strings), disclosed; Gate CLOSED; broker gate tests pass |
| Regression + CI | backend **244 passed** (233→244, +11), frontend **12·29**, ruff `All checks passed!`, npm audit 0; **CI via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → marker + `LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U01); no migration (head `20260716_0023`); no UI (stated) |
| D-W2-001 | no per-market model / symbol-identity feature |

---

## 5. Findings ledger

| ID | Severity | Status |
|---|---|---|
| — | — | R5-1 non-actuation by construction (registry test + grep) ✅ |
| — | — | R5-3 four injection/secret refusals, audited in DB with reason codes ✅ |
| — | — | R5-5 grounding-or-refuse / disclaimer / write-limited ✅ |
| — | — | R5-4 inert plan/journal (reject forbidden fields + triggers-nothing) ✅ |
| — | — | R5-2 no LLM/dep · R5-8 grep+gate · 244 tests · CI exit 0 ✅ |

**No CRITICAL/HIGH. No unmet mandatory evidence. No open residual.** All acceptance criteria met on target.

---

## 6. Disposition & next step

- **W5-U01 — ✅ APPROVED, CLEAN.** Platform **v0.38.0 → v0.39.0**. The Wave-5 safety envelope is proven.
- Commendation: the assistant is safe **by architecture** (registry enforces read + own-audited-write only),
  and — notably — **every attack class refusal is provable in the database** (audit_events with reason codes),
  not just in unit tests. Contracts-only persistence correctly stated (R5-7 N/A). Every prior lesson held
  (forbidden-key-only greps, CI via Git-Bash, build-identity-first).
- **Next:** ITRGA recommends **W5-U02 — Audited Assistant Research Responses**: persist assistant response +
  refusal records (their own table), carrying **R5-3** (re-run injection/secret refusal + audited),
  **R5-5** (grounding-or-refuse), **R5-6** (disclaimer in the browser if a panel is added), **R5-7**
  (persistence-capture INLINE — raw SELECT + no-orphan audit on the new table). On operator authorization ITRGA
  issues `BUILD_ORDER_W5-U02.md`.
- Reminder: any external LLM remains a **future, separately hard-gated** Build Order (R5-2) — never inside a
  feature unit. DA does not self-authorize W5-U02, ship an LLM, add an actuating tool/execution/order/sizing/
  account linkage, or open the Gate.

> **We don't guess. We prove.** — ITRGA
