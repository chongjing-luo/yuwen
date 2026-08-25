#!/usr/bin/env python3
"""Validate the derived six-domain map against the canonical principles.

This checker protects the boundary between the human-readable P-01—P-47
statutes and their design-oriented organization view.  It deliberately checks
primary placement and mechanism references only; semantic review remains a
human review gate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re

import yaml


PRINCIPLE_ID = re.compile(r"P-(\d{2})")
CANONICAL_HEADING = re.compile(r"^###\s+(\d+)\.\s+", re.MULTILINE)
DOMAIN_HEADING = re.compile(r"^###\s+域([一二三四五六])\b.*$", re.MULTILINE)
NODE_ID = re.compile(r"\b([KUJ]\d+)\b")


def canonical_ids(text: str) -> set[str]:
    return {f"P-{int(number):02d}" for number in CANONICAL_HEADING.findall(text)}


def primary_assignments(text: str) -> list[str]:
    assignments: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if (
            stripped.startswith("- **总纲**")
            or stripped.startswith("- **跨域底线")
            or stripped.startswith("条款：")
        ):
            assignments.extend(PRINCIPLE_ID.findall(stripped))
    return [f"P-{number}" for number in assignments]


def domain_mechanism_errors(
    text: str,
    valid_nodes: set[str],
    principle_nodes: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    matches = list(DOMAIN_HEADING.finditer(text))
    expected_domains = set("一二三四五六")
    found_domains = {match.group(1) for match in matches}
    for domain in sorted(expected_domains - found_domains):
        errors.append(f"缺少域{domain}")

    for index, match in enumerate(matches):
        domain = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        mechanism_line = next(
            (line.strip() for line in body.splitlines() if line.strip().startswith("机制节点：")),
            None,
        )
        if mechanism_line is None:
            errors.append(f"域{domain}缺少机制节点")
            continue
        nodes = NODE_ID.findall(mechanism_line)
        if not nodes:
            errors.append(f"域{domain}机制节点为空")
            continue
        unknown = sorted(set(nodes) - valid_nodes)
        if unknown:
            errors.append(f"域{domain}含未知机制节点: {', '.join(unknown)}")
            continue

        assignment_line = next(
            (line.strip() for line in body.splitlines() if line.strip().startswith("条款：")),
            None,
        )
        if assignment_line is None:
            errors.append(f"域{domain}缺少条款主归属行")
            continue
        assigned_principles = {
            f"P-{number}" for number in PRINCIPLE_ID.findall(assignment_line)
        }
        expected_nodes: set[str] = set()
        for principle_id in assigned_principles:
            expected_nodes.update(principle_nodes.get(principle_id, set()))
        actual_nodes = set(nodes)
        missing = sorted(expected_nodes - actual_nodes)
        extra = sorted(actual_nodes - expected_nodes)
        if missing:
            errors.append(f"域{domain}机制节点遗漏: {', '.join(missing)}")
        if extra:
            errors.append(f"域{domain}机制节点越界: {', '.join(extra)}")
    return errors


def validate(system_map: Path, canonical: Path, registry: Path) -> list[str]:
    map_text = system_map.read_text(encoding="utf-8")
    canonical_text = canonical.read_text(encoding="utf-8")
    registry_data = yaml.safe_load(registry.read_text(encoding="utf-8"))

    expected = canonical_ids(canonical_text)
    registry_principles = {
        item["id"]
        for item in registry_data.get("principles", [])
        if re.fullmatch(r"P-\d{2}", str(item.get("id", "")))
    }
    principle_nodes = {
        item["id"]: set(item.get("nodes", []))
        for item in registry_data.get("principles", [])
        if re.fullmatch(r"P-\d{2}", str(item.get("id", "")))
    }
    valid_nodes = set(registry_data.get("nodes", {}))
    counts = Counter(primary_assignments(map_text))

    errors: list[str] = []
    for principle_id in sorted(expected):
        count = counts.get(principle_id, 0)
        if count == 0:
            errors.append(f"缺少主归属: {principle_id}")
        elif count > 1:
            errors.append(f"重复主归属: {principle_id} ({count}次)")
    for principle_id in sorted(set(counts) - expected):
        errors.append(f"未知主归属: {principle_id}")

    missing_registry = sorted(expected - registry_principles)
    extra_registry = sorted(registry_principles - expected)
    if missing_registry:
        errors.append(f"注册库缺少法条: {', '.join(missing_registry)}")
    if extra_registry:
        errors.append(f"注册库存在非权威P法条: {', '.join(extra_registry)}")

    errors.extend(domain_mechanism_errors(map_text, valid_nodes, principle_nodes))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    args = parser.parse_args()

    errors = validate(args.map, args.canonical, args.registry)
    if errors:
        print("原则体系映射校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    total = len(canonical_ids(args.canonical.read_text(encoding="utf-8")))
    print(f"原则体系映射校验通过：主归属 {total}/{total}；六域机制节点完整；注册库一致")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
