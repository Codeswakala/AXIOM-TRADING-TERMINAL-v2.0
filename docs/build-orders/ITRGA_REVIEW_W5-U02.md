# ITRGA INDEPENDENT REVIEW — W5-U02 (Audited Assistant Research Responses)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W5-U02** — Audited Assistant Research Responses |
| Wave | 5 — Human-AI Collaboration |
| Build Order | `docs/BUILD_ORDER_W5-U02.md` |
| Evidence | `uploads/DELIVERY_REPORT_W5-U02.md` + `uploads/operator results.md` (1,297 lines) |
| DA-claimed platform | 0.40.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.40.0** |
| Confidence | **HIGH** — persistence audited with zero orphans; no-raw-text/hash-only proven; all six refusal classes persisted+audited |

> **We don't guess. We prove.** The assistant now has an accountable memory: every response and refusal is persisted, audited, disclaimed, and grounded-or-refused — and no raw prompt or secret is stored. Approved.

---

## 1. Bottom line

W5-U02 gives the assistant a **fully accountable memory**: grounded responses and refusals persist to
`assistant_research_responses`, each with **grounding source ids + provenance + disclaimer**, each linked to
its immutable audit event (**no orphan**), with **no raw request text stored (SHA-256 hash only)** and **no
secret/raw-internal**. Read-only API (401/list-200/detail-200/POST-405); still **no external LLM/dependency**;
assistant remains **non-actuating and grounded-or-refuses**. All 24 named collaboration tests pass; full suite
257; CI exit 0 via Git-Bash. **APPROVED, CLEAN, no residual.**

---

## 2. R5-7 — persistence-capture, INLINE, no orphan (keystone) ✅

- Migration `20260716_0023 → 20260717_0024 (head)`; `assistant_research_responses` created.
- **Raw `SELECT FROM assistant_research_responses`** → 7 rows (6 refusals + 1 grounded), each with
  `refused/refusal_reason/research_status/request_text_hash/source_artifact_ids/disclaimer`.
- **No-orphan audit JOIN** (matched on `resource_id` **and** `correlation_id` **and** action ∈
  {`assistant.response_draft_created`,`assistant.refused`}) → **`orphan_count 0`.**
- The JOIN result shows every row's `refusal_reason` **equals** the audit event's `audit_refusal_reason` —
  response↔audit integrity proven, not merely asserted. Repository raises on audit failure (transaction
  rolls back) → no orphan by construction. ✅

## 3. R5-3 — injection/secret refusal persisted+audited; NO raw text (keystone) ✅

- All six refusal classes persisted with reason codes and matching audit events (DB JOIN):
  `ORDER_INSTRUCTION_REFUSED`, `GATE_OPEN_INSTRUCTION_REFUSED`, `SECRET_EXFILTRATION_REFUSED`,
  `UNBOUNDED_TOOL_REQUEST_REFUSED`, `GROUNDING_REQUIRED`, `ASSISTANT_DISABLED`.
- **No-raw-text proven with a purpose-built query:** all rows show `request_hash_length 64`,
  `request_hash_is_sha256 = t`, `raw_request_text_stored = false` — hash-only privacy, the strongest form.
- Named tests: `..._no_raw_request_text_stored PASSED`, six `..._refuses_*_persists_and_audits PASSED`,
  `..._table_has_no_forbidden_collaboration_fields PASSED`. Sampled secret-marker check clean (GR-11).

## 4. Other controls — PROVEN on target ✅

| Control | Evidence |
|---|---|
| Build identity | `Test-Path` new model/migration/test True; v0.40.0; `git`… |
| **R5-5 grounding-or-refuse** | `..._response_has_grounding_or_refuses PASSED`; grounded row has `source_artifact_ids`; ungrounded → `GROUNDING_REQUIRED` refusal persisted |
| **R5-1 non-actuation (re-run)** | `..._registry_remains_non_actuating PASSED` + `test_assistant_tool_registry_non_actuating_by_construction PASSED` |
| **R5-6 disclaimer** | `..._disclaimer_on_every_record PASSED`; disclaimer on every row; **no UI panel added → browser N/A (correctly stated)** |
| Read-only API | `..._read_only_api_requires_auth_and_returns_list_detail PASSED`; `..._post_mutation_endpoint_not_available PASSED`; `POST_STATUS:405` |
| **R5-2 no LLM/dep** | `..._no_llm_or_unspiked_dependency_or_execution_path PASSED`; grep no `openai\|anthropic\|transformers\|langchain\|llama` |
| **R5-8 grep + gate** | collaboration grep no LLM/exec; Gate CLOSED |
| Regression + CI | 24 named collab tests PASS; backend **257 passed** (244→257, +13), frontend **12·29**, ruff clean, npm audit 0; **CI via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → marker + `LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U02) |
| D-W2-001 | no per-market model / symbol-identity feature |

---

## 5. Findings ledger

| ID | Severity | Status |
|---|---|---|
| — | — | R5-7 inline raw SELECT + no-orphan audit (`orphan_count 0`, resource_id+correlation_id+action JOIN) ✅ |
| — | — | R5-3 six refusal classes persisted+audited; no-raw-text/hash-only proven (sha256, raw_request_text_stored=false) ✅ |
| — | — | R5-5 / R5-1 / R5-6 / read-only API 401·list200·detail200·POST405 / R5-2 no-LLM / gate-closed / 257 tests / CI exit 0 ✅ |

**No CRITICAL/HIGH. No unmet mandatory evidence. No open residual.** All acceptance criteria met on target.

---

## 6. Disposition & next step

- **W5-U02 — ✅ APPROVED, CLEAN.** Platform **v0.39.0 → v0.40.0**.
- Commendation: the audit integrity is proven by a **JOIN that matches resource_id AND correlation_id AND
  action** (not just existence), the repository is **no-orphan by construction** (rolls back on audit failure),
  and the **no-raw-text privacy is proven with a bespoke sha256/`raw_request_text_stored=false` query** — the
  strongest form. Every prior lesson held.
- **Next:** ITRGA recommends **W5-U03 — Chart Research Annotations & Drawing Tools**: inert annotations/drawings
  linked to source artifacts, presentation-only over chart context, carrying **R5-4** (inert — no order/sizing/
  account fields), **R5-6** (disclaimer + **browser evidence mandatory** for the UI), **R5-7** (persistence-
  capture inline), **R5-8** (grep + gate), and — if AI-assisted annotations — R5-5 grounding + R5-3 refusal.
  On operator authorization ITRGA issues `BUILD_ORDER_W5-U03.md`.
- External LLM remains future hard-gated (R5-2). DA does not self-authorize W5-U03, ship an LLM, add an
  actuating tool/execution/order/account linkage, or open the Gate.

> **We don't guess. We prove.** — ITRGA
