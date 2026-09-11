import type { DockPosition, PanelDimensions } from "./panelRegistry";

export type PanelPlacement = {
  panelId: string;
  dock: DockPosition;
  order: number;
  dimensions: PanelDimensions;
  visible: boolean;
};

export type LayoutDescriptor = {
  layoutId: string;
  workspaceId: string;
  placements: PanelPlacement[];
};

export type DockArrangement = Record<DockPosition, PanelPlacement[]>;

const DOCKS: DockPosition[] = ["left", "right", "top", "bottom", "center"];

export function computeDockArrangement(descriptor: LayoutDescriptor): DockArrangement {
  const arrangement: DockArrangement = {
    left: [],
    right: [],
    top: [],
    bottom: [],
    center: [],
  };
  for (const placement of descriptor.placements.filter((item) => item.visible)) {
    arrangement[placement.dock].push({ ...placement });
  }
  for (const dock of DOCKS) {
    arrangement[dock] = arrangement[dock].sort((left, right) =>
      left.order === right.order ? left.panelId.localeCompare(right.panelId) : left.order - right.order,
    );
  }
  return arrangement;
}

export function movePanel(
  descriptor: LayoutDescriptor,
  panelId: string,
  dock: DockPosition,
  order: number,
): LayoutDescriptor {
  return {
    ...descriptor,
    placements: descriptor.placements.map((placement) =>
      placement.panelId === panelId ? { ...placement, dock, order } : placement,
    ),
  };
}

export function placementSignature(descriptor: LayoutDescriptor): string {
  return JSON.stringify(computeDockArrangement(descriptor));
}
