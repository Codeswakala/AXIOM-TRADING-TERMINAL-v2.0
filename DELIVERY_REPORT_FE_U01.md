# Delivery Report Template

| Field | Value |
|-------|--------|
| Build Order ID | BO-FE-U01 (AXIOM-V2-BO-FE-U01-DRAFT-001, ADOPTED AS DRAFTED per AXIOM-V2-BO-FE-U01-ADOPT-001, md5 `265c2918cfc28e9afff862e587d9c7b8`) |
| Wave / Unit | FE-U01 — Sign-In Surface (the V2 frontend programme's first unit) |
| Version | v1.4.1 — FINAL: OPERATOR-APPROVED (OD-FEPACK-FEU01-004-001); SUBMITTED FOR ITRGA DETERMINATION (hygiene restamp per DET-FE-U01-001 §2: Readiness-Statement pack id corrected -001 → -004; no other content moved) |
| Date | 2026-09-10 |
| Author | Development Authority |

*(Template: `docs/templates/DELIVERY_REPORT_TEMPLATE.md`, md5 `5c8e9de9983cb3ddaec623722fb1d1ec`, per BO §4 E-8 and OD-FE0-001 §1.2b. CF-1 stands: if the Operator's word at any point names the 17-section house template instead, the DA re-stamps on it without content change.)*

## Executive Summary

FE-U01 is implemented and evidence-packed. The sign-in door now tells the truth: the hardcoded pre-auth claims (`GATE: CLOSED`, `RESEARCH-ONLY · NON-ACTUATING`, `SAL-2 …`) are gone, replaced by the Operator-pinned pattern (b) label `POSTURE: VERIFIED AFTER SIGN-IN` in neutral styling, plus one live backend fact — a reachability chip fed by unauthenticated `GET /health` (checking / reachable / unreachable, stale-renders-as-checking). The dead `rememberWorkstation` control is removed. Credential rejection (401, backend `detail` verbatim, red) and transport failure (amber, distinct copy and `data-error-kind`) are now visibly different states. The door received its first coupon family: **21 tests, written fail-first and demonstrated red (13 genuine reds) before any implementation byte.** Full frontend suite: **1,014/1,014 green (189 files)** — the D0-1 floor of 975 plus the new family, zero regressions. Evidence pack `FEPACK-FEU01-001` captures every contract state from a REAL browser against a REAL seeded backend, both viewport pins, with transport states produced by actually stopping the server.

## Objectives Completed

BO §2.1 pattern (b) posture label ✅ · §2.2 AAE-006 exclusions (all three literal families removed; footer reduced to truthful platform name) ✅ · §2.3 AAE-007 removal (control + its CSS retired, no replacement) ✅ · §2.4 real auth contract only (401 `detail` verbatim in `role="alert"`; transport distinct via SURF-P03 `.status` typing; SSO/reset/sign-up/MFA absent, scan-proven) ✅ · §2.5 `/health` reachability chip with generation-guarded poll (stale → "checking", never a stale value) ✅ · §2.6 decorative scene constrained (value-free, aria-hidden, static under reduced motion — witnessed by real emulation, computed `animationName: none`) ✅ · §2.7 session mechanics untouched; redirect law witnessed live (deep-link `/journal` → door → sign-in → `/journal`) ✅ · §2.8 the door's first coupon family ships (F-3 resolved) ✅ · §3 fail-first honored ✅.

## Architecture Summary

No architectural change. The unit consumed existing seams as contracted: `useAuth().login` (AuthContext, AAE-004), `fetchHealth()` (existing client export, AAE-009 relative-URL discipline), `--ix-*` tokens only for all new styling (AAE-001). New client-side state is confined to the page: reachability tri-state with poll-generation guard; `errorKind` typology derived from the SURF-P03 `.status` field. No new endpoints, no client mechanics changes, no storage semantics changes (F-4/F-5 untouched as ordered).

## Files Created / Modified

**Bounded diff: exactly 6 files** (full before/after hashes in pack E-7):

| File | Change |
|---|---|
| `frontend/src/pages/LoginPage.tsx` | MODIFIED — posture pattern (b), reachability chip, error typology, AAE-006/007 removals, truthful footer. After: md5 `cdfaf0e624b65e52ba69a8e72f219421` |
| `frontend/src/pages/LoginPage.css` | MODIFIED — `gov-pill-unverified` + reachability chip styles (retired pills removed), credentials/transport banner variants, checkbox styles retired. After: md5 `2a0b74e50a6bd5bb27dc8f913009bffc` |
| `frontend/src/pages/LoginPage.test.tsx` | **CREATED** — 21-coupon family. md5 `538723c9f096626c64b16ccf2a8b36b9` |
| `frontend/src/test/f00_design_system.test.tsx` | MODIFIED — 1 assertion block superseded BY CITATION (BO §2.1/2.2 cited in-place) |
| `frontend/src/test/uiconv_p01_security_invariants.test.ts` | MODIFIED — 2 assertion blocks superseded BY CITATION; the excluded literals are now NEGATIVELY pinned (`not.toContain`) — the old claims cannot silently return |
| `frontend/src/test/uiconv_p01_shell.test.tsx` | MODIFIED — chip/checkbox assertions superseded BY CITATION (absence now the invariant); login mock corrected to model the real 401 shape |

**Supersession disclosure (DR-F1-class):** the three V1 test files asserted the exact literals/control the BO orders excluded; each edit carries its BO citation in-place, and each replacement asserts the NEW law (presence of the pattern-(b) label / absence of the retired artifacts). No test was deleted; every superseded assertion was replaced by its lawful successor.

## Testing Summary

- **Fail-first:** 21 coupons written first; run against the as-built page: **13 failed / 8 passed** — the 8 pre-passing coupons pin as-built behavior the contract keeps (labels, required fields, reveal toggle, aria-hidden scene, redirect law). Red transcript: pack `E3_FAILFIRST_RED_TRANSCRIPT.txt`.
- **Post-implementation:** LoginPage family **21/21 green** (`E3_GREEN_TRANSCRIPT.txt`).
- **Full suite (E-6):** **189 files / 1,014 tests / 0 failures** (`E6_V1_REGRESSION_TRANSCRIPT.txt`). Census reconciliation, measured: D0-1 static-grep floor 975 → static grep now 996 (975 + 21); runtime executed count 1,014 (parameterized cases expand at runtime — both planes disclosed, both counted, no number recalled).
- **Typecheck:** `tsc --noEmit` exit 0.

## Validation Evidence

Pack `FEPACK-FEU01-001` (`docs/evidence/frontend/FE-U01/FEPACK-FEU01-001/`), 13 renders + 8 transcripts/records + capture script + manifest. Real-conditions law held throughout: 401 from the live auth service (seeded wrong password), success from the seeded bootstrap admin, transport/unreachable from a genuinely stopped backend, reduced-motion from browser emulation with computed-style proof (`animationName: none`). Both viewport pins (1440×900, 390×844) on every capturable contract state. Interaction script executed verbatim (C6 steps 1–2, 4–9; step 3 native-required behavior is coupon-covered; step 10 = E-4). Seed state recorded (`E2_SEED_STATE_RECORD.txt`); scratch world `/tmp/feu01_evidence_world.db` disposed after the pack.

## Risks

- The reachability chip races submit on a just-stopped backend (chip may read "checking" while a submit already fails as transport) — both renders are truthful; no misstatement is possible. LOW.
- The transport banner's fixed copy does not surface the raw network error string — deliberate (C3 render rule: no fabricated detail); the verbatim rule applies to 401 `detail` only. Noted for the Operator's eye.

## Technical Debt

Untouched as ordered: F-4 (no token rotation — backend-coupled, future BO), F-5 (localStorage tokens — future BO), FE0-BF-1 (public posture endpoint — uncommissioned). No new debt introduced. The retired CSS pill classes were removed rather than orphaned (zero dead selectors added; two dead selectors removed).

## Documentation Updates

`V2_CURRENT_STATE.md` → v98.0.0 (this delivery) · campaign register line `FE-U01-DELIVERED` · this DR at repo root · pack manifest with full hashes (E-9 discharged).

## Known Limitations

- jsdom coupons cannot apply media queries; the reduced-motion coupon witnesses the CSS source, while the REAL emulation capture provides the computed-style proof — two planes, one law.
- Contrast evidence rests on the token system's AA recital (AAE-001/021) plus the fact that no new color pair was invented; no independent photometric measurement was run this delivery (available on request).
- E-7 harness note: before-hashes were pre-captured for the 2 surface files only; the 3 V1 test files' before-state is their HEAD state (git-diffable) — disclosed, nothing hidden.

## Recommendations

1. Operator visual review of the 13 renders — the pack is capture-complete for the C5 matrix's real-condition cells.
2. CF-1 template word (13- vs 17-section) whenever convenient; re-stamp is free.
3. FE0-BF-1 remains the path to an *asserted* pre-auth posture if ever desired; the door is honest without it.

## Corrective Cycle 1 (v1.1.0 delta — 2026-09-10)

**Authorizing event:** Operator visual rejection of FEPACK-FEU01-001's composition, with transmitted reference REF-001 (`docs/design/references/REF-001_Login_Signup_Screens.jpg`, md5 `24aff50af75cec0be35c4b5bd3537b15`) and the instruction "professional 3D animated trading terminal." Per §A.5: same unit, same scope, corrective cycle; the pinned contract PC-FEU01-1 (`4521605b…`) is UNCHANGED and re-satisfied.

**Reference absorption:** REF-001 entered the D0-2 register as AAE-030…036 — composition ADAPTED (floating glass shell over full-bleed animated scene; identity strip; split hero/form), auth affordances EXCLUDED (no third-party sign-in row, no recovery link, no account creation, no email identity — none exist on the backend; all five now scan-needled).

**Delta:** EXACTLY 2 files (LoginPage.tsx recomposed, LoginPage.css rewritten — after: md5s in FEPACK-FEU01-002 E-7). The 21-coupon family and the 3 cited V1 tests are BYTE-STILL — the recomposition passed the same law. New scene layers (holo rings, scan beam, horizon, second orb) are all transform/opacity-only and covered by the reduced-motion freeze block, proven per-layer by computed style in a real reduced-motion browser context.

**Evidence:** `FEPACK-FEU01-002` (8 renders both viewports, 17-row manifest; real-conditions law re-held end to end). FEPACK-FEU01-001 retained untouched as history.

**Self-catches disclosed (2):** the build's own comments twice carried scan needles ('SSO', 'Register' — in prose about excluding them); the C9 coupon and the E-4 transcript each fired genuine red and the comments were reworded. The honesty machine audits its author.

**One DA-eye defect caught pre-presentation:** the 410×408 brand asset overflowed its 40px monogram box in the first corrective build; containment CSS restored; recaptured before presentation.

## Corrective Cycle 3 (v1.2.0 delta — 2026-09-10): REF-002 REPLACEMENT BUILD

**Authorizing events:** (1) Operator instruction — the old UI is being REPLACED, not evolved; (2) REF-002 transmitted (`docs/design/references/REF-002_Login_Page_Template.png`, md5 `343be6a077cde53adf56a87b5dd02cf4`) with "build the attached login page exactly as it is"; (3) two in-channel Operator elections, recorded:
- **REF-002-E1** ("build them now"): all four template affordances BUILT. *Remember me* is FUNCTIONAL — a new `setTokenPersistence` seam in `tokenStorage.ts` (checked → localStorage, unchecked → sessionStorage; cross-store clear; both arms witnessed in a real browser). *Continue with Google*, *Forgot password?*, *Register* render per template and answer with truthful unavailability notices — no backend flows exist (findings **FE0-BF-2/3/4** opened for future backend BOs). They never fake success, never navigate. This election supersedes the AAE-033…035 exclusions and retires their scan needles (needle law re-keyed in E-4).
- **REF-002-E2** (rebuild in code): the hero is a code-built, value-free scene — night-city bokeh, window grid, terminal screen with 16 candle silhouettes, bar-only side panel, desk plane. Zero market values in the DOM, coupon-asserted.

**Replacement scope:** `LoginPage.tsx`/`LoginPage.css` replaced whole; coupon family re-cut (21 coupons incl. the E1 affordance-truthfulness family); 3 V1 tests superseded by citation (old wave-scene pins retired with the old surface; placeholder law re-keyed to generic-label form — placeholders are field names, never example values). Bounded diff 6 files. One unplanned asset disclosed (`login-hero-ref002.png`, unreferenced probe artifact — flagged for removal at acceptance, not silently deleted).

**Adaptation note (§B.9, one line):** the template's "TRADING TERMINAL" / "Better Trades" / "continue trading" wording is rendered as "RESEARCH TERMINAL" / "Better Research." / "continue your research" — the platform's truthful posture; everything else follows the template. The truthful status line (posture pattern (b) + reachability) rides inside the card above the greeting.

**Evidence:** `FEPACK-FEU01-003` — 8 renders both viewports; real-conditions law re-held (live 401, seeded success, stopped-backend transport, CDP reduced-motion with computed proof); Remember-me BOTH persistence arms browser-witnessed; affordance notices browser-witnessed; full suite **189 files / 1,016 / 0**; tsc clean; 19-row manifest.

## Corrective Cycle 4 (v1.3.0 delta — 2026-09-10): REF-003 HOLOGRAPHIC HERO

**Authorizing events:** Operator partial verdict on the cycle-3 build — **right card APPROVED verbatim** ("the right card looks perfect"), left hero rejected; REF-003 transmitted (`docs/design/references/REF-003_Hero_Holographic_Terminal.png`, md5 `a7ef8fe7f9b338b59126e2865be7f836`) with the instruction to implement it on the left panel, 3D animated.

**Election REF-003-E1 recorded** ("even if the placeholder values were incorrect"): the decorative hero may carry the reference image's OWN readout values as STATIC FICTION — the ESMS/NQMS/YMMS/CLMS/GCQS ticker block, the DATA FEED/LATENCY/TIMESTAMP/SESSION block (frozen 2025-05-23 timestamp), and the VOL/DVOL/ADV/DEC/UNCH block — rendered aria-hidden + `data-fictional`, outside the candle-scene subtree, never sourced from live data. New coupon `test_feu01_ref003_readouts_are_hidden_static_fiction` witnesses all four properties in jsdom; the E-3 script re-witnesses them in the real DOM. The 'DATA FEED LIVE' string is part of the elected fiction art, not a mode claim — the card's truthful posture chip remains the page's only posture statement.

**The hero as built (3D animated, transform/opacity-only):** flowing perspective floor grid + standing back lattice · breathing blue nebula and bokeh · 18-candle holographic field tracing REF-003's dip-and-rally arc (solid and hollow bodies, glowing wicks, floor reflections, per-candle flicker phases) · rising scanline · wireframe AXIOM lockup with the thin-stroke mark and letter-spaced word. Reduced-motion freezes every layer — computed-style proven for nebula, floor grid, scanline, candles, and glow in a real reduced-motion browser context.

**Bounded diff: EXACTLY 3 files** (LoginPage.tsx hero section, LoginPage.css hero styles — auth-card styles carried verbatim; LoginPage.test.tsx +1 coupon). The approved right card's JSX and CSS are byte-carried within those files; tokenStorage and the three V1 test files are BYTE-STILL from cycle 3. Suite **189 files / 1,017 / 0**; tsc clean; permanent needles zero.

**Evidence:** `FEPACK-FEU01-004` — 7 renders both viewports, real-conditions law re-held end to end, 17-row manifest. Packs -001…-003 retained append-only.

## Final Submission Record (v1.4.0 — 2026-09-10): OPERATOR APPROVAL + ITRGA HANDOFF

### 1. The approval
**Operator Decision `OD-FEPACK-FEU01-004-001`** (md5 `89559dac5ca7b901749e93d362672aec`, filed to `docs/governance/`): *"the current login page is approved"* — recorded per §A.4 as the decision naming evidence pack **`FEPACK-FEU01-004`** (MANIFEST md5 `be730cafc3dcaafd7778778969fe0d60` · PACK_CLOSING md5 `b3afb0fdd4ab7b08f6ebd6155c92f062`). Approval trail inside the unit: cycle-3 partial (right card verbatim) → cycle-4 whole page. BO-FE-U01 §5.1–§5.2 are DISCHARGED; this report is the §5.3 submission.

### 2. Post-approval cleanup (executed, witnessed)
The one open E-7 flag closed: `frontend/public/branding/login-hero-ref002.png` (unreferenced probe artifact from the cycle-3 hero-option probe, md5 `48526bd594d6fc5af44418f2b1d35353`) was REMOVED at acceptance exactly as flagged — zero source references proven by grep BEFORE removal; **full suite re-run whole AFTER: 189 files / 1,017 / 0.** No other byte moved in the cleanup.

### 3. Final delivered-state identities (measured from final bytes, this filing)

| File | md5 | Role |
|---|---|---|
| `frontend/src/pages/LoginPage.tsx` | `74469d6f750324c54614b1c6d272c7ac` (sha256 `9be13755…cd07c6`) | The approved surface |
| `frontend/src/pages/LoginPage.css` | `e3968db898ca51f05d94111c35c1054c` (sha256 `bcafd11e…f2ffe`) | The approved styles |
| `frontend/src/pages/LoginPage.test.tsx` | `af907cc29a2d760cf1cda19a039120eb` | 22-coupon family (F-3 resolved) |
| `frontend/src/auth/tokenStorage.ts` | `97e58199d8bf05d11e70e8f89a3f778a` | REF-002-E1 persistence seam |
| `frontend/src/test/f00_design_system.test.tsx` | `75282e3bb81c9252588c6457570d3b00` | Superseded-by-citation (scene re-key) |
| `frontend/src/test/uiconv_p01_shell.test.tsx` | `eeac897e63d792bb5b733ec5376d2105` | Superseded-by-citation (chips/checkbox/placeholder/401-mock) |
| `frontend/src/test/uiconv_p01_security_invariants.test.ts` | `27da1e4b3f7107d62aab44f134acb4f1` | Superseded-by-citation (posture/SAL-2 negative pins) |

**Total unit footprint: EXACTLY 7 delivered files** (6 modified + 1 created) + the removed probe asset. Nothing outside the authorized boundary moved at any cycle (per-cycle E-7 inventories in the packs).

### 4. The elections ledger (everything the approved state stands on)

| Election | Word | Executed as | Witness |
|---|---|---|---|
| Pattern (b) door posture | OD-FE0-001 §2 (pinned pre-BO) | `POSTURE: VERIFIED AFTER SIGN-IN` neutral chip; no asserted pre-auth claims | coupon + every pack's renders |
| REF-002-E1 "build them now" | in-channel, cycle 3 | 4 affordances built; Remember-me FUNCTIONAL (localStorage/sessionStorage, both arms browser-witnessed); Google/Forgot/Register = truthful-notice pattern, never fake success | 5-coupon family + FEPACK-003 browser transcript |
| REF-002-E2 code-built hero | in-channel, cycle 3 | superseded by REF-003 composition at cycle 4 | — |
| REF-003-E1 fiction readouts | in-channel, cycle 4 ("even if the placeholder values were incorrect") | image's own values as STATIC FICTION: aria-hidden + data-fictional + outside scene subtree + frozen 2025 timestamp | 4-property coupon + real-DOM witness |

Findings opened for future backend BOs (uncommissioned): **FE0-BF-1** (public posture endpoint) · **FE0-BF-2/3/4** (SSO / password recovery / registration flows). F-4 (rotation) and F-5 (storage-class hardening) remain register debts, untouched as ordered.

### 5. Verification summary for the ITRGA seat

- Fail-first: 13 genuine reds before implementation (FEPACK-001 E-3); every subsequent cycle green-first-run against the carried coupons or red-caught-and-fixed with disclosure.
- Real-conditions law held in ALL FOUR packs: live 401s from the seeded auth service, genuine stopped-backend transport states, CDP reduced-motion with per-layer computed-style proof, both Remember-me persistence arms in a real browser.
- Prohibition discipline: permanent needles zero at every cycle; needle-law changes only by recorded election (REF-002-E1 retirement set); THREE self-catches disclosed across the campaign (the scanner caught its own author's comments twice, the transcript once).
- V1 regression: suite whole at every cycle close — final **189 files / 1,017 tests / 0 failures**; census reconciliation disclosed (static-grep vs runtime-expanded counts, both measured).
- Bounded-diff discipline: cycle diffs of 6/2/6/3 files, each inventoried with before/after hashes; the approved right card byte-carried through cycle 4.
- Packs: FEPACK-FEU01-001 → -004, all manifested (every file hashed), all retained append-only; -004 is the approval-bearing pack.

## Readiness Statement

> Implementation completed and submitted for independent ITRGA review. Not self-approved.

**This report's approval-bearing pack is `FEPACK-FEU01-004`** — named by the issued Operator
Decision `OD-FEPACK-FEU01-004-001`; the pack authorizes nothing of itself. ITRGA determination
on that same pack is the unit's sole open gate. Only then does FE-U02 become draftable.
*(v1.4.1 hygiene restamp per DET-FE-U01-001 §2: the prior line's `-001` pack id predated the
corrective cycles and was stale — the -001…-003 packs are append-only history; -004 bears
the approval.)*
