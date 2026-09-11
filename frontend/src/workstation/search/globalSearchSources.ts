import {
  fetchAdvisorySignals,
  fetchJournalEntries,
  fetchResearchManagementBundle,
  type AdvisorySignal,
  type ManualJournalEntry,
  type ResearchCollection,
} from "../../api/client";
import { WORKSPACE_REGISTRY, type WorkspaceDefinition } from "../registry/workspaceRegistry";
import type { GlobalSearchResult, GlobalSearchSource } from "./globalSearchTypes";

function includesQuery(parts: readonly string[], query: string): boolean {
  const normalized = query.trim().toLowerCase();
  return parts.some((part) => part.toLowerCase().includes(normalized));
}

function workspaceResult(workspace: WorkspaceDefinition): GlobalSearchResult {
  return {
    id: `workspace:${workspace.id}`,
    entityType: "workspace",
    title: workspace.displayName,
    subtitle: workspace.description,
    sourceWorkspaceId: workspace.id,
    route: workspace.route,
    badges: [workspace.navigationCategory, "Read-only jump-to"],
    provenance: "workspace-registry",
    resultAction: "navigate",
    readonly: true,
    sourceId: "workspace",
  };
}

function signalResult(signal: AdvisorySignal): GlobalSearchResult {
  return {
    id: `signal:${signal.signal_id}`,
    entityType: "signal",
    title: `${signal.symbol} ${signal.timeframe} advisory signal`,
    subtitle: `${signal.signal_state} · ${signal.state_reason}`,
    sourceWorkspaceId: "research.advisory_signals",
    route: "/signals",
    artifactId: signal.signal_id,
    badges: ["Signal", "Read-only jump-to"],
    snippet: signal.rationale,
    provenance: "existing-read-api",
    resultAction: "navigate",
    readonly: true,
    sourceId: "signals",
  };
}

function journalResult(entry: ManualJournalEntry): GlobalSearchResult {
  return {
    id: `journal:${entry.journal_id}`,
    entityType: "journal-entry",
    title: entry.title,
    subtitle: "Research journal entry",
    sourceWorkspaceId: "review.journal",
    route: "/journal",
    artifactId: entry.journal_id,
    badges: ["Journal", "Read-only jump-to"],
    snippet: entry.reflection_text,
    provenance: "existing-read-api",
    resultAction: "navigate",
    readonly: true,
    sourceId: "journal",
  };
}

function collectionResult(collection: ResearchCollection): GlobalSearchResult {
  return {
    id: `research-collection:${collection.collection_id}`,
    entityType: "research-collection",
    title: collection.name,
    subtitle: "Research collection",
    sourceWorkspaceId: "review.research_management",
    // UI-CONV-P03 item 4: jump-to targets the post-absorption home directly
    // (the terminal research stage) rather than the legacy redirect.
    route: "/?view=research",
    artifactId: collection.collection_id,
    badges: ["Collection", "Read-only jump-to"],
    snippet: collection.description ?? undefined,
    provenance: "existing-read-api",
    resultAction: "navigate",
    readonly: true,
    sourceId: "research-collections",
  };
}

export function createWorkspaceSearchSource(
  workspaces: readonly WorkspaceDefinition[] = WORKSPACE_REGISTRY,
): GlobalSearchSource {
  return {
    id: "workspace",
    label: "Workspaces",
    async fetchResults({ query }) {
      return workspaces
        .filter((workspace) => !workspace.aliasFor)
        .filter((workspace) =>
          includesQuery(
            [workspace.displayName, workspace.description, workspace.navigationCategory, workspace.route],
            query,
          ),
        )
        .map(workspaceResult);
    },
  };
}

export function createSignalSearchSource(
  fetcher: typeof fetchAdvisorySignals = fetchAdvisorySignals,
): GlobalSearchSource {
  return {
    id: "signals",
    label: "Signals",
    async fetchResults({ query, abortSignal }) {
      if (abortSignal?.aborted) return [];
      const signals = await fetcher({ limit: 50 });
      if (abortSignal?.aborted) return [];
      return signals
        .filter((signal) =>
          includesQuery(
            [signal.signal_id, signal.symbol, signal.timeframe, signal.signal_state, signal.state_reason, signal.rationale],
            query,
          ),
        )
        .map(signalResult);
    },
  };
}

export function createJournalSearchSource(
  fetcher: typeof fetchJournalEntries = fetchJournalEntries,
): GlobalSearchSource {
  return {
    id: "journal",
    label: "Journal",
    async fetchResults({ query, abortSignal }) {
      if (abortSignal?.aborted) return [];
      const entries = await fetcher(50);
      if (abortSignal?.aborted) return [];
      return entries
        .filter((entry) =>
          includesQuery([entry.journal_id, entry.title, entry.reflection_text, entry.lesson_notes ?? ""], query),
        )
        .map(journalResult);
    },
  };
}

export function makeResearchCollectionsSearchSource(
  fetcher: typeof fetchResearchManagementBundle = fetchResearchManagementBundle,
): GlobalSearchSource {
  return {
    id: "research-collections",
    label: "Research collections",
    async fetchResults({ query, abortSignal }) {
      if (abortSignal?.aborted) return [];
      const bundle = await fetcher(50);
      if (abortSignal?.aborted) return [];
      return bundle.collections
        .filter((collection) =>
          includesQuery([collection.collection_id, collection.name, collection.description ?? ""], query),
        )
        .map(collectionResult);
    },
  };
}

export function createDefaultGlobalSearchSources(): GlobalSearchSource[] {
  return [
    createWorkspaceSearchSource(),
    createSignalSearchSource(),
    createJournalSearchSource(),
    makeResearchCollectionsSearchSource(),
  ];
}

export const GLOBAL_SEARCH_SOURCE_IDS = createDefaultGlobalSearchSources().map((source) => source.id);
