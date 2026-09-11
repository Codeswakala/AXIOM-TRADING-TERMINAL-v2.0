# AXIOM — BUILD ORDER B-06
## Governed Assistant Ask Path

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-06` |
| Programme | Backend Operationalization (reconciled v2; predictive track deferred per Operator decision) |
| Authorizing authority | **Operator** (directive of 2026-08-20: "authorized") |
| Predecessors | B-00 → B-05 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · predictive deferral |
| Governing documents | `05_SYSTEM_ARCHITECTURE.md` v2.0 §37, §57 · onboarding §20–25 (assistant boundary) · `17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing

The governed assistant is the **one remaining scaffold-only capability with no request path** (FIND-3 in the original audit). The responder already exists and is correct:

- `RuleBasedGroundedAssistant.respond()` — deterministic, local, **no external LLM**, no action tools.
- A safety policy with the constitutional refusal classes (`ORDER_INSTRUCTION_REFUSED`, `GATE_OPEN_INSTRUCTION_REFUSED`, `SECRET_EXFILTRATION_REFUSED`, `UNBOUNDED_TOOL_REQUEST_REFUSED`, plus `GROUNDING_REQUIRED` when the grounding bundle is empty).
- A `GroundingBundle` contract (`source_artifact_ids` + `summaries`) that ties every answer to persisted governed artifacts.

But it is **unreachable**: the collaboration router exposes only read-only `GET /assistant-responses` (and unrelated chart-annotation/trade-plan/journal POSTs). No endpoint invokes `respond()`.

This order exposes the ask path and makes grounding real, while **preserving the constitutional assistant boundary** (onboarding §20, §25, §34): research-only, explainable, grounded, deterministic/local, read-only, auditable, non-actuating — not an external LLM, not an actor, not financial advice.

---

## 1. Objective

1. Expose a governed `POST /api/v1/collaboration/assistant-respond` over the existing rule-based responder.
2. Build **real** grounding bundles from persisted governed artifacts (summaries, lineage, source ids) so `GROUNDING_REQUIRED` fires only when genuinely ungrounded.
3. Persist responses **and** refusals with hash/lineage + audit correlation; wire the existing read-only surfaces.
4. Prove the non-actuation, no-external-calls, and refusal-class invariants.

---

## 2. Scope

### B-06.1 — The ask endpoint
- `POST /api/v1/collaboration/assistant-respond` — operator-authenticated (`CurrentOperatorDep`).
- Request: a prompt + a set of **operator-selected artifact ids** (the grounding basis). The assistant answers grounded in these persisted artifacts — it does not free-form generate.
- Response: `AssistantResponse` — either a grounded summary (with `source_artifact_ids`, disclaimer, audit correlation) or a classed refusal.
- Behavior is delegated **entirely** to `RuleBasedGroundedAssistant.respond()` — no new reasoning logic is introduced.

### B-06.2 — Real grounding bundles
- Build the `GroundingBundle` from the selected artifacts' **persisted** summaries/notes/lineage (e.g. intelligence reports from B-04, research artifacts, dataset snapshots). The endpoint resolves artifact ids → their stored summaries.
- Unknown/nonexistent artifact ids are excluded from grounding (and if the result is empty, the responder returns `GROUNDING_REQUIRED` — honest, not fabricated).
- **No** groundless generation: a prompt with no valid grounding artifacts is refused, not answered from thin air.

### B-06.3 — Persistence + auditability
- Responses and refusals are persisted via the existing `AssistantResearchResponseRepository` (hash-only request text, no orphan audit linkage, policy version, provider metadata).
- Every ask produces an audit row (actor + correlation id).
- The existing `GET /assistant-responses` (+`/{id}`) surfaces the new records unchanged in contract.

### B-06.4 — Boundary invariants (binding)
- **No external LLM, no external network calls** (deterministic local responder only).
- **No actuation**: the responder cannot place orders, open gates, mutate state, or run tools (already enforced by the safety policy + non-actuating tool registry; must remain).
- **No state mutation beyond the assistant response/refusal record + audit row.**

---

## 3. Exclusions (out of scope — do NOT do)

- **No** external LLM integration, no autonomous tools, no agent behavior (onboarding §20/§25 — any such change requires a separate governing instrument).
- **No** order/execution/broker/account/gate mutation.
- **No** free-form ungrounded generation; the assistant answers only from operator-selected persisted artifacts.
- **No** weakening of the refusal policy or the non-actuating tool registry.
- **No** ML model, prediction, or promotion (predictive track deferred).
- **No** frontend changes (F-01 assistant input surface comes later; this is the backend seam it will call).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. `POST /assistant-respond` endpoint (authenticated, grounding-resolving, responder-delegating).
2. Grounding-bundle resolution over real persisted artifacts.
3. Persisted responses + refusals with hash/lineage/audit correlation.
4. Tests (new/churn): happy-path grounded answer, each refusal class, empty-grounding refusal, no-external-calls, no-actuation, auth.
5. Delivery Report (§9) with relay-accurate transmission manifest.

---

## 5. Dependencies

- **Upstream:** B-04 (intelligence reports = real grounding artifacts) · B-00 (provenance) · B-01 (tier rule).
- **Downstream:** F-01 (assistant input surface) consumes this endpoint.
- **Independent of:** any promoted model (assistant grounds on deterministic research artifacts, not ML predictions).

---

## 6. Allowed files / components

- `backend/app/api/routes/collaboration.py` (add the respond endpoint; existing endpoints unchanged).
- `backend/app/collaboration/*` (consume the responder + contracts; no weakening of `assistant.py`/`contracts.py`).
- `backend/app/models/*` (request/response schemas).
- `backend/tests/**` (new/churn tests).
- `backend/docs/**` (any ADR).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- Authenticated; no unauth ask.
- The safety policy and refusal classes are **constitutional** and must not be weakened or bypassed.
- No secrets/credentials; **no external network calls** from the responder (deterministic local only).
- Grounding resolution must not leak internal storage structure; it returns persisted summaries only.
- The assistant remains research-only and non-actuating; no state mutation beyond the response/refusal record + audit.

---

## 8. Acceptance criteria

- [ ] `POST /assistant-respond` exists, authenticated.
- [ ] A prompt with valid grounding artifacts returns a grounded summary carrying source ids, disclaimer, and audit correlation.
- [ ] A prompt with empty/invalid grounding returns `GROUNDING_REQUIRED` (not fabricated content).
- [ ] Each refusal class fires correctly (order/gate/secret/tool probes).
- [ ] Responses and refusals are persisted; read back via `GET /assistant-responses`.
- [ ] No external network calls (test-pinned); no actuation surface (test-pinned).
- [ ] Full backend suite green; new tests executed with output.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1, hard gate)

**Binding (CA-TRANSMIT-1):** artifacts must be uploaded and confirmed against the review channel. A declared-but-untransmitted artifact is an automatic CORRECTION REQUIRED.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed test output (new/churn) | Level II | run transcript |
| Ask-path evidence (grounded answer + each refusal + empty-grounding) | Level I | API probe output |
| Persistence + read-back evidence | Level I | API probe output |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Endpoint description (request → grounding resolution → responder → response/refusal)
4. Grounding-bundle resolution description (which persisted artifacts, how summaries are sourced)
5. Ask-path evidence (grounded + refusals + empty-grounding)
6. Non-actuation + no-external-calls evidence
7. Test evidence (executed)
8. Deviations register
9. Transmission manifest (relay-accurate)
10. Known limitations / technical debt

---

## 11. Rollback / containment

- New endpoint + response/refusal rows are additive; revert = drop rows, revert patch.
- No schema migration authorized by default (existing `assistant_research_responses` table is reused).
- No data produced affects production (Gate CLOSED).

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of B-06, B-07 (Cross-Cutting Hardening) may be issued, and F-01 (assistant input surface) is unblocked to call this endpoint.

---

**End of Build Order B-06**
