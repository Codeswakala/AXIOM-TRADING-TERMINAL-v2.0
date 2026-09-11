import { useEffect, useMemo, useRef, useState } from "react";
import { commandMatches } from "../commands/commandRegistry";
import type { RegisteredCommand } from "../commands/commandTypes";
import { useOverlayController } from "./OverlayProvider";

export type CommandPaletteProps = {
  commands: readonly RegisteredCommand[];
};

export function CommandPalette({ commands }: CommandPaletteProps) {
  const overlay = useOverlayController();
  const inputRef = useRef<HTMLInputElement>(null);
  const triggerReturnRef = useRef<HTMLElement | null>(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    if (overlay.commandOpen) {
      triggerReturnRef.current = document.activeElement as HTMLElement | null;
      window.setTimeout(() => inputRef.current?.focus(), 0);
    }
  }, [overlay.commandOpen]);

  function close() {
    overlay.closeCommandPalette();
    triggerReturnRef.current?.focus();
  }

  const items = useMemo(
    () => commands.filter((command) => commandMatches(command, query)),
    [commands, query],
  );

  const groupedItems = useMemo(() => {
    const groups = new Map<string, RegisteredCommand[]>();
    for (const item of items) {
      const current = groups.get(item.group) ?? [];
      current.push(item);
      groups.set(item.group, current);
    }
    return [...groups.entries()];
  }, [items]);

  if (!overlay.commandOpen) return null;

  return (
    <div
      className="ix-command-palette"
      role="dialog"
      aria-modal="true"
      aria-label="Command palette"
      data-ui002-component="command-palette-registry"
      onKeyDown={(event) => {
        if (event.key === "Escape") {
          event.preventDefault();
          close();
        }
      }}
    >
      <input
        ref={inputRef}
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        aria-label="Search workspaces and shell commands"
        placeholder="Open workspace or shell command…"
        data-testid="command-palette-input"
      />
      <div className="ix-command-list" role="menu" aria-label="Workspace and shell commands">
        {groupedItems.length === 0 ? (
          <p className="ix-command-empty" data-testid="command-palette-empty" role="status">
            No matching workspace or action.
          </p>
        ) : null}
        {groupedItems.map(([group, groupItems]) => (
          <section className="ix-command-group" key={group} aria-label={`${group} commands`}>
            <h2 className="ix-nav-group-title">{group}</h2>
            {groupItems.map((item, index) => (
              <button
                type="button"
                role="menuitem"
                className={`ix-command-item${index === 0 ? " active" : ""}`}
                key={item.id}
                aria-disabled={!item.enabled}
                data-command-id={item.id}
                data-command-type={item.commandType}
                data-command-source={item.source}
                onClick={() => {
                  if (!item.enabled) return;
                  item.onSelect();
                  close();
                }}
              >
                <span>{item.label}</span>
                <span className="ix-metadata">
                  {item.commandType === "navigation" ? "Navigate" : "UI toggle"}
                  {!item.enabled ? " · Deferred" : ""}
                </span>
              </button>
            ))}
          </section>
        ))}
      </div>
    </div>
  );
}
