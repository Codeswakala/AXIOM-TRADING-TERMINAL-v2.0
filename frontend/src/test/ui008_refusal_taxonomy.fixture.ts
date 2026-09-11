// N-8: ui008_refusal_taxonomy.fixture.ts
// Source: /home/user/axiom/frontend/src/test/ui008_refusal_taxonomy.fixture.ts
// BO-UI008-P01 §1.5; D-2.6 conformance; six-code refusal taxonomy-of-record per BO §3.2
// Source-of-record: ITRGA_REVIEW_W5-U02 §3 R5-3 keystone (verbatim)

/**
 * The six refusal reason codes of record (W5-U02 keystone; BO §3.2).
 * Pin: byte-equal wherever they render; never re-typed.
 */
export const ASSISTANT_REFUSAL_REASON_CODES = [
  "ORDER_INSTRUCTION_REFUSED",
  "GATE_OPEN_INSTRUCTION_REFUSED",
  "SECRET_EXFILTRATION_REFUSED",
  "UNBOUNDED_TOOL_REQUEST_REFUSED",
  "GROUNDING_REQUIRED",
  "ASSISTANT_DISABLED",
] as const;

export type AssistantRefusalReasonCode = (typeof ASSISTANT_REFUSAL_REASON_CODES)[number];

/**
 * The five request-refusal classes (the "safety" subset).
 * ASSISTANT_DISABLED is the admin-state code (distinct from the five request-refusal classes).
 */
export const ASSISTANT_REQUEST_REFUSAL_REASON_CODES: readonly AssistantRefusalReasonCode[] = [
  "ORDER_INSTRUCTION_REFUSED",
  "GATE_OPEN_INSTRUCTION_REFUSED",
  "SECRET_EXFILTRATION_REFUSED",
  "UNBOUNDED_TOOL_REQUEST_REFUSED",
  "GROUNDING_REQUIRED",
] as const;

/** The admin-state refusal code (distinct from the five request-refusal classes). */
export const ASSISTANT_DISABLED_REASON: AssistantRefusalReasonCode = "ASSISTANT_DISABLED";

/**
 * Class rationale per ITRGA_REVIEW_W5-U02 §3 R5-3 (verbatim):
 * "All six refusal classes persisted with reason codes and matching audit events (DB JOIN)."
 *
 * The five request-refusal classes correspond to safety/adversarial conditions.
 * ASSISTANT_DISABLED corresponds to operator/system state: the assistant is
 * administratively disabled; requests return this refusal rather than any of the
 * five request-refusal classes.
 */
export const REFUSAL_CLASS_RATIONALE: Readonly<Record<AssistantRefusalReasonCode, string>> = {
  ORDER_INSTRUCTION_REFUSED:
    "order-intent / order-payload / side / quantity / position-size refused",
  GATE_OPEN_INSTRUCTION_REFUSED:
    "gate-open / allow-execution / governance-gate bypass refused",
  SECRET_EXFILTRATION_REFUSED:
    "secret / credential / API-key / token material refused",
  UNBOUNDED_TOOL_REQUEST_REFUSED:
    "unbounded / unscoped / batch tool call refused",
  GROUNDING_REQUIRED:
    "ungrounded claim; no source_artifact_ids; refusal-or-ground",
  ASSISTANT_DISABLED:
    "admin-state code; the operator or system has placed the assistant in a disabled state",
};
