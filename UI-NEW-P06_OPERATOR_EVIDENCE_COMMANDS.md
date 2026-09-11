# UI-NEW-P06 Operator Evidence Commands

## Whole-Terminal Integration, Visual Audit & Handover

Run from the operator Windows target unless otherwise stated:

```powershell
cd C:\Users\Swakala\.vscode\AXIOM\axiom
$ErrorActionPreference = "Stop"
```

Optional transcript wrapper:

```powershell
Start-Transcript -Path docs\evidence\UI-NEW-P06_OPERATOR_RESULTS.txt -Force
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
Get-Content DELIVERY_REPORT_UI-NEW-P06.md -TotalCount 25
git rev-parse HEAD
git rev-parse --verify UI-NEW-P06_DELIVERY

Get-FileHash -Algorithm SHA256 `
  frontend\src\terminal\terminalWholeSurface.test.tsx, `
  frontend\src\test\uinew_p06_security_invariants.test.ts, `
  frontend\src\components\terminal\TradingTerminalWorkspace.tsx, `
  frontend\src\components\terminal\TerminalMultiPaneLayout.tsx, `
  frontend\src\components\terminal\TerminalTopTicker.tsx, `
  frontend\src\components\terminal\TerminalWatchlistDock.tsx, `
  frontend\src\components\terminal\TerminalChartStage.tsx, `
  frontend\src\components\terminal\TerminalSignalStream.tsx, `
  frontend\src\components\terminal\TerminalMarketTelemetry.tsx, `
  frontend\src\components\terminal\TerminalIntelligenceCards.tsx, `
  frontend\src\components\terminal\TerminalBottomDock.tsx, `
  frontend\src\components\terminal\TerminalGovernanceBadge.tsx, `
  frontend\src\components\terminal\TerminalMultiPane.css, `
  frontend\src\workstation\registry\workspaceRegistry.tsx, `
  frontend\src\App.tsx, `
  frontend\src\api\client.ts, `
  docs\governance\GOVERNANCE_AMENDMENTS.md, `
  PROJECT_STATE.md, `
  CHANGELOG.md, `
  docs\plans\UI-NEW_ENGINEERING_DESIGN_PLAN.md | Format-Table -AutoSize
```

Expected SHA-256 for Master Plan:
`8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308`

---

## 2. Six mandatory named UI-NEW-P06 tests — display passing by name

```powershell
cd frontend
npm test -- --run --reporter=verbose src/terminal/terminalWholeSurface.test.tsx src/test/uinew_p06_security_invariants.test.ts
cd ..
```

Required test names to be displayed passing:

```text
test_uinew_p06_all_five_terminal_zones_mount_together_without_dom_collision
test_uinew_p06_symbol_selection_propagates_to_chart_telemetry_signals_and_risk
test_uinew_p06_dock_tab_switching_does_not_unmount_or_disturb_sibling_panes
test_uinew_p06_governance_chips_render_in_assembled_surface_not_only_in_units
test_uinew_p06_whole_frontend_contains_zero_actuation_llm_orderbook_or_secret_affordance
test_uinew_p06_every_rendered_statistical_value_carries_uncertainty_or_explicit_unavailable
```

---

## 3. Programme-scope safety audits (B-P06-3)

```powershell
# 1. T-1 Actuation audit
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern '\b(place_order\(|submit_order\(|order_ticket\(|connect_broker\(|open_gate\(|allow_execution\()\b'
Write-Host "Expected: no functional actuation invocations across whole frontend."

# 2. T-4 External LLM audit
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern 'api\.openai\.com|api\.anthropic\.com|from ["\x27]openai["\x27]|from ["\x27]@anthropic-ai["\x27]|from ["\x27]langchain["\x27]'
Write-Host "Expected: no output above (0 external LLM SDK imports in source)."

# 3. C-1 Permanence audit (zero depth ladder / order book)
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern 'depth.?ladder|order.?book|orderbook|\bbid_size\b|\bask_size\b'
Write-Host "Expected: no output above (0 depth ladder / order book rendering in terminal module)."

# 4. S-3 Sandbox safety audit
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern 'dangerouslySetInnerHTML|eval\(|new Function\(' |
  Where-Object { $_.Path -notmatch '\.test\.' }
Write-Host "Expected: no output above (0 dynamic DOM injection or eval in source)."

# 5. T-7 / S-5 Secrets audit
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern '(password|secret|api_key|private_key|bearer)\s*[:=]\s*["\x27][^"\x27]+["\x27]'
Write-Host "Expected: no output above (0 hardcoded credentials in frontend source)."
```

---

## 4. Design-token audit reconciliation (B-P06-2)

```powershell
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern '#[0-9A-Fa-f]{3,8}\b' |
  Where-Object { $_.Path -notmatch 'tokens\.css|\.test\.' }
```

Expected finding: 0 matches in terminal module; legacy styling in `global.css` and fallback strings in `PriceChart.tsx` accounted for and documented under `TD-005`.

---

## 5. Route inventory verification (B-P06-4)

```powershell
cd frontend
npm test -- --run --reporter=verbose -t "B-P06-4"
cd ..
```

Expected: 16 protected workspace routes registered in `WORKSPACE_REGISTRY` + 1 public `/login` route = 17 total routes in React Router.

---

## 6. No-drift substitute + Alembic head

```powershell
cd backend
alembic current
cd ..
Write-Host "Expected: 20260717_0037 (head)"
```

---

## 7. Full frontend Vitest regression, TypeScript, and Vite build

```powershell
cd frontend
npm audit --audit-level=high
$auditExitCode = $LASTEXITCODE
Write-Host "NPM_AUDIT_HIGH_EXIT_CODE:" $auditExitCode

& cmd.exe /d /s /c "npm test -- --run --reporter=verbose > ..\docs\evidence\uinew\vitest_full.log 2>&1"
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
- Frontend: **160 test files / 704 tests passed** (100%)
- TypeScript: Clean (exit 0)
- Vite build: Clean (exit 0, `dist/assets/index-CVVoXKT4.js` 712.99 kB)

---

## 8. Backend Pytest regression and Ruff

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

## 9. Browser served-session evidence (1920×1080 screenshots)

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

Capture the following five screenshots at 1920×1080 viewport (BO §10(f)):

1. **`UI-NEW-P06_01_WHOLE_ASSEMBLED_TERMINAL.png`**:
   - URL: `http://localhost:5173/` (Logged in, all five terminal zones populated).
2. **`UI-NEW-P06_02_SYMBOL_SELECTION_PROPAGATION.png`**:
   - URL: `http://localhost:5173/` (Switch symbol to `GBP/USD`, telemetry dock active).
3. **`UI-NEW-P06_03_BOTTOM_DOCK_TAB_SWITCHING.png`**:
   - URL: `http://localhost:5173/` (Bottom dock tab: `Risk & Drawdown` with intact EUR/USD chart stage).
4. **`UI-NEW-P06_04_LOGGED_OUT_REDIRECT.png`**:
   - URL: `http://localhost:5173/login` (Authentication guard enforced).
5. **`UI-NEW-P06_05_GOVERNANCE_CHIPS_FULL_BLEED.png`**:
   - URL: `http://localhost:5173/` (Full-bleed workstation view showing persistent governance badges).

Save screenshots to `docs/evidence/uinew/` and `/home/user/uploads/`.

---

## 10. Submission package checklist

Attach:
1. `DELIVERY_REPORT_UI-NEW-P06.md`
2. `UI-NEW-P06_OPERATOR_EVIDENCE_COMMANDS.md`
3. Five 1920×1080 browser screenshots from §9
4. Verified Git commit SHA & tag (`UI-NEW-P06_DELIVERY`)

---

**End of UI-NEW-P06_OPERATOR_EVIDENCE_COMMANDS.md**
