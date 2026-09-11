"""Chronology and data-integrity guard (W2-U01)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Iterable

from app.core.time import require_utc


class GuardStage(StrEnum):
    INGESTION = "ingestion"
    DATASET_CONSTRUCTION = "dataset_construction"
    TRAINING_SET_GENERATION = "training_set_generation"
    EXPERIMENT_EXECUTION = "experiment_execution"


class SourceAuthority(StrEnum):
    AUTHORITATIVE = "authoritative"
    SIMULATED = "simulated"
    SYNTHETIC = "synthetic"
    UNKNOWN = "unknown"


class QuarantineReason(StrEnum):
    FUTURE_OPEN_TIME = "FUTURE_OPEN_TIME"
    OUT_OF_ORDER_TIME = "OUT_OF_ORDER_TIME"
    DUPLICATE_NATURAL_KEY = "DUPLICATE_NATURAL_KEY"
    SYNTHETIC_SOURCE_NOT_AUTHORITATIVE = "SYNTHETIC_SOURCE_NOT_AUTHORITATIVE"
    SIMULATED_FORWARD_DATED = "SIMULATED_FORWARD_DATED"
    NAIVE_TIMESTAMP = "NAIVE_TIMESTAMP"
    SPLIT_LEAKAGE = "SPLIT_LEAKAGE"
    UNKNOWN_SOURCE_AUTHORITY = "UNKNOWN_SOURCE_AUTHORITY"
    LABEL_HORIZON_LEAKAGE = "LABEL_HORIZON_LEAKAGE"


@dataclass(frozen=True, slots=True)
class GuardRecord:
    source_record_id: str | None
    market_class: str
    provider: str
    symbol: str
    timeframe: str
    open_time: datetime
    source: str
    authority: SourceAuthority
    ingestion_finished_at: datetime
    as_of_time: datetime
    self_declared_as_of_time: datetime | None = None

    @property
    def series_key(self) -> tuple[str, str, str, str]:
        return (self.market_class, self.provider, self.symbol, self.timeframe)

    @property
    def natural_key(self) -> tuple[str, str, str, str, datetime, str]:
        return (*self.series_key, self.open_time, self.source)


@dataclass(frozen=True, slots=True)
class QuarantineEvent:
    record: GuardRecord | None
    reason: QuarantineReason
    stage: GuardStage
    detail: str
    open_time: datetime | None = None


class ChronologyGuard:
    """Formal chronology contract for ML datasets."""

    def validate_records(
        self,
        records: Iterable[GuardRecord],
        *,
        stage: GuardStage,
        allow_resort: bool = False,
        authoritative_training: bool = True,
    ) -> tuple[list[GuardRecord], list[QuarantineEvent]]:
        accepted: list[GuardRecord] = []
        quarantine: list[QuarantineEvent] = []
        seen: set[tuple[str, str, str, str, datetime, str]] = set()
        last_by_series: dict[tuple[str, str, str, str], datetime] = {}

        for record in records:
            try:
                require_utc(record.open_time, boundary="chronology.record.open_time")
                require_utc(
                    record.ingestion_finished_at,
                    boundary="chronology.ingestion_finished_at",
                )
                require_utc(record.as_of_time, boundary="chronology.as_of_time")
            except ValueError as exc:
                quarantine.append(
                    QuarantineEvent(
                        record=record,
                        reason=QuarantineReason.NAIVE_TIMESTAMP,
                        stage=stage,
                        detail=str(exc),
                        open_time=record.open_time,
                    )
                )
                continue

            if (
                record.open_time > record.as_of_time
                or record.open_time > record.ingestion_finished_at
            ):
                quarantine.append(
                    QuarantineEvent(
                        record=record,
                        reason=QuarantineReason.FUTURE_OPEN_TIME,
                        stage=stage,
                        detail="open_time exceeds authoritative as-of/ingestion anchor",
                        open_time=record.open_time,
                    )
                )
                continue

            if record.natural_key in seen:
                quarantine.append(
                    QuarantineEvent(
                        record=record,
                        reason=QuarantineReason.DUPLICATE_NATURAL_KEY,
                        stage=stage,
                        detail="duplicate natural key",
                        open_time=record.open_time,
                    )
                )
                continue
            seen.add(record.natural_key)

            last_time = last_by_series.get(record.series_key)
            if last_time is not None and record.open_time < last_time:
                if record.authority == SourceAuthority.AUTHORITATIVE and not allow_resort:
                    quarantine.append(
                        QuarantineEvent(
                            record=record,
                            reason=QuarantineReason.OUT_OF_ORDER_TIME,
                            stage=stage,
                            detail=(
                                "authoritative series out of order; "
                                "quarantine, do not resort silently"
                            ),
                            open_time=record.open_time,
                        )
                    )
                    continue
            last_by_series[record.series_key] = max(last_time or record.open_time, record.open_time)

            if authoritative_training:
                if (
                    record.authority == SourceAuthority.SYNTHETIC
                    or record.source == "seed:synthetic"
                ):
                    quarantine.append(
                        QuarantineEvent(
                            record=record,
                            reason=QuarantineReason.SYNTHETIC_SOURCE_NOT_AUTHORITATIVE,
                            stage=stage,
                            detail=(
                                "synthetic seed data excluded from "
                                "authoritative training datasets"
                            ),
                            open_time=record.open_time,
                        )
                    )
                    continue
                if (
                    record.authority == SourceAuthority.SIMULATED
                    and record.source == "live:simulated"
                ):
                    quarantine.append(
                        QuarantineEvent(
                            record=record,
                            reason=QuarantineReason.SIMULATED_FORWARD_DATED,
                            stage=stage,
                            detail=(
                                "simulated live data excluded from "
                                "authoritative training datasets"
                            ),
                            open_time=record.open_time,
                        )
                    )
                    continue
                if record.authority == SourceAuthority.UNKNOWN:
                    quarantine.append(
                        QuarantineEvent(
                            record=record,
                            reason=QuarantineReason.UNKNOWN_SOURCE_AUTHORITY,
                            stage=stage,
                            detail="unknown source authority not allowed in authoritative datasets",
                            open_time=record.open_time,
                        )
                    )
                    continue

            accepted.append(record)
        return accepted, quarantine

    def validate_temporal_split(self, *, split_strategy: str) -> None:
        if split_strategy.lower() in {"random", "shuffle", "random_row"}:
            raise ValueError(QuarantineReason.SPLIT_LEAKAGE.value)

    def validate_label_horizon(
        self,
        *,
        label_start: datetime,
        label_horizon_end: datetime,
        validation_start: datetime,
        embargo: timedelta = timedelta(0),
    ) -> None:
        require_utc(label_start, boundary="label_horizon.start")
        require_utc(label_horizon_end, boundary="label_horizon.end")
        require_utc(validation_start, boundary="label_horizon.validation_start")
        if label_horizon_end + embargo > validation_start:
            raise ValueError(QuarantineReason.LABEL_HORIZON_LEAKAGE.value)
