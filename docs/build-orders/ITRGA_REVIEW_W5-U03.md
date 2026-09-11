# ITRGA INDEPENDENT REVIEW — W5-U03 (Chart Research Annotations & Drawing Tools)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W5-U03** — Chart Research Annotations & Drawing Tools (first Wave-5 UI) |
| Wave | 5 — Human-AI Collaboration |
| Build Order | `docs/BUILD_ORDER_W5-U03.md` |
| Evidence | `uploads/DELIVERY_REPORT_W5-U03.md` + `uploads/operator results.md` (1,522 lines) + 4 browser screenshots |
| DA-claimed platform | 0.41.0 |
| Review date | 2026-07-17 |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.41.0** |
| Confidence | **HIGH** — annotations inert by schema (forbidden-column query 0 rows), no-orphan audit, browser-proven, and `/execute`+`/emit-signal` proven absent (405) |

> **We don't guess. We prove.** The first Wave-5 UI renders inert research markups on the chart, proves no execution/signal endpoint exists, and shows the disclaimer + logged-out block in the browser. Approved.

---

## 1. Bottom line

W5-U03 delivers inert, audited chart research annotations/drawings, presentation-only, browser-proven. Every
keystone is met on target: **inert by schema (R5-4)** — the forbidden-column query returns **0 rows** and 7
named tests confirm rejection of order/sizing/account/raw-score/guarantee fields; **persisted no-orphan
(R5-7)**; **read-only reads 401/200 + create authenticated + `/execute` and `/emit-signal` proven ABSENT
(405)**; **presentation-only, no raw score, no LLM (R5-2)**; **browser evidence complete (R5-6)**. Full suite
264; CI exit 0 via Git-Bash. **APPROVED, CLEAN, no residual.**

---

## 2. R5-4 — annotations INERT (keystone) ✅

- **Inert schema proven directly:** `SELECT column_name FROM information_schema.columns … IN (order_payload,
  order_intent, side, quantity, lot_size, order_size, position_size, entry_price_order, stop_loss, take_profit,
  broker_account_id, account_id, position_id, execution_status, live_position, signal_payload, emit_signal,
  raw_score, predicted_outcome, guaranteed_outcome)` → **`(0 rows)`.** None exist.
- Named tests: `..._contract_rejects_forbidden_fields`, `..._rejects_raw_score_and_guarantee_text`,
  `..._schema_has_no_forbidden_fields`, `..._triggers_nothing_beyond_annotation_and_audit`,
  `..._api_rejects_forbidden_payload` — all PASSED. The API itself rejects a forbidden payload. ✅

## 3. R5-7 — persisted, no orphan (inline) ✅

- Migration `20260717_0024 → 20260717_0025 (head)`; raw `SELECT FROM chart_research_annotations` → **2 rows**
  (research_note + research_drawing, both `research_only`, full "not a signal, not an order… AXIOM does not
  act" disclaimer, source_artifact_ids present).
- **No-orphan audit JOIN** (resource_id + correlation_id + action `chart_research_annotation.created`) →
  **`orphan_count 0`.** No-orphan by construction (repo rolls back on audit failure). ✅

## 4. API — read-only + create; NO execute/signal endpoint ✅

| Call | Status |
|---|---|
| unauth list | **401** |
| auth list | **200** |
| auth detail | **200** |
| `POST …/{id}/execute` | **405 (endpoint absent)** |
| `POST …/{id}/emit-signal` | **405 (endpoint absent)** |

The operator went above spec and proved the execution/signal endpoints **do not exist** — the strongest form
of "annotation is not an order/signal." Operator-authored create writes to the annotation store only. ✅

## 5. R5-6 — BROWSER EVIDENCE (mandatory) — complete ✅

Four screenshots on a reachable served session (`localhost:8000`, W5-U03 / v0.41.0):
- **Chart Workspace rendered** (`/charts`, WS CONNECTED) — "**Research markup only.** …not a signal, not an
  order, and not an instruction. AXIOM does not act." + data-provenance note (seed:synthetic non-authoritative).
- **Annotations rendered** — RESEARCH NOTE / RESEARCH ZONE cards with source ids + per-card disclaimer; inert
  drawing tools (research note/zone/trend guide, "Add research markup").
- **No execution controls anywhere** — chart controls are Candles/Line/Area/Start-Stop-feed/Seed/Reload only;
  no buy/sell/order/broker; nav has no trade surface.
- **Logged-out block** — `localhost:8000/login` on an unauthenticated visit (not rendered).
No `ERR_CONNECTION_REFUSED`. ✅

## 6. Other controls ✅

| Control | Evidence |
|---|---|
| Presentation-only (GR-8) | UI states "no client-side inference, no authoritative analytics recompute, no AI-assisted generation in W5-U03"; collaboration grep no recompute |
| No raw score / no guarantee | rejected by contract + not rendered (test + screenshot) |
| **R5-2 no LLM/dep** | collaboration grep no `openai\|anthropic\|transformers\|langchain\|llama`; existing stack |
| AI path | none this unit (correctly stated); W5-U01/U02 safety tests remain in regression |
| **R5-8 grep + gate** | wave-wide residuals benign (forbidden-key lists / governed `advisory_status=` promotion / disclosed); Gate CLOSED |
| Regression + CI | 31 named collab tests PASS; backend **264 passed** (257→264, +7), frontend **13 files / 33 tests** (+4), ruff clean, npm audit 0; **CI via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → marker + `LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U03) |
| D-W2-001 | no per-market model / symbol-identity feature |

---

## 7. Findings ledger

| ID | Severity | Status |
|---|---|---|
| — | — | R5-4 inert (forbidden-column query 0 rows + 7 named tests) ✅ |
| — | — | R5-7 raw SELECT 2 rows + no-orphan audit (`orphan_count 0`) ✅ |
| — | — | API 401/200/200 + execute/emit-signal ABSENT (405) ✅ |
| — | — | R5-6 browser (rendered + disclaimer + no-exec + logged-out) ✅ |
| — | — | GR-8 presentation-only · R5-2 no-LLM · R5-8 grep+gate · 264 tests · CI exit 0 ✅ |

**No CRITICAL/HIGH. No unmet mandatory evidence. No open residual.** All acceptance criteria met on target.

---

## 8. Disposition & next step

- **W5-U03 — ✅ APPROVED, CLEAN.** Platform **v0.40.0 → v0.41.0**.
- Commendation: inert proven **directly against `information_schema` (0 rows)**, no-orphan audit inline, and —
  above spec — the operator proved `/execute` and `/emit-signal` **don't exist (405)**, the strongest possible
  "annotation is not an order/signal." Browser set complete; every prior lesson held.
- **Next:** ITRGA recommends **W5-U04 — Signal Investigation Workspace**: operator surface to explore signal
  rationale/guardrails/linked intelligence reports, read-only, presentation-only; the assistant (if used) may
  **summarize only grounded artifacts** (R5-5 grounding-or-refuse, R5-3 refusal, R5-1 non-actuation, disclaimer,
  audited) with **no signal mutation**; browser evidence mandatory (R5-6); R5-8. On operator authorization ITRGA
  issues `BUILD_ORDER_W5-U04.md`.
- External LLM remains future hard-gated (R5-2). DA does not self-authorize W5-U04, ship an LLM, add an
  actuating tool/execution/order/account linkage, or open the Gate.

> **We don't guess. We prove.** — ITRGA
