# DELIVERY REPORT — BO-F-04
## Alerts Center Completion (domain filtering + lineage/timestamp surfacing)

| Item | Value |
|------|-------|
| Build Order | `BO-F-04` (Operator directive 2026-08-21: "authorized") |
| Predecessors | F-03 CLOSED (ITRGA 2026-08-21) · B-05 (emission) · SURF-P02 (existing alerts surface) |
| Implementer | Development Authority (DA) |
| Deliverable class | Frontend implementation unit (chain position 35) |
| Governance Gate | CLOSED · Production NOT CERTIFIED (unchanged) |
| Determination | Awaiting ITRGA independent determination (BO §12) |

---

## 1. Claimed scope vs. this Build Order

Executed exactly BO-F-04 §2: F-04.1 domain filtering, F-04.2 timestamp +
lineage surfacing, F-04.3 ack discipline preserved, F-04.4 honesty. §3
exclusions honored: no backend change (pure consumer of `GET /alerts` +
`POST /alerts/{id}/ack`), no frontend emission, no auto-action on ack, no
actuation controls, no design-language weakening, no repo publication. §6
allowed files plus one disclosed addition (D1) and one strengthening test
churn outside the list (D3 — see §8). Register rows ship in the patch per the
standing append-only convention (BO §9 binding).

## 2. What changed (files + SHAs + chain position)

Patch `f04.patch` — **chain position 35**, 5 files (3 modified + 2 new), zero
backend files. Applies clean onto `34f4c62` + elements 1–34; post-apply cmp
5/5; register hunk proven to apply onto a drifted (baseline-era) register with
the code at chain-34. Patch sha256:
`920f8acf36682398958ab86e6ebca47a856e6cdabdc230d90aca78e33462d895`.

| File | Change |
|---|---|
| `frontend/src/components/alerts/MonitoringAlertsPanel.tsx` | `alertDomain(alert)` mapping + `formatAlertTimestamp` + five-domain filter bar + per-card domain chip/timestamp/lineage lines + detail-record Domain row |
| `frontend/src/components/alerts/MonitoringAlertsPanel.css` | **New** — filter bar, domain chips, meta lines (pure token consumption; D1) |
| `frontend/src/terminal/terminalDeepLinks.test.tsx` | Churn (D3): the alerts deep-link test's fixture assertions moved inside its `waitFor` — the pre-existing provider-population race that was ITRGA's OBS-F03-1 custody failure |
| `frontend/src/test/f04_alerts_domains.test.tsx` | **New** — 13 tests (§6) |
| `docs/governance/TECHNICAL_DEBT_REGISTER.md` | This unit's rows + F-03 CLOSED status row + OBS-B-AUDIT-1-STATUS — pure-addition hunk in the patch (§9) |

## 3. Domain-filter mapping (data-origin derivation)

`alertDomain(alert)` derives the domain from the alert's **persisted fields**
in documented priority order — never a client-invented category:

| Priority | Condition | Domain |
|---|---|---|
| 1 | `signal_id` set, or subject `advisory_signal` | **signal** |
| 2 | `model_artifact_id` set, or subject `model_artifact` | **risk** |
| 3 | subject `market_series`, or any `market_class` | **market** |
| 4 | subject `system_component` | **system** |
| 5 | anything else (unknown / null-fielded subjects) | **research** — the documented neutral bucket |

The filter bar (`role=tablist`: ALL + five domains) filters the fetched list
client-side with an accurate `filtered/total` count; each card carries its
derived domain chip (`data-domain` pinned); a domain with no alerts renders
the honest *"No alerts in the X domain."* notice — distinct from the global
empty state.

## 4. Timestamp + lineage surfacing description

Every alert card now visibly renders:
- **`Created: {absolute UTC}`** — via `formatAlertTimestamp` (never a relative
  age; invalid input falls back to the raw string, honest);
- **`Lineage: {source}`** — the `lineage.source` where present, an honest
  `Lineage: none` otherwise;
- the existing `Subject: {subject_type}/{subject_id} · Ack:` line (preserved
  verbatim).

The detail record keeps its full field set and gains a **Domain** row.

## 5. Ack read-state-only preservation evidence

The acknowledge path is untouched: provider-owned M2 (state renders only after
the API confirms — no optimistic update), the exact "Acknowledge" label, the
disabled-while-acknowledging state, acknowledged-alerts-stay-visible. All
existing pins green (Panel + Surfacing + DeepLinks suites, 36/36 pre-F-04;
49/49 with the new suite); new pins cover unacked-only rendering and the
disabled-while-acknowledging state. Capture: acking one alert moved the
surface from 4 unacked to 3 + one "Ack: yes" with the backend POST 200 in the
log — confirmed after the API, not before.

## 6. Screenshot evidence (Level-I, `docs/evidence/f04/`)

| Capture | File | Result |
|---|---|---|
| All domains | `f04_all_domains.png` | 4/4 alerts with derived chips: market (LIVE_DATA_STALE), risk (DRIFT_DETECTED), system (INFERENCE_HEALTH_DEGRADED), signal (SIGNAL_WITHHELD) — all with absolute-UTC Created lines + lineage sources |
| Market filter | `f04_market_filter.png` | 1/4 — LIVE_DATA_STALE only, domain chip `market` |
| Risk filter | `f04_risk_filter.png` | 1/4 — DRIFT_DETECTED only, domain chip `risk` |
| Research empty | `f04_research_empty.png` | Honest "No alerts in the research domain." |
| Ack state | `f04_ack_state.png` | 4 ack buttons → 3 + one "Ack: yes" (read-state-only) |
| Probe log | `f04_capture_log.txt` | All states + counts + no-actuation scan (violations: none) |

The four concrete-domain alerts were emitted through the **real B-05 paths**
(stale `live:simulated` candle, drift record, withheld advisory signal,
inference-health input) — disclosed capture fixture, local dev DB only.

**Disclosed observation (non-blocking, backend-unrelated):** under the
capture's concurrent load, the B-AUDIT defensive path fired once — a
ws-ticket audit row could not be verified in 2 attempts and the durable marker
could not persist, so the structured-log final record fired; the endpoint
still returned 200 and the loss was NON-SILENT. This is the materialization of
the recorded residual (OBS-B-AUDIT-1: file-sqlite business-write transaction
merging) — the mechanism held exactly as designed; the future serialization
unit remains recommended. Registered as OBS-B-AUDIT-1-STATUS.

## 7. Test evidence (executed)

- Workspace full frontend suite: **946 passed / 176 files** (933 floor + 13
  new), 171.48s, exit 0 — `f04_vitest_fullsuite.log`.
- Typecheck: `tsc -b` exit 0 — `f04_tsc.log`.
- Production build: green (chunk-size warning pre-existing).
- Clone-side (gold standard): pristine `34f4c62` → 35 elements → `npm ci` →
  tsc clean → **946 passed** — `f04_cloneside_vitest.log` — **including the
  alerts deep-link test that was ITRGA's OBS-F03-1 custody failure and
  reproduced as a full-suite timing flake on this chain pre-churn.**

## 8. Deviations register

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | `MonitoringAlertsPanel.css` — a new stylesheet for the named component | The §6 "+ its stylesheet if needed" umbrella; pure token consumption; governance scans pass. |
| D2 | Filter state lives inside the panel (not `AlertsProvider.tsx`) | The BO permits the provider "only if the filter state lives there" — it doesn't need to; the panel-owned `useState` is self-contained and keeps the provider untouched (its M2 ack discipline stays exactly as pinned). |
| D3 | Churn to `frontend/src/terminal/terminalDeepLinks.test.tsx` — outside the §6 allowed list | **Strengthening churn, justified:** the test asserted the provider fixture with an immediate `getByText` after waiting only for the panel mount — a race that ITRGA flagged as OBS-F03-1 (its custody failure) and that reproduced as a full-suite flake on the DA chain during this unit's clone verification. The two fixture assertions moved inside the existing `waitFor` (the test's stated intent: "the surfaced panel renders the genuine fixture from the provider"). No assertion removed, none weakened. |
| D4 | Capture fixture seeding via the real B-05 emission paths | Same disclosed class as prior units; local dev DB only; honest labels. |

## 9. Register rows in patch (confirmed) + transmission manifest (relay-accurate)

The patch's register hunk is a zero-context pure-addition (12 appended lines):
TD-F03-UNIT-STATUS (CLOSED — APPROVED WITH OBSERVATIONS, incl. the OBS-F03-1/2
records), OBS-B-AUDIT-1-STATUS (the observed defensive-path firing), TD-F04-UNIT
(this unit). Verified to apply onto the chain-34 register (cmp byte-identical)
AND onto a baseline-era drifted register (DRIFT-PROOF OK).

All files newly transmitted with this delivery; byte-identical copies in
`/home/user/f04_transmission/`, cmp-verified; hashes mechanically verified
against the folder before this message (sha256sum -c MANIFEST.txt exit 0). This
report's own sha256 is declared in the DA's closing message; `MANIFEST.txt`
carries it.

| # | File | sha256 |
|---|---|---|
| 1 | `f04_transmission/f04.patch.txt` | `920f8acf36682398958ab86e6ebca47a856e6cdabdc230d90aca78e33462d895` |
| 2 | `f04_transmission/f04_ack_state.png` | `5273bea1e490878ebe7b5a385bb6503d27dd6abdf0b46855b223608aac26c46a` |
| 3 | `f04_transmission/f04_all_domains.png` | `aaa3c46c3205b5ca0efbf37997cf6d544cd79639bdd2912dea2da569bbbb8fdf` |
| 4 | `f04_transmission/f04_applycheck_transcript.txt` | `96c4f49a6ebf211606447f5f32e4e2e4a91dab170a9747056a56c00cdeae87ec` |
| 5 | `f04_transmission/f04_capture_log.txt` | `89f5bab1856b22119417c956f687ee1e3aedabca597ee7892a638b2696253d70` |
| 6 | `f04_transmission/f04_cloneside_vitest.log.txt` | `23d72126096cc83b6f374b9886db8832bc30f53a7249f1a6c69137a3a1af3a92` |
| 7 | `f04_transmission/f04_market_filter.png` | `44b31bd791382989d9fb582e85de02588e04f65924f1e7cb2c40bd6a122cf9bf` |
| 8 | `f04_transmission/f04_research_empty.png` | `5a9c61530b355b81215b40cd119ef45db88168150502ea1802d74a31554f4004` |
| 9 | `f04_transmission/f04_risk_filter.png` | `34bd8c7b6ccd48e5e1edae675cdb7224501f7080fe26e2fb6eebd3c847320c74` |
| 10 | `f04_transmission/f04_tsc.log.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 11 | `f04_transmission/f04_vitest_fullsuite.log.txt` | `49e4a77ab724640a12df6e59746c0cc5e7974b5fa843d54618d0e8dd8d56fded` |

---

**Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.**
