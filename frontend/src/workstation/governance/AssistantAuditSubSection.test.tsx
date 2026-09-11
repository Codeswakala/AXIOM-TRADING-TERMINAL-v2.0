// N-5: AssistantAuditSubSection.test.tsx
// Source: /home/user/axiom/frontend/src/workstation/governance/AssistantAuditSubSection.test.tsx
// BO-UI008-P01 §5 named tests; render-only; vitest; no live wiring
// Tests: 21, 22, 23, 27 (render-only limbs)

import { describe, expect, it } from "vitest";
import { render, screen, within } from "@testing-library/react";
import { AssistantAuditSubSection } from "./AssistantAuditSubSection";
import { ASSISTANT_REFUSAL_REASON_CODES } from "../../test/ui008_refusal_taxonomy.fixture";

describe("UI-008 P01 AssistantAuditSubSection (P01 skeleton; render-only)", () => {
  // Test 20: workspace_registry_zero_new_entries (P01 limb)
  it("test_ui008_workspace_registry_zero_new_entries__audit_sub_section_is_sub_section_not_workspace", () => {
    const { container } = render(<AssistantAuditSubSection />);
    const subSection = container.querySelector('[data-ui008-component="assistant-audit-sub-section"]');
    expect(subSection).not.toBeNull();
    expect(subSection?.getAttribute("role")).toBe("region");
  });

  // Test 21: open_register_rendered_at_full_severity
  it("test_ui008_open_register_rendered_at_full_severity__audit_sub_section", () => {
    render(<AssistantAuditSubSection />);
    const register = screen.getByRole("list", { name: /Carried-Open Register/i });
    expect(register).toBeInTheDocument();
    const rows = within(register).getAllByRole("listitem");
    expect(rows.length).toBeGreaterThanOrEqual(18);
  });

  // Test 22: no_color_alone_disclosure_discipline
  it("test_ui008_no_color_alone_disclosure_discipline__audit_sub_section", () => {
    const { container } = render(<AssistantAuditSubSection />);
    const rows = container.querySelectorAll('[data-ui008-disclosure-row]');
    expect(rows.length).toBeGreaterThanOrEqual(18);
    for (const row of rows) {
      expect(row.querySelector('[data-ui008-icon]')).not.toBeNull();
      expect(row.querySelector('[data-ui008-severity]')).not.toBeNull();
      expect(row.querySelector('[data-ui008-disclosure-text]')).not.toBeNull();
      expect(row.querySelector('[data-ui008-source-pin]')).not.toBeNull();
    }
  });

  // Test 23: assistant_ai_generated_disclaimer_rendered (render-only limb)
  it("test_ui008_assistant_ai_generated_disclaimer_rendered__audit_sub_section__render_only_limb", () => {
    render(<AssistantAuditSubSection />);
    const disclaimer = screen.getByTestId("r5-6");
    expect(disclaimer).toBeInTheDocument();
    expect(disclaimer.textContent).toContain("AXIOM does not act");
  });

  // Test 23: TD-078 self-description banner (R-7 REQUIRED)
  it("test_ui008_self_description_banner__audit_sub_section__td_078_r7_required", () => {
    render(<AssistantAuditSubSection />);
    const banner = screen.getByTestId("td-078-self-description");
    expect(banner).toBeInTheDocument();
    expect(banner.textContent).toBe("deterministic local assistant; no external LLM; external LLM requires a future gated Build Order");
  });

  // Test 27: refusal_surface_renders_all_six_taxonomy_codes
  it("test_ui008_refusal_surface_renders_all_six_taxonomy_codes__audit_sub_section", () => {
    render(<AssistantAuditSubSection />);
    const refusalSurface = screen.getByRole("list", { name: /Refusal Taxonomy/i });
    expect(refusalSurface).toBeInTheDocument();
    for (const code of ASSISTANT_REFUSAL_REASON_CODES) {
      const codeEl = within(refusalSurface).getByTestId(code);
      expect(codeEl).toBeInTheDocument();
    }
  });
});
