// N-7: AssistantCommandSurface.disclaimer.test.tsx
// Source: /home/user/axiom/frontend/src/workstation/ai/AssistantCommandSurface.disclaimer.test.tsx
// BO-UI008-P01 §5 test 23; render-only limb; vitest; the D-2.5 served-browser screenshot is a separate
// Operator-run evidence item at the delivery report.

import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { AssistantCommandSurface } from "./AssistantCommandSurface";

describe("UI-008 P01 test 23 assistant_ai_generated_disclaimer_rendered (render-only limb)", () => {
  it("test_ui008_assistant_ai_generated_disclaimer_rendered__command_surface", () => {
    render(<AssistantCommandSurface />);
    const disclaimer = screen.getByTestId("r5-6");
    expect(disclaimer).toBeInTheDocument();
    // Byte-equal to the BO §3.4 pinned string
    expect(disclaimer.textContent).toBe(
      "AI-generated research assistance only. Not financial advice, not an instruction, may be wrong. Operator judgment required. AXIOM does not act."
    );
  });
});
