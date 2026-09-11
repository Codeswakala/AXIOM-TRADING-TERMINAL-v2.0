import { beforeEach, describe, expect, it, vi } from "vitest";
import type { OperatorWorkspacePreference } from "../../api/client";
import { defaultLayoutForWorkspace } from "../panels/layoutManager";
import {
  SHELL_WORKSPACE_KEY,
  findShellWorkspacePreference,
  loadShellLayoutPreference,
  persistShellLayoutPreference,
  shellPreferenceFromRecord,
  toShellPreferenceWrite,
  type ShellLayoutPreference,
} from "./shellPreferences";

const api = vi.hoisted(() => ({
  fetchWorkspacePreferences: vi.fn(),
  createWorkspacePreference: vi.fn(),
  updateWorkspacePreference: vi.fn(),
}));

vi.mock("../../api/client", () => api);

function preference(overrides: Partial<OperatorWorkspacePreference> = {}): OperatorWorkspacePreference {
  return {
    preference_id: "pref-shell",
    created_at: "2026-07-19T00:00:00Z",
    updated_at: "2026-07-19T00:00:00Z",
    operator_id: "operator-1",
    workspace_key: SHELL_WORKSPACE_KEY,
    layout_config: {
      active_workspace: "monitor.operations",
      last_route: "/signals",
      navigation: { collapsed: true },
      panel_layout: defaultLayoutForWorkspace("monitor.operations"),
    },
    visible_modules: ["operations"],
    theme_config: { mode: "dark" },
    research_status: "research_only",
    metadata: { ui_workstream: "UI-001-P04" },
    audit_correlation_id: "corr-shell",
    ...overrides,
  };
}

function shellState(): ShellLayoutPreference {
  return {
    activeWorkspaceId: "monitor.operations",
    lastRoute: "/signals",
    navigationCollapsed: true,
    panelLayout: defaultLayoutForWorkspace("monitor.operations"),
    // BO-F-00 supersession: six-theme vocabulary replaces "dark"/"light".
    themeMode: "midnight",
    updatedAt: "2026-07-19T00:00:00Z",
  };
}

beforeEach(() => {
  api.fetchWorkspacePreferences.mockReset();
  api.createWorkspacePreference.mockReset();
  api.updateWorkspacePreference.mockReset();
});

describe("shellPreferences", () => {
  it("test_shell_layout_persists_via_operator_workspace_preferences_no_new_table", async () => {
    api.fetchWorkspacePreferences.mockResolvedValue([]);
    api.createWorkspacePreference.mockResolvedValue(preference());
    await persistShellLayoutPreference(shellState());
    expect(api.createWorkspacePreference).toHaveBeenCalledWith(
      expect.objectContaining({ workspace_key: SHELL_WORKSPACE_KEY }),
    );
    const payload = api.createWorkspacePreference.mock.calls[0][0];
    expect(payload.layout_config.panel_layout).toBeTruthy();
    expect(JSON.stringify(payload)).not.toContain("new_table");
  });

  it("test_shell_layout_restores_previous_session_after_login", async () => {
    api.fetchWorkspacePreferences.mockResolvedValue([preference()]);
    const loaded = await loadShellLayoutPreference();
    expect(loaded?.activeWorkspaceId).toBe("monitor.operations");
    expect(loaded?.lastRoute).toBe("/signals");
    expect(loaded?.navigationCollapsed).toBe(true);
    expect(loaded?.panelLayout.workspaceId).toBe("monitor.operations");
  });

  it("test_shell_persistence_no_execution_or_actuation_and_no_secret_fields", () => {
    const payload = toShellPreferenceWrite(shellState());
    const text = JSON.stringify(payload).toLowerCase();
    const forbidden = [
      "buy",
      "sell",
      "place_order",
      "submit order",
      "go live",
      "connect broker",
      "account_id",
      "order_ticket",
      "access_token",
      "refresh_token",
      "jwt",
      "password",
      "api_key",
      "private_key",
    ];
    for (const marker of forbidden) {
      expect(text).not.toContain(marker);
    }
  });

  it("finds and parses only the institutional shell preference", () => {
    expect(findShellWorkspacePreference([preference({ workspace_key: "other" })])).toBeNull();
    const parsed = shellPreferenceFromRecord(preference());
    expect(parsed?.lastRoute).toBe("/signals");
  });
});
