# SURF-P02 DELIVERY REPORT
## Alerts surfaced — rail badge, ALERTS right-dock tab, acknowledge, severity, detail (closes TD-061)

| Field | Value |
|---|---|
| Delivery | SURF-P02 — second item of the SURF programme (Build Order `BUILD_ORDER_SURF-P02.md`, Operator-authorized 2026-08-17) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | AXIOM ITRGA |
| Date | 2026-08-17 |
| Base chain | `34f4c62` + item3 `b7b4c4f7…` + item5 `4c03910c…` + item6 `f65da5c3…` + item4 Rev B `a516c2c1…` + SURF-P01 `62c4d021…` + OBS-SURF1-2 `69964afe…` |
| Patch | `/home/user/surf_p02.patch` — sha256 `e039c74bc99936406b51c034134f7d707c9759d2c4c0581dd34f3454a4054a40` (1,600 lines / 66,641 B / 15 files, LF, terminating newline) |
| Governance posture | Gate CLOSED · Production NOT CERTIFIED · advisory-only |

---

## 1. Chosen home + reasoning (S1)

**The terminal right dock gains a fourth tab — ALERTS** (`/?dock=alerts`), reached from the
left-rail alerts launcher (which now carries the genuine unread badge and deep-links
here), the dock tab itself, and the deep-link parser. Reasoning:

1. **Alerts are short list items** — type, summary, severity badge, ack state — the
   Build Order's own §3 flags the right dock as plausible for exactly this shape.
2. **The bottom dock is a 180 px drawer of dense cards** and the stage views are
   full-height document surfaces; neither fits a live notice feed. The right dock's
   320 px column presents the list legibly (capture 02: three full-height cards,
   containment verified).
3. **The rail badge requires a shell-level shared state** regardless of home; the
   `AlertsProvider` mounts once in `InstitutionalWorkspaceShell`, the rail renders the
   genuine count, and the dock panel consumes the same list/ack state — one fetch, one
   source of truth, no badge/dock divergence after an acknowledge.

## 2. Capability disposition — every §2.3 element mapped

| §2.3 element | Where it lives now | State |
|---|---|---|
| `MonitoringAlertsPanel` (title, disclaimer, list, error/loading/empty, per-alert type/summary/subject/Ack, severity badge) | `components/alerts/MonitoringAlertsPanel.tsx` — **extended in place** | Preserved + extended |
| `severityClass()` mapping (critical→danger, warning→degraded, else→stub) | same module, exported | Preserved verbatim; all three Literals named-tested |
| `fetchMonitoringAlerts` | `api/client.ts` — default raised 5 → 200 (S6) | Truncation removed |
| Left-rail alerts launcher | `UnifiedModuleRail` — genuine badge + `/?dock=alerts` navigation | Placeholder replaced |
| NEW: unread badge count | `AlertsProvider` (derived: `acknowledged === false`) | Genuine; absence when unknown |
| NEW: acknowledge control | panel `Acknowledge` button → `acknowledgeMonitoringAlert` → provider state | M1/M2/M3 |
| NEW: alert detail record | `TerminalAlertsDock` → `fetchMonitoringAlertDetail` → panel detail section | S5 |

## 3. Endpoint coverage — all three

| Endpoint | State |
|---|---|
| `GET /alerts` | already surfaced (`fetchMonitoringAlerts`) — default limit raised 5 → 200 (S6) |
| `GET /alerts/{alert_id}` | **surfaced** — `fetchMonitoringAlertDetail` |
| `POST /alerts/{alert_id}/ack` | **surfaced** — `acknowledgeMonitoringAlert` (the only write; read-state + audit, verified in-scope by ITRGA §2.2) |

## 4. M1–M4 confirmations

- **M1 — label:** the control's exact label is **`Acknowledge`** (pending state
  `Acknowledging…`). No `Resolve`, `Dismiss`, `Clear`, `Fix`, `Action` or `Handle`
  string exists anywhere in the surface — asserted by a named test.
- **M2 — no optimistic update:** the provider awaits `POST /alerts/{id}/ack`; only the
  API-confirmed record replaces the list entry. Named test holds the promise open and
  proves the item still reads `Ack: no` while pending; failure sets `alerts-ack-error`
  and leaves the alert unacknowledged with its control intact (named test).
- **M3 — acknowledged stay visible:** the acknowledged alert remains in the list
  rendering `Ack: yes`; its control disappears (read-state consumed). No filter was
  added at all — the default view is the full list.
- **M4 — frontend T-1 guard:** `test_alerts_ui_module_has_no_forbidden_controls`
  appended to `backend/tests/test_monitoring_alerts.py` (suite now 6/6), pinning
  `MonitoringAlertsPanel.tsx` with three non-vacuity anchors (`Monitoring Alerts`, the
  R1 disclaimer sentence verbatim, `Acknowledge`) and the forbidden vocabulary
  (`place_order`, `submit order`, `go live`, `connect broker`, `broker_account`,
  `resolve_alert`, `auto_action`, `execute`, `retrain`, `remediate`). **Disclosed
  carve-out (Deviation 1):** R1 requires the disclaimer sentence verbatim in the
  module, and that sentence legitimately contains `retrain` and `remediate`; the guard
  removes exactly that sentence before asserting absence and asserts the sentence
  itself as an anchor. The guard code comment documents this.

## 5. S6 disposition — limit raised

`fetchMonitoringAlerts` default raised **5 → 200** (the API maximum), with a comment
naming the OBS-CONV2-1 class. The panel additionally discloses the boundary whenever
the response reaches the cap: *"Showing the most recent 200 alerts (list cap)."* A
named test pins both the client default and the cap note.

## 6. R8 disposition — the orphan panel is EXTENDED in place

`MonitoringAlertsPanel.tsx` was **extended** (not relocated, not superseded): its
title, disclaimer, list rendering, severity mapping and states are preserved, and the
ack/detail/testid extensions were added in the same module. Its test file was extended
alongside it. `TerminalAlertsDock` is a thin integration mount (provider wiring +
detail fetch), not a second alerts surface — it renders the panel.

## 7. R9 — TD-061 register line, before and after

```
BEFORE: | TD-061 | Alert UI indicator absent | Low-Med | **Reduced** W3-U08 adds read-only alert panel to Operations dashboard for closeout visibility; richer alert UI still deferred | Future UI unit |
AFTER:  | TD-061 | Alert UI indicator absent | Low-Med | **Closed** SURF-P02: left-rail unread badge, terminal ALERTS right-dock tab, read-state-only acknowledge, severity styling, alert detail record | — |
```

## 8. Raw console transcripts (excerpts; full logs in `docs/evidence/uiconv/`)

```
$ git clone /home/user/axiom /tmp/p02verify && cd /tmp/p02verify
$ git apply item3.patch && git apply item5.patch && git apply item6.patch && git apply item4.patch && git apply surf_p01.patch && git apply surf_p01_obs1-2.patch
$ git apply --check surf_p02.patch
GIT_APPLY_CHECK_EXIT=0
$ git apply surf_p02.patch
$ <15-path tree audit vs DA tree>
all paths identical
$ npm ci --no-audit --no-fund
added 148 packages in 2s
$ npx tsc -b --force --pretty false
verify tsc exit: 0
$ npx vitest run
Test Files  168 passed (168)
     Tests  803 passed (803)
$ .venv/bin/python -m pytest -q
417 passed, 1 warning in 113.45s (0:01:53)
$ npm run build
dist/assets/index-B1ixir5U.js   704.00 kB │ gzip: 189.41 kB
$ sha256sum dist/assets/index-*.js
788a3a753d293c9d61541d50da1b8b1f0c4186d17e9372045948efc0b01868fc  (verify tree)
788a3a753d293c9d61541d50da1b8b1f0c4186d17e9372045948efc0b01868fc  (DA tree)  ← identical
```

**Platform: 168 suites / 803 frontend + 417 backend = 1,220 tests green** (floor 1,201
exceeded). Bundle 697.62 → **704.00 kB (+6.38 kB)** — disclosed per OBS-5.

## 9. Level-I captures (raw PNGs preferred per BO §6.9)

Gallery `SURF-P02_CAPTURES.html` sha256 `c41b277d4f08b01780d8b59747480f53386b94469e019d37f6ef73f8b350b6c5`;
raw PNGs in `/home/user/surf_p02_upload/`; machine-recorded DOM state
`SURF-P02_CAPTURE_VERIFICATION.json` sha256 `bce446a77e488080ed4c110e229e640d3f077e1351fc2857a1b75e0730590b78`.

| Capture | Proof | SHA-256 |
|---|---|---|
| 01 Rail badge | genuine unread **2**; aria `System Alerts (2 Unread)` | `bd8c0b5b…459ad` |
| 02 Dock populated | 3 real records, severities info/warning/critical, 2 ack controls, 1 acknowledged; containment `cardsFullyInsidePanel: true` | `ebf0d8b9…e170d` |
| 03a Ack before | hit-test **TRUE**; badge 2; alert unacknowledged (pixel-identical to 02 — same untouched state, disclosed) | `ebf0d8b9…e170d` |
| 03b Ack after | real API write: badge **2 → 1**, `Ack: yes`, 1 control left; audit row written | `343eaaed…a3c7bd` |
| 04 Empty, scrolled | "No monitoring alerts returned." in viewport; badge ABSENT (never 0) | `3262624e…8594` |
| 05 Load failure | panel error surfaced; badge absent; shell intact | `b5b3650e…36d2` |

## 10. Deviations and disclosures (unprompted)

1. **M4 guard carve-out (design-level, disclosed in-code and here):** the Build Order's
   forbidden list includes `retrain` and `remediate`, while its own R1 mandates the
   disclaimer sentence containing those exact words verbatim in the module. The guard
   excludes precisely that sentence and asserts it as an anchor; everything outside
   it is clean. No forbidden vocabulary was weakened.
2. **Evidence fixture (OBS-CONV2-5 class):** three alerts were inserted into the LOCAL
   dev database via the existing `MonitoringAlertService.create_alert` seam
   (`scripts/seed_surf_p02_alerts.py`) to power captures 01–03 — a genuine unread
   count and a real acknowledge write with audit row. Deviation register row
   `TD-UI-SURF-P02-ALERTS-EVIDENCE-FIXTURE` added to the debt register. No schema,
   endpoint or service change.
3. **Placeholder removal re-targeted one pinned test:** `uiconv_p01_shell` previously
   asserted a fabricated badge `"3"`; the assertion now pins the genuine mocked count
   `"1"` with a documented re-target comment. This is the exact fabrication class the
   Build Order exists to close.
4. **Capture 03a pixel-identical to 02** (the before-frame shows the same untouched
   state as the populated capture) — disclosed rather than re-shot with artificial
   difference.
5. **Bundle +6.38 kB** — OBS-5.

**No backend endpoint, schema, model or service change.** Only the `ack` write is
surfaced; no creation, dismissal, deletion or bulk mutation exists anywhere.

## 11. Standing

SURF-P01 closed clean (OBS-SURF1-1 / OBS-SURF1-2 closed by ITRGA). SURF-P02 delivered
per this report and awaiting determination. SURF-P03, DATA, CHART, POLISH remain
unauthorized. `TD-062` (external providers) untouched — out of scope per the Build
Order. Repository untouched — Operator-only.

---

**Gate CLOSED · Production NOT CERTIFIED**

*— AXIOM Development Authority (DA)*
*2026-08-17*

---

## 12. POST-DETERMINATION ADDENDUM (2026-08-17)

ITRGA issued `ITRGA_DETERMINATION_SURF-P02`: **APPROVED — no observations. `TD-061`
CLOSED.** This is the first unqualified approval of the programme. ITRGA credited, in
its own words: (1) the acknowledge write correctly constrained and evidenced
end-to-end; (2) the M4 guard "solved a problem I had not anticipated" — the forbidden
terms `retrain`/`remediate` legitimately appear in the mandatory disclaimer, and the
guard's excise-then-assert handling is recorded as "strictly stronger than what I
specified" (a naive implementation would have failed against correct code, with the
likely fix being to weaken a constitutional honesty surface); (3) the orphan panel
extended rather than duplicated; (4) every capture hash reconciling with a machine
record measuring the right property. S2's `null`-not-`0` unknown-count discipline was
singled out as the OBS-CONV2-1 class applied to a trivial-looking number, and the
03a/02 hash identity was accepted as expected, not flagged.

**Programme position:** CONV COMPLETE · SURF-P01 APPROVED WITH OBSERVATIONS (no open
findings) · SURF-P02 **APPROVED** · SURF-P03 **not authorized** (ITRGA will inventory —
noting CONV item 5 already surfaced the governance overlay — before issuing any Build
Order). Open findings programme-wide: `OBS-5` (bundle, POLISH-P01) · `OBS-CONV2-5`
(seeded fixtures) · `F-BRAND-1` (GA-173, Operator).

**No DA action outstanding on SURF-P02.** The DA stands by for the SURF-P03 Build
Order, and implements nothing until it arrives.
