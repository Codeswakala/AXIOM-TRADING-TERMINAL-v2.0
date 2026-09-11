/**
 * AXIOM Atomic Component — Accordion (UI-009-P02)
 *
 * Scoped, accessible collapsible accordion component.
 * Keyboard: Enter / Space triggers expansion.
 * ARIA: aria-expanded, aria-controls, aria-labelledby.
 * Animation: var(--ix-motion-fast) with prefers-reduced-motion override.
 */

import { useState, type ReactNode } from "react";
import "./Accordion.css";

export interface AccordionItem {
  id: string;
  title: string;
  content: ReactNode;
  defaultExpanded?: boolean;
}

export interface AccordionProps {
  items: AccordionItem[];
  allowMultiple?: boolean;
  className?: string;
}

export function Accordion({
  items,
  allowMultiple = false,
  className = "",
}: AccordionProps) {
  const [expandedIds, setExpandedIds] = useState<Set<string>>(() => {
    const set = new Set<string>();
    for (const item of items) {
      if (item.defaultExpanded) {
        set.add(item.id);
      }
    }
    return set;
  });

  function toggleItem(id: string) {
    setExpandedIds((prev) => {
      const next = new Set(allowMultiple ? prev : []);
      if (prev.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }

  return (
    <div className={`ix-accordion ${className}`} data-ui009-component="accordion">
      {items.map((item) => {
        const isExpanded = expandedIds.has(item.id);
        const headerId = `ix-accordion-header-${item.id}`;
        const panelId = `ix-accordion-panel-${item.id}`;

        return (
          <div
            key={item.id}
            className={`ix-accordion-item ${isExpanded ? "ix-accordion-item--expanded" : ""}`}
            data-testid={`accordion-item-${item.id}`}
          >
            <h3 className="ix-accordion-heading">
              <button
                type="button"
                id={headerId}
                className="ix-accordion-trigger"
                aria-expanded={isExpanded}
                aria-controls={panelId}
                onClick={() => toggleItem(item.id)}
                data-testid={`accordion-trigger-${item.id}`}
              >
                <span className="ix-accordion-title">{item.title}</span>
                <span className="ix-accordion-icon" aria-hidden="true">
                  {isExpanded ? "\u{25B4}" : "\u{25BE}"}
                </span>
              </button>
            </h3>

            {isExpanded && (
              <div
                id={panelId}
                role="region"
                aria-labelledby={headerId}
                className="ix-accordion-panel"
                data-testid={`accordion-panel-${item.id}`}
              >
                <div className="ix-accordion-content">{item.content}</div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
