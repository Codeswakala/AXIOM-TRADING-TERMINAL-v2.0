# RISK_REGISTER.md

| Version | 3.0.0 |
| Status | Active (Tier 7) |
| Updated | 2026-07-19 (W7-U08) |

| ID | Risk | Severity | Mitigation | Status |
|----|------|----------|------------|--------|
| R-SEC-01 | Weak JWT / default admin in shared env | High | U08 enforce secret + bootstrap policy | Mitigated |
| R-SEC-02 | Refresh token theft / reuse | High | Rotation + reuse family revoke | Mitigated |
| R-SEC-03 | JWT in WS query logs | Medium | Short-lived ticket default; W1-U02 redaction tests/log evidence | Mitigated |
| R-SEC-04 | Secrets/tokens/passwords/DB credentials leaked through logs/metrics | Critical | W1-U02 redaction utility + target log evidence | Mitigated |
| R-DATA-01 | Dual schema create_all vs Alembic | Medium | Auto-create default false; prod forbid | Mitigated |
| R-DATA-02 | Synthetic candles pollute ML | High | W2-U01 source authority + quarantine/exclusion guard | Mitigated pending ITRGA evidence |
| R-DATA-03 | Naive/ambiguous timestamps contaminate future analytics | Medium | W1-U01 strict UTC trusted boundaries + W2-U01 guard | Mitigated |
| R-DATA-04 | Simulated/forward-generated candle chronology mistaken for real market chronology | High | W2-U01 `SIMULATED_FORWARD_DATED` / source authority quarantine | Mitigated pending ITRGA evidence |
| R-ML-01 | Data leakage / look-ahead enters ML datasets | Critical | W2-U01 chronology guard, temporal split and label-horizon negative tests | Mitigated pending ITRGA evidence |
| R-ML-02 | Dataset snapshots are not reproducible | High | W2-U01 immutable frozen snapshots + deterministic content hash | Mitigated pending ITRGA evidence |
| R-ML-03 | Symbol identity leaks into learned features | High | D-W2-001; no symbol identity feature pattern; future W2-U03 enforcement | Controlled |
| R-ML-04 | Label horizon overlaps validation/test window | Critical | W2-U01 `LABEL_HORIZON_LEAKAGE` contract and negative test | Mitigated pending ITRGA evidence |
| R-ML-05 | Dataset package incompatibility on Windows/Python 3.14 | Medium | W2-U01/W2-U02 use existing stdlib/Pydantic/SQLAlchemy stack; future package compatibility spikes | Controlled |
| R-ML-06 | Provider added as new top-level market class | High | W2-U02 canonical market validation; Deriv is provider under Synthetic; tests | Mitigated pending evidence |
| R-ML-07 | Provider-native vocabulary leaks into ML internals | Medium-High | W2-U02 provider adapter isolation + structural tests | Mitigated pending evidence |
| R-ML-08 | Metadata becomes learned symbol identity | High | D-W2-001 structural tests; metadata_role governance_evaluation_only; W2-U03 feature-exclusion test | Mitigated pending evidence |
| R-ML-09 | Feature look-ahead / non-causal feature leakage | Critical | W2-U03 causal feature definitions + peeking-feature negative test | Mitigated pending evidence |
| R-ML-10 | Duplicate or unreproducible feature definitions/records | High | W2-U03 unique feature definitions + deterministic feature hash | Mitigated pending evidence |
| R-ML-11 | Irreproducible dataset snapshots / split manifests | Critical | W2-U04 deterministic snapshot and split hashes; build-twice tests | Mitigated pending evidence |
| R-ML-12 | Random/shuffled split leakage | Critical | W2-U04 temporal-only split engine rejects random/shuffle | Mitigated pending evidence |
| R-ML-13 | Label horizon overlaps validation/test split | Critical | W2-U04 label-horizon + embargo guard rejects leakage | Mitigated pending evidence |
| R-ML-14 | P-hacking / post-hoc experiment rewrite | Critical | W2-U05 pre-registration, approval, plan hash, immutability, audit | Mitigated pending evidence |
| R-ML-15 | Hidden or undocumented experiments | High | W2-U05 rejects incomplete/undocumented experiment plans | Mitigated pending evidence |
| R-ML-16 | Experiment not pinned to reproducible dataset/split | High | W2-U05 requires frozen snapshot hash + split manifest hash | Mitigated |
| R-ML-17 | Model trained outside approved experiment governance | Critical | W2-U06 harness refuses non-approved experiments | Mitigated pending evidence |
| R-ML-18 | Symbol identity reaches model input | Critical | W2-U06 model-input identity guard and tests | Mitigated pending evidence |
| R-ML-19 | Target ML package incompatibility on Windows/Python 3.14 | Medium | W2-U06 pure-Python baseline, no new ML package | Mitigated |
| R-ML-20 | Baseline metric over-interpreted as predictive skill | Medium | Research-only artifact and explicit baseline note; deeper validation deferred | Controlled |
| R-ML-21 | Validation reports point estimates without uncertainty | Critical | W2-U07 uncertainty-mandatory report contract rejects missing CI/bootstrap | Mitigated pending evidence |
| R-ML-22 | Random/non-temporal validation leakage | Critical | W2-U07 random CV refusal and temporal walk-forward folds | Mitigated pending evidence |
| R-ML-23 | P-hacking / metric cherry-picking in validation | High | W2-U07 validates pre-registered plan; no post-hoc metric changes | Controlled |
| R-ML-24 | Poorly calibrated model confidence passes silently | Critical | W2-U08 ECE/Brier/reliability bins and miscalibration warning tests | Mitigated pending evidence |
| R-ML-25 | Base-rate-blind significance flatters majority baseline | High | W2-U08 no-information-rate/base-rate null significance | Mitigated pending evidence |
| R-ML-26 | Statistical success mistaken for economic usability | Critical | W2-U09 reports statistical and economic conclusions independently | Mitigated pending evidence |
| R-ML-27 | False precision in cost assumptions | High | W2-U09 cost provenance and sensitivity ranges required | Mitigated pending evidence |
| R-ML-28 | Economic validation drifts toward execution simulation | Critical | W2-U09 research-only reports; no execution/order/broker paths | Controlled |
| R-ML-29 | Model evaluated outside validated operating domain | High | W2-U10 operating-domain warning guardrail | Mitigated pending evidence |
| R-ML-30 | Drift triggers silent auto-retrain | Critical | W2-U10 drift records never trigger retrain; governance required | Mitigated pending evidence |
| R-ML-31 | Generalization result cherry-picks markets | High | W2-U10 trained-on/evaluated-on report records all holdout results | Mitigated pending evidence |
| R-W3-01 | Ineligible model served advisory inference | Critical | W3-U01 governed eligibility gate and refusal tests | Mitigated |
| R-W3-02 | Ungoverned advisory promotion | Critical | W3-U01 explicit approver/timestamp/audit promotion | Mitigated |
| R-W3-03 | Non-deterministic live inference | High | W3-U01 deterministic input hash/score test | Mitigated |
| R-W3-04 | Premature signal/execution path | Critical | W3-U01/W3-U02 no UI/alert/live stream; no execution grep; broker gate closed | Controlled |
| R-W3-05 | Ineligible or research-only model emits advisory signal | Critical | W3-U02/W3-U03 reuse W3-U01 eligibility gate; ineligible/out-of-domain cases persist as `withheld` with named reasons | Mitigated |
| R-W3-06 | Opaque advisory signal without rationale | High | W3-U02/W3-U03 require rationale for emitted signal; no-rationale candidate persists as `withheld` | Mitigated |
| R-W3-07 | Raw model score presented as confidence | High | W3-U02/W3-U03 store calibrated confidence from W2-U08 calibration bins/base rate; poor calibration becomes `warning` | Mitigated |
| R-W3-08 | Signal record becomes executable order payload | Critical | W3-U02/W3-U03 schema omits order/broker/payload fields; structural no-order-payload test and grep | Controlled |
| R-W3-09 | Advisory signal emitted outside validated operating domain | Critical | W3-U03 emit-time domain guardrail withholds provider/symbol/source/domain violations | Mitigated |
| R-W3-10 | Economically unusable model shown as clean usable signal | High | W3-U03 economic verdict guardrail downgrades to `warning` and preserves verdict | Mitigated |
| R-W3-11 | Stale signal shown as current | High | W3-U03 max input staleness, signal validity/expiry, and `current_only` API filter | Mitigated |
| R-W3-12 | Future live candle leaks into inference input | Critical | W3-U04 as-of query window admits only `open_time <= requested_as_of_time`; future count evidence | Mitigated pending evidence |
| R-W3-13 | Stale live market data scored as current | High | W3-U04 anchors input time to freshest included candle; W3-U03 `STALE_INPUT` guardrail withholds stale live path | Mitigated pending evidence |
| R-W3-14 | Unauthorized external live feed introduced | High | W3-U04 reuses W1 persisted live seam only; no new provider/egress imports; grep/structural proof | Controlled |
| R-W3-15 | Symbol/provider identity enters live model features | High | W3-U04 adapter features are causal numeric fields only; identity remains metadata on `InferenceInput` not learned features | Mitigated pending evidence |
| R-W3-16 | Operator overtrusts advisory signal as instruction | High | W3-U05 visible research-advisory disclaimer, guardrail state visibility, and no action controls | Mitigated |
| R-W3-17 | UI hides warning/withheld/expired guardrail outcome | High | W3-U05 distinct visual state badges and detail copy for warning/withheld/expired/superseded states | Mitigated |
| R-W3-18 | Client computes or alters inference/signal/economic logic | Critical | W3-U05 reads history API only and performs presentation/formatting only; structural test/evidence | Mitigated |
| R-W3-19 | Execution controls appear in first advisory UI | Critical | W3-U05 excludes transaction action controls; test/grep/browser screenshot evidence | Mitigated |
| R-W3-20 | Monitoring alert triggers auto-action/remediation | Critical | W3-U06 alert service persists/audits only; no remediation payload; negative tests prove no model/order side effects | Mitigated |
| R-W3-21 | Drift alert triggers automatic retraining | Critical | W3-U06 drift alert reads W2-U10 drift record and does not change drift/model retraining fields | Mitigated |
| R-W3-22 | Monitoring mutates model or config state | Critical | W3-U06 monitoring service has no model/config mutation path; ack changes alert read-state only | Controlled |
| R-W3-23 | Alert is unpersisted or unaudited | High | W3-U06 alert table and audit events mandatory for creation/ack | Mitigated |
| R-W3-24 | Analytics displayed with false precision | High | W3-U07 backend metrics include uncertainty interval and sample count; UI flags point-estimate-only metrics | Mitigated |
| R-W3-25 | Analytics implies guaranteed future outcome | High | W3-U07 advisory-not-guaranteed disclaimer and tests; no promised outcome wording | Mitigated |
| R-W3-26 | Raw score shown as confidence | High | W3-U07 confidence bands use calibrated confidence only; raw score excluded from analytics payload/UI | Mitigated |
| R-W3-27 | Client recomputes authoritative analytics | High | W3-U07 browser reads backend analytics API; presentation-only grep/tests | Mitigated |
| R-W3-28 | Wave-3 closeout misses an unaudited signal or alert | Critical | W3-U08 no-orphan audit joins for advisory signals and monitoring alerts | Mitigated |
| R-W3-29 | Wave-wide execution path introduced by accumulated surfaces | Critical | W3-U08 wave-wide grep, inert schemas, and gate-closed proof | Mitigated |
| R-W3-30 | Operator alert evidence lacks UI/browser surface | Medium | W3-U08 hardening adds read-only monitoring alert panel to existing Operations dashboard; no action controls | Mitigated with observations |
| R-W4-01 | Unspiked compiled dependency enters application code | High | W4-U01 dependency policy, target spike and import tests; numpy/pandas/scipy approved by ITRGA | Mitigated |
| R-W4-02 | Intelligence artifact carries action/remediation payload | Critical | W4-U01 artifact contract rejects forbidden action/remediation keys; structural tests | Mitigated |
| R-W4-03 | Institutional Intelligence context owns broker/feed/auth responsibilities | High | W4-U01 bounded context reads existing contexts only; structural no-execution tests | Controlled |
| R-W4-04 | Wave-4 artifact lacks uncertainty/lineage | High | W4-U01 mandatory artifact contract fields include uncertainty, sample count, lineage, audit correlation | Mitigated |
| R-W4-05 | Future candle leaks into correlation report | Critical | W4-U02 as-of-bounded query excludes `open_time > as_of_end`; named negative test | Mitigated |
| R-W4-06 | Correlation displayed as signal or causation | High | W4-U02 inert artifact limitations, no signal side-effect test, no UI in unit | Mitigated |
| R-W4-07 | Correlation point estimate without uncertainty | High | W4-U02 Fisher interval and sample count mandatory; tests | Mitigated |
| R-W4-08 | Correlation report persisted without audit | High | W4-U02 creates audit event and no-orphan proof accepted by ITRGA | Mitigated |
| R-W4-09 | Future candle leaks into regime report | Critical | W4-U03 as-of-bounded backward-looking query excludes `open_time > as_of_end`; named negative test | Mitigated |
| R-W4-10 | Regime label becomes signal or instruction | High | W4-U03 inert artifact, no signal side-effect test, research-only limitations | Mitigated pending evidence |
| R-W4-11 | Symbol identity influences regime classification | High | W4-U03 normalized features exclude symbol identity; same normalized inputs yield same regime across symbols | Mitigated |
| R-W4-12 | Regime report persists without audit | High | W4-U03 audit event and no-orphan proof required in evidence pack | Mitigated |
| R-W4-13 | Scenario treated as trade instruction or sizing directive | Critical | W4-U04 hypothetical labels, inert schema, no order/sizing fields, no side-effect tests | Mitigated |
| R-W4-14 | Future candle leaks into scenario baseline | Critical | W4-U04 as-of-bounded query excludes `open_time > as_of_end`; named negative test | Mitigated |
| R-W4-15 | Scenario result lacks uncertainty or assumptions | High | W4-U04 stores assumptions, inputs, uncertainty, and sample count; tests | Mitigated |
| R-W4-16 | Scenario report persists without audit | High | W4-U04 audit event and no-orphan proof required in evidence pack | Mitigated |
| R-W4-17 | Portfolio/risk report links to real account, broker, or position | Critical | W4-U05 schema/tests/grep prove market-series only and no account/broker/position linkage | Mitigated |
| R-W4-18 | Portfolio/risk metrics imply guaranteed returns | High | W4-U05 hypothetical/not-guaranteed limitations and tests | Mitigated |
| R-W4-19 | Risk metric lacks uncertainty/sample count | High | W4-U05 per-metric uncertainty and sample count; tests | Mitigated |
| R-W4-20 | Portfolio/risk report persists without audit | High | W4-U05 audit event and no-orphan proof accepted by ITRGA | Mitigated |
| R-W4-21 | Signal validation cherry-picks flattering scope | Critical | W4-U06 declared scope stored; full matching signal set included; deterministic tests | Mitigated |
| R-W4-22 | Raw model score appears in signal validation output | High | W4-U06 raw score excluded downstream despite source signals containing raw_score | Mitigated |
| R-W4-23 | Signal validation fabricates realized outcomes | Critical | W4-U06 outcome_data_status reports governed outcomes unavailable; no realized performance fabricated | Mitigated |
| R-W4-24 | Signal validation report persists without audit | High | W4-U06 audit event and no-orphan proof accepted by ITRGA | Mitigated |
| R-W4-25 | Institutional dashboard adds execution controls | Critical | W4-U07 UI tests, grep, and browser evidence require no execution/order/broker controls | Mitigated with observation closure pending |
| R-W4-26 | Institutional dashboard recomputes analytics client-side | High | W4-U07 reads existing APIs and formats only; presentation-only grep/tests | Mitigated |
| R-W4-27 | Institutional dashboard hides uncertainty/sample count | High | W4-U08 fixes interval-bound rendering and evidence pack requires browser proof | Mitigated pending closeout evidence |
| R-W4-28 | Raw score appears on dashboard | High | W4-U07 sanitizes uncalibrated raw-score key and tests absence | Mitigated |
| R-W4-29 | Wave-4 closeout misses an unaudited report | Critical | W4-U08 evidence requires no-orphan audit proof across all five W4 report tables | Mitigated pending closeout evidence |
| R-W4-30 | Wave-wide account/broker/position/execution path introduced by accumulated W4 surfaces | Critical | W4-U08 wave-wide grep, inert schemas, and gate-closed proof | Controlled pending closeout evidence |
| R-W5-01 | Assistant prompt-injected into action | Critical | W5-U01 no action tools by registry, injection refusal tests, audited refusals; W5-U02 re-runs and persists refusals | Mitigated |
| R-W5-02 | Assistant leaks secrets or tokens | Critical | W5-U01 secret-exfiltration refusal and sampled output marker test; W5-U02 persists refusals without secret markers | Mitigated |
| R-W5-03 | Assistant emits ungrounded claims | High | W5-U01 grounding-or-refuse policy and test; W5-U02 persists ungrounded requests only as `GROUNDING_REQUIRED` refusals | Mitigated |
| R-W5-04 | Trade plan or journal becomes order ticket | Critical | W5-U01 inert contracts reject order/sizing/account fields; no persistence/execution path | Mitigated |
| R-W5-05 | External LLM introduced before safety gate | High | W5-U01/W5-U02 use deterministic local assistant only; grep proves no LLM imports | Controlled |
| R-W5-06 | Assistant response persisted without audit | High | W5-U02 repository writes response row and audit event in one transaction; no-orphan audit join required | Mitigated pending evidence |
| R-W5-07 | Raw request text or secrets stored in assistant memory | Critical | W5-U02 schema stores `request_text_hash` only, has no raw prompt/request column, and tests sampled secret-marker exclusion | Mitigated pending evidence |
| R-W5-08 | Assistant response API becomes mutation or action surface | Critical | W5-U02 exposes authenticated GET list/detail only; POST returns 405/404; no action endpoint/tool | Controlled |
| R-W5-09 | Chart annotation becomes order ticket or execution instruction | Critical | W5-U03 inert schema and recursive forbidden-field rejection block order/sizing/account/execution/position/signal payloads | Mitigated pending browser/DB evidence |
| R-W5-10 | Chart annotation UI hides disclaimer or shows execution controls | Critical | W5-U03 chart UI displays research/not-instruction disclaimer; browser screenshots and UI tests required; no execution controls added | Mitigated pending browser evidence |
| R-W5-11 | Chart annotation persists without audit | High | W5-U03 repository writes annotation plus `chart_research_annotation.created` audit event in one transaction; no-orphan join required | Mitigated pending evidence |
| R-W5-12 | Browser recomputes authoritative inference/analytics or renders raw score/guarantee | High | W5-U03 UI renders persisted annotation fields only; raw-score/guarantee display tests added | Controlled |
| R-W5-13 | Signal investigation mutates/re-emits/re-grades an advisory signal | Critical | W5-U04 uses existing read-only APIs; named triggers-nothing test verifies signal/model rows unchanged after investigation reads | Mitigated pending browser/target evidence |
| R-W5-14 | Signal investigation UI displays raw model score or hides research framing | High | W5-U04 displays calibrated confidence only, tests absence of raw score, and requires browser screenshot of research framing | Mitigated pending browser evidence |
| R-W5-15 | Signal investigation becomes execution/action surface | Critical | W5-U04 adds no signal write/action endpoint and UI tests prove no action controls | Controlled |
| R-W5-16 | Scenario comparison generates new scenarios or hypothetical outcomes | Critical | W5-U05 uses existing read-only scenario APIs only; named test proves scenario row count unchanged after reads | Mitigated pending browser/target evidence |
| R-W5-17 | Scenario comparison hides uncertainty/provenance or implies guarantee | High | W5-U05 displays uncertainty/source ids/limitations and tests hypothetical/not-guaranteed framing | Mitigated pending browser evidence |
| R-W5-18 | Scenario comparison becomes action or execution surface | Critical | W5-U05 adds no scenario write/action endpoint and UI tests prove no action controls | Controlled |
| R-W5-19 | Trade plan note becomes order ticket | Critical | W5-U06 inert schema omits order/sizing/account/execution fields and factory rejects forbidden fields recursively | Mitigated pending browser/DB evidence |
| R-W5-20 | Trade planning UI displays order-ticket controls | Critical | W5-U06 frontend tests and browser evidence require no buy/sell/quantity/SL/TP/position/execute controls | Mitigated pending browser evidence |
| R-W5-21 | Trade plan note triggers execution/signal side effects | Critical | W5-U06 triggers-nothing and not-read-by-execution-path tests added; no execute/submit/signal endpoint | Controlled |
| R-W5-22 | Manual journal becomes broker/account/execution record | Critical | W5-U07 inert schema omits broker/account/execution/fill/P&L fields and factory rejects them recursively | Mitigated pending browser/DB evidence |
| R-W5-23 | Manual journal UI displays broker-import/account/execution/P&L controls | Critical | W5-U07 frontend tests and browser evidence require no such fields/controls | Mitigated pending browser evidence |
| R-W5-24 | Journal entry triggers execution/signal side effects | Critical | W5-U07 triggers-nothing and not-read-by-execution-path tests added; no execute/submit/signal endpoint | Controlled |
| R-W5-25 | Wave-5 accumulated surfaces introduce hidden actuation path | Critical | W5-U08 full-wave grep, inert schema proof, Gate CLOSED proof, broker tests, and auth/action endpoint checks required | Mitigated pending closeout evidence |
| R-W5-26 | Assistant prompt injection bypasses safety after surface accumulation | Critical | W5-U08 assistant prompt-injection proof index maps refusal classes to named tests and audited reason codes | Mitigated pending closeout evidence |
| R-W5-27 | Wave-5 artifact persists without audit | High | W5-U08 no-orphan audit joins required across all Wave-5 collaboration tables | Mitigated |
| R-W6-01 | Constitutional Governance Gate opens during Execution Research | Critical | W6-U01 and every W6 unit must prove Gate CLOSED; broker refusal tests remain mandatory | Controlled pending W6-U01 evidence |
| R-W6-02 | Live broker SDK/credentials or venue path enters code | Critical | W6-U01 dependency/containment tests and greps prove no broker SDK, credentials, or live endpoint | Controlled pending W6-U01 evidence |
| R-W6-03 | Closed-Gate broker refusals are unaudited | High | W6-U01 writes refusal rows to `audit_events.details->>'reason_code'` and requires raw GROUP BY evidence | Mitigated pending W6-U01 evidence |
| R-W6-04 | Execution Research context contains live execution path | Critical | W6-U01 `execution_research` bright-line grep and tests require no live execution/account path | Controlled |
| R-W6-05 | Simulated execution artifacts are mistaken for live orders/fills | Critical | W6-U02 stores `simulation_mode=SIMULATED`, research status, disclaimer, and tests no live-fill/real-P&L framing | Mitigated pending evidence |
| R-W6-06 | Simulated run operator attribution becomes broker/account linkage | Critical | W6-U02 `operator_id` FKs to `operators.id`; no broker/account forbidden columns; no-orphan operator join required | Mitigated pending evidence |
| R-W6-07 | Fill model is nondeterministic or silently rewrites versions | High | W6-U02 deterministic test and immutable policy/fill-model version fields/audit evidence required | Mitigated pending evidence |
| R-W6-08 | Simulated run/fill artifacts persist without audit | High | W6-U02 no-orphan audit joins required for both tables | Mitigated |
| R-W6-09 | Simulated ledger return estimate is mistaken for real P&L | Critical | W6-U03 uses simulated-return estimate with uncertainty, SIMULATED disclaimer, and no-real-P&L tests | Mitigated pending evidence |
| R-W6-10 | Simulated ledger links to real account/broker/position | Critical | W6-U03 schema forbids account/broker/position columns and references simulated run/fill artifacts only | Mitigated pending evidence |
| R-W6-11 | Simulated ledger persists without audit or lineage | High | W6-U03 no-orphan audit/operator/run/fill joins required | Mitigated |
| R-W6-12 | Execution risk report actuates sizing or action | Critical | W6-U04 report service writes report only, contains no sizing columns, and triggers-nothing test required | Mitigated pending evidence |
| R-W6-13 | Execution risk report links to real account/capital/margin | Critical | W6-U04 forbidden-column proof includes account/capital/margin/sizing fields | Mitigated pending evidence |
| R-W6-14 | Execution risk metrics are presented as economic success | High | W6-U04 separates `risk_metrics` from `economic_usefulness` and requires uncertainty/limitations/no-guarantee tests | Mitigated |
| R-W6-15 | Trade replay leaks future data into experiments | Critical | W6-U05 stores as-of bounded lineage and tests future-row exclusion with negative check | Mitigated pending evidence |
| R-W6-16 | Execution experiment scope is cherry-picked post hoc | Critical | W6-U05 immutable plan hash and scope equality tests prevent silent narrowing | Mitigated pending evidence |
| R-W6-17 | Experiment replay uses live feed/broker path | Critical | W6-U05 no-live-feed/broker/Gate grep and tests require frozen inputs only | Controlled |
| R-W6-18 | Simulated analytics cherry-picks favorable subset | Critical | W6-U06 persists declared/analyzed scope and tests exact full-scope equality | Mitigated pending evidence |
| R-W6-19 | Simulated analytics presents statistics as economic success | High | W6-U06 separates structured metrics from economic usefulness and uses not_assessed verdict | Mitigated pending evidence |
| R-W6-20 | Simulated analytics lacks uncertainty or sample count | High | W6-U06 requires per-metric uncertainty or insufficient-sample limitation plus sample_count | Mitigated |
| R-W6-21 | Execution Research UI exposes actuation controls | Critical | W6-U07 frontend tests and browser evidence require no buy/sell/submit/execute/go-live/connect-broker/account controls | Mitigated pending browser evidence |
| R-W6-22 | Execution Research UI recomputes authoritative analytics client-side | High | W6-U07 displays server-persisted artifacts only and states no browser authoritative recomputation | Controlled |
| R-W6-23 | Wave-6 accumulated surfaces introduce hidden live execution path | Critical | W6-U08 whole-wave bright-line grep, broker containment test, Gate-CLOSED proof, and browser E2E required | Mitigated pending closeout evidence |
| R-W6-24 | Wave-6 simulated artifacts persist without audit | High | W6-U08 no-orphan audit joins required across all six W6 tables | Mitigated pending closeout evidence |
| R-W6-25 | W6 UI or artifacts are presented as live/real P&L | Critical | W6-U08 SIMULATED-everywhere proof and browser E2E accepted by ITRGA | Mitigated |
| R-W7-01 | Institutional platform API/plugin surface exposes execution or broker path | Critical | Wave-7 design guardrails require Gate CLOSED, plugin/API containment, no execution endpoints, and default-deny tests | Controlled pending design review |
| R-W7-02 | Multi-user readiness leaks cross-operator data | Critical | Wave-7 design requires two-operator isolation tests and scoped APIs | Controlled pending design review |
| R-W7-03 | Plugin architecture bypasses audit or imports broker/order/account logic | Critical | Wave-7 design requires sandboxed contracts and hostile-plugin refusal tests | Controlled pending future plugin unit |
| R-W7-04 | Institutional API exposes unauthenticated or execution/order/broker/account endpoint | Critical | W7-U01 route inventory, auth tests, and absent endpoint checks prove security foundation | Mitigated pending evidence |
| R-W7-05 | RBAC grants Gate/execution/order/account capability | Critical | W7-U01 default-deny RBAC vocabulary excludes forbidden capabilities | Mitigated pending evidence |
| R-W7-06 | Cross-operator institutional data leakage | Critical | W7-U01 two-real-operator isolation tests and evidence pack require 0 leakage | Mitigated |
| R-W7-07 | Workspace preferences expose action/order/account configuration | Critical | W7-U02 schema and recursive validation reject forbidden fields; UI tests/grep prove no actuation controls | Mitigated pending evidence |
| R-W7-08 | Workspace preference config stores secrets or PII | High | W7-U02 recursive marker rejection and persisted/API payload checks required | Mitigated pending evidence |
| R-W7-09 | Workspace preferences leak across operators | Critical | W7-U02 operator-scoped API and two-operator isolation evidence required | Mitigated pending evidence |
| R-W7-10 | Research management mutates source artifacts or source audits | Critical | W7-U03 source before/after hash and source-audit count proof accepted by ITRGA | Mitigated |
| R-W7-11 | Research management collections/tags leak across operators | Critical | W7-U03 valid-token two-operator isolation and raw 0-leakage proof accepted by ITRGA | Mitigated |
| R-W7-12 | API catalogue exposes execution/order/broker/account/open-gate route | Critical | W7-U04 generated catalogue asserts no actuation/Gate capability; forbidden route probes and tests prove 404/405 | Mitigated pending evidence |
| R-W7-13 | API catalogue leaks secrets/PII in route metadata | High | W7-U04 response marker tests and evidence pack require clean catalogue/API response grep | Mitigated pending evidence |
| R-W7-14 | Catalogued routes expose unauthenticated research data | Critical | W7-U04 auth-gating tests and operator evidence require unauth 401 on catalogue/representative catalogued routes | Mitigated pending evidence |
| R-W7-15 | Plugin contract layer introduces dynamic or third-party code execution | Critical | W7-U05 code-defined contracts/refusal only; no dynamic loader/runtime; grep/tests require no eval/exec/importlib/entry-point/subprocess path | Mitigated pending evidence |
| R-W7-16 | Plugin contract bypass reaches broker/order/account/live/Gate path | Critical | W7-U05 §16/§17 containment grep/tests and hostile refusal/audit proof | Mitigated pending evidence |
| R-W7-17 | Hostile plugin request is not refused or not audited | Critical | W7-U05 hostile request refusal seam writes existing audit_events row with reason code; raw audit evidence required | Mitigated pending evidence |
| R-W7-18 | Plugin contract surface leaks secrets/PII | Critical | W7-U05 contract surface marker tests and evidence pack require clean response grep | Mitigated pending evidence |
| R-W7-19 | Portfolio research dashboard is mistaken for real account or P&L view | Critical | W7-U06 forbids real account/P&L fields and labels; UI/API tests and browser evidence require hypothetical research framing | Mitigated pending evidence |
| R-W7-20 | Portfolio report presents statistical descriptors as economic success | High | W7-U06 requires uncertainty, sample_count, limitations, and separate `economic_usefulness=not_assessed` | Mitigated pending evidence |
| R-W7-21 | Portfolio/report scope cherry-picks favorable artifacts | High | W7-U06 generated reports include full current-operator source scope and deterministic report hash | Mitigated pending evidence |
| R-W7-22 | Portfolio dashboard leaks cross-operator research artifacts | Critical | W7-U06 valid-token two-operator scoping proof requires B sees 0 of A's source ids | Mitigated pending evidence |
| R-W7-23 | Enterprise hardening weakens default-deny RBAC or auth | Critical | W7-U07 re-proves unprivileged 403, auth isolation, and permission vocabulary safety | Mitigated pending evidence |
| R-W7-24 | Historical admin/admin123 accepted in production framing | Critical | W7-U07 proves default bootstrap credential rejected when insecure-dev flag is off | Mitigated pending evidence |
| R-W7-25 | Observability/logging leaks secrets under scalability hardening | Critical | W7-U07 redaction/log marker tests and evidence pack require clean output | Mitigated pending evidence |
| R-W7-26 | Rate/abuse guard silently omitted | Medium | W7-U07 formally defers under TD-W7-U07-RATE-GUARD with rationale | Controlled |
| R-W7-27 | Wave-7 accumulated surfaces introduce hidden execution/Gate path | Critical | W7-U08 whole-wave bright-line grep, broker containment, Gate-CLOSED proof, and browser E2E required | Mitigated pending closeout evidence |
| R-W7-28 | W7 closeout misses orphaned institutional artifacts | Critical | W7-U08 four-table row count and no-orphan audit joins required | Mitigated pending closeout evidence |
| R-W7-29 | Whole-project milestone declared without reconciling prior milestones | High | W7-U08 milestone reconciliation accepted by ITRGA final closeout; DA did not self-declare milestone | Mitigated |
| R-PROD-02 | Roadmap completion mistaken for production deployment certification | Critical | `11_PRODUCTION_READINESS_CERTIFICATION.md` governs final production certification; deployment not approved until ITRGA certification outcome | Controlled |
| R-OPS-01 | Manual-only regression detection | Medium | CI workflow + local CI equivalent; W6/W7 closeouts record CI exit 0 | Mitigated |
| R-OPS-02 | Runtime failures hard to diagnose | Medium | W1-U02 correlation IDs, structured logs, metrics, exception diagnostics | Mitigated |
| R-PROD-01 | Live broker / execution premature | Critical | Roadmap gate Wave 6; W1-U03 gate closed | Controlled |
| R-BROKER-01 | Future broker connection/execution accidentally enabled before governance authorization | Critical | W1-U03 hard-closed Constitutional Governance Gate + NullBroker + tests | Mitigated |
| R-BROKER-02 | Broker-specific vocabulary leaks into inner subsystems | High | External Integration bounded context + structural containment test | Mitigated |
| R-BROKER-03 | Broker credentials introduced or logged prematurely | High | No credential config/models; no broker I/O; grep evidence required | Controlled |
| R-UI-01 | Incomplete browser evidence | Low | Operator capture checklist | Open residual |
| R-API-01 | Operational endpoint data exposure | Medium | W1-U01 endpoint inventory + shared Bearer auth | Mitigated |
| R-CI-01 | Remote GitHub CI run not observed in DA sandbox | Low | W1-U02/W1-U04 CI gate + local equivalent; close when remote run attached | Open residual |
| R-FE-01 | Frontend toolchain npm audit reports critical/high transitive vulnerabilities | High | W1-U04 Vite/Vitest/plugin upgrade; npm audit 0 vulnerabilities | Mitigated |

---

**End**
