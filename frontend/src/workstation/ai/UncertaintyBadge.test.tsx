import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { UncertaintyBadge, computeConfidenceLevel } from "./UncertaintyBadge";

describe("UI-008-P04 UncertaintyBadge Component (T-3, U-1, U-4)", () => {
  it("renders confidence level and calibrated percentage (T-3, U-1)", () => {
    render(
      <UncertaintyBadge
        confidenceLevel="HIGH"
        calibratedConfidence={0.88}
        sampleCount={120}
        statusLabel="CALIBRATED"
      />,
    );

    const badge = screen.getByTestId("uncertainty-badge");
    expect(badge).toBeInTheDocument();
    expect(badge.getAttribute("data-ui008-confidence-level")).toBe("HIGH");
    expect(screen.getByTestId("confidence-level-text")).toHaveTextContent("HIGH CONFIDENCE");
    expect(screen.getByTestId("confidence-percent")).toHaveTextContent("88.0% calibrated");
    expect(screen.getByTestId("sample-count")).toHaveTextContent("n=120");
    expect(screen.getByTestId("calibration-status")).toHaveTextContent("CALIBRATED");
  });

  it("renders uncertainty interval bounds when supplied (U-4)", () => {
    render(
      <UncertaintyBadge
        confidenceLevel="MODERATE"
        calibratedConfidence={0.65}
        interval={{ lower: -0.15, upper: 0.22, confidenceLevel: 0.95 }}
      />,
    );

    const interval = screen.getByTestId("uncertainty-interval");
    expect(interval).toBeInTheDocument();
    expect(interval.textContent).toContain("95% CI: [-0.15, +0.22]");
  });

  it("computeConfidenceLevel helper calculates correct confidence levels", () => {
    expect(computeConfidenceLevel(null)).toBe("UNCALIBRATED");
    expect(computeConfidenceLevel(0.8, 5)).toBe("LIMITED"); // low sample size
    expect(computeConfidenceLevel(0.85, 100)).toBe("HIGH");
    expect(computeConfidenceLevel(0.60, 100)).toBe("MODERATE");
    expect(computeConfidenceLevel(0.40, 100)).toBe("LIMITED");
  });
});
