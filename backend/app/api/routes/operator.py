"""Operator profile endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.auth.dependencies import CurrentOperatorDep
from app.models.auth import OperatorRead

router = APIRouter(prefix="/operator", tags=["operator"])


@router.get("/me", response_model=OperatorRead, summary="Current operator profile")
async def me(operator: CurrentOperatorDep) -> OperatorRead:
    return OperatorRead.model_validate(operator)
