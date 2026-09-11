"""BE-9 credential vault — the SOLE secret-resolution module (S2; BO T-7).

BE-3 P2 credential-boundary law generalized: no other module may import
the backends defined here (import-boundary test enforced). The resolved
tuple (investor read-only password + account/server):

- never enters module/global state;
- is never serialized, repr'd, logged, audited, or returned by any API;
- is held only inside the request-scoped call chain;
- passphrase NEVER stored — cryptographic N4 blindness.

Scheme (S2.1): AES-256-GCM over an Argon2id-derived key; the vault file
lives OUTSIDE the repo tree (path from AXIOM_BROKER_VAULT_PATH at unlock
time only — never created under the repo; test vaults are in-memory).
DPAPI wrapping is the Windows-console second layer applied by the
operator-side act; this module handles the inner (portable) layer.
"""

from __future__ import annotations

import json
import os
import secrets
from dataclasses import dataclass, field

from argon2.low_level import Type, hash_secret_raw
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_KDF_TIME_COST = 3
_KDF_MEMORY_KIB = 65536
_KDF_PARALLELISM = 4
_KEY_LEN = 32
_SALT_LEN = 16
_NONCE_LEN = 12

VAULT_TTL_HOURS_DEFAULT = 8  # O-2 (BO-pinned default; operator may set at INT)


@dataclass(frozen=True)
class ResolvedBrokerCredential:
    """Value fields excluded from repr/str — can never leak via rendering."""

    state: str  # "present" | "absent"
    investor_password: str | None = field(default=None, repr=False)
    account_number: str | None = field(default=None, repr=False)
    server_hostname: str | None = field(default=None, repr=False)

    def __str__(self) -> str:  # defence in depth
        return f"ResolvedBrokerCredential(state={self.state})"


ABSENT = ResolvedBrokerCredential(state="absent")

# BE-12A AM-4 (BO-V2-BE12A-001 SS1.e; adopted REQ S-4): credential CLASS
# vocabulary. The standing investor class is read-only forever (BE-9
# operating law untouched). 'practice_trade' is REGISTERED here as a
# class NAME with hygiene law only — its registration DOORWAY (a sealed
# write path into a vault payload) is 12B scope; in 12A resolution of
# the class always answers ABSENT (fail-closed stub). The funded-account
# class is NOT in this tuple and remains NONEXISTENT until the
# activation instrument (R-6.3 register line law).
CREDENTIAL_CLASSES = ("investor_read_only", "practice_trade")


def seal_practice_vault_bytes(passphrase: str, trade_password: str,
                              account_number: str,
                              server_hostname: str) -> bytes:
    """BE-12B (BO-V2-BE12B-001 SS1.e): seal the practice_trade payload.

    Own sealed payload family — the AAD pins the CLASS so an investor
    payload can never masquerade as a practice one (and vice versa).
    Registration acts remain operator-console RECORDS-OF-INTENT: this
    function is called by console acts only; no credential plaintext
    ever travels any API.
    """
    salt = secrets.token_bytes(_SALT_LEN)
    nonce = secrets.token_bytes(_NONCE_LEN)
    key = _derive_key(passphrase, salt)
    plaintext = json.dumps({
        "credential_class": "practice_trade",
        "trade_password": trade_password,
        "account_number": account_number,
        "server_hostname": server_hostname,
    }).encode("utf-8")
    ciphertext = AESGCM(key).encrypt(nonce, plaintext,
                                     b"axiom-v2-be12b-practice")
    return salt + nonce + ciphertext


def open_practice_vault_bytes(passphrase: str,
                              payload: bytes) -> ResolvedBrokerCredential:
    """Decrypt the practice payload; ANY failure or class mismatch =>
    ABSENT (never an exception that could carry material). The distinct
    AAD makes the investor payload structurally unopenable here."""
    try:
        salt = payload[:_SALT_LEN]
        nonce = payload[_SALT_LEN:_SALT_LEN + _NONCE_LEN]
        ciphertext = payload[_SALT_LEN + _NONCE_LEN:]
        key = _derive_key(passphrase, salt)
        plaintext = AESGCM(key).decrypt(nonce, ciphertext,
                                        b"axiom-v2-be12b-practice")
        data = json.loads(plaintext.decode("utf-8"))
        if data.get("credential_class") != "practice_trade":
            return ABSENT
        return ResolvedBrokerCredential(
            state="present",
            investor_password=data["trade_password"],
            account_number=data["account_number"],
            server_hostname=data["server_hostname"])
    except (InvalidTag, KeyError, ValueError, IndexError):
        return ABSENT


def resolve_practice_trade_credential(
        passphrase: str | None = None) -> ResolvedBrokerCredential:
    """AM-4 doorway (BE-12B, BY CITED EDIT of the 12A ABSENT stub —
    BO-V2-BE12B-001 SS1.e; provisioning law per ITRGA-REV-V2-BE12B-001
    §14 R1).

    PASSPHRASE-PROVISIONING LAW (R1, V2-BE12B-DEL-001): when no
    passphrase argument is supplied (the API/boundary chain — no
    material may travel it), the passphrase is read from
    `AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE` HERE, at request time,
    INSIDE vault.py ONLY — never captured into module or app state,
    never returned, never logged; the local name dies with this frame.
    The operator provisions both env names by console act (file-fed per
    THE CREDENTIAL LAW); absent either => ABSENT. N4 posture preserved:
    material exists transiently in the sole-resolution module and
    nowhere else.

    Path env `AXIOM_BROKER_PRACTICE_VAULT_PATH` names a location OUTSIDE
    the repo tree; absent env, absent file, absent/wrong passphrase,
    tampered payload, or wrong credential class => ABSENT — never an
    exception carrying material. The repr-blind return type is the
    standing contract. The investor class + read-only operating law are
    untouched: this function cannot open an investor payload (AAD
    disjoint), and the investor resolver cannot open this one.
    """
    if not passphrase:
        # R1 law: request-time env read, confined to this frame.
        passphrase = os.environ.get(
            "AXIOM_BROKER_PRACTICE_VAULT_PASSPHRASE")
    if not passphrase:
        return ABSENT
    path = os.environ.get("AXIOM_BROKER_PRACTICE_VAULT_PATH")
    if not path or not os.path.isfile(path):
        return ABSENT
    with open(path, "rb") as f:
        return open_practice_vault_bytes(passphrase, f.read())


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=passphrase.encode("utf-8"), salt=salt,
        time_cost=_KDF_TIME_COST, memory_cost=_KDF_MEMORY_KIB,
        parallelism=_KDF_PARALLELISM, hash_len=_KEY_LEN,
        type=Type.ID)


def seal_vault_bytes(passphrase: str, investor_password: str,
                     account_number: str, server_hostname: str) -> bytes:
    """Produce the encrypted vault payload (inner layer)."""
    salt = secrets.token_bytes(_SALT_LEN)
    nonce = secrets.token_bytes(_NONCE_LEN)
    key = _derive_key(passphrase, salt)
    plaintext = json.dumps({
        "investor_password": investor_password,
        "account_number": account_number,
        "server_hostname": server_hostname,
    }).encode("utf-8")
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, b"axiom-v2-be9")
    return salt + nonce + ciphertext


def open_vault_bytes(passphrase: str,
                     payload: bytes) -> ResolvedBrokerCredential:
    """Decrypt; wrong passphrase or tamper => ABSENT (never an exception
    that could carry material)."""
    try:
        salt = payload[:_SALT_LEN]
        nonce = payload[_SALT_LEN:_SALT_LEN + _NONCE_LEN]
        ciphertext = payload[_SALT_LEN + _NONCE_LEN:]
        key = _derive_key(passphrase, salt)
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, b"axiom-v2-be9")
        data = json.loads(plaintext.decode("utf-8"))
        return ResolvedBrokerCredential(
            state="present",
            investor_password=data["investor_password"],
            account_number=data["account_number"],
            server_hostname=data["server_hostname"])
    except (InvalidTag, KeyError, ValueError, IndexError):
        return ABSENT


def resolve_from_file(passphrase: str) -> ResolvedBrokerCredential:
    """Operator-console path resolution (unlock act only). The path env
    var names a location OUTSIDE the repo tree; absent/unset => ABSENT."""
    path = os.environ.get("AXIOM_BROKER_VAULT_PATH")
    if not path or not os.path.isfile(path):
        return ABSENT
    with open(path, "rb") as f:
        return open_vault_bytes(passphrase, f.read())
