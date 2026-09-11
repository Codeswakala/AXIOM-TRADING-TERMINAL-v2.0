import { PANEL_REGISTRY, type PanelDimensions } from "./panelRegistry";
import type { LayoutDescriptor, PanelPlacement } from "./dockingEngine";

export type LayoutStore = {
  load: (workspaceId: string) => LayoutDescriptor | null;
  save: (layout: LayoutDescriptor) => void;
  clear: () => void;
};

const STORE_PREFIX = "axiom.ui001.p03.layout";

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

export function defaultLayoutForWorkspace(workspaceId: string): LayoutDescriptor {
  const placements: PanelPlacement[] = PANEL_REGISTRY.map((panel, index) => ({
    panelId: panel.id,
    dock: panel.panelCategory === "activity" ? "bottom" : "right",
    order: index,
    dimensions: panel.defaultDimensions,
    visible: true,
  }));
  return { layoutId: `session.${workspaceId}`, workspaceId, placements };
}

export function serializeLayout(layout: LayoutDescriptor): string {
  return JSON.stringify(layout);
}

export function restoreLayout(serialized: string): LayoutDescriptor {
  const parsed = JSON.parse(serialized) as LayoutDescriptor;
  validateLayout(parsed);
  return parsed;
}

export function validateLayout(layout: LayoutDescriptor): boolean {
  const registered = new Set(PANEL_REGISTRY.map((panel) => panel.id));
  for (const placement of layout.placements) {
    if (!registered.has(placement.panelId)) {
      throw new Error(`UNKNOWN_PANEL:${placement.panelId}`);
    }
  }
  return true;
}

export function resizePanel(
  layout: LayoutDescriptor,
  panelId: string,
  dimensions: Partial<PanelDimensions>,
): LayoutDescriptor {
  const registration = PANEL_REGISTRY.find((panel) => panel.id === panelId);
  if (!registration) throw new Error(`UNKNOWN_PANEL:${panelId}`);
  return {
    ...layout,
    placements: layout.placements.map((placement) => {
      if (placement.panelId !== panelId) return placement;
      return {
        ...placement,
        dimensions: {
          width: clamp(
            dimensions.width ?? placement.dimensions.width,
            registration.minimumDimensions.width,
            registration.maximumDimensions.width,
          ),
          height: clamp(
            dimensions.height ?? placement.dimensions.height,
            registration.minimumDimensions.height,
            registration.maximumDimensions.height,
          ),
        },
      };
    }),
  };
}

export function createSessionLayoutStore(): LayoutStore {
  return {
    load(workspaceId: string) {
      const raw = window.sessionStorage.getItem(`${STORE_PREFIX}.${workspaceId}`);
      return raw ? restoreLayout(raw) : null;
    },
    save(layout: LayoutDescriptor) {
      window.sessionStorage.setItem(`${STORE_PREFIX}.${layout.workspaceId}`, serializeLayout(layout));
    },
    clear() {
      for (const key of Object.keys(window.sessionStorage)) {
        if (key.startsWith(STORE_PREFIX)) window.sessionStorage.removeItem(key);
      }
    },
  };
}
