"""BO-B-06 — assistant ask-path request schema.

The ask endpoint takes a bounded prompt and operator-selected grounding
artifact ids. The responder is deterministic, local, non-actuating; the
request contract reflects exactly that (no tools, no options, no injection).
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class AssistantRespondRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=1000)
    grounding_source_ids: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("prompt")
    @classmethod
    def _strip_nonempty(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("prompt must not be blank")
        return stripped

    @field_validator("grounding_source_ids")
    @classmethod
    def _clean_ids(cls, value: list[str]) -> list[str]:
        cleaned: list[str] = []
        for item in value:
            stripped = item.strip()
            if not stripped or len(stripped) > 128:
                raise ValueError("grounding source ids must be 1..128 characters")
            cleaned.append(stripped)
        return cleaned
