/**
 * AXIOM Institutional UI Component — DataTable (UI-009-P04)
 *
 * Reusable institutional data table primitive supporting:
 * - Generic row typing
 * - Monospace tabular-nums alignment for numeric data
 * - Sortable column headers with ARIA states
 * - Loading skeleton states with aria-busy
 * - Honest empty states with role="status"
 * - Optional integrated pagination
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { type ReactNode } from "react";
import { SortableHeader, type SortDirection } from "./SortableHeader";
import { Pagination, type PaginationProps } from "./Pagination";
import "./DataTable.css";

export type ColumnAlign = "left" | "center" | "right" | "numeric";

export interface ColumnDef<T> {
  key: string | keyof T;
  header: ReactNode | string;
  sortable?: boolean;
  align?: ColumnAlign;
  width?: string;
  render?: (value: any, row: T, index: number) => ReactNode;
  className?: string;
}

export interface DataTableProps<T> {
  columns: ColumnDef<T>[];
  rows: T[];
  sortKey?: string | keyof T;
  sortDirection?: SortDirection;
  onSort?: (key: any, direction: SortDirection) => void;
  loading?: boolean;
  skeletonRowCount?: number;
  emptyText?: string;
  emptyIcon?: ReactNode;
  pagination?: PaginationProps;
  rowKey?: (row: T, index: number) => string | number;
  onRowClick?: (row: T) => void;
  caption?: string;
  ariaLabel?: string;
  ariaLabelledBy?: string;
  className?: string;
  id?: string;
}

export function DataTable<T extends Record<string, any>>({
  columns,
  rows,
  sortKey,
  sortDirection,
  onSort,
  loading = false,
  skeletonRowCount = 5,
  emptyText = "No data available",
  emptyIcon,
  pagination,
  rowKey,
  onRowClick,
  caption,
  ariaLabel,
  ariaLabelledBy,
  className = "",
  id,
}: DataTableProps<T>) {
  const getRowKey = (row: T, index: number): string | number => {
    if (rowKey) return rowKey(row, index);
    if (row && typeof row === "object" && "id" in row && row.id != null) {
      return String(row.id);
    }
    return index;
  };

  const isInteractive = Boolean(onRowClick);

  return (
    <div
      id={id}
      className={`ix-data-table-container ${className}`}
      data-ui009-component="data-table"
      data-loading={loading}
      data-empty={!loading && rows.length === 0}
    >
      <div className="ix-data-table-wrapper">
        <table
          className="ix-data-table"
          aria-label={ariaLabel}
          aria-labelledby={ariaLabelledBy}
          aria-busy={loading}
        >
          {caption && <caption className="ix-data-table__caption">{caption}</caption>}

          <thead className="ix-data-table__head">
            <tr>
              {columns.map((col) => {
                const colKeyStr = String(col.key);
                const isSorted = sortKey === col.key || sortKey === colKeyStr;
                const alignClass = `ix-data-table__th--${col.align || "left"}`;
                const ariaSortVal = col.sortable
                  ? isSorted
                    ? sortDirection === "asc"
                      ? "ascending"
                      : "descending"
                    : "none"
                  : undefined;

                return (
                  <th
                    key={colKeyStr}
                    scope="col"
                    aria-sort={ariaSortVal}
                    className={`ix-data-table__th ${alignClass} ${col.className || ""}`}
                    style={col.width ? { width: col.width } : undefined}
                    data-testid={`column-header-${colKeyStr}`}
                  >
                    {col.sortable && onSort ? (
                      <SortableHeader
                        columnKey={colKeyStr}
                        header={col.header}
                        sorted={isSorted}
                        sortDirection={sortDirection}
                        onSort={(k, dir) => onSort(k, dir)}
                        align={col.align}
                      />
                    ) : (
                      <span className="ix-data-table__header-text">{col.header}</span>
                    )}
                  </th>
                );
              })}
            </tr>
          </thead>

          <tbody className="ix-data-table__body">
            {loading ? (
              Array.from({ length: skeletonRowCount }).map((_, idx) => (
                <tr key={`skeleton-${idx}`} className="ix-data-table__skeleton-row" data-testid="table-skeleton-row">
                  {columns.map((col) => (
                    <td
                      key={`skeleton-cell-${String(col.key)}`}
                      className={`ix-data-table__cell ix-data-table__cell--${col.align || "left"}`}
                    >
                      <span className="ix-data-table__skeleton-bar" aria-hidden="true" />
                    </td>
                  ))}
                </tr>
              ))
            ) : rows.length === 0 ? (
              <tr className="ix-data-table__empty-row" data-testid="table-empty-row">
                <td colSpan={columns.length} className="ix-data-table__empty-cell">
                  <div className="ix-data-table__empty-state" role="status" data-testid="table-empty-state">
                    {emptyIcon && <span className="ix-data-table__empty-icon">{emptyIcon}</span>}
                    <span className="ix-data-table__empty-text">{emptyText}</span>
                  </div>
                </td>
              </tr>
            ) : (
              rows.map((row, rowIndex) => {
                const key = getRowKey(row, rowIndex);
                return (
                  <tr
                    key={key}
                    className={`ix-data-table__row ${isInteractive ? "ix-data-table__row--clickable" : ""}`}
                    onClick={onRowClick ? () => onRowClick(row) : undefined}
                    tabIndex={isInteractive ? 0 : undefined}
                    data-testid={`table-row-${key}`}
                  >
                    {columns.map((col) => {
                      const colKeyStr = String(col.key);
                      const rawValue = row[col.key];
                      const renderedValue = col.render
                        ? col.render(rawValue, row, rowIndex)
                        : rawValue != null
                          ? String(rawValue)
                          : "—";

                      const alignClass = `ix-data-table__cell--${col.align || "left"}`;

                      return (
                        <td
                          key={`${key}-${colKeyStr}`}
                          className={`ix-data-table__cell ${alignClass} ${col.className || ""}`}
                          data-column-key={colKeyStr}
                        >
                          {renderedValue}
                        </td>
                      );
                    })}
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {pagination && <Pagination {...pagination} />}
    </div>
  );
}
