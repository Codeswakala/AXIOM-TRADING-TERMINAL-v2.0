# AXIOM — DESIGN PLAN B-06 (DA engineering design, pre-Build-Order)
## Governed Assistant Ask Path — exposing the existing tested engine over a bounded read-only-adjacent POST

| Item | Value |
|---|---|
| Document class | **DA design plan** (per the governed lifecycle: Operator Directive → DA design planning → ITRGA review → Build Order → implementation). **NOT a Build Order, NOT self-authorization, NOT implementation.** |
| Prepared by | AXIOM Development Authority (DA) |
| Date | 2026-08-20 |
| Basis | `BACKEND_ROADMAP_v2.md` §B-06 ("B-06 off critical path; start in parallel") · ITRGA capability assessment FIND-3 (no ask path) · BO-B-ML negative result (B-03/B-04/B-05 remain gated; B-06 is not model-dependent) |
| Status of the plan | Ready for ITRGA review; implementation begins only on an issued Build Order |

---

## 0. Current state (verified this session, cited to code)

- The engine **already exists, is tested, and is unexposed**: `RuleBasedGroundedAssistant.respond()` in `backend/app/collaboration/assistant.py` — deterministic, local, no external LLM, six-code refusal policy (`AssistantSafetyPolicy.refusal_reason`), `GROUNDING_REQUIRED` discipline for empty grounding, secret-marker redaction (`redact_secret_markers`), audit correlation ids, and **persistence of both responses and refusals** via `AssistantResearchResponseRepository.create_from_response` (table `assistant_research_responses`).
- The tool registry is asserted non-actuating (`registry.assert_non_actuating()`).
- The contracts exist: `AssistantRequest` (prompt, operator_id, `GroundingBundle`, prompt_hash), `AssistantResponse`, `GroundingBundle` (`source_artifact_ids` + `summaries`, `is_empty`).
- **The gap (FIND-3, confirmed):** the collaboration router exposes only GET on `/assistant-responses`; no HTTP path constructs an `AssistantRequest`. The frontend suggestion chips set state only (no submit path — F-01 scope).

## 1. Objective

Expose the existing engine as a bounded HTTP surface: an operator can ask a grounded research question and receive either a grounded response or a classed refusal — both persisted, audited, and provenance-bearing — with **zero actuation, zero external calls, zero state mutation beyond the response record itself**.

## 2. Proposed design

### 2.1 Endpoint

`POST /api/v1/collaboration/assistant-respond` — operator-authenticated (`CurrentOperatorDep`), request-scoped.

Request schema (bounded, field-whitelisted):

```
{
  "prompt": str                       # required, 1..1000 chars after strip
  "grounding_source_ids": [str] | null # optional, max 10, each must resolve to a real artifact
  "use_workspace_context": bool = false # optional: pull the most recent governed artifacts
}
```

Response: the persisted `AssistantResearchResponseRead` — response OR refusal record (`refused=true`, `refusal_reason` set), with `source_artifact_ids`, `grounding_summary`, disclaimer, request hash.

### 2.2 Grounding assembly (new module `backend/app/collaboration/grounding.py`)

`assemble_grounding(session, *, source_ids, use_workspace_context) -> GroundingBundle` — **read-only queries only** over real persisted artifacts. Candidate families (all existing tables):

| Family | Summary field used | Provenance |
|---|---|---|
| Advisory signals | `rationale` | signal id + model/experiment lineage |
| Signal validation reports | `notes`/metrics summary | report id |
| Scenario reports | assumptions/notes | scenario id |
| Research annotations | `content` | annotation id |
| Journal entries | `content` | entry id |
| Trade plan notes | `content`/title | plan id |
| Research artifacts/collections | stored summary fields | artifact id |

- **Operator-supplied ids:** each id resolves against its family; unknown id → **422 with the id named** (never silently empty; never fabricated).
- **Workspace context:** deterministic bounded default — the most recent N artifacts (N=10) across families, ordered by family then timestamp; deterministic given database state.
- **Empty bundle after resolution → the engine's existing `GROUNDING_REQUIRED` refusal** (no new behavior invented).
- Summaries are joined stored fields; the engine's `redact_secret_markers` runs before response text is built (existing).

### 2.3 Mutation boundary (binding)

The POST creates **exactly one** `assistant_research_response` row (response or refusal — the engine already persists both). It does **not** create or modify orders, broker state, account state, trade plans, annotations, governance records, or any other row. No tool execution — the non-actuating registry is the only tool surface and is asserted. **No external network call of any kind** (the engine is pure-local; the plan adds no HTTP client).

### 2.4 Refusal classes surfaced

The six-code taxonomy the UI already renders, now reachable via the ask path: `ORDER_INSTRUCTION_REFUSED` · `GATE_OPEN_INSTRUCTION_REFUSED` · `SECRET_EXFILTRATION_REFUSED` · `UNBOUNDED_TOOL_REQUEST_REFUSED` · `GROUNDING_REQUIRED` · (assistant-disabled state unchanged).

### 2.5 Determinism

Same prompt + same grounding + same database state → same `response_text` and `grounding_summary`. Timestamps and uuids are run-instance fingerprints (same disclosed limitation class as B-ML D7 — full fingerprint determinism is a future hardening unit).

## 3. Proposed test plan (fail-first)

1. Unauthenticated POST → 401.
2. Unknown grounding id → 422 naming the id; nothing persisted.
3. Empty/absent grounding → `GROUNDING_REQUIRED` refusal persisted with audit row.
4. Order-instruction prompt → `ORDER_INSTRUCTION_REFUSED` persisted; response text carries the disclaimer.
5. Gate-open prompt → `GATE_OPEN_INSTRUCTION_REFUSED`.
6. Secret-exfiltration prompt → `SECRET_EXFILTRATION_REFUSED` + redaction applied.
7. Tool-request prompt → `UNBOUNDED_TOOL_REQUEST_REFUSED`.
8. Valid grounding → grounded response persisted with `source_artifact_ids` + disclaimer; `GET /assistant-responses/{id}` returns it.
9. **No-external-calls proof:** static guard (no http/urllib/socket import surface in the ask path) + runtime negative control (response produced while network access is absent).
10. **Mutation boundary proof:** after a POST, exactly one new `assistant_research_response` row; counts of all other tables unchanged.
11. Determinism: same inputs → identical `response_text`/`grounding_summary`.
12. Existing W5-U01 assistant suite stays green unchanged.

## 4. Proposed allowed files (for the eventual Build Order)

- `backend/app/api/routes/collaboration.py` (add the POST).
- `backend/app/collaboration/grounding.py` (new — read-only assembly).
- `backend/app/models/collaboration.py` (request schema; read model reused).
- `backend/tests/**` (new/churn tests).
- `backend/docs/**` (any ADR).
- Delivery report. — Anything else out of scope.

## 5. Exclusions

No frontend changes (F-01 is a separate order, final acceptance gated on B-06.1). No external LLM (T-4/T-5 unchanged). No rate limiting here (formally deferred TD-095/TD-W7-U07-RATE-GUARD — lands in B-07.2; noted as a known limitation). No actuation, no new dependencies, no schema migration (table exists).

## 6. Proposed acceptance criteria (for the eventual Build Order)

- [ ] POST exists, operator-authenticated, bounded request schema.
- [ ] Every refusal class reachable and persisted with audit rows.
- [ ] Grounding resolves real artifacts only; unknown ids → 422; empty → GROUNDING_REQUIRED.
- [ ] Mutation boundary proven (single-row write; no other table changes).
- [ ] No-external-calls proven (static + runtime).
- [ ] Determinism proven.
- [ ] Full backend suite green; transmission manifest complete (CA-B01-1, relay-accurate).

## 7. Evidence + delivery (when authorized)

Patch + `git apply --check` transcript (chain position 24) · fail-first probe log · executed test log · API probe log (live POST + refusal walk-through against the dev server) · delivery report with transmission manifest — same discipline as B-00→B-ML.

---

**End of Design Plan B-06** — submitted for ITRGA review; the DA implements only on an issued Build Order.

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
