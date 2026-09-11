import { render, screen, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "../auth/ProtectedRoute";
import { WorkspaceCustomizationWorkspace } from "./WorkspaceCustomizationPage";
import type { OperatorWorkspacePreference } from "../api/client";

vi.mock("../context/AuthContext", () => ({
  useAuth: () => ({
    operator: null,
    loading: false,
    isAuthenticated: false,
    login: vi.fn(),
    logout: vi.fn(),
    refreshProfile: vi.fn(),
  }),
}));

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

describe("WorkspaceCustomizationWorkspace", () => {
  it("renders and applies operator preferences", () => {
    const onCreatePreference = vi.fn();
    const onUpdatePreference = vi.fn();
    render(
      <WorkspaceCustomizationWorkspace
        preferences={[preference()]}
        onCreatePreference={onCreatePreference}
        onUpdatePreference={onUpdatePreference}
      />,
    );

    expect(screen.getByText("Workspace Customization")).toBeInTheDocument();
    expect(screen.getByText("Presentation preferences only.")).toBeInTheDocument();
    const detail = screen.getByLabelText("Workspace preference detail");
    expect(within(detail).getByText("default")).toBeInTheDocument();
    expect(within(detail).getByText(/operations, execution_research/)).toBeInTheDocument();

    screen.getByText("Save preferences").click();
    expect(onCreatePreference).toHaveBeenCalledTimes(1);
    screen.getByText("Update selected preferences").click();
    expect(onUpdatePreference).toHaveBeenCalledTimes(1);
  });

  it("exposes no execution, order, or account controls", () => {
    render(<WorkspaceCustomizationWorkspace preferences={[preference()]} />);

    const buttonText = screen
      .getAllByRole("button")
      .map((button) => button.textContent?.toLowerCase() ?? "")
      .join(" ");
    const forbidden = ["b" + "uy", "s" + "ell", "submit", "exec" + "ute", "go live"];
    for (const word of forbidden) {
      expect(buttonText).not.toContain(word);
    }

    const editor = screen.getByLabelText("Workspace preference editor");
    expect(within(editor).queryByLabelText(/order/i)).not.toBeInTheDocument();
    expect(within(editor).queryByLabelText(/broker/i)).not.toBeInTheDocument();
    expect(within(editor).queryByLabelText(/account/i)).not.toBeInTheDocument();
  });

  it("requires auth and blocks logged-out access", () => {
    render(
      <MemoryRouter initialEntries={["/workspace"]}>
        <Routes>
          <Route path="/login" element={<div>Operator login required</div>} />
          <Route
            path="/workspace"
            element={
              <ProtectedRoute>
                <WorkspaceCustomizationWorkspace preferences={[preference()]} />
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Operator login required")).toBeInTheDocument();
    expect(screen.queryByText("Workspace Customization")).not.toBeInTheDocument();
  });
});
