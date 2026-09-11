import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MOTION_TOKENS, institutionalTheme } from "./theme";
import {
  Button,
  Select,
  Collapsible,
  Toast,
  Dialog,
} from "../../components/ui";

describe("Micro-Interaction Consistency & Motion Restraint (UI-011-P03 / T-1, T-2, AC-1, AC-2, AC-3)", () => {
  it("AC-1: defines motion timing tokens and standardized ease curve in theme contract", () => {
    expect(MOTION_TOKENS.fast).toBe("var(--ix-motion-fast)");
    expect(MOTION_TOKENS.standard).toBe("var(--ix-motion-standard)");
    expect(MOTION_TOKENS.panel).toBe("var(--ix-motion-panel)");
    expect(MOTION_TOKENS.ease).toBe("var(--ix-motion-ease)");

    expect(institutionalTheme.motion.fast).toBe("var(--ix-motion-fast)");
    expect(institutionalTheme.motion.ease).toBe("var(--ix-motion-ease)");
  });

  it("AC-1 & AC-2: renders interactive Button with standardized micro-interaction classes and variants", () => {
    const { rerender } = render(
      <Button variant="primary" size="md">
        Execute Observation
      </Button>,
    );

    const button = screen.getByRole("button", { name: "Execute Observation" });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass("ix-button");
    expect(button).toHaveClass("ix-button--primary");
    expect(button).toHaveClass("ix-button--md");

    rerender(
      <Button variant="secondary" size="sm">
        Secondary Action
      </Button>,
    );
    expect(screen.getByRole("button", { name: "Secondary Action" })).toHaveClass("ix-button--secondary");

    rerender(
      <Button variant="ghost" size="lg">
        Ghost Action
      </Button>,
    );
    expect(screen.getByRole("button", { name: "Ghost Action" })).toHaveClass("ix-button--ghost");

    rerender(
      <Button variant="destructive" size="md">
        Destructive Reset
      </Button>,
    );
    expect(screen.getByRole("button", { name: "Destructive Reset" })).toHaveClass("ix-button--destructive");
  });

  it("AC-1 & AC-2: renders Select component with interactive trigger and option states", () => {
    const options = [
      { value: "EURUSD", label: "EUR / USD" },
      { value: "GBPUSD", label: "GBP / USD" },
    ];
    render(
      <Select
        label="Select Instrument"
        options={options}
        value="EURUSD"
        onChange={() => {}}
      />,
    );

    const trigger = screen.getByRole("button", { name: /select instrument/i });
    expect(trigger).toBeInTheDocument();
    expect(trigger).toHaveClass("ix-select-trigger");
    expect(screen.getByText("EUR / USD")).toBeInTheDocument();
  });

  it("AC-1, AC-2 & AC-3: renders Collapsible, Toast, and Dialog with micro-interaction surfaces", () => {
    render(
      <div>
        <Collapsible title="Market Risk Telemetry" defaultExpanded={true}>
          <p>Collapsible risk content with motion restraint.</p>
        </Collapsible>
        <Toast
          id="toast-01"
          variant="info"
          title="Telemetry Update"
          description="Signal batch processed with 120ms transition curve."
          onDismiss={() => {}}
        />
        <Dialog
          open={true}
          onClose={() => {}}
          title="Institutional Confirmation"
          description="Advisory research overlay frame."
        >
          <p>Dialog body adhering to reduced-motion and motion restraint.</p>
        </Dialog>
      </div>,
    );

    expect(screen.getByRole("button", { name: "Market Risk Telemetry" })).toHaveClass("ix-collapsible__trigger");
    expect(screen.getByText("Collapsible risk content with motion restraint.")).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveClass("ix-toast");
    expect(screen.getByRole("dialog")).toHaveClass("ix-dialog");
  });
});
