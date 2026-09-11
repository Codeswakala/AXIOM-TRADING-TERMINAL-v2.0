// N-10: ui008_assistant_disabled_state_refusal_persisted_and_audited.test.ts
// Source: /home/user/axiom/frontend/src/test/ui008_assistant_disabled_state_refusal_persisted_and_audited.test.ts
// BO-UI008-P01 §5; the F-G2-2 sixth-code addition; vitest; render-only at P01 (no live wiring)
// P01 disposition: the refusal surface renders the ASSISTANT_DISABLED code in the taxonomy fixture
// (test 27 covers rendering; this test pins the persistence expectation for P02+ wiring)

import { describe, expect, it } from "vitest";
import { ASSISTANT_DISABLED_REASON, ASSISTANT_REFUSAL_REASON_CODES } from "./ui008_refusal_taxonomy.fixture";

describe("UI-008 P01 test 11/27 assistant_disabled_state_refusal (P01 render-only; P02+ wiring)", () => {
  it("test_ui008_assistant_disabled_state_refusal_persisted_and_audited__taxonomy_includes_disabled", () => {
    // P01 render-only limb: the taxonomy fixture must include ASSISTANT_DISABLED
    expect(ASSISTANT_REFUSAL_REASON_CODES).toContain(ASSISTANT_DISABLED_REASON);
    expect(ASSISTANT_DISABLED_REASON).toBe("ASSISTANT_DISABLED");
    // P02+ wiring expectation (deferred): when the assistant is administratively disabled,
    // a refusal is persisted to assistant_research_responses with refused=true +
    // refusal_reason=ASSISTANT_DISABLED, and the corresponding audit_events row carries
    // action="assistant.refused" + details.refusal_reason="ASSISTANT_DISABLED".
    // The P01 skeleton does not exercise the live wiring; the test class is pinned here.
  });
});
