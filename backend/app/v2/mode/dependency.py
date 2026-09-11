"""V2 Mode Dependencies — FastAPI dependencies for mode enforcement.

Mode is injected from config, not from client input.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from app.v2.errors.contract import ModeError, V2ErrorCode


def get_request_mode(request: Request) -> str:
    """FastAPI dependency: mode from config, not from client."""
    return request.app.state.v2_mode


def require_mode(*allowed: str):
    """Dependency factory: reject requests not in allowed modes."""

    def checker(mode: str = Depends(get_request_mode)) -> str:
        if mode not in allowed:
            raise ModeError(V2ErrorCode.MODE_NOT_AUTHORIZED, mode)
        return mode

    return checker


# Pre-built dependencies for common mode requirements
RequireResearch = Annotated[str, Depends(require_mode("RESEARCH"))]
RequireSimulation = Annotated[str, Depends(require_mode("SIMULATION"))]
RequireResearchOrSimulation = Annotated[
    str, Depends(require_mode("RESEARCH", "SIMULATION"))
]
