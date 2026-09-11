"""W4-U01 Institutional Intelligence foundation tests."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from app.institutional_intelligence import (
    APPROVED_COMPILED_DEPENDENCIES,
    SCIENTIFIC_DEPENDENCY_POLICY,
    WAVE4_CANDIDATE_DEPENDENCIES,
    IntelligenceArtifactDraft,
    IntelligenceArtifactFactory,
)
from app.institutional_intelligence.scientific_fallbacks import mean, pearson_correlation


def _draft(**overrides):  # noqa: ANN003, ANN201
    data = {
        "artifact_type": "foundation_policy_test",
        "method_version": "w4-u01.v1",
        "config": {"window": 20},
        "input_lineage": {"source": "unit-test", "as_of_policy": "point_in_time"},
        "source_artifact_ids": ["signal-1", "validation-1"],
        "market_scope": {"markets": ["forex"], "timeframes": ["M1"]},
        "as_of_start": datetime(2026, 7, 16, 9, 0, tzinfo=timezone.utc),
        "as_of_end": datetime(2026, 7, 16, 10, 0, tzinfo=timezone.utc),
        "sample_count": 42,
        "uncertainty": {
            "method": "wilson_score_interval",
            "confidence_level": 0.95,
            "sample_count": 42,
        },
        "results": {"metric": 0.5, "interpretation": "research_only"},
        "limitations": ["advisory_research_only", "not_a_trade_instruction"],
        "created_by": "pytest",
    }
    data.update(overrides)
    return IntelligenceArtifactDraft(**data)


def test_artifact_contract_contains_mandatory_fields_and_audit_details() -> None:
    artifact = IntelligenceArtifactFactory().build(_draft())
    assert artifact.artifact_id
    assert artifact.created_at.tzinfo is not None
    assert artifact.research_status == "research_only"
    assert artifact.sample_count == 42
    assert artifact.uncertainty["method"] == "wilson_score_interval"
    assert artifact.report_hash
    details = artifact.to_audit_details()
    assert details["artifact_id"] == artifact.artifact_id
    assert details["report_hash"] == artifact.report_hash
    assert details["audit_correlation_id"] == artifact.audit_correlation_id


def test_artifact_contract_rejects_action_or_remediation_payloads() -> None:
    with pytest.raises(ValueError, match="ARTIFACT_ACTION_PAYLOAD_FORBIDDEN"):
        IntelligenceArtifactFactory().build(
            _draft(results={"metric": 0.5, "order_payload": {"side": "none"}})
        )
    with pytest.raises(ValueError, match="ARTIFACT_ACTION_PAYLOAD_FORBIDDEN"):
        IntelligenceArtifactFactory().build(
            _draft(config={"remediation_payload": {"auto": True}})
        )


def test_artifact_contract_rejects_missing_uncertainty_or_bad_time() -> None:
    with pytest.raises(ValueError, match="ARTIFACT_UNCERTAINTY_REQUIRED"):
        IntelligenceArtifactFactory().build(_draft(uncertainty={"method": "none"}))
    with pytest.raises(ValueError, match="ARTIFACT_AS_OF_RANGE_INVALID"):
        IntelligenceArtifactFactory().build(
            _draft(
                as_of_start=datetime(2026, 7, 16, 11, 0, tzinfo=timezone.utc),
                as_of_end=datetime(2026, 7, 16, 10, 0, tzinfo=timezone.utc),
            )
        )
    with pytest.raises(ValueError, match="ARTIFACT_RESEARCH_ONLY_REQUIRED"):
        IntelligenceArtifactFactory().build(_draft(research_status="deployed"))


def test_pure_python_scientific_fallbacks_known_values() -> None:
    assert mean([Decimal("1"), Decimal("2"), Decimal("3")]) == 2.0
    assert pearson_correlation([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)
    assert pearson_correlation([1, 2, 3], [3, 2, 1]) == pytest.approx(-1.0)


def test_compiled_dependency_policy_has_candidates_but_no_unapproved_imports() -> None:
    assert {item.package for item in WAVE4_CANDIDATE_DEPENDENCIES} == {"numpy", "pandas", "scipy"}
    assert APPROVED_COMPILED_DEPENDENCIES == ()
    assert "No Wave-4 application code may import" in SCIENTIFIC_DEPENDENCY_POLICY

    root = Path(__file__).resolve().parents[1] / "app" / "institutional_intelligence"
    forbidden_imports = ("import numpy", "import pandas", "import scipy", "import sklearn")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden_imports:
            assert needle not in text


def test_institutional_intelligence_context_has_no_execution_or_broker_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "institutional_intelligence"
    forbidden = (
        "place_order",
        "cancel_order",
        "broker.",
        "advisory_status =",
        "model.status =",
    )
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text
