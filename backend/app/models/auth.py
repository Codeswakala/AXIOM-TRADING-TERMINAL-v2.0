"""Auth API schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.core.time import coerce_external_utc


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class OperatorRead(BaseModel):
    id: str
    username: str
    role: str
    is_active: bool
    display_name: str | None
    last_login_at: datetime | None
    created_at: datetime

    @field_validator("last_login_at", "created_at")
    @classmethod
    def _datetimes_utc(cls, value: datetime | None) -> datetime | None:
        return coerce_external_utc(value, source="operator schema output")

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    tokens: TokenResponse
    operator: OperatorRead
