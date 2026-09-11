# ITRGA OBS-1 CLOSURE NOTE — W4-U03 (Regime Detection Reports)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM ITRGA** |
| Unit | **W4-U03** — Regime Detection Reports |
| Relates to | `ITRGA_REVIEW_W4-U03.md` (APPROVED WITH OBSERVATIONS, 2026-07-16) — OBS-1 |
| Evidence | OBS-1 clean CI re-run `operator results.md` (422 lines) |
| Platform | 0.33.0 |
| Date | 2026-07-16 |
| **RESULT** | **✅ OBS-1 CLOSED. W4-U03 is now RESIDUAL-FREE.** |
| Confidence | HIGH |

> **We don't guess. We prove.** The CI gate is green via the documented invocation. The residual is closed.

---

## 1. Context

W4-U03 was APPROVED WITH OBSERVATIONS. The sole residual, **OBS-1**, was a red `LOCAL_CI_EXIT_CODE: 1` caused
by a **proven-unrelated WSL `/bin/bash` spawn error** — the CI had been invoked as bare `bash scripts/
local_ci.sh` (→ WSL relay, `/bin/bash` absent) rather than the documented Git-Bash path, *after* all gates ran
green. The fix was simply to re-run CI correctly; no product change was required.

## 2. OBS-1 — CLOSED ✅

The re-run uses the **documented invocation** and completes cleanly:

- Invocation: `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` ✅ (no bare `bash` → WSL)
- CI body green end-to-end: `==> Ruff → All checks passed!`; `==> Pytest → 211 passed`; `==> npm audit →
  found 0 vulnerabilities`; `==> Vitest → 11 files / 25 tests`; `==> Frontend build → ✓ built`.
- `==> Local CI equivalent complete` **and** **`LOCAL_CI_EXIT_CODE: 0`**.
- **No `execvpe(/bin/bash)` / WSL error; no test failures.**

The earlier exit-1 is confirmed to have been the environment/invocation artifact and nothing more.

*(Cosmetic OBS, non-blocking: the `Tee-Object`/`Select-String` still reference the
`W3-U08.1_LOCAL_CI_TRANSCRIPT.txt` filename — a leftover label — but the live run shows the marker + exit 0
inline. Point the transcript filename at W4-U03 next time; does not affect the result.)*

## 3. Disposition

- **OBS-1 CLOSED.** **W4-U03 is RESIDUAL-FREE.** Platform of record **v0.33.0** (unchanged).
- No re-review of W4-U03's functional/governance gates needed — those were approved on target
  (`ITRGA_REVIEW_W4-U03.md`); this note closes the single CI residual only.
- **Next:** on operator authorization, ITRGA issues **`BUILD_ORDER_W4-U04.md`** — Scenario Simulation Research
  Reports, carrying **R-2** (no-look-ahead), **R-4** (persistence-capture, inline raw SELECT + audit),
  **R-5** (economic-usefulness reported), and **R-6** (scenario is hypothetical — no order/sizing payload; the
  highest-risk framing in plan §8).
- DA does not self-authorize W4-U04, adopt an unspiked dep, add execution/broker, or open the Gate.

> **We don't guess. We prove.** — ITRGA
