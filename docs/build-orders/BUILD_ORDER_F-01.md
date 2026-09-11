# AXIOM — BUILD ORDER F-01
## Assistant Input Surface (the ask path)

| Item | Value |
|------|-------|
| Build Order ID | `BO-F-01` |
| Programme | Frontend Operationalization (Visual Blueprint approved) |
| Authorizing authority | **Operator** (directive 2026-08-21: "authorized") |
| Predecessors | B-06 (backend `POST /collaboration/assistant-respond` — delivered) · F-00 (design foundation) · custody decision (new baseline) |
| Governing documents | `VISUAL_BLUEPRINT.md` · `08_UI_UX_SPEC.md` · onboarding §20–25 (assistant boundary) · `FRONTEND_ROADMAP_v2.md` §F-01 |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and framing

The backend assistant ask path exists (B-06: `POST /api/v1/collaboration/assistant-respond` — grounded, deterministic, non-actuating, refusal-classed). The frontend is still **read-only**: `ContextualAssistantPanel` renders *static prompt-suggestion chips* (cosmetic strings) and `assistantClient.ts` has **only GET** functions — there is **no input box, no submit, no POST**. This was FIND-3's frontend half.

This order builds the **real ask surface**: an accessible question input + submit, wired to the B-06 endpoint, with grounded-response and refusal rendering. The assistant remains **grounded, deterministic, local, non-actuating** — it answers from operator-selected persisted artifacts, never free-form.

---

## 1. Objective

1. Add a `POST` ask function to the assistant client (`assistantClient.ts`).
2. Build a real, accessible question input + submit surface (replacing/upgrading the cosmetic chips), with **operator-selected grounding artifacts**.
3. Render grounded responses (source ids + disclaimer + audit correlation) and classed refusals distinctly.
4. Handle loading / empty / error / 401 states honestly.

---

## 2. Scope

### F-01.1 — Ask API client
- Add `askAssistant(prompt, groundingSourceIds)` → `POST /api/v1/collaboration/assistant-respond` (Bearer JWT), returning the persisted `AssistantResearchResponse` (response **or** refusal).
- Keep the existing GET functions intact (no regression).

### F-01.2 — Question input + grounding selection
- A real, accessible question input (label, placeholder, `role`, keyboard submit) + a submit button.
- A **grounding-source selector**: the operator selects one or more persisted artifacts (intelligence reports, snapshots, etc.) to ground the answer — mirroring the B-06 contract (`grounding_source_ids` ≤ 10). If none selected, the submit still works and the backend returns `GROUNDING_REQUIRED` (honest, not an error).
- The static prompt-suggestion chips may remain as *clickable shortcuts* that pre-fill the input, but they are no longer the only surface.

### F-01.3 — Response rendering
- **Grounded response:** show the `grounding_summary`, `source_artifact_ids`, the `response_text`, and the mandatory disclaimer, plus the audit correlation id (small, muted).
- **Refusal:** render each refusal class plainly (e.g. "Refused: ORDER_INSTRUCTION_REFUSED") with the disclaimer — visually distinct from a grounded answer.
- **States:** loading (skeleton), empty (prompt first), error (banner), 401 (auth-required notice), all honest.

### F-01.4 — Boundary invariants (binding)
- The assistant UI must **not** imply the assistant is generative, autonomous, or financial advice. It must surface the "deterministic local assistant · no external LLM" disclosure and the "RESEARCH-ONLY · NON-ACTUATING" framing (already in the code; preserve it).
- **No** actuation controls anywhere in the assistant surface.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** external LLM integration, autonomous tools, or agent behavior (any such change needs a separate governing instrument).
- **No** order/execution/broker/account/gate controls.
- **No** change to the backend assistant contract (B-06 is fixed; this is a consumer).
- **No** ungrounded/free-form generation client-side.
- **No** weakening of accessibility or the design language (F-00 tokens/themes).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. `askAssistant` POST client function + a hook (e.g. `useAskAssistant`).
2. The accessible question input + submit + grounding selector.
3. Grounded-response and refusal rendering.
4. Tests (new/churn): submit → POST call, grounded render, refusal render, empty-grounding, 401, accessibility (label/focus/keyboard), no-actuation.
5. Delivery Report (§9) with relay-accurate transmission manifest + register-in-patch rows.

---

## 5. Dependencies

- **Upstream:** B-06 backend endpoint (delivered) · F-00 design foundation + theme system.
- **Downstream:** F-02 → F-06 inherit the assistant surface; X-01 Terminal Tier includes it.

---

## 6. Allowed files / components

- `frontend/src/api/assistantClient.ts` (add POST ask; keep GET).
- `frontend/src/workstation/ai/ContextualAssistantPanel.tsx` + related assistant components.
- `frontend/src/workstation/ai/AssistantCommandSurface.tsx` (if it hosts the input).
- `frontend/src/test/**` + relevant `*.test.tsx` (new/churn).
- `docs/governance/TECHNICAL_DEBT_REGISTER.md` (register-in-patch rows — **required**).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- Bearer JWT on the ask call; 401 handled gracefully (no token in URL, no logging of prompts).
- The prompt is sent as plain text to the *local* backend only — no third party (the backend is deterministic/local; verify no external call is introduced client-side either).
- The UI must not fabricate a response while loading or on error (honest empty/error states).
- Accessibility preserved (label, focus, keyboard, contrast per F-00 themes).

---

## 8. Acceptance criteria

- [ ] `askAssistant` posts to the correct endpoint with Bearer auth; GET functions unchanged.
- [ ] Question input + submit + grounding selector are accessible (label, keyboard, focus).
- [ ] A grounded ask renders the summary + source ids + disclaimer + audit correlation.
- [ ] Each refusal class renders distinctly and honestly.
- [ ] Empty-grounding and 401 states are handled (no fabricated response).
- [ ] No actuation controls in the assistant surface (test-pinned).
- [ ] Register rows for this unit ship in the patch (register-in-patch convention).
- [ ] Full frontend suite green (`npm test`) + typecheck green (`tsc -b`); executed output supplied.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1 + register-in-patch)

**Binding (CA-TRANSMIT-1):** artifacts uploaded and confirmed against the review channel.

**Binding (register-in-patch):** this unit's register rows must be in the patch.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed frontend test output + typecheck | Level II | run transcript |
| Screenshot captures (ask flow: grounded answer + a refusal + empty state) | Level I | images |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Ask-surface description (input, grounding selector, submit, response/refusal rendering)
4. Screenshot evidence (grounded + refusal + empty)
5. Boundary-invariant evidence (no-actuation, no-external, disclosure present)
6. Test evidence (executed)
7. Deviations register
8. Register rows in patch (confirmed)
9. Transmission manifest (relay-accurate)

---

## 11. Rollback / containment

- New client function + component changes are frontend-only; revert = revert patch.
- No backend change, no schema change, no new runtime dependency.

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of F-01, **F-02 (signal presentation)** and the remaining F-units may be issued, leading to the X-01 Terminal Tier.

---

**End of Build Order F-01**
