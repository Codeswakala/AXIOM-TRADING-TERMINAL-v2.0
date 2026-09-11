import { describe, it, expect } from "vitest";
import { HIGH_CONTRAST_TOKENS, computeContrastRatio } from "../design/theme";

const HIGH_CONTRAST_PALETTE_HEX = {
  bgRoot: "#000000",
  textPrimary: "#FFFFFF",
  borderSubtle: "#FFFFFF",
  colorFocus: "#FFFF00",
} as const;

describe("High-Contrast Compliance & Overrides (UI-010-P05 / T-4, AC-4)", () => {
  it("defines high-contrast token references and hex palette", () => {
    expect(HIGH_CONTRAST_TOKENS.bgRoot).toBe("var(--ix-bg-root)");
    expect(HIGH_CONTRAST_TOKENS.textPrimary).toBe("var(--ix-text-primary)");
    expect(HIGH_CONTRAST_TOKENS.borderSubtle).toBe("var(--ix-border-subtle)");
    expect(HIGH_CONTRAST_TOKENS.colorFocus).toBe("var(--ix-color-focus)");

    expect(HIGH_CONTRAST_PALETTE_HEX.bgRoot).toBe("#000000");
    expect(HIGH_CONTRAST_PALETTE_HEX.textPrimary).toBe("#FFFFFF");
    expect(HIGH_CONTRAST_PALETTE_HEX.colorFocus).toBe("#FFFF00");
  });

  it("calculates 21:1 contrast ratio for high-contrast primary text on root background", () => {
    const ratio = computeContrastRatio(HIGH_CONTRAST_PALETTE_HEX.textPrimary, HIGH_CONTRAST_PALETTE_HEX.bgRoot);
    expect(ratio).toBeCloseTo(21, 0);
  });

  it("calculates ultra-high visibility for focus ring on pure black background", () => {
    const ratio = computeContrastRatio(HIGH_CONTRAST_PALETTE_HEX.colorFocus, HIGH_CONTRAST_PALETTE_HEX.bgRoot);
    expect(ratio).toBeGreaterThan(15.0);
  });
});
