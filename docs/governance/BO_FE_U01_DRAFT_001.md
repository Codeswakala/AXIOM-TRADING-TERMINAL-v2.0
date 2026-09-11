# BUILD ORDER DRAFT — BO-FE-U01 (Sign-In Surface)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BO-FE-U01-DRAFT-001 |
| Class | **DRAFT — PENDING OPERATOR ADOPTION. On adoption, implementation authority vests in the DA for this unit's scope ONLY; before adoption it authorizes NOTHING** |
| Date drafted | 2026-09-10 (ITRGA hand, adjudicable instrument) |
| Executing authority | **DA only.** ITRGA does not implement |
| Pinned contract | **PC-FEU01-1** in `AXIOM-V2-FE0-D04-001` (upload corpus, md5 `4521605b108b818a36c9488a77d70294`), as accepted by OD-FE0-001 with correction order |
| Pinned elections | Door posture **pattern (b)** (Operator Decision, 2026-09-10); AAE-006 exclusion binding; AAE-007 removal binding |
| Programme frame | U3 `AXIOM-V2-FE-ROADMAP-003` (adoption word pending — recorded, non-blocking: this BO carries its own authority); DPR-001 acceptance path §4.4 |
| Unit loop (U3 §A.3) | This BO = step 1. Then: DA design confirmation → **fail-first tests** → DA implementation → evidence pack `FEPACK-FEU01-001` → **Operator visual approval (decision naming pack id)** → ITRGA determination → U01 closure; only then U02 becomes issuable |

## 1. UNIT SCOPE — exactly ONE surface (§A.1)

**In scope:** route `/login` — the `LoginPage` family (its component, its CSS) and the auth-session seam it triggers, per PC-FEU01-1 C1.
**Out of scope:** everything else rendered, restyled, or touched, including: the post-login redirect target (consumed, not owned); any workspace, registry, chrome, client mechanics beyond this file; F-4 (token rotation) and F-5 (storage hardening) — backend-coupled, own future BOs; FE0-BF-1 — uncommissioned. Files moving outside this unit's scope = defect (E-7).

## 2. REQUIRED CHANGES (contract clauses abbreviated; the contract governs)

1. **Truthful-posture pattern (b) at the door:** pre-auth posture chips render the literal `POSTURE: VERIFIED AFTER SIGN-IN` in neutral (unverified) styling — never an asserted state.
2. **EXCLUDE hardcoded claims (AAE-006):** remove static `GATE: CLOSED`, `RESEARCH-ONLY · NON-ACTUATING` posture strings and the `SAL-2 (Internal) · Hardware Security & Audit Trail Active` footer literal; footer limited to truthful platform-name text.
3. **REMOVE the dead `rememberWorkstation` control (AAE-007)** — no replacement.
4. **Form per the real backend contract only:** username/password → `POST /api/v1/auth/login`; 401 `detail` rendered **verbatim** in an error region (`role="alert"`); transport failure renders a state **distinct** from 401; remain ABSENT: SSO, password-reset/"forgot", sign-up, MFA affordances (backend supports none; scan-enforced per C9).
5. **Reachability chip** powered by `GET /health` (unauthenticated): reachable / unreachable / checking; stale > poll window renders "checking", not the last value.
6. **Decorative scene constrained (C4):** value-free only (no symbols/quotes/levels/P&L), `aria-hidden`, fully static under reduced motion — as accepted in AAE-008.
7. **Session mechanics consumed as-is (AAE-004):** restore via `GET /api/v1/operator/me`; `ProtectedRoute` redirect law preserved (`state.from`), witnessed by C6 steps 6–7.
8. **Ship the door's first coupon family (F-3 resolution):** co-located/unit tests of `LoginPage` per repo convention (tests mock only AuthContext).

## 3. FAIL-FIRST (mandatory)

Before any implementation byte: tests exist for the C5 state-matrix cells (401-verbatim; transport-distinct; checking-states; redirect law) and C9 needle-zero assertions, and are demonstrated **red** against the as-built page. Transcript into the pack (E-3).

## 4. EVIDENCE PACK — `FEPACK-FEU01-001` (per D0-5)

- **E-1** contract pin: PC-FEU01-1 at md5 `4521605b…` (rekey to its filed identity after the correction order executes).
- **E-2** renders: every C5 cell × C7 viewport — `render_<viewport>_<source>_<state>.png` at **1440×900** and **390×844**, from a real running frontend against the seeded test backend; seed state recorded (script+hash).
- **Real conditions, never injection-only (standing law):** 401 via seeded credentials; unreachable/transport via stopped test server; reduced motion via emulation.
- **E-3** C6 script transcript verbatim (10 steps; deviations typed, not re-run silently).
- **E-4** C9 needle scans: exact command + full output; zero hits outside the C3(b) label; allowlisted layout constants each named.
- **E-5** accessibility evidence: keyboard traversal, focus rings, announcement strings as read, contrast pairs, reduced-motion capture.
- **E-6** V1 regression: full frontend suite transcript with count re-measured against the D0-1 census floor (188 files / 975 cases — measured, not assumed); all 16 protected routes + `/chart` alias intact (F-8); byte-diff of any shared file surfaced as finding.
- **E-7** delivered-file inventory (before/after md5+sha256).
- **E-8** Delivery Report on the house template at its true path (`docs/templates/DELIVERY_REPORT_TEMPLATE.md`).
- **E-9** register updates (`V2_CURRENT_STATE.md`, technical-debt delta, frontend campaign line).
- Closes with `PACK_CLOSING.md` carrying the line: *"This pack authorizes nothing; it awaits the Operator Decision naming it."*

## 5. ACCEPTANCE PATH

1. DA delivers implementation + `FEPACK-FEU01-001`.
2. **Operator visual approval** — recorded as an Operator Decision naming `FEPACK-FEU01-001`.
3. ITRGA determination on the same pack (corrective cycles re-key to `-002`, rejected packs retained append-only).
4. U01 closure → FE-U02's Build Order becomes draftable. One unit at a time, ever.

## 6. PRECONDITIONS

1. **Adoption of this BO by the Operator** (the implementation-bearing word for this unit).
2. OD-FE0-001 correction order executed by the DA (docs-only) — custody of D0 set filed; the contract's filed identity supersedes the upload pin in E-1.

---

**This draft awaits your adoption word.** On adoption: the DA begins at §3 (fail-first), and the first surface you will ever approve under the serial cadence is the sign-in door — with its posture rendered honestly, verified only after you sign in.
