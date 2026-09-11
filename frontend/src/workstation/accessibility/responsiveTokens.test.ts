import { describe, it, expect } from "vitest";
import { BREAKPOINT_TOKENS, BREAKPOINTS_PX, TABLE_TOKENS } from "../design/theme";

describe("UI-010-P02 Responsive Breakpoint Tokens & Theme Contracts (T-1, AC-1)", () => {
  it("AC-1: confirms breakpoint tokens and sticky header z-index are defined in theme contracts", () => {
    expect(BREAKPOINT_TOKENS.lg).toBe("var(--ix-breakpoint-lg)");
    expect(BREAKPOINT_TOKENS.md).toBe("var(--ix-breakpoint-md)");
    expect(BREAKPOINT_TOKENS.sm).toBe("var(--ix-breakpoint-sm)");

    expect(BREAKPOINTS_PX.lg).toBe(1280);
    expect(BREAKPOINTS_PX.md).toBe(1024);
    expect(BREAKPOINTS_PX.sm).toBe(768);

    expect(TABLE_TOKENS.stickyHeaderZIndex).toBe("var(--ix-table-sticky-header-z-index)");
  });
});
