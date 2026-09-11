/**
 * AXIOM Institutional UI Component — Pagination (UI-009-P04)
 *
 * Accessible pagination controls for data tables and list views.
 * Supports first/prev/next/last navigation, page size selector, and bounds protection.
 *
 * Invariant: Pure token consumption via var(--ix-*); zero ad-hoc hex.
 */

import { forwardRef, type HTMLAttributes, type ChangeEvent } from "react";
import "./Pagination.css";

export interface PaginationProps extends Omit<HTMLAttributes<HTMLElement>, "onChange"> {
  page: number;
  pageSize: number;
  totalRows: number;
  onPageChange: (page: number) => void;
  onPageSizeChange?: (pageSize: number) => void;
  pageSizeOptions?: number[];
  className?: string;
}

export const Pagination = forwardRef<HTMLElement, PaginationProps>(
  (
    {
      page,
      pageSize,
      totalRows,
      onPageChange,
      onPageSizeChange,
      pageSizeOptions = [10, 25, 50, 100],
      className = "",
      ...rest
    },
    ref,
  ) => {
    const totalPages = Math.max(1, Math.ceil(totalRows / Math.max(1, pageSize)));
    const currentPage = Math.min(Math.max(1, page), totalPages);

    const isFirstDisabled = currentPage <= 1 || totalRows === 0;
    const isPrevDisabled = currentPage <= 1 || totalRows === 0;
    const isNextDisabled = currentPage >= totalPages || totalRows === 0;
    const isLastDisabled = currentPage >= totalPages || totalRows === 0;

    const handlePageChange = (targetPage: number) => {
      const validPage = Math.min(Math.max(1, targetPage), totalPages);
      if (validPage !== currentPage && totalRows > 0) {
        onPageChange(validPage);
      }
    };

    const handlePageSizeChange = (e: ChangeEvent<HTMLSelectElement>) => {
      const newSize = parseInt(e.target.value, 10);
      if (!isNaN(newSize) && newSize > 0) {
        onPageSizeChange?.(newSize);
      }
    };

    const startRow = totalRows === 0 ? 0 : (currentPage - 1) * pageSize + 1;
    const endRow = totalRows === 0 ? 0 : Math.min(currentPage * pageSize, totalRows);

    return (
      <nav
        ref={ref}
        role="navigation"
        aria-label="Pagination Navigation"
        className={`ix-pagination ${className}`}
        data-ui009-component="pagination"
        data-page={currentPage}
        data-total-pages={totalPages}
        data-total-rows={totalRows}
        {...rest}
      >
        <div className="ix-pagination__info" data-testid="pagination-info">
          <span className="ix-pagination__range">
            Showing <strong className="ix-pagination__mono">{startRow}–{endRow}</strong> of <strong className="ix-pagination__mono">{totalRows}</strong>
          </span>
          <span className="ix-pagination__page-indicator" aria-current="page">
            Page <strong className="ix-pagination__mono">{currentPage}</strong> of <strong className="ix-pagination__mono">{totalPages}</strong>
          </span>
        </div>

        <div className="ix-pagination__controls">
          {onPageSizeChange && (
            <div className="ix-pagination__page-size">
              <label htmlFor="ix-pagination-size-select" className="ix-pagination__size-label">
                Rows per page:
              </label>
              <select
                id="ix-pagination-size-select"
                className="ix-pagination__size-select"
                value={pageSize}
                onChange={handlePageSizeChange}
                aria-label="Select rows per page"
                data-testid="pagination-page-size-select"
              >
                {pageSizeOptions.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="ix-pagination__buttons">
            <button
              type="button"
              className="ix-pagination__btn ix-pagination__btn--first"
              disabled={isFirstDisabled}
              onClick={() => handlePageChange(1)}
              aria-label="Go to first page"
              data-testid="pagination-first"
            >
              {"« First"}
            </button>

            <button
              type="button"
              className="ix-pagination__btn ix-pagination__btn--prev"
              disabled={isPrevDisabled}
              onClick={() => handlePageChange(currentPage - 1)}
              aria-label="Go to previous page"
              data-testid="pagination-prev"
            >
              {"‹ Prev"}
            </button>

            <span className="ix-pagination__current-badge" aria-hidden="true">
              {currentPage}
            </span>

            <button
              type="button"
              className="ix-pagination__btn ix-pagination__btn--next"
              disabled={isNextDisabled}
              onClick={() => handlePageChange(currentPage + 1)}
              aria-label="Go to next page"
              data-testid="pagination-next"
            >
              {"Next ›"}
            </button>

            <button
              type="button"
              className="ix-pagination__btn ix-pagination__btn--last"
              disabled={isLastDisabled}
              onClick={() => handlePageChange(totalPages)}
              aria-label="Go to last page"
              data-testid="pagination-last"
            >
              {"Last »"}
            </button>
          </div>
        </div>
      </nav>
    );
  },
);

Pagination.displayName = "Pagination";
