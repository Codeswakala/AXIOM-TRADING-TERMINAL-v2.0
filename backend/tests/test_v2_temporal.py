"""V2 Temporal Tests — naive datetime rejection, timezone validation."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.v2.errors.contract import TemporalError
from app.v2.temporal.validation import is_naive, require_utc, utc_iso, utc_now


class TestV2TemporalValidation:
    """Test V2 temporal validation."""

    def test_utc_now_returns_aware_utc(self):
        """utc_now returns timezone-aware UTC datetime."""
        now = utc_now()
        assert now.tzinfo is not None
        assert now.tzinfo == timezone.utc

    def test_is_naive_detects_naive(self):
        """is_naive detects naive datetimes."""
        naive = datetime(2026, 1, 1, 12, 0, 0)
        assert is_naive(naive) is True

    def test_is_naive_rejects_aware(self):
        """is_naive returns False for aware datetimes."""
        aware = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        assert is_naive(aware) is False

    def test_require_utc_accepts_aware_utc(self):
        """require_utc accepts timezone-aware UTC datetimes."""
        aware = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = require_utc(aware, boundary="test")
        assert result == aware

    def test_require_utc_converts_aware_non_utc(self):
        """require_utc converts aware non-UTC datetimes to UTC."""
        est = timezone(offset=__import__('datetime').timedelta(hours=-5))
        aware_est = datetime(2026, 1, 1, 12, 0, 0, tzinfo=est)
        result = require_utc(aware_est, boundary="test")
        assert result.tzinfo == timezone.utc
        assert result.hour == 17  # 12 EST = 17 UTC

    def test_require_utc_rejects_naive(self):
        """require_utc rejects naive datetimes with TemporalError."""
        naive = datetime(2026, 1, 1, 12, 0, 0)
        with pytest.raises(TemporalError, match="Naive datetime rejected"):
            require_utc(naive, boundary="test")

    def test_require_utc_accepts_none(self):
        """require_utc accepts None."""
        assert require_utc(None, boundary="test") is None

    def test_utc_iso_returns_iso_string(self):
        """utc_iso returns ISO-8601 string."""
        aware = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = utc_iso(aware)
        assert "2026-01-01T12:00:00" in result

    def test_utc_iso_returns_none_for_none(self):
        """utc_iso returns None for None input."""
        assert utc_iso(None) is None

    def test_utc_iso_rejects_naive(self):
        """utc_iso rejects naive datetimes."""
        naive = datetime(2026, 1, 1, 12, 0, 0)
        with pytest.raises(TemporalError):
            utc_iso(naive)
