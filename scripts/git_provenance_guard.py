#!/usr/bin/env python3
"""Staged provenance pre-commit guard (TD-AXIOM-GIT-PROVENANCE)."""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

CLASS_A = re.compile(
    r"(?P<key>PGPASSWORD|POSTGRES_PASSWORD|DB_PASSWORD|SECRET_KEY|JWT_SECRET|"
    r"JWT_SECRET_KEY|BOOTSTRAP_ADMIN_PASSWORD|ADMIN_PASSWORD|PASSWORD|PASSWD|"
    r"API_KEY|APIKEY|PRIVATE_KEY|CLIENT_SECRET|ACCESS_KEY)\s*[:=]\s*[\"']"
    r"(?P<value>[^\"'$<>{}\s]{4,})[\"']",
    re.IGNORECASE,
)
CLASS_B = re.compile(r"[a-z0-9+]+://[^/\s:@]+:[^/\s:@]+@", re.IGNORECASE)
CLASS_C = re.compile(
    r"Bearer\s+[A-Za-z0-9._-]{20,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.",
    re.IGNORECASE,
)
CONFLICT = re.compile(r"^(<<<<<<< .+|=======$|>>>>>>> .+)$", re.MULTILINE)
MANIFEST = "docs/governance/TD-AXIOM-GIT-PROVENANCE_D2_EXCEPTION_MANIFEST.md"
GUARD_IMPLEMENTATION_VERSION = "td-provenance-guard-v2-strict-conflict-ascii"
MANIFEST_ROW = re.compile(
    r"^\|\s+`(?P<path>[^`]+)`\s+\|\s+(?P<line>\d+)\s+\|\s+"
    r"(?P<class>[ABC])\s+\|\s+`(?P<identifier>[^`]+)`\s+\|\s+"
    r"`(?P<digest>[0-9a-f]{12})`\s+\|",
    re.MULTILINE | re.IGNORECASE,
)


@dataclass(frozen=True)
class ExceptionEntry:
    path: str
    line: int
    marker_class: str
    identifier: str
    digest: str


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    if check and result.returncode:
        sys.stderr.write(result.stderr)
        raise RuntimeError(f"git {' '.join(args)} failed ({result.returncode})")
    return result.stdout


def staged_paths() -> list[str]:
    raw = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]
    )
    return [item for item in raw.decode().split("\0") if item]


def staged_text(path: str) -> str:
    result = subprocess.run(["git", "show", f":{path}"], capture_output=True)
    if result.returncode:
        raise RuntimeError(f"unable to read staged path: {path}")
    return result.stdout.decode("utf-8", errors="replace")


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def parse_manifest() -> list[ExceptionEntry]:
    text = staged_text(MANIFEST)
    entries = [
        ExceptionEntry(
            path=m.group("path"),
            line=int(m.group("line")),
            marker_class=m.group("class").upper(),
            identifier=m.group("identifier").upper(),
            digest=m.group("digest").lower(),
        )
        for m in MANIFEST_ROW.finditer(text)
    ]
    if len(entries) != 2:
        raise RuntimeError(f"D2 manifest must contain exactly 2 entries; found {len(entries)}")
    if len({(e.path, e.marker_class, e.identifier, e.digest) for e in entries}) != len(entries):
        raise RuntimeError("D2 manifest contains duplicate path/class/identifier/hash entry")
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("pre-commit", "evidence", "redaction-candidates"), default="pre-commit")
    _ = parser.parse_args()
    try:
        if _.mode == "redaction-candidates":
            roots = [Path("docs/governance"), Path("docs/build-orders")]
            candidates: list[str] = []
            for root in roots:
                if root.exists():
                    candidates.extend(str(path.as_posix()) for path in root.rglob("*.md"))
            candidates.extend(str(path.as_posix()) for path in Path(".").glob("DELIVERY_REPORT*.md"))
            class_counts = {"A": 0, "B": 0, "C": 0}
            file_count = 0
            for path in sorted(set(candidates)):
                content = Path(path).read_text(encoding="utf-8", errors="replace")
                found = 0
                for label, pattern in (("A", CLASS_A), ("B", CLASS_B), ("C", CLASS_C)):
                    count = len(list(pattern.finditer(content)))
                    class_counts[label] += count
                    found += count
                if found:
                    file_count += 1
            print(f"REDACTION_CANDIDATE_FILE_COUNT: {file_count}")
            print(f"REDACTION_CANDIDATE_CLASS_A_COUNT: {class_counts['A']}")
            print(f"REDACTION_CANDIDATE_CLASS_B_COUNT: {class_counts['B']}")
            print(f"REDACTION_CANDIDATE_CLASS_C_COUNT: {class_counts['C']}")
            return 0
        entries = parse_manifest()
        by_signature = {(e.path, e.marker_class, e.identifier, e.digest): e for e in entries}
        paths = sorted(set(staged_paths()) | {e.path for e in entries})
        raw_matches: list[tuple[str, int, str, str, str | None]] = []
        conflicts: list[tuple[str, int]] = []
        for path in paths:
            text = staged_text(path)
            for marker in CONFLICT.finditer(text):
                conflicts.append((path, line_number(text, marker.start())))
            for marker in CLASS_A.finditer(text):
                identifier = marker.group("key").upper()
                digest = hashlib.sha256(marker.group("value").encode("utf-8")).hexdigest()[:12]
                entry = by_signature.get((path, "A", identifier, digest))
                raw_matches.append((path, line_number(text, marker.start()), "A", identifier, entry.digest if entry else None))
            for marker in CLASS_B.finditer(text):
                raw_matches.append((path, line_number(text, marker.start()), "B", "URL", None))
            for marker in CLASS_C.finditer(text):
                raw_matches.append((path, line_number(text, marker.start()), "C", "BEARER_OR_JWT", None))

        d2 = [match for match in raw_matches if match[4] is not None]
        unreviewed = [match for match in raw_matches if match[4] is None]
        d5 = 0
        print("=== TD-AXIOM-GIT-PROVENANCE STAGED VALUE SCAN ===")
        print(f"GUARD_IMPLEMENTATION_VERSION: {GUARD_IMPLEMENTATION_VERSION}")
        for path, line, marker_class, identifier, digest in raw_matches:
            disposition = "D2_PERMITTED_EXCEPTION" if digest else "UNREVIEWED"
            print(f"CLASS_MATCH: {path}:{line} | {marker_class} | {identifier} | {disposition}")
        for path, line in conflicts:
            print(f"CONFLICT_MARKER: {path}:{line}")
        print(f"STAGED_SECRET_MARKER_COUNT: {len(unreviewed)}")
        print(f"D2_PERMITTED_EXCEPTION_COUNT: {len(d2)}")
        print(f"D5_SYNTHETIC_DEMO_EXCEPTION_COUNT: {d5}")
        print(f"TOTAL_CLASS_MATCH_COUNT: {len(raw_matches)}")
        print(
            "COUNTER_RECONCILIATION: "
            f"{len(unreviewed)} + {len(d2)} + {d5} = {len(unreviewed) + len(d2) + d5}"
        )
        manifest_seen = {(p, c, i, d) for p, _, c, i, d in d2}
        expected = {(e.path, e.marker_class, e.identifier, e.digest) for e in entries}
        valid = (
            not conflicts
            and len(unreviewed) == 0
            and len(d2) == len(entries) == 2
            and len(raw_matches) == len(unreviewed) + len(d2) + d5
            and manifest_seen == expected
        )
        print("TD_AXIOM_GIT_PROVENANCE_GUARD_RESULT:", "PASS" if valid else "FAIL")
        return 0 if valid else 1
    except Exception as exc:  # no secret values are emitted
        print("TD_AXIOM_GIT_PROVENANCE_GUARD_RESULT: FAIL")
        print(f"GUARD_ERROR: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
