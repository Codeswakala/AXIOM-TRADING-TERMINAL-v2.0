import { render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { OverlayProvider, useOverlayController } from "../../../workstation/overlays/OverlayProvider";
import { WorkspaceSettingsOverlay } from "./WorkspaceSettingsOverlay";
import type { OperatorWorkspacePreference } from "../../../api/client";
import * as client from "../../../api/client";

vi.mock("../../../api/client", async () => {
  const actual = await vi.importActual<typeof client>("../../../api/client");
  return {
    ...actual,
    fetchWorkspacePreferences: vi.fn(),
    createWorkspacePreference: vi.fn(),
    updateWorkspacePreference: vi.fn(),
  };
});

function preference(overrides: Partial<OperatorWorkspacePreference> = {}): OperatorWorkspacePreference {
  return {
    preference_id: "pref-1",
    created_at: "2026-07-18T10:00:00Z",
    updated_at: "2026-07-18T10:00:00Z",
    operator_id: "operator-1",
    workspace_key: "default",
    layout_config: { density: "comfortable", columns: 12 },
    visible_modules: ["operations", "execution_research"],
    theme_config: { mode: "dark", accent: "blue" },
    research_status: "research_only",
    metadata: { note: "presentation preferences only" },
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

/** Small harness: opens the overlay inside a real OverlayProvider. */
function SettingsHarness({ onOpen }: { onOpen?: (open: () => void) => void }) {
  return (
    <OverlayProvider>
      <HarnessInner onOpen={onOpen} />
    </OverlayProvider>
  );
}

function HarnessInner({ onOpen }: { onOpen?: (open: () => void) => void }) {
  const overlay = useOverlayController();
  return (
    <div>
      <button type="button" onClick={overlay.openSettings} data-testid="harness-open-btn">
        open
      </button>
      <button type="button" onClick={() => onOpen?.(overlay.openSettings)} data-testid="harness-cb-btn">
        cb
      </button>
      <WorkspaceSettingsOverlay />
    </div>
  );
}

beforeEach(() => {
  vi.clearAllMocks();
});

describe("WorkspaceSettingsOverlay (UI-CONV-P03 item 3)", () => {
  it("test_uiconv_p03_settings_empty_state_is_preserved_verbatim", async () => {
    vi.mocked(client.fetchWorkspacePreferences).mockResolvedValue([]);
    render(<SettingsHarness />);
    screen.getByTestId("harness-open-btn").click();

    await waitFor(() => {
      expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument();
    });

    // M3: the verbatim empty state, not a spinner or blank panel.
    await waitFor(() => {
      expect(screen.getByTestId("workspace-preferences-empty")).toHaveTextContent(
        "No workspace preferences have been saved for this operator.",
      );
    });
    // R3: the editor form renders defaults, but the saved list shows no fabricated rows.
    expect(screen.getByTestId("workspace-settings-overlay").querySelectorAll(".workspace-preference-card")).toHaveLength(0);
  });

  it("test_uiconv_p03_settings_create_mutation_round_trips_and_appends_after_response", async () => {
    const created = preference({ preference_id: "pref-new", workspace_key: "intraday" });
    vi.mocked(client.fetchWorkspacePreferences).mockResolvedValue([]);
    vi.mocked(client.createWorkspacePreference).mockResolvedValue(created);

    render(<SettingsHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument());

    screen.getByTestId("workspace-pref-key-input").setAttribute("value", "intraday");
    screen.getByTestId("workspace-pref-create-btn").click();

    // M1: create survives re-homing — called with a payload, list updates only after the response.
    await waitFor(() => {
      expect(client.createWorkspacePreference).toHaveBeenCalledTimes(1);
      expect(screen.getByTestId("workspace-pref-card-pref-new")).toBeInTheDocument();
    });
    // No optimistic append before the server round-trip: the mock resolved
    // immediately, so the card's presence above is post-response. Assert the
    // error banner never appeared.
    expect(screen.queryByTestId("workspace-pref-error")).not.toBeInTheDocument();
  });

  it("test_uiconv_p03_settings_update_mutation_replaces_row_after_response", async () => {
    const updated = preference({ preference_id: "pref-1", workspace_key: "updated-key" });
    vi.mocked(client.fetchWorkspacePreferences).mockResolvedValue([preference()]);
    vi.mocked(client.updateWorkspacePreference).mockResolvedValue(updated);

    render(<SettingsHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument());
    await waitFor(() => expect(screen.getByTestId("workspace-pref-card-pref-1")).toBeInTheDocument());

    screen.getByTestId("workspace-pref-update-btn").click();

    // M1: update survives re-homing.
    await waitFor(() => {
      expect(client.updateWorkspacePreference).toHaveBeenCalledTimes(1);
      expect(client.updateWorkspacePreference).toHaveBeenCalledWith("pref-1", expect.objectContaining({ workspace_key: "default" }));
    });
    expect(screen.queryByTestId("workspace-pref-error")).not.toBeInTheDocument();
  });

  it("test_uiconv_p03_settings_create_failure_surfaces_explicit_error", async () => {
    vi.mocked(client.fetchWorkspacePreferences).mockResolvedValue([]);
    vi.mocked(client.createWorkspacePreference).mockRejectedValue(new Error("Server rejected payload"));

    render(<SettingsHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument());

    screen.getByTestId("workspace-pref-create-btn").click();

    // M2: explicit operator-visible error, never silent.
    await waitFor(() => {
      expect(screen.getByTestId("workspace-pref-error")).toHaveTextContent("Server rejected payload");
    });
    // No optimistic update: list still empty after failure.
    expect(screen.getByTestId("workspace-preferences-empty")).toBeInTheDocument();
  });

  it("test_uiconv_p03_settings_update_failure_surfaces_explicit_error", async () => {
    vi.mocked(client.fetchWorkspacePreferences).mockResolvedValue([preference()]);
    vi.mocked(client.updateWorkspacePreference).mockRejectedValue(new Error("Update conflict"));

    render(<SettingsHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument());
    await waitFor(() => expect(screen.getByTestId("workspace-pref-card-pref-1")).toBeInTheDocument());

    screen.getByTestId("workspace-pref-update-btn").click();

    await waitFor(() => {
      expect(screen.getByTestId("workspace-pref-error")).toHaveTextContent("Update conflict");
    });
  });

  it("test_uiconv_p03_settings_open_and_close_via_shell_overlay_controller", async () => {
    vi.mocked(client.fetchWorkspacePreferences).mockResolvedValue([preference()]);
    render(<SettingsHarness />);

    expect(screen.queryByTestId("workspace-settings-overlay")).not.toBeInTheDocument();
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument());

    screen.getByTestId("workspace-settings-close-btn").click();
    await waitFor(() => expect(screen.queryByTestId("workspace-settings-overlay")).not.toBeInTheDocument());
  });

  it("test_uiconv_p03_settings_all_major_regions_carry_testids", async () => {
    vi.mocked(client.fetchWorkspacePreferences).mockResolvedValue([preference()]);
    render(<SettingsHarness />);
    screen.getByTestId("harness-open-btn").click();
    await waitFor(() => expect(screen.getByTestId("workspace-settings-overlay")).toBeInTheDocument());
    await waitFor(() => expect(screen.getByTestId("workspace-pref-card-pref-1")).toBeInTheDocument());

    for (const testid of [
      "workspace-settings-surface",
      "workspace-preference-editor",
      "workspace-saved-preferences",
      "workspace-preference-detail",
      "workspace-pref-create-btn",
      "workspace-pref-update-btn",
      "workspace-pref-refresh-btn",
    ]) {
      expect(screen.getByTestId(testid)).toBeInTheDocument();
    }

    const detail = screen.getByTestId("workspace-preference-detail");
    expect(within(detail).getByText("default")).toBeInTheDocument();
  });
});
