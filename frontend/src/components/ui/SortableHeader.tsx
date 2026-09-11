/**
 * AXIOM Institutional UI Component — SortableHeader (UI-009-P04)
 *
 * Accessible sortable table header control.
 * Supports keyboard navigation (Enter/Space), ARIA sort state, and directional indicator.
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type ButtonHTMLAttributes, type KeyboardEvent, type ReactNode } from "react";
import "./SortableHeader.css";

export type SortDirection = "asc" | "desc";

export interface SortableHeaderProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onSort"> {
  columnKey: string;
  header: ReactNode;
  sorted: boolean;
  sortDirection?: SortDirection;
  onSort: (key: string, direction: SortDirection) => void;
  align?: "left" | "center" | "right" | "numeric";
  className?: string;
}

export const SortableHeader = forwardRef<HTMLButtonElement, SortableHeaderProps>(
  (
    {
      columnKey,
      header,
      sorted,
      sortDirection = "asc",
      onSort,
      align = "left",
      className = "",
      ...rest
    },
    ref,
  ) => {
    const nextDirection: SortDirection = sorted && sortDirection === "asc" ? "desc" : "asc";

    const handleToggle = () => {
      onSort(columnKey, nextDirection);
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLButtonElement>) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        handleToggle();
      }
    };

    const headerText = typeof header === "string" ? header : columnKey;
    const sortAriaState = sorted ? (sortDirection === "asc" ? "ascending" : "descending") : "none";
    const ariaLabel = `${headerText}, sortable column, currently ${sortAriaState}. Click or press Enter to sort ${nextDirection === "asc" ? "ascending" : "descending"}.`;

    const iconSymbol = sorted
      ? sortDirection === "asc"
        ? "\u{2191}" // ↑
        : "\u{2193}" // ↓
      : "\u{2195}"; // ↕

    return (
      <button
        ref={ref}
        type="button"
        className={`ix-sortable-header ix-sortable-header--align-${align} ${
          sorted ? "ix-sortable-header--active" : ""
        } ${className}`}
        aria-label={ariaLabel}
        data-ui009-component="sortable-header"
        data-column-key={columnKey}
        data-sorted={sorted}
        data-direction={sorted ? sortDirection : "none"}
        onClick={handleToggle}
        onKeyDown={handleKeyDown}
        {...rest}
      >
        <span className="ix-sortable-header__text">{header}</span>
        <span
          className={`ix-sortable-header__icon ${sorted ? "ix-sortable-header__icon--active" : ""}`}
          aria-hidden="true"
          data-testid="sort-indicator"
        >
          {iconSymbol}
        </span>
      </button>
    );
  },
);

SortableHeader.displayName = "SortableHeader";
