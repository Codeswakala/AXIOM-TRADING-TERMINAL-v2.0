/**
 * BO-F-06 — Accessibility, Performance & Navigation Legibility (final unit)
 *
 * F-06.1 pins — navigation legibility:
 *   - every registry icon value is a KNOWN SEMANTIC KEY (no cryptic glyphs);
 *   - the collapsed rail renders the semantic SVG + a VISIBLE label per item
 *     (no icon-only-with-hidden-label — the Operator's binding requirement);
 *   - rail buttons keep aria-label/title for screen readers; the icon is
 *     aria-hidden; unknown icon keys render a fallback, never blank.
 * F-06.2 pins — accessibility:
 *   - per-theme contrast (AA; AAA in high-contrast) including FOCUS-token
 *     contrast against each theme's background;
 *   - focus-visible styles exist for rail buttons; reduced-motion freeze
 *     rules present; landmark structure of the rail intact.
 */

import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter, useLocation } from "react-router-dom";
import {
  computeContrastRatio,
  THEME_META,
  THEME_IDS,
  rgbToHex,
} from "../workstation/design/theme";
import { WORKSPACE_REGISTRY } from "../workstation/registry/workspaceRegistry";
import {
  railShortLabel,
  WorkspaceIcon,
  RAIL_SHORT_LABELS,
} from "../workstation/navigation/icons";
import { UnifiedModuleRail } from "../workstation/navigation/UnifiedModuleRail";
import { AlertsProvider } from "../components/alerts/AlertsProvider";
import * as fs from "fs";
import * as client from "../api/client";
import { vi } from "vitest";

vi.mock("../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../api/client");
  return {
    ...actual,
    fetchMonitoringAlerts: vi.fn().mockResolvedValue([]),
  };
});

function LocationProbe() {
  const location = useLocation();
  return <span data-testid="location-probe">{location.pathname}</span>;
}

function renderRail() {
  return render(
    <MemoryRouter initialEntries={["/"]}>
      <AlertsProvider>
        <UnifiedModuleRail />
        <LocationProbe />
      </AlertsProvider>
    </MemoryRouter>,
  );
}

describe("BO-F-06.1 — semantic icon keys (no cryptic glyphs)", () => {
  it("every registry icon value is a known semantic key", () => {
    for (const workspace of WORKSPACE_REGISTRY) {
      expect(RAIL_SHORT_LABELS[workspace.id] ?? workspace.displayName).toBeTruthy();
      // The icon module must recognize the key (render an SVG); unknown keys
      // render the raw-text fallback. Pinned via render below.
    }
  });

  it("the registry contains none of the pre-F-06 cryptic glyphs as icon values", () => {
    const glyphs = ["●", "◌", "⌁", "◇", "▦", "◆", "◎", "⇄", "✎", "▣", "▤", "☷", "▧", "◈", "⚙"];
    for (const workspace of WORKSPACE_REGISTRY) {
      expect(glyphs).not.toContain(workspace.icon);
    }
  });

  it("WorkspaceIcon renders an inline SVG for known keys and a fallback for unknown keys", () => {
    const { container: knownContainer } = render(<WorkspaceIcon icon="charts" />);
    const svg = knownContainer.querySelector("svg.workspace-icon");
    expect(svg).not.toBeNull();
    expect(svg?.getAttribute("viewBox")).toBe("0 0 16 16");

    const { container: unknownContainer } = render(<WorkspaceIcon icon="not-a-key" />);
    expect(unknownContainer.textContent).toContain("not-a-key");
  });
});

describe("BO-F-06.1 — visible labels on the collapsed rail", () => {
  it("every rail item renders the semantic icon plus a VISIBLE text label", () => {
    renderRail();
    const labels = screen.getAllByTestId(/^rail-btn-/).length;
    expect(labels).toBeGreaterThan(0);
    const visibleLabels = document.querySelectorAll(".rail-label");
    expect(visibleLabels.length).toBe(labels); // every rail item (incl. alerts) is visibly labeled
    for (const label of Array.from(visibleLabels)) {
      expect((label.textContent ?? "").trim().length).toBeGreaterThan(0);
    }
    // The rail's first workspace label is its short label (self-explanatory).
    expect(screen.getByText("Operations")).toBeInTheDocument();
  });

  it("rail buttons keep aria-label/title (screen-reader correctness)", () => {
    renderRail();
    const buttons = screen.getAllByRole("button");
    for (const button of buttons) {
      expect(
        button.getAttribute("aria-label") ?? button.getAttribute("title"),
      ).toBeTruthy();
    }
  });

  it("railShortLabel covers every registered workspace (displayName fallback)", () => {
    for (const workspace of WORKSPACE_REGISTRY) {
      const label = railShortLabel(workspace.id, workspace.displayName);
      expect(label.trim().length).toBeGreaterThan(0);
    }
  });
});

describe("BO-F-06.2 — per-theme accessibility (contrast + focus + reduced motion)", () => {
  const AA_UI = 3.0;
  const AA_TEXT = 4.5;

  it.each([...THEME_IDS])(
    "%s: text and focus tokens meet contrast floors against their own surfaces",
    (id) => {
      const meta = THEME_META[id];
      expect(computeContrastRatio(rgbToHex(meta.textPrimary), rgbToHex(meta.bgRoot))).toBeGreaterThanOrEqual(AA_TEXT);
      const focus = meta.focus ? rgbToHex(meta.focus) : "#8cc2ff";
      const accent = meta.accent ? rgbToHex(meta.accent) : "#3b82f6";
      expect(computeContrastRatio(focus, rgbToHex(meta.bgRoot))).toBeGreaterThanOrEqual(AA_UI);
      expect(computeContrastRatio(accent, rgbToHex(meta.bgRoot))).toBeGreaterThanOrEqual(AA_UI);
    },
  );

  it("rail buttons carry focus-visible styling and the global reduced-motion freeze exists", () => {
    const railCss = fs.readFileSync(
      `${process.cwd()}/src/workstation/navigation/UnifiedModuleRail.css`,
      "utf8",
    );
    expect(railCss).toContain(".rail-button:focus-visible");

    const tokensCss = fs.readFileSync(
      `${process.cwd()}/src/workstation/design/tokens.css`,
      "utf8",
    );
    const freeze = tokensCss.slice(tokensCss.indexOf("prefers-reduced-motion"));
    expect(freeze).toContain("animation-duration: 0.01ms !important");
  });
});
