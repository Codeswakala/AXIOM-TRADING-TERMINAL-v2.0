# UI-NEW-P05 Operator Evidence Commands

## Risk, Portfolio Analytics & Research Journal

Run from the operator Windows target unless otherwise stated:

```powershell
cd C:\Users\Swakala\.vscode\AXIOM\axiom
$ErrorActionPreference = "Stop"
```

Optional transcript wrapper:

```powershell
Start-Transcript -Path docs\evidence\UI-NEW-P05_OPERATOR_RESULTS.txt -Force
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
Get-Content DELIVERY_REPORT_UI-NEW-P05.md -TotalCount 25
git rev-parse HEAD
git rev-parse --verify UI-NEW-P05_DELIVERY

Get-FileHash -Algorithm SHA256 `
  frontend\src\components\terminal\TerminalBottomDock.tsx, `
  frontend\src\components\terminal\TerminalSignalStream.tsx, `
  frontend\src\components\terminal\TerminalIntelligenceCards.tsx, `
  frontend\src\components\terminal\TerminalChartStage.tsx, `
  frontend\src\components\terminal\TerminalMarketTelemetry.tsx, `
  frontend\src\components\terminal\TradingTerminalWorkspace.tsx, `
  frontend\src\components\terminal\TerminalMultiPane.css, `
  frontend\src\components\terminal\index.ts, `
  frontend\src\api\client.ts, `
  frontend\src\terminal\terminalRiskJournal.test.tsx, `
  frontend\src\terminal\terminalSignalsIntelligence.test.tsx, `
  frontend\src\terminal\terminalWatchlistDepth.test.tsx, `
  frontend\src\test\uinew_p05_security_invariants.test.ts, `
  docs\governance\GOVERNANCE_AMENDMENTS.md, `
  PROJECT_STATE.md, `
  CHANGELOG.md, `
  docs\plans\UI-NEW_ENGINEERING_DESIGN_PLAN.md | Format-Table -AutoSize
```

Expected SHA-256 for Master Plan:
`8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308`

---

## 2. Eight mandatory named UI-NEW-P05 tests — display passing by name

```powershell
cd frontend
npm test -- --run --reporter=verbose src/terminal/terminalRiskJournal.test.tsx src/test/uinew_p05_security_invariants.test.ts
cd ..
```

Required test names to be displayed passing:

```text
test_uinew_p05_trade_plan_form_exposes_no_price_stop_target_size_or_side_fields
test_uinew_p05_trade_plans_and_journal_entries_render_disclaimer_and_audit_correlation_id
test_uinew_p05_edited_records_visibly_disclose_updated_at_distinct_from_created_at
test_uinew_p05_risk_metrics_never_render_without_uncertainty_or_explicit_unavailable
test_uinew_p05_stress_loss_renders_with_its_assumptions_and_sample_window
test_uinew_p05_no_client_side_computation_of_drawdown_volatility_or_stress_values
test_uinew_p05_failed_writes_render_explicit_error_and_never_optimistic_success
test_uinew_p05_every_rendered_interval_brackets_its_own_point_estimate
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

## 5. B-P05-1 Trade Plan Purity & B-P05-2 Risk Uncertainty Verification

```powershell
cd frontend
npm test -- --run --reporter=verbose -t "test_uinew_p05_trade_plan_form_exposes_no_price_stop_target_size_or_side_fields"
npm test -- --run --reporter=verbose -t "test_uinew_p05_risk_metrics_never_render_without_uncertainty_or_explicit_unavailable"
npm test -- --run --reporter=verbose -t "test_uinew_p05_every_rendered_interval_brackets_its_own_point_estimate"
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
- Frontend: **158 test files / 686 tests passed** (100%)
- TypeScript: Clean (exit 0)
- Vite build: Clean (exit 0, `dist/assets/index-CVVoXKT4.js` 712.99 kB)

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

1. **`UI-NEW-P05_01_TRADE_PLANS_TAB.png`**:
   - URL: `http://localhost:5173/` (Logged in, bottom dock tab: `TRADE_PLANS`)
   - Must show: Bottom dock displaying trade plans list with at least one plan showing `research_disclaimer` and `audit_correlation_id`.
2. **`UI-NEW-P05_02_TRADE_PLAN_CREATE_FORM.png`**:
   - URL: `http://localhost:5173/` (Click `+ New Trade Plan`)
   - Must show: Create trade plan modal form showing research hypothesis, context, invalidating conditions, decision status, and ZERO price/stop/size/side fields.
3. **`UI-NEW-P05_03_RESEARCH_JOURNAL_EDITED_ENTRY.png`**:
   - URL: `http://localhost:5173/` (Bottom dock tab: `JOURNAL`)
   - Must show: Research journal tab with an edited entry (`journ-002` or `plan-002`) visibly disclosing `[EDITED]` and `updated_at`.
4. **`UI-NEW-P05_04_RISK_AND_DRAWDOWN_TAB.png`**:
   - URL: `http://localhost:5173/` (Bottom dock tab: `RISK`)
   - Must show: Risk & Drawdown tab displaying `max_drawdown`, `realized_volatility`, and `stress_loss` with uncertainty intervals bracketing their point estimates, plus model assumptions box accessible without navigation.
5. **`UI-NEW-P05_05_MACRO_SCENARIOS_OR_WRITE_FAILURE.png`**:
   - URL: `http://localhost:5173/` (Bottom dock tab: `SCENARIOS`)
   - Must show: Macro Scenarios tab with hypothetical shock simulations and assumptions.

Save screenshots to `docs/evidence/uinew/` and `/home/user/uploads/`.

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
1. `DELIVERY_REPORT_UI-NEW-P05.md`
2. `UI-NEW-P05_OPERATOR_EVIDENCE_COMMANDS.md`
3. Five 1920×1080 browser screenshots from §11
4. Verified Git commit SHA & tag (`UI-NEW-P05_DELIVERY`)

---

**End of UI-NEW-P05_OPERATOR_EVIDENCE_COMMANDS.md**
