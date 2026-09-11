# DA Response to ITRGA Review — W0-U07

| Item | Value |
|------|--------|
| Review | `ITRGA_REVIEW_W0-U07.md` |
| Verdict received | **PASS WITH OBSERVATIONS — CONDITIONAL** (approval withheld) |
| Date recorded | 2026-07-11 |
| Authority | Development Authority |

---

## 1. Verdict acknowledgement

The Development Authority **accepts** the ITRGA disposition:

- U07 is **not approved** until the mandated Level-I evidence set (C-1) is complete.
- Engineering is credited as sound; governance posture is clean.
- **W0-U08 must not be issued** by DA and will not be started without a new Build Order after approval.

---

## 2. Corrections status

| ID | Requirement | DA action | Owner for remaining proof |
|----|-------------|-----------|---------------------------|
| **C-1** | Full §6.2 evidence: multi-frame live, EURUSD frame, logged-out gate, operator pytest/vitest/tsc console | **Cannot complete in DA headless sandbox.** Checklist prepared for Operator (below). DA-run tests remain: backend 55, frontend 16. | **Operator** (Level-I browser + local console) |
| **C-2** | Synthetic seed non-authoritative marker | **Code fix applied:** DB already stores `source=seed:synthetic`; UI now shows **Data provenance** banner + per-source counts after seed/start/reload. | ITRGA re-verify in browser |
| **C-3** | Canonical chart route | **Canonical path = `/charts`**. Alias `/chart` also serves the same page. Docs/PROJECT_STATE aligned. | Confirmed |
| **R-1** | Legible default viewport | **Code fix applied:** default visible logical range ≈ last **80** bars (not full fit of 200+). | Operator zoomed-in screenshot optional |
| **R-2** | Source excerpts for §30 | Provided in §4 below | ITRGA code review |
| **R-3** | Logged-out `/live` screenshot | Same Operator capture list as C-1 | Operator |

---

## 3. Operator capture checklist (C-1) — PowerShell + browser

### 3.1 Operator-run test console (required)

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q

cd ..\frontend
npm test
npx tsc -b --pretty false
```

Capture full terminal output including collection/pass counts.

### 3.2 Browser screenshots (required)

With server running (`npm run build` then uvicorn on port 8000):

1. **Historical render** — `/charts` with bars visible (already have similar).  
2. **Live frame A** — note timestamp in status (`last live …`).  
3. **Live frame B** — ≥ few seconds later; candle/last-live time changed.  
4. **EURUSD** — switch symbol dropdown to EURUSD; chart reloads that symbol.  
5. **Logged-out `/charts`** — Sign out, open `http://localhost:8000/charts` → login redirect.  
6. **Logged-out `/live`** (OBS-1/R-3) — open `http://localhost:8000/live` → login redirect.  
7. **Optional R-1** — zoomed-in candles legible after scroll wheel.

Submit these with the U07 package for ITRGA to convert CONDITIONAL → APPROVED.

---

## 4. Source excerpts (R-2 / §30)

**Chart State is presentation-only** (`frontend/src/chart/useChartState.ts`): holds symbol/timeframe/chartType/viewport; no fetch/analytics.

**Live merge** (`frontend/src/chart/types.ts` `mergeLiveBar`): same `time` → update forming bar; newer `time` → append; older → ignore.

**Route guard** (`frontend/src/auth/ProtectedRoute.tsx` + `App.tsx`): `/charts` and `/chart` and `/live` under `ProtectedRoute`.

**Seed marker** (`backend/app/services/chart_seed_service.py`): `source="seed:synthetic"` on all seeded rows.

**UI provenance banner** (`ChartWorkspacePage.tsx`): explicit non-authoritative notice + source counts.

---

## 5. Disposition

| Item | Status |
|------|--------|
| Engineering corrections C-2, C-3, R-1 | **Done in codebase** |
| C-1 Level-I evidence | **Awaiting Operator** |
| DA starts W0-U08 | **No** — blocked until ITRGA APPROVED + new BO |

---

**End of DA Response**
