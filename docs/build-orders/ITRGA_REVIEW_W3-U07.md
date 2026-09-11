# ITRGA INDEPENDENT REVIEW — W3-U07 (Performance Analytics + Confidence Visualization)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit under review | **W3-U07** — Performance Analytics + Confidence Visualization |
| Wave | 3 — Live Research Advisor |
| Build Order | `docs/BUILD_ORDER_W3-U07.md` |
| Delivery under review | `uploads/DELIVERY_REPORT_W3-U07.md`, `uploads/operator results.md`, 3 screenshots |
| DA-claimed platform version | 0.29.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **🔴 APPROVAL WITHHELD — MANDATORY OPERATOR EVIDENCE ABSENT (WRONG UNIT SUBMITTED)** |
| Confidence | **HIGH** — the finding rests on the literal content of the submitted evidence file, not on interpretation |

> **We don't guess. We prove.** The evidence supplied does not test the unit under review. It cannot be approved.

---

## 1. Bottom line

**W3-U07 is WITHHELD.** This is **not** a finding about the quality of the implementation — it is that **the operator evidence submitted for W3-U07 does not exercise W3-U07 at all.** The attached `operator results.md` is, line for line, the **W3-U06 monitoring-alerts evidence pack** re-submitted unchanged. It contains **zero** commands, tests, API calls, or database reads that touch the Performance Analytics feature. One of the three screenshots additionally shows the analytics route **failing to load** (`ERR_CONNECTION_REFUSED`), directly contradicting the two screenshots that show it rendered.

Per the standing rule — **runtime approval requires operator-run evidence on the target, and a single unmet mandatory-evidence requirement ⇒ APPROVAL WITHHELD** — there is no lawful path to approval on this submission. The unit is not rejected on merit; it is **un-reviewable as submitted.**

---

## 2. The disqualifying finding

### C-1 (CRITICAL) — The operator evidence is for the wrong unit (stale W3-U06 pack)

Every executed command in `operator results.md` belongs to W3-U06 (monitoring alerts), not W3-U07 (analytics). Proof from the file itself:

| Expected for W3-U07 | Present in `operator results.md`? | Evidence |
|---|---|---|
| `pytest tests/test_advisory_analytics.py` (DA claims "4 passed") | **NO** | `grep -niE "analytics"` over the whole file → **NONE FOUND** |
| API read-back of `GET /api/v1/analytics/advisory-performance` | **NO** | No `analytics` endpoint is ever called; only `/api/v1/alerts`, `/api/v1/market/live/*` appear |
| Seeding of source `advisory_signals` for analytics + `psql SELECT` of computed metrics | **NO** | No analytics seed/select; the only `advisory_signals` mentions are the W3-U02 test names and the DROP-CASCADE list |
| No-execution / presentation-only grep over `PerformanceAnalyticsPage.tsx` | **NO** | The only greps present target `live_signal\|emit_signal\|place_order\|cancel_order` over the **monitoring** module (W3-U06) |
| `LOCAL_CI_EXIT_CODE: 0` echo | **NO** | Marker `==> Local CI equivalent complete` present; the exit-code echo is again absent (long-standing LOW — but here it is the least of the problems) |

**What the pack actually is:** it opens by dropping/recreating the schema, upgrading Alembic to head `20260715_0018` (the **W3-U06** head — consistent with "W3-U07 adds no migration"), then `\d monitoring_alerts`, then the W3-U06 alert-proof flow: `$AlertId = "operator-alert-proof-…"`, `psql SELECT … FROM monitoring_alerts`, `audit_events WHERE resource_type='monitoring_alert'`, `drift_monitoring_records`, `Get-Content ..\docs\evidence\W3-U06_ALERT_PROOF_IDS.json`, `Invoke-RestMethod … /api/v1/alerts`, and `Tee-Object ..\docs\evidence\W3-U06_PRIOR_GATE_REGRESSION_VERBOSE.txt`. This is verbatim the evidence that supported the **W3-U06** verdict.

**Classification: CRITICAL.** Mandatory operator-run evidence for the unit under review is entirely absent. This alone withholds approval.

---

## 3. Internal-consistency failures (independent of C-1)

Even setting aside that the wrong pack was sent, the numbers in the **DELIVERY_REPORT** do not reconcile with the **operator run**, and the run does not reconcile with itself against the DA's own baseline.

| Metric | DA Delivery Report §7 | Operator run (`operator results.md`) | Build Order baseline | Reconciles? |
|---|---|---|---|---|
| Backend tests | **192 passed** | **188 passed** (lines 340 & 1394) | 188 | **NO** — operator ran the baseline suite; the 4 claimed new analytics tests never executed |
| Frontend test files | **10 passed** | **9 passed** (lines 372 & 1426) | 9 | **NO** |
| Frontend tests | **24 passed** | **20 passed** | 20 | **NO** — the claimed +4 UI tests never executed |
| Named `test_advisory_analytics.py` | "4 passed" | **not run anywhere** | — | **NO** |

The operator's suite is **exactly the W3-U06 baseline (188 / 9 / 20)**. This is the signature of the **pre-W3-U07 codebase** being tested. The DA's self-reported 192 / 10 / 24 (its own sandbox run) is plausible but is **Level-IV report-claim only** and, per standing rule, **cannot substitute** for target evidence. **A count mismatch is a finding, not a rounding note.**

---

## 4. Screenshot analysis — contradictory, cannot corroborate

Three screenshots were supplied. They do not agree with each other, so they cannot be used to rescue the missing text evidence.

| Screenshot | What it shows | Assessment |
|---|---|---|
| `Screenshot 2026-07-16 003557.png` | Browser at `127.0.0.1:5173/analytics` → **"This site can't be reached — 127.0.0.1 refused to connect. ERR_CONNECTION_REFUSED"** | The analytics route was **unreachable** — dev server not running / not serving that route at capture time. This is a **negative** result for the unit. |
| `Screenshot 2026-07-16 003630.png` | Rendered "Performance Analytics" page: disclaimer banner ("Research analytics only… not a guarantee… read with its uncertainty"), 4 metric cards with 95% Wilson intervals + sample count + method, "Refresh Analytics" | Content is on-spec **if genuine**, but capture context is unverifiable and it conflicts with 003557. |
| `Screenshot 2026-07-16 003643.png` | Calibrated confidence bands (Low/Neutral/High), **"Confidence unreliable — calibration warning present."**, "Raw model score is intentionally excluded", RESEARCH source-note badges | On-spec content **if genuine**, same caveats. |

**Why this is not "proven-unrelated flake" territory (R13):** the two rendered screenshots and the "connection refused" screenshot cannot both be true of the same running system at the same time, and **none of them is backed by the corresponding text evidence** (no server-start log, no analytics API read-back, no browser DevTools/network showing a `200` from `/api/v1/analytics/advisory-performance`). Unverifiable + self-contradictory screenshots are a **non-result**, exactly as a blank grep is a non-result (R7). The UI-screenshot mandate (W0-U06 precedent) requires screenshots that corroborate a proven-running build — these do the opposite.

---

## 5. What is *not* being held against the unit

To be fair and precise (R13 proportionality):

- The **absence of a new migration** is legitimate — analytics reads existing `advisory_signals`; "no new persisted artifact" is a valid design and does not trigger the persistence-capture control (which fires only when a **new** report/artifact type is persisted).
- The **Delivery Report's structure, scope discipline, and non-self-approval** are correct and commendable (§15 DA Non-Approval Statement is exactly right).
- The **design intent** shown in the report and the rendered screenshots (uncertainty-mandatory, calibrated-not-raw, unreliability warning, advisory-not-guaranteed framing, presentation-only, no execution controls) **matches the Build Order** — *on paper.* None of it is **proven on target**, so none of it can be credited toward approval.

This is why the verdict is **WITHHELD (un-reviewable)** rather than **REJECTED (defective)**.

---

## 6. Required to clear this verdict — re-submit a correct W3-U07 evidence pack

The operator must re-run the **W3-U07** evidence commands (`docs/evidence/W3-U07_OPERATOR_EVIDENCE_COMMANDS.md`) on the target **against the W3-U07 codebase** and submit the raw console. Mandatory, non-waivable:

1. **Confirm the build under test is W3-U07** — e.g. `git log -1 --oneline` / show the new files exist on the target (`PerformanceAnalyticsPage.tsx`, `analytics/service.py`, `test_advisory_analytics.py`).
2. **Full backend `pytest`** showing the **new higher total (expected ≥ 192), 0 failed**, and the named run `pytest tests/test_advisory_analytics.py -vv` with each analytics test PASSED (named, not just a count).
3. **Full frontend `vitest`** showing the **new higher totals (expected 10 files / 24 tests), 0 failed**, including the point-estimate-rejection test by name and the `PerformanceAnalyticsPage.test.tsx` file present in the file list.
4. **Read-only API evidence**: unauthenticated `GET /api/v1/analytics/advisory-performance` → **401**; authenticated → **200** with a payload that shows, verbatim, (a) every metric carrying `sample_count` + interval + method, (b) at least one band with `calibration: warning` and the unreliability flag, (c) **no raw model score field**. A write attempt (`POST`) → **405/404**.
5. **Seed + source proof**: seed source `advisory_signals` (clean + guardrailed/withheld/expired mix) and show the API metrics are computed from those rows — so the on-screen numbers are demonstrably data-driven, not hard-coded.
6. **Browser screenshots that corroborate a running build**: the **same session** must show (a) the server serving `/analytics` (no `ERR_CONNECTION_REFUSED`), (b) the disclaimer, (c) uncertainty on every metric, (d) the calibration-warning card, (e) **no execution controls anywhere**, (f) logged-out `/analytics` blocked. Replace the contradictory 003557 shot.
7. **Grep evidence with command + output** (R7): no-execution grep over `frontend/src` and presentation-only grep over `PerformanceAnalyticsPage.tsx` — showing the command **and** its (empty) output.
8. **`LOCAL_CI_EXIT_CODE: 0`** echoed inline after `==> Local CI equivalent complete` (standing LOW request — please finally capture it this cycle).

On a clean, self-consistent W3-U07 pack meeting the above, I expect to move to **APPROVED** quickly — the design is sound; it simply has not been proven yet.

---

## 7. Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| **C-1** | **CRITICAL** | Operator evidence is the stale **W3-U06** pack; zero W3-U07 commands/tests/API/DB reads | **Blocks approval** — re-submit correct pack |
| F-2 | HIGH | Test-count mismatch: DA claims 192/10/24; operator ran 188/9/20 (= W3-U06 baseline); named analytics tests never executed on target | Resolved by §6.2–6.3 |
| F-3 | HIGH | Screenshots self-contradict: `/analytics` shows `ERR_CONNECTION_REFUSED` in one shot, rendered in two; none corroborated by text/network evidence | Resolved by §6.6 |
| F-4 | LOW | `LOCAL_CI_EXIT_CODE: 0` echo again not captured inline | Non-blocking; keep asking (§6.8) |

**Verdict: a single CRITICAL (C-1) plus unmet mandatory operator evidence ⇒ APPROVAL WITHHELD.** No approval on report-claims alone (Level-IV is the lowest tier).

---

## 8. Process note (no blame, just correctness)

The most likely cause is a **file mix-up during relay** — the previous turn's `operator results.md` (W3-U06) was attached again instead of the new W3-U07 run. That is an easy fix and does **not** impugn the DA's implementation. But the ITRGA cannot approve what it cannot see proven, and it will never label an un-run gate "green." Please re-collect and re-submit; the door opens as soon as the lock is proven on target.

> **We don't guess. We prove.** — ITRGA
