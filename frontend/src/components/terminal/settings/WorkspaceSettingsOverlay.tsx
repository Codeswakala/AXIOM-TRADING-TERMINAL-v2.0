import { useEffect, useMemo, useState } from "react";
import {
  createWorkspacePreference,
  fetchWorkspacePreferences,
  updateWorkspacePreference,
  type OperatorWorkspacePreference,
  type OperatorWorkspacePreferenceWrite,
} from "../../../api/client";
import { useOverlayController } from "../../../workstation/overlays/OverlayProvider";
import "./WorkspaceSettingsOverlay.css";

/**
 * WorkspaceSettingsOverlay (UI-CONV-P03 item 3)
 *
 * Re-homed home of WorkspaceCustomizationPage: a shell-owned settings overlay
 * (modal surface in the overlay layer), reachable from
 *   - the global command header (Settings button),
 *   - the left module rail (via /workspace -> /?open=settings redirect),
 *   - the legacy route /workspace (redirect, never 404 — R2).
 *
 * Chosen home reasoning (BUILD_DIRECTIVE_UI-CONV-P03_ITEM3 §3):
 *   - NOT a bottom-dock tab: settings carry a different intent and lifecycle
 *     than the research tabs (TRADE_PLANS|JOURNAL|RISK|SCENARIOS|PORTFOLIO).
 *   - NOT the 320px right dock: the preference editor's form fields need width.
 *   - NOT the primary stage: the stage is reserved for research-scale surfaces
 *     (chart | research), per ITRGA's verified constraints.
 *   - The shell already owns an overlay layer with the exact modal pattern
 *     (CommandPalette, GlobalSearch, GlobalDialog) — the settings surface joins
 *     that layer with zero new architecture.
 *
 * Constitutional notes:
 *   - M1: BOTH persisted mutations survive re-homing (create + update).
 *   - M2: explicit operator-visible error text on every failure; updates apply
 *     only AFTER the server round-trip — no optimistic mutation of persisted
 *     state (a data-honesty requirement in the OBS-CONV2-1 family).
 *   - M3: the verbatim empty state "No workspace preferences have been saved
 *     for this operator." is preserved.
 *   - R3: no fabricated defaults presented as saved operator state — the form's
 *     initial values are editor defaults, the list/detail render server rows only.
 *   - T-1/T-6: presentation preferences only; AXIOM does not act.
 */

const DEFAULT_MODULES = [
  "operations",
  "advisory_signals",
  "institutional_intelligence",
  "chart_workspace",
  "execution_research",
];

const DEFAULT_FORM: OperatorWorkspacePreferenceWrite = {
  workspace_key: "default",
  layout_config: { density: "comfortable", columns: 12, primary_view: "research" },
  visible_modules: DEFAULT_MODULES,
  theme_config: { mode: "dark", accent: "blue" },
  metadata: { note: "presentation preferences only" },
};

export type WorkspaceCustomizationProps = {
  preferences: OperatorWorkspacePreference[];
  loading?: boolean;
  error?: string | null;
  onCreatePreference?: (payload: OperatorWorkspacePreferenceWrite) => Promise<void> | void;
  onUpdatePreference?: (
    preferenceId: string,
    payload: OperatorWorkspacePreferenceWrite,
  ) => Promise<void> | void;
  onRefresh?: () => void;
};

function parseList(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function formatJson(value: Record<string, unknown> | undefined): string {
  return JSON.stringify(value ?? {}, null, 2);
}

function parseJsonObject(value: string, fallback: Record<string, unknown>): Record<string, unknown> {
  try {
    const parsed = JSON.parse(value) as unknown;
    return parsed && typeof parsed === "object" && !Array.isArray(parsed)
      ? (parsed as Record<string, unknown>)
      : fallback;
  } catch {
    return fallback;
  }
}

/**
 * Presentational surface — relocated from pages/WorkspaceCustomizationPage.tsx
 * with its export name and contract preserved so existing consumers and tests
 * bind unchanged. Extended with data-testid hooks on every major region (R4).
 */
export function WorkspaceCustomizationWorkspace({
  preferences,
  loading = false,
  error = null,
  onCreatePreference,
  onUpdatePreference,
  onRefresh,
}: WorkspaceCustomizationProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selected = useMemo(
    () => preferences.find((preference) => preference.preference_id === selectedId) ?? preferences[0] ?? null,
    [preferences, selectedId],
  );
  const [workspaceKey, setWorkspaceKey] = useState(DEFAULT_FORM.workspace_key ?? "default");
  const [layoutText, setLayoutText] = useState(formatJson(DEFAULT_FORM.layout_config));
  const [visibleModulesText, setVisibleModulesText] = useState(DEFAULT_MODULES.join(", "));
  const [themeText, setThemeText] = useState(formatJson(DEFAULT_FORM.theme_config));
  const [metadataText, setMetadataText] = useState(formatJson(DEFAULT_FORM.metadata));

  function loadPreference(preference: OperatorWorkspacePreference) {
    setSelectedId(preference.preference_id);
    setWorkspaceKey(preference.workspace_key);
    setLayoutText(formatJson(preference.layout_config));
    setVisibleModulesText(preference.visible_modules.join(", "));
    setThemeText(formatJson(preference.theme_config));
    setMetadataText(formatJson(preference.metadata));
  }

  function payloadFromForm(): OperatorWorkspacePreferenceWrite {
    return {
      workspace_key: workspaceKey,
      layout_config: parseJsonObject(layoutText, DEFAULT_FORM.layout_config ?? {}),
      visible_modules: parseList(visibleModulesText),
      theme_config: parseJsonObject(themeText, DEFAULT_FORM.theme_config ?? {}),
      metadata: parseJsonObject(metadataText, DEFAULT_FORM.metadata ?? {}),
    };
  }

  return (
    <div className="workspace-settings-surface" data-testid="workspace-settings-surface">
      <div className="page-header">
        <div>
          <h1>Workspace Customization</h1>
          <p className="muted">
            Per-operator presentation preferences for research surfaces. Layout, theme, and
            visible-module choices are scoped to the signed-in operator and do not change research
            artifacts.
          </p>
        </div>
        <button
          type="button"
          className="btn primary"
          onClick={onRefresh}
          data-testid="workspace-pref-refresh-btn"
        >
          Refresh Preferences
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Workspace preference disclaimer">
        <strong>Presentation preferences only.</strong> These settings customize the research terminal
        view for the current operator. AXIOM does not act.
      </section>

      {error ? (
        <p className="error-text" data-testid="workspace-pref-error">
          {error}
        </p>
      ) : null}
      {loading ? (
        <p className="muted" data-testid="workspace-pref-loading">
          Loading workspace preferences…
        </p>
      ) : null}

      <div className="workspace-preference-grid">
        <section
          className="panel workspace-preference-form"
          aria-label="Workspace preference editor"
          data-testid="workspace-preference-editor"
        >
          <h2>Preference Editor</h2>
          <label className="field">
            <span>Workspace key</span>
            <input
              value={workspaceKey}
              onChange={(event) => setWorkspaceKey(event.target.value)}
              data-testid="workspace-pref-key-input"
            />
          </label>
          <label className="field">
            <span>Layout config JSON</span>
            <textarea
              value={layoutText}
              onChange={(event) => setLayoutText(event.target.value)}
              data-testid="workspace-pref-layout-input"
            />
          </label>
          <label className="field">
            <span>Visible modules</span>
            <input
              value={visibleModulesText}
              onChange={(event) => setVisibleModulesText(event.target.value)}
              data-testid="workspace-pref-modules-input"
            />
          </label>
          <label className="field">
            <span>Theme config JSON</span>
            <textarea
              value={themeText}
              onChange={(event) => setThemeText(event.target.value)}
              data-testid="workspace-pref-theme-input"
            />
          </label>
          <label className="field">
            <span>Metadata JSON</span>
            <textarea
              value={metadataText}
              onChange={(event) => setMetadataText(event.target.value)}
              data-testid="workspace-pref-metadata-input"
            />
          </label>
          <div className="workspace-preference-actions">
            <button
              type="button"
              className="btn primary"
              onClick={() => void onCreatePreference?.(payloadFromForm())}
              data-testid="workspace-pref-create-btn"
            >
              Save preferences
            </button>
            {selected ? (
              <button
                type="button"
                className="btn"
                onClick={() => void onUpdatePreference?.(selected.preference_id, payloadFromForm())}
                data-testid="workspace-pref-update-btn"
              >
                Update selected preferences
              </button>
            ) : null}
          </div>
        </section>

        <section
          className="panel"
          aria-label="Persisted workspace preferences"
          data-testid="workspace-saved-preferences"
        >
          <h2>Saved Preferences</h2>
          {preferences.length === 0 && !loading ? (
            <p
              className="muted"
              data-testid="workspace-preferences-empty"
            >
              No workspace preferences have been saved for this operator.
            </p>
          ) : null}
          <div className="workspace-preference-list">
            {preferences.map((preference) => (
              <button
                key={preference.preference_id}
                type="button"
                className={`workspace-preference-card${
                  selected?.preference_id === preference.preference_id ? " active" : ""
                }`}
                onClick={() => loadPreference(preference)}
                data-testid={`workspace-pref-card-${preference.preference_id}`}
              >
                <span className="badge stub">{preference.research_status}</span>
                <strong>{preference.workspace_key}</strong>
                <small>{preference.visible_modules.join(", ")}</small>
              </button>
            ))}
          </div>
        </section>

        <section
          className="panel"
          aria-label="Workspace preference detail"
          data-testid="workspace-preference-detail"
        >
          <h2>Preference Detail</h2>
          {selected ? (
            <article className="workspace-preference-detail">
              <h3>{selected.workspace_key}</h3>
              <dl className="kv compact">
                <dt>Operator</dt>
                <dd className="mono">{selected.operator_id}</dd>
                <dt>Status</dt>
                <dd>{selected.research_status}</dd>
                <dt>Modules</dt>
                <dd>{selected.visible_modules.join(", ")}</dd>
                <dt>Theme</dt>
                <dd>{formatJson(selected.theme_config)}</dd>
              </dl>
            </article>
          ) : (
            <p className="muted">Select a preference.</p>
          )}
        </section>
      </div>
    </div>
  );
}

/**
 * Self-fetching overlay container. Both persisted mutations are wired (M1);
 * every failure surfaces explicit operator-visible error text (M2); state
 * updates only after the server round-trip (no optimistic mutation).
 */
export function WorkspaceSettingsOverlay() {
  const overlay = useOverlayController();
  const [preferences, setPreferences] = useState<OperatorWorkspacePreference[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setPreferences(await fetchWorkspacePreferences(50));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load workspace preferences");
    } finally {
      setLoading(false);
    }
  }

  async function createPreference(payload: OperatorWorkspacePreferenceWrite) {
    setError(null);
    try {
      const created = await createWorkspacePreference(payload);
      setPreferences((current) => [created, ...current]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save workspace preferences");
    }
  }

  async function updatePreference(preferenceId: string, payload: OperatorWorkspacePreferenceWrite) {
    setError(null);
    try {
      const updated = await updateWorkspacePreference(preferenceId, payload);
      setPreferences((current) =>
        current.map((preference) =>
          preference.preference_id === preferenceId ? updated : preference,
        ),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update workspace preferences");
    }
  }

  // Load on first open; refresh is operator-initiated via the Refresh button.
  const [hasLoaded, setHasLoaded] = useState(false);
  useEffect(() => {
    if (overlay.settingsOpen && !hasLoaded) {
      setHasLoaded(true);
      void load();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- load-on-first-open only
  }, [overlay.settingsOpen, hasLoaded]);

  if (!overlay.settingsOpen) return null;

  return (
    <div className="ix-settings-backdrop" data-testid="workspace-settings-backdrop">
      <div
        className="ix-settings-overlay"
        role="dialog"
        aria-modal="true"
        aria-label="Workspace settings"
        data-testid="workspace-settings-overlay"
      >
        <div className="ix-settings-header">
          <span className="ix-metadata mono">WORKSPACE SETTINGS</span>
          <button
            type="button"
            className="ix-shell-button"
            onClick={overlay.closeSettings}
            aria-label="Close workspace settings"
            data-testid="workspace-settings-close-btn"
          >
            Close
          </button>
        </div>
        <div className="ix-settings-body">
          <WorkspaceCustomizationWorkspace
            preferences={preferences}
            loading={loading}
            error={error}
            onCreatePreference={(payload) => void createPreference(payload)}
            onUpdatePreference={(preferenceId, payload) => void updatePreference(preferenceId, payload)}
            onRefresh={() => void load()}
          />
        </div>
      </div>
    </div>
  );
}
