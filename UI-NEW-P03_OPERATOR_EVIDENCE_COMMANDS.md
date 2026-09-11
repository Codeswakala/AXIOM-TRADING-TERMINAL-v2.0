# UI-NEW-P03 Operator Evidence Commands

## Primary Chart Stage · Multi-Timeframe Controls · Technical Overlays · Research Annotations

Run from the operator Windows target unless otherwise stated:

```powershell
cd C:\Users\Swakala\.vscode\AXIOM\axiom
$ErrorActionPreference = "Stop"
```

Optional transcript wrapper:

```powershell
Start-Transcript -Path docs\evidence\UI-NEW-P03_OPERATOR_RESULTS.txt -Force
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
Get-Content DELIVERY_REPORT_UI-NEW-P03.md -TotalCount 25
git rev-parse HEAD
git rev-parse --verify UI-NEW-P03_DELIVERY

Get-FileHash -Algorithm SHA256 `
  frontend\src\components\terminal\TerminalChartStage.tsx, `
  frontend\src\components\terminal\tokenResolver.ts, `
  frontend\src\components\chart\PriceChart.tsx, `
  frontend\src\components\terminal\TradingTerminalWorkspace.tsx, `
  frontend\src\components\terminal\TerminalMultiPane.css, `
  frontend\src\components\terminal\index.ts, `
  frontend\src\chart\types.ts, `
  frontend\src\terminal\terminalChartStage.test.tsx, `
  frontend\src\test\uinew_p03_security_invariants.test.ts, `
  frontend\src\test\setup.ts, `
  docs\governance\GOVERNANCE_AMENDMENTS.md, `
  PROJECT_STATE.md, `
  CHANGELOG.md, `
  docs\plans\UI-NEW_ENGINEERING_DESIGN_PLAN.md | Format-Table -AutoSize
```

Expected SHA-256 for Master Plan:
`8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308`

---

## 2. Seven mandatory named UI-NEW-P03 tests — display passing by name

```powershell
cd frontend
npm test -- --run --reporter=verbose src/terminal/terminalChartStage.test.tsx src/test/uinew_p03_security_invariants.test.ts
cd ..
```

Required test names to be displayed passing:

```text
test_uinew_p03_chart_stage_renders_candles_from_backend_series_only
test_uinew_p03_timeframe_switching_discloses_resampled_or_incomplete_series
test_uinew_p03_chart_tokens_resolve_to_concrete_values_with_no_hardcoded_hex
test_uinew_p03_annotations_reject_order_entry_stop_target_and_size_fields
test_uinew_p03_seed_and_live_provenance_are_visually_distinguished
test_uinew_p03_chart_contains_no_execution_or_order_or_broker_or_account_control
test_uinew_p03_overlays_are_presentation_only_and_emit_no_signal_or_confidence
```

---

## 3. T-1 zero-actuation & annotation write-path audit

```powershell
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern '\b(buy|sell|place_order|submit_order|order_ticket|execute|connect-broker|account_id|position|balance|margin|open_gate|allow_execution)\b'
Write-Host "Expected: no output above (0 functional actuation matches)."

Get-ChildItem frontend\src\components\terminal -Recurse -File -Include TerminalChartStage.tsx |
  Select-String -Pattern 'stop_loss|take_profit|position_size|lot|volume_size'
Write-Host "Expected: matches only inside forbiddenOrderMarkers rejection validation."
```

---

## 4. T-4 zero-external-LLM grep audit

```powershell
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern 'openai|anthropic|langchain|gpt|claude|external_llm|llm_summary|ai_summary|api\.openai|remote_prompt'
Write-Host "Expected: no output above (0 external AI SDK imports in terminal module)."

git diff frontend/package.json
Write-Host "Expected: no output above (package dependencies unchanged; lightweight-charts retained)."
```

---

## 5. B-P03-1 Token Resolver & B-P03-2 Timeframe Honesty Verification

```powershell
cd frontend
npm test -- --run --reporter=verbose -t "test_uinew_p03_chart_tokens_resolve_to_concrete_values_with_no_hardcoded_hex"
npm test -- --run --reporter=verbose -t "test_uinew_p03_timeframe_switching_discloses_resampled_or_incomplete_series"
cd ..
```

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
- Frontend: **154 test files / 650 tests passed** (100%)
- TypeScript: Clean (exit 0)
- Vite build: Clean (exit 0, `dist/assets/index-*.js` ~670 kB)

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

Capture the following 1920×1080 screenshots (OBS-P01-5):

1. **`UI-NEW-P03_01_PRIMARY_CHART_STAGE.png`**:
   - URL: `http://localhost:5173/` (Logged in)
   - Must show: Full-bleed terminal with candlestick chart centerpiece rendering in center stage, timeframe toolbar, overlays, and `live:simulated` badge.
2. **`UI-NEW-P03_02_HIGHER_TIMEFRAME_RESAMPLED_NOTICE.png`**:
   - URL: `http://localhost:5173/` (Select 1H or 4H timeframe)
   - Must show: Explicit `Resampled from M1 stream · Sparse/Incomplete higher-timeframe data (TD-029)` honesty notice.
3. **`UI-NEW-P03_03_RESEARCH_ANNOTATION_MODAL.png`**:
   - URL: `http://localhost:5173/` (Click `+ Note` button)
   - Must show: Research annotation dialog with note text area, price level input, and research-only disclaimer.
4. **`UI-NEW-P03_04_LOGGED_OUT_REDIRECT.png`**:
   - URL: `http://localhost:5173/` (Logged out / unauthenticated)
   - Must show: Route `/` correctly blocked and redirected to `/login` (discharging B-P03-6).

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
1. `DELIVERY_REPORT_UI-NEW-P03.md`
2. `UI-NEW-P03_OPERATOR_EVIDENCE_COMMANDS.md`
3. 1920×1080 browser screenshots from §11
4. Verified Git commit SHA & tag (`UI-NEW-P03_DELIVERY`)

---

**End of UI-NEW-P03_OPERATOR_EVIDENCE_COMMANDS.md**
