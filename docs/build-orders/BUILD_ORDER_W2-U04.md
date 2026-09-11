# AXIOM BUILD ORDER — W2-U04

## ML Research: Reproducible Dataset Snapshot Builder + Temporal Split Engine

**Build Order ID:** W2-U04
**Wave:** 2 — Machine Learning Research Framework · **Unit:** 04
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-13
**Authorized By:** ITRGA, following **W2-U03 APPROVED** (Platform v0.15.0) + operator authorization
("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on:** W2-U01 (dataset architecture + chronology guard + **R-2 label-horizon/embargo contract**) +
W2-U02 (query port + market metadata) + W2-U03 (feature store + causal features + reproducible feature hash).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Reproducible Dataset Snapshot Builder** and the **Temporal Split Engine** — the last
dataset-layer unit before the experiment registry (W2-U05) and the hard model gate. This unit turns
guarded, canonical data + versioned features into **frozen, content-hashed, bit-for-bit reproducible
training snapshots**, split into **train / validation / test by time only**, with **label-horizon /
embargo (purge) leakage refused** at the split boundary.

This is where the two most catastrophic ML mistakes are finally *made impossible by construction*:
**(1) an irreproducible dataset** (you can't trust or audit a result you can't rebuild), and **(2) split
leakage** (a random split, or a label horizon bleeding across the train/test boundary, that silently
inflates every downstream metric). W2-U01 defined the contract and reason codes (`SPLIT_LEAKAGE`,
`LABEL_HORIZON_LEAKAGE`, R-2/R-3); **this unit builds the engine that enforces them and proves it refuses
the bad cases.**

This unit builds **datasets and splits** (research artifacts) but **no model, no training, no inference,
no execution.**

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No model / training / inference / prediction.** Snapshot + split artifacts only. Labels may be
  *constructed as inert dataset columns* (needed to test horizon leakage), but **nothing is trained**.
- ❌ **No execution / broker / provider live connection / credentials.** W1-U03 Governance Gate CLOSED;
  External Integration untouched.
- ❌ **No random / shuffled train-val-test split.** Splits are **temporal only** — a random-split request
  must be **rejected** (`SPLIT_LEAKAGE`), proven by negative test.
- ❌ **No label-horizon leakage.** No training label's forward horizon may overlap the validation/test
  window; an **embargo/purge gap** must separate splits. A label crossing the boundary must be **rejected**
  (`LABEL_HORIZON_LEAKAGE`), proven by negative test (the R-2 contract, now enforced by the engine).
- ❌ **No non-reproducible snapshot.** Rebuilding a snapshot over unchanged inputs must yield the
  **identical content hash** (deterministic ordering, precision, serialization; pinned feature version;
  UTC normalization; no wall-clock-derived values). Proven by build-twice → same hash.
- ❌ **No authoritative use of quarantined / synthetic / forward-dated records.** The W2-U01 chronology
  guard still governs what may enter a snapshot; `seed:synthetic` / forward `live:simulated` stay
  excluded from authoritative training sets (OBS-1, enforced).
- ❌ **No symbol identity in the training matrix (D-W2-001).** The snapshot's feature columns exclude
  symbol/provider identity (metadata may be *attached for slicing/evaluation*, not as a learned column) —
  keep the W2-U03 exclusion assertion green.
- ❌ **No DB reach-around** (query port only), **no secrets in logs** (§77), **no fabricated data.**
- ❌ **No regression** (Wave-0/1 + W2-U01/U02/U03). Full suite + prior guard tests + parity smoke green.
- ✅ **Preserve:** advisory/research-first, single-uvicorn, canonical v2.0, tz-aware UTC, observability,
  dataset architecture + chronology guard + query port + feature store, and all prior hardening.

---

## 3. Scope — Components A–F

### Component A — Reproducible Dataset Snapshot Builder (`07_ML_SPEC` §Dataset Governance / plan §5.5)
- Build a **frozen dataset snapshot** from a `MarketSeriesKey` selection + a pinned `feature_set_version`:
  assemble guarded canonical records → causal features (W2-U03) → an immutable, content-hashed artifact
  bound to the W2-U01 `dataset_snapshots` architecture (deterministic ordering
  `(market_class, provider, symbol, timeframe, open_time, source, id)`; canonical serialization; SHA-256).
- **Reproducibility mechanisms** (plan §5.5): pinned feature version, deterministic numeric precision/
  rounding policy, UTC normalization, environment/code manifest, artifact checksum, **no wall-clock-derived
  feature values.** Rebuild `vX` → identical hash.
- A frozen snapshot is **immutable**; any change → a **new version**, never mutation (already enforced in
  W2-U01 — re-prove it survives the builder path).

### Component B — Temporal Split Engine (train / validation / test)
- Split a snapshot **by time only** into train/validation/test with explicit boundary timestamps.
- **Reject random/shuffled splits** (`SPLIT_LEAKAGE`) — negative test.
- Splits are themselves **deterministic and hashed** (same snapshot + same split config → same split
  manifest hash), so an experiment can pin an exact split.

### Component C — Label-Horizon / Embargo (Purge) enforcement (the R-2 headline)
- Support **inert label construction** (e.g. forward-return over N bars) as dataset columns — **not for
  training, only to make horizon leakage testable.**
- Enforce an **embargo/purge gap** between splits sized to the label horizon: **no training label's forward
  horizon may reach into the validation/test window.**
- **Negative test (the headline proof):** a label whose horizon crosses the split boundary is **rejected**
  (`LABEL_HORIZON_LEAKAGE`); a correctly-embargoed split **passes.** This is the ML analogue of the W1-U03
  gate refusal and the W2-U03 look-ahead refusal — *prove the leaky split is refused.*

### Component D — Persistence, manifests & lineage
- Persist the snapshot artifact + **split manifest** (boundaries, embargo size, per-split row counts,
  hashes) into the dataset architecture (Alembic migration if new columns/tables needed; conceptually a
  `dataset_split_manifests` record referencing the snapshot). Lineage: snapshot → split → (future)
  experiment input, traceable both ways (plan §5.4).
- Quality/summary: per-split row counts, date ranges, embargo gap, authoritative-source confirmation.

### Component E — Governance, registers, ADR
- **ADR:** *Temporal Split / Snapshot Reproducibility* (plan §11.3).
- **Registers:** record split-leakage & label-horizon-leakage risks as **mitigated (engine + negative
  tests)**; reproducibility risk mitigated (hash); update `PROJECT_STATE` / `CHANGELOG`; note deferrals
  (experiment pinning of splits → W2-U05; model consumption → W2-U06+).
- **OBS-1:** re-confirm the guard governs what enters a snapshot (synthetic/forward-dated excluded).

### Component F — Verification & Delivery
- Full suite green (baseline **112** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: **build-twice → identical snapshot hash**; **random split rejected** (`SPLIT_LEAKAGE`); **temporal
  split boundary correctness**; **label-horizon leakage rejected / embargoed split passes**
  (`LABEL_HORIZON_LEAKAGE`); frozen-snapshot immutability via builder; **no symbol identity in training
  matrix**; guard still excludes synthetic/forward-dated from snapshots; port-only access.
- Delivery Report per §5.

### Explicitly OUT of scope (defer)
Experiment registry / pre-registration (W2-U05); any model / training / inference / evaluation / calibration
/ economic / statistical validation (W2-U06+); live provider connections/credentials; numpy/pandas/
scikit-learn adoption **unless** a target-platform compatibility spike (Windows+Py3.14.6 install/import/
smoke) is delivered *and reviewed* per plan §4.2.

---

## 4. Success Criteria (Definition of Done)

- [ ] Snapshot builder produces a **frozen, content-hashed** dataset from guarded data + pinned feature
      version; **rebuild → identical hash**; frozen = immutable (change → new version).
- [ ] Temporal split engine produces **train/val/test by time only**, deterministic + hashed;
      **random/shuffled split rejected** (`SPLIT_LEAKAGE`) — negative test.
- [ ] **Label-horizon/embargo enforced:** a horizon-crossing label is **rejected** (`LABEL_HORIZON_LEAKAGE`),
      a correctly-embargoed split passes — negative + positive test (R-2 engine).
- [ ] Split manifest + lineage persisted (snapshot → split); authoritative-source-only confirmed; synthetic/
      forward-dated excluded (OBS-1 guard still governs).
- [ ] **No symbol identity in training matrix** (D-W2-001 assertion green); no model/training/execution;
      gate CLOSED; port-only; no secrets; no fabricated data.
- [ ] ADR + registers synced; full suite green (112/16 + new tests); no regression; W2-U01/U02/U03 tests
      still pass; conforms to `07_ML_SPEC` (§Dataset Governance / §Data Pipeline / §Statistical Validation
      temporal splits / §Research Integrity) + 05 v2.0 (§16/§77).

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **Operator test console** (raw, `collected N`): backend `pytest` **≥112 + new tests, 0 failed**;
   frontend `vitest 16`; `ruff` clean; `tsc`/build clean.
2. **Migration evidence** (if schema added): clean `alembic upgrade head` on `PostgresqlImpl`, new head id
   shown. (If none, state so; show head unchanged.)
3. **Reproducibility evidence:** build a snapshot **twice → identical content hash** (show both hashes
   equal); frozen snapshot rejects mutation (new version created).
4. **Split-leakage negative evidence:** a **random/shuffled split request is rejected** (`SPLIT_LEAKAGE`);
   a temporal split shows correct boundary timestamps + per-split counts.
5. **Label-horizon evidence (headline):** a horizon-crossing label **rejected** (`LABEL_HORIZON_LEAKAGE`);
   a correctly-embargoed split **passes** — both visible.
6. **Named-test capture:** `pytest <ml test files> -vv` **captured** (`| Tee-Object` / `-rA`) so each named
   W2-U04 test PASS is visible (continue the W2-U03 capture standard).
7. **Containment/D-W2-001 evidence:** shown grep (R7) that the training matrix excludes symbol identity and
   the builder uses the query port (no ORM reach-around).
8. **CI evidence:** orchestrated pipeline green on PostgreSQL (local acceptable; remote preferred),
   fail-closed.
9. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
10. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Clean architecture / bounded context / single ownership (ML Research owns the builder + split engine);
dependency-inward via query port + feature store; **temporal-only, embargoed, leak-free splits**
(`07_ML_SPEC` §Statistical Validation / §Research Integrity; R18); **reproducible** (snapshot + split
hashes); **no symbol identity in training matrix** (D-W2-001); **no fabricated data**; no broker/execution/
credentials (§15, gate CLOSED); no secrets (§77); tz-aware UTC. Every change in the registers (R20).
Cross-platform (Windows + docker/PostgreSQL).

---

## 7. Process
Implement → internal verify (suite + reproducibility + split-leakage + label-horizon negative/positive) →
doc sync (PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence (operator-run, green, leaky
split refused, build-twice-same-hash, named tests captured) → **submit to ITRGA** → independent review →
corrections if required → approval → next Build Order (W2-U05). The DA does not self-approve, does not
self-authorize the next unit, and does not open the gate.

---

## 8. Priority Guidance (if staged)
**A (reproducible snapshot builder + hash) → B (temporal split engine + reject random) → C (label-horizon/
embargo enforcement — the R-2 headline) → D (manifests + lineage) → E (ADR/registers) → F (verify).**
Highest-value / highest-risk: the **label-horizon/embargo** and **random-split-rejected** negatives, plus
**build-twice→same-hash** — these are the leakage-and-reproducibility guarantees every downstream model
result depends on. *Prove the leaky split is refused and the rebuild is identical* — do not assert them.

---

## 8b. Hard Gate Reminder
**No model unit (W2-U06+) is reviewable until W2-U01–U05 are Level-I proven on the target.** U01 + U02 +
U03 proven; this is **U04 — the penultimate gate layer.** Only **U05 (experiment registry / pre-
registration)** remains after this before any model work. Broker gate CLOSED throughout Wave 2.

---

*ITRGA — Build a dataset you can rebuild to the same hash, and split it by time with a moat between train
and test so no label can see its own future. The two mistakes that quietly ruin ML research —
irreproducibility and leakage — end here, proven by a leaky split that is refused and a snapshot that
rebuilds identical. One layer left after this before the first model. We don't guess. We prove.*
