export type GlobalSearchSourceId = "workspace" | "signals" | "journal" | "research-collections";

export type GlobalSearchEntityType =
  | "workspace"
  | "signal"
  | "journal-entry"
  | "research-collection";

export type GlobalSearchResult = {
  id: string;
  entityType: GlobalSearchEntityType;
  title: string;
  subtitle: string;
  sourceWorkspaceId: string;
  route: string;
  artifactId?: string;
  badges: readonly string[];
  snippet?: string;
  provenance: "workspace-registry" | "existing-read-api";
  resultAction: "navigate";
  readonly: true;
  sourceId: GlobalSearchSourceId;
};

export type GlobalSearchSourceContext = {
  query: string;
  abortSignal?: AbortSignal;
};

export type GlobalSearchSource = {
  id: GlobalSearchSourceId;
  label: string;
  fetchResults: (context: GlobalSearchSourceContext) => Promise<GlobalSearchResult[]>;
};

export type GlobalSearchIndexOptions = {
  minQueryLength: number;
  maxResultsPerSource: number;
  maxResultsTotal: number;
  ttlMs: number;
};

export type GlobalSearchState = {
  loading: boolean;
  results: GlobalSearchResult[];
  error: string | null;
};
