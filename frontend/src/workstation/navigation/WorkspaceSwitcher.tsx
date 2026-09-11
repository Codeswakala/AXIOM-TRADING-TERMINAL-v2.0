import { useEffect, useMemo, useRef, useState } from "react";
import type { NavigationSection } from "./navigationGenerator";
import { visibleRecentWorkspaceIds } from "./workspaceHistory";

export type WorkspaceSwitcherProps = {
  sections: NavigationSection[];
  activeWorkspaceId: string;
  recentWorkspaceIds: readonly string[];
  onNavigate: (route: string, workspaceId: string) => void;
};

type SwitcherItem = {
  workspaceId: string;
  route: string;
  label: string;
  stage: string;
};

export function WorkspaceSwitcher({
  sections,
  activeWorkspaceId,
  recentWorkspaceIds,
  onNavigate,
}: WorkspaceSwitcherProps) {
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const itemRefs = useRef<Array<HTMLButtonElement | null>>([]);
  const visibleItems = useMemo<SwitcherItem[]>(
    () =>
      sections.flatMap((section) =>
        section.workspaces.map((workspace) => ({
          workspaceId: workspace.id,
          route: workspace.route,
          label: workspace.displayName,
          stage: section.category,
        })),
      ),
    [sections],
  );
  const visibleIds = useMemo(
    () => new Set(visibleItems.map((item) => item.workspaceId)),
    [visibleItems],
  );
  const recentItems = visibleRecentWorkspaceIds(recentWorkspaceIds, visibleIds)
    .map((workspaceId) => visibleItems.find((item) => item.workspaceId === workspaceId))
    .filter((item): item is SwitcherItem => Boolean(item));

  useEffect(() => {
    if (open) window.setTimeout(() => itemRefs.current[0]?.focus(), 0);
  }, [open]);

  function closeAndRestoreFocus() {
    setOpen(false);
    window.setTimeout(() => triggerRef.current?.focus(), 0);
  }

  function focusItem(currentIndex: number, direction: 1 | -1) {
    const items = itemRefs.current.filter(Boolean) as HTMLButtonElement[];
    if (items.length === 0) return;
    const targetIndex = (currentIndex + direction + items.length) % items.length;
    items[targetIndex]?.focus();
  }

  function selectItem(item: SwitcherItem) {
    onNavigate(item.route, item.workspaceId);
    closeAndRestoreFocus();
  }

  let itemIndex = 0;

  return (
    <div className="ix-workspace-switcher" data-ui002-component="workspace-switcher" data-region="A">
      <button
        type="button"
        ref={triggerRef}
        className="ix-shell-button"
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen((current) => !current)}
        onKeyDown={(event) => {
          if (event.key === "ArrowDown" || event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            setOpen(true);
          }
        }}
      >
        Workspace switcher
      </button>
      {open ? (
        <div
          className="ix-workspace-switcher-menu"
          role="menu"
          aria-label="Workspace switcher"
          onKeyDown={(event) => {
            if (event.key === "Escape") {
              event.preventDefault();
              closeAndRestoreFocus();
            }
          }}
        >
          {recentItems.length > 0 ? (
            <section aria-label="Recent workspaces" className="ix-switcher-section">
              <h2 className="ix-nav-group-title">Recent workspaces</h2>
              {recentItems.map((item) => {
                const currentIndex = itemIndex;
                itemIndex += 1;
                return renderItem(item, currentIndex);
              })}
            </section>
          ) : null}
          {sections.map((section) => (
            <section
              aria-label={`${section.category} switcher workspaces`}
              className="ix-switcher-section"
              key={section.category}
            >
              <h2 className="ix-nav-group-title">{section.category}</h2>
              {section.workspaces.map((workspace) => {
                const currentIndex = itemIndex;
                itemIndex += 1;
                return renderItem(
                  {
                    workspaceId: workspace.id,
                    route: workspace.route,
                    label: workspace.displayName,
                    stage: section.category,
                  },
                  currentIndex,
                );
              })}
            </section>
          ))}
        </div>
      ) : null}
    </div>
  );

  function renderItem(item: SwitcherItem, currentIndex: number) {
    return (
      <button
        type="button"
        role="menuitem"
        className="ix-switcher-item"
        key={`${item.workspaceId}.${currentIndex}`}
        aria-current={item.workspaceId === activeWorkspaceId ? "page" : undefined}
        data-workspace-id={item.workspaceId}
        ref={(element) => {
          itemRefs.current[currentIndex] = element;
        }}
        onClick={() => selectItem(item)}
        onKeyDown={(event) => {
          if (event.key === "ArrowDown") {
            event.preventDefault();
            focusItem(currentIndex, 1);
          }
          if (event.key === "ArrowUp") {
            event.preventDefault();
            focusItem(currentIndex, -1);
          }
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            selectItem(item);
          }
        }}
      >
        <span>{item.label}</span>
        <small>{item.stage} · Navigate</small>
      </button>
    );
  }
}
