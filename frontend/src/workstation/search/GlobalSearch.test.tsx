import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { OverlayProvider, useOverlayController } from "../overlays/OverlayProvider";
import { WORKSPACE_REGISTRY } from "../registry/workspaceRegistry";
import { GlobalSearchOverlay } from "./GlobalSearchOverlay";
import { assertReadOnlyNavigationResult, runGlobalSearch } from "./globalSearchIndex";
import {
  createDefaultGlobalSearchSources,
  createJournalSearchSource,
  makeResearchCollectionsSearchSource,
  createSignalSearchSource,
  createWorkspaceSearchSource,
  GLOBAL_SEARCH_SOURCE_IDS,
} from "./globalSearchSources";
import type { GlobalSearchResult, GlobalSearchSource } from "./globalSearchTypes";

function searchResult(overrides: Partial<GlobalSearchResult> = {}): GlobalSearchResult {
  return {
    id: "workspace:monitor.operations",
    entityType: "workspace",
    title: "Operations",
    subtitle: "Platform operations",
    sourceWorkspaceId: "monitor.operations",
    route: "/",
    badges: ["Workspace", "Read-only jump-to"],
    provenance: "workspace-registry",
    resultAction: "navigate",
    readonly: true,
    sourceId: "workspace",
    ...overrides,
  };
}

const stubSources: GlobalSearchSource[] = [
  {
    id: "workspace",
    label: "Workspaces",
    fetchResults: async () => [searchResult({ title: "Operations", route: "/" })],
  },
  {
    id: "signals",
    label: "Signals",
    fetchResults: async () => [
      searchResult({
        id: "signal:sig-1",
        entityType: "signal",
        title: "EURUSD advisory signal",
        subtitle: "warning",
        route: "/signals",
        sourceWorkspaceId: "research.advisory_signals",
        provenance: "existing-read-api",
        sourceId: "signals",
      }),
    ],
  },
  {
    id: "journal",
    label: "Journal",
    fetchResults: async () => [
      searchResult({
        id: "journal:j-1",
        entityType: "journal-entry",
        title: "EURUSD research reflection",
        subtitle: "Research journal entry",
        route: "/journal",
        sourceWorkspaceId: "review.journal",
        provenance: "existing-read-api",
        sourceId: "journal",
      }),
    ],
  },
  {
    id: "research-collections",
    label: "Research collections",
    fetchResults: async () => [
      searchResult({
        id: "research-collection:c-1",
        entityType: "research-collection",
        title: "EURUSD collection",
        subtitle: "Research collection",
        // UI-CONV-P03 item 4: re-pointed to the post-absorption research stage.
        route: "/?view=research",
        sourceWorkspaceId: "review.research_management",
        provenance: "existing-read-api",
        sourceId: "research-collections",
      }),
    ],
  },
];

function SearchHarness({ onNavigate = vi.fn() }: { onNavigate?: (route: string) => void }) {
  const overlay = useOverlayController();
  return (
    <>
      <button type="button" onClick={overlay.openGlobalSearch}>
        Open search
      </button>
      <GlobalSearchOverlay sources={stubSources} onNavigate={onNavigate} />
    </>
  );
}

function renderSearchHarness(onNavigate = vi.fn()) {
  render(
    <MemoryRouter>
      <OverlayProvider>
        <SearchHarness onNavigate={onNavigate} />
      </OverlayProvider>
    </MemoryRouter>,
  );
}

async function readRawSource(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const parts = pathSuffix.split("/");
  const fileName = parts[parts.length - 1] ?? pathSuffix;
  const entry = Object.entries(modules).find(
    ([path]) => path.endsWith(pathSuffix) || path.endsWith(fileName),
  );
  if (!entry) throw new Error(`Raw source not found: ${pathSuffix}`);
  const loader = entry[1] as () => Promise<string>;
  return loader();
}

describe("UI-002-P04 global search framework", () => {
  it("test_ui002_global_search_returns_read_only_navigation_results", async () => {
    const results = await runGlobalSearch(stubSources, "eurusd");
    expect(results.length).toBeGreaterThanOrEqual(3);
    for (const result of results) {
      expect(result.resultAction).toBe("navigate");
      expect(result.readonly).toBe(true);
      expect(result.route.startsWith("/")).toBe(true);
      expect("onSelect" in result).toBe(false);
    }
  });

  it("test_ui002_global_search_uses_workspace_registry_and_existing_read_sources", async () => {
    expect(GLOBAL_SEARCH_SOURCE_IDS).toEqual(["workspace", "signals", "journal", "research-collections"]);
    expect(createDefaultGlobalSearchSources().map((source) => source.id)).toEqual(GLOBAL_SEARCH_SOURCE_IDS);

    const workspace = await createWorkspaceSearchSource(WORKSPACE_REGISTRY).fetchResults({ query: "operations" });
    const signals = await createSignalSearchSource(async () => [
      {
        signal_id: "sig-1",
        created_at: "2026-07-22T00:00:00Z",
        as_of_time: "2026-07-22T00:00:00Z",
        market_class: "fx",
        provider: "sample",
        symbol: "EURUSD",
        timeframe: "H1",
        model_artifact_id: "model-1",
        model_version: "v1",
        feature_set_version: "features-v1",
        experiment_id: "exp-1",
        statistical_report_id: null,
        calibration_report_id: null,
        economic_report_id: null,
        generalization_report_id: null,
        inference_input_hash: "hash",
        raw_score: null,
        calibrated_confidence: null,
        input_staleness_seconds: null,
        signal_validity_seconds: null,
        expires_at: null,
        freshness_status: null,
        signal_direction: "withheld",
        signal_state: "warning",
        state_reason: "guardrail",
        eligibility_reasons: [],
        operating_domain_status: "in_domain",
        calibration_status: "calibrated",
        economic_verdict: "research_only",
        risk_notes: null,
        rationale: "EURUSD research context",
        explainability_summary: {},
        state_transition_history: [],
        audit_correlation_id: "audit",
      },
    ]).fetchResults({ query: "eurusd" });
    const journal = await createJournalSearchSource(async () => [
      {
        journal_id: "j-1",
        created_at: "2026-07-22T00:00:00Z",
        operator_id: "op-1",
        title: "EURUSD reflection",
        reflection_text: "research reflection",
        linked_plan_id: null,
        linked_signal_ids: [],
        linked_report_ids: [],
        emotion_tags: [],
        process_tags: [],
        lesson_notes: null,
        research_disclaimer: "research only",
        research_status: "research_only",
        audit_correlation_id: "audit",
      },
    ]).fetchResults({ query: "eurusd" });
    const collections = await makeResearchCollectionsSearchSource(async () => ({
      collections: [
        {
          collection_id: "c-1",
          created_at: "2026-07-22T00:00:00Z",
          updated_at: "2026-07-22T00:00:00Z",
          operator_id: "op-1",
          name: "EURUSD collection",
          description: "research collection",
          research_status: "research_only",
          audit_correlation_id: "audit",
        },
      ],
      members: [],
      tags: [],
      supported_artifact_types: [],
      posture: "reference_only",
    })).fetchResults({ query: "eurusd" });

    expect(workspace[0].sourceId).toBe("workspace");
    expect(signals[0].sourceId).toBe("signals");
    expect(journal[0].sourceId).toBe("journal");
    expect(collections[0].sourceId).toBe("research-collections");
  });

  it("test_ui002_global_search_never_registers_mutation_or_actuation_results", () => {
    expect(() => assertReadOnlyNavigationResult(searchResult())).not.toThrow();
    expect(() =>
      assertReadOnlyNavigationResult(
        searchResult({ resultAction: "mutate" as "navigate", readonly: false as true }),
      ),
    ).toThrow(/UNSAFE_SEARCH_RESULT/);
  });

  it("test_ui002_global_search_does_not_persist_query_text_or_artifact_payloads", async () => {
    const sourceText = (
      await Promise.all(
        [
          "search/globalSearchTypes.ts",
          "search/globalSearchIndex.ts",
          "search/globalSearchSources.ts",
          "search/GlobalSearchOverlay.tsx",
        ].map((path) => readRawSource(path)),
      )
    ).join("\n");
    for (const marker of ["localStorage", "sessionStorage", "search_query", "artifact_payload", "business_payload"]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui002_global_search_accessibility_keyboard_and_result_announcement", async () => {
    const onNavigate = vi.fn();
    renderSearchHarness(onNavigate);
    fireEvent.click(screen.getByRole("button", { name: "Open search" }));
    const input = await screen.findByLabelText("Global search query");
    expect(input).toHaveFocus();
    fireEvent.change(input, { target: { value: "eurusd" } });

    const listbox = screen.getByRole("listbox", { name: "Global search results" });
    await waitFor(() => expect(within(listbox).getAllByRole("option").length).toBeGreaterThanOrEqual(3));
    fireEvent.keyDown(screen.getByRole("dialog", { name: "Global search" }), { key: "Enter" });
    expect(onNavigate).toHaveBeenCalledWith(expect.stringMatching(/^\//));
  });

  it("test_ui002_global_search_adds_no_backend_schema_or_dependency_change", async () => {
    const sourceText = await readRawSource("search/globalSearchSources.ts");
    expect(sourceText).toContain("fetchAdvisorySignals");
    expect(sourceText).toContain("fetchJournalEntries");
    expect(sourceText).toContain("fetchResearchManagementBundle");
    expect(sourceText).not.toContain("/api/v1/search");
    expect(sourceText).not.toContain("search_index");
    expect(sourceText).not.toContain("fuse.js");
    expect(sourceText).not.toContain("fuzzysort");
  });
});
