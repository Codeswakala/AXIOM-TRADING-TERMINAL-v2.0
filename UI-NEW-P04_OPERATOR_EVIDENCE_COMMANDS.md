# UI-NEW-P04 Operator Evidence Commands

## Quantitative Signals, Intelligence & Uncertainty Stream

Run from the operator Windows target unless otherwise stated:

```powershell
cd C:\Users\Swakala\.vscode\AXIOM\axiom
$ErrorActionPreference = "Stop"
```

Optional transcript wrapper:

```powershell
Start-Transcript -Path docs\evidence\UI-NEW-P04_OPERATOR_RESULTS.txt -Force
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
Get-Content DELIVERY_REPORT_UI-NEW-P04.md -TotalCount 25
git rev-parse HEAD
git rev-parse --verify UI-NEW-P04_DELIVERY

Get-FileHash -Algorithm SHA256 `
  frontend\src\components\terminal\TerminalSignalStream.tsx, `
  frontend\src\components\terminal\TerminalIntelligenceCards.tsx, `
  frontend\src\components\terminal\TerminalChartStage.tsx, `
  frontend\src\components\terminal\TradingTerminalWorkspace.tsx, `
  frontend\src\components\terminal\TerminalMultiPane.css, `
  frontend\src\components\terminal\index.ts, `
  frontend\src\api\client.ts, `
  frontend\src\terminal\terminalSignalsIntelligence.test.tsx, `
  frontend\src\test\uinew_p04_security_invariants.test.ts, `
  docs\governance\GOVERNANCE_AMENDMENTS.md, `
  PROJECT_STATE.md, `
  CHANGELOG.md, `
  docs\plans\UI-NEW_ENGINEERING_DESIGN_PLAN.md | Format-Table -AutoSize
```

Expected SHA-256 for Master Plan:
`8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308`

---

## 2. Seven mandatory named UI-NEW-P04 tests — display passing by name

```powershell
cd frontend
npm test -- --run --reporter=verbose src/terminal/terminalSignalsIntelligence.test.tsx src/test/uinew_p04_security_invariants.test.ts
cd ..
```

Required test names to be displayed passing:

```text
test_uinew_p04_signal_stream_renders_only_backend_signals_with_no_client_fabrication
test_uinew_p04_calibrated_confidence_never_renders_without_uncertainty_or_explicit_unavailable
test_uinew_p04_no_client_side_computation_of_ece_brier_wilson_or_correlation
test_uinew_p04_signal_direction_renders_with_state_and_never_as_instruction
test_uinew_p04_withheld_expired_and_superseded_signals_remain_visible_and_distinct
test_uinew_p04_stale_and_expired_signals_are_explicitly_marked_with_absolute_utc_time
test_uinew_p04_model_version_feature_set_and_input_hash_render_for_every_signal
```

---

## 3. T-1 zero-actuation & non-imperative language audit

```powershell
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern '\b(buy|sell|place_order|submit_order|order_ticket|execute|connect-broker|account_id|position|balance|margin|open_gate|allow_execution)\b'
Write-Host "Expected: no output above (0 functional actuation matches in terminal components)."
```

---

## 4. T-4 / T-5 zero-external-LLM grep audit

```powershell
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern 'openai|anthropic|langchain|gpt|claude|external_llm|llm_summary|ai_summary|api\.openai|remote_prompt'
Write-Host "Expected: no output above (0 external AI SDK imports in terminal module)."

git diff frontend/package.json
Write-Host "Expected: no output above (package dependencies unchanged)."
```

---

## 5. B-P04-1 Uncertainty Discipline & B-P04-2 Zero Client-Side Stats Verification

```powershell
cd frontend
npm test -- --run --reporter=verbose -t "test_uinew_p04_calibrated_confidence_never_renders_without_uncertainty_or_explicit_unavailable"
npm test -- --run --reporter=verbose -t "test_uinew_p04_no_client_side_computation_of_ece_brier_wilson_or_correlation"
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

Get-ChildItem frontend\src\components\terminal,frontend\src\components\chart,frontend\src\pages\ChartWorkspacePage.tsx -Recurse -File -Include *.css,*.tsx |
  Select-String -Pattern '#[0-9A-Fa-f]{3,8}'
Write-Host "Expected: no output above (0 ad-hoc hex literals across all touched files)."

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
- Frontend: **156 test files / 668 tests passed** (100%)
- TypeScript: Clean (exit 0)
- Vite build: Clean (exit 0, `dist/assets/index-B7UyJjBO.js` 685.23 kB)

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
- `415 passed, 1 warning`

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

Capture the following five screenshots at 1920×1080 viewport (BO §10(f)):

1. **`UI-NEW-P04_01_SIGNAL_STREAM_WITH_UNCERTAINTY.png`**:
   - URL: `http://localhost:5173/` (Logged in, right-dock tab: `SIGNALS`)
   - Must show: Right dock displaying `TerminalSignalStream` with at least one `emitted` signal showing calibrated confidence with Wilson score interval (e.g. `78.4% · Wilson: [72.4% – 84.1%]`) and non-actuating research disclaimer.
2. **`UI-NEW-P04_02_WITHHELD_OR_EXPIRED_SIGNAL.png`**:
   - URL: `http://localhost:5173/` (Click `WITHHELD` or `EXPIRED` filter chip)
   - Must show: Withheld or expired signal card with distinct amber/red visual styling, state rationale, and absolute UTC time.
3. **`UI-NEW-P04_03_CHART_SIGNAL_OVERLAYS_OVER_SEEDED_WALK.png`**:
   - URL: `http://localhost:5173/` (Chart Stage center)
   - Must show: Candlestick chart rendering the non-degenerate seeded series with visual signal marker chips overlaid at the top of the canvas.
4. **`UI-NEW-P04_04_INTELLIGENCE_CARDS_CALIBRATION_CORRELATION.png`**:
   - URL: `http://localhost:5173/` (Right-dock tab: `INTELLIGENCE`)
   - Must show: Calibration card with server-validated ECE and Brier score, and Correlation card with Pearson `r` and Fisher Z confidence interval.
5. **`UI-NEW-P04_05_SIGNAL_UNCERTAINTY_UNAVAILABLE_QUALIFIER.png`**:
   - URL: `http://localhost:5173/` (Signal without linked validation report)
   - Must show: Explicit `62.5% · [Uncertainty: Unavailable]` qualifier.

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
1. `DELIVERY_REPORT_UI-NEW-P04.md`
2. `UI-NEW-P04_OPERATOR_EVIDENCE_COMMANDS.md`
3. Five 1920×1080 browser screenshots from §11
4. Verified Git commit SHA & tag (`UI-NEW-P04_DELIVERY`)

---

**End of UI-NEW-P04_OPERATOR_EVIDENCE_COMMANDS.md**
