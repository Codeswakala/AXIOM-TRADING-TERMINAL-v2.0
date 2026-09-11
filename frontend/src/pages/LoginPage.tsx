import { FormEvent, useEffect, useRef, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { fetchHealth } from "../api/client";
import { setTokenPersistence } from "../auth/tokenStorage";
import "./LoginPage.css";

/**
 * LoginPage — FE-U01 Sign-In Surface (corrective cycle 4).
 *
 * RIGHT CARD: REF-002 build, Operator-approved verbatim ("the right card
 * looks perfect") — UNTOUCHED this cycle.
 *
 * LEFT HERO: rebuilt to REF-003 (md5 a7ef8fe7f9b338b59126e2865be7f836) —
 * the blue holographic 3D terminal: wireframe AXIOM lockup, volumetric
 * candle field rising over a perspective grid, nebula glow, and the
 * image's terminal readouts.
 *
 * Recorded Operator election REF-003-E1 ("even if the placeholder values
 * were incorrect"): the decorative hero may carry the reference image's
 * OWN readout values as STATIC FICTION — frozen placeholder strings
 * (including its 2025-05-23 timestamp), aria-hidden, data-fictional,
 * never sourced from nor implying live data. The value-free law still
 * binds the candle scene itself; the readout layer is the elected
 * exception, coupon-pinned as hidden+fictional.
 *
 * All other laws carried unchanged: pattern-(b) posture + reachability
 * chips, C5 error typology, redirect law, REF-002-E1 affordances,
 * reduced-motion full freeze, transform/opacity-only motion.
 */

const HEALTH_POLL_MS = 30_000;

type Reachability = "checking" | "reachable" | "unreachable";
type ErrorKind = "credentials" | "transport";

/** Holographic candle field silhouettes (decorative layout constants):
 *  [height(px), lift(px), hollow?] — traces REF-003's dip-and-rally arc. */
const HOLO_CANDLES: Array<[number, number, boolean]> = [
  [92, 44, false],
  [64, 30, true],
  [118, 60, false],
  [76, 26, false],
  [140, 78, true],
  [96, 40, false],
  [70, 18, true],
  [54, 8, false],
  [88, 26, false],
  [122, 58, false],
  [86, 34, true],
  [150, 92, false],
  [110, 64, false],
  [178, 118, true],
  [136, 96, false],
  [206, 148, false],
  [164, 126, true],
  [238, 178, false],
];

export function LoginPage() {
  const { login, isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: string } | null)?.from ?? "/";

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [errorKind, setErrorKind] = useState<ErrorKind>("transport");
  const [notice, setNotice] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [reachability, setReachability] = useState<Reachability>("checking");
  const pollGeneration = useRef(0);

  useEffect(() => {
    let disposed = false;

    async function probe() {
      const generation = ++pollGeneration.current;
      setReachability("checking");
      try {
        await fetchHealth();
        if (!disposed && pollGeneration.current === generation) {
          setReachability("reachable");
        }
      } catch {
        if (!disposed && pollGeneration.current === generation) {
          setReachability("unreachable");
        }
      }
    }

    void probe();
    const timer = window.setInterval(() => void probe(), HEALTH_POLL_MS);
    return () => {
      disposed = true;
      window.clearInterval(timer);
    };
  }, []);

  if (!loading && isAuthenticated) {
    return <Navigate to={from} replace />;
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setNotice(null);
    setSubmitting(true);
    setTokenPersistence(rememberMe);
    try {
      await login(username, password);
      navigate(from, { replace: true });
    } catch (err) {
      const status = (err as Error & { status?: number }).status;
      if (status === 401) {
        setErrorKind("credentials");
        setError(err instanceof Error ? err.message : "Authentication refused");
      } else {
        setErrorKind("transport");
        setError(
          "The platform could not be reached to verify your credentials. " +
            "This is a transport failure, not a credential rejection.",
        );
      }
    } finally {
      setSubmitting(false);
    }
  }

  function onForgotPassword() {
    setError(null);
    setNotice(
      "Password recovery is not yet provisioned on this platform. " +
        "Contact your platform administrator to reset your operator credentials.",
    );
  }

  function onGoogleSignIn() {
    setError(null);
    setNotice(
      "Google sign-in is not yet provisioned on this platform. " +
        "Use your operator credentials above.",
    );
  }

  function onRegister() {
    setError(null);
    setNotice(
      "Accounts are provisioned by the platform administrator. " +
        "Self-registration is not yet available.",
    );
  }

  return (
    <div className="login-page-container" data-testid="login-page-container">
      {/* ========= LEFT HERO — REF-003 holographic terminal (cycle 4) ========= */}
      <section className="hero-panel" aria-label="AXIOM Institutional Overview" data-testid="login-hero-pane">
        {/* 3D scene (value-free; the candle field carries no text). */}
        <div className="login-decorative-scene" aria-hidden="true" data-testid="login-decorative-scene">
          <div className="scene-nebula" />
          <div className="scene-bokeh bokeh-1" />
          <div className="scene-bokeh bokeh-2" />
          <div className="scene-back-grid" />
          <div className="scene-floor-grid" />
          <div className="login-glow-pulse" data-testid="login-glow-pulse" />
          <div className="holo-field" data-testid="login-wave-field">
            {HOLO_CANDLES.map(([h, lift, hollow], index) => (
              <div
                key={`holo-${index}`}
                className={`deco-candle holo-candle ${hollow ? "hollow" : "solid"} holo-c${index % 6}`}
                style={{ height: `${h}px`, marginBottom: `${lift}px` }}
              />
            ))}
          </div>
          <div className="scene-scanline" />
        </div>

        {/* Terminal readouts — STATIC FICTION per REF-003-E1 (Operator
            election): the reference image's own placeholder values, frozen
            (note the fictional 2025 timestamp), aria-hidden, decorative. */}
        <div
          className="hero-readouts"
          aria-hidden="true"
          data-fictional="true"
          data-testid="login-hero-readouts"
        >
          <div className="readout readout-tickers">
            <div className="ticker-row"><span className="tick-sym">ESMS</span><span className="tick-val">5,272.25</span></div>
            <div className="ticker-row"><span className="tick-sym">NQMS</span><span className="tick-val">18,612.75</span></div>
            <div className="ticker-row"><span className="tick-sym">YMMS</span><span className="tick-val">39,812.00</span></div>
            <div className="ticker-row"><span className="tick-sym">CLMS</span><span className="tick-val">77.32</span></div>
            <div className="ticker-row"><span className="tick-sym">GCQS</span><span className="tick-val">2,402.60</span></div>
            <div className="ticker-row ticker-delta"><span className="tick-val">+0.82%</span></div>
          </div>
          <div className="readout readout-feed">
            <div className="feed-row"><span className="feed-key">DATA FEED</span><span className="feed-val feed-live">LIVE</span></div>
            <div className="feed-row"><span className="feed-key">LATENCY</span><span className="feed-val">01.2ms</span></div>
            <div className="feed-row"><span className="feed-key">TIMESTAMP</span><span className="feed-val">2025-05-23 09:31:42 UTC</span></div>
            <div className="feed-row"><span className="feed-key">SESSION</span><span className="feed-val">NEW YORK</span></div>
          </div>
          <div className="readout readout-stats">
            <div className="feed-row"><span className="feed-key">VOL</span><span className="feed-val">1.28</span></div>
            <div className="feed-row"><span className="feed-key">DVOL</span><span className="feed-val">687.3M</span></div>
            <div className="feed-row"><span className="feed-key">ADV</span><span className="feed-val">2,152</span></div>
            <div className="feed-row"><span className="feed-key">DEC</span><span className="feed-val">1,847</span></div>
            <div className="feed-row"><span className="feed-key">UNCH</span><span className="feed-val">186</span></div>
          </div>
        </div>

        {/* Wireframe brand lockup (REF-003 top-left). */}
        <div className="hero-lockup" data-testid="login-hero-lockup">
          <span className="wire-mark" data-testid="login-brand-monogram" aria-hidden="true">
            <svg viewBox="0 0 64 60" width="72" height="68" data-testid="login-brand-logo-mark" role="img" aria-label="AXIOM logo">
              <g fill="none" stroke="rgba(226, 232, 240, 0.92)" strokeWidth="1.6" strokeLinejoin="round">
                <path d="M32 6 L54 52 H44 L32 26 L20 52 H10 Z" />
                <path d="M36 38 L46 52 H38 L32 42 Z" opacity="0.85" />
              </g>
            </svg>
          </span>
          <span className="wire-word">AXIOM</span>
          <span className="wire-sub">INSTITUTIONAL RESEARCH TERMINAL</span>
        </div>
      </section>

      {/* ============ RIGHT PANEL — the sign-in card (APPROVED; untouched) ======== */}
      <section className="auth-panel" aria-label="Operator Authentication Form" data-testid="login-form-pane">
        <div className="auth-card" data-testid="login-auth-card">
          <div className="auth-lockup">
            <span className="lockup-mark lockup-mark-lg" aria-hidden="true">
              <svg viewBox="0 0 48 44" width="52" height="48">
                <defs>
                  <linearGradient id="axg2" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0" stopColor="var(--ix-color-success-green)" />
                    <stop offset="1" stopColor="var(--ix-color-electric-blue)" />
                  </linearGradient>
                </defs>
                <path d="M24 2 L44 42 H36 L24 18 L12 42 H4 Z" fill="url(#axg2)" />
                <path d="M24 26 L30 38 H18 Z" fill="url(#axg2)" opacity="0.75" />
              </svg>
            </span>
            <span className="lockup-words">
              <strong>AXIOM</strong>
              <em>RESEARCH TERMINAL</em>
            </span>
          </div>

          <div
            className="auth-status-line"
            role="status"
            aria-label="Pre-authentication status: platform posture is verified after sign-in"
            data-testid="login-governance-chips"
          >
            <span className="gov-pill-unverified" data-testid="login-posture-unverified">
              POSTURE: VERIFIED AFTER SIGN-IN
            </span>
            <span className="chip-sep" aria-hidden="true">·</span>
            <span
              className={`reachability-chip reachability-${reachability}`}
              data-testid="login-reachability-chip"
            >
              {reachability === "checking" && "PLATFORM: CHECKING…"}
              {reachability === "reachable" && "PLATFORM: REACHABLE"}
              {reachability === "unreachable" && "PLATFORM: UNREACHABLE"}
            </span>
          </div>

          <div className="auth-head">
            <h2 className="auth-title">Welcome Back</h2>
            <p className="auth-sub">Sign in to your account to continue your research.</p>
          </div>

          {error ? (
            <div
              className={`auth-alert auth-alert-${errorKind} login-error-banner`}
              role="alert"
              data-error-kind={errorKind}
              data-testid="login-error-banner"
            >
              <span aria-hidden="true">⚠</span>
              <span>{error}</span>
            </div>
          ) : null}

          {notice ? (
            <div className="auth-notice" role="status" data-testid="login-affordance-notice">
              <span aria-hidden="true">ℹ</span>
              <span>{notice}</span>
            </div>
          ) : null}

          <form className="auth-form" onSubmit={onSubmit} data-testid="login-form">
            <label className="sr-only" htmlFor="username-input">
              Email or Username
            </label>
            <div className="field-shell">
              <span className="field-icon" aria-hidden="true">
                <svg viewBox="0 0 20 20" width="17" height="17"><circle cx="10" cy="6.5" r="3.5" fill="none" stroke="currentColor" strokeWidth="1.5"/><path d="M3 17.5 c1.5 -4 12.5 -4 14 0" fill="none" stroke="currentColor" strokeWidth="1.5"/></svg>
              </span>
              <input
                id="username-input"
                className="field-input"
                type="text"
                placeholder="Email or Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
                required
                data-testid="login-username-input"
              />
            </div>

            <label className="sr-only" htmlFor="password-input">
              Password
            </label>
            <div className="field-shell">
              <span className="field-icon" aria-hidden="true">
                <svg viewBox="0 0 20 20" width="17" height="17"><rect x="4" y="9" width="12" height="8" rx="1.5" fill="none" stroke="currentColor" strokeWidth="1.5"/><path d="M7 9 V6.5 a3 3 0 0 1 6 0 V9" fill="none" stroke="currentColor" strokeWidth="1.5"/></svg>
              </span>
              <input
                id="password-input"
                className="field-input"
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                required
                data-testid="login-password-input"
              />
              <button
                type="button"
                className="field-reveal"
                onClick={() => setShowPassword((prev) => !prev)}
                aria-label={showPassword ? "Hide password" : "Show password"}
                data-testid="password-reveal-btn"
              >
                <svg viewBox="0 0 20 20" width="17" height="17" aria-hidden="true">
                  <path d="M2 10 c2.5 -4.5 13.5 -4.5 16 0 c-2.5 4.5 -13.5 4.5 -16 0 Z" fill="none" stroke="currentColor" strokeWidth="1.5" />
                  <circle cx="10" cy="10" r="2.4" fill="none" stroke="currentColor" strokeWidth="1.5" />
                  {showPassword ? <line x1="4" y1="16" x2="16" y2="4" stroke="currentColor" strokeWidth="1.5" /> : null}
                </svg>
              </button>
            </div>

            <div className="auth-options-row">
              <label className="remember-label">
                <input
                  type="checkbox"
                  className="remember-box"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  data-testid="remember-me-checkbox"
                />
                <span>Remember me</span>
              </label>
              <button
                type="button"
                className="forgot-link"
                onClick={onForgotPassword}
                data-testid="forgot-password-link"
              >
                Forgot password?
              </button>
            </div>

            <button
              className="auth-submit"
              type="submit"
              disabled={submitting}
              data-testid="login-submit-btn"
            >
              {submitting ? "Signing in…" : "Sign In"}
              <span className="submit-arrow" aria-hidden="true">→</span>
            </button>
          </form>

          <div className="auth-divider" aria-hidden="true">
            <span className="divider-rule" />
            <span className="divider-word">OR</span>
            <span className="divider-rule" />
          </div>

          <button
            type="button"
            className="google-btn"
            onClick={onGoogleSignIn}
            data-testid="google-signin-btn"
          >
            <span className="google-mark" aria-hidden="true">
              <svg viewBox="0 0 24 24" width="18" height="18">
                <path d="M23.5 12.27 c0 -0.85 -0.08 -1.66 -0.22 -2.45 H12 v4.64 h6.45 a5.52 5.52 0 0 1 -2.39 3.62 v3 h3.87 c2.26 -2.09 3.57 -5.16 3.57 -8.81 Z" fill="rgb(66,133,244)" />
                <path d="M12 24 c3.24 0 5.96 -1.07 7.93 -2.92 l-3.87 -3 c-1.07 0.72 -2.45 1.15 -4.06 1.15 -3.13 0 -5.78 -2.11 -6.73 -4.96 H1.29 v3.09 A12 12 0 0 0 12 24 Z" fill="rgb(52,168,83)" />
                <path d="M5.27 14.27 a7.22 7.22 0 0 1 0 -4.54 V6.64 H1.29 a12 12 0 0 0 0 10.72 Z" fill="rgb(251,188,5)" />
                <path d="M12 4.77 c1.76 0 3.35 0.61 4.6 1.8 l3.43 -3.43 A11.98 11.98 0 0 0 1.29 6.64 l3.98 3.09 C6.22 6.88 8.87 4.77 12 4.77 Z" fill="rgb(234,67,53)" />
              </svg>
            </span>
            Continue with Google
          </button>

          <div className="auth-register-row">
            <span>Don't have an account?</span>
            <button
              type="button"
              className="register-link"
              onClick={onRegister}
              data-testid="register-link"
            >
              Register
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
