# BUILD ORDER — SURF-P03

**Issuing authority:** Independent Technical Review & Governance Authority
**Authorized by:** Operator, 2026-08-17
**Programme:** SURF — Surface the unsurfaced · **Phase 3 of 3 — final SURF phase**
**Base:** `34f4c62` + item3 (`b7b4c4f7…`) + item5 (`4c03910c…`) + item6 (`f65da5c3…`) + item4 Rev B (`a516c2c1…`) + SURF-P01 (`62c4d021…`) + OBS-SURF1-2 (`69964afe…`) + SURF-P02 (`e039c74b…`)
**Predecessor:** SURF-P02 — APPROVED, no observations

---

## 1. OBJECTIVE

Blueprint §5, verbatim:

> **SURF-P03** **Governance & platform** — audit trail, RBAC, scope records, API catalogue, route inventory, plugin contracts, workspace preferences.

---

## 2. ⚠ SCOPE CORRECTION — FOUR OF SEVEN ARE ALREADY SURFACED

I flagged this overlap risk when approving SURF-P02 and have now inventoried it. **The blueprint's list predates CONV items 3, 4 and 5.**

| Blueprint item | Current state | In scope? |
|---|---|---|
| **Audit trail** | **Fully surfaced** — CONV item 5 governance overlay: Audit Explorer, `{selectedEvent.action}`, Details payload, Refusal reason-code viewer | **NO** |
| **Workspace preferences** | **Fully surfaced** — CONV item 3 settings overlay: Preference Editor, Saved Preferences, Preference Detail, create + update | **NO** |
| **RBAC** | **Summary only** — overlay shows `RBAC policy`, `RBAC vocabulary` | **PARTIAL** |
| **Route inventory** | **Summary only** — `version`, `actuation_surface_present`, `governance_gate_capability_present` | **PARTIAL** |
| **API catalogue** | **Summary only** — `version / route count`, `Abuse guard` | **PARTIAL** |
| **Plugin contracts** | **Summary only** — `Dynamic plugin code enabled`, `Third-party plugin enabled` | **PARTIAL** |
| **Scope records** | **Not surfaced at all** — no client function exists | **YES** |

**Do not re-home the audit trail or workspace preferences.** They are single-implementation and correctly placed. Duplicating them would violate the turn-56 reframe and reintroduce the orphan pattern closed in `OBS-CONV3-3`.

---

## 3. VERIFIED STARTING STATE

### 3.1 Four client functions exist and NOTHING consumes them

```
api/client.ts:733  fetchRouteInventory()      → 0 consumers (incl. tests)
              :741  fetchRbacPermissions()     → 0 consumers
              :749  fetchApiCatalogue()        → 0 consumers
              :757  fetchPluginContracts()     → 0 consumers
```

Verified by `grep -rl` across all of `frontend/src` excluding `api/client.ts`: **zero files, tests included.** These are dead client functions — written, typed, and never called. This is the `MonitoringAlertsPanel` orphan pattern one layer lower.

### 3.2 The overlay reads a *different* endpoint

`GovernanceOverlay.tsx:547` renders "Route, RBAC, API & plugin posture" from `fetchPlatformOperationsEvidence` — a **summary bundle**. It shows scalars only:

```
Route inventory version · Route actuation surface present · Route Gate capability present
RBAC policy · RBAC vocabulary
API catalogue version / route count · Abuse guard
Dynamic plugin code enabled · Third-party plugin enabled
```

**The dedicated endpoints return substantially more**, and the record arrays are what is missing:

| Endpoint | Unsurfaced content |
|---|---|
| `GET /route-inventory` | **`routes: Array<Record<string, unknown>>`** — the inventory itself |
| `GET /rbac/permissions` | **`roles: Record<string, string[]>`** — per-role permission lists · `forbidden_capabilities_present` |
| `GET /api-catalogue` | **`routes: Array<...>`** · `abuse_guard {status, reason}` · `persistence {catalogue_table_persisted, alembic_head_expected}` |
| `GET /plugin-contracts` | **`contracts: Array<...>`** · `capability_allowlist: string[]` · `plugin_execution_audit_table_present` |

**The summary says a route inventory exists and reports its version. It never shows the routes.** That is the surfacing gap.

### 3.3 Scope records — RBAC-gated, entirely unsurfaced

```python
@router.get("/operator-scope-records")          # institutional_platform.py:234
async def list_operator_scope_records(operator: CurrentOperatorDep) -> list[dict[str, str]]:
    if "institutional.operator_scope.read" not in permissions_for_role(operator.role):
        raise HTTPException(status_code=403, detail="Institutional scope access denied")
    return [asdict(InstitutionalScopeRecord.from_operator(operator))]

@router.get("/operator-scope-records/{operator_id}")   # :247
```

`grep -c 'operator-scope-records|OperatorScope'` in `api/client.ts` → **0**. No client function, no type, no UI.

**This endpoint returns 403 for insufficient role.** It is the only SURF-P03 surface that can legitimately deny access — see M3.

### 3.4 No frontend T-1 guard on any platform surface

`test_api_catalogue.py`, `test_institutional_platform_security.py`, `test_plugin_contracts.py` — **none pins a frontend path.** Same gap SURF-P01 M1 and SURF-P02 M4 closed for their domains.

---

## 4. SCOPE

### IN SCOPE

**S1 — Surface the four record collections.** `routes` (route inventory), `roles` (RBAC), `routes` + `abuse_guard` + `persistence` (API catalogue), `contracts` + `capability_allowlist` (plugin contracts). Wire the four dead client functions to a rendered surface.

**S2 — Surface operator scope records.** Add the client function(s) and UI for `GET /operator-scope-records` and `/{operator_id}`, subject to M3.

**S3 — Choose a home and state the reasoning.** These are governance-platform records. Extending the existing **governance overlay** with a deeper platform section is the obvious candidate — it already owns this domain, and `GovernanceOverlay.tsx` already renders the summary these records expand. A separate surface is defensible if argued. **A bottom-dock research tab is not** — this is not research output.

**S4 — `data-testid` across all new regions.** Prior deliveries: 8, 10, 20, 17, 23, 20, 27, and SURF-P02's set.

### OUT OF SCOPE

- **Audit trail and workspace preferences** — §2. Do not touch, do not duplicate.
- **The 4 POST / 1 PUT / 3 DELETE endpoints** on `institutional_platform.py`. Those belong to research collections, tags, members and workspace preferences — already surfaced by CONV items 3 and 4 where in scope. **No new write path is authorized in this phase.**
- DATA · CHART · POLISH · the 704 kB bundle (`OBS-5`) · `F-BRAND-1` · **any backend endpoint, schema, model or service change**.

---

## 5. 🔴 MANDATORY

**M1 — Frontend T-1 guard.** Extend `test_institutional_platform_security.py` with a source-inspection test over the new UI module, per the SURF-P01 M1 / SURF-P02 M4 pattern:
- **non-vacuity anchors** — positive assertions that the file renders the surface,
- absence of `place_order`, `submit order`, `go live`, `connect broker`, `broker_account`, `execute`, `enable_plugin`, `grant_permission`, `elevate_role`.

The domain-specific risk here is a **governance-inspection surface appearing to confer governance-mutation capability**. Rendering an RBAC role list must never look like editing one. Apply the SURF-P02 disclaimer-exclusion technique if a legitimate sentence contains a forbidden term.

**M2 — Read-only presentation, unmistakably.** No control may imply editing roles, enabling plugins, registering routes, or changing scope. Every one of these surfaces is an **inspection** view of governance state.

**M3 — Handle the scope-records 403 honestly.** If the operator lacks `institutional.operator_scope.read`, render an explicit, plainly-worded access notice. **Never** an empty list, `0`, `—`, or a silent omission. An access denial rendered as absence-of-data is a data-honesty defect of the `OBS-CONV2-1` family: the operator would conclude no records exist when the truth is that they may not see them. This must be **visibly distinct** from a genuine empty result.

**M4 — Do not contradict the existing summary.** The overlay already renders scalars from `fetchPlatformOperationsEvidence`; the detail comes from four different endpoints. If a value appears in both places it must agree, or the divergence must be shown and explained rather than silently preferring one source. **One code path per statistic** — the `CA-P04-2` / `OBS-CONV2-1` defence.

---

## 6. STANDING REQUIREMENTS

**R1 — No fabricated values.** Route counts, permission lists, contract entries, allowlists render verbatim or as explicit absence. Never a plausible-looking number.

**R2 — Independent degradation.** Five fetches; one failure must not blank the surface. The SURF-P01 per-source pattern with genuine loaded counts is the standard.

**R3 — RBAC not widened.** 16/16 `protectedWorkspace()` wrappers, `ALL_AUTHENTICATED_ROLES = ["admin","operator"]`. Note the backend enforces `institutional.operator_scope.read` independently — **the UI must not attempt to pre-empt or bypass that check.** Call the endpoint and render what it returns, including the 403.

**R4 — Layout.** `OBS-SURF1-2`'s `flex-shrink: 0` fix is in the base. Any new scroll container must be verified at 1920×1080 — **by looking at the capture**, not by tests alone.

**R5 — Suite green.** Current: **803 frontend / 417 backend = 1,220**. New surface requires new tests. Never delete a failing test to reach green.

**R6 — `npm ci` before `tsc -b`.**

**R7 — Deletion discipline.** No orphans. If anything is superseded, delete it and re-point dependants in the same cycle.

---

## 7. DELIVERY REQUIREMENTS

**Transport — seven consecutive hash-reconciled deliveries; repeat exactly.** Neither authority commits to the repository; the verified patch is the artifact of record.

```bash
git diff <base> > surf_p03.patch
git apply --check surf_p03.patch ; echo "exit=$?"
sha256sum surf_p03.patch
```

Inline in the message body · **LF endings, terminating newline** · **state the full eight-element base chain**.

**Report must contain:**

1. Chosen home + reasoning, explicitly addressing §2 — what was **already surfaced** and therefore untouched.
2. Coverage table for the five target endpoints, marking what is newly rendered versus previously summary-only.
3. **M1** guard: non-vacuity anchors and forbidden list, confirmed passing.
4. **M3** disposition: the exact access-denied text, and how it is visually distinct from an empty result.
5. **M4** disposition: which values also appear in the overlay summary, and how agreement is guaranteed.
6. Raw console transcripts — vitest, tsc -b, vite build, pytest.
7. **Level-I captures — raw PNGs** (the HTML gallery has failed to upload twice):
   - the four record collections rendered with genuine content,
   - **the scope-records 403 access notice** — the M3 evidence,
   - **an empty-state capture scrolled to the empty region**,
   - a single-seam failure showing independent degradation.
8. **Interaction trace** for any click-dependent affordance — Playwright `elementFromPoint`, per the item-4 method.
9. Exact wording: *deleted* / *relocated* / *copied* / *extended* / *surfaced*.

---

## 8. ACCEPTANCE

1. Route inventory `routes`, RBAC `roles`, API catalogue `routes` + `abuse_guard` + `persistence`, plugin `contracts` + `capability_allowlist` all rendered.
2. Operator scope records surfaced, both list and detail.
3. **M1** frontend T-1 guard present, non-vacuous, passing.
4. **M2** no governance-mutation affordance, real or implied.
5. **M3** 403 rendered as an explicit access notice, visually distinct from empty.
6. **M4** no contradiction with the existing overlay summary.
7. Audit trail and workspace preferences **untouched**.
8. No new write path.
9. `data-testid` across all new regions.
10. R1 absence renders as absence.
11. R2 independent degradation across five fetches.
12. Suite green ≥ 1,220; nothing deleted to force green.
13. `tsc -b` clean; `vite build` succeeds.
14. RBAC not widened.
15. Captures attached incl. the 403 notice and a scrolled empty state; interaction trace supplied.

---

## 9. ON SURF PROGRAMME CLOSURE

SURF-P03 is the final phase of the SURF programme. On approval I will issue the programme determination for SURF and assess the position before DATA-P01.

Blueprint §5 rates SURF *highest value per unit effort*, and the phases bear that out: SURF-P01 surfaced 6 unreachable detail endpoints and removed a silent truncation; SURF-P02 closed `TD-061` and mounted a panel that had been built, tested and unreachable. SURF-P03 addresses **four dead client functions and one entirely unsurfaced endpoint** — the same pattern a third time.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This Build Order authorizes **SURF-P03 only**. It is not authorization for DATA, CHART or POLISH.

**We don't guess. We prove.**
