import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { InstitutionalWorkspaceShell } from "../components/InstitutionalWorkspaceShell";
import { ProtectedRoute } from "../../auth/ProtectedRoute";
import { InstitutionalIntelligenceWorkspace } from "../../pages/InstitutionalIntelligencePage";
import { ProfessionalMarketOverview } from "../../components/chart/ChartWorkspaceSurface";
import { SignalInvestigationFrame } from "../../components/terminal/signals/SignalInvestigationRecords";
import { PanelHeader } from "../../components/ui/PanelHeader";

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

function renderShellWithContent(content: React.ReactNode, path = "/") {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route
          element={
            <ProtectedRoute>
              <InstitutionalWorkspaceShell />
            </ProtectedRoute>
          }
        >
          <Route path={path} element={<div>{content}</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

describe("UI-010-P01 Semantic Accessibility Audit Harness (T-2, T-3, T-4, AC-2, AC-3)", () => {
  // T-2 / AC-2: Landmark Completeness
  it("T-2 / AC-2: verifies landmark completeness across workstation shell (banner, navigation, main, complementary, region)", () => {
    renderShellWithContent(<h1>Semantic Audit Main</h1>);

    // Banner (Region A)
    const banner = screen.getByRole("banner", { name: /Global command bar/i });
    expect(banner).toBeInTheDocument();

    // Primary Navigation (Region B)
    const nav = screen.getByRole("navigation", { name: /Institutional workflow navigation/i });
    expect(nav).toBeInTheDocument();

    // Primary Main (Region C)
    const main = screen.getByRole("main");
    expect(main).toBeInTheDocument();
    expect(main).toHaveAttribute("id", "main-content");

    // Context Panel (Region D)
    const context = screen.getByRole("complementary", { name: /Context panel/i });
    expect(context).toBeInTheDocument();

    // Activity Dock (Region E)
    const activity = screen.getByRole("region", { name: /Activity dock/i });
    expect(activity).toBeInTheDocument();

    // SkipLink existence inside banner
    const skipLink = screen.getByRole("link", { name: /Skip to main content/i });
    expect(skipLink).toBeInTheDocument();
    expect(skipLink).toHaveAttribute("href", "#main-content");
  });

  // T-3 / AC-3: Heading Hierarchy Unbroken
  it("T-3 / AC-3: verifies heading hierarchy structure across representative workspace components", () => {
    // 1. Institutional Intelligence headings
    const { container: c1 } = render(
      <div>
        <InstitutionalIntelligenceWorkspace bundle={null} />
      </div>,
    );
    const h1List1 = c1.querySelectorAll("h1");
    const h2List1 = c1.querySelectorAll("h2");
    expect(h1List1.length).toBeGreaterThanOrEqual(1);
    expect(h2List1.length).toBeGreaterThanOrEqual(1);

    // 2. Professional Market Overview headings
    const { container: c2 } = render(
      <ProfessionalMarketOverview
        symbol="EURUSD"
        timeframe="M1"
        chartType="candlestick"
        barCount={100}
        connectionState="connected"
        feedRunning={true}
        lastLiveAt="2026-08-11T10:00:00Z"
        sourceSummary="seed:synthetic"
      />,
    );
    const h2List2 = c2.querySelectorAll("h2");
    expect(h2List2.length).toBeGreaterThanOrEqual(1);

    // 3. Signal Investigation headings
    const { container: c3 } = render(
      <SignalInvestigationFrame />,
    );
    const h1List3 = c3.querySelectorAll("h1");
    const h2List3 = c3.querySelectorAll("h2");
    expect(h1List3.length).toBeGreaterThanOrEqual(1);
    expect(h2List3.length).toBeGreaterThanOrEqual(1);

    // 4. PanelHeader semantic levels
    render(
      <div>
        <PanelHeader title="Level 2 Title" headingLevel={2} titleId="h2-id" />
        <PanelHeader title="Level 3 Subtitle" headingLevel={3} titleId="h3-id" />
      </div>,
    );
    expect(screen.getByRole("heading", { level: 2, name: /Level 2 Title/i })).toHaveAttribute("id", "h2-id");
    expect(screen.getByRole("heading", { level: 3, name: /Level 3 Subtitle/i })).toHaveAttribute("id", "h3-id");
  });

  // T-4: Interactive Element Focusability
  it("T-4: verifies all interactive controls in shell header and navigation are keyboard focusable", () => {
    renderShellWithContent(<p>Focus test content</p>);

    const buttons = screen.getAllByRole("button");
    for (const btn of buttons) {
      if (!btn.hasAttribute("disabled") && !btn.getAttribute("aria-hidden")) {
        expect(btn.tabIndex).toBeGreaterThanOrEqual(0);
      }
    }

    const links = screen.getAllByRole("link");
    for (const link of links) {
      expect(link.tabIndex).toBeGreaterThanOrEqual(0);
    }
  });
});
