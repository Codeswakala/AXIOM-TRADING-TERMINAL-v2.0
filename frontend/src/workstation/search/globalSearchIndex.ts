import type {
  GlobalSearchIndexOptions,
  GlobalSearchResult,
  GlobalSearchSource,
} from "./globalSearchTypes";

const DEFAULT_OPTIONS: GlobalSearchIndexOptions = {
  minQueryLength: 2,
  maxResultsPerSource: 8,
  maxResultsTotal: 24,
  ttlMs: 30_000,
};

type CacheEntry = {
  expiresAt: number;
  results: GlobalSearchResult[];
};

const sourceCache = new Map<string, CacheEntry>();

export function normalizeSearchQuery(query: string): string {
  return query.trim().toLowerCase();
}

export function rankGlobalSearchResult(result: GlobalSearchResult, query: string): number {
  const normalized = normalizeSearchQuery(query);
  const title = result.title.toLowerCase();
  const subtitle = result.subtitle.toLowerCase();
  const snippet = (result.snippet ?? "").toLowerCase();
  if (title === normalized) return 0;
  if (title.startsWith(normalized)) return 1;
  if (title.split(/\s+/).some((word) => word.startsWith(normalized))) return 2;
  if (title.includes(normalized)) return 3;
  if (subtitle.includes(normalized)) return 4;
  if (snippet.includes(normalized)) return 5;
  return 9;
}

export function resultMatchesQuery(result: GlobalSearchResult, query: string): boolean {
  return rankGlobalSearchResult(result, query) < 9;
}

export function assertReadOnlyNavigationResult(result: GlobalSearchResult): void {
  if (result.resultAction !== "navigate" || result.readonly !== true) {
    throw new Error(`UNSAFE_SEARCH_RESULT:${result.id}`);
  }
}

export async function runGlobalSearch(
  sources: readonly GlobalSearchSource[],
  query: string,
  abortSignal?: AbortSignal,
  options: Partial<GlobalSearchIndexOptions> = {},
): Promise<GlobalSearchResult[]> {
  const resolvedOptions = { ...DEFAULT_OPTIONS, ...options };
  const normalized = normalizeSearchQuery(query);
  if (normalized.length < resolvedOptions.minQueryLength) return [];

  const grouped = await Promise.all(
    sources.map(async (source) => {
      const cacheKey = `${source.id}:${normalized}`;
      const cached = sourceCache.get(cacheKey);
      if (cached && cached.expiresAt > Date.now()) return cached.results;
      if (abortSignal?.aborted) return [];
      const fetched = await source.fetchResults({ query: normalized, abortSignal });
      const results = fetched
        .filter((result) => resultMatchesQuery(result, normalized))
        .sort((left, right) => rankGlobalSearchResult(left, normalized) - rankGlobalSearchResult(right, normalized))
        .slice(0, resolvedOptions.maxResultsPerSource);
      for (const result of results) assertReadOnlyNavigationResult(result);
      sourceCache.set(cacheKey, { expiresAt: Date.now() + resolvedOptions.ttlMs, results });
      return results;
    }),
  );

  return grouped
    .flat()
    .sort((left, right) => rankGlobalSearchResult(left, normalized) - rankGlobalSearchResult(right, normalized))
    .slice(0, resolvedOptions.maxResultsTotal);
}

export function clearGlobalSearchCache(): void {
  sourceCache.clear();
}
