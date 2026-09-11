# RESPONSE TO ITRGA CAPABILITY-IMPLEMENTATION ASSESSMENT
## AXIOM Development Authority — finding-by-finding disposition

| Item | Value |
|---|---|
| Responding party | AXIOM Development Authority (DA) |
| Date | 2026-08-19 |
| Subject | ITRGA `CAPABILITY_ASSESSMENT.md` (post-closure capability-implementation verification; Determination: **CAPABILITIES: PARTIALLY IMPLEMENTED**) |
| Ingested | `/home/user/uploads/CAPABILITY_ASSESSMENT.md` sha256 `979f815ff1a2f8ca5310918e1060084bfdc19725f68f7af8468af51cb56cfa72`; record copy at `docs/build-orders/CAPABILITY_ASSESSMENT.md` (byte-identical, cmp-verified) |
| DA method | Every finding re-verified mechanically against the working tree (baseline `34f4c62` + 18-element patch chain) this session — no finding accepted or disputed from the document alone. Both test suites re-run fresh: **476 backend passed (135.55s) · 860 frontend passed / 175 files (198.15s) · 1,336 total**, logs at `docs/evidence/uiconv/pytest_capassess_r1.log` and `docs/evidence/uiconv/vitest_capassess_r1.log` |
| Artifacts transmitted | None — this is a workspace-deliverable response; no patch is shipped with it (two corrections are staged as proposals, §4, awaiting Operator routing per standing post-closure practice) |

---

## §0 Method

The DA re-verified, per finding, with raw console output this session:

1. **FIND-1** — grepped all of `backend/app` for `LiveMarketInferenceAdapter` references and instantiations.
2. **FIND-2** — grepped all of `backend/app` for `create_report`/`create(` callers outside service modules; enumerated router verbs.
3. **FIND-3** — enumerated `@router` verbs on the collaboration router; grepped `backend/app/api` for any ask/respond path; inspected the frontend assistant surface for any input/submit path.
4. **FIND-4** — read `backend/app/ml/__init__.py`; enumerated route files for any `/ml` surface; searched for model-artifact seeds.
5. **FIND-5** — read the simulated feed adapter (`backend/app/market/adapters/simulated.py`) including its bar-timestamp construction and tick interval.
6. **FIND-6** — ran `npm audit --json` against a freshly restored `node_modules` (`npm ci` exit 0); traced the advisory chain with `npm ls`.

Raw evidence is quoted in §2. No summary-of-summary: every claim below cites the transcript.

---

## §1 Disposition table

| Finding | DA verdict | Classification | Disposition |
|---|---|---|---|
| FIND-1 — Signals not operable end-to-end | **CONFIRMED** | By design (R3 / no model authorization / T-5) | Accepted; recorded; no code change without a Build Order |
| FIND-2 — Intelligence has no generation path | **CONFIRMED** (one refinement: execution-research risk reports DO have an operator-triggered generation path — the finding correctly covers the other five families) | By design (no training-data authorization) | Accepted; recorded |
| FIND-3 — Assistant has no request path | **CONFIRMED** | By design (UI-008 documented read-only API seams; T-4/T-5) | Accepted; recorded; engine exists and is tested — exposing it = new endpoint = needs authorization |
| FIND-4 — ML platform is a stub | **CONFIRMED** | By design (W0-U01 architectural boundary) | Accepted; recorded |
| FIND-5 — Future-dated simulated bars | **CONFIRMED** (rate measured at ~60×, not the assessment's ~30× — direction identical) | **DEFECT CLASS** — violates the closure standard "a displayed value means what it claims" | Correction designed and staged (§4.1); awaiting Operator routing — the DA will not open the simulator unilaterally |
| FIND-6 — Supply-chain advisories | **PARTIALLY CONFIRMED** with two refinements (§2.6) | Mixed: postcss already closed; react-router already registered; **nanoid HIGH is new and breaches the project's own high-audit gate** | Correction designed and staged (§4.2); awaiting Operator routing |

Determination "CAPABILITIES: PARTIALLY IMPLEMENTED" — **ACCEPTED**, with the reconciliation in §3: the runtime-data lens ITRGA applied is finer than the DA's code-presence checklist, and the DA adopts it for the record. The reconciled position: the platform is a fully operable terminal shell and analysis engine; every generation-dependent surface is correctly absent by design, not by defect, and says so honestly in-product. No production-certification implication was ever claimed by the DA; posture unchanged.

---

## §2 Verification evidence per finding

### §2.1 FIND-1 — signals: adapter defined, never instantiated. CONFIRMED.

```
$ grep -rn "LiveMarketInferenceAdapter" backend/app --include="*.py" | grep -v test
backend/app/trading_intelligence/live_market/__init__.py:5:    LiveMarketInferenceAdapter,
backend/app/trading_intelligence/live_market/__init__.py:13:    "LiveMarketInferenceAdapter",
backend/app/trading_intelligence/live_market/adapter.py:50:class LiveMarketInferenceAdapter:

$ grep -rn "LiveMarketInferenceAdapter(" backend/app --include="*.py"
(no output — zero instantiations anywhere)
```

The assessment's claim is exactly right: export + class definition only, no instantiation, no invocation. **By design:** signal generation requires an `advisory_approved` model with validation/calibration/economic/generalization reports; no model training was ever authorized in any of the eight approved phases; the ML platform is a W0-U01 stub (FIND-4); T-5 prohibits external-LLM generation. The SURF-P03-approved signal surface is the presentation + honesty layer: with no rows and no generator, it renders "No advisory signals returned." — the R3 discipline ITRGA itself mandated and approved across SURF-P03. The DA's R1 checklist marking §7 IMPLEMENTED measured code-presence; under ITRGA's runtime lens it is SCAFFOLD-by-design. Both statements are true of different measurements; the reconciled record (§3) carries both.

### §2.2 FIND-2 — intelligence: five families have no generation caller. CONFIRMED (one refinement).

```
$ for svc in correlation regime scenario portfolio_risk signal_validation; do
>   grep -rn "create_report" backend/app/institutional_intelligence/$svc.py | grep "async def"
> done
correlation.py:49:    async def create_report(
regime.py:71:        async def create_report(
scenario.py:56:       async def create_report(
portfolio_risk.py:55:    async def create_report(
signal_validation.py:50: async def create_report(

$ grep -rn "create_report" backend/app --include="*.py" | grep -v "def create_report" | grep -v test
backend/app/api/routes/execution_research.py:262:  return await service.create_report(draft=draft, actor="operator")
backend/app/api/routes/execution_research.py:374:  return await service.create_report(draft=draft, actor="operator")
```

Five `create_report` services exist; the only runtime callers in the entire backend are the two execution-research endpoints (the simulated risk-report generation path, which IS operator-triggered and works — the assessment's matrix correctly treats execution research separately). The intelligence router exposes list/get only. **Refinement to the finding:** "no endpoint or startup hook calls create_report" is true for the five intelligence families and false for execution research — the DA states the distinction so the record is exact. **By design:** these services generate reports from datasets; the programme authorized no training/generation datasets (the ITRGA Analytics assessment documents the data-gating basis). The read-only surfaces honestly render "No … returned."

### §2.3 FIND-3 — assistant: no request path anywhere. CONFIRMED.

```
$ grep -n "@router" backend/app/api/routes/collaboration.py
 72:@router.get(     # list assistant-responses
 86:@router.get(     # get assistant-response/{id}
103:@router.get(     # chart-annotations list
121:@router.get(     # chart-annotation detail
138:@router.post(    # chart-annotations create  (audited inert annotation)
164:@router.patch(   # chart-annotation update
188:@router.delete(  # chart-annotation delete
207:@router.get(     # trade plans list
221:@router.get(     # trade plan detail
238:@router.post(    # trade plan create  (audited inert research note)
257:@router.put(     # trade plan update
281:@router.get(     # journal list
295:@router.get(     # journal detail
312:@router.post(    # journal create  (audited inert reflection)
331:@router.put(     # journal update

$ grep -rn "assistant/ask\|/ask\b\|respond(" backend/app/api --include="*.py"
(no output)
```

Frontend half, `AssistantCommandSurface.tsx` lines 87–91:

```
function handlePromptClick(prompt: string) {
    setSelectedPrompt(prompt);
    if (onSelectPrompt) { onSelectPrompt(prompt); }
}
```

Suggestion chips set state only. No input element, no submit handler, no POST call exists on any assistant surface. `RuleBasedGroundedAssistant.respond()` exists backend-side with the six-code refusal policy and is unit-tested, but is not exposed over HTTP. **By design:** the UI-008 Build Order documented "authenticated **read-only** API seams" for the assistant — the deliverable was an audited response/refusal record viewer with a deterministic grounded-summary engine, scoped under T-4/T-5 (zero external LLMs, assistant subordinate, grounding required). The assessment's "record viewer, not an assistant" phrasing is accurate and will be adopted in the record. If an operable local ask path is ever desired, the engine already exists; the new endpoint requires a Build Order — the DA will not create endpoints without authorization.

### §2.4 FIND-4 — ML stub. CONFIRMED.

```
$ head -8 backend/app/ml/__init__.py
"""Machine Learning platform package stub.

Per Build Order W0-U01, no ML pipelines or models are implemented.
This package exists solely to reserve the architectural boundary defined
in SYSTEM_ARCHITECTURE.md and ML_SPEC.md.
"""
ML_PLATFORM_STATUS = "stub"
```

Route inventory: 16 router files (`auth, advisory_analytics, advisory_signals, collaboration, execution_research, health, ingestion, institutional_platform, intelligence, market, monitoring_alerts, observability, operator, persistence, system, ws`) — **no `/ml` surface**. Model-artifact schema exists (DB models), zero seeds, zero rows, zero experiments. This is the W0-U01 architectural boundary, unchanged by every phase; the ITRGA Analytics assessment recorded the data-gating basis. The catalogue's ML-family language is design-level; nothing in the product claims otherwise.

### §2.5 FIND-5 — future-dated bars. CONFIRMED; rate measured at ~60×.

`backend/app/market/adapters/simulated.py`, lines 23 and 157:

```
interval_seconds: float = 1.0        # constructor default
...
open_time = self._start_time + timedelta(minutes=self._seq)
```

One M1 bar per ~1-second wall tick: the simulated clock advances one minute per wall second — **~60× real-time** (the assessment's "one M1 bar per ~2s tick ⇒ ~30×" is the same defect class; the DA measured the actual default interval at 1.0s). After N seconds of feed runtime the latest bar is dated ~N minutes in the future; after a long session it is hours ahead. The specific 17:57Z-vs-15:05Z observation additionally contains the sandbox wall-clock-jump contribution already disclosed in `LOCAL_RUN_GUIDE.md` (the seed was generated while the sandbox clock read ~17:57; the clock later jumped back) — but the future-dating is **inherent to the adapter design**, not caused by the sandbox: it begins within the first minute of any run.

On the "carried OBS-3" label: the register's OBS-3 row is **Closed** — "W2-U01 guard rejects naive trusted timestamps". That closure covered the *naive-vs-aware* timestamp class. The *accelerated-clock/future-dating* class is distinct (timestamps are timezone-aware and structurally valid, but future-dated) and has not previously been adjudicated. The DA therefore treats FIND-5 as a **new defect class**, and accepts it: a displayed bar time that runs ahead of wall clock violates the programme's own closure standard — *a terminal where a displayed value means what it claims*. Nothing is mislabelled as to source (the `LIVE:SIMULATED` provenance stays true), but the time axis itself overstates what the simulator has actually reached.

**Status: correction designed (§4.1), staged, awaiting Operator routing.** The DA notes the standing ITRGA instruction "do not open the generators now" was scoped to the programme's seed generators; regardless, post-closure changes are Operator directives, and the DA does not open this adapter unilaterally.

### §2.6 FIND-6 — advisories. PARTIALLY CONFIRMED; two refinements; one new HIGH.

Fresh `npm audit --json` against a restored install (exit-verified `npm ci`):

```
nanoid           | severity: high     | GHSA-2v37-7h3g-55p8 | fixAvailable: True
react-router     | severity: moderate | CVE-2025-68470 bypass + SSR constructor injection | fixAvailable: True
react-router-dom | severity: moderate | open redirect leading to XSS | fixAvailable: True
```

Dependency chain (verified with `npm ls nanoid`): `vite@8.1.4 → postcss@8.5.23 → nanoid@3.3.16` (fix: nanoid ≥3.3.18).

**Refinement 1:** the assessment attributes the high severity to `react-router-dom` + `postcss`. The current audit attributes HIGH to **nanoid** (transitive via the already-remediated postcss); the react-router family is MODERATE. Register status of each component: the postcss advisory itself is **Closed** (row TD-UI-POSTCSS-HIGH: "ITRGA approved vite-8 toolchain remediation with postcss@8.5.23 and `npm audit --audit-level=high` exit 0"); the react-router moderates are **already registered** (row TD-UI-REACTROUTER-MODERATE: "Open, non-blocking; below high audit gate").

**Refinement 2 (the new fact):** nanoid@3.3.16 is a HIGH that is **not** in the register and **breaches the project's own gate** — the closed postcss row established `npm audit --audit-level=high` exit 0 as the remediation standard, and today's install fails that gate (1 high / 2 moderate / 0 critical). The DA accepts FIND-6 on this basis. Fix is a patch-level transitive bump (nanoid 3.3.16 → ≥3.3.18, `npm audit fix` resolves); the package-lock changes, so the artifact chain changes — Operator routing required. Correction staged (§4.2).

---

## §3 Checklist reconciliation (DA R1 vs ITRGA runtime assessment)

ITRGA's measurement axis (runtime data presence + end-to-end operability) is finer than the DA R1 axis (code presence in the artifact chain), and per the programme principle *"if an aspect has already been built, it must be presented in the best possible way"* the DA adopts the finer lens. `CAPABILITY_CHECKLIST.md` now carries an R2 addendum with this reconciliation table (column-per-status):

| § | DA R1 | ITRGA | Reconciled R2 (adopted) |
|---|---|---|---|
| 7 Signals | IMPLEMENTED | 🟡 | **SCAFFOLD-BY-DESIGN** — read/drill-down operable; generation absent by design (R3, no model authorization) |
| 8 Intelligence | IMPLEMENTED | 🟡 | **SCAFFOLD-BY-DESIGN** — list/get operable; `create_report` uncalled for the five families by design |
| 9 Research mgmt | IMPLEMENTED | 🟡 | **OPERABLE for operator-authored artifacts** (collections/tags/membership/annotations CRUD verified) — empty of *generated* artifacts by design |
| 10 Artifact explorer | IMPLEMENTED | 🟡 | **OPERABLE** (10 sources read) — rows empty by design |
| 11 Investigation | IMPLEMENTED | 🟡 | **OPERABLE** (planning/journal/execution continuity) — signal-dependent stages empty by design |
| 12 Scenarios | IMPLEMENTED | 🟡 | **SCAFFOLD-BY-DESIGN** — read-only by T-1/R3 |
| 13 Portfolio | PARTIAL | 🟡 | **PARTIAL** (unchanged) — hypothetical research descriptors; live venue records governed-absent |
| 14 Risk | IMPLEMENTED | 🟡 | **SCAFFOLD-BY-DESIGN** — read seams operable; report generation absent by design |
| 15 Alerts | IMPLEMENTED | 🟡 | **IMPLEMENTED (partial-operable)** — list/detail/acknowledge operable; auto-trigger generation absent by design |
| 17 Lineage | IMPLEMENTED | 🟡 | **OPERABLE** (lineage columns + tree over operator-authored artifacts) — empty of generated artifacts by design |
| 20 Assistant | IMPLEMENTED | 🔴 | **NOT IMPLEMENTED as an operable assistant** — audited record viewer only; no request path (UI-008 read-only scope). Engine exists, tested, not exposed |
| 21 Refusals | IMPLEMENTED | 🟡 | **IMPLEMENTED (engine)** — policy + persistence + tests; unreachable from UI because no request path |
| 23 AI auditability | IMPLEMENTED | 🟡 | **IMPLEMENTED (record viewer)** — empty pending generated responses |
| 33 Performance | PARTIAL | 🔴 | **PARTIAL** (unchanged) — build/chunk evidence exists; no interaction-latency targets measured; ITRGA's 🔴 is accepted for the latency-target absence |
| 35–37 Convergence | IMPLEMENTED | 🟡 | **OPERABLE as a terminal** — research/intelligence content empty by design |
| 38 Operator workflow | IMPLEMENTED+VERIFIED | 🟡 | **VERIFIED through the analysis stage** — signal/intelligence/assistant stages empty by design |

All other sections: ITRGA 🟢 where the DA said IMPLEMENTED/PARTIAL — no disagreements. Section 32 (accessibility): ITRGA's "one gap: no `<h1>` on `/`" is noted as a new, previously unrecorded product observation — added to the register as a carried observation (§5.3).

---

## §4 Staged corrections (awaiting Operator routing — NOT executed)

### §4.1 FIND-5 — simulated-clock cap (defect-class fix, designed)

**Scope:** `backend/app/market/adapters/simulated.py` only (+ fail-first tests). No schema, no endpoint, no frontend change.

**Design (the honest semantics):** the simulated feed may run accelerated **while its clock is behind wall time** (startup catch-up, demo liveliness preserved), but a bar whose `open_time` would exceed wall-clock UTC is **not emitted until real time reaches it** — the simulated clock may never point into the future. Concretely: compute `candidate = self._start_time + timedelta(minutes=self._seq)`; if `candidate > now_utc`, hold the sequence (emit nothing, keep the task alive) until `now_utc` catches up, then emit with `open_time = now_utc`-aligned minute. Net effect: after catch-up, one M1 bar per real minute; never a future-dated timestamp. Provenance labels (`LIVE:SIMULATED`) are untouched; no new labels are invented.

**Proof plan (fail-first):** a new backend test asserting (a) after N accelerated ticks the latest emitted `open_time` ≤ wall-clock now; (b) the feed continues emitting after a held period once wall time advances. Existing feed tests must remain green unchanged.

### §4.2 FIND-6 — nanoid HIGH (dependency-hygiene correction, designed)

**Scope:** `frontend/package.json` + `frontend/package-lock.json` (transitive bump nanoid 3.3.16 → ≥3.3.18 via `npm audit fix` or an `overrides` entry pinning the postcss→nanoid sub-tree). No application code changes.

**Proof plan:** post-bump `npm audit --audit-level=high` exit 0 (the project's own remediation standard), full frontend suite 860/860, backend 476/476 (unchanged, sanity), `tsc -b` exit 0, production build reproduced.

Both corrections are **staged as designs only**; per post-closure practice the DA executes them on Operator directive and registers them as `TD-UI-POSTCLOSURE-*` rows, "not ITRGA-reviewed; routed at the Operator's discretion" — or, at the Operator's choice, they can be routed to ITRGA first as proposed corrections.

---

## §5 Record updates performed this session (workspace records only; no artifact-chain changes)

1. **Ingested** `CAPABILITY_ASSESSMENT.md` → `docs/build-orders/CAPABILITY_ASSESSMENT.md`, sha256 `979f815ff1a2f8ca5310918e1060084bfdc19725f68f7af8468af51cb56cfa72` (byte-identical to the upload).
2. **Suites re-run fresh** (addresses the assessment's Honest Limitations §1): 476 BE / 860 FE; logs `docs/evidence/uiconv/pytest_capassess_r1.log`, `docs/evidence/uiconv/vitest_capassess_r1.log`. The "162 suites / 736 tests" figure cited from `PROJECT_STATE.md` is a baseline document, not the DA's record; the DA's verified record is 476/860 and stands re-proven this session.
3. **Register rows added** (`docs/governance/TECHNICAL_DEBT_REGISTER.md`):
   - `TD-UI-CAPASSESS-GENERATION-WIRING` — FIND-1..4 consolidated: signals inference, five intelligence families, assistant ask-path, ML platform — all by design under R3/T-4/T-5/W0-U01; no code change without a Build Order.
   - `TD-UI-CAPASSESS-SIMCLOCK` — FIND-5 defect class; correction staged per §4.1; awaiting Operator routing.
   - `TD-UI-CAPASSESS-NANOID-HIGH` — FIND-6 new HIGH (GHSA-2v37-7h3g-55p8); correction staged per §4.2; breaches the high-audit gate until remediated.
   - `OBS-CAPASSESS-H1` — carried observation: no `<h1>` on `/` (ITRGA matrix row 32).
   - React-router moderates: existing row `TD-UI-REACTROUTER-MODERATE` already covers them; no duplicate row created.
4. **`CAPABILITY_CHECKLIST.md`** — R2 addendum appended carrying the reconciliation table (§3). The R1 content is preserved verbatim as the delivered record; R2 does not rewrite it.

---

## §6 Deviations and standing disclosures

1. **No patch artifacts transmitted** with this response (OBS-DELIVERY-PROCESS compliance: nothing declared that does not exist on disk — there is nothing to declare; two corrections are staged as designs).
2. **Standing riders, restated:** post-closure patches `postclosure_hotfix.patch` and `postclosure_brand.patch` remain applied-but-not-ITRGA-reviewed; `OBS-SURF3-1` remains the sole open programme finding (non-blocking; Operator/ITRGA ruling required on the untransmitted PNG); the repository has no commits, pushes, or pulls — the working tree and the 18-element patch chain are the record.
3. **Rate refinement disclosed:** the DA measured FIND-5's acceleration at ~60× (1.0s default interval), not the assessment's ~30×; the defect class and the correction design are identical either way.
4. **Matrix refinements disclosed:** §9/§10/§17 are operable for operator-authored artifacts (the DA's programme captures and this session's suites prove the write seams); §13/§14 governed-absences were already PARTIAL/disclosed in the DA R1 checklist; §33 latency targets were already PARTIAL in R1.

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
