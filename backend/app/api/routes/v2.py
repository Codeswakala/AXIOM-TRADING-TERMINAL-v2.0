"""V2 API route mount — mounts V2 router into the main API."""

from __future__ import annotations

from app.v2.api.router import router as v2_router

__all__ = ["v2_router"]
