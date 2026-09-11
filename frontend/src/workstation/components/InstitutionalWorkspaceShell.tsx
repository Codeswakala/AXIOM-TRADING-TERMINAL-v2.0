import { useEffect, useMemo, useRef, useState } from "react";
import { LogoMark } from "../../components/branding/LogoMark";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { fetchHealth, fetchV2Mode } from "../../api/client";
import { createCommandRegistry } from "../commands/commandRegistry";
import { ShellEventBusProvider } from "../events/shellEventBus";
import "../design/tokens.css";
import { THEME_META } from "../design/theme";
import {
  createWorkspaceActivationEvent,
  generateNavigationSections,
} from "../navigation/navigationGenerator";
import { BreadcrumbTrail } from "../navigation/BreadcrumbTrail";
import { NavigationDock } from "../navigation/NavigationDock";
import { UnifiedModuleRail } from "../navigation/UnifiedModuleRail";
import { AlertsProvider } from "../../components/alerts/AlertsProvider";
import { WorkspaceSwitcher } from "../navigation/WorkspaceSwitcher";
import { recordRecentWorkspace } from "../navigation/workspaceHistory";
import { defaultLayoutForWorkspace, createSessionLayoutStore } from "../panels/layoutManager";
import { PanelHost } from "../panels/PanelHost";
import { OverlayLayer } from "../overlays/OverlayLayer";
import { OverlayProvider, useOverlayController } from "../overlays/OverlayProvider";
import {
  loadShellLayoutPreference,
  persistShellLayoutPreference,
} from "../persistence/shellPreferences";
import { WORKSPACE_REGISTRY, workspaceForPath } from "../registry/workspaceRegistry";
import { WorkspaceHost } from "./WorkspaceHost";
import { SkipLink } from "../accessibility/SkipLink";
import { RouteAnnouncer } from "../accessibility/RouteAnnouncer";
import "./InstitutionalWorkspaceShell.css";

/**
 * InstitutionalWorkspaceShell
 *
 * Unified application shell hosting all 16 authenticated workspace routes (B-CONV-1).
 * Replaces the legacy workstation chrome with a unified topology:
 * - Top Global Ticker / Command Bar (banner)
 * - Compact Left Module Rail (navigation)
 * - Primary Workspace Stage (main / WorkspaceHost)
 * - Global Command Palette (accessible everywhere via Ctrl+K / header trigger)
 *
 * Adheres to:
 * - T-1: Zero actuation controls
 * - T-4 / T-5: Zero external LLMs
 * - Doc 16 Brand Standards: Official AX Monogram retained (F-BRAND-1)
 * - Pure Token Consumption: 100% var(--ix-*) design tokens
 * - Presentation container: classification recital lives in the governance
 *   register, not in code comments (FE-U02 ACC-1 site 6 expulsion)
 */
export function InstitutionalWorkspaceShell() {
  return (
    <ShellEventBusProvider>
      <OverlayProvider>
        <AlertsProvider>
          <InstitutionalWorkspaceShellFrame />
        </AlertsProvider>
      </OverlayProvider>
    </ShellEventBusProvider>
  );
}

function InstitutionalWorkspaceShellFrame() {
  const { operator, logout } = useAuth();
  const overlay = useOverlayController();
  const location = useLocation();
  const navigate = useNavigate();
  const activeWorkspace = workspaceForPath(location.pathname);
  const workspaceRef = useRef<HTMLElement>(null);
  const contextRef = useRef<HTMLElement>(null);
  const activityRef = useRef<HTMLElement>(null);
  const commandTriggerRef = useRef<HTMLButtonElement>(null);
  const previousWorkspaceIdRef = useRef<string | null>(null);
  const preserveHeaderFocusAfterNavigationRef = useRef(false);
  const shellPreferenceLoadedRef = useRef(false);
  // PC-FEU02-1 storage election: rail collapse honestly persisted
  // (localStorage key axiom_chrome_rail_collapsed — a UI preference,
  // REF-002-E1 remembered-preference pattern).
  const [navigationCollapsed, setNavigationCollapsedState] = useState(
    () => localStorage.getItem("axiom_chrome_rail_collapsed") === "true",
  );
  const setNavigationCollapsed = (
    updater: boolean | ((current: boolean) => boolean),
  ) => {
    setNavigationCollapsedState((current) => {
      const next = typeof updater === "function" ? updater(current) : updater;
      localStorage.setItem("axiom_chrome_rail_collapsed", String(next));
      return next;
    });
  };
  const [recentWorkspaceIds, setRecentWorkspaceIds] = useState<string[]>([]);
  const [clockUtc, setClockUtc] = useState<string>("");
  // PC-FEU02-1 C3: global health strip — GET /health, generation-guarded
  // 30s poll (the U01 pattern promoted chrome-wide); stale ⇒ CHECKING.
  const [platformHealth, setPlatformHealth] = useState<
    "checking" | "reachable" | "unreachable"
  >("checking");
  const healthGenerationRef = useRef(0);
  // PC-FEU02-1 C3 / ACC-5: mode badge = locked-config law. The registered
  // stance (RESEARCH · NON-ACTUATING) persists; the verification mark
  // turns verified when an authed mode read succeeds this session.
  const [modeVerified, setModeVerified] = useState(false);

  useEffect(() => {
    let disposed = false;

    async function probeHealth() {
      const generation = ++healthGenerationRef.current;
      setPlatformHealth("checking");
      try {
        await fetchHealth();
        if (!disposed && healthGenerationRef.current === generation) {
          setPlatformHealth("reachable");
        }
      } catch {
        if (!disposed && healthGenerationRef.current === generation) {
          setPlatformHealth("unreachable");
        }
      }
    }

    void probeHealth();
    const timer = window.setInterval(() => void probeHealth(), 30_000);
    return () => {
      disposed = true;
      window.clearInterval(timer);
    };
  }, []);

  useEffect(() => {
    // Verified when the session's mode read succeeds (fetchV2Mode is the
    // authed read; absence of the client function or a failed read keeps
    // the honest unverified mark — never a fabricated verification).
    let disposed = false;
    void (async () => {
      try {
        const body = await fetchV2Mode();
        if (!disposed && body.mode === "RESEARCH") {
          setModeVerified(true);
        }
      } catch {
        /* unverified mark stands — honest */
      }
    })();
    return () => {
      disposed = true;
    };
  }, []);
  const layoutStore = useMemo(() => createSessionLayoutStore(), []);
  const [layout, setLayout] = useState(() =>
    layoutStore.load(activeWorkspace.id) ?? defaultLayoutForWorkspace(activeWorkspace.id),
  );
  const [activationEvent, setActivationEvent] = useState(() =>
    createWorkspaceActivationEvent(activeWorkspace),
  );

  useEffect(() => {
    const updateTime = () => {
      const d = new Date();
      setClockUtc(d.toTimeString().slice(0, 8) + " UTC");
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // UI-CONV-P03 deep links: /?open=settings opens the settings overlay (item 3);
  // /?open=governance opens the governance & evidence overlay (item 5).
  const openParam = useMemo(() => new URLSearchParams(location.search).get("open"), [location.search]);
  useEffect(() => {
    if (openParam === "settings") {
      overlay.openSettings();
    } else if (openParam === "governance") {
      overlay.openGovernance();
    }
  }, [openParam, overlay]);

  const navigationSections = useMemo(
    () => generateNavigationSections({ workspaces: WORKSPACE_REGISTRY, operator }),
    [operator],
  );

  const commandWorkspaces = useMemo(
    () => navigationSections.flatMap((section) => section.workspaces),
    [navigationSections],
  );

  const visibleWorkspaceIds = useMemo(
    () => new Set(commandWorkspaces.map((workspace) => workspace.id)),
    [commandWorkspaces],
  );

  const routeByWorkspaceId = useMemo(
    () => new Map(WORKSPACE_REGISTRY.map((workspace) => [workspace.id, workspace.route])),
    [],
  );

  const commandRegistry = useMemo(
    () =>
      createCommandRegistry({
        visibleWorkspaceIds,
        routeForWorkspaceId: (workspaceId) => routeByWorkspaceId.get(workspaceId) ?? null,
        recentWorkspaceIds,
        onNavigate: navigateCommand,
        onToggleNavigation: () => setNavigationCollapsed((curr) => !curr),
        onToggleContext: () => {},
        onToggleActivity: () => {},
        onToggleTheme: overlay.toggleTheme,
        onOpenGlobalSearch: overlay.openGlobalSearch,
        onOpenShellStatus: () =>
          overlay.openDialog({
            title: "Workstation shell status",
            // FE-U02 C4: status dialog speaks backend truth, not literals.
            body: `Command registry active. Mode: RESEARCH · NON-ACTUATING. Platform: ${platformHealth}.`,
          }),
        onShowGovernanceNotification: () =>
          overlay.notify(
            "Governance",
            "RESEARCH · NON-ACTUATING",
            "The platform's registered mode stance. Details on the governance workspace.",
          ),
        onFocusRegion: focusRegion,
        onUnavailable: (label) =>
          overlay.notify("Information", label, "This quick action is reserved for a later phase."),
      }),
    [activeWorkspace.id, overlay, platformHealth, recentWorkspaceIds, routeByWorkspaceId, visibleWorkspaceIds],
  );

  useEffect(() => {
    let cancelled = false;
    async function restoreShellPreference() {
      try {
        const restored = await loadShellLayoutPreference();
        if (cancelled || !restored) return;
        if (restored.themeMode !== overlay.themeMode) {
          // BO-F-00: persisted six-theme restore (setTheme normalizes legacy
          // "dark"/"light" records to the six-theme vocabulary).
          overlay.setTheme(restored.themeMode);
        }
        if (location.pathname === "/" && restored.lastRoute !== "/") {
          navigate(restored.lastRoute, { replace: true });
        }
      } finally {
        if (!cancelled) shellPreferenceLoadedRef.current = true;
      }
    }
    void restoreShellPreference();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    setRecentWorkspaceIds((current) => {
      const next = recordRecentWorkspace(
        current,
        previousWorkspaceIdRef.current,
        activeWorkspace.id,
      );
      previousWorkspaceIdRef.current = activeWorkspace.id;
      return next;
    });
    setActivationEvent(createWorkspaceActivationEvent(activeWorkspace));
    setLayout(layoutStore.load(activeWorkspace.id) ?? defaultLayoutForWorkspace(activeWorkspace.id));
    if (preserveHeaderFocusAfterNavigationRef.current) {
      preserveHeaderFocusAfterNavigationRef.current = false;
    } else {
      window.setTimeout(() => workspaceRef.current?.focus(), 0);
    }
  }, [activeWorkspace, layoutStore]);

  useEffect(() => {
    if (!shellPreferenceLoadedRef.current) return;
    const handle = window.setTimeout(() => {
      void persistShellLayoutPreference({
        activeWorkspaceId: activeWorkspace.id,
        lastRoute: location.pathname,
        navigationCollapsed,
        panelLayout: layout,
        themeMode: overlay.themeMode,
        updatedAt: new Date().toISOString(),
      });
    }, 250);
    return () => window.clearTimeout(handle);
  }, [activeWorkspace.id, layout, location.pathname, navigationCollapsed, overlay.themeMode]);

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        overlay.openCommandPalette();
      }
      if (event.altKey && event.key === "1") {
        event.preventDefault();
        (document.querySelector('[data-region="B"]') as HTMLElement | null)?.focus();
      }
      if (event.altKey && event.key === "2") {
        event.preventDefault();
        workspaceRef.current?.focus();
      }
      if (event.altKey && event.key === "3") {
        event.preventDefault();
        contextRef.current?.focus();
      }
      if (event.altKey && event.key === "4") {
        event.preventDefault();
        activityRef.current?.focus();
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [overlay]);

  function navigateCommand(route: string) {
    navigate(route);
    workspaceRef.current?.focus();
  }

  function navigateFromSwitcher(route: string) {
    preserveHeaderFocusAfterNavigationRef.current = true;
    navigate(route);
  }

  function focusRegion(region: "B" | "C" | "D" | "E") {
    if (region === "C") {
      workspaceRef.current?.focus();
    } else if (region === "B") {
      (document.querySelector('[data-region="B"]') as HTMLElement | null)?.focus();
    } else if (region === "D") {
      contextRef.current?.focus();
    } else if (region === "E") {
      activityRef.current?.focus();
    }
  }

  const isTerminalRoot = location.pathname === "/";

  return (
    <div
      className={`ix-shell unified-terminal-shell${isTerminalRoot ? " terminal-root-active" : ""}${
        navigationCollapsed ? " nav-collapsed" : ""
      } theme-${overlay.themeMode}`}
      data-testid="institutional-workspace-shell"
    >
      {/* Top Global Command & Ticker Bar */}
      <header
        className="ix-global-header"
        role="banner"
        aria-label="Global command bar"
        data-region="A"
      >
        <SkipLink href="#main-content" />
        <RouteAnnouncer />

        {/* Brand Block — POLISH-P01 M6 / GA-173: compass + epsilon mark */}
        <div className="ix-brand-block">
          <div className="ix-brand-mark" data-testid="shell-brand-mark">
            <LogoMark testid="shell-brand-logo-mark" />
          </div>
          <div className="ix-brand-copy">
            <span className="ix-workspace-title">{activeWorkspace.displayName}</span>
            <BreadcrumbTrail />
            <span className="ix-metadata">AXIOM Institutional Workstation · v0.62.0</span>
          </div>
        </div>

        {/* Truthful status cluster (PC-FEU02-1 C3/C4 — FE-U02 rebuild):
            the asserted heritage chips are EXPELLED (ACC-1 census); what
            renders is backend truth only — the locked-config mode badge
            (ACC-5 law: registered stance + honest verification mark)
            and the live health chip (tri-state; stale ⇒ CHECKING). */}
        <div
          className="ix-header-status"
          role="status"
          aria-label="Platform mode and health status"
          data-testid="shell-governance-status"
        >
          <span
            className="ix-status-chip neutral mono"
            data-testid="chrome-mode-badge"
            data-verification={modeVerified ? "verified" : "unverified"}
            title={
              modeVerified
                ? "Mode verified from platform configuration"
                : "Registered platform stance; verified after a mode read succeeds"
            }
          >
            RESEARCH · NON-ACTUATING
          </span>
          <span
            className={`ix-status-chip mono chrome-health-${platformHealth}`}
            data-testid="chrome-health-chip"
          >
            {platformHealth === "checking" && "PLATFORM: CHECKING…"}
            {platformHealth === "reachable" && "PLATFORM: REACHABLE"}
            {platformHealth === "unreachable" && "PLATFORM: UNREACHABLE"}
          </span>
          {clockUtc ? (
            <span className="ix-clock-badge mono" data-testid="shell-clock-badge">
              {clockUtc}
            </span>
          ) : null}
        </div>

        {/* Operator Controls & Command Palette Launcher */}
        <div className="ix-operator-controls">
          <WorkspaceSwitcher
            sections={navigationSections}
            activeWorkspaceId={activeWorkspace.id}
            recentWorkspaceIds={recentWorkspaceIds}
            onNavigate={navigateFromSwitcher}
          />
          <button
            type="button"
            className="ix-shell-button"
            onClick={overlay.openGlobalSearch}
            aria-haspopup="dialog"
            data-testid="shell-global-search-btn"
          >
            Global search
          </button>
          <button
            type="button"
            className="ix-shell-button command-palette-trigger"
            ref={commandTriggerRef}
            onClick={overlay.openCommandPalette}
            aria-haspopup="dialog"
            data-testid="shell-command-palette-btn"
          >
            Command palette <span className="ix-metadata mono">Ctrl K</span>
          </button>
          <button
            type="button"
            className="ix-shell-button"
            onClick={overlay.openSettings}
            aria-haspopup="dialog"
            data-testid="shell-settings-btn"
          >
            Settings
          </button>
          <button
            type="button"
            className="ix-shell-button theme-toggle-btn"
            onClick={overlay.toggleTheme}
            aria-label={`Cycle theme. Current theme: ${THEME_META[overlay.themeMode].label}.`}
            data-testid="shell-theme-toggle-btn"
            data-theme-id={overlay.themeMode}
          >
            Theme: {THEME_META[overlay.themeMode].label}
          </button>
          <span className="ix-metadata operator-tag mono" data-testid="shell-operator-name">
            {operator?.username ?? "operator"}
          </span>
          <button
            type="button"
            className="ix-shell-button sign-out-btn"
            onClick={() => void logout()}
            data-testid="shell-signout-btn"
          >
            Sign out
          </button>
        </div>
      </header>

      {/* Left Module Launcher Rail (B-CONV-1 / B-CONV-4; SURF-P02 alerts wiring) */}
      <UnifiedModuleRail
        collapsed={navigationCollapsed}
        onToggleCollapsed={() => setNavigationCollapsed((current) => !current)}
      />

      {/* Primary Workspace Content Stage */}
      <main
        id="main-content"
        className="ix-primary-workspace"
        role="main"
        aria-label="Primary workspace"
        tabIndex={-1}
        ref={workspaceRef}
        data-region="C"
        data-active-telemetry-id={activeWorkspace.telemetryId}
        data-testid="primary-workspace-stage"
      >
        <WorkspaceHost />
      </main>

      {/* Retired Legacy Chrome Containers (Maintained for accessibility landmark compatibility & isolated units) */}
      <div className="legacy-retired-chrome">
        <NavigationDock
          sections={navigationSections}
          collapsed={navigationCollapsed}
          onToggleCollapsed={() => setNavigationCollapsed((current) => !current)}
        />
        <aside
          className="ix-context-panel"
          role="complementary"
          aria-label="Context panel"
          tabIndex={-1}
          ref={contextRef}
          data-region="D"
        >
          <PanelHost
            category="context"
            activeWorkspace={activeWorkspace}
            layout={layout}
            setLayout={setLayout}
            store={layoutStore}
          />
        </aside>
        <section
          className="ix-activity-dock"
          role="region"
          aria-label="Activity dock"
          tabIndex={-1}
          ref={activityRef}
          data-region="E"
        >
          <div className="ix-activity-section">
            <h2 className="ix-panel-title">Activity telemetry</h2>
            <span className="ix-metadata">
              Last workspace activation: {activationEvent.telemetryId} · {activationEvent.type}
            </span>
          </div>
          <PanelHost
            category="activity"
            activeWorkspace={activeWorkspace}
            layout={layout}
            setLayout={setLayout}
            store={layoutStore}
          />
        </section>
      </div>

      {/* Global Command Palette & Overlay Modal Layer */}
      <OverlayLayer commands={commandRegistry} onNavigate={navigateCommand} />
    </div>
  );
}
