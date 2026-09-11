# AXIOM — Validation-Tier Separation
## Binding programme rule (BO-B-01 §B-01.1a · BACKEND_ROADMAP_v2.md §B-01.1a)

| Item | Value |
|---|---|
| Instrument | `BO-B-01` §B-01.1a (Operator-authorized 2026-08-19) |
| Status | **BINDING for every downstream ML/report unit** (B-02 → B-07, X-01) |
| Enforcement | `backend/app/ml/dataset/service.py` (tier-aware snapshot freeze) · `backend/app/ml/dataset/market_data_query.py` (`authority_from_source`) · `backend/app/ml/dataset/chronology_guard.py` (source-authority quarantine) |

## R1 — The four tiers

| Tier | Data required | Purpose | Synthetic permitted? |
|---|---|---|---|
| `pipeline_validation` | Any honestly labeled corpus (synthetic permitted) | Prove the pipeline works | **Yes — with the source label persisted end-to-end** |
| `research_validation` | Real historical data (authoritative sources only) | Substantive market conclusions | No |
| `economic_validation` | Real historical + realistic cost assumptions | Economic viability | No |
| `generalization_validation` | Real hold-out data | Cross-market robustness | No |

## R2 — Data-class labeling

Every data-driven output must carry one of the programme-wide source classes:

```
synthetic · simulated · historical real · live · stale/cached · unavailable
```

- The shared classification rule `authority_from_source()` (single source of
  truth, `market_data_query.py`) maps labels to authorities:
  `synthetic` → SYNTHETIC · `seed:synthetic` → SYNTHETIC ·
  `live:simulated` → SIMULATED · `historical:real` → AUTHORITATIVE.
  Unrecognized labels are UNKNOWN and quarantined from authoritative tiers.
- Synthetic/simulated data may prove the pipeline works. It may **not**,
  silently or otherwise, substantiate real-world market or trading conclusions.

## R3 — Enforcement points

1. **Snapshot freeze** (`DatasetService.freeze_from_canonical_records`): the
   snapshot's persisted tier (`source_policy.tier`) decides whether the
   chronology guard runs in authoritative mode. `pipeline_validation` accepts
   labeled synthetic/simulated sources (still rejecting future-dated,
   out-of-order, duplicate, and naive-timestamp records); every higher tier is
   authoritative-only and quarantines synthetic/simulated/unknown sources with
   recorded reasons.
2. **Tier validation** (`create_draft_snapshot`): unknown tiers are rejected;
   the strict research tier is the default, so synthetic acceptance can never
   occur silently.
3. **Ingestion** (`IngestionService`): every successfully ingested series
   persists a `market_series_metadata` row carrying its classified source
   authority.
4. **Features** (`FeatureStore`): feature outputs may never encode
   symbol/provider/market identity (ML Spec §Market-Agnostic Learning).

## R4 — Unit declarations

Every downstream unit's Delivery Report must declare its tier and data class.
A synthetic corpus may close **pipeline-validation** units only. This unit
(BO-B-01) is **pipeline_validation** tier over a labeled `synthetic` corpus.

---

**End of Validation-Tier Separation (BO-B-01 §B-01.1a)**
