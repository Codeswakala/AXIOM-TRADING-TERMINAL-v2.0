"""Inference and eligibility errors (W3-U01)."""

from __future__ import annotations


class EligibilityError(RuntimeError):
    """Base eligibility error."""


class ModelEligibilityError(EligibilityError):
    """Raised when a model fails governed eligibility checks."""


class InferenceInputError(EligibilityError):
    """Raised when inference input violates chronology/domain/identity rules."""
