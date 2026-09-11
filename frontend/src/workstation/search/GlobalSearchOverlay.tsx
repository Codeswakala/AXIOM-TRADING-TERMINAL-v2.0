import { useEffect, useMemo, useRef, useState } from "react";
import { runGlobalSearch } from "./globalSearchIndex";
import { createDefaultGlobalSearchSources } from "./globalSearchSources";
import type { GlobalSearchResult, GlobalSearchSource, GlobalSearchState } from "./globalSearchTypes";
import { useOverlayController } from "../overlays/OverlayProvider";

export type GlobalSearchOverlayProps = {
  onNavigate: (route: string) => void;
  sources?: readonly GlobalSearchSource[];
};

export function GlobalSearchOverlay({ onNavigate, sources }: GlobalSearchOverlayProps) {
  const overlay = useOverlayController();
  const inputRef = useRef<HTMLInputElement>(null);
  const triggerReturnRef = useRef<HTMLElement | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const [state, setState] = useState<GlobalSearchState>({ loading: false, results: [], error: null });
  const searchSources = useMemo(() => sources ?? createDefaultGlobalSearchSources(), [sources]);

  useEffect(() => {
    if (overlay.searchOpen) {
      triggerReturnRef.current = document.activeElement as HTMLElement | null;
      window.setTimeout(() => inputRef.current?.focus(), 0);
    }
  }, [overlay.searchOpen]);

  useEffect(() => {
    if (!overlay.searchOpen) return;
    const handle = window.setTimeout(() => {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;
      setActiveIndex(0);
      setState((current) => ({ ...current, loading: true, error: null }));
      void runGlobalSearch(searchSources, query, controller.signal)
        .then((results) => {
          if (!controller.signal.aborted) setState({ loading: false, results, error: null });
        })
        .catch((error: unknown) => {
          if (!controller.signal.aborted) {
            setState({ loading: false, results: [], error: error instanceof Error ? error.message : "Search failed" });
          }
        });
    }, 250);
    return () => {
      window.clearTimeout(handle);
      abortRef.current?.abort();
    };
  }, [overlay.searchOpen, query, searchSources]);

  function close() {
    overlay.closeGlobalSearch();
    setQuery("");
    setState({ loading: false, results: [], error: null });
    triggerReturnRef.current?.focus();
  }

  function selectResult(result: GlobalSearchResult) {
    if (result.resultAction !== "navigate" || result.readonly !== true) return;
    onNavigate(result.route);
    close();
  }

  if (!overlay.searchOpen) return null;

  return (
    <div
      className="ix-global-search"
      role="dialog"
      aria-modal="true"
      aria-label="Global search"
      data-ui002-component="global-search-overlay"
      onKeyDown={(event) => {
        if (event.key === "Escape") {
          event.preventDefault();
          close();
        }
        if (event.key === "ArrowDown") {
          event.preventDefault();
          setActiveIndex((current) => Math.min(current + 1, Math.max(state.results.length - 1, 0)));
        }
        if (event.key === "ArrowUp") {
          event.preventDefault();
          setActiveIndex((current) => Math.max(current - 1, 0));
        }
        if (event.key === "Enter" && state.results[activeIndex]) {
          event.preventDefault();
          selectResult(state.results[activeIndex]);
        }
      }}
    >
      <label className="ix-metadata" htmlFor="ix-global-search-input">
        Search workspaces and read-only artifacts
      </label>
      <input
        id="ix-global-search-input"
        ref={inputRef}
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        aria-label="Global search query"
        placeholder="Search workspace, signal, journal, or collection…"
      />
      <div className="ix-search-status" aria-live="polite">
        {state.loading
          ? "Loading search results"
          : `${state.results.length} read-only navigation results`}
      </div>
      {state.error ? <p className="ix-metadata">{state.error}</p> : null}
      <div className="ix-search-results" role="listbox" aria-label="Global search results">
        {state.results.map((result, index) => (
          <button
            type="button"
            role="option"
            aria-selected={index === activeIndex}
            className={`ix-search-result${index === activeIndex ? " active" : ""}`}
            key={result.id}
            data-result-action={result.resultAction}
            data-readonly={result.readonly}
            data-source-id={result.sourceId}
            onMouseEnter={() => setActiveIndex(index)}
            onClick={() => selectResult(result)}
          >
            <span>{result.title}</span>
            <small>{result.subtitle}</small>
            <span className="ix-metadata">{result.badges.join(" · ")}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
