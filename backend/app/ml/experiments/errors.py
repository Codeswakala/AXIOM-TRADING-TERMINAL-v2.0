"""Experiment registry errors (W2-U05)."""

from __future__ import annotations


class ExperimentRegistryError(RuntimeError):
    """Base experiment registry error."""


class IncompleteExperimentError(ExperimentRegistryError):
    """Raised when a required pre-registration field is missing."""


class UnreproducibleExperimentPinError(ExperimentRegistryError):
    """Raised when dataset/split pins are missing, unfrozen, or mismatched."""


class ExperimentApprovalRequiredError(ExperimentRegistryError):
    """Raised when a runnable check is attempted before approval."""


class ImmutableExperimentError(ExperimentRegistryError):
    """Raised when an approved experiment plan mutation is attempted."""


class InvalidEvaluationPlanError(ExperimentRegistryError):
    """Raised when evaluation plan violates temporal/no-random split policy."""
