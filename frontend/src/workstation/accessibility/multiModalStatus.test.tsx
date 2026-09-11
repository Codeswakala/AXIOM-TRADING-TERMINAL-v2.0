import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Badge, StatusChip, Toast, ErrorBanner } from "../../components/ui";

describe("Multi-Modal Status Encoding Verification (UI-010-P05 / T-3, AC-3)", () => {
  it("Badge renders text label alongside variant class (not color alone)", () => {
    render(<Badge variant="critical">CRITICAL ALERT</Badge>);
    const label = screen.getByText("CRITICAL ALERT");
    expect(label).toBeInTheDocument();
    expect(label.closest(".ix-badge")).toHaveClass("ix-badge--critical");
  });

  it("StatusChip renders symbol and textual label together", () => {
    render(<StatusChip level="HIGH" label="High Confidence" />);
    expect(screen.getByText("◆◆◆")).toBeInTheDocument();
    expect(screen.getByText("High Confidence")).toBeInTheDocument();
  });

  it("Toast renders semantic symbol, uppercase badge, and title text", () => {
    render(
      <Toast
        id="toast-warn"
        variant="warning"
        title="Ingestion Delay"
        description="Market feed latency exceeding threshold."
        onDismiss={() => {}}
      />,
    );
    expect(screen.getByTestId("toast-symbol")).toHaveTextContent("⚠");
    expect(screen.getByText("WARNING")).toBeInTheDocument();
    expect(screen.getByTestId("toast-title")).toHaveTextContent("Ingestion Delay");
  });

  it("ErrorBanner renders distinct symbol, badge text, and explicit message", () => {
    render(
      <ErrorBanner
        title="Persistence Unreachable"
        message="SQLite storage layer returned I/O timeout."
        variant="error"
      />,
    );
    expect(screen.getByTestId("error-banner-icon")).toHaveTextContent("✕");
    expect(screen.getByText("ERROR")).toBeInTheDocument();
    expect(screen.getByTestId("error-banner-title")).toHaveTextContent("Persistence Unreachable");
    expect(screen.getByTestId("error-banner-message")).toHaveTextContent("SQLite storage layer returned I/O timeout.");
  });
});
