import { describe, it, expect } from "vitest";
import {
  formatUncertaintyInterval,
  formatSampleCount,
  formatPearsonR,
  formatPips,
  formatPercent,
} from "./formatters";

describe("UI-009-P04 Uncertainty & Statistical Formatters (T-5, AC-5)", () => {
  it("formatUncertaintyInterval formats bounded confidence intervals deterministically", () => {
    const ci1 = formatUncertaintyInterval({ lower: -0.15, upper: 0.22, confidence: 0.95 });
    expect(ci1).toBe("95% CI [-0.15, +0.22]");

    const ci2 = formatUncertaintyInterval({ lower: 0.05, upper: 0.50, confidence: 0.90 });
    expect(ci2).toBe("90% CI [+0.05, +0.50]");

    // Single bound (lower === upper)
    const ciSingle = formatUncertaintyInterval({ lower: 0.42, upper: 0.42, confidence: 0.95 });
    expect(ciSingle).toBe("95% CI [+0.42]");

    // Invalid input fallback
    const ciInvalid = formatUncertaintyInterval({ lower: NaN, upper: 0.5 });
    expect(ciInvalid).toBe("CI [—, —]");
  });

  it("formatSampleCount formats sample count descriptors", () => {
    expect(formatSampleCount(120)).toBe("n=120");
    expect(formatSampleCount(5)).toBe("n=5");
    expect(formatSampleCount(0)).toBe("n=0");
    expect(formatSampleCount(-10)).toBe("n=0");
    expect(formatSampleCount(NaN)).toBe("n=0");
  });

  it("formatPearsonR formats correlation coefficients and clamps within [-1, 1]", () => {
    expect(formatPearsonR(0.73)).toBe("r=0.73");
    expect(formatPearsonR(-0.45)).toBe("r=-0.45");
    expect(formatPearsonR(0)).toBe("r=0.00");
    expect(formatPearsonR(1.5)).toBe("r=1.00");
    expect(formatPearsonR(-2.0)).toBe("r=-1.00");
    expect(formatPearsonR(NaN)).toBe("r=—");
  });

  it("formatPips formats currency pip metrics with sign prefixes", () => {
    expect(formatPips(14.2)).toBe("+14.2 pips");
    expect(formatPips(-5.0)).toBe("-5.0 pips");
    expect(formatPips(0)).toBe("0.0 pips");
    expect(formatPips(NaN)).toBe("— pips");
  });

  it("formatPercent formats percentage values", () => {
    expect(formatPercent(12.5)).toBe("12.5%");
    expect(formatPercent(-3.2)).toBe("-3.2%");
    expect(formatPercent(0.456, 1)).toBe("0.5%");
    expect(formatPercent(NaN)).toBe("—%");
  });
});
