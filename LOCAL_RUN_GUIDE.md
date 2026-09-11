# AXIOM — LOCAL LAUNCH & RENDER-VERIFICATION GUIDE

**For the Operator's machine.** Every command below was executed cold in the
DA's environment on 2026-08-19 and verified end-to-end (login → terminal →
timeframes → indicators → confluence → lazy routes → stage views, zero page
errors). The artifact of record is the verified patch chain, not a commit.

---

## 0. What you need

| Tool | Version verified |
|---|---|
| git | any modern (2.30+) |
| Node.js | 20.x (verified 20.20.2) |
| npm | 10.x (verified 10.8.2) |
| Python | 3.13 (verified 3.13.14) — 3.11+ works |

No Docker required. No database server required — the backend uses a local
SQLite file. No network dependency beyond npm/pip package registries and
GitHub.

## 1. One-time setup (first run only)

```bash
# 1. Clone the repository
git clone https://github.com/Codeswakala/AXIOM-TRADING-TERMINAL-v1.0.git axiom-local
cd axiom-local

# 2. Check out the clean development baseline
git checkout 34f4c62dbef11e685de965415b4b8ab697cef487

# 3. Apply the verified patch chain — IN THIS ORDER (the artifact of record).
#    Copy the 16 *.patch.txt files into the repo root first, then:
for p in \
  item3 item5 item6 item4 \
  surf_p01 surf_p01_obs1-2 surf_p02 surf_p03 \
  data_p01 data_p01_correction data_p01_correction2 data_p02 \
  chart_p01 chart_p02 chart_p03 polish_p01; do
  git apply --check "$p.patch.txt" || { echo "APPLY CHECK FAILED: $p"; exit 1; }
  git apply "$p.patch.txt"
done
echo "16-element chain applied clean"

# 4. (Post-closure hotfix — recommended, see §5)
#    Fixes a chart-stage crash on timeframe switching with no live feed.
git apply --check postclosure_hotfix.patch.txt && git apply postclosure_hotfix.patch.txt

# 4b. (Post-closure brand — the Operator-supplied logo, see §6)
git apply --check postclosure_brand.patch.txt && git apply postclosure_brand.patch.txt

# 5. Backend environment
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# 6. Create the local environment file (copy the delivered .env.example and
#    keep these keys):
#      AXIOM_ALLOW_INSECURE_DEV=true
#      AXIOM_BOOTSTRAP_ADMIN_ENABLED=true
#      AXIOM_BOOTSTRAP_ADMIN_USERNAME=admin
#      AXIOM_BOOTSTRAP_ADMIN_PASSWORD=AxiomSecurePass2026!
#      AXIOM_LIVE_MARKET_SYMBOLS=EURUSD,GBPUSD,USDJPY,AUDUSD,USDCAD,USDCHF,NZDUSD,EURGBP,BTCUSD,ETHUSD,SOLUSD
cp .env.example .env     # then edit .env to match the lines above if needed

# 7. Frontend dependencies
cd ../frontend
npm ci --no-audit --no-fund
```

> **Why no commits?** The governance correction (`ITRGA_GOVERNANCE_CORRECTION_REPOSITORY_ROLE.md`)
> established that the repo is Operator-only storage; the verified patch is the
> artifact of record. Applying patches into your working tree exactly
> reproduces the reviewed state — nothing needs committing. If you prefer a
> commit on your own clone for convenience, that is your call as Operator; the
> DA makes none.

## 2. Launch

Two terminals.

```bash
# Terminal 1 — backend (from backend/)
cd axiom-local/backend
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2 — frontend (from frontend/)
cd axiom-local/frontend
./node_modules/.bin/vite --host 0.0.0.0 --port 5173
```

Open **http://localhost:5173** in a browser.

**Login:**
- username `admin` · password `AxiomSecurePass2026!`
- seeded role accounts (`operator-pass-123`): `w7-u06-a-0a16e141` (operator),
  `w7-u06-b-c3290abc` (operator), `surf-p03-unprivileged-028efc57` (unprivileged)

## 3. What to click — the render checklist (verified 2026-08-19, zero page errors)

| # | Do this | Expect |
|---|---|---|
| 1 | Open `/login` | Split-screen sign-in; **drawing-compass + epsilon logo** top-left; governance chips (GATE: CLOSED · RESEARCH-ONLY · NON-ACTUATING) |
| 2 | Log in as admin | Terminal workspace: watchlist with **11 price rows**, candlestick chart, session-context strip, 6 drawing tools, 5 indicator engine menus |
| 3 | Watchlist | Prices + `LIVE:SIMULATED`/`SEED:SYNTHETIC` provenance chips + sparklines; BTC's row fully inside its column |
| 4 | Click `1H` then `1D` then `1M` | Honest notice each time ("Resampled from M1 stream · wall-clock aligned 60-minute buckets…"), hourly/daily bars, clean return to "Native M1 Stream" |
| 5 | Click `SMA 20`, then a Momentum menu → `RSI 14` | Real overlay line + a separate RSI pane below the chart; the **EVIDENCE CONFLUENCE** strip appears (score · uncertainty band · NON-ACTUATING) |
| 6 | Draw: select `Trendline`, click two points on the chart | Drawing persists at its price/time anchors; switch `1M → 1H → 1M` and it returns to the same bars (absent on 1H by design — scoped per timeframe) |
| 7 | Menu `MarketStructure` → `Swings` / `BOS` | Zones/lines appear with the disclosure "Geometric pattern detection over simulated OHLC — not evidence of institutional activity or order placement." |
| 8 | Visit `/intelligence` as admin | Intelligence workspace loads (lazy chunk) |
| 9 | Log out; log in as `surf-p03-unprivileged-028efc57`; visit `/intelligence` | **ACCESS DENIED — "This is an access restriction, not an empty result."** |
| 10 | Visit `/?view=research` and `/?view=execution` | Research Hub stage and Execution Research stage render |
| 11 | Start the feed (top-right `Start Feed`) | Prices tick; live provenance appears; stop it anytime |

## 4. Running the test suites (optional but complete)

```bash
# Backend — 476 tests (~2 min)
cd axiom-local/backend
AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' \
AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true \
AXIOM_JWT_SECRET_KEY='local-test-secret-key-at-least-32-chars-!!' \
AXIOM_ALLOW_INSECURE_DEV=true \
AXIOM_ENVIRONMENT=testing \
.venv/bin/python -m pytest -q

# Frontend — 175 files / 860 tests (~3.5 min)
cd ../frontend
npx vitest run

# Type check + production build (initial chunk ≈ 626.6 kB, 6 lazy route chunks)
./node_modules/.bin/tsc -b --force --pretty false
npm run build
npm run preview -- --host 0.0.0.0 --port 4173   # serve the production build
```

## 5. The post-closure hotfix — disclosed

While executing this verification at your request, the DA found one latent
defect in the delivered chain and fixed it:

- **Symptom:** on a fresh machine with the live feed never started, switching
  the chart timeframe `1m → 1h` (or `1d`) crashed the whole chart stage
  ("Cannot update oldest data" — lightweight-charts rejects updating with an
  older bar time).
- **Root cause:** the chart's incremental update path only detected series
  *length* changes. Switching to a longer timeframe always *regresses* the
  last-bar time, because the DATA-P02 partial-bucket rule excludes the
  still-forming bucket. The approved captures masked this because the live
  quote merged into the native series changed its length, forcing a reset.
- **Fix (defect class, not the cited line):** the reset condition now also
  fires when the new series' last bar time is older than the previous series'
  last bar time. `frontend/src/components/chart/PriceChart.tsx` only, plus a
  fail-first source-pin test. Nothing else changed.
- **Artifact:** `postclosure_hotfix.patch` — sha256
  `002eee83ae75fd94d922bede27c4917a660551e140507b6540b99d078a4015a2`
  (61 lines, 2 files, LF, terminating newline; applies clean as the 17th
  element of the chain in a pristine clone). The suite re-ran after the fix:
  **476 backend / 860 frontend, tsc 0** — and the full browser smoke test in
  §3 passed with **zero page errors**. Route it to ITRGA if you want it on the
  reviewed record; it is not required for the terminal to run.

## 6. The logo — post-closure Operator directive (2026-08-19)

The logo the Operator supplied (`Screenshot 2026-08-19 104729.png`, 410×408) is
wired in as the project mark at `frontend/public/branding/axiom-logo.png` —
rendered on the login page and the shell header, used exactly as provided (no
cropping). `postclosure_brand.patch` sha256
`f4c08e41d9be28cd7ad829cb71d0a6b25319d6ea18e600be39b2a9c46e2a185c`
includes the image as a binary patch, so a pristine-clone apply reproduces it
byte-identical to the upload. The GA-173 compass+epsilon SVG remains only as a
load-failure fallback. If you want the mark cropped/resized/padded, tell me and
send a clean export — the DA applies assets exactly as provided.

## 7. Known sandbox-only quirks (NOT expected on your machine)

These occurred only in the DA's ephemeral sandbox and are documented for
completeness — a normal local machine does not exhibit them:
- `node_modules`, `.venv` and the Playwright browser binary drop between
  sessions (recreated by the commands above).
- The sandbox wall clock can jump hours between operations, which ages JWTs
  and makes the live feed outgrow seeded windows (re-login / re-seed fixes it).
- One SQLite `no such savepoint` audit line (TD-031 dev-harness class) can
  appear under concurrent load; logins still succeed.

---

Gate **CLOSED** · Production **NOT CERTIFIED**.
Programme status: **CLOSED** — all authorized phases approved
(`ITRGA_PROGRAMME_CLOSURE.md`, 2026-08-18). This guide is operator-facing
documentation of the delivered state, not new implementation authority.

**We don't guess. We prove.**
