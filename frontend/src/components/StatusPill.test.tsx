import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { StatusPill } from "./StatusPill";

describe("StatusPill", () => {
  it("renders healthy label", () => {
    render(<StatusPill state="ok" />);
    expect(screen.getByText("Healthy")).toBeInTheDocument();
  });

  it("renders custom label", () => {
    render(<StatusPill state="loading" label="connecting" />);
    expect(screen.getByText("connecting")).toBeInTheDocument();
  });
});
