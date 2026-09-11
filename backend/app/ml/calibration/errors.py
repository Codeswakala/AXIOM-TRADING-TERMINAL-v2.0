"""Calibration framework errors (W2-U08)."""

from __future__ import annotations


class CalibrationError(RuntimeError):
    """Base calibration error."""


class CalibrationReportInvalidError(CalibrationError):
    """Raised when a calibration report lacks mandatory probability-quality fields."""


class CalibrationPinError(CalibrationError):
    """Raised when experiment/model/validation pins do not resolve."""
