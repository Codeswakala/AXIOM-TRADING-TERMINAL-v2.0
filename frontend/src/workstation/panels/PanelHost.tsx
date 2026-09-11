import type { WorkspaceDefinition } from "../registry/workspaceRegistry";
import { useShellEventBus } from "../events/shellEventBus";
import { defaultLayoutForWorkspace, resizePanel, type LayoutStore } from "./layoutManager";
import { panelsForCategory, type PanelCategory } from "./panelRegistry";
import type { LayoutDescriptor } from "./dockingEngine";

export type PanelHostProps = {
  category: PanelCategory;
  activeWorkspace: WorkspaceDefinition;
  layout: LayoutDescriptor;
  setLayout: (layout: LayoutDescriptor) => void;
  store?: LayoutStore;
};

export function PanelHost({ category, activeWorkspace, layout, setLayout, store }: PanelHostProps) {
  const bus = useShellEventBus();
  const panels = panelsForCategory(category);
  const defaultLayout = defaultLayoutForWorkspace(activeWorkspace.id);
  const missingPlacements = defaultLayout.placements.filter(
    (placement) => !layout.placements.some((existing) => existing.panelId === placement.panelId),
  );
  const effectiveLayout: LayoutDescriptor =
    missingPlacements.length > 0
      ? { ...layout, placements: [...layout.placements, ...missingPlacements] }
      : layout;

  function updateLayout(next: LayoutDescriptor) {
    setLayout(next);
    store?.save(next);
  }

  return (
    <div className="ix-panel-stack" data-panel-category={category}>
      {panels.map((panel) => {
        const placement = effectiveLayout.placements.find((item) => item.panelId === panel.id);
        if (!placement?.visible) return null;
        const PanelComponent = panel.Component;
        return (
          <section
            className="ix-docked-panel"
            key={panel.id}
            tabIndex={0}
            aria-label={panel.displayName}
            data-panel-id={panel.id}
            data-dock={placement.dock}
            onFocus={() =>
              bus.publish({
                type: "panel.focused",
                source: panel.id,
                payload: { telemetryId: panel.telemetryId },
              })
            }
          >
            <header className="ix-docked-panel-header">
              <h2 className="ix-panel-title">{panel.displayName}</h2>
              {panel.resizable ? (
                <div className="ix-panel-controls" aria-label={`${panel.displayName} panel controls`}>
                  <button
                    type="button"
                    className="ix-shell-button"
                    onClick={() => {
                      const next = resizePanel(effectiveLayout, panel.id, {
                        width: placement.dimensions.width + 32,
                        height: placement.dimensions.height + 24,
                      });
                      updateLayout(next);
                      bus.publish({ type: "panel.resized", source: panel.id });
                    }}
                  >
                    Widen panel
                  </button>
                  <button
                    type="button"
                    className="ix-shell-button"
                    onClick={() => {
                      const next = resizePanel(effectiveLayout, panel.id, {
                        width: placement.dimensions.width - 32,
                        height: placement.dimensions.height - 24,
                      });
                      updateLayout(next);
                      bus.publish({ type: "panel.resized", source: panel.id });
                    }}
                  >
                    Narrow panel
                  </button>
                </div>
              ) : null}
            </header>
            <PanelComponent activeWorkspace={activeWorkspace} />
          </section>
        );
      })}
    </div>
  );
}
