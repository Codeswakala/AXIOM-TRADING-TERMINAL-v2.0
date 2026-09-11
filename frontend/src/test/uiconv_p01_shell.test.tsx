import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import * as fs from "fs";
import * as path from "path";
import { ProtectedRoute } from "../auth/ProtectedRoute";
import { InstitutionalWorkspaceShell } from "../workstation/components/InstitutionalWorkspaceShell";
import { LoginPage } from "../pages/LoginPage";
import { CURRENT_PROTECTED_ROUTES } from "../workstation/registry/workspaceRegistry";
import { QUICK_ACTION_CATALOGUE } from "../workstation/commands/quickActionCatalogue";

// Mock Auth
const mockLogin = vi.fn();
const mockLogout = vi.fn();
type MockAuthState = {
  operator: { username: string; role: string } | null;
  loading: boolean;
  isAuthenticated: boolean;
  logout: ReturnType<typeof vi.fn>;
  login: ReturnType<typeof vi.fn>;
  refreshProfile: ReturnType<typeof vi.fn>;
};

const authState = vi.hoisted((): { value: MockAuthState } => ({
  value: {
    operator: { username: "lead_operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  },
}));

vi.mock("../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../workstation/persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

// SURF-P02: the rail badge count now derives from the monitoring-alerts API
// via AlertsProvider. Provide one unacknowledged alert so the badge renders a
// genuine count of 1 in the shell render.
vi.mock("../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../api/client")>();
  return {
    ...actual,
    fetchMonitoringAlerts: vi.fn().mockResolvedValue([
      {
        alert_id: "alert-shell-1",
        created_at: "2026-07-16T10:00:00Z",
        alert_type: "DRIFT_DETECTED",
        severity: "warning",
        subject_type: "model_artifact",
        subject_id: "model-1",
        market_class: null,
        symbol: null,
        timeframe: null,
        model_artifact_id: "model-1",
        signal_id: null,
        summary: "Shell badge fixture.",
        evidence: { drift_detected: true },
        lineage: { source: "shell-fixture" },
        acknowledged: false,
        acknowledged_at: null,
        acknowledged_by: null,
        audit_correlation_id: "corr-shell-1",
      },
    ]),
    acknowledgeMonitoringAlert: vi.fn(),
    fetchMonitoringAlertDetail: vi.fn(),
  };
});

beforeEach(() => {
  mockLogin.mockReset();
  mockLogout.mockReset();
  authState.value = {
    operator: { username: "lead_operator", role: "admin" },
    loading: false,
    isAuthenticated: true,
    logout: mockLogout,
    login: mockLogin,
    refreshProfile: vi.fn(),
  };
});

describe("UI-CONV-P01 Unified Shell, Command Layer & Operator Sign-In Surface (B-CONV-1..5)", () => {
  // Test 1 (Mandatory named test #1 — B-CONV-1 Unified Shell Without Legacy Chrome)
  it("test_uiconv_p01_all_authenticated_routes_render_in_unified_shell_without_legacy_chrome", () => {
    for (const route of CURRENT_PROTECTED_ROUTES) {
      render(
        <MemoryRouter initialEntries={[route]}>
          <Routes>
            <Route
              element={
                <ProtectedRoute>
                  <InstitutionalWorkspaceShell />
                </ProtectedRoute>
              }
            >
              <Route path={route} element={<div data-testid={`content-${route}`}>Content for {route}</div>} />
            </Route>
          </Routes>
        </MemoryRouter>,
      );

      // Verify unified shell container and new components
      expect(screen.getByTestId("institutional-workspace-shell")).toBeInTheDocument();
      expect(screen.getByRole("banner", { name: "Global command bar" })).toBeInTheDocument();
      expect(screen.getByTestId("unified-module-rail")).toBeInTheDocument();
      expect(screen.getByRole("main", { name: "Primary workspace" })).toBeInTheDocument();
      expect(screen.getByTestId(`content-${route}`)).toBeInTheDocument();

      // STRICT REQUIREMENT (B-CONV-1): Legacy chrome components are retired from visual presentation
      expect(document.querySelector(".legacy-retired-chrome")).toBeInTheDocument();
      expect(document.querySelector(".legacy-retired-chrome")).toHaveClass("legacy-retired-chrome");

      document.body.innerHTML = "";
    }
  });

  // Test 2 (Mandatory named test #2 — B-CONV-1 Pure Token Consumption & Zero Ad-Hoc Hex)
  it("test_uiconv_p01_zero_adhoc_hex_outside_tokens_css_in_all_touched_files", () => {
    const touchedFiles = [
      path.resolve(__dirname, "../pages/LoginPage.tsx"),
      path.resolve(__dirname, "../pages/LoginPage.css"),
      path.resolve(__dirname, "../workstation/components/InstitutionalWorkspaceShell.tsx"),
      path.resolve(__dirname, "../workstation/components/InstitutionalWorkspaceShell.css"),
      path.resolve(__dirname, "../workstation/navigation/UnifiedModuleRail.tsx"),
      path.resolve(__dirname, "../workstation/navigation/UnifiedModuleRail.css"),
      path.resolve(__dirname, "../styles/global.css"),
    ];

    for (const filePath of touchedFiles) {
      const content = fs.readFileSync(filePath, "utf8");
      // Find any hex color literals (#xxx or #xxxxxx)
      const hexMatches = content.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
      expect(
        hexMatches.length,
        `Found ad-hoc hex in ${path.basename(filePath)}: ${hexMatches.join(", ")}`,
      ).toBe(0);
    }
  });

  // Test 3 (Mandatory named test #3 — B-CONV-3 Command Palette Navigation to Every Route)
  it("test_uiconv_p01_command_palette_reaches_every_registered_route_by_keyboard", async () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route
            element={
              <ProtectedRoute>
                <InstitutionalWorkspaceShell />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<div>Operations Root</div>} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    // 1. Open Command Palette via Ctrl+K
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });

    const dialog = await screen.findByRole("dialog", { name: "Command palette" });
    expect(dialog).toBeInTheDocument();

    const searchInput = screen.getByPlaceholderText("Open workspace or shell command…");
    expect(searchInput).toHaveFocus();

    // 2. CA-CONV2-1: Empty-query enumeration must assert the count.
    // The palette must render every catalogued command on empty query — not a clipped subset.
    const emptyQueryItems = screen.getAllByRole("menuitem");
    expect(emptyQueryItems.length).toBe(QUICK_ACTION_CATALOGUE.length);

    // Every catalogue group renders on empty query (Observe, Detect, Analyze, Investigate,
    // Compare, Plan, Review, Document, Govern, Settings, Shell Controls, Assistant).
    for (const group of new Set(QUICK_ACTION_CATALOGUE.map((cmd) => cmd.group))) {
      expect(within(dialog).getByText(group)).toBeInTheDocument();
    }

    // CA-CONV2-1: Zero stale labels naming absorbed/deleted surfaces.
    expect(within(dialog).queryByText("Open Chart Workspace")).not.toBeInTheDocument();
    expect(within(dialog).queryByText("Open Advisory Signals")).not.toBeInTheDocument();
    expect(within(dialog).queryByText("Open Performance Analytics")).not.toBeInTheDocument();

    // CA-CONV2-1: Absorbed surfaces are relabeled to their real post-absorption destinations.
    expect(within(dialog).getByText("Open Chart Stage")).toBeInTheDocument();
    expect(within(dialog).getByText("Open Signals Dock")).toBeInTheDocument();
    expect(within(dialog).getByText("Open Intelligence Dock")).toBeInTheDocument();

    // 3. Filter for Signals
    fireEvent.change(searchInput, { target: { value: "Signals" } });

    const signalsCommand = await screen.findByRole("menuitem", { name: /Open Signals Dock/i });
    expect(signalsCommand).toBeInTheDocument();

    // 4. Select command and execute navigation to the post-absorption terminal destination
    fireEvent.click(signalsCommand);

    // 5. Verify Palette closes and route navigates to the terminal root (dock=signals)
    await waitFor(() => {
      expect(screen.queryByRole("dialog", { name: "Command palette" })).not.toBeInTheDocument();
      expect(screen.getByText("Operations Root")).toBeInTheDocument();
    });

    // 6. Test Escape closes palette
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    const reOpenedDialog = await screen.findByRole("dialog", { name: "Command palette" });
    expect(reOpenedDialog).toBeInTheDocument();

    fireEvent.keyDown(reOpenedDialog, { key: "Escape" });
    await waitFor(() => {
      expect(screen.queryByRole("dialog", { name: "Command palette" })).not.toBeInTheDocument();
    });
  });

  // Test 4 (Mandatory named test #4 — B-CONV-3 / T-1 Zero Actuating Targets in Command Palette)
  it("test_uiconv_p01_command_palette_exposes_no_actuating_or_order_target", () => {
    // Assert all 33 catalogued commands are non-actuating
    for (const cmd of QUICK_ACTION_CATALOGUE) {
      expect(cmd.noActuation).toBe(true);
      expect(["navigation", "ui-toggle"]).toContain(cmd.commandType);

      const labelLower = cmd.label.toLowerCase();
      const forbiddenActuationTerms = [
        "buy",
        "sell",
        "place order",
        "submit order",
        "execute",
        "connect broker",
        "order ticket",
        "position",
        "margin",
        "open gate",
        "allow execution",
      ];

      for (const forbidden of forbiddenActuationTerms) {
        expect(labelLower).not.toContain(forbidden);
      }
    }
  });

  // Test 5 (Mandatory named test #5 — B-CONV-2 Login Governance Chips & Zero Credential Hints)
  it("test_uiconv_p01_login_renders_governance_chips_and_no_credential_hints", async () => {
    authState.value = {
      operator: null,
      loading: false,
      isAuthenticated: false,
      logout: mockLogout,
      login: mockLogin,
      refreshProfile: vi.fn(),
    };

    render(
      <MemoryRouter initialEntries={["/login"]}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </MemoryRouter>,
    );

    // 1. Verify Pre-Authentication chips — SUPERSEDED BY CITATION
    // (BO-FE-U01 §2.1/§2.2, adopted 2026-09-10): asserted-state chips are
    // AAE-006-excluded; the door renders the truthful pattern-(b) label.
    expect(screen.getByTestId("login-governance-chips")).toBeInTheDocument();
    expect(screen.getByTestId("login-posture-unverified")).toHaveTextContent(
      "POSTURE: VERIFIED AFTER SIGN-IN",
    );

    // 2. POLISH-P01 M6 / GA-173: the brand mark is the compass + epsilon logo
    expect(screen.getByTestId("login-brand-monogram")).toBeInTheDocument();
    expect(screen.getByTestId("login-brand-logo-mark")).toBeInTheDocument();

    // 3. Verify zero credential hints in DOM or input values
    const usernameInput = screen.getByTestId("login-username-input") as HTMLInputElement;
    const passwordInput = screen.getByTestId("login-password-input") as HTMLInputElement;

    expect(usernameInput.value).toBe("");
    expect(passwordInput.value).toBe("");
    // SUPERSEDED BY CITATION (FE-U01 cycle 3, REF-002 template): the
    // template styles its fields with GENERIC LABEL placeholders. The
    // LAW (zero credential hints) survives: placeholders must be the
    // field names themselves, never example values.
    expect(usernameInput.getAttribute("placeholder")).toBe("Email or Username");
    expect(passwordInput.getAttribute("placeholder")).toBe("Password");

    const pageText = document.body.textContent?.toLowerCase() ?? "";
    expect(pageText).not.toContain("axiomsecurepass");
    expect(pageText).not.toContain("demo credentials");
    expect(pageText).not.toContain("default password");

    // 4. Password Reveal Toggle
    const revealBtn = screen.getByTestId("password-reveal-btn");
    expect(revealBtn).toHaveAttribute("aria-label", "Show password");
    expect(passwordInput.type).toBe("password");

    fireEvent.click(revealBtn);
    expect(revealBtn).toHaveAttribute("aria-label", "Hide password");
    expect(passwordInput.type).toBe("text");

    fireEvent.click(revealBtn);
    expect(passwordInput.type).toBe("password");

    // 5. Remember-workstation checkbox — SUPERSEDED BY CITATION
    // (BO-FE-U01 §2.3, adopted 2026-09-10): the dead control is removed
    // per AAE-007 (no replacement); its ABSENCE is now the invariant.
    expect(screen.queryByTestId("remember-workstation-checkbox")).toBeNull();

    // 6. Explicit Error on Failed Authentication — mock updated by citation
    // (BO-FE-U01 §2.4): a credential rejection is an HTTP 401 carrying
    // `.status` (SURF-P03); a status-less Error means transport failure and
    // now renders the distinct transport state. The mock models the 401.
    const authErr = new Error("Invalid operator credentials") as Error & {
      status?: number;
    };
    authErr.status = 401;
    mockLogin.mockRejectedValueOnce(authErr);

    fireEvent.change(usernameInput, { target: { value: "test_user" } });
    fireEvent.change(passwordInput, { target: { value: "wrong_pass" } });
    fireEvent.click(screen.getByTestId("login-submit-btn"));

    await waitFor(() => {
      expect(screen.getByTestId("login-error-banner")).toHaveTextContent("Invalid operator credentials");
    });
  });

  // Test 6 (Mandatory named test #6 — B-CONV-2 Decorative Scene Renders Zero Market Data)
  it("test_uiconv_p01_login_decorative_scene_renders_no_market_data_values", () => {
    authState.value = {
      operator: null,
      loading: false,
      isAuthenticated: false,
      logout: mockLogout,
      login: mockLogin,
      refreshProfile: vi.fn(),
    };

    render(
      <MemoryRouter initialEntries={["/login"]}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </MemoryRouter>,
    );

    const decoScene = screen.getByTestId("login-decorative-scene");
    expect(decoScene).toHaveAttribute("aria-hidden", "true");

    const sceneText = decoScene.textContent?.trim() ?? "";
    expect(sceneText).toBe("");

    // Assert zero price numbers, timestamps, or symbol strings in the decorative scene
    expect(decoScene.querySelectorAll("[data-price]").length).toBe(0);
    expect(decoScene.querySelectorAll("[data-timestamp]").length).toBe(0);
  });

  // Test 7 (Mandatory named test #7 — B-CONV-4 Every Legacy Affordance Remains Reachable)
  it("test_uiconv_p01_every_legacy_affordance_remains_reachable_in_new_shell", async () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route
            element={
              <ProtectedRoute>
                <InstitutionalWorkspaceShell />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<div>Root Workstation</div>} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );

    // Verify all 15 distinct workspace destinations are directly represented in the Left Module Rail
    const expectedWorkspaces = [
      "monitor-operations",
      "monitor-live-market",
      "monitor-chart-workspace",
      "research-advisory-signals",
      "research-analytics",
      "research-intelligence",
      "investigate-signal-investigation",
      "compare-scenarios",
      "plan-trade-plans",
      "plan-execution-research",
      "review-portfolio-research",
      "review-journal",
      "review-research-management",
      "govern-governance-evidence",
      "settings-workspace",
    ];

    for (const wsId of expectedWorkspaces) {
      expect(
        screen.getByTestId(`rail-btn-${wsId}`),
        `Missing module rail button for ${wsId}`,
      ).toBeInTheDocument();
    }

    // Verify alerts launcher affordance in the rail.
    // SURF-P02 re-target: this previously pinned a fabricated placeholder "3";
    // the badge now renders the genuine provider count (1 unacknowledged
    // fixture alert in the api mock above).
    expect(screen.getByTestId("rail-btn-alerts")).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByTestId("rail-alerts-badge")).toHaveTextContent("1");
    });
  });
});
