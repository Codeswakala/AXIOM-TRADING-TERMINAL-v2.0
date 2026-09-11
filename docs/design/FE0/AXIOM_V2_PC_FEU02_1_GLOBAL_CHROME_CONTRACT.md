# PC-FEU02-1 — FE-U02 GLOBAL CHROME PAGE CONTRACT (PCF-1 format)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-PC-FEU02-1 |
| Version | 1.0.0 |
| Author | DA · 2026-09-11 (docs-only turn per BO-FE-U02 §6.2 / adoption §3.1) |
| Format authority | PCF-1 in `AXIOM_V2_FE0_D04_PAGE_CONTRACT_FORMAT_AND_FEU01_SIGNIN.md` (md5 `4521605b108b818a36c9488a77d70294`) — twelve sections C1–C12 |
| BO | `AXIOM-V2-BO-FE-U02-DRAFT-001` (md5 `b5f60dc6f8c2796bbf6530185af1f7e3`), ADOPTED AS DRAFTED (`07ecde6367353a8fa5844f2d9b8b2b9e`) |
| Review posture | Rides ITRGA review, adjudicable, acceptance-with-correction. E-1 re-keys to this file's published identity |
| As-built baseline (measured this filing) | Heritage shell `InstitutionalWorkspaceShell.tsx` 446 L (+ .css) · `UnifiedModuleRail.tsx` 99 L (+ .css) · `RouteAnnouncer.tsx` (UI-010-P05, route-truth announcing) · tokens.css 282 props · registry 16 workspaces. Heritage shell carries 4 asserted-posture hits (`Gate CLOSED` chip ×2 sites, command-registry toast literals) + `live:simulated` posture badge + `SAL-2 (Internal)` container recital |

## C1. Identity

Unit **FE-U02**; owns exactly ONE surface family: **the chrome** — app shell/layout primitive (`InstitutionalWorkspaceShell` family), header strip, left nav rail (`UnifiedModuleRail` family), route announcer, and the token/primitive baseline (`workstation/design/tokens.css` + `theme.ts`). Everything rendered *under* the chrome is consumed, not owned. The `/login` door (U01, closed) stays chrome-free.

**Delivered-file family (E-7 inventory basis):** `workstation/components/InstitutionalWorkspaceShell.{tsx,css,test.tsx}` · `workstation/navigation/UnifiedModuleRail.{tsx,css}` + navigation tests it pins · `workstation/accessibility/RouteAnnouncer.{tsx,test.tsx}` (only if bytes must move — route-truth law already conforms) · `workstation/design/tokens.css`/`theme.ts` (only if the baseline codification requires additions — no removals) · one NEW coupon family file for the chrome contract. Any file outside this list moving = scope defect.

## C2. Purpose + AXIOM identity expression

The frame every later surface lives inside: identity, orientation, command access, operator session, time, mode truth, platform health — rendered only ever as truthful as the capability beneath it. Identity: AXIOM brand via `--ix-*` tokens; **branding covenant: `axiom-logo.png` is the sole image asset** (new asset class = disclosure-and-election first).

## C3. Backend truth sources

| Fact | Source | Auth | Render rule |
|---|---|---|---|
| Global health | `GET /health` (unauthenticated; poll 30s, generation-guarded — the U01 pattern promoted chrome-wide) | none | REACHABLE (green) / UNREACHABLE (amber) / CHECKING (muted); stale > poll window renders CHECKING, never last value. **DEGRADED cell: N/A this unit** — no real degraded-classifying source exists on the backend today (`/health` returns ok-or-fails); a degraded state without a source would be fabricated. Finding FE0-BF-5 (health granularity endpoint) opened for a future backend BO |
| Mode badge | Mode is backend-locked (`AXIOM_V2_MODE=RESEARCH`; `/api/v1/v2/mode` is authed). Chrome-wide the badge renders the platform's standing truth: **RESEARCH · NON-ACTUATING** — sourced from the authed mode read when a session exists; pre-auth/failed read renders the same disposition marked `unverified` (pattern (b) at chrome level: the label is the platform's registered posture, the verification state is honest) | Bearer when available | No PAPER/BROKER/LIVE cue may exist anywhere in the chrome — needle-enforced |
| Operator identity chip | `GET /api/v1/operator/me` via the AuthContext session (AAE-004, consumed as-is) | Bearer | Authenticated: username + role. Unauthenticated: the shell renders under ProtectedRoute so this state is structurally unreachable; if ever rendered sessionless, the chip renders neutral "—" and asserts nothing |
| Time | Client clock, UTC, labeled UTC (as-built pattern kept) | — | Display-only; never presented as server time |
| Nav rail route set | `WORKSPACE_REGISTRY` + `generateNavigationSections({workspaces, operator})` — the real entitlement surface (AAE-003) | session | Items render only for roles whose `allowedRoles` admit them; no aspirational items |
| Command/search | **ELECTION C4-a taken: shipped truthful** — the existing command registry over the REAL navigable set (registry workspaces + registered actions), with empty-state honesty ("No matching workspace or action"). No faux results, no dead toasts: the two heritage command-registry toast literals asserting `Gate CLOSED` are expelled (C9) |

## C4. Surface anatomy

- **Header strip:** brand block (logo + AXIOM wordmark) · command/search trigger (palette, C3 election a) · governance status cluster **rebuilt truthful**: mode badge (RESEARCH · NON-ACTUATING per C3), health chip, UTC clock — the asserted `Gate CLOSED` / `Research-only` / `Presentation shell` / `live:simulated` literal chips are EXPELLED and replaced by the two backend-sourced chips + clock · operator cluster (identity chip, workspace switcher, theme toggle, settings, sign-out — as-built, kept).
- **Left nav rail:** as-built role-aware registry rail kept; **collapse control added** with honestly persisted preference (localStorage key `axiom_chrome_rail_collapsed`; a UI preference is not a security artifact — REF-002-E1's remembered-preference pattern; declared here as the storage election); full keyboard traversal; collapsed rail keeps accessible names.
- **Route announcer:** as-built `RouteAnnouncer` conforms (announces the rendered destination only) — consumed; bytes move only if integration demands.
- **Token baseline:** the 282-prop set codified as the chrome baseline; visual-regression baseline captured over the chrome renders (E-2 set doubles as the baseline corpus).

## C5. State matrix (per source)

| State | Health chip | Mode badge | Operator chip | Nav rail | Command palette |
|---|---|---|---|---|---|
| loading/checking | CHECKING (muted) | unverified-marked until first authed read | session-loading neutral | renders (registry is static) | opens; registry local |
| empty | N/A (always one value) | N/A | N/A | N/A (≥1 route always) | "No matching workspace or action" |
| error | UNREACHABLE (amber) | stays last-verified w/ unverified mark; never invents | falls to neutral on session loss | unchanged | unchanged (local) |
| denied | N/A (unauthenticated endpoint) | unverified mark | structurally unreachable (ProtectedRoute); neutral if forced | role-filtered (that IS the denied render) | role-filtered set only |
| stale | CHECKING, never last value | unverified mark after TTL (same 30s window) | session events refresh | static | static |
| degraded | **N/A this unit (no source — FE0-BF-5)** | N/A | N/A | N/A | N/A |
| unknown | pre-first-poll CHECKING | pre-first-read unverified | pre-session neutral | registry-static | registry-static |

## C6. Interaction script (evidence capture = these steps)

1. Authenticated boot at `/` → chrome renders: header truthful cluster + rail + announcer live region present; capture both viewports.
2. Health tri-state: backend up → REACHABLE; stop backend → UNREACHABLE; restart window → CHECKING transition. Captures at each.
3. Keyboard: Tab traversal across all header landmarks and rail items in order; collapse toggle via keyboard; captures of focus rings.
4. Rail collapse → persists across reload (storage election witnessed); collapsed rail retains accessible names.
5. Route navigation `/` → `/journal` → announcer announces the rendered destination (string captured from live region).
6. Command palette: open, query a real workspace → real result navigates; query gibberish → empty-state honesty render.
7. Role-aware: seeded `unprivileged`-class session (real role) → rail renders the role-filtered set; capture.
8. Reduced-motion emulation → any chrome motion static.
9. Mode badge: authed read verified vs pre-read unverified mark — both states captured.
10. Needle scans (C9) over the delivered family; transcript to pack.

## C7. Viewport pins

1440×900 desktop · 390×844 narrow (rail behavior at narrow: collapsed-by-default drawer per as-built responsive pattern; no horizontal scroll; touch targets ≥44px).

## C8. Accessibility contract

Landmarks: `banner` (header) / `navigation` (rail, labeled) / `main` (host) / `status` (announcer + health). All interactives keyboard-reachable, visible focus ≥3:1; announcer `role="status" aria-live="polite" aria-atomic` (as-built law kept); collapse control carries accessible expanded/collapsed name; contrast AA on all new chips via existing token pairs (no new color pairs); reduced-motion: all chrome transitions disabled.

## C9. Prohibitions + scan needles (executable; boundary-scoped per F-B3-SCOPE)

**Boundary = the delivered-file family (C1).** Needles, zero-hit inside the boundary:
`SAL-2` · `GATE: CLOSED`/`Gate CLOSED` · `Research-only` (as asserted chip literal) · `Presentation shell` · `live:simulated` · `PAPER`/`BROKER`/`LIVE` (capability-cue class, word-boundary, case-sensitive contexts declared in the scan) · order-vocabulary family (`order ticket`, `BUY`/`SELL` CTA class, `entry/stop/target`, `R:R`) · `rememberWorkstation` (resurrection guard) · faux-search vocabulary (`coming soon`, `not implemented` as *result* strings) · credential-hint family.
**Heritage protection clause:** the same literals in files OUTSIDE the boundary (`components/terminal/*`, `terminal/*`, V1 test pins) are protected heritage until their owning unit — the scan reports them as OUT-OF-BOUNDARY, never as unit defects, and the unit MUST NOT edit them.

## C10. V1 regression scope

Suite floor **189 files / 1,017 cases / 0 failures** (re-based by DET-FE-U01-002; re-measured never assumed). All 16 protected routes + `/chart` alias reachable through the delivered rail. V1 coupons pinning heritage shell literals: the shell-owning coupons that assert the EXPELLED literals will be superseded-by-citation with negative pins (the U01 pattern); coupons pinning OUT-OF-BOUNDARY heritage stay byte-still. U01's door coupons (22) must stay green — the chrome never wraps `/login`.

## C11. Security & secrets

No new endpoints; no provider/broker/AI references (§B.5); tokens untouched (F-4/F-5 stand); collapse preference carries zero sensitive data; command registry executes navigation only — no actuation verbs (§B.7 boundary respected chrome-wide).

## C12. Findings & debts

Opens: **FE0-BF-5** (health granularity/degraded source — backend, future BO). Touches: the 4 heritage asserted-posture hits + `live:simulated` badge inside the boundary (expelled per §2.9). Deliberately untouched: out-of-boundary heritage literals (21-file family, protected); F-4/F-5; FE0-BF-1…4. Storage election declared: `axiom_chrome_rail_collapsed` (UI preference, localStorage).
