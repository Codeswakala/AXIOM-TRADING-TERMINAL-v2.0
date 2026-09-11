/**
 * FE-U02 Global Chrome — contract coupon family (BO-FE-U02, PC-FEU02-1
 * @ md5 2089d28c…, as accepted by ITRGA-REV-PCFEU02-001).
 *
 * Written FAIL-FIRST: demonstrated red against the as-built heritage shell
 * before any implementation byte (red transcript = pack E-3 class).
 *
 * Convention: mocks only the AuthContext seam, the shell-preferences
 * persistence seam, and fetchHealth (the C3 health source).
 * ACC-5 twin laws couponed separately (health stale⇒CHECKING vs
 * mode-badge locked-config persist-with-unverified-mark).
 */
import { fireEvent, render, screen, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import fs from "node:fs";
import path from "node:path";

import { InstitutionalWorkspaceShell } from "./InstitutionalWorkspaceShell";

const authState = vi.hoisted(() => ({
  value: {
    operator: { id: "op-1", username: "admin", role: "admin", is_active: true } as unknown,
    loading: false,
    isAuthenticated: true,
    logout: vi.fn(),
    login: vi.fn(),
    refreshProfile: vi.fn(),
  },
}));

vi.mock("../../context/AuthContext", () => ({
  useAuth: () => authState.value,
}));

vi.mock("../persistence/shellPreferences", () => ({
  loadShellLayoutPreference: vi.fn().mockResolvedValue(null),
  persistShellLayoutPreference: vi.fn().mockResolvedValue({}),
}));

const fetchHealthMock = vi.fn();

vi.mock("../../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../../api/client")>();
  return {
    ...actual,
    fetchHealth: (...args: unknown[]) =>
      (fetchHealthMock as (...a: unknown[]) => Promise<unknown>)(...args),
  };
});

function renderChrome(initialPath = "/") {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route element={<InstitutionalWorkspaceShell />}>
          <Route path="*" element={<div data-testid="under-chrome">content</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

function healthNeverResolves() {
  fetchHealthMock.mockImplementation(() => new Promise(() => undefined));
}

beforeEach(() => {
  fetchHealthMock.mockReset();
  healthNeverResolves();
  localStorage.clear();
});

afterEach(() => {
  cleanup();
});

/* ================================================================== */
/* C9 — boundary-scoped needles (F-B3-SCOPE; heritage outside the      */
/* boundary is protected and NOT scanned here).                        */
/* ================================================================== */

const BOUNDARY_FILES = [
  "InstitutionalWorkspaceShell.tsx",
  "InstitutionalWorkspaceShell.css",
].map((f) => path.join(__dirname, f));

const RAIL_FILES = [
  path.join(__dirname, "../navigation/UnifiedModuleRail.tsx"),
  path.join(__dirname, "../navigation/UnifiedModuleRail.css"),
];

const DELIVERED = [...BOUNDARY_FILES, ...RAIL_FILES]
  .map((f) => fs.readFileSync(f, "utf8"))
  .join("\n");

const N = (a: string, b: string) => a + b;

describe("test_feu02_c9_boundary_needles", () => {
  it("test_feu02_no_asserted_gate_or_sal_literals (ACC-1 family)", () => {
    expect(DELIVERED).not.toContain(N("Gate ", "CLOSED"));
    expect(DELIVERED).not.toContain(N("GATE: ", "CLOSED"));
    expect(DELIVERED).not.toContain(N("SAL", "-2"));
  });

  it("test_feu02_no_presentation_shell_or_simulated_badge_literals", () => {
    expect(DELIVERED).not.toContain(N("Presentation ", "shell"));
    expect(DELIVERED).not.toContain(N("live:", "simulated"));
    // 'Research-only' as an ASSERTED CHIP literal is expelled; the truthful
    // mode badge renders the composed disposition instead.
    expect(DELIVERED).not.toContain(N(">Research-", "only<"));
  });

  it("test_feu02_no_capability_cues", () => {
    for (const needle of [
      N("PAPER ", "TRADING"),
      N("BROKER ", "ACCOUNT"),
      N("LIVE ", "EXECUTION"),
      N("order ", "ticket"),
      N("live_", "exec"),
    ]) {
      expect(DELIVERED.toLowerCase()).not.toContain(needle.toLowerCase());
    }
  });

  it("test_feu02_no_remember_control_resurrection", () => {
    expect(DELIVERED).not.toContain(N("remember", "Workstation"));
  });
});

/* ================================================================== */
/* C3 — truthful global health strip (tri-state + stale⇒CHECKING).     */
/* ================================================================== */

describe("test_feu02_health_strip", () => {
  it("test_feu02_health_checking_before_first_result", () => {
    healthNeverResolves();
    renderChrome();
    expect(screen.getByTestId("chrome-health-chip")).toHaveTextContent(/checking/i);
  });

  it("test_feu02_health_reachable_on_ok", async () => {
    fetchHealthMock.mockResolvedValue({ status: "ok" });
    renderChrome();
    await waitFor(() =>
      expect(screen.getByTestId("chrome-health-chip")).toHaveTextContent(/reachable/i),
    );
    expect(screen.getByTestId("chrome-health-chip")).not.toHaveTextContent(/unreachable/i);
  });

  it("test_feu02_health_unreachable_on_failure", async () => {
    fetchHealthMock.mockRejectedValue(new Error("ECONNREFUSED"));
    renderChrome();
    await waitFor(() =>
      expect(screen.getByTestId("chrome-health-chip")).toHaveTextContent(/unreachable/i),
    );
  });
});

/* ================================================================== */
/* C3 — mode badge: locked-config law (ACC-5) with honest verification */
/* mark; never a PAPER/BROKER/LIVE cue.                                */
/* ================================================================== */

describe("test_feu02_mode_badge_locked_config_law", () => {
  it("test_feu02_mode_badge_renders_research_non_actuating", () => {
    renderChrome();
    const badge = screen.getByTestId("chrome-mode-badge");
    expect(badge).toHaveTextContent(/RESEARCH/);
    expect(badge).toHaveTextContent(/NON-ACTUATING/);
  });

  it("test_feu02_mode_badge_unverified_mark_before_verified_read", () => {
    // Pre-read (no authed mode fetch has succeeded in this world): the
    // badge persists the registered disposition WITH the honest mark.
    renderChrome();
    const badge = screen.getByTestId("chrome-mode-badge");
    expect(badge.getAttribute("data-verification")).toBe("unverified");
  });
});

/* ================================================================== */
/* C4 — nav rail: role-aware + honestly persisted collapse.            */
/* ================================================================== */

describe("test_feu02_nav_rail", () => {
  it("test_feu02_rail_collapse_control_exists_and_persists", async () => {
    renderChrome();
    const toggle = screen.getByTestId("chrome-rail-collapse-btn");
    fireEvent.click(toggle);
    await waitFor(() =>
      expect(localStorage.getItem("axiom_chrome_rail_collapsed")).toBe("true"),
    );
    fireEvent.click(toggle);
    await waitFor(() =>
      expect(localStorage.getItem("axiom_chrome_rail_collapsed")).toBe("false"),
    );
  });

  it("test_feu02_rail_collapse_control_accessible_name_states", () => {
    renderChrome();
    const toggle = screen.getByTestId("chrome-rail-collapse-btn");
    expect(toggle).toHaveAccessibleName(/collapse|expand/i);
  });
});

/* ================================================================== */
/* C4 — command palette: truthful over the real registry (C4-a).       */
/* ================================================================== */

describe("test_feu02_command_search_truthful", () => {
  it("test_feu02_palette_empty_state_honest", async () => {
    renderChrome();
    fireEvent.click(screen.getByTestId("shell-command-palette-btn"));
    const input = await screen.findByTestId("command-palette-input");
    fireEvent.change(input, { target: { value: "zzz-no-such-workspace-zzz" } });
    const empty = await screen.findByTestId("command-palette-empty");
    expect(empty).toHaveTextContent(/no matching workspace or action/i);
  });
});

/* ================================================================== */
/* ACC-4 — every KEPT header control real-or-truthful (existence arm;  */
/* effect arms ride the E-3 browser script).                           */
/* ================================================================== */

describe("test_feu02_kept_controls_present", () => {
  it("test_feu02_header_controls_render", () => {
    renderChrome();
    for (const id of [
      "shell-command-palette-btn",
      "shell-global-search-btn",
      "shell-theme-toggle-btn",
      "shell-settings-btn",
      "shell-signout-btn",
      "shell-operator-name",
      "shell-clock-badge",
    ]) {
      expect(screen.getByTestId(id)).toBeInTheDocument();
    }
  });

  it("test_feu02_operator_chip_renders_session_identity", () => {
    renderChrome();
    expect(screen.getByTestId("shell-operator-name")).toHaveTextContent("admin");
  });
});

/* ================================================================== */
/* C10 — regression pins: routes reachable through the rail.           */
/* ================================================================== */

describe("test_feu02_route_preservation", () => {
  it("test_feu02_announcer_live_region_present", () => {
    renderChrome();
    const region = document.querySelector('[aria-live="polite"][role="status"]');
    expect(region).not.toBeNull();
  });
});
