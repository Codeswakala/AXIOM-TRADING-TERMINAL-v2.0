# UI-CONV-P01 Operator Evidence Commands

## Unified Shell, Command Layer & Operator Sign-In Surface

Run from the operator Windows target unless otherwise stated:

```powershell
cd C:\Users\Swakala\.vscode\AXIOM\axiom
$ErrorActionPreference = "Stop"
```

Optional transcript wrapper:

```powershell
Start-Transcript -Path docs\evidence\UI-CONV-P01_OPERATOR_RESULTS.txt -Force
```

---

## 0. Environment reminder

```powershell
$env:PGPASSWORD = "axiom_dev_password"
$env:AXIOM_DATABASE_URL = "postgresql+asyncpg://axiom:axiom_dev_password@localhost:5432/axiom"
$env:AXIOM_DATABASE_AUTO_CREATE_SCHEMA = "false"
$env:AXIOM_ENVIRONMENT = "development"
$env:AXIOM_JWT_SECRET_KEY = "local-evidence-secret-key-at-least-32-chars"
$env:AXIOM_BOOTSTRAP_ADMIN_ENABLED = "true"
$env:AXIOM_BOOTSTRAP_ADMIN_USERNAME = "admin"
$env:AXIOM_BOOTSTRAP_ADMIN_PASSWORD = "AxiomSecurePass2026!"
$env:AXIOM_ALLOW_INSECURE_DEV = "true"
```

---

## 1. Build identity & artifact integrity

```powershell
Get-Content DELIVERY_REPORT_UI-CONV-P01.md -TotalCount 25
git rev-parse HEAD
git rev-parse --verify UI-CONV-P01_DELIVERY

Get-FileHash -Algorithm SHA256 `
  frontend\src\pages\LoginPage.tsx, `
  frontend\src\pages\LoginPage.css, `
  frontend\src\workstation\components\InstitutionalWorkspaceShell.tsx, `
  frontend\src\workstation\components\InstitutionalWorkspaceShell.css, `
  frontend\src\workstation\navigation\UnifiedModuleRail.tsx, `
  frontend\src\workstation\navigation\UnifiedModuleRail.css, `
  frontend\src\styles\global.css, `
  frontend\src\test\uiconv_p01_shell.test.tsx, `
  frontend\src\test\uiconv_p01_security_invariants.test.ts, `
  docs\governance\GOVERNANCE_AMENDMENTS.md, `
  PROJECT_STATE.md, `
  CHANGELOG.md, `
  AXIOM_UI_TRANSFORMATION_BLUEPRINT.md | Format-Table -AutoSize
```

---

## 2. Seven mandatory named UI-CONV-P01 tests — display passing by name

```powershell
cd frontend
npm test -- --run --reporter=verbose src/test/uiconv_p01_shell.test.tsx src/test/uiconv_p01_security_invariants.test.ts
cd ..
```

Required test names to be displayed passing:

```text
test_uiconv_p01_all_authenticated_routes_render_in_unified_shell_without_legacy_chrome
test_uiconv_p01_zero_adhoc_hex_outside_tokens_css_in_all_touched_files
test_uiconv_p01_command_palette_reaches_every_registered_route_by_keyboard
test_uiconv_p01_command_palette_exposes_no_actuating_or_order_target
test_uiconv_p01_login_renders_governance_chips_and_no_credential_hints
test_uiconv_p01_login_decorative_scene_renders_no_market_data_values
test_uiconv_p01_every_legacy_affordance_remains_reachable_in_new_shell
```

---

## 3. Brand Governance verification (F-BRAND-1)

```powershell
# Verify AX Monogram is retained in production code
Select-String -Path frontend\src\pages\LoginPage.tsx, frontend\src\workstation\components\InstitutionalWorkspaceShell.tsx -Pattern 'AX'
Write-Host "Expected: AX Monogram present in shell and login header."

# Verify candidate compass+Epsilon mark is NOT referenced in production code
Select-String -Path frontend\src -Recurse -Include *.tsx,*.ts,*.css -Pattern 'candidate_compass_epsilon|compass_epsilon'
Write-Host "Expected: no output above (0 candidate brand mark references in production code)."
```

---

## 4. Programme-scope safety & token audits (B-CONV-1..5)

```powershell
# 1. T-1 Actuation audit
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern '\b(place_order\(|submit_order\(|order_ticket\(|connect_broker\(|open_gate\(|allow_execution\()\b'
Write-Host "Expected: no functional actuation invocations across frontend source."

# 2. T-4 External LLM audit
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern 'api\.openai\.com|api\.anthropic\.com|from ["\x27]openai["\x27]|from ["\x27]@anthropic-ai["\x27]|from ["\x27]langchain["\x27]'
Write-Host "Expected: no output above (0 external LLM SDK imports in source)."

# 3. Ad-hoc hex audit in touched files
Get-ChildItem frontend\src\pages\LoginPage.*, frontend\src\workstation\components\InstitutionalWorkspaceShell.*, frontend\src\workstation\navigation\UnifiedModuleRail.*, frontend\src\styles\global.css -File |
  Select-String -Pattern '#[0-9A-Fa-f]{3,8}\b'
Write-Host "Expected: no output above (0 ad-hoc hex literals across all touched files)."
```

---

## 5. No-drift substitute + Alembic head

```powershell
cd backend
alembic current
cd ..
Write-Host "Expected: 20260717_0037 (head)"
```

---

## 6. Full frontend Vitest regression, TypeScript, and Vite build

```powershell
cd frontend
npm audit --audit-level=high
$auditExitCode = $LASTEXITCODE
Write-Host "NPM_AUDIT_HIGH_EXIT_CODE:" $auditExitCode

& cmd.exe /d /s /c "npm test -- --run --reporter=verbose > ..\docs\evidence\uiconv\vitest_full.log 2>&1"
$vitestExitCode = $LASTEXITCODE
cd ..

Get-Content docs\evidence\uiconv\vitest_full.log -Tail 60
Write-Host "FRONTEND_VITEST_EXIT_CODE:" $vitestExitCode
if ($vitestExitCode -ne 0) { throw "FRONTEND_VITEST_FAILED:$vitestExitCode" }

cd frontend
npx tsc -b
npx vite build
cd ..
```

Expected:
- Frontend: **162 test files / 722 tests passed** (100%)
- TypeScript: Clean (exit 0)
- Vite build: Clean (exit 0, `dist/assets/index-BquLFTtV.js` 718.45 kB)

---

## 7. Backend Pytest regression and Ruff

```powershell
cd backend
ruff check .
pytest -q
cd ..
```

Expected:
- `All checks passed!`
- `415 passed, 1 warning`

---

## 8. Browser served-session evidence (1920×1080 screenshots)

Start local backend and frontend servers:

```powershell
# Terminal A (Backend)
cd backend
python -m alembic upgrade head
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal B (Frontend)
cd frontend
npm run dev -- --host 0.0.0.0
```

Capture the following six screenshots at 1920×1080 viewport (BO §10(f)):

1. **`UI-CONV-P01_01_LOGIN_SURFACE.png`**:
   - URL: `http://localhost:5173/login` (3D perspective decorative scene, pre-auth governance chips, AX monogram).
2. **`UI-CONV-P01_02_LOGIN_FAILED_AUTH_ERROR.png`**:
   - URL: `http://localhost:5173/login` (Explicit `Invalid username or password` error banner).
3. **`UI-CONV-P01_03_TERMINAL_ROOT_UNIFIED_SHELL.png`**:
   - URL: `http://localhost:5173/` (Root terminal workstation in unified shell with Left Module Rail).
4. **`UI-CONV-P01_04_NON_TERMINAL_ROUTE_UNIFIED_SHELL.png`**:
   - URL: `http://localhost:5173/signals` (Non-terminal route rendering cleanly in unified shell).
5. **`UI-CONV-P01_05_COMMAND_PALETTE_OPEN_WITH_RESULTS.png`**:
   - URL: `http://localhost:5173/signals` (Command palette open via Ctrl+K with filtered results).
6. **`UI-CONV-P01_06_REDUCED_MOTION_OR_LIGHT_THEME.png`**:
   - URL: `http://localhost:5173/signals` (Light theme variant in unified shell).

Save screenshots to `docs/evidence/uiconv/` and `/home/user/uploads/`.

---

## 9. Submission package checklist

Attach:
1. `DELIVERY_REPORT_UI-CONV-P01.md`
2. `UI-CONV-P01_OPERATOR_EVIDENCE_COMMANDS.md`
3. Six 1920×1080 browser screenshots from §8
4. Verified Git commit SHA & tag (`UI-CONV-P01_DELIVERY`)

---

**End of UI-CONV-P01_OPERATOR_EVIDENCE_COMMANDS.md**
