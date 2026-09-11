# OPERATOR B-BATTERY RUNBOOK — the final verification plane (TX R1 §3)

**One copy-paste block. Run it from the studio repo root, paste the RAW output back to
ITRGA verbatim (text only — no code content leaves the studio; the outputs are hashes,
counts, and filenames).** The B3 needle is scoped to the DELIVERY BOUNDARY per finding
F-B3-SCOPE (DA pre-run + ITRGA VM §1 both corroborate: tree-wide hits are heritage V1
shell classification, lawful and outside this unit).

```bash
echo "=== B1 — file identities ==="
md5sum frontend/src/pages/LoginPage.tsx frontend/src/pages/LoginPage.css \
  frontend/src/pages/LoginPage.test.tsx frontend/src/auth/tokenStorage.ts \
  frontend/src/test/f00_design_system.test.tsx frontend/src/test/uiconv_p01_shell.test.tsx \
  frontend/src/test/uiconv_p01_security_invariants.test.ts

echo "=== B2 — boundary diff ==="
git status --short -- frontend/
git diff --stat HEAD -- frontend/ | tail -12
ls frontend/public/branding/

echo "=== B3 — needles (delivery-boundary scope per F-B3-SCOPE) ==="
grep -icE "GATE: CLOSED|SAL-2" frontend/src/pages/LoginPage.tsx frontend/src/pages/LoginPage.css frontend/src/auth/tokenStorage.ts
grep -c "POSTURE: VERIFIED AFTER SIGN-IN" frontend/src/pages/LoginPage.tsx
grep -c "data-fictional" frontend/src/pages/LoginPage.tsx
grep -cE "2025-05-23" frontend/src/pages/LoginPage.tsx
grep -rniE "rememberWorkstation" frontend/src --include="*.tsx" | wc -l
wc -l frontend/src/pages/LoginPage.test.tsx

echo "=== B4 — suite floor (fresh run; ~3 min) ==="
cd frontend && npx vitest run 2>&1 | tail -4 && cd ..

echo "=== B5 — pack anchors ==="
md5sum docs/evidence/frontend/FE-U01/FEPACK-FEU01-004/MANIFEST.md \
       docs/evidence/frontend/FE-U01/FEPACK-FEU01-004/PACK_CLOSING.md
find docs/evidence/frontend/FE-U01 -type f | wc -l
```

**Expected values (DA station pre-run; your paste should reproduce):**

| Check | Expect |
|---|---|
| B1 | `74469d6f…` tsx · `e3968db8…` css · `af907cc2…` test · `97e58199…` tokenStorage · `75282e3b…` f00 · `eeac897e…` shell · `27da1e4b…` security |
| B2 | 6 ` M` + 1 `??` (LoginPage.test.tsx), nothing else; diff-stat = 6 files, 972+/605−; branding dir = `axiom-logo.png` only |
| B3 | 0,0,0 (per-file) · 1 · 2 · 2 · 0 · 367 |
| B4 | `Test Files 189 passed` · `Tests 1017 passed` · 0 failures |
| B5 | `be730caf…` · `b3afb0fd…` · 76 files |
