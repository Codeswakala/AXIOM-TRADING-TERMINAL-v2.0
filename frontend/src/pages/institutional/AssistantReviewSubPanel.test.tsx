// N-6: AssistantReviewSubPanel.test.tsx
// Source: /home/user/axiom/frontend/src/pages/institutional/AssistantReviewSubPanel.test.tsx
// BO-UI008-P01 §5 named tests; render-only; vitest; no live wiring
// Tests: 20, 23 (render-only limb), TD-078 banner

import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { AssistantReviewSubPanel } from "./AssistantReviewSubPanel";

describe("UI-008 P01 AssistantReviewSubPanel (P01 skeleton; render-only)", () => {
  // Test 20: workspace_registry_zero_new_entries (P01 limb)
  it("test_ui008_workspace_registry_zero_new_entries__review_sub_panel_is_sub_panel_not_workspace", () => {
    const { container } = render(<AssistantReviewSubPanel />);
    const subPanel = container.querySelector('[data-ui008-component="assistant-review-sub-panel"]');
    expect(subPanel).not.toBeNull();
    expect(subPanel?.getAttribute("role")).toBe("region");
  });

  // Test 23: assistant_ai_generated_disclaimer_rendered (render-only limb)
  it("test_ui008_assistant_ai_generated_disclaimer_rendered__review_sub_panel__render_only_limb", () => {
    render(<AssistantReviewSubPanel />);
    const disclaimer = screen.getByTestId("r5-6");
    expect(disclaimer).toBeInTheDocument();
    expect(disclaimer.textContent).toContain("AXIOM does not act");
  });

  // Test 23: TD-078 self-description banner (R-7 REQUIRED)
  it("test_ui008_self_description_banner__review_sub_panel__td_078_r7_required", () => {
    render(<AssistantReviewSubPanel />);
    const banner = screen.getByTestId("td-078-self-description");
    expect(banner).toBeInTheDocument();
    expect(banner.textContent).toBe("deterministic local assistant; no external LLM; external LLM requires a future gated Build Order");
  });

  // Empty state (F-16): P01 honest-empty
  it("test_ui008_p01_honest_empty_state__review_sub_panel__f_16", () => {
    render(<AssistantReviewSubPanel />);
    const empty = screen.getByTestId("p01-skeleton");
    expect(empty).toBeInTheDocument();
    expect(empty.textContent).toContain("Institutional-intelligence integration deferred to P03+");
  });
});
