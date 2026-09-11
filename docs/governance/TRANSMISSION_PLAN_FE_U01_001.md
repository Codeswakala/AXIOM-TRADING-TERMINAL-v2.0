# TRANSMISSION PLAN — FE-U01 Evidence Custody (REVISED — CODE-CHANNEL LAW)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-TX-FE-U01-001 **R1** (supersedes the initial issue) |
| Date | 2026-09-10 |
| **Channel law (Operator, 2026-09-10, binding)** | **CODE ARTIFACTS SHALL NOT BE TRANSMITTED OVER THIS CHANNEL.** Against the governing documents; struck: the T-1 request for the seven delivered code files. Renders, transcripts, manifests, docs, and reference images remain transmittable classes |
| Consequence | In-corpus code re-measurement / needle-scan re-execution / suite re-run are not available for this unit. Replaced by **two-party verification**: (1) DA pack artifacts transmitted (non-code classes), (2) an **Operator-executed spot battery** (§3) — raw terminal output pasted, no code content |

## T-1′ — THE SPINE, code-class struck (one tar.gz, ≪1 MB)

1. ~~The seven code files~~ — **STRUCK (channel law).**
2. All four packs' `MANIFEST.md` + `PACK_CLOSING.md`.
3. Transcripts: E-3 fail-first RED + post-green · E-4 needle scans (all cycles) · E-6 suite runs · E-7 file inventories (hash/size tables — metadata, not code) · E-2 seed-state record.
4. The corrected D0 set (`docs/design/FE0/` incl. D0-2 with AAE-030…036).
5. `V2_CURRENT_STATE.md` v98.0.0 + campaign register line file.

## T-2 — unchanged, images are not code

-004's seven renders + REF-001/002/003 (2–3 messages, ~8 MB). Retires the §9 prototypes HOLD on arrival.

## §3 — OPERATOR-EXECUTED SPOT BATTERY (run in the studio repo; paste raw output verbatim — text only)

```bash
# B1 — file identities (should match MANIFEST E-7 AFTER rows)
cd <studio repo> && md5sum frontend/src/pages/LoginPage.tsx frontend/src/pages/LoginPage.css \
  frontend/src/pages/LoginPage.test.tsx frontend/src/auth/tokenStorage.ts \
  frontend/src/test/f00_design_system.test.tsx frontend/src/test/uiconv_p01_shell.test.tsx \
  frontend/src/test/uiconv_p01_security_invariants.test.ts
# expected (claims on the table): 74469d6f…  e3968db8…  af907cc2…  97e58199…  75282e3b…  eeac897e…  27da1e4b…

# B2 — boundary diff (expect: exactly the named frontend files ± disclosed probe removal; nothing else)
git status --short -- frontend/
git diff --stat HEAD -- frontend/ | tail -12
ls frontend/public/branding/

# B3 — needle scans, my exact needles (expectations recorded below each)
grep -rniE "GATE: CLOSED|SAL-2" frontend/src --include="*.tsx" --include="*.css" --include="*.ts" | wc -l        # expect 0
grep -c "POSTURE: VERIFIED AFTER SIGN-IN" frontend/src/pages/LoginPage.tsx                                     # expect ≥1
grep -c "data-fictional" frontend/src/pages/LoginPage.tsx                                                      # expect ≥1
grep -rniE "2025-05-23" frontend/src/pages/LoginPage.tsx | wc -l                                               # expect ≥1 (frozen fiction timestamp)
grep -rniE "rememberWorkstation" frontend/src --include="*.tsx" --include="*.tsx" | wc -l                      # expect 0
wc -l frontend/src/pages/LoginPage.test.tsx                                                                    # coupon file exists, size of record

# B4 — suite floor, fresh execution
cd frontend && npx vitest run 2>&1 | tail -6                                                                   # expect 189 files / ≥1017 / 0 failures

# B5 — pack tree census (names + sizes + hashes of the -004 anchor files)
md5sum docs/evidence/frontend/FE-U01/FEPACK-FEU01-004/MANIFEST.md \
       docs/evidence/frontend/FE-U01/FEPACK-FEU01-004/PACK_CLOSING.md                                          # expect be730caf… b3afb0fd…
find docs/evidence/frontend/FE-U01 -type f | sort | head -60
```

*(B4 optional if heavy: the E-6 transcript in T-1′ plus B1–B3 suffice for the adapted grade.)*

## Determination class honestly declared

On T-1′ + T-2 + B-outputs: **TRANSMISSION-ADAPTED DETERMINATION** — graded *evidence-consistent* on two-party planes (DA pack manifests/transcripts/renders ⊗ operator-executed battery), with the residual scope declared in the determination record (no in-corpus code re-execution this unit; T-3 rejected-pack renders manifest-narrated). Should the code-channel law ever lift, byte landings trigger full re-measurement. Suspension record `AXIOM-V2-DET-FE-U01-001` remains the measure of record; this revision changes custody mechanics only.
