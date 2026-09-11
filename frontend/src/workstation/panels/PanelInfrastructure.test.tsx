import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { WORKSPACE_REGISTRY } from "../registry/workspaceRegistry";
import { ShellEventBusProvider } from "../events/shellEventBus";
import { computeDockArrangement, placementSignature } from "./dockingEngine";
import {
  createSessionLayoutStore,
  defaultLayoutForWorkspace,
  resizePanel,
  restoreLayout,
  serializeLayout,
  validateLayout,
} from "./layoutManager";
import { PanelHost } from "./PanelHost";
import { PANEL_REGISTRY } from "./panelRegistry";

describe("PanelInfrastructure", () => {
  it("test_panel_registry_only_registered_panels_participate", () => {
    const registered = new Set(PANEL_REGISTRY.map((panel) => panel.id));
    const layout = defaultLayoutForWorkspace("monitor.operations");
    expect(layout.placements.length).toBe(PANEL_REGISTRY.length);
    for (const placement of layout.placements) {
      expect(registered.has(placement.panelId)).toBe(true);
    }
    expect(() =>
      validateLayout({
        ...layout,
        placements: [
          ...layout.placements,
          {
            panelId: "unknown.panel",
            dock: "right",
            order: 99,
            dimensions: { width: 100, height: 100 },
            visible: true,
          },
        ],
      }),
    ).toThrow(/UNKNOWN_PANEL/);
    expect(PANEL_REGISTRY.every((panel) => panel.noActuation)).toBe(true);
  });

  it("test_docking_engine_placement_is_deterministic", () => {
    const layout = defaultLayoutForWorkspace("monitor.operations");
    const first = computeDockArrangement(layout);
    const second = computeDockArrangement({ ...layout, placements: [...layout.placements].reverse() });
    expect(JSON.stringify(first)).toBe(JSON.stringify(second));
    expect(placementSignature(layout)).toBe(placementSignature(layout));
  });

  it("test_layout_manager_serialize_restore_roundtrip_no_persistence_backend", async () => {
    const layout = defaultLayoutForWorkspace("monitor.operations");
    const resized = resizePanel(layout, "shell.context.workspace", { width: 384, height: 220 });
    const restored = restoreLayout(serializeLayout(resized));
    expect(restored).toEqual(resized);
    const store = createSessionLayoutStore();
    store.clear();
    store.save(resized);
    expect(store.load("monitor.operations")).toEqual(resized);

    const modules = import.meta.glob("./**/*.{ts,tsx}", {
      query: "?raw",
      import: "default",
    });
    const productionLoaders = Object.entries(modules)
      .filter(([path]) => !path.includes(".test."))
      .map(([, loader]) => loader);
    const texts = await Promise.all(productionLoaders.map((loader) => loader()));
    const sourceText = texts.join("\n");
    expect(sourceText).not.toContain("/api/v1/");
    expect(sourceText).not.toContain("operator_workspace_preferences");
    expect(sourceText).not.toContain("fetch(");
  });

  it("test_panel_infrastructure_contains_no_execution_or_actuation", async () => {
    const modules = import.meta.glob("./**/*.{ts,tsx}", {
      query: "?raw",
      import: "default",
    });
    const productionLoaders = Object.entries(modules)
      .filter(([path]) => !path.includes(".test."))
      .map(([, loader]) => loader);
    const texts = await Promise.all(productionLoaders.map((loader) => loader()));
    const sourceText = texts.join("\n").toLowerCase();
    const forbidden = [
      "b" + "uy",
      "s" + "ell",
      "place_order",
      "submit order",
      "go live",
      "connect broker",
      "account_id",
      "order_ticket",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("renders registered panels with focusable docked panel containers", () => {
    const activeWorkspace = WORKSPACE_REGISTRY[0];
    const layout = defaultLayoutForWorkspace(activeWorkspace.id);
    render(
      <MemoryRouter>
        <ShellEventBusProvider>
          <PanelHost
            category="context"
            activeWorkspace={activeWorkspace}
            layout={layout}
            setLayout={() => undefined}
          />
        </ShellEventBusProvider>
      </MemoryRouter>,
    );
    expect(screen.getByLabelText("Workspace context")).toBeInTheDocument();
    expect(screen.getByLabelText("Governance context")).toBeInTheDocument();
    expect(screen.getAllByText("Widen panel").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Narrow panel").length).toBeGreaterThan(0);
  });
});
