/**
 * FE-U01 Sign-In Surface — coupon family (BO-FE-U01, PC-FEU01-1).
 *
 * CORRECTIVE CYCLE 3 (REF-002 pixel-faithful rebuild, Operator instruction
 * 2026-09-10 "build the attached login page exactly as it is" + recorded
 * elections REF-002-E1/E2):
 *  - E1: the template's four auth affordances (Google sign-in, Forgot
 *    password?, Register, Remember me) are BUILT NOW — rendered per
 *    template; the three without backend flows answer with TRUTHFUL
 *    unavailability notices until their flows exist (findings FE0-BF-2/3/4);
 *    Remember me is FUNCTIONAL (session persistence election). This
 *    election supersedes the AAE-033…035 exclusions and their scan needles.
 *  - E2: hero rebuilt in code, value-free (no price/symbol strings).
 *
 * Standing laws still pinned: pattern-(b) posture + reachability chips,
 * C5 error typology (401 verbatim vs transport), redirect law, aria-hidden
 * value-free scene, reduced-motion freeze, zero credential hints.
 */
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import fs from "node:fs";
import path from "node:path";

import { LoginPage } from "./LoginPage";

const loginMock = vi.fn();

vi.mock("../context/AuthContext", () => ({
  useAuth: () => ({
    operator: null,
    loading: false,
    isAuthenticated: false,
    login: loginMock,
    logout: vi.fn(),
    refreshProfile: vi.fn(),
  }),
}));

const fetchHealthMock = vi.fn();

vi.mock("../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../api/client")>();
  return {
    ...actual,
    fetchHealth: (...args: unknown[]) =>
      (fetchHealthMock as (...a: unknown[]) => Promise<unknown>)(...args),
  };
});

const setTokenPersistenceMock = vi.fn();

vi.mock("../auth/tokenStorage", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../auth/tokenStorage")>();
  return {
    ...actual,
    setTokenPersistence: (...args: unknown[]) =>
      (setTokenPersistenceMock as (...a: unknown[]) => void)(...args),
  };
});

function renderDoor() {
  return render(
    <MemoryRouter initialEntries={["/login"]}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

function healthNeverResolves() {
  fetchHealthMock.mockImplementation(() => new Promise(() => undefined));
}

beforeEach(() => {
  loginMock.mockReset();
  fetchHealthMock.mockReset();
  setTokenPersistenceMock.mockReset();
  healthNeverResolves();
});

afterEach(() => {
  cleanup();
  vi.clearAllTimers();
  vi.useRealTimers();
});

/* ================================================================== */
/* C9 — prohibition needles (REF-002-E1: the SSO/reset/register/       */
/* remember needles are RETIRED BY ELECTION; the remaining needles     */
/* stay permanent).                                                    */
/* ================================================================== */

const PAGE_SRC = fs.readFileSync(path.join(__dirname, "LoginPage.tsx"), "utf8");
const CSS_SRC = fs.readFileSync(path.join(__dirname, "LoginPage.css"), "utf8");
const DELIVERED = PAGE_SRC + "\n" + CSS_SRC;

const N = (a: string, b: string) => a + b;

describe("test_feu01_c9_prohibition_needles", () => {
  it("test_feu01_no_hardcoded_gate_claim (AAE-006)", () => {
    expect(DELIVERED).not.toContain(N("GATE: ", "CLOSED"));
  });

  it("test_feu01_no_sal_claim_literal (AAE-006)", () => {
    expect(DELIVERED).not.toContain(N("SAL", "-2"));
    expect(DELIVERED.toLowerCase()).not.toContain(
      N("audit trail ", "active").toLowerCase(),
    );
  });

  it("test_feu01_no_hardcoded_posture_assertion (AAE-006)", () => {
    expect(DELIVERED).not.toContain(N("RESEARCH-ONLY · NON-", "ACTUATING"));
  });

  it("test_feu01_no_corridor_vocabulary_or_credential_hints", () => {
    const lower = DELIVERED.toLowerCase();
    for (const needle of [
      N("live_", "exec"),
      N("order ", "ticket"),
      N("execute ", "trade"),
      N("axiomsecure", "pass"),
      N("demo ", "credentials"),
      N("default ", "password"),
    ]) {
      expect(lower).not.toContain(needle);
    }
  });

  it("test_feu01_decorative_scene_value_free (REF-002-E2)", () => {
    renderDoor();
    const scene = screen.getByTestId("login-decorative-scene");
    expect(scene.getAttribute("aria-hidden")).toBe("true");
    expect(scene.textContent?.trim()).toBe("");
  });

  it("test_feu01_ref003_readouts_are_hidden_static_fiction (REF-003-E1)", () => {
    // Operator election REF-003-E1: the hero may carry the REF-003 image's
    // OWN placeholder values as STATIC FICTION. The witness: the layer is
    // aria-hidden, marked data-fictional, lives OUTSIDE the candle scene
    // subtree, and carries the image's frozen 2025 timestamp — provably
    // not live data.
    renderDoor();
    const readouts = screen.getByTestId("login-hero-readouts");
    expect(readouts.getAttribute("aria-hidden")).toBe("true");
    expect(readouts.getAttribute("data-fictional")).toBe("true");
    expect(readouts.textContent).toContain("2025-05-23 09:31:42 UTC");
    const scene = screen.getByTestId("login-decorative-scene");
    expect(scene.contains(readouts)).toBe(false);
  });
});

/* ================================================================== */
/* Truthful posture + reachability (pattern (b) — STILL PINNED).       */
/* ================================================================== */

describe("test_feu01_truthful_posture_pattern_b", () => {
  it("test_feu01_posture_label_verified_after_sign_in_renders", () => {
    renderDoor();
    expect(screen.getByTestId("login-posture-unverified")).toHaveTextContent(
      "POSTURE: VERIFIED AFTER SIGN-IN",
    );
  });

  it("test_feu01_reachability_checking_before_first_result", () => {
    healthNeverResolves();
    renderDoor();
    expect(screen.getByTestId("login-reachability-chip")).toHaveTextContent(/checking/i);
  });

  it("test_feu01_reachability_reachable_on_health_ok", async () => {
    fetchHealthMock.mockResolvedValue({ status: "ok" });
    renderDoor();
    await waitFor(() =>
      expect(screen.getByTestId("login-reachability-chip")).toHaveTextContent(/reachable/i),
    );
  });

  it("test_feu01_reachability_unreachable_on_health_failure", async () => {
    fetchHealthMock.mockRejectedValue(new Error("connect ECONNREFUSED"));
    renderDoor();
    await waitFor(() =>
      expect(screen.getByTestId("login-reachability-chip")).toHaveTextContent(/unreachable/i),
    );
  });
});

/* ================================================================== */
/* C5 — error typology (STILL PINNED).                                 */
/* ================================================================== */

describe("test_feu01_error_states_distinct", () => {
  function submit() {
    fireEvent.change(screen.getByTestId("login-username-input"), {
      target: { value: "operator" },
    });
    fireEvent.change(screen.getByTestId("login-password-input"), {
      target: { value: "pw" },
    });
    fireEvent.click(screen.getByTestId("login-submit-btn"));
  }

  it("test_feu01_401_detail_rendered_verbatim_role_alert", async () => {
    const detail = "Invalid username or password";
    const err = new Error(detail) as Error & { status?: number };
    err.status = 401;
    loginMock.mockRejectedValue(err);
    renderDoor();
    submit();
    const banner = await screen.findByTestId("login-error-banner");
    expect(banner).toHaveAttribute("role", "alert");
    expect(banner).toHaveTextContent(detail);
    expect(banner.getAttribute("data-error-kind")).toBe("credentials");
  });

  it("test_feu01_transport_failure_distinct_from_401", async () => {
    loginMock.mockRejectedValue(new Error("Request failed"));
    renderDoor();
    submit();
    const banner = await screen.findByTestId("login-error-banner");
    expect(banner.getAttribute("data-error-kind")).toBe("transport");
  });

  it("test_feu01_5xx_renders_transport_class_not_credentials", async () => {
    const err = new Error("Internal Server Error") as Error & { status?: number };
    err.status = 500;
    loginMock.mockRejectedValue(err);
    renderDoor();
    submit();
    const banner = await screen.findByTestId("login-error-banner");
    expect(banner.getAttribute("data-error-kind")).toBe("transport");
  });

  it("test_feu01_no_error_region_before_first_interaction", () => {
    renderDoor();
    expect(screen.queryByTestId("login-error-banner")).toBeNull();
  });
});

/* ================================================================== */
/* REF-002 form contract (labels per template; accessible names).      */
/* ================================================================== */

describe("test_feu01_ref002_form_contract", () => {
  it("test_feu01_email_or_username_and_password_fields_required", () => {
    renderDoor();
    const username = screen.getByLabelText(/email or username/i);
    const password = screen.getByLabelText(/^password$/i);
    expect(username).toBeRequired();
    expect(password).toBeRequired();
    expect(password).toHaveAttribute("type", "password");
  });

  it("test_feu01_password_reveal_accessible_name_swaps", () => {
    renderDoor();
    const toggle = screen.getByTestId("password-reveal-btn");
    expect(toggle).toHaveAccessibleName(/show password/i);
    fireEvent.click(toggle);
    expect(toggle).toHaveAccessibleName(/hide password/i);
    expect(screen.getByTestId("login-password-input")).toHaveAttribute("type", "text");
  });

  it("test_feu01_submit_disabled_while_submitting", async () => {
    let resolveLogin: () => void = () => undefined;
    loginMock.mockImplementation(
      () => new Promise<void>((resolve) => (resolveLogin = resolve)),
    );
    renderDoor();
    fireEvent.change(screen.getByTestId("login-username-input"), {
      target: { value: "operator" },
    });
    fireEvent.change(screen.getByTestId("login-password-input"), {
      target: { value: "pw" },
    });
    fireEvent.click(screen.getByTestId("login-submit-btn"));
    await waitFor(() => expect(screen.getByTestId("login-submit-btn")).toBeDisabled());
    resolveLogin();
  });
});

/* ================================================================== */
/* REF-002-E1 — the four affordances, BUILT NOW with truthful behavior */
/* ================================================================== */

describe("test_feu01_ref002_e1_affordances", () => {
  it("test_feu01_remember_me_present_and_controls_persistence", async () => {
    loginMock.mockResolvedValue(undefined);
    renderDoor();
    const remember = screen.getByTestId("remember-me-checkbox") as HTMLInputElement;
    expect(remember.checked).toBe(true); // template default: checked
    fireEvent.click(remember);
    expect(remember.checked).toBe(false);
    fireEvent.change(screen.getByTestId("login-username-input"), {
      target: { value: "operator" },
    });
    fireEvent.change(screen.getByTestId("login-password-input"), {
      target: { value: "pw" },
    });
    fireEvent.click(screen.getByTestId("login-submit-btn"));
    await waitFor(() => expect(loginMock).toHaveBeenCalled());
    // The election's functional wiring: persistence follows the checkbox.
    expect(setTokenPersistenceMock).toHaveBeenCalledWith(false);
  });

  it("test_feu01_forgot_password_present_answers_truthfully", async () => {
    renderDoor();
    fireEvent.click(screen.getByTestId("forgot-password-link"));
    const notice = await screen.findByTestId("login-affordance-notice");
    expect(notice).toHaveTextContent(/not yet provisioned|administrator/i);
  });

  it("test_feu01_google_signin_present_answers_truthfully", async () => {
    renderDoor();
    fireEvent.click(screen.getByTestId("google-signin-btn"));
    const notice = await screen.findByTestId("login-affordance-notice");
    expect(notice).toHaveTextContent(/not yet provisioned|operator credentials/i);
  });

  it("test_feu01_register_present_answers_truthfully", async () => {
    renderDoor();
    fireEvent.click(screen.getByTestId("register-link"));
    const notice = await screen.findByTestId("login-affordance-notice");
    expect(notice).toHaveTextContent(/provisioned by the platform administrator/i);
  });

  it("test_feu01_affordances_never_claim_success_or_navigate", () => {
    renderDoor();
    fireEvent.click(screen.getByTestId("google-signin-btn"));
    // Still at the door; no fabricated auth state.
    expect(screen.getByTestId("login-form")).toBeInTheDocument();
    expect(loginMock).not.toHaveBeenCalled();
  });
});

/* ================================================================== */
/* Redirect law + reduced motion (STILL PINNED).                       */
/* ================================================================== */

describe("test_feu01_redirect_and_motion_laws", () => {
  it("test_feu01_login_success_navigates_to_state_from", async () => {
    loginMock.mockResolvedValue(undefined);
    render(
      <MemoryRouter initialEntries={[{ pathname: "/login", state: { from: "/journal" } }]}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/journal" element={<div data-testid="journal-arrival">journal</div>} />
        </Routes>
      </MemoryRouter>,
    );
    fireEvent.change(screen.getByTestId("login-username-input"), {
      target: { value: "operator" },
    });
    fireEvent.change(screen.getByTestId("login-password-input"), {
      target: { value: "pw" },
    });
    fireEvent.click(screen.getByTestId("login-submit-btn"));
    await screen.findByTestId("journal-arrival");
  });

  it("test_feu01_reduced_motion_freeze_block_present", () => {
    expect(CSS_SRC).toMatch(/prefers-reduced-motion:\s*reduce/);
    const firstQuery = CSS_SRC.indexOf("@media (prefers-reduced-motion: reduce)");
    expect(firstQuery).toBeGreaterThan(-1);
    expect(CSS_SRC.slice(firstQuery)).toMatch(/animation:\s*none/);
  });
});
