import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { RouteAnnouncer } from "./RouteAnnouncer";

describe("RouteAnnouncer (UI-010-P05 / T-1, AC-1)", () => {
  it("renders live region with role='status', aria-live='polite', and aria-atomic='true'", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <RouteAnnouncer />
      </MemoryRouter>,
    );

    const liveRegion = screen.getByTestId("route-announcer");
    expect(liveRegion).toBeInTheDocument();
    expect(liveRegion).toHaveAttribute("role", "status");
    expect(liveRegion).toHaveAttribute("aria-live", "polite");
    expect(liveRegion).toHaveAttribute("aria-atomic", "true");
    expect(liveRegion).toHaveAttribute("aria-label", "Route announcements");
    expect(liveRegion).toHaveClass("ix-sr-only");
  });

  it("announces route navigation to active workspace", () => {
    render(
      <MemoryRouter initialEntries={["/charts"]}>
        <RouteAnnouncer />
      </MemoryRouter>,
    );

    const liveRegion = screen.getByTestId("route-announcer");
    expect(liveRegion).toHaveTextContent(/Navigated to Chart Workspace/);
  });

  it("supports explicit custom routeTitle override", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <RouteAnnouncer routeTitle="Custom Operational Intelligence" />
      </MemoryRouter>,
    );

    const liveRegion = screen.getByTestId("route-announcer");
    expect(liveRegion).toHaveTextContent("Navigated to Custom Operational Intelligence");
  });
});
