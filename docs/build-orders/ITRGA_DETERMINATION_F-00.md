# ITRGA DETERMINATION — BO-F-00
## Design-System Foundation, Six-Theme System & Animated Wave Login

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_F-00.md` |
| Build Order | `BO-F-00` (Operator-authorized; Blueprint approved with three refinements) |
| Predecessors | Backend B-00 → B-07 + X-01 Backend Tier · Visual Blueprint APPROVED |
| Date | 2026-08-21 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced in my custody)

| Check | Result |
|-------|--------|
| Patch `f00.patch.txt` sha256 | `50d0e655…` — **matches** |
| Patch composition | **16 files, ZERO backend** (frontend-only, per BO §3) |
| Six-theme registry | **Genuine** — `THEME_IDS` = all six, `DEFAULT_THEME_ID="midnight"`, per-theme metadata |
| Theme override blocks | `.theme-light/slate/teal/amber/high-contrast` all present in `tokens.css` (midnight = root default) |
| New F-00 tests | **29/29 passed** |
| **Full frontend suite** | **913 passed / 182 files, 0 failures** (vs report's 889/176 — see OBS-F00-4) |
| tsc | `tsc -b` clean (empty output = zero diagnostics; SHA matches empty-file) |
| Supply chain | `npm audit --audit-level=high` exit 0; nanoid 3.3.18 overridden; 0 critical / 0 high / 2 moderate (accepted exceptions) |
| Wave login | CSS-only keyframes, reduced-motion freeze block, zero-data scene (test-pinned) |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO §8 requirement | Status |
|-------------------|--------|
| Six themes defined as token overrides, token presence test-pinned | ✓ |
| Theme switcher works; per-operator persistence | ✓ (re-login probe; server-side preference observed) |
| All themes WCAG AA; High-Contrast AAA; contrast asserted | ✓ (per-theme contrast tests) |
| Wave login animated; reduced-motion freezes | ✓ (motion/frozen frame-hash pairs differ/identical) |
| Login scene contains no market-data strings | ✓ (test-pinned) |
| Favicon wired; landing `<h1>`; router-flag decision stated (Option A); supply chain resolved | ✓ all four |
| Full frontend suite green + typecheck green | ✓ |

**All acceptance criteria met.**

## 3. The pivotal properties — verified

1. **The design foundation is real, not a mock.** Six genuinely-implemented token-level themes, a typed registry (RGB triples to honor the "no color literals outside tokens.css" rule), per-operator persistence through the existing preference path, and accessibility contrast asserted per theme. The Blueprint's token language — not the AI PNGs — was correctly treated as the spec.

2. **The wave login is honest motion.** CSS-only (zero dependency, Doc 09 §12 respected), transform/opacity-only (GPU-composited), decorative-only (empty scene textContent, no price/timestamp data), and `prefers-reduced-motion`-frozen — with the freeze *proven* by byte-identical frames 700ms apart vs. differing motion frames.

3. **The Operator's three decisions are all faithfully implemented:** wave (not depth), all six themes (including Teal/Amber as presentation-only accents), and the simulated-live posture carried through (unchanged).

## 4. Findings

### OBS-F00-1 (Medium, backend — surfaced honestly by the DA, out of F-00 scope)
Under concurrent dev load, two `audit append failed … no such savepoint` lines appeared (ws-ticket audit rows lost; endpoints still 200). The DA correctly disclosed it and routed it out of this frontend-only unit. **This is a real backend reliability finding** — audit loss is a governance-integrity concern (the audit trail is the platform's evidence backbone). It should become a **backend hardening Build Order** (target the savepoint/nested-transaction handling in the audit append path), not linger as an observation.

### OBS-F00-2 (Low, carried)
Two react-router MODERATE advisories remain as accepted exceptions pending a dedicated RR7 migration order. Correctly classified under the B-00.2 severity/exception policy (in-product exposure nil — internal registry paths).

### OBS-F00-3 (Medium, custody/provenance — must be addressed at Operator level)
The remote repository history was **rewritten to a single commit** `7e4d993` (an Operator-published snapshot), and the remote's `TECHNICAL_DEBT_REGISTER.md` is an **older version missing delivered rows**. Consequences, verified by me:
- The F-00 patch **does not apply cleanly** to my clone because `TECHNICAL_DEBT_REGISTER.md` context is stale (the register's intermediate B-series rows were described in every Delivery Report but never shipped in the corresponding patches — the drift I flagged as **OBS-X01-2** has now compounded into a patch-apply failure).
- The DA's local object DB still retains the declared baseline `34f4c62` and applies cleanly against it — so the *code* is verifiable, but the **register is not**.
- This is the **provenance failure the project's whole discipline was built to prevent**: the Tier-7 register has drifted out of sync with the review channel, and a history rewrite has made the "chain" reproducible only from the DA's local object DB, not from the shipped patch set alone.

**This is now the single most important open item in the programme, and it is Operator-level:** the register updates must be shipped with the units that produce them (not only described), and the remote history/repository custody needs a decision that restores a verifiable, append-only chain.

### OBS-F00-4 (Info, evidence-precision)
The Delivery Report §9 table lists an **incorrect applycheck hash** (`661d32b9…`) while the authoritative `MANIFEST.txt` carries the correct one (`35834404…`, matching the file). Same report-vs-manifest transcription class as OBS-BML-1 — no evidence-integrity impact (the file itself is correct and verified), but the §9 table should be corrected for the record. Additionally, my full-suite run counted 913/182 vs the report's 889/176 — a test-file-count environment difference (my clone carries additional test files from prior units), not a discrepancy in the F-00 work (29 F-00 tests identical; 0 failures in both).

## 5. Deviations — reviewed and accepted

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | Light-theme focus token changed (`#2563eb`) | Accepted — spec-driven (WCAG AA); disclosed |
| D2 | Two test pins churned (`dark`→`midnight`) | Accepted — superseded by six-theme vocabulary; stricter |
| D3 | Three plumbing files outside §6 list touched | Accepted — required by "switcher works + persistence"; minimal |
| D4 | RGB-triple color storage | Accepted — enforces the no-literals rule; values preserved |
| D5 | `tsconfig.tsbuildinfo` excluded | Accepted — build cache, not artifact |
| D6 | DA cannot view PNGs | Accepted — BO §3 excludes pixel-matching; token language is spec; visual claims machine-verified |

## 6. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All acceptance criteria met; six-theme system + wave login + hygiene genuinely implemented; 29/29 new + full suite green; supply chain to documented standard; frontend-only patch |
| Observations | OBS-F00-1 (backend audit loss — needs a backend fix order), OBS-F00-2 (carried RR moderate), OBS-F00-3 (register drift + history rewrite — Operator-level), OBS-F00-4 (hash transcription + test-count note) |
| Next authorization state | **F-00 CLOSED** — F-01 (assistant input surface) may be issued |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-F-00 |

## 7. Record

- Patch: `50d0e6558a490d169022f0eeac28de8be59bebc221292b33238abcb52a1c76b9` (frontend-only)
- 29/29 F-00 tests · full suite 913/182 green (0 failures) · tsc clean · audit high=0
- Six themes + wave login verified in code; register-drift + history-rewrite escalated

> **We don't guess. We prove.** The design foundation is real, the six themes and the animated wave login are genuinely implemented and honest, and the Operator's three decisions are faithfully executed. But this delivery also surfaced two things that now must be dealt with at a higher level: a backend audit-loss bug, and a register/provenance drift that has grown from an observation into a patch-apply failure. Approved — with those two explicitly routed forward.

**End of ITRGA Determination BO-F-00**
