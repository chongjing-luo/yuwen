#!/usr/bin/env python3
"""Validate the canonical storage layout contract.

The contract lives in docs/architecture/storage-layout.json.  This check keeps
human-facing navigation, machine paths and the filesystem on the same layout.
Historical ADRs and archived development logs may name former paths; active
operational files may not.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/architecture/storage-layout.json"
ACTIVE_TEXT_ROOTS = (
    ROOT / "AGENTS.md",
    ROOT / "DEVLOG.md",
    ROOT / ".agents/skills",
    ROOT / "scripts",
    ROOT / "tests",
    ROOT / "work",
    ROOT / "docs/architecture",
    ROOT / "docs/workflow",
)
TEXT_SUFFIXES = {".md", ".py", ".js", ".json", ".jsonl", ".yaml", ".yml", ".txt"}
SCAN_EXCLUDES = {
    CONTRACT,
    ROOT / "work/knowledge/_meta/catalog.jsonl",
    ROOT / "work/knowledge/INDEX.md",
}


def _text_files(path: Path):
    if path.is_file():
        if path.suffix in TEXT_SUFFIXES:
            yield path
        return
    if not path.exists():
        return
    for item in path.rglob("*"):
        if item.is_file() and item.suffix in TEXT_SUFFIXES and item not in SCAN_EXCLUDES:
            yield item


def validate(root: Path = ROOT) -> list[str]:
    contract_path = root / "docs/architecture/storage-layout.json"
    if not contract_path.is_file():
        return [f"missing storage contract: {contract_path.relative_to(root)}"]
    data = json.loads(contract_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    for label, rel in data.get("canonical_roots", {}).items():
        if not (root / rel).is_dir():
            errors.append(f"missing canonical root {label}: {rel}")

    for rel in data.get("legacy_roots", []):
        if (root / rel).exists():
            errors.append(f"legacy root still exists: {rel}")

    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    for rel in data.get("important_paths", []):
        if not (root / rel).exists():
            errors.append(f"important path does not resolve: {rel}")
        if f"`{rel}`" not in agents:
            errors.append(f"AGENTS.md does not register important path: {rel}")

    # Test repositories rooted elsewhere only need structural checks above.
    if root != ROOT:
        return errors

    legacy = tuple(data.get("legacy_roots", []))
    for start in ACTIVE_TEXT_ROOTS:
        for path in _text_files(start):
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for old in legacy:
                if old in content:
                    errors.append(
                        f"active file still references legacy path {old}: {path.relative_to(root)}"
                    )
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("storage layout: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("storage layout: PASSED (storage contract)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
