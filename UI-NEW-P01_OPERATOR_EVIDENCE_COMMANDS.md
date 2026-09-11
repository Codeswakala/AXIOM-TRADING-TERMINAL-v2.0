# UI-NEW-P01 Operator Evidence Commands

## Terminal Foundation & Multi-Pane Shell Architecture

Run from the operator Windows target unless otherwise stated:

```powershell
cd C:\Users\Swakala\.vscode\AXIOM\axiom
$ErrorActionPreference = "Stop"
```

Optional transcript wrapper:

```powershell
Start-Transcript -Path docs\evidence\UI-NEW-P01_OPERATOR_RESULTS.txt -Force
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
$env:AXIOM_BOOTSTRAP_ADMIN_PASSWORD = "admin123"
$env:AXIOM_ALLOW_INSECURE_DEV = "true"
```

---

## 1. Build identity & artifact integrity

```powershell
Get-Content DELIVERY_REPORT_UI-NEW-P01.md -TotalCount 25
git rev-parse HEAD
git rev-parse --verify UI-NEW-P01_DELIVERY

Get-FileHash -Algorithm SHA256 `
  frontend\src\components\terminal\TerminalGovernanceBadge.tsx, `
  frontend\src\components\terminal\TerminalTopTicker.tsx, `
  frontend\src\components\terminal\TerminalMultiPaneLayout.tsx, `
  frontend\src\components\terminal\TradingTerminalWorkspace.tsx, `
  frontend\src\components\terminal\TerminalMultiPane.css, `
  frontend\src\components\terminal\index.ts, `
  frontend\src\terminal\terminalShell.test.tsx, `
  frontend\src\test\uinew_p01_security_invariants.test.ts, `
  frontend\src\pages\DashboardPage.tsx, `
  frontend\src\workstation\design\tokens.css, `
  frontend\src\workstation\design\theme.ts, `
  docs\governance\GOVERNANCE_AMENDMENTS.md, `
  PROJECT_STATE.md, `
  CHANGELOG.md, `
  docs\plans\UI-NEW_ENGINEERING_DESIGN_PLAN.md | Format-Table -AutoSize
```

Expected SHA-256 for Master Plan:
`8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308`

---

## 2. Six mandatory named UI-NEW-P01 tests — display passing by name

```powershell
cd frontend
npm test -- --reporter=verbose src/terminal/terminalShell.test.tsx src/test/uinew_p01_security_invariants.test.ts
cd ..
```

Required test names to be displayed passing:

```text
test_uinew_p01_terminal_shell_mounts_multipane_layout_without_dom_collisions
test_uinew_p01_terminal_shell_renders_default_docked_placeholders
test_uinew_p01_global_ticker_renders_symbol_price_change_clock_and_ws_status
test_uinew_p01_terminal_contains_no_execution_or_order_or_broker_or_account_control
test_uinew_p01_terminal_renders_no_fabricated_market_values_and_labels_unavailable_states
test_uinew_p01_root_route_mounts_terminal_workstation_and_preserves_existing_routes
test_uinew_p01_governance_badge_renders_gate_closed_research_only_inert
```

---

## 3. T-1 zero-actuation grep audit (production source)

```powershell
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern '\b(buy|sell|place_order|submit_order|order_ticket|execute|go-live|connect-broker|broker|account_id|position|balance|margin|capital|real_pnl|open_gate|allow_execution)\b'
Write-Host "Expected: no output above (0 functional actuation matches in terminal components)."
```

---

## 4. T-4 zero-external-LLM grep audit

```powershell
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern 'openai|anthropic|langchain|gpt|claude|external_llm|llm_summary|ai_summary|api\.openai|remote_prompt'
Write-Host "Expected: no output above (0 external AI SDK imports in terminal module)."

git diff frontend/package.json
Write-Host "Expected: no output above (package dependencies unchanged)."
```

---

## 5. T-6 data-honesty & unavailable state proof

```powershell
cd frontend
npm test -- --reporter=verbose -t "test_uinew_p01_terminal_renders_no_fabricated_market_values_and_labels_unavailable_states"
cd ..
```

Verifies that disconnected, connecting, degraded, and empty feeds render explicit labels (`Loading…`, `Disconnected`, `Empty Feed`, `--`) rather than fabricated numbers.

---

## 6. C-1 permanence grep audit (zero depth ladder / order book)

```powershell
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern 'depth.?ladder|order.?book|orderbook|\bbid\b|\bask\b'
Write-Host "Expected: no output above (0 depth ladder / order book rendering in terminal components)."
```

---

## 7. Sandbox safety, token purity, and secrets audit

```powershell
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern 'dangerouslySetInnerHTML|eval\(|new Function'
Write-Host "Expected: no output above (0 DOM injection or eval matches)."

Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.css,*.tsx |
  Select-String -Pattern '#[0-9A-Fa-f]{3,8}'
Write-Host "Expected: no output above (0 ad-hoc hex literals outside tokens.css; pure token consumption)."

Get-ChildItem frontend\src\components\terminal,frontend\src\terminal -Recurse -File |
  Select-String -Pattern '(password|secret|api_key|private_key|bearer)'
Write-Host "Expected: no output above (0 hardcoded credentials)."
```

---

## 8. No-drift substitute + Alembic head

```powershell
cd backend
alembic current
cd ..
Write-Host "Expected: 20260717_0037 (head)"
```

---

## 9. Full frontend Vitest regression, TypeScript, and Vite build

```powershell
cd frontend
npm audit --audit-level=high
$auditExitCode = $LASTEXITCODE
Write-Host "NPM_AUDIT_HIGH_EXIT_CODE:" $auditExitCode

& cmd.exe /d /s /c "npm test -- --reporter=verbose > ..\docs\evidence\uinew\vitest_full.log 2>&1"
$vitestExitCode = $LASTEXITCODE
cd ..

Get-Content docs\evidence\uinew\vitest_full.log -Tail 60
Write-Host "FRONTEND_VITEST_EXIT_CODE:" $vitestExitCode
if ($vitestExitCode -ne 0) { throw "FRONTEND_VITEST_FAILED:$vitestExitCode" }

cd frontend
npx tsc -b
npx vite build
cd ..
```

Expected:
- Frontend: **150 test files / 617 tests passed** (100%)
- TypeScript: Clean (exit 0)
- Vite build: Clean (exit 0, `dist/assets/index-*.js` ~650 kB)

---

## 10. Backend Pytest regression and Ruff

```powershell
cd backend
ruff check .
pytest -q
cd ..
```

Expected:
- `All checks passed!`
- `414 passed, 1 warning`

---

## 11. Browser served-session evidence (1920×1080 screenshots)

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

Capture the following three screenshots at 1920×1080 viewport:

1. **`UI-NEW-P01_01_TERMINAL_SHELL_IN_FRAME.png`**:
   - URL: `http://localhost:5173/` (Logged in as operator/admin)
   - Must show: Full-bleed multi-pane grid layout (`TerminalMultiPaneLayout`), persistent top ticker header (`TerminalTopTicker`), `GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING` badge, and **zero execution controls anywhere in the frame**.
2. **`UI-NEW-P01_02_DISCONNECTED_HONEST_STATE.png`**:
   - URL: `http://localhost:5173/` (With live market feed stopped/disconnected)
   - Must show: Persistent ticker header in honest disconnected/idle state rendering `Disconnected` / `WS: DISCONNECTED [○]` / `--` (never plausible dummy prices).
3. **`UI-NEW-P01_03_LOGGED_OUT_REDIRECT.png`**:
   - URL: `http://localhost:5173/` (Logged out / unauthenticated)
   - Must show: Route `/` correctly blocked and redirected to `/login`.

Save screenshots to `docs/evidence/uinew/` and attach to submission package.

---

## 12. Local CI verification

```powershell
& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh | Tee-Object docs\evidence\uinew\local_ci.log
$localCiExitCode = $LASTEXITCODE
Write-Host "LOCAL_CI_EXIT_CODE:" $localCiExitCode
```

---

## 13. Submission package checklist

Attach:
1. `DELIVERY_REPORT_UI-NEW-P01.md`
2. `UI-NEW-P01_OPERATOR_EVIDENCE_COMMANDS.md`
3. Three 1920×1080 browser screenshots from §11 (`UI-NEW-P01_01_TERMINAL_SHELL_IN_FRAME.png`, `UI-NEW-P01_02_DISCONNECTED_HONEST_STATE.png`, `UI-NEW-P01_03_LOGGED_OUT_REDIRECT.png`)
4. Verified Git commit SHA & tag (`UI-NEW-P01_DELIVERY`)

---

**End of UI-NEW-P01_OPERATOR_EVIDENCE_COMMANDS.md**
