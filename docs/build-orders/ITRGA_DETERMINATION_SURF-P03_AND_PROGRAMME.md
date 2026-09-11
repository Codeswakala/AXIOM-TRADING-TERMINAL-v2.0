# ITRGA DETERMINATION — SURF-P03 · AND SURF PROGRAMME CLOSURE

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** Governance & platform records — final SURF phase
**Date:** 2026-08-17
**Base:** `34f4c62` + item3 + item5 + item6 + item4 Rev B + SURF-P01 + OBS-SURF1-2 + SURF-P02
**Verification:** `/tmp/p3f` — pristine clone → eight-element chain → SURF-P03 applied

| Artifact | sha256 | Size |
|---|---|---|
| `surf_p03.patch.txt` | `c18d5d05816de0cb` | 1,609 lines · 9 files |
| `DELIVERY_REPORT_SURF-P03.md` | `cc4c7d35c3928393` | 175 lines |
| `SURF-P03_CAPTURE_VERIFICATION.json (1).txt` | `0908df2a26c79bea` | 95 lines |
| 5 PNGs transmitted | all reconcile | 1920×1080 |

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

Every mandatory and standing requirement is met. One observation: a sixth capture is described in the verification record but was not transmitted.

**Transport:** `c18d5d05816de0cb…` matches exactly; `git apply --check` exit 0; full eight-element base chain declared. **Eighth consecutive hash-reconciled delivery.**

---

## 2. M3 — THE ACCESS-DENIAL REQUIREMENT, CORRECTLY MET

This was the phase's governing risk: a 403 rendered as absence would tell the operator *no records exist* when the truth is *you may not see them*.

**It is not handled by string-matching an error message.** The client types the outcome:

```ts
export type OperatorScopeListResult =
  | { kind: "denied"; detail: string }
  | ...
return status === 403 ? { kind: "denied", detail } : { kind: "error", detail };
```

A distinct `denied` kind, discriminated on **HTTP status**, flowing into a distinct UI state — `"loading" | "error" | "ready" | "denied"` — with its own testid `platform-source-status-denied`.

The rendered notice:

> **Access denied.** Access to institutional scope records is denied for your role. **This is an access restriction, not an empty result.**
> `Institutional scope access denied`

That final clause states the distinction explicitly to the operator. Empty results render entirely different strings — *"No scope records returned for this operator."* Denial and emptiness cannot be confused.

**Capture 04 confirms it under a real backend 403**, with the unprivileged operator visible in the header (`surf-p03-unprivileged-028efc57`) and all four record sections showing `Institutional permission denied by default-deny policy` in red. **Produced by the real default-deny policy, not by interception** — the DA states this and the seeded-operator fixture supports it.

---

## 3. REMAINING REQUIREMENTS

### M1 — Frontend T-1 guard ✓

`test_platform_records_ui_module_has_no_governance_mutation_controls` at `test_institutional_platform_security.py:270`, with **four non-vacuity anchors**:

```python
assert "platform records" in text
assert "route inventory" in text
assert "inspection view" in text
assert "access restriction, not an empty result" in text
forbidden = (..., "enable_plugin", "grant_permission", "elevate_role")
```

The fourth anchor is notable: it pins the **M3 notice itself** as a guard condition, so the access-denial honesty cannot be silently removed in a later phase.

The docstring names the domain risk precisely — *"rendering an RBAC role list must never look like editing one, and a plugin contract list must never look like enabling a plugin."* No institutional-platform security test pinned a frontend path before this phase.

### M2 — Inspection posture ✓

Zero mutation affordances found. The surface declares itself:

> **Inspection view** — No control here can modify roles, register routes, alter scope, or enable plugins

### M4 — One code path per statistic ✓

> Every value below is an existing record read from the institutional platform. Values that also appear in the posture summary above come from the same endpoints and **must agree; nothing here is reconciled silently.**

The `CA-P04-2` / `OBS-CONV2-1` defence, stated in the UI.

### Scope and standing requirements

| Req | Result |
|---|---|
| **S1** four collections | Route Inventory · RBAC Role Permission · API Catalogue · Plugin Contract — all rendered |
| **S2** scope records | List + detail, both surfaced |
| **S3** home | Governance overlay extended — correct; it already owned the summary |
| **S4** testids | **33** |
| **R2** degradation | Per-source `loading/error/ready/denied` across five fetches |
| §2 exclusions | **Audit trail and workspace preferences untouched** — 0 references |
| No new write path | Confirmed |

**Capture 01 evidences the surfacing gap being closed:** `routeEntries: 17`, `roleEntries: 2`, `catalogueEntries: 70`, `contractEntries: 3`, `scopeRecords: 1`. Before this phase the overlay reported an API catalogue *version and route count*; **the 70 catalogue routes themselves were unreachable.** Four dead client functions now have consumers.

`capture01_source_status_legibility` records `cardCount: 5`, `cardsFullyInsidePanel: true` — the `OBS-SURF1-2` collapse check is now standard practice, applied without being asked.

### Execution evidence

```
Test Files  169 passed (169)
     Tests  813 passed (813)      ← +10
tsc exit: 0
pytest      418 passed            ← +1 (the M1 guard)
build       index-ByTeB58D.js 718.83 kB │ gzip 192.26 kB
```

**1,231 tests green.** Bundle 704.00 → 718.83 kB (+14.83 kB), disclosed under `OBS-5`.

---

## 4. `OBS-CONV2-5` — CLOSED

The seeded evidence fixtures have been carried as an open finding since CONV-P02. This delivery **formally registers them** in `TECHNICAL_DEBT_REGISTER.md`:

- `TD-UI-SURF-P02-ALERTS-EVIDENCE-FIXTURE` — three alerts, one per severity Literal, one acknowledged
- `TD-UI-SURF-P03-UNPRIVILEGED-EVIDENCE-FIXTURE` — one `unprivileged` operator, *"produced by the REAL backend default-deny 403, not by interception"*

Both entries name the seed script, the lineage actor, and state *"local-only and gitignored; no schema, endpoint or service change."*

That is exactly the disposition I asked for when the `sig-004` fixture was first disclosed. **The register is now the record, not the delivery reports.**

---

## 5. OBSERVATION — `OBS-SURF3-1`: capture 03 not transmitted

| Field | Content |
|---|---|
| **Requirement** | Build Order §7.7 — Level-I captures attached. |
| **Evidence** | The verification JSON declares `SURF-P03_03_OPERATOR_ROLE_REAL_403_PARTIAL_DENIAL.png` (`f08ab63d…`) recording `errorRows: 2, readyRows: 3, scopeListRendered: true`. **Not among the transmitted files.** |
| **What it uniquely showed** | A **partial** denial — the `operator` role denied on route-inventory and RBAC while three other sources render and the scope list still populates. Captures 04 (full denial) and 06 (single-seam failure) do not cover the mixed case. |
| **Mitigating** | The behaviour is corroborated by the machine record and by source: the per-source state machine treats `denied` per source, so mixed states follow structurally. Five of six captures transmitted, all hashes reconciling. |
| **Required Correction** | Attach the file. |
| **Owner** | DA |

**Not blocking.** No acceptance criterion depends solely on it. Note also that capture 04 was attached twice, byte-identical (`e666e2ff…`) — harmless, but suggests the omission was an attachment slip rather than a withheld artifact.

---

## 6. SURF PROGRAMME — COMPLETE

| Phase | Determination |
|---|---|
| SURF-P01 Execution Research dock | APPROVED WITH OBSERVATIONS — closed |
| SURF-P02 Alerts | **APPROVED** — `TD-061` closed |
| SURF-P03 Governance & platform | **APPROVED WITH OBSERVATIONS** |

# SURF programme: COMPLETE

Blueprint §5 rated SURF *highest value per unit effort*. The record bears that out — the phase found the same pattern three times:

- **P01** — six detail GETs unreachable; a silent `slice(0, 5)` truncation; **no frontend T-1 guard** on the most execution-adjacent surface in the platform.
- **P02** — `MonitoringAlertsPanel` built, tested, and mounted nowhere; `limit = 5` against an endpoint accepting 200.
- **P03** — four client functions written, typed, and **called by nothing**; one endpoint with no client at all.

**Capability that exists but cannot be reached is the platform's dominant defect class.** Every SURF phase surfaced real, already-built functionality rather than adding new capability — precisely the turn-56 reframe.

Three frontend T-1 guards were added, one per phase, each with non-vacuity anchors. Before SURF, no frontend path was pinned by any execution-research, alerts, or institutional-platform security test.

---

## 7. STATUS

| Finding | State |
|---|---|
| **SURF-P03** | **APPROVED WITH OBSERVATIONS** |
| **SURF programme** | **COMPLETE** |
| `OBS-CONV2-5` seeded fixtures | **CLOSED** — formally registered |
| `OBS-SURF3-1` capture 03 | **NEW** — one attachment |
| `OBS-5` bundle 718.83 kB | Open — **POLISH-P01**, now +36.7 kB across SURF |
| `F-BRAND-1` | Open — GA-173, Operator |

**Artifacts of record** (`/home/user/uploads/`), applying clean in order:

```
item3.patch.txt            b7b4c4f74f3016cb
item5.patch.txt            4c03910c76fdcbf2
item6.patch.txt            f65da5c3ce8433ec
item4.patch (1).txt        a516c2c144c1f2f6
surf_p01.patch.txt         62c4d021e5b6f0a0
surf_p01_obs1-2.patch.txt  69964afec17b9c0f
surf_p02.patch.txt         e039c74bc9993640
surf_p03.patch.txt         c18d5d05816de0cb
```

**Next: DATA-P01** — extend the simulated feed to all 11 instruments with correlated realistic walks, per-symbol seeding, watchlist sparklines from real series. Blueprint §5 notes *"Ten rows showing `--` is the single largest perceived-quality defect."* Every capture in this programme confirms it: the watchlist shows `--` for all eleven pairs throughout.

**DATA-P01 changes character again.** CONV re-homed, SURF surfaced — DATA *generates*. That raises a provenance question the earlier phases did not: simulated series must be unmistakably labelled as such, and must never be presentable as market data. I will inventory the feed and its provenance guarantees before issuing the Build Order. **Not authorized.**

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination approves SURF-P03 and closes the SURF programme. It is not authorization for DATA, CHART or POLISH.

**We don't guess. We prove.**
