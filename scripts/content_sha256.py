#!/usr/bin/env python3
"""Compute the deterministic 2.0-textbook-eval-1 content SHA.

The file SHA is the byte hash of the input.  The content SHA excludes only the
DG4 lifecycle metadata block and the top-level ``status``/``reviewers`` YAML
fields.  It deliberately preserves the Markdown body byte-for-byte after LF
normalisation, so punctuation, IDs, evidence and version history remain part of
the hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml

LIFECYCLE_START = "<!-- lifecycle-metadata:start -->"
LIFECYCLE_END = "<!-- lifecycle-metadata:end -->"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class ContentShaError(ValueError):
    """Raised when a file cannot be canonicalised under the frozen rules."""


def _lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _front_matter(text: str) -> tuple[dict[str, Any], str]:
    text = _lf(text)
    if not text.startswith("---\n"):
        raise ContentShaError("YAML front matter must start at byte zero")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ContentShaError("YAML front matter closing marker is missing")
    raw = text[4:end]
    parsed = yaml.safe_load(raw)
    if not isinstance(parsed, dict):
        raise ContentShaError("front matter must decode to an object")
    body = text[end + len("\n---\n") :]
    return parsed, body


def _without_lifecycle(body: str) -> str:
    starts = [m.start() for m in re.finditer(re.escape(LIFECYCLE_START), body)]
    ends = [m.start() for m in re.finditer(re.escape(LIFECYCLE_END), body)]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        raise ContentShaError(
            "body must contain exactly one ordered lifecycle-metadata block"
        )
    end = ends[0] + len(LIFECYCLE_END)
    # Remove a whole surrounding line when present, but do not normalise any
    # other Markdown whitespace.
    left = starts[0]
    right = end
    if left > 0 and body[left - 1] == "\n":
        left -= 1
    if right < len(body) and body[right : right + 1] == "\n":
        right += 1
    return body[:left] + body[right:]


def canonical_payload(text: str) -> bytes:
    front, body = _front_matter(text)
    for key in ("status", "reviewers"):
        front.pop(key, None)
    body = _without_lifecycle(body)
    front_json = json.dumps(
        front, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return (front_json + "\n---\n" + body).encode("utf-8")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_sha256(path: Path) -> str:
    return hashlib.sha256(canonical_payload(path.read_text(encoding="utf-8"))).hexdigest()


def hashes(path: Path) -> dict[str, str]:
    return {
        "path": str(path),
        "pre_merge_file_sha256": file_sha256(path),
        "content_sha256": content_sha256(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        result = hashes(args.path)
    except (OSError, UnicodeError, ContentShaError, yaml.YAMLError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

