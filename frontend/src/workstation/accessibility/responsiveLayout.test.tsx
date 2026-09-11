import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { ProtectedRoute } from "../../auth/ProtectedRoute";

const authState = vi.hoisted(() => ({
  value: {
    operator: { username: "operator", role: "admin" },
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

function renderShell() {
  return render(
    <MemoryRouter initialEntries={["/"]}>
      <Routes>
        <Route
          element={
            <ProtectedRoute>
              <InstitutionalWorkspaceShell />
            </ProtectedRoute>
          }
        >
          <Route path="/" element={<h1>Responsive Shell Test</h1>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("UI-010-P02 Responsive Layout Adaptivity & Panel Collapsing (T-2, AC-2, U-3)", () => {
  it("AC-2: renders collapsible navigation toggle and preserves keyboard focusability", () => {
    renderShell();

    const toggleBtn = screen.getByRole("button", { name: /Collapse navigation/i });
    expect(toggleBtn).toBeInTheDocument();
    expect(toggleBtn.tabIndex).toBeGreaterThanOrEqual(0);

    const shell = screen.getByTestId("institutional-workspace-shell");
    expect(shell.className).not.toContain("nav-collapsed");

    // Click collapse toggle
    fireEvent.click(toggleBtn);
    expect(shell.className).toContain("nav-collapsed");

    // Click again to expand
    fireEvent.click(toggleBtn);
    expect(shell.className).not.toContain("nav-collapsed");
  });

  it("AC-2: maintains main workspace and context landmark visibility during adaptive reflow", () => {
    renderShell();

    expect(screen.getByRole("main")).toHaveAttribute("id", "main-content");
    expect(screen.getByRole("complementary", { name: /Context panel/i })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: /Activity dock/i })).toBeInTheDocument();
  });
});
