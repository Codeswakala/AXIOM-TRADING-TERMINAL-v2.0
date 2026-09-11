import {
  createWorkspacePreference,
  fetchWorkspacePreferences,
  updateWorkspacePreference,
  type OperatorWorkspacePreference,
  type OperatorWorkspacePreferenceWrite,
} from "../../api/client";
import { normalizeThemeId, type ThemeId } from "../design/theme";
import type { LayoutDescriptor } from "../panels/dockingEngine";

export const SHELL_WORKSPACE_KEY = "institutional-shell-v1";

export type ShellLayoutPreference = {
  activeWorkspaceId: string;
  lastRoute: string;
  navigationCollapsed: boolean;
  panelLayout: LayoutDescriptor;
  /** BO-F-00 supersession: six-theme vocabulary (Blueprint §3). Legacy records
      carrying the pre-F-00 "dark"/"light" strings normalize at read time. */
  themeMode: ThemeId;
  updatedAt: string;
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

export function findShellWorkspacePreference(
  preferences: OperatorWorkspacePreference[],
): OperatorWorkspacePreference | null {
  return preferences.find((preference) => preference.workspace_key === SHELL_WORKSPACE_KEY) ?? null;
}

export function toShellPreferenceWrite(
  state: ShellLayoutPreference,
): OperatorWorkspacePreferenceWrite {
  return {
    workspace_key: SHELL_WORKSPACE_KEY,
    layout_config: {
      active_workspace: state.activeWorkspaceId,
      last_route: state.lastRoute,
      navigation: { collapsed: state.navigationCollapsed },
      panel_layout: state.panelLayout,
      persistence_scope: "operator_shell_layout",
    },
    visible_modules: ["operations", "research_journal", "institutional_intelligence"],
    theme_config: { mode: state.themeMode, density: "institutional" },
    metadata: { ui_workstream: "UI-001-P04", version: "shell-persistence-v1" },
  };
}

export function shellPreferenceFromRecord(
  preference: OperatorWorkspacePreference | null,
): ShellLayoutPreference | null {
  if (!preference || !isRecord(preference.layout_config)) return null;
  const layout = preference.layout_config;
  const navigation = isRecord(layout.navigation) ? layout.navigation : {};
  const panelLayout = isRecord(layout.panel_layout) ? (layout.panel_layout as LayoutDescriptor) : null;
  const activeWorkspaceId = String(layout.active_workspace ?? "");
  const lastRoute = String(layout.last_route ?? "");
  if (!activeWorkspaceId || !lastRoute || !panelLayout) return null;
  const themeMode = normalizeThemeId(preference.theme_config.mode);
  return {
    activeWorkspaceId,
    lastRoute,
    navigationCollapsed: Boolean(navigation.collapsed),
    panelLayout,
    themeMode,
    updatedAt: preference.updated_at,
  };
}

export async function loadShellLayoutPreference(): Promise<ShellLayoutPreference | null> {
  const preferences = await fetchWorkspacePreferences(100);
  return shellPreferenceFromRecord(findShellWorkspacePreference(preferences));
}

export async function persistShellLayoutPreference(
  state: ShellLayoutPreference,
): Promise<OperatorWorkspacePreference> {
  const preferences = await fetchWorkspacePreferences(100);
  const existing = findShellWorkspacePreference(preferences);
  const payload = toShellPreferenceWrite(state);
  if (existing) {
    return updateWorkspacePreference(existing.preference_id, payload);
  }
  return createWorkspacePreference(payload);
}
