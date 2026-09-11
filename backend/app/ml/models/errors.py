"""Baseline model harness errors (W2-U06)."""

from __future__ import annotations


class ModelHarnessError(RuntimeError):
    """Base model harness error."""


class ExperimentNotApprovedError(ModelHarnessError):
    """Raised when training is attempted without an approved experiment."""


class UnresolvedExperimentPinError(ModelHarnessError):
    """Raised when dataset/split/feature pins cannot be resolved."""


class IdentityInModelInputError(ModelHarnessError):
    """Raised when symbol/provider/market identity reaches model input."""


class NonTemporalSplitError(ModelHarnessError):
    """Raised when a split manifest is not temporal/walk-forward."""
