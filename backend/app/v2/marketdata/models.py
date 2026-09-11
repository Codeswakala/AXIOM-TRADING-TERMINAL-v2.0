"""V2 BE-2 Pydantic response/request models — typed envelopes throughout.

Every data-bearing response carries the mandatory provenance block; every
verification response carries reconstructive=false / capability
"verification-only" (ITRGA-DET-V2-BE-2-PLAN-001 §1.2 / OBS-V2-BE2-02).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class V2ProvenanceModel(BaseModel):
    """Mandatory provenance block. No data response may omit it."""

    source_kind: str
    authority: str
    source_id: str
    as_of: datetime | None
    display_label: str
    verification_id: str | None = None


class V2MdInstrumentModel(BaseModel):
    instrument_id: str
    market_class: str
    display_symbol: str
    precision: int
    created_at: datetime


class V2MdSymbolMapModel(BaseModel):
    source_id: str
    source_symbol: str
    instrument_id: str


class V2MdInstrumentListResponse(BaseModel):
    instruments: list[V2MdInstrumentModel]
    mappings: list[V2MdSymbolMapModel]
    total: int
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdInstrumentDetailResponse(BaseModel):
    instrument: V2MdInstrumentModel
    mappings: list[V2MdSymbolMapModel]
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdSourceModel(BaseModel):
    source_id: str
    kind: str
    authority: str
    mode_scope: str
    active: bool
    display_label: str


class V2MdSourceListResponse(BaseModel):
    sources: list[V2MdSourceModel]
    total: int
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdSeriesModel(BaseModel):
    instrument_id: str
    timeframe: str
    source_id: str
    first_open_time: datetime | None
    last_open_time: datetime | None
    bar_count: int
    freshness: str = Field(description="Computed at read time; never persisted")
    availability: str
    provenance: V2ProvenanceModel


class V2MdSeriesListResponse(BaseModel):
    series: list[V2MdSeriesModel]
    total: int
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdBarModel(BaseModel):
    open_time: datetime
    open: str
    high: str
    low: str
    close: str
    volume: str | None


class V2MdBarsResponse(BaseModel):
    instrument_id: str
    timeframe: str
    bars: list[V2MdBarModel]
    total: int
    provenance: V2ProvenanceModel
    freshness: str
    availability: str
    gaps_disclosed: list[str] = Field(
        default_factory=list,
        description="Missing-period starts inside the returned window (disclosed, never filled)",
    )
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdExceptionModel(BaseModel):
    id: str
    series_ref: str
    operator_id: str
    exception_type: str
    fingerprint: str
    detail: dict[str, Any] | None
    observed_at: datetime
    mode: str
    correlation_id: str | None


class V2MdExceptionListResponse(BaseModel):
    exceptions: list[V2MdExceptionModel]
    total: int
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdVerificationScopeItemModel(BaseModel):
    instrument_id: str
    timeframe: str
    source_id: str


class V2MdVerificationCreateRequest(BaseModel):
    scope: list[V2MdVerificationScopeItemModel] = Field(min_length=1, max_length=20)
    as_of: datetime


class V2MdVerificationModel(BaseModel):
    verification_id: str
    scope: dict[str, Any]
    as_of: datetime
    content_hash: str
    row_count: int
    source_ids: list[str]
    created_by_operator_id: str
    created_at: datetime
    reconstructive: bool = Field(
        default=False,
        description="Always false: tamper-evidence only; cannot reconstruct original rows",
    )
    capability: str = Field(default="verification-only")


class V2MdVerificationListResponse(BaseModel):
    records: list[V2MdVerificationModel]
    total: int
    scope: str  # "operator" | "all"
    reconstructive: bool = False
    capability: str = "verification-only"
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdVerificationDetailResponse(BaseModel):
    record: V2MdVerificationModel
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdVerifyResultResponse(BaseModel):
    verification_id: str
    match: bool
    expected_hash: str
    actual_hash: str
    row_count_now: int
    reconstructive: bool = False
    capability: str = "verification-only"
    mode: str
    correlation_id: str | None = None
    timestamp: datetime


class V2MdCatalogRefreshResponse(BaseModel):
    series_created: int
    series_updated: int
    series_unchanged: int
    exceptions_appended: int
    exceptions_deduplicated: int
    unmapped_sources: list[str]
    mode: str
    correlation_id: str | None = None
    timestamp: datetime
