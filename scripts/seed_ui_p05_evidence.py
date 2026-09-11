"""Seed script for UI-NEW-P05 Level I served evidence data."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from sqlalchemy import delete
from app.db.session import close_db, create_schema, init_db, session_scope
from app.db.models.model_artifact import ModelArtifact
from app.db.models.candle import Candle
from app.db.models.advisory_signal import AdvisorySignal
from app.db.models.signal_validation_report import SignalValidationReport
from app.db.models.correlation_report import CorrelationReport
from app.db.models.regime_report import RegimeReport
from app.db.models.trade_plan_note import TradePlanNoteRecord
from app.db.models.manual_trade_journal_entry import ManualTradeJournalEntryRecord
from app.db.models.portfolio_risk_report import PortfolioRiskReport
from app.db.models.scenario_report import ScenarioReport


async def seed_data() -> None:
    init_db()
    await create_schema()
    async with session_scope() as session:
        # 1. Clear stale synthetic candles and previous records
        await session.execute(delete(Candle).where(Candle.source == "seed:synthetic"))
        await session.execute(delete(AdvisorySignal))
        await session.execute(delete(SignalValidationReport))
        await session.execute(delete(CorrelationReport))
        await session.execute(delete(RegimeReport))
        await session.execute(delete(TradePlanNoteRecord))
        await session.execute(delete(ManualTradeJournalEntryRecord))
        await session.execute(delete(PortfolioRiskReport))
        await session.execute(delete(ScenarioReport))
        await session.execute(delete(ModelArtifact))

        # 2. Seed Model Artifact
        artifact = ModelArtifact(
            id="model.eurusd.classifier",
            name="EURUSD Multi-Timeframe Classifier",
            version="1.4.2",
            status="approved",
            framework="xgboost",
            feature_set_version="feat.m1.v2",
            supported_markets=["forex:EURUSD"],
            metrics={"accuracy": 0.68, "f1": 0.66, "brier_score": 0.118, "ece": 0.042},
            notes="Governed classifier for EUR/USD advisory signals.",
            experiment_id="exp-001",
        )
        session.add(artifact)
        await session.flush()

        # 3. Seed Non-degenerate Candles for EURUSD and BTCUSD
        rng = random.Random(42)
        bars = 80
        now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        start = now - timedelta(minutes=bars)

        # EURUSD Candles
        price = Decimal("1.10250")
        eurusd_candles: list[Candle] = []
        for i in range(bars):
            open_time = start + timedelta(minutes=i)
            step = Decimal(str(round(rng.gauss(0.00004, 0.00015), 5)))
            open_ = price
            close = (open_ + step).quantize(Decimal("0.00001"))
            high_wick = Decimal(str(round(abs(rng.gauss(0.00008, 0.00004)), 5)))
            low_wick = Decimal(str(round(abs(rng.gauss(0.00008, 0.00004)), 5)))
            high = (max(open_, close) + high_wick).quantize(Decimal("0.00001"))
            low = (min(open_, close) - low_wick).quantize(Decimal("0.00001"))
            volume = Decimal(str(int(150000 + abs(rng.gauss(40000, 20000)))))

            eurusd_candles.append(
                Candle(
                    market_class="forex",
                    symbol="EURUSD",
                    timeframe="M1",
                    open_time=open_time,
                    open=open_,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    source="seed:synthetic",
                )
            )
            price = close
        session.add_all(eurusd_candles)

        # BTCUSD Candles
        price_btc = Decimal("42500.00")
        btc_candles: list[Candle] = []
        for i in range(bars):
            open_time = start + timedelta(minutes=i)
            step = Decimal(str(round(rng.gauss(10.0, 45.0), 2)))
            open_ = price_btc
            close = (open_ + step).quantize(Decimal("0.01"))
            high_wick = Decimal(str(round(abs(rng.gauss(15.0, 25.0)), 2)))
            low_wick = Decimal(str(round(abs(rng.gauss(15.0, 25.0)), 2)))
            high = (max(open_, close) + high_wick).quantize(Decimal("0.01"))
            low = (min(open_, close) - low_wick).quantize(Decimal("0.01"))
            volume = Decimal(str(int(1200 + abs(rng.gauss(500, 250)))))

            btc_candles.append(
                Candle(
                    market_class="crypto",
                    symbol="BTCUSD",
                    timeframe="M1",
                    open_time=open_time,
                    open=open_,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    source="seed:synthetic",
                )
            )
            price_btc = close
        session.add_all(btc_candles)
        await session.flush()

        # 4. Seed Signal Validation Report
        val_report = SignalValidationReport(
            id="val-001",
            created_at=now - timedelta(hours=1),
            artifact_type="signal_validation_report",
            method_version="w4-u06.signal_validation.v1",
            scope_start=now - timedelta(days=7),
            scope_end=now,
            sample_count=520,
            metrics={
                "clean_advisory_rate": {
                    "value": 0.824,
                    "sample_count": 520,
                    "uncertainty": {
                        "method": "wilson_score_interval",
                        "lower": 0.789,
                        "upper": 0.854,
                        "confidence_level": 0.95,
                        "sample_count": 520,
                    },
                },
                "guardrail_intervention_rate": {
                    "value": 0.176,
                    "sample_count": 520,
                    "uncertainty": {
                        "method": "wilson_score_interval",
                        "lower": 0.146,
                        "upper": 0.211,
                        "confidence_level": 0.95,
                        "sample_count": 520,
                    },
                },
                "calibrated_confidence_coverage": {
                    "value": 0.784,
                    "sample_count": 520,
                    "uncertainty": {
                        "method": "wilson_score_interval",
                        "lower": 0.724,
                        "upper": 0.841,
                        "confidence_level": 0.95,
                        "sample_count": 520,
                    },
                },
            },
            uncertainty={
                "method": "wilson_score_interval",
                "lower": 0.724,
                "upper": 0.841,
                "confidence_level": 0.95,
                "sample_count": 520,
            },
            validation_scope={
                "market_class": "forex",
                "symbol": "EURUSD",
                "timeframe": "M1",
                "include_states": ["emitted", "warning", "withheld", "expired"],
            },
            outcome_data_status={
                "status": "not_available",
                "reason": "Governed forward outcome labels are not present in W4-U06.",
            },
            economic_usefulness={
                "verdict": "not_assessed",
                "reason": "Signal quality validation is research context.",
            },
            config={"scope": {"market_class": "forex", "symbol": "EURUSD"}},
            input_lineage={"source": "advisory_signals", "uncalibrated_model_score_excluded": True},
            source_signal_ids=["sig-001", "sig-002", "sig-003"],
            market_scope={"market_class": "forex", "symbol": "EURUSD", "timeframe": "M1"},
            results={},
            limitations=["historical_research_only", "not_a_guarantee", "uncalibrated_model_score_excluded"],
            report_hash="val-hash-01",
            research_status="research_only",
            created_by="operator",
            audit_correlation_id="audit-val-001",
            notes="Historical advisory signal validation report.",
        )
        session.add(val_report)
        await session.flush()

        # 5. Seed Correlation Report
        corr_report = CorrelationReport(
            id="corr-001",
            created_at=now - timedelta(hours=1),
            artifact_type="correlation_report",
            method_version="w4-u02.correlation.v1",
            left_market_class="forex",
            left_symbol="EURUSD",
            right_market_class="forex",
            right_symbol="USDCHF",
            timeframe="M1",
            as_of_start=now - timedelta(days=1),
            as_of_end=now,
            sample_count=1440,
            correlation_value=-0.742,
            uncertainty={
                "method": "fisher_z_confidence_interval",
                "lower": -0.815,
                "upper": -0.652,
                "confidence_level": 0.95,
            },
            significance={"p_value": 0.0001},
            economic_usefulness={"verdict": "not_assessed"},
            config={},
            input_lineage={},
            source_artifact_ids=[],
            market_scope={"left_symbol": "EURUSD", "right_symbol": "USDCHF"},
            results={},
            limitations=["historical_research_only"],
            report_hash="corr-hash-01",
            research_status="research_only",
            created_by="operator",
            audit_correlation_id="audit-corr-001",
            notes="EURUSD vs USDCHF correlation analysis.",
        )
        session.add(corr_report)

        # 6. Seed Regime Report
        reg_report = RegimeReport(
            id="reg-001",
            created_at=now - timedelta(hours=1),
            artifact_type="regime_report",
            method_version="w4-u03.regime.v1",
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            as_of_start=now - timedelta(days=1),
            as_of_end=now,
            sample_count=500,
            regime_label="TRENDING_BULLISH",
            confidence=0.845,
            uncertainty={
                "method": "posterior_interval",
                "lower": 0.782,
                "upper": 0.908,
            },
            evidence={"adx_14": 28.4, "atr_ratio": 1.15},
            economic_meaning={"regime": "trending_bullish"},
            config={},
            input_lineage={},
            source_artifact_ids=[],
            market_scope={"symbol": "EURUSD"},
            results={},
            limitations=["historical_research_only"],
            report_hash="reg-hash-01",
            research_status="research_only",
            created_by="operator",
            audit_correlation_id="audit-reg-001",
            notes="EURUSD M1 regime detection report.",
        )
        session.add(reg_report)
        await session.flush()

        # 7. Seed Advisory Signals for EURUSD
        # Signal 1: Emitted (With Wilson Bounds via val-001, bracketed)
        sig1 = AdvisorySignal(
            signal_id="sig-001",
            created_at=now - timedelta(minutes=2),
            as_of_time=now - timedelta(minutes=2),
            market_class="forex",
            provider="model.ensemble.v1",
            symbol="EURUSD",
            timeframe="M1",
            model_artifact_id="model.eurusd.classifier",
            model_version="1.4.2",
            feature_set_version="feat.m1.v2",
            experiment_id="exp-001",
            statistical_report_id=None,
            calibration_report_id="val-001",
            economic_report_id=None,
            generalization_report_id=None,
            inference_input_hash="a1b2c3d4e5f6789012345678abcdef01",
            raw_score=0.812,
            calibrated_confidence=0.784,
            input_staleness_seconds=4,
            signal_validity_seconds=300,
            expires_at=now + timedelta(hours=2),
            freshness_status="fresh",
            signal_direction="LONG_BIAS",
            signal_state="emitted",
            state_reason="Domain criteria validated",
            eligibility_reasons=["low_spread", "high_liquidity"],
            operating_domain_status="in_domain",
            calibration_status="calibrated",
            economic_verdict="cost_favorable",
            risk_notes="Elevated spread risk during session rollover.",
            rationale="Multi-timeframe momentum alignment with order flow imbalance.",
            explainability_summary={"rsi_14": 0.324, "macd_hist": 0.182, "momentum_z": 0.441},
            state_transition_history=["draft", "validated", "emitted"],
            audit_correlation_id="audit-sig-001",
        )

        # Signal 2: Expired (Uncertainty: Unavailable)
        sig2 = AdvisorySignal(
            signal_id="sig-002",
            created_at=now - timedelta(minutes=45),
            as_of_time=now - timedelta(minutes=45),
            market_class="forex",
            provider="model.ensemble.v1",
            symbol="EURUSD",
            timeframe="M1",
            model_artifact_id="model.eurusd.classifier",
            model_version="1.4.2",
            feature_set_version="feat.m1.v2",
            experiment_id="exp-001",
            statistical_report_id=None,
            calibration_report_id=None,
            economic_report_id=None,
            generalization_report_id=None,
            inference_input_hash="b2c3d4e5f6a1789012345678abcdef02",
            raw_score=0.650,
            calibrated_confidence=0.625,
            input_staleness_seconds=350,
            signal_validity_seconds=60,
            expires_at=now - timedelta(minutes=15),
            freshness_status="expired",
            signal_direction="SHORT_BIAS",
            signal_state="expired",
            state_reason="Signal validity TTL exceeded",
            eligibility_reasons=[],
            operating_domain_status="in_domain",
            calibration_status="uncalibrated",
            economic_verdict="unverified",
            risk_notes=None,
            rationale="Mean-reversion trigger at upper Bollinger band.",
            explainability_summary={"bb_upper": 0.450},
            state_transition_history=["emitted", "expired"],
            audit_correlation_id="audit-sig-002",
        )

        # Signal 3: Withheld (Unbracketed confidence 0.480 vs [0.724, 0.841] -> Uncertainty: Unavailable)
        sig3 = AdvisorySignal(
            signal_id="sig-003",
            created_at=now - timedelta(minutes=30),
            as_of_time=now - timedelta(minutes=30),
            market_class="forex",
            provider="model.ensemble.v1",
            symbol="EURUSD",
            timeframe="M1",
            model_artifact_id="model.eurusd.classifier",
            model_version="1.4.2",
            feature_set_version="feat.m1.v2",
            experiment_id="exp-001",
            statistical_report_id=None,
            calibration_report_id="val-001",
            economic_report_id=None,
            generalization_report_id=None,
            inference_input_hash="c3d4e5f6a1b2789012345678abcdef03",
            raw_score=0.420,
            calibrated_confidence=0.480,
            input_staleness_seconds=12,
            signal_validity_seconds=60,
            expires_at=now - timedelta(minutes=10),
            freshness_status="withheld",
            signal_direction="NEUTRAL",
            signal_state="withheld",
            state_reason="High volatility regime threshold exceeded",
            eligibility_reasons=["volatility_clamp"],
            operating_domain_status="out_of_domain",
            calibration_status="calibrated",
            economic_verdict="unfavorable",
            risk_notes="News release volatility regime.",
            rationale="Indeterminate trend direction under news release volatility.",
            explainability_summary={},
            state_transition_history=["draft", "withheld"],
            audit_correlation_id="audit-sig-003",
        )
        session.add_all([sig1, sig2, sig3])

        # 8. Seed Trade Plans (P05)
        plan1 = TradePlanNoteRecord(
            plan_id="plan-001",
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=2),
            operator_id="operator_admin",
            title="London Open Momentum Thesis",
            market_context="EUR/USD M1 London Open breakout session",
            hypothesis="Order flow imbalance indicates multi-timeframe upward momentum bias.",
            linked_signal_ids=["sig-001"],
            linked_report_ids=["val-001"],
            scenario_notes="Dependent on ECB rate pause stability.",
            risk_notes="Elevated spread risk during Asian transition.",
            invalidating_conditions_text="Spread widening above 1.5 pips or volume dry-up.",
            decision_status="reviewed",
            research_disclaimer=(
                "Trade plan research note only. Hypothetical research, not financial advice, "
                "not a trade instruction, not an order ticket. Operator judgment required. AXIOM does not act."
            ),
            research_status="research_only",
            audit_correlation_id="audit-plan-001-abc",
        )

        plan2 = TradePlanNoteRecord(
            plan_id="plan-002",
            created_at=now - timedelta(hours=4),
            updated_at=now - timedelta(hours=1), # Disclosed as EDITED
            operator_id="operator_admin",
            title="Mean Reversion at Bollinger Band",
            market_context="EUR/USD M1 Overextended Range",
            hypothesis="Mean reversion expected following 2.5 sigma excursion.",
            linked_signal_ids=[],
            linked_report_ids=[],
            scenario_notes=None,
            risk_notes="High impact news release scheduled in 30 minutes.",
            invalidating_conditions_text="Breakout beyond 3.0 sigma on volume spike.",
            decision_status="draft",
            research_disclaimer=(
                "Trade plan research note only. Hypothetical research, not financial advice, "
                "not a trade instruction, not an order ticket. Operator judgment required. AXIOM does not act."
            ),
            research_status="research_only",
            audit_correlation_id="audit-plan-002-def",
        )
        session.add_all([plan1, plan2])

        # 9. Seed Manual Journal Entries (P05)
        journ1 = ManualTradeJournalEntryRecord(
            journal_id="journ-001",
            created_at=now - timedelta(hours=1),
            operator_id="operator_admin",
            title="Session Execution Reflection",
            reflection_text="Maintained strict patience during high spread environment; respected invalidating condition.",
            linked_plan_id="plan-001",
            linked_signal_ids=["sig-001"],
            linked_report_ids=[],
            emotion_tags=["disciplined", "patient"],
            process_tags=["followed_checklist", "logged_hypothesis"],
            lesson_notes="Avoid entering before London liquidity injection confirms.",
            research_disclaimer=(
                "Manual research journal entry only. Not financial advice, not a trade record, "
                "not a trade instruction. Operator judgment required. AXIOM does not act."
            ),
            research_status="research_only",
            audit_correlation_id="audit-journ-001-ghi",
        )

        journ2 = ManualTradeJournalEntryRecord(
            journal_id="journ-002",
            created_at=now - timedelta(hours=5),
            operator_id="operator_admin",
            title="Asian Range Boundary Review",
            reflection_text="Observed tight compression prior to European crossover.",
            linked_plan_id=None,
            linked_signal_ids=[],
            linked_report_ids=[],
            emotion_tags=["observant"],
            process_tags=["spread_monitored"],
            lesson_notes="Keep position size zero in presentation mode.",
            research_disclaimer=(
                "Manual research journal entry only. Not financial advice, not a trade record, "
                "not a trade instruction. Operator judgment required. AXIOM does not act."
            ),
            research_status="research_only",
            audit_correlation_id="audit-journ-002-jkl",
        )
        session.add_all([journ1, journ2])

        # 10. Seed Portfolio Risk Report (P05)
        risk_rep = PortfolioRiskReport(
            id="risk-001",
            created_at=now - timedelta(hours=1),
            artifact_type="portfolio_risk_report",
            method_version="w4-u05.market_series_risk_pure_python.v1",
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            as_of_start=now - timedelta(days=7),
            as_of_end=now,
            sample_count=500,
            max_drawdown=-0.142,
            realized_volatility=0.118,
            stress_loss=-0.225,
            metrics={
                "max_drawdown": -0.142,
                "realized_volatility": 0.118,
                "stress_loss": -0.225,
            },
            uncertainty={
                "max_drawdown": {
                    "lower": -0.185,
                    "upper": -0.112,
                    "confidence_level": 0.95,
                    "method": "bootstrap_percentile",
                },
                "realized_volatility": {
                    "lower": 0.095,
                    "upper": 0.138,
                    "confidence_level": 0.95,
                    "method": "chi_square_interval",
                },
                "stress_loss": {
                    "lower": -0.285,
                    "upper": -0.182,
                    "confidence_level": 0.95,
                    "method": "historical_simulation",
                },
            },
            assumptions={
                "stress_multiplier": 2.0,
                "tail_quantile": 0.05,
                "scenario_horizon": "1-day",
            },
            economic_usefulness={"verdict": "not_assessed"},
            config={},
            input_lineage={"source": "market_candles"},
            source_artifact_ids=[],
            market_scope={"symbol": "EURUSD"},
            results={},
            limitations=["Historical research only", "Zero execution guarantee"],
            report_hash="risk-hash-01",
            research_status="research_only",
            created_by="system",
            audit_correlation_id="audit-risk-001",
            notes="Portfolio risk analytics report",
        )
        session.add(risk_rep)

        # 11. Seed Scenario Report (P05)
        scen_rep = ScenarioReport(
            id="scen-001",
            created_at=now - timedelta(hours=1),
            artifact_type="scenario_report",
            method_version="w4-u04.scenario_shock.v1",
            market_class="forex",
            symbol="EURUSD",
            timeframe="M1",
            as_of_start=now - timedelta(days=7),
            as_of_end=now,
            sample_count=500,
            scenario_name="Hawkish Central Bank Rate Shock",
            hypothetical_return=-0.084,
            scenario_result={"shock_magnitude_bps": 75},
            assumptions={"rate_hike_bps": 75, "volatility_multiplier": 1.8},
            inputs={},
            uncertainty={
                "lower": -0.115,
                "upper": -0.055,
                "confidence_level": 0.95,
            },
            economic_usefulness={"verdict": "not_assessed"},
            config={},
            input_lineage={},
            source_artifact_ids=[],
            market_scope={"symbol": "EURUSD"},
            results={},
            limitations=["Hypothetical simulation only"],
            report_hash="scen-hash-01",
            research_status="research_only",
            created_by="system",
            audit_correlation_id="audit-scen-001",
            notes="Macro scenario shock report",
        )
        session.add(scen_rep)

        await session.commit()

    await close_db()
    print("UI_NEW_P05_EVIDENCE_SEED_COMPLETE")


if __name__ == "__main__":
    asyncio.run(seed_data())
