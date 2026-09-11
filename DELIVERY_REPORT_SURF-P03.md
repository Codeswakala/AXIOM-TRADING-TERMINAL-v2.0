# SURF-P03 DELIVERY REPORT
## Governance & platform records surfaced — route inventory · RBAC · API catalogue · plugin contracts · operator scope records

| Field | Value |
|---|---|
| Delivery | SURF-P03 — final phase of the SURF programme (Build Order `BUILD_ORDER_SURF-P03.md`, Operator-authorized 2026-08-17) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | AXIOM ITRGA |
| Date | 2026-08-17 |
| Base chain | `34f4c62` + item3 `b7b4c4f7…` + item5 `4c03910c…` + item6 `f65da5c3…` + item4 Rev B `a516c2c1…` + SURF-P01 `62c4d021…` + OBS-SURF1-2 `69964afe…` + SURF-P02 `e039c74b…` |
| Patch | `/home/user/surf_p03.patch` — sha256 `c18d5d05816de0cbd3e453d9126197d90406c13d11b995fc379d45736494d605` (1,609 lines / 68,165 B / 9 files, LF, terminating newline) |
| Governance posture | Gate CLOSED · Production NOT CERTIFIED · advisory-only |

---

## 1. Chosen home + reasoning, addressing §2 explicitly

**Home: the existing governance overlay, extended with a new "Platform Records"
section** (`PlatformRecordsSection`, mounted inside `GovernanceEvidenceWorkspace`
immediately after the Platform Operations posture panel). Reasoning:

1. **§2 obeyed — the already-surfaced surfaces were untouched.** The audit trail
   (Audit Explorer) and workspace preferences (settings overlay) are single-
   implementation and correctly placed; **zero lines of either were modified** in
   this patch — the diff touches neither `TerminalSignalStream`-adjacent audit code
   nor the settings overlay.
2. The overlay already owns the governance domain and already renders the summary
   these records expand (M4's agreement anchor); a second governance surface would
   split the domain and risk the orphan pattern `OBS-CONV3-3` closed.
3. A bottom-dock tab is research output; these are governance-platform records — the
   Build Order itself rules that home out.

## 2. Coverage — the five target endpoints

| Endpoint | Prior state | Now |
|---|---|---|
| `GET /route-inventory` | summary scalars only (version/actuation/gate) | **routes array rendered** — 17 entries, per-route path/methods/permission/description |
| `GET /rbac/permissions` | summary scalars only | **roles rendered** — per-role permission lists + policy + `forbidden_capabilities_present` |
| `GET /api-catalogue` | summary scalars only | **routes array + abuse_guard + persistence rendered** — 70 routes, abuse-guard status/reason, catalogue-table/alembic-head posture |
| `GET /plugin-contracts` | summary scalars only | **contracts + capability_allowlist rendered** — 3 contracts with names/versions/capabilities, allowlist verbatim |
| `GET /operator-scope-records` + `/{operator_id}` | **no client function, no type, no UI** | **surfaced** — list + detail, with honest 403 handling (M3) |

## 3. M1 — frontend T-1 guard

`test_platform_records_ui_module_has_no_governance_mutation_controls` appended to
`backend/tests/test_institutional_platform_security.py` (suite now **10/10**),
pinning `PlatformRecordsSection.tsx` with four non-vacuity anchors (`platform
records`, `route inventory`, `inspection view`, `access restriction, not an empty
result`) and the forbidden list (`place_order`, `submit order`, `go live`, `connect
broker`, `broker_account`, `execute`, `enable_plugin`, `grant_permission`,
`elevate_role`). Both the new module and the overlay were swept — **zero hits**.

## 4. M3 disposition — the access-denied text

Exact notice (scope list and scope detail share it):

> **Access denied.** Access to institutional scope records is denied for your role.
> This is an access restriction, not an empty result. `{verbatim backend detail}`

Visual distinction is structural, not cosmetic: three separate renderings with
separate testids — `platform-scope-access-denied` (error styling + bold lead),
`platform-scope-empty` ("No scope records returned for this operator."), and
`platform-scope-error` (transport failures). The 403 path is identified by HTTP
status (the shared `request` helper now attaches `status` to its errors — message
unchanged, disclosed) and mapped to `denied`, never to empty. Named tests assert all
three states are mutually exclusive. Capture 04 proves it against the **real
backend**: an unprivileged session renders the notice with the verbatim backend
detail, the empty state is not rendered, and the four collection rows show their own
real 403s separately.

## 5. M4 disposition — summary agreement

The posture summary (bundle) and this section (five independent fetches) both read
the same immutable institutional endpoints. Disposition:
- The section renders **records** — content the summary never shows — and renders no
  scalar card that duplicates the summary's.
- The section header carries the agreement statement: *"Values that also appear in
  the posture summary above come from the same endpoints and must agree; nothing
  here is reconciled silently."*
- Where a value necessarily appears in both (e.g., catalogue abuse-guard status),
  it is rendered "as returned" by this fetch with the same endpoint provenance; the
  endpoints are static configuration with no write path, so divergence is not
  producible — and if it ever occurred, both renderings are visible rather than
  reconciled.

## 6. R1–R7

| Req | Result |
|---|---|
| R1 | All record values verbatim or explicit absence; five empty-state markers; counts are genuine array lengths |
| R2 | **Five independent fetches**, per-source status rows with genuine counts; capture 03 proves real-backend partial denial (2 error + 3 ready); capture 06 proves a single aborted seam leaves 4 sources rendering |
| R3 | RBAC unchanged — the UI calls the endpoints and renders what returns, including 403s; no pre-emption or bypass exists |
| R4 | Legibility instrument run on the new section: `cardsFullyInsidePanel: true` (capture 01); the overlay body already scrolls inside the OBS-SURF1-2-hardened layout |
| R5 | **169 suites / 813 frontend + 418 backend = 1,231 tests** (floor 1,220) |
| R6 | `npm ci` before `tsc -b` in both trees |
| R7 | Nothing superseded, nothing orphaned — the orphan pattern itself was the target, and the four previously-dead client functions are now rendered through the overlay (they were already internally wired by `fetchPlatformOperationsEvidence`; what was unsurfaced was their record payloads) |

## 7. Raw console transcripts (excerpts; full logs in `docs/evidence/uiconv/`)

```
$ git clone /home/user/axiom /tmp/p03verify && cd /tmp/p03verify
$ git apply item3.patch && git apply item5.patch && git apply item6.patch && git apply item4.patch && git apply surf_p01.patch && git apply surf_p01_obs1-2.patch && git apply surf_p02.patch
$ git apply --check surf_p03.patch
GIT_APPLY_CHECK_EXIT=0
$ git apply surf_p03.patch
$ <9-path tree audit vs DA tree>
all paths identical
$ npm ci --no-audit --no-fund
added 148 packages in 2s
$ npx tsc -b --force --pretty false
verify tsc exit: 0
$ npx vitest run
Test Files  169 passed (169)
     Tests  813 passed (813)
$ .venv/bin/python -m pytest -q
418 passed, 1 warning in 116.06s (0:01:56)
$ npm run build
dist/assets/index-ByTeB58D.js   718.83 kB │ gzip: 192.26 kB
$ sha256sum dist/assets/index-*.js
c112dfe535552ca5f25b9e4e0495fddddeddc2fdebb28478ff79cea6620791b8  (verify tree)
c112dfe535552ca5f25b9e4e0495fddddeddc2fdebb28478ff79cea6620791b8  (DA tree)  ← identical
```

Bundle 704.00 → **718.83 kB (+14.83 kB)** — the records section and scope client
layer; disclosed per OBS-5.

## 8. Level-I captures (raw PNGs, per BO §7)

Gallery `SURF-P03_CAPTURES.html` sha256 `30dad942ccc564c8f576400e9f1022808200eed0ae11c88e1293684497ad6c03`;
raw PNGs in `/home/user/surf_p03_upload/`; machine-recorded DOM state
`SURF-P03_CAPTURE_VERIFICATION.json` sha256 `0908df2a26c79beaa871ab1950fc3e468e51e5779c61ac27650a67032a52b165`.

| Capture | Proof | SHA-256 |
|---|---|---|
| 01 Populated records (admin) | 17 routes · 2 roles · 70 catalogue · 3 contracts · 1 scope; 5/5 ready; containment true | `86484983…b386` |
| 02 Scope detail interaction | hit-test **TRUE**; detail 0→1 with real record | `99e9f947…62f1` |
| 03 Operator-role REAL 403s | backend verbatim denial ×2 + 3 ready + scope rendered | `f08ab63d…4d15` |
| 04 Unprivileged M3 notice | "Access denied. … not an empty result." + verbatim detail; denied ≠ empty ≠ error | `e666e2ff…cacc` |
| 05 Empty collections scrolled | 5/5 absence markers; marker in-viewport true | `13a7eb42…09b5` |
| 06 Single-seam failure | 1 error + 4 ready; others render | `9be51843…3648` |

## 9. Deviations and disclosures (unprompted)

1. **`request()` now attaches `status` to its errors** (message unchanged) — the
   M3 403 discrimination depends on it. Disclosed: existing callers are unaffected.
2. **Evidence fixture** (register row `TD-UI-SURF-P03-UNPRIVILEGED-EVIDENCE-FIXTURE`):
   one local-dev operator with role `unprivileged` created so the REAL backend
   default-deny 403 — not interception — powers captures 03/04. Seed script
   `scripts/seed_surf_p03_unprivileged.py`, password `operator-pass-123`. No schema,
   endpoint or service change.
3. **Capture 05 uses response interception** — the five endpoints cannot return
   empty in dev (static config + one always-present own scope record), so the empty
   rendering is exercised by fulfilling them with empty payloads; recorded in the
   JSON, not concealed.
4. **R2 vs M4 tension resolved by design choice, argued not hidden:** the section
   uses five independent fetches (the Build Order's stated standard) rather than
   reusing the summary bundle; M4 is guarded by rendering records only, the
   same-endpoint agreement statement, and no silent reconciliation (§5).
5. **Bundle +14.83 kB** — OBS-5.

**No backend endpoint, schema, model or service change. No write path added — the
only buttons in the new surface are "Refresh scope" and "View detail".**

## 10. Standing

SURF-P01 and SURF-P02 closed clean. SURF-P03 delivered per this report and awaiting
determination — the final SURF phase. DATA, CHART, POLISH remain unauthorized.
Repository untouched — Operator-only.

---

**Gate CLOSED · Production NOT CERTIFIED**

*— AXIOM Development Authority (DA)*
*2026-08-17*
