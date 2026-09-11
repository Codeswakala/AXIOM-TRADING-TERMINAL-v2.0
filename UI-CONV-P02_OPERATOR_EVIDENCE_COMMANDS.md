# UI-CONV-P02 Operator Evidence Commands

## Duplicate Surface Absorption & Single Statistical Code Path

Run from the operator Windows target unless otherwise stated:

```powershell
cd C:\Users\Swakala\.vscode\AXIOM\axiom
$ErrorActionPreference = "Stop"
```

Optional transcript wrapper:

```powershell
Start-Transcript -Path docs\evidence\UI-CONV-P02_OPERATOR_RESULTS.txt -Force
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
Get-Content DELIVERY_REPORT_UI-CONV-P02.md -TotalCount 25
git rev-parse HEAD
git rev-parse --verify UI-CONV-P02_DELIVERY

Get-FileHash -Algorithm SHA256 `
  frontend\src\components\terminal\StatisticalValueRenderer.tsx, `
  frontend\src\components\terminal\TerminalSignalStream.tsx, `
  frontend\src\components\terminal\TradingTerminalWorkspace.tsx, `
  frontend\src\components\chart\PriceChart.tsx, `
  frontend\src\workstation\registry\workspaceRegistry.tsx, `
  frontend\src\test\uiconv_p02_absorption.test.tsx, `
  frontend\src\test\uiconv_p02_security_invariants.test.ts, `
  scripts\capture_conv_p02_evidence.mjs, `
  docs\governance\TECHNICAL_DEBT_REGISTER.md, `
  docs\governance\GOVERNANCE_AMENDMENTS.md, `
  PROJECT_STATE.md, `
  CHANGELOG.md | Format-Table -AutoSize
```

---

## 2. Eight mandatory named UI-CONV-P02 tests — display passing by name

```powershell
cd frontend
npm test -- --run --reporter=verbose src/test/uiconv_p02_absorption.test.tsx src/test/uiconv_p02_security_invariants.test.ts
cd ..
```

Required test names to be displayed passing:

```text
test_uiconv_p02_calibrated_confidence_renders_through_exactly_one_shared_component
test_uiconv_p02_no_bare_confidence_percentage_renders_anywhere_in_frontend
test_uiconv_p02_every_rendered_interval_brackets_its_own_point_estimate
test_uiconv_p02_retired_routes_redirect_to_terminal_with_correct_dock_active
test_uiconv_p02_signal_detail_exposes_rationale_guardrails_lineage_and_explainability
test_uiconv_p02_every_retired_page_capability_has_a_verified_new_home
test_uiconv_p02_seed_and_live_provenance_labels_survive_absorption
test_uiconv_p02_zero_adhoc_hex_across_whole_frontend_outside_tokens_css
```

---

## 3. Single statistical path & bracketing invariants (B-CONV2-1)

```powershell
# Verify StatisticalValueRenderer is the single source of truth for calibrated confidence & intervals
Select-String -Path frontend\src\components\terminal\StatisticalValueRenderer.tsx -Pattern 'export function CalibratedConfidenceBadge|export function MetricWithInterval|isBracketed'
Write-Host "Expected: CalibratedConfidenceBadge and MetricWithInterval exported with strict bracketing check."

# Verify legacy formatters are deleted
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern '\bformatConfidence\b|\bintervalText\b'
Write-Host "Expected: 0 matches outside tests or legacy archival references."
```

---

## 4. Programme-scope safety & token audits (B-CONV2-3 / B-CONV2-4)

```powershell
# 1. T-1 Actuation audit
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern '\b(place_order\(|submit_order\(|order_ticket\(|connect_broker\(|open_gate\(|allow_execution\()\b'
Write-Host "Expected: no functional actuation invocations across terminal components."

# 2. C-1 Order book / depth ladder audit
Get-ChildItem frontend\src\components\terminal -Recurse -File -Include *.tsx,*.ts |
  Select-String -Pattern 'depth_ladder|orderbook|bid_size|ask_size'
Write-Host "Expected: no output above (0 order book or depth ladder rendering in terminal)."

# 3. T-4 External LLM audit
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts,*.css |
  Select-String -Pattern 'api\.openai\.com|api\.anthropic\.com|from ["\x27]openai["\x27]|from ["\x27]@anthropic-ai["\x27]|from ["\x27]langchain["\x27]'
Write-Host "Expected: no output above (0 external LLM SDK imports in source)."

# 4. Ad-hoc hex audit across whole frontend source
Get-ChildItem frontend\src -Recurse -File -Include *.tsx,*.ts,*.css -Exclude tokens.css |
  Where-Object { $_.Name -notmatch '\.test\.' } |
  Select-String -Pattern '#[0-9A-Fa-f]{3,8}\b'
Write-Host "Expected: no output above (0 ad-hoc hex literals across whole frontend source)."
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
- Frontend: **164 test files / 741 tests passed** (100%)
- TypeScript: Clean (exit 0)
- Vite build: Clean (exit 0, `dist/assets/index-BNDuTlcT.js` 681.93 kB — **36.52 kB reduction from CONV-P01**)

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

Capture the following six screenshots at 1920×1080 viewport (BO §9(f)):

1. **`UI-CONV-P02_01_TERMINAL_SIGNALS_DRILLDOWN.png`**:
   - URL: `http://localhost:5173/` (Terminal workstation with SIGNALS dock open and active signal card expanded showing full lineage, rationale, guardrails, and feature attribution).
2. **`UI-CONV-P02_02_INTELLIGENCE_DOCK_CALIBRATION.png`**:
   - URL: `http://localhost:5173/` (Terminal workstation with INTELLIGENCE dock active, showing calibration metrics with Wilson intervals, correlation matrix, and regime classification).
3. **`UI-CONV-P02_03_SIGNALS_REDIRECT_TERMINAL.png`**:
   - URL: `http://localhost:5173/signals` (Deep link `/signals` redirecting to `/?dock=signals` with SIGNALS dock active).
4. **`UI-CONV-P02_04_CHART_STAGE_SEEDED_PROVENANCE.png`**:
   - URL: `http://localhost:5173/?view=chart` (Chart stage with seeded synthetic history, technical overlays, and provenance badges).
5. **`UI-CONV-P02_05_COMMAND_PALETTE_EMPTY_QUERY.png`**:
   - URL: `http://localhost:5173/` (Command palette open via `Ctrl+K` with **empty query**, displaying all 16 routes grouped by category — closes OBS-CONV-3).
6. **`UI-CONV-P02_06_PREFERS_REDUCED_MOTION_LOGIN.png`**:
   - URL: `http://localhost:5173/login` (Sign-in surface rendered under `prefers-reduced-motion: reduce` — closes OBS-CONV-2).

Save screenshots to `docs/evidence/uiconv/` and `/home/user/uploads/`.

---

## 9. Submission package checklist

Attach:
1. `DELIVERY_REPORT_UI-CONV-P02.md`
2. `UI-CONV-P02_OPERATOR_EVIDENCE_COMMANDS.md`
3. Six 1920×1080 browser screenshots from §8
4. Verified Git commit SHA & tag (`UI-CONV-P02_DELIVERY`)

---

**End of UI-CONV-P02_OPERATOR_EVIDENCE_COMMANDS.md**
