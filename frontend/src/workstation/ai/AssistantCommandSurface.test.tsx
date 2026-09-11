// N-4: AssistantCommandSurface.test.tsx
// Source: /home/user/axiom/frontend/src/workstation/ai/AssistantCommandSurface.test.tsx
// BO-UI008-P01 §5 named tests; render-only; vitest; no live wiring
// Tests: 20 (workspace_registry_zero_new_entries), 21 (open_register_rendered_at_full_severity),
//        22 (no_color_alone_disclosure_discipline), 23 (assistant_ai_generated_disclaimer_rendered — render-only limb)

import { describe, expect, it } from "vitest";
import { render, screen, within } from "@testing-library/react";
import { AssistantCommandSurface } from "./AssistantCommandSurface";
import { ASSISTANT_REFUSAL_REASON_CODES, ASSISTANT_DISABLED_REASON } from "../../test/ui008_refusal_taxonomy.fixture";

describe("UI-008 P01 AssistantCommandSurface (P01 skeleton; render-only)", () => {
  // Test 20: workspace_registry_zero_new_entries (P01 limb; the surface is a sub-section, not a workspace entry)
  it("test_ui008_workspace_registry_zero_new_entries__command_surface_is_sub_section_not_workspace", () => {
    const { container } = render(<AssistantCommandSurface />);
    // The surface renders as a sub-section (role=region), NOT as a workspace route
    const surface = container.querySelector('[data-ui008-component="assistant-command-surface"]');
    expect(surface).not.toBeNull();
    expect(surface?.getAttribute("role")).toBe("region");
    // No new route declared; the surface renders without a Route registration
    expect(surface?.getAttribute("data-ui008-p01-skeleton-empty")).toBe("true");
  });

  // Test 21: open_register_rendered_at_full_severity
  it("test_ui008_open_register_rendered_at_full_severity__command_surface", () => {
    render(<AssistantCommandSurface />);
    const register = screen.getByRole("list", { name: /Carried-Open Register/i });
    expect(register).toBeInTheDocument();
    // Every disclosure-register row is rendered with text + icon + position (never color alone; BO §3.7)
    const rows = within(register).getAllByRole("listitem");
    expect(rows.length).toBeGreaterThanOrEqual(18);
    for (const row of rows) {
      const text = within(row).getByTestId("disclosure-text");
      const sourcePin = within(row).getByTestId("source-pin");
      expect(text.textContent).toBeTruthy();
      expect(sourcePin.textContent).toMatch(/source:/);
    }
  });

  // Test 22: no_color_alone_disclosure_discipline
  it("test_ui008_no_color_alone_disclosure_discipline__command_surface", () => {
    const { container } = render(<AssistantCommandSurface />);
    // Every disclosure row carries an icon, a severity text, an ID, and a source pin (never color alone)
    const rows = container.querySelectorAll('[data-ui008-disclosure-row]');
    expect(rows.length).toBeGreaterThanOrEqual(18);
    for (const row of rows) {
      const id = row.querySelector('[class*="id"]');
      const severity = row.querySelector('[data-ui008-severity]');
      const icon = row.querySelector('[data-ui008-icon]');
      const text = row.querySelector('[data-ui008-disclosure-text]');
      const sourcePin = row.querySelector('[data-ui008-source-pin]');
      expect(id).not.toBeNull();
      expect(severity).not.toBeNull();
      expect(icon).not.toBeNull();
      expect(text).not.toBeNull();
      expect(sourcePin).not.toBeNull();
    }
  });

  // Test 23 (render-only limb; the browser limb is the D-2.5 served-browser screenshot)
  it("test_ui008_assistant_ai_generated_disclaimer_rendered__command_surface__render_only_limb", () => {
    render(<AssistantCommandSurface />);
    const disclaimer = screen.getByTestId("r5-6");
    expect(disclaimer).toBeInTheDocument();
    expect(disclaimer.textContent).toContain("AI-generated research assistance only");
    expect(disclaimer.textContent).toContain("AXIOM does not act");
  });

  // Test 23: TD-078 self-description banner (R-7 REQUIRED)
  it("test_ui008_self_description_banner__command_surface__td_078_r7_required", () => {
    render(<AssistantCommandSurface />);
    const banner = screen.getByTestId("td-078-self-description");
    expect(banner).toBeInTheDocument();
    expect(banner.textContent).toBe("deterministic local assistant; no external LLM; external LLM requires a future gated Build Order");
  });

  // Test 27: refusal_surface_renders_all_six_taxonomy_codes
  it("test_ui008_refusal_surface_renders_all_six_taxonomy_codes__command_surface", () => {
    render(<AssistantCommandSurface />);
    const refusalSurface = screen.getByRole("list", { name: /Refusal Taxonomy/i });
    expect(refusalSurface).toBeInTheDocument();
    for (const code of ASSISTANT_REFUSAL_REASON_CODES) {
      const codeEl = within(refusalSurface).getByTestId(code);
      expect(codeEl).toBeInTheDocument();
    }
    const disabledEl = within(refusalSurface).getByTestId(ASSISTANT_DISABLED_REASON);
    expect(disabledEl).toBeInTheDocument();
  });

  // Empty state (F-16): P01 honest-empty; no fabricated responses
  it("test_ui008_p01_honest_empty_state__command_surface__f_16", () => {
    render(<AssistantCommandSurface />);
    const empty = screen.getByTestId("p01-skeleton");
    expect(empty).toBeInTheDocument();
    expect(empty.textContent).toContain("Live wiring deferred to P02");
  });
});
