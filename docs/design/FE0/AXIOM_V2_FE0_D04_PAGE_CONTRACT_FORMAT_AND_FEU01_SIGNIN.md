# FE-0 / D0-4 — Page Contract Format + FE-U01 Sign-In Page Contract (Complete)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE0-D04-001 |
| Parent | AXIOM-V2-FE0-DESIGN-PLAN-001 (under AXIOM-V2-DPR-001) |
| Author | DA · 2026-09-10 |
| Scope law (DPR §3.5) | The FORMAT (Part I) + the FE-U01 contract (Part II) ONLY. No other unit's contract is written here; each arrives inside its own loop |
| Authority | This contract AUTHORIZES NOTHING. It is the drafting source for the future `BO-FE-U01`; implementation waits for that BO's adoption |

---

# PART I — THE PAGE CONTRACT FORMAT (PCF-1)

Every unit's contract carries exactly these twelve sections, in order. A BO pins the
contract by hash; the evidence pack proves each section's clauses; ITRGA determines on the
same pack (§A.3/§A.4).

| § | Section | Content law |
|---|---|---|
| C1 | Identity | Unit id, route(s)/panel family owned, the ONE surface (§A.1); everything else is out of scope by construction |
| C2 | Purpose + AXIOM identity expression | What the surface is for; which identity/brand elements appear (token-cited) |
| C3 | Backend truth sources | Every backend fact consumed: endpoint, auth requirement, the exact field(s), and the render rule. **A rendered claim with no row in this table is a defect (fabricated state)** |
| C4 | Surface anatomy | Regions/components, with Adopt/Adapt/Exclude citations (D0-2 entry ids) |
| C5 | State matrix | loading / empty / error / denied / stale / degraded / unknown — for EVERY C3 source; each cell names its distinct visible render. Cells may be marked N/A only with a reason |
| C6 | Interaction script | Numbered, deterministic, replayable steps (the evidence pack's capture script IS this script) |
| C7 | Viewport pins | 1440×900 desktop + 390×844 narrow (U3 §A.4 default) unless the unit's BO amends; per-viewport layout deltas named |
| C8 | Accessibility contract | Keyboard paths, focus order, screen-reader announcements (verbatim strings), contrast (AA), reduced-motion behavior |
| C9 | Prohibitions + scan needles | Unit-scoped forbidden vocabulary/behaviors AND the literal scan needles the evidence pack greps — scans are executable, not aspirational |
| C10 | V1 regression scope | Which existing routes/tests must remain green; the unit's regression evidence list |
| C11 | Security & secrets | Token handling, no provider/broker/AI secrets in browser code (§B.5), storage semantics |
| C12 | Findings & debts | Pre-existing debt touched or deliberately not touched (D0-1 finding ids), plus new findings for future BOs |

---

# PART II — FE-U01 SIGN-IN PAGE CONTRACT (PC-FEU01-1)

## C1. Identity
- Unit **FE-U01**; owns exactly ONE surface: route `/login` (`LoginPage` family incl. its CSS and the auth session seam it triggers). Nothing else rendered, restyled, or touched. The post-login redirect target is consumed, not owned.

## C2. Purpose + AXIOM identity expression
- The terminal's door: authenticate an operator against the real backend auth service and truthfully present the platform's identity and governance posture before any session exists.
- Identity: AXIOM logomark (AAE-020), brand palette and typography via `--ix-*` tokens only (AAE-001). No vendor claims, no certifications, no market values (§B.9).

## C3. Backend truth sources

| Fact | Source | Auth | Render rule |
|---|---|---|---|
| Authentication | `POST /api/v1/auth/login` (username 1–64, password 1–128) | none | 200 → tokens + operator; 401 → render `detail` verbatim in the error region; network failure → distinct transport-error state (not the same render as 401) |
| Session restore | `GET /api/v1/operator/me` | Bearer | Existing-token boot path; failure clears tokens, stays at door |
| Platform reachability | `GET /health` (unauthenticated, exists today) | none | Powers the door's honest reachability chip: reachable / unreachable / checking |
| Governance posture at the door | **NO unauthenticated posture source exists** (D0-1 F-1: `/api/v1/v2/mode` is authed) | — | **THE TRUTHFUL-POSTURE PATTERN (binding):** pre-auth posture chips may render ONLY (a) facts from an unauthenticated endpoint, or (b) the explicit label `POSTURE: VERIFIED AFTER SIGN-IN` (styled as unverified/neutral, never as an asserted state). Hardcoded `GATE: CLOSED` / `SAL-2 …` claims are EXCLUDED (AAE-006). If the Operator wants asserted pre-auth posture, that is backend finding **FE0-BF-1** (public read-only posture fact endpoint) for a future backend BO — not a frontend invention |

## C4. Surface anatomy (Adopt/Adapt/Exclude cited)
- **Hero pane** (ADAPT, AAE-005/AAE-008): AXIOM monogram + titles; decorative scene permitted only value-free (no real/realistic symbols, quotes, levels, P&L; `aria-hidden`; fully static under reduced motion); posture chips per C3 pattern; principle quote allowed (brand text, not a state claim).
- **Form pane** (ADAPT, AAE-005): title; username + password fields (backend contract only); password reveal toggle (accessible name swaps Hide/Show); submit; error region; footer limited to truthful text (platform-name/mode-agnostic; the SAL-2/audit-trail literal is EXCLUDED with AAE-006 unless backend-sourced).
- **REMOVED:** `rememberWorkstation` checkbox (AAE-007) — no invented persistence semantics.
- **ABSENT by law:** SSO buttons, password-reset/"forgot password" links, sign-up, MFA affordances — the backend supports none of these (ruling §2; §B.9). Scan-enforced (C9).

## C5. State matrix (per source)

| State | Login POST | Session restore | Reachability | Posture chips |
|---|---|---|---|---|
| loading | submit disabled + "Signing in…" | full-door "Checking operator session…" | "checking" chip | render as VERIFIED-AFTER-SIGN-IN (never blank-then-claim) |
| empty | N/A (form) | N/A | N/A | N/A — chips always render one lawful value |
| error | 401 detail verbatim, role=alert | silent to door (tokens cleared) + door remains usable | unreachable chip + submit still attempts (backend may differ) | N/A (pattern (b) carries no error) |
| denied | 401 IS the denial (no separate cell) | expired/invalid → door, no message fabrication | N/A | N/A |
| stale | N/A (no cached auth facts rendered) | N/A | reachability older than its poll window renders "checking", not last value | N/A |
| degraded | 5xx → transport-error render, distinct from 401 | same | unreachable | N/A |
| unknown | pre-first-interaction: no error region rendered | pre-boot-check | pre-first-poll = "checking" | the (b) label IS the honest unknown |

## C6. Interaction script (evidence capture = these steps)
1. Load `/login` (no tokens) → capture both viewports.
2. Keyboard-only traversal: Tab order username → password → reveal → submit; capture focus rings.
3. Submit empty → native required behavior captured.
4. Submit bad credentials (seeded test backend) → 401 detail rendered; capture.
5. Toggle reveal; capture accessible-name swap (`aria-label` state).
6. Submit good credentials → redirect to `/` (or `state.from`); capture arrival.
7. Deep-link probe: visit `/journal` unauthenticated → redirected to door with `from` preserved → sign in → land on `/journal`.
8. Backend down (stopped test server): reachability chip + transport-error submit render; capture.
9. Reduced-motion emulation → decorative scene static; capture.
10. Prohibition scans (C9 needles) over the unit's delivered files; transcript into pack.

## C7. Viewport pins
- 1440×900 desktop: split composition permitted.
- 390×844 narrow: single column, form-first, hero reduced to identity strip; no horizontal scroll; touch targets ≥44px.

## C8. Accessibility contract
- All interactives keyboard-reachable in visual order; visible focus (≥3:1); Enter submits.
- Error region `role="alert"`, programmatically associated; announced on appearance.
- Labels: explicit `<label for>` on both fields (as-built pattern kept); reveal button accessible name states action; decorative scene `aria-hidden="true"`.
- Contrast AA (4.5:1 text) on both panes including over gradients; reduced-motion: all animation (grid drift, particles, pulses) disabled.
- Screen-reader door announcement names the surface ("AXIOM operator sign-in") — exact string pinned at BO.

## C9. Prohibitions + scan needles (executable)
- Needles (case-insensitive) over the unit's delivered files, expected ZERO hits outside the C3(b) label: `SSO`, `single sign-on`, `forgot`, `reset your password`, `password reset`, `sign up`, `register`, `two-factor`, `MFA`, `GATE: CLOSED` (as literal), `SAL-2`, order/trade-verb family (`buy`, `sell`, `order ticket`, `execute trade`), any `live_exec` path, any provider/broker hostname, any hardcoded credential.
- No market values in decorative content: numeric-literal scan over hero-scene sources with a declared allowlist (layout constants), each allowlisted value named in the pack.

## C10. V1 regression scope
- All 16 protected routes still route; `ProtectedRoute` redirect law intact (steps 6–7 witness it); existing frontend suite (975 cases at D0-1 census) green at the unit's close — count re-measured, not assumed; auth API client functions byte-diff-reviewed if touched.

## C11. Security & secrets
- Credentials POSTed over the relative-URL client only (AAE-009); never logged, never in URL/query.
- Token storage: as-built localStorage stands for U01 (F-5 hardening = future backend-coupled BO; not silently changed here). No rotation added in U01 (F-4 recorded, untouched).
- Zero provider/broker/AI-secret references (§B.5) — covered by C9 scans.

## C12. Findings & debts
- Touches: F-1 (resolved by C3 pattern), F-2 (resolved by removal), F-3 (resolved — the unit ships the door's first coupon family), F-6 (constrained by C4/C9).
- Deliberately untouched: F-4 (no rotation), F-5 (storage), FE0-BF-1 (public posture endpoint — backend finding, needs its own BO if the Operator elects asserted pre-auth posture).
