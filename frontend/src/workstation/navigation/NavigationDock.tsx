import { useRef } from "react";
import { NavLink } from "react-router-dom";
import type { NavigationSection } from "./navigationGenerator";
import { WorkspaceIcon } from "./icons";

export type NavigationDockProps = {
  sections: NavigationSection[];
  collapsed: boolean;
  onToggleCollapsed: () => void;
};

export function NavigationDock({ sections, collapsed, onToggleCollapsed }: NavigationDockProps) {
  const linkRefs = useRef<Array<HTMLAnchorElement | null>>([]);

  function focusSibling(currentIndex: number, direction: 1 | -1) {
    const links = linkRefs.current.filter(Boolean) as HTMLAnchorElement[];
    const targetIndex = (currentIndex + direction + links.length) % links.length;
    links[targetIndex]?.focus();
  }

  let linkIndex = 0;
  return (
    <nav
      className={`ix-nav-dock${collapsed ? " collapsed" : ""}`}
      aria-label="Institutional workflow navigation"
      tabIndex={-1}
      data-region="B"
      data-navigation-source="workspace-registry"
    >
      <button
        type="button"
        className="ix-shell-button ix-nav-toggle"
        onClick={onToggleCollapsed}
        aria-pressed={collapsed}
      >
        {collapsed ? "Expand navigation" : "Collapse navigation"}
      </button>
      {sections.map((section) => (
        <section className="ix-nav-group" key={section.category} aria-label={`${section.category} workspaces`}>
          <h2 className="ix-nav-group-title">{section.category}</h2>
          {section.workspaces.map((workspace) => {
            const currentLinkIndex = linkIndex;
            linkIndex += 1;
            return (
              <NavLink
                key={workspace.id}
                to={workspace.route}
                end={workspace.route === "/"}
                ref={(element) => {
                  linkRefs.current[currentLinkIndex] = element;
                }}
                title={workspace.displayName}
                data-workspace-id={workspace.id}
                data-telemetry-id={workspace.telemetryId}
                className={({ isActive }) => `ix-nav-link${isActive ? " active" : ""}`}
                onKeyDown={(event) => {
                  if (event.key === "ArrowDown") {
                    event.preventDefault();
                    focusSibling(currentLinkIndex, 1);
                  }
                  if (event.key === "ArrowUp") {
                    event.preventDefault();
                    focusSibling(currentLinkIndex, -1);
                  }
                }}
              >
                <span className="ix-nav-icon" aria-hidden>
                  <WorkspaceIcon icon={workspace.icon} />
                </span>
                <span className="ix-nav-copy">
                  <span>{workspace.displayName}</span>
                  <small>{workspace.description}</small>
                </span>
                <span className="ix-nav-indicator" aria-hidden>
                  •
                </span>
              </NavLink>
            );
          })}
        </section>
      ))}
    </nav>
  );
}
