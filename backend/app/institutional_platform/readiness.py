"""Enterprise scalability and multi-user readiness dispositions (W7-U07)."""

from __future__ import annotations

from dataclasses import asdict, dataclass

READINESS_VERSION = "w7-u07.enterprise_readiness.v1"
RATE_GUARD_TECHNICAL_DEBT_ID = "TD-W7-U07-RATE-GUARD"


@dataclass(frozen=True, slots=True)
class ReadinessDisposition:
    item: str
    status: str
    technical_debt_id: str | None
    rationale: str
    method_version: str = READINESS_VERSION

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


RATE_GUARD_DISPOSITION = ReadinessDisposition(
    item="abuse_rate_guard",
    status="implemented",
    technical_debt_id=RATE_GUARD_TECHNICAL_DEBT_ID,
    rationale=(
        "BO-B-07.1 closed the W7-U07 deferral: an in-memory sliding-window "
        "limiter, operator-keyed, with per-route and global ceilings, an admin "
        "allowlist, and fail-safe deny on misconfiguration. Pure standard "
        "library; no new dependency; applied to the authenticated write "
        "surfaces (ingestion, intelligence generation, collaboration POSTs, "
        "alert checks) on both API mounts. Residual deferral (disclosed): the "
        "state is per-process; a multi-instance deployment requires a shared "
        "store as a separately-governed future unit."
    ),
)

ADMIN_DEFAULT_CREDENTIAL_DISPOSITION = ReadinessDisposition(
    item="admin_admin123",
    status="rejected_when_insecure_dev_off",
    technical_debt_id=None,
    rationale=(
        "Bootstrap admin creation refuses the historical admin123 default unless "
        "AXIOM_ALLOW_INSECURE_DEV=true. Production/staging cannot enable the "
        "insecure-dev escape hatch."
    ),
)


def readiness_dispositions() -> dict[str, dict[str, str | None]]:
    return {
        "abuse_rate_guard": RATE_GUARD_DISPOSITION.to_dict(),
        "admin_admin123": ADMIN_DEFAULT_CREDENTIAL_DISPOSITION.to_dict(),
    }
