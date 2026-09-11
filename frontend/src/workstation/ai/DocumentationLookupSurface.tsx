/**
 * DocumentationLookupSurface Component (UI-008-P05)
 *
 * In-app searchable platform architecture, statistical definitions,
 * indicator formulas, and governance rules lookup surface.
 *
 * Invariants:
 * - 100% static, client-side, sandboxed documentation search.
 * - Safe Markdown rendering with zero raw script execution.
 * - Zero order/trade execution controls (Read-only guidance only).
 * - Mandatory "RESEARCH-ONLY · NON-ACTUATING" disclaimer.
 */

import { useState, useMemo, useEffect, type KeyboardEvent } from "react";
import {
  PLATFORM_DOCUMENTATION_INDEX,
  searchDocumentation,
} from "./documentationIndex";

export const DOC_LOOKUP_DISCLAIMER =
  "Platform documentation and knowledge lookup for research only. Not financial advice, not an instruction. Operator judgment required. AXIOM does not act.";

export interface DocumentationLookupSurfaceProps {
  onClose?: () => void;
  initialQuery?: string;
  initialDocId?: string;
}

/**
 * Sandboxed text/markdown renderer that safely renders headings, bold, bullet points,
 * and code snippets without dangerously-SetInner-HTML script execution risks.
 */
export function SandboxedMarkdownViewer({ content }: { content: string }) {
  const lines = content.split("\n");

  return (
    <div className="ix-sandboxed-markdown" data-testid="sandboxed-markdown-viewer">
      {lines.map((line, idx) => {
        const trimmed = line.trim();

        if (trimmed.startsWith("### ")) {
          return (
            <h3 key={idx} className="ix-md-h3">
              {trimmed.replace("### ", "")}
            </h3>
          );
        }
        if (trimmed.startsWith("## ")) {
          return (
            <h2 key={idx} className="ix-md-h2">
              {trimmed.replace("## ", "")}
            </h2>
          );
        }
        if (trimmed.startsWith("- ")) {
          return (
            <li key={idx} className="ix-md-li">
              {trimmed.replace("- ", "")}
            </li>
          );
        }
        if (trimmed.startsWith("$$") && trimmed.endsWith("$$")) {
          return (
            <div key={idx} className="ix-md-math mono" data-testid="math-block">
              {trimmed.replace(/\$\$/g, "")}
            </div>
          );
        }
        if (!trimmed) {
          return <div key={idx} className="ix-md-spacer" />;
        }
        return (
          <p key={idx} className="ix-md-p">
            {trimmed}
          </p>
        );
      })}
    </div>
  );
}

export function DocumentationLookupSurface({
  onClose,
  initialQuery = "",
  initialDocId,
}: DocumentationLookupSurfaceProps) {
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedDocId, setSelectedDocId] = useState<string>(
    initialDocId ?? PLATFORM_DOCUMENTATION_INDEX[0].id,
  );

  const searchResults = useMemo(() => {
    const results = searchDocumentation(searchQuery);
    if (selectedCategory === "all") return results;
    return results.filter((doc) => doc.category === selectedCategory);
  }, [searchQuery, selectedCategory]);

  const activeDoc = useMemo(
    () =>
      searchResults.find((d) => d.id === selectedDocId) ??
      searchResults[0] ??
      PLATFORM_DOCUMENTATION_INDEX[0],
    [searchResults, selectedDocId],
  );

  useEffect(() => {
    if (searchResults.length > 0 && !searchResults.some((d) => d.id === selectedDocId)) {
      setSelectedDocId(searchResults[0].id);
    }
  }, [searchResults, selectedDocId]);

  function handleKeyDown(event: KeyboardEvent<HTMLElement>) {
    if (event.key === "Escape" && onClose) {
      event.preventDefault();
      onClose();
    }
  }

  const categories = [
    { id: "all", label: "All Topics" },
    { id: "governance", label: "Governance" },
    { id: "architecture", label: "Architecture" },
    { id: "statistics", label: "Statistics & Math" },
    { id: "indicators", label: "Indicators" },
  ];

  return (
    <section
      className="ix-documentation-lookup-surface"
      data-testid="documentation-lookup-surface"
      data-ui008-component="documentation-lookup"
      role="region"
      aria-label="Platform Documentation & Knowledge Lookup"
      onKeyDown={handleKeyDown}
      tabIndex={-1}
    >
      <header className="ix-doc-lookup-header">
        <div className="ix-doc-lookup-title-block">
          <span className="ix-doc-icon" aria-hidden="true">{"\u{1F4DA}"}</span>
          <h2 className="ix-doc-lookup-title">AXIOM Documentation & Knowledge Lookup</h2>
        </div>
        {onClose && (
          <button
            type="button"
            className="ix-doc-close-btn"
            onClick={onClose}
            aria-label="Close documentation lookup"
            data-testid="doc-close-button"
          >
            {"\u{2715}"} Close (Esc)
          </button>
        )}
      </header>

      <p
        className="ix-doc-disclaimer"
        data-ui008-disclaimer="doc-lookup-r5-6"
        data-testid="doc-disclaimer"
      >
        {DOC_LOOKUP_DISCLAIMER}
      </p>

      {/* Search Input & Category Filters */}
      <div className="ix-doc-search-bar" role="search" aria-label="Documentation search">
        <div className="ix-search-input-wrapper">
          <span className="ix-search-icon" aria-hidden="true">{"\u{1F50D}"}</span>
          <input
            type="text"
            className="ix-doc-search-input"
            placeholder="Search governance rules, architecture, formulas, indicators... (e.g. Wilson Score, Zero Trust)"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            aria-label="Search documentation"
            data-testid="doc-search-input"
            autoFocus
          />
          {searchQuery && (
            <button
              type="button"
              className="ix-clear-search-btn"
              onClick={() => setSearchQuery("")}
              aria-label="Clear search query"
            >
              Clear
            </button>
          )}
        </div>

        <div className="ix-category-filters" role="group" aria-label="Filter documentation by category">
          {categories.map((cat) => (
            <button
              key={cat.id}
              type="button"
              className={`ix-cat-pill ${selectedCategory === cat.id ? "ix-cat-pill--active" : ""}`}
              onClick={() => setSelectedCategory(cat.id)}
              aria-pressed={selectedCategory === cat.id}
              data-testid={`cat-filter-${cat.id}`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Split-Pane Document View (U-1) */}
      <div className="ix-doc-split-pane">
        {/* Left Pane: Search Results & Document Navigation (U-3) */}
        <aside className="ix-doc-list-pane" aria-label="Document search results">
          <div className="ix-doc-results-meta">
            <span className="ix-metadata">
              Found {searchResults.length} topic{searchResults.length === 1 ? "" : "s"}
            </span>
          </div>

          {searchResults.length === 0 ? (
            <div className="ix-no-results" data-testid="no-results-message">
              <p className="muted">No matching topics found for "{searchQuery}". Try different keywords.</p>
            </div>
          ) : (
            <ul className="ix-doc-item-list" role="list">
              {searchResults.map((doc) => (
                <li
                  key={doc.id}
                  className={`ix-doc-nav-item ${selectedDocId === doc.id ? "ix-doc-nav-item--selected" : ""}`}
                  data-testid={`doc-item-${doc.id}`}
                  onClick={() => setSelectedDocId(doc.id)}
                >
                  <div className="ix-doc-nav-header">
                    <span className="ix-doc-category-tag mono">{doc.category}</span>
                    <strong className="ix-doc-item-title">{doc.title}</strong>
                  </div>
                  <p className="ix-doc-item-summary">{doc.summary}</p>
                  <div className="ix-doc-tags-row">
                    {doc.tags.slice(0, 3).map((t) => (
                      <span key={t} className="ix-tag-pill">
                        #{t}
                      </span>
                    ))}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </aside>

        {/* Right Pane: Document Reading View (U-4) */}
        <main className="ix-doc-viewer-pane" aria-label="Document viewer">
          {activeDoc ? (
            <article className="ix-doc-article" data-testid="active-doc-article">
              <header className="ix-article-header">
                <div className="ix-article-meta-row">
                  <span className="ix-category-badge mono">{activeDoc.category.toUpperCase()}</span>
                  <span className="ix-doc-id mono">ID: {activeDoc.id}</span>
                </div>
                <h1 className="ix-article-title">{activeDoc.title}</h1>
                <p className="ix-article-summary">{activeDoc.summary}</p>
                <div className="ix-article-tags">
                  {activeDoc.tags.map((tag) => (
                    <span key={tag} className="ix-article-tag">
                      #{tag}
                    </span>
                  ))}
                </div>
              </header>

              <hr className="ix-divider" />

              <div className="ix-article-content">
                <SandboxedMarkdownViewer content={activeDoc.contentMarkdown} />
              </div>
            </article>
          ) : (
            <div className="ix-doc-empty">
              <p className="muted">Select a topic from the list on the left to read.</p>
            </div>
          )}
        </main>
      </div>
    </section>
  );
}
