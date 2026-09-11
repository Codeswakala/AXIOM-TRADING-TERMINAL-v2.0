# OPERATOR B-BATTERY RUNBOOK — FE-U02 (custody law; expectations pre-declared)

Run from the studio repo root; paste RAW output. B3 boundary-scoped per F-B3-SCOPE.

```bash
echo "=== B1 — identities ==="
md5sum frontend/src/workstation/components/InstitutionalWorkspaceShell.tsx \
  frontend/src/workstation/components/InstitutionalWorkspaceShell.css \
  frontend/src/workstation/components/ChromeContract.test.tsx \
  frontend/src/workstation/navigation/UnifiedModuleRail.tsx \
  frontend/src/workstation/navigation/UnifiedModuleRail.css \
  frontend/src/workstation/overlays/CommandPalette.tsx frontend/src/api/client.ts
echo "=== B2 — boundary ==="
git status --short -- frontend/ | wc -l
ls frontend/public/branding/
echo "=== B3 — needles (boundary) ==="
grep -icE "SAL-2|Gate CLOSED|live:simulated|Presentation shell" \
  frontend/src/workstation/components/InstitutionalWorkspaceShell.tsx \
  frontend/src/workstation/navigation/UnifiedModuleRail.tsx
echo "=== B4 — suite ==="
cd frontend && npx vitest run 2>&1 | tail -4 && cd ..
echo "=== B5 — ACC-2 conditional files byte-still ==="
md5sum frontend/src/workstation/accessibility/RouteAnnouncer.tsx frontend/src/workstation/design/tokens.css
```

**Expected:** B1 `87dc00a6…` `052a9772…` `64641ea7…` `dd652b0c…` `5f910b18…` `8a1d5363…` `bffffba0…` · B2 = 17 lines; branding = axiom-logo.png only · B3 = 0,0 · B4 = 190 files / 1,032 / 0 · B5 `RouteAnnouncer` + `tokens.css` at their E-7 byte-still md5s.
