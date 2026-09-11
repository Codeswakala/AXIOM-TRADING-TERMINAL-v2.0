# AXIOM — DESIGN PLAN B-07 (DA engineering design, pre-Build-Order)
## Cross-Cutting Hardening & Certification-Prep

| Item | Value |
|---|---|
| Document class | **DA design plan** (governed lifecycle: Operator Directive → DA design planning → ITRGA review → Build Order → implementation). **NOT a Build Order, NOT self-authorization, NOT implementation.** |
| Prepared by | AXIOM Development Authority (DA) |
| Date | 2026-08-20 |
| Basis | `BACKEND_ROADMAP_v2.md` §B-07 ("continuous from B-03") · BO-B-06 §12 (B-07 issuable on B-06 approval) · register rows TD-095 / TD-W7-U07-RATE-GUARD (formally deferred) · TD-B04-UNIT D2 (RBAC depth deferred here) |
| Status | Ready for ITRGA review; implementation begins only on an issued Build Order |

---

## 0. Verified current state (what exists — the plan hardens this, not builds it from zero)

- **Observability:** the observability middleware assigns a correlation id per request (`cid=` in every server log); the W-pipeline audit rows (B-04/B-05/B-06 included) carry actor + correlation id. Missing: per-pipeline span/metric telemetry beyond audit rows.
- **Security:** every new endpoint (B-04/B-05/B-06) is `CurrentOperatorDep`-authenticated with request-schema validation; secret-marker redaction is enforced in the assistant path; the non-actuation static guards pass. Deferred: rate limiting (TD-095 / TD-W7-U07-RATE-GUARD), permission-granular RBAC on the new families (B-04 D2).
- **Performance:** WS hub exists with fan-out; the intelligence/alert surfaces gained new query patterns (list+filter; alert dedup by `(alert_type, subject_id)`). Known hot paths: alert dedup scans, report list ordering, B-04 grounding multi-family resolution.
- **Evidence base:** 537 backend + (this turn) frontend suites; 9 transmission sets; audit rows for every governed action; refusal records; the full 27-element chain.

## 1. Proposed scope (candidate — the BO governs)

### B-07.1 — Observability completeness
- Per-pipeline telemetry on the new generation/emission/ask paths: count, duration, and correlation id per family (structured log lines, no new infrastructure — consistent with the zero-dependency discipline).
- Correlation-id propagation audit: every B-04/B-05/B-06 path writes audit rows carrying the request correlation id (verify by probe, not assertion).

### B-07.2 — Security review + rate limiting
- **Endpoint security audit** of all 27-element-chain endpoints: RBAC, input validation, 401/404/409/422 semantics, secret-marker redaction, hidden-actuation scan — evidenced per endpoint, not summarized.
- **Rate limiting (closes TD-095 / TD-W7-U07-RATE-GUARD):** the register rows bind a spike before a BO. **Spike proposal:** a pure-Python in-memory sliding-window limiter (bounded per-operator+endpoint), no new dependency, no storage — honest limits with 429 responses. Alternative (redis-backed, distributed) requires a dependency + storage spike and is NOT proposed unless the BO directs it.
- **Permission-granular RBAC** on the B-04 generation families and the B-05/B-06 write paths (if authorized): role→endpoint matrix, default-deny, test-pinned with the unprivileged fixture role.

### B-07.3 — Performance & indexing
- **Index proposal (migration — requires BO authorization per standing no-migration-by-default rule):** `monitoring_alerts(alert_type, subject_id, created_at)` for the dedup window; report-family `created_at` indexes if the probe shows order-by scans; `assistant_research_responses(created_at)` for the read surface.
- Concurrency/load probes: generation endpoints under repeated calls (dedup/cooldown correctness under concurrency), WS fan-out sanity, B-04/B-06 query latency with the real corpus populated.

### B-07.4 — Doc 11 evidence assembly
- Inventory and index the evidence the platform already holds (audit rows, refusal records, security-invariant suites, transmission sets, per-phase verification JSONs) into the Doc-11 structure — **assembly and indexing only**. Production certification remains a separate Operator/ITRGA decision; nothing in B-07 changes the gate.

## 2. Exclusions (candidate)

No actuation/gate changes · no new external services · no ML · no frontend (F-units) · no scheduled/background actors beyond what exists · no schema migration without BO authorization (the index proposal is flagged AS a migration-requiring item).

## 3. Proposed acceptance criteria (for the eventual BO)

- [ ] Per-pipeline telemetry present and probed on the B-04/B-05/B-06 paths.
- [ ] Endpoint security audit delivered per-endpoint with evidence.
- [ ] Rate limiting live with 429 semantics; spike justification documented; TD-095/TD-W7-U07-RATE-GUARD closure proposal recorded.
- [ ] Any authorized index migration applied with the migration-justification documented; no other schema change.
- [ ] Doc 11 evidence index assembled.
- [ ] Full suites green (backend 537+ · frontend); transmission manifest relay-accurate (CA-TRANSMIT-1).

## 4. Evidence + delivery (when authorized)

Patch + `git apply --check` transcript (chain position 28) · fail-first probes · executed test logs · per-endpoint probe outputs · delivery report with transmission manifest — the standing discipline.

---

**End of Design Plan B-07** — submitted for ITRGA review; the DA implements only on an issued Build Order.

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
