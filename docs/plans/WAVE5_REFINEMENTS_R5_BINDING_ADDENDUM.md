# Wave-5 Design Plan Binding Refinements Addendum

| Field | Value |
|---|---|
| Source review | `docs/build-orders/ITRGA_REVIEW_WAVE5_DESIGN_PLAN.md` |
| Wave | 5 — Human-AI Collaboration |
| Status | Design plan accepted with refinements; no implementation authorized |
| Date recorded | 2026-07-16 |

---

## 1. ITRGA disposition

ITRGA accepted the Wave-5 Design Plan with refinements R5-1 through R5-8.

This addendum records those refinements as binding requirements for future Wave-5 Build Orders.

---

## 2. Binding refinements

| ID | Binding refinement summary | Applies |
|---|---|---|
| R5-1 | Non-actuation must be proven structurally through the assistant tool registry and wave-wide grep, not only tests. | W5-U01 and assistant units |
| R5-2 | W5-U01 uses no external LLM/API and no unspiked dependency; any future LLM is a separate hard-gated unit. | W5-U01+ |
| R5-3 | Prompt-injection and secret-exfiltration refusal tests are mandatory and each refusal must be audited; sampled-output secret-marker check required. | W5-U01 and assistant-touching units |
| R5-4 | Plan/journal inertness must be proven by inert schema, named rejection tests, grep, and no-action tests. | W5-U01 contracts and W5-U06/W5-U07 |
| R5-5 | Assistant response must have grounding/provenance or refuse. No ungrounded claims. | Every assistant unit |
| R5-6 | AI-generated output disclaimer must be visible and browser-proven for assistant UI surfaces. | Assistant UI units |
| R5-7 | Every new collaboration table requires first-submission raw SELECT + no-orphan audit proof. | Every artifact-introducing unit |
| R5-8 | Wave-wide bright-line grep and Git-Bash CI with `LOCAL_CI_EXIT_CODE: 0` are mandatory every unit. | Every Wave-5 unit |

---

## 3. DA boundary

The design plan acceptance does not authorize implementation.

DA will not begin W5-U01 until ITRGA issues `BUILD_ORDER_W5-U01.md` and the operator authorizes that Build Order.

---

**End of Wave-5 Refinements Addendum**
