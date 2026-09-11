"""V2 Mode Tests — mode enforcement, bypass refusal, Paper/Live refusal."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from app.v2.mode.contract import DEFERRED_MODES, VALID_MODES, get_mode


class TestV2ModeContract:
    """Test V2 mode contract."""

    def test_mode_defaults_to_research(self):
        """Mode defaults to RESEARCH when AXIOM_V2_MODE is not set."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AXIOM_V2_MODE", None)
            assert get_mode() == "RESEARCH"

    def test_mode_from_env_var(self):
        """Mode is read from AXIOM_V2_MODE environment variable."""
        with patch.dict(os.environ, {"AXIOM_V2_MODE": "SIMULATION"}):
            assert get_mode() == "SIMULATION"

    def test_mode_case_insensitive(self):
        """Mode value is case-insensitive."""
        with patch.dict(os.environ, {"AXIOM_V2_MODE": "research"}):
            assert get_mode() == "RESEARCH"

    def test_mode_accepts_paper(self):
        """PAPER mode is valid as of BE-8 (D-2 ruling,
        ITRGA-REV-V2-BE-8-DESIGN-001 §6; BO-V2-BE-8-001 T-2).
        Superseding churn of the BE-1-era rejection pin — disclosed."""
        with patch.dict(os.environ, {"AXIOM_V2_MODE": "PAPER"}):
            assert get_mode() == "PAPER"

    def test_mode_live_registered_locked(self):
        """AM-2 third state (BE-12A): LIVE constructs, carries the
        locked tag, actuation refuses `mode_locked` at the chokepoint.

        SUPERSEDES BY CITATION: `test_mode_rejects_live` (BE-1-era
        ValueError pin) — superseded under BO-V2-BE12A-001 SS1.e /
        DR-V2-BE-12-001 AM-2 / DA DR-review DR-F1 law (tuples stay
        byte-identical; only THIS coupon moves; no byte-pinned boundary
        file is touched).
        """
        from app.v2.live_exec.locks import (
            ActuationRefused,
            ActuationState,
            require_actuation,
        )
        from app.v2.mode.contract import (
            REGISTERED_LOCKED_MODES,
            is_registered_locked,
        )

        with patch.dict(os.environ, {"AXIOM_V2_MODE": "LIVE"}):
            mode = get_mode()  # constructs — no ValueError (AM-2)
        assert mode == "LIVE"
        assert REGISTERED_LOCKED_MODES == ("LIVE",)
        assert is_registered_locked(mode) is True
        assert is_registered_locked("PAPER") is False
        # behaviorally locked: the actuation door refuses mode_locked
        with pytest.raises(ActuationRefused) as exc:
            require_actuation(ActuationState(mode="LIVE"))
        assert exc.value.reason == "mode_locked"

    def test_mode_rejects_invalid(self):
        """Invalid mode values are rejected."""
        with patch.dict(os.environ, {"AXIOM_V2_MODE": "INVALID"}):
            with pytest.raises(ValueError, match="AXIOM_V2_MODE must be one of"):
                get_mode()

    def test_valid_modes_include_paper_as_of_be8(self):
        """Valid modes are RESEARCH, SIMULATION, PAPER (D-2, BE-8)."""
        assert VALID_MODES == ("RESEARCH", "SIMULATION", "PAPER")

    def test_deferred_modes_are_live_only(self):
        """LIVE remains the sole deferred mode (BE-10)."""
        assert DEFERRED_MODES == ("LIVE",)
