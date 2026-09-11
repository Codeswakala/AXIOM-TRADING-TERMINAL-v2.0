# AXIOM — POWERSHELL LAUNCH & VERIFICATION GUIDE (Windows)

**For the Operator's Windows machine.** Mirrors `LOCAL_RUN_GUIDE.md` (bash/Linux).
Every command below is the PowerShell equivalent of the sequence the DA executed
and verified on 2026-08-19 (login → terminal → timeframes → indicators →
confluence → lazy routes → stage views, zero page errors), plus the
Operator-supplied logo.

---

## 0. Prerequisites

| Tool | Version verified |
|---|---|
| Git | any modern (2.30+) — `git --version` |
| Node.js | 20.x — `node -v` |
| npm | 10.x — `npm -v` |
| Python | 3.11+ (verified on 3.13) — `python --version` |

No Docker, no database server — the backend uses a local SQLite file.

## 1. One-time setup (PowerShell)

```powershell
# 1. Clone and check out the clean development baseline
git clone https://github.com/Codeswakala/AXIOM-TRADING-TERMINAL-v1.0.git axiom-local
Set-Location axiom-local
git checkout 34f4c62dbef11e685de965415b4b8ab697cef487

# 2. Copy the patch files (*.patch.txt) into the repo root, then apply the
#    verified chain IN THIS ORDER — the artifact of record:
$patches = @(
  "item3", "item5", "item6", "item4",
  "surf_p01", "surf_p01_obs1-2", "surf_p02", "surf_p03",
  "data_p01", "data_p01_correction", "data_p01_correction2", "data_p02",
  "chart_p01", "chart_p02", "chart_p03", "polish_p01"
)
foreach ($p in $patches) {
  git apply --check "$p.patch.txt"
  if ($LASTEXITCODE -ne 0) { throw "APPLY CHECK FAILED: $p" }
  git apply "$p.patch.txt"
  if ($LASTEXITCODE -ne 0) { throw "APPLY FAILED: $p" }
}
Write-Host "16-element chain applied clean"

# 3. Post-closure hotfix (timeframe-switch crash fix — recommended, see guide §5)
git apply --check postclosure_hotfix.patch.txt
git apply postclosure_hotfix.patch.txt

# 4. Post-closure brand (the Operator-supplied logo, see guide §6)
git apply --check postclosure_brand.patch.txt
git apply postclosure_brand.patch.txt

# 5. Backend environment
Set-Location backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env   # ensure these keys are present (see below)

# 6. Frontend dependencies
Set-Location ..\frontend
npm ci --no-audit --no-fund
```

**Required `.env` keys** (edit `backend\.env`):
```
AXIOM_ALLOW_INSECURE_DEV=true
AXIOM_BOOTSTRAP_ADMIN_ENABLED=true
AXIOM_BOOTSTRAP_ADMIN_USERNAME=admin
AXIOM_BOOTSTRAP_ADMIN_PASSWORD=AxiomSecurePass2026!
AXIOM_LIVE_MARKET_SYMBOLS=EURUSD,GBPUSD,USDJPY,AUDUSD,USDCAD,USDCHF,NZDUSD,EURGBP,BTCUSD,ETHUSD,SOLUSD
```

> **Why no commits?** The repo is Operator-only storage (governance correction
> `ITRGA_GOVERNANCE_CORRECTION_REPOSITORY_ROLE.md`); the verified patch is the
> artifact of record. The DA makes no commits — on your own clone, committing is
> your call.

## 2. Launch — two PowerShell windows

```powershell
# Window 1 — backend (from ...\axiom-local\backend)
.\.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000
#   (if the execution policy blocks it:
#    Set-ExecutionPolicy -Scope Process Bypass
#    .\.venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000)

# Window 2 — frontend (from ...\axiom-local\frontend)
npm run dev -- --host 0.0.0.0 --port 5173
```

Open **http://localhost:5173** in a browser.

**Login:** `admin` / `AxiomSecurePass2026!`
Role accounts (password `operator-pass-123`): `w7-u06-a-0a16e141` (operator),
`w7-u06-b-c3290abc` (operator), `surf-p03-unprivileged-028efc57` (unprivileged).

## 3. Render checklist (verified 2026-08-19, zero page errors)

| # | Do this | Expect |
|---|---|---|
| 1 | Open `/login` | Split-screen sign-in with **the Operator-supplied logo** top-left and the governance chips (GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING) |
| 2 | Log in as admin | Terminal: 11 watchlist price rows, candlestick chart, session strip, 6 drawing tools, 5 indicator menus, the logo in the shell header |
| 3 | Click `1H` → `1D` → `1M` | Honest notices ("Resampled from M1 stream · wall-clock aligned …-minute buckets"), clean return to "Native M1 Stream" |
| 4 | Click `SMA 20`, then Momentum menu → `RSI 14` | Real overlay line + RSI pane + **EVIDENCE CONFLUENCE** strip (score · uncertainty · NON-ACTUATING) |
| 5 | Draw a `Trendline` on the chart; switch `1M → 1H → 1M` | Drawing returns to the same anchors (absent on 1H by design) |
| 6 | MarketStructure menu → `Swings`/`BOS` | Detections + the disclosure "…not evidence of institutional activity or order placement." |
| 7 | Log in as `surf-p03-unprivileged-028efc57`; open `/intelligence` | **ACCESS DENIED** — "an access restriction, not an empty result." |
| 8 | `/?view=research` and `/?view=execution` | Research Hub and Execution Research stage views render |

## 4. Test suites and build (PowerShell)

```powershell
# Backend — 476 tests (~2 min)
Set-Location backend
$env:AXIOM_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
$env:AXIOM_DATABASE_AUTO_CREATE_SCHEMA = "true"
$env:AXIOM_JWT_SECRET_KEY = "local-test-secret-key-at-least-32-chars-!!"
$env:AXIOM_ALLOW_INSECURE_DEV = "true"
$env:AXIOM_ENVIRONMENT = "testing"
.\.venv\Scripts\python -m pytest -q

# Frontend — 175 files / 860 tests (~3.5 min)
Set-Location ..\frontend
npm test                # == vitest run

# Type check + production build (initial chunk ~626.7 kB, lazy route chunks)
npm run lint            # == tsc -b --pretty false
npm run build
npm run preview -- --host 0.0.0.0 --port 4173   # production build at http://localhost:4173
```

## 5. The post-closure hotfix — disclosed

Found while the DA verified your local-run request (2026-08-19): on a fresh
machine with the live feed never started, switching `1m → 1h`/`1d` crashed the
chart stage ("Cannot update oldest data"). Cause: the incremental update path
detected only series-LENGTH changes, but a longer timeframe always REGRESSES the
last-bar time (the DATA-P02 partial-bucket rule excludes the forming bucket).
Fix: the reset now also fires on last-bar time regression — `PriceChart.tsx`
only, plus a pin test. `postclosure_hotfix.patch` sha256
`002eee83ae75fd94d922bede27c4917a660551e140507b6540b99d078a4015a2`.

## 6. The logo — post-closure Operator directive

The logo you supplied (`Screenshot 2026-08-19 104729.png`, 410×408) is wired in
as the project mark at `frontend/public/branding/axiom-logo.png`, rendered on the
login page and the shell header — used exactly as provided (no cropping).
`postclosure_brand.patch` sha256
`f4c08e41d9be28cd7ad829cb71d0a6b25319d6ea18e600be39b2a9c46e2a185c`
includes the image (binary patch) so the pristine clone reproduces it
byte-identical. The GA-173 compass+epsilon SVG remains only as a fallback if the
image ever fails to load.

> If you'd like the mark cropped, resized, or given padding/rounding, tell me
> what you want and send a clean export — the DA applies the asset exactly as
> provided and cannot judge artwork visually.

---

Gate **CLOSED** · Production **NOT CERTIFIED** · Programme **CLOSED**
(all authorized phases approved — `ITRGA_PROGRAMME_CLOSURE.md`, 2026-08-18).
The hotfix and brand patches are post-closure Operator-directed items, not
ITRGA-reviewed phases.

**We don't guess. We prove.**
