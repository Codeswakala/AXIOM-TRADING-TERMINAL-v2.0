# DELIVERY REPORT — BO-F-05
## Lineage & Evidence Visualization (traceability across the terminal)

| Item | Value |
|------|-------|
| Build Order | `BO-F-05` (Operator directive 2026-08-21: "authorized") |
| Predecessors | F-04 CLOSED (ITRGA 2026-08-21) · Reconciliation §17/§37 · B-00 provenance protocol |
| Implementer | Development Authority (DA) |
| Deliverable class | Frontend implementation unit (chain position 36) |
| Governance Gate | CLOSED · Production NOT CERTIFIED (unchanged) |
| Determination | Awaiting ITRGA independent determination (BO §12) |

---

## 1. Claimed scope vs. this Build Order

Executed exactly BO-F-05 §2: F-05.1 lineage surfacing on intelligence cards,
signals, and alerts; F-05.2 the read-only lineage/evidence view reusing
`ArtifactLineageTree`; F-05.3 scope discipline; F-05.4 honesty. §3 exclusions
honored: no backend change (pure consumer of already-persisted lineage
fields), no fabricated relationships, no mutation/actuation, no over-labeling
of presentation-only values, no design-language weakening, no repo
publication. §6 allowed files plus one disclosed addition (D1). Register rows
ship in the patch per the standing append-only convention (BO §9 binding).

## 2. What changed (files + SHAs + chain position)

Patch `f05.patch` — **chain position 36**, 9 files (7 modified + 2 new), zero
backend files. Applies clean onto `34f4c62` + elements 1–35; post-apply cmp
9/9; register hunk proven to apply onto a drifted (baseline-era) register with
the code at chain-35. Patch sha256:
`cae375af459c95002d84ef795c92f4e19f0709c94c8549c987db61121f69db35`.

| File | Change |
|---|---|
| `frontend/src/api/client.ts` | The correlation/regime read types gained the backend's persisted `source_artifact_ids`/`audit_correlation_id`/`created_by`; signal-validation gained `source_signal_ids`/`audit_correlation_id`/`created_by` (all optional — "where present"; no fixture churn) |
| `frontend/src/workstation/ai/ArtifactLineageTree.tsx` | Neutral `source_artifact` node type + icon (D2 — needed so lineage panels never fabricate a role) |
| `frontend/src/components/terminal/LineageEvidencePanel.tsx` | **New** — the read-only lineage/evidence view: persisted-only nodes + evidence block + honest absence + the 12-source render cap with disclosure |
| `frontend/src/components/terminal/TerminalIntelligenceCards.tsx` | Per-report Lineage toggle on all five families rendering the panel |
| `frontend/src/components/terminal/TerminalSignalStream.tsx` | The three missing report ids (statistical/economic/generalization); the fabricated `"exp-001"` fallback → honest `"not recorded"` (D3) |
| `frontend/src/components/alerts/MonitoringAlertsPanel.tsx` | Card `Audit:` line + detail-record audit-correlation row |
| `frontend/src/components/terminal/TerminalMultiPane.css` | F-05 styles (toggle, panel, evidence block) — pure token consumption (D1) |
| `frontend/src/test/f05_lineage_evidence.test.tsx` | **New** — 10 tests (§6) |
| `docs/governance/TECHNICAL_DEBT_REGISTER.md` | This unit's rows + F-04 CLOSED status row — pure-addition hunk in the patch (§9) |

## 3. Lineage-surfacing description (per surface, per field)

- **Intelligence cards (all five families):** a per-report **Lineage** toggle
  opens the evidence panel showing the real `report_hash`, `audit_correlation_id`,
  `created`/`created_by`, and the persisted `source_artifact_ids` (correlation/
  regime/scenario/portfolio-risk; signal-validation surfaces its
  `source_signal_ids` through the same panel — disclosed D4).
- **Advisory signals:** the expanded lineage section now carries all three
  previously-missing report ids (statistical / economic / generalization)
  alongside the existing model id, experiment id, feature set, input hash,
  calibration report, and audit correlation — and the pre-F-05 fabricated
  `"exp-001"` fallback is replaced by the honest `"not recorded"`.
- **Alerts:** every card renders `Audit: {audit_correlation_id}` (honest
  "provenance not recorded" when absent) next to the F-04 `Created`/`Lineage`
  lines; the detail record gains an audit-correlation row.
- **Chart/structural events:** the F-02 provenance line (symbol/timeframe/
  series kind) remains the chart-side lineage; the series-kind provenance is
  already visible where relevant (structural stream + chart stage).

## 4. Lineage/evidence view description

`LineageEvidencePanel` reuses `ArtifactLineageTree` with **persisted-only
nodes** (`buildPersistedLineageNodes`): the artifact node (id, real
`report_hash` when persisted, timestamp, research status) plus one neutral
`source_artifact` node per persisted source id. The tree's illustrative
default chain — market → features → model → report, with its placeholder
hash — is **never** rendered for real artifacts (it would fabricate
relationships the record does not assert; that path remains only for the
legacy assistant summarizer that was built on it). The evidence block lists
hash/audit-correlation/created/created-by with per-field honest absence, and
a banner appears only when nothing at all is recorded (a timestamp counts as
evidence). A 12-source render cap with an honest disclosure note handles real
reports whose persisted lineage ids run to hundreds (the capture caught a
real correlation report carrying per-bar source ids — the cap is the fix).

## 5. Scope-discipline + honesty evidence

- Scope: the intelligence tab bar and the counter badges (presentation-only
  values) carry **zero** lineage controls — test-pinned.
- Honesty: absent fields render "provenance not recorded" per field;
  `exp-001`-class fabrications are gone from the signal lineage; the tree
  renders no invented roles or hashes.

## 6. Screenshot evidence (Level-I, `docs/evidence/f05/`)

| Capture | File | Result |
|---|---|---|
| Report lineage panel | `f05_lineage_report.png` | Real correlation report (`d93d7302…`): hash `34070aaf…`, audit `b9e1d9ee…`, capped source list (12 + disclosure), fabricated chain absent, zero controls inside the panel |
| Signal lineage | `f05_signal_lineage.png` | Real experiment id + truncated audit correlation + honest "not recorded" rows; no `exp-001` |
| Alert detail audit row | `f05_alert_lineage.png` | Real alert `5b7233f2…` detail record with audit row `8404039e…` |
| Probe log | `f05_capture_log.txt` | All assertions above |

The report/signal/alert were persisted through the real backend paths
(real-corpus generation; service-seam signal seeding; B-05 inference-health
emission) — disclosed capture fixture, local dev DB only.

## 7. Non-actuation/read-only evidence

The only lineage control is the expand toggle; the panel itself contains
**zero** buttons/inputs/links (test-pinned + capture). No mutation, no
actuation anywhere in the lineage surfaces.

## 8. Test evidence (executed)

- Workspace full frontend suite: **956 passed / 176 files** (946 floor + 10
  new), 176.24s, exit 0 — `f05_vitest_fullsuite.log`.
- Typecheck: `tsc -b` exit 0 — `f05_tsc.log`.
- Production build: green (chunk-size warning pre-existing).
- Clone-side (gold standard): pristine `34f4c62` → 36 elements → `npm ci` →
  tsc clean → **956 passed** — `f05_cloneside_vitest.log`.

## 9. Deviations register

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | `TerminalMultiPane.css` edited (the dock stylesheet home) + `client.ts`/`ArtifactLineageTree.tsx` touched | The §6 surface list includes the four component files; the stylesheet follows the established umbrella; `client.ts` is the typed home of the persisted fields being surfaced; the tree file was explicitly allowed ("extend only if strictly needed"). |
| D2 | `source_artifact` node type added to the tree's union | Strictly needed: without a neutral role, rendering a persisted source id would require fabricating a role (model/signal/etc.). The legacy default chain is untouched. |
| D3 | Signal-stream honesty churn: `"exp-001"` fallback → `"not recorded"` | The pre-F-05 fallback fabricated an experiment id. Removing it is stricter, spec-superseded (F-05.4: absent lineage renders honestly), disclosed inline + here. |
| D4 | Signal-validation lineage via the panel's `source_artifact_ids` parameter (read model carries `source_signal_ids`) | The panel renders the ids the record carries; the signal-validation card passes its `source_signal_ids` list. One panel, persisted-only fields, no invented types. |
| D5 | 12-source render cap | Real reports carry per-bar lineage ids (hundreds — observed in capture); the cap keeps the tree legible and is disclosed on-screen + here. |

## 10. Register rows in patch (confirmed) + transmission manifest (relay-accurate)

The patch's register hunk is a zero-context pure-addition (11 appended lines):
TD-F04-UNIT-STATUS (CLOSED — APPROVED WITH OBSERVATIONS, OBS-F03-1 closed by
the D3 race fix, OBS-F03-2 now optional), TD-F05-UNIT (this unit). Verified to
apply onto the chain-35 register (cmp byte-identical) AND onto a baseline-era
drifted register (DRIFT-PROOF OK).

All files newly transmitted with this delivery; byte-identical copies in
`/home/user/f05_transmission/`, cmp-verified; hashes mechanically verified
against the folder before this message (sha256sum -c MANIFEST.txt exit 0). This
report's own sha256 is declared in the DA's closing message; `MANIFEST.txt`
carries it.

| # | File | sha256 |
|---|---|---|
| 1 | `f05_transmission/f05.patch.txt` | `cae375af459c95002d84ef795c92f4e19f0709c94c8549c987db61121f69db35` |
| 2 | `f05_transmission/f05_alert_lineage.png` | `21b1dcefb5ac42a6cc536bc5a0a4a3ad5a90c15387ed56643a21df1c3b82a97b` |
| 3 | `f05_transmission/f05_applycheck_transcript.txt` | `2a064965e8b9c0ea5690aa118f06540f4120caf72b2dfdc180e9d64274aff654` |
| 4 | `f05_transmission/f05_capture_log.txt` | `1aaad5eb92c1c92ffc5749d68e782c972d215b0e92071160739fbab4532969f8` |
| 5 | `f05_transmission/f05_cloneside_vitest.log.txt` | `dc6cc68583a915d7d9f5e9505f6512a34993cd1a45e243c67437242e185f4c45` |
| 6 | `f05_transmission/f05_lineage_report.png` | `3928be6f61f965fa947406500c8bccf9e91398c4fe0e231edd01d530a7dc773b` |
| 7 | `f05_transmission/f05_signal_lineage.png` | `70e4f8c47cfbef561bc8a13cbb0f6e375c3bd745208307509d06a67037386d2f` |
| 8 | `f05_transmission/f05_tsc.log.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 9 | `f05_transmission/f05_vitest_fullsuite.log.txt` | `6746d9c45eb2a1968b0fd9d1554bae093f01a3a3f8d39de746457925b89226eb` |

---

**Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.**
