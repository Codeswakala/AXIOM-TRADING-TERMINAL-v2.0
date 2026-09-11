"""Read-only advisory analytics service (W3-U07)."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.advisory_signal import AdvisorySignal


@dataclass(frozen=True, slots=True)
class MetricUncertainty:
    method: str
    lower: float
    upper: float
    confidence_level: float
    sample_count: int


@dataclass(frozen=True, slots=True)
class AdvisoryMetric:
    key: str
    label: str
    value: float
    unit: str
    sample_count: int
    uncertainty: MetricUncertainty
    interpretation: str


@dataclass(frozen=True, slots=True)
class ConfidenceBand:
    label: str
    lower: float
    upper: float
    sample_count: int
    average_calibrated_confidence: float | None
    calibration_status: str
    uncertainty: MetricUncertainty
    unreliable: bool
    economic_context: str


@dataclass(frozen=True, slots=True)
class AdvisoryAnalyticsSnapshot:
    generated_from: str
    disclaimer: str
    metrics: list[AdvisoryMetric]
    confidence_bands: list[ConfidenceBand]
    notes: list[str]


class AdvisoryAnalyticsService:
    """Aggregates persisted advisory signal records without mutating state."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def snapshot(self, *, limit: int = 500) -> AdvisoryAnalyticsSnapshot:
        signals = await self._signals(limit=limit)
        total = len(signals)
        emitted = self._count(signals, "emitted")
        warning = self._count(signals, "warning")
        withheld = self._count(signals, "withheld")
        expired = self._count(signals, "expired")
        metrics = [
            self._proportion_metric(
                key="clean_advisory_rate",
                label="Clean advisory rate",
                numerator=emitted,
                denominator=total,
                interpretation="Share of persisted records that were clean advisory records.",
            ),
            self._proportion_metric(
                key="guardrail_intervention_rate",
                label="Guardrail intervention rate",
                numerator=warning + withheld + expired,
                denominator=total,
                interpretation=(
                    "Share of records where guardrails warned, withheld, "
                    "or expired the advisory."
                ),
            ),
            self._proportion_metric(
                key="withheld_rate",
                label="Withheld rate",
                numerator=withheld,
                denominator=total,
                interpretation=(
                    "Share of records withheld rather than presented as "
                    "clean advisory research."
                ),
            ),
            self._proportion_metric(
                key="expiry_rate",
                label="Expiry rate",
                numerator=expired,
                denominator=total,
                interpretation="Share of records expired and therefore not current.",
            ),
        ]
        return AdvisoryAnalyticsSnapshot(
            generated_from="advisory_signals_read_only",
            disclaimer=(
                "Research advisory analytics only. Metrics describe persisted advisory "
                "records with "
                "uncertainty; they are not financial advice and are not guaranteed future results."
            ),
            metrics=metrics,
            confidence_bands=self._confidence_bands(signals),
            notes=[
                "No returns or outcome guarantees are computed by this service.",
                "Every displayed metric includes sample count and interval uncertainty.",
                "Raw model score is intentionally excluded from analytics output.",
            ],
        )

    async def _signals(self, *, limit: int) -> list[AdvisorySignal]:
        stmt = select(AdvisorySignal).order_by(AdvisorySignal.created_at.desc()).limit(limit)
        result = await self._session.scalars(stmt)
        return list(result.all())

    def _count(self, signals: list[AdvisorySignal], state: str) -> int:
        return sum(1 for signal in signals if signal.signal_state == state)

    def _proportion_metric(
        self,
        *,
        key: str,
        label: str,
        numerator: int,
        denominator: int,
        interpretation: str,
    ) -> AdvisoryMetric:
        value = numerator / denominator if denominator else 0.0
        return AdvisoryMetric(
            key=key,
            label=label,
            value=value,
            unit="proportion",
            sample_count=denominator,
            uncertainty=self._wilson_interval(numerator=numerator, denominator=denominator),
            interpretation=interpretation,
        )

    def _confidence_bands(self, signals: list[AdvisorySignal]) -> list[ConfidenceBand]:
        bands = [
            ("Low calibrated confidence", 0.0, 0.45),
            ("Neutral calibrated confidence", 0.45, 0.55),
            ("High calibrated confidence", 0.55, 1.0),
        ]
        output: list[ConfidenceBand] = []
        for label, lower, upper in bands:
            members = [
                signal
                for signal in signals
                if signal.calibrated_confidence is not None
                and lower <= float(signal.calibrated_confidence) <= upper
            ]
            warning_count = sum(
                1
                for signal in members
                if str(signal.calibration_status).startswith("warning")
            )
            avg = (
                sum(float(signal.calibrated_confidence or 0.0) for signal in members) / len(members)
                if members
                else None
            )
            output.append(
                ConfidenceBand(
                    label=label,
                    lower=lower,
                    upper=upper,
                    sample_count=len(members),
                    average_calibrated_confidence=avg,
                    calibration_status="warning" if warning_count else "calibrated",
                    uncertainty=self._wilson_interval(
                        numerator=warning_count, denominator=len(members)
                    ),
                    unreliable=warning_count > 0,
                    economic_context=self._economic_context(members),
                )
            )
        return output

    def _economic_context(self, signals: list[AdvisorySignal]) -> str:
        if not signals:
            return "no_signal_support"
        verdicts: dict[str, int] = {}
        for signal in signals:
            verdict = signal.economic_verdict or "unknown"
            verdicts[verdict] = verdicts.get(verdict, 0) + 1
        return max(verdicts, key=verdicts.get)

    def _wilson_interval(self, *, numerator: int, denominator: int) -> MetricUncertainty:
        if denominator <= 0:
            return MetricUncertainty(
                method="wilson_score_interval",
                lower=0.0,
                upper=0.0,
                confidence_level=0.95,
                sample_count=0,
            )
        z = 1.96
        n = float(denominator)
        p = numerator / n
        denom = 1.0 + (z * z / n)
        centre = p + (z * z / (2.0 * n))
        margin = z * math.sqrt((p * (1.0 - p) / n) + (z * z / (4.0 * n * n)))
        lower = max(0.0, (centre - margin) / denom)
        upper = min(1.0, (centre + margin) / denom)
        return MetricUncertainty(
            method="wilson_score_interval",
            lower=lower,
            upper=upper,
            confidence_level=0.95,
            sample_count=denominator,
        )

    def to_dict(self, snapshot: AdvisoryAnalyticsSnapshot) -> dict[str, Any]:
        return {
            "generated_from": snapshot.generated_from,
            "disclaimer": snapshot.disclaimer,
            "metrics": [
                {
                    "key": metric.key,
                    "label": metric.label,
                    "value": metric.value,
                    "unit": metric.unit,
                    "sample_count": metric.sample_count,
                    "uncertainty": asdict(metric.uncertainty),
                    "interpretation": metric.interpretation,
                }
                for metric in snapshot.metrics
            ],
            "confidence_bands": [
                {
                    "label": band.label,
                    "lower": band.lower,
                    "upper": band.upper,
                    "sample_count": band.sample_count,
                    "average_calibrated_confidence": band.average_calibrated_confidence,
                    "calibration_status": band.calibration_status,
                    "uncertainty": asdict(band.uncertainty),
                    "unreliable": band.unreliable,
                    "economic_context": band.economic_context,
                }
                for band in snapshot.confidence_bands
            ],
            "notes": snapshot.notes,
        }
