#!/usr/bin/env python3
"""Create traceable subquestion Markdown files for 2018--2020 Q7 groups.

The parent Q7 files remain untouched.  Each derived file links back to its
parent question/analysis segment, MinerU source and PDF, and records that the
boundary is derived rather than a new authoritative scan.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM_ROOT = ROOT / "Data/2008-2024·（四川）语文高考真题"
TARGETS = {
    2018: {"group_total": 20, "subtypes": {"1": "idiom_usage", "2": "sentence_error", "3": "completion"}},
    2019: {"group_total": 9, "subtypes": {"1": "lexical_usage", "2": "sequence_selection", "3": "sentence_error"}},
    2020: {"group_total": 9, "subtypes": {"1": "sequence_selection", "2": "lexical_usage", "3": "sentence_error"}},
}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def q7_section(text: str) -> str:
    """Keep the last top-level Q7 section, avoiding preceding Q6 analysis."""
    matches = list(re.finditer(r"(?m)^#{0,6}\s*7\s*[\.．、)]", text))
    if not matches:
        return text.strip()
    section = text[matches[-1].start():]
    next_match = re.search(r"(?m)^#{0,6}\s*8\s*[\.．、)]", section)
    return section[: next_match.start()] if next_match else section


def split_parts(section: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?<!\w)[（(]\s*([123])\s*[）)]", section))
    parts: dict[str, str] = {}
    for index, match in enumerate(matches):
        code = match.group(1)
        if code in parts:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        parts[code] = section[match.start():end].strip()
        if len(parts) == 3:
            break
    return parts


def read_parent(year: int, role: str) -> tuple[Path, str, dict]:
    exam_id = f"GK-NC3-{year}"
    parent = EXAM_ROOT / f"exam_extract/{exam_id}/segments/{role}/Q007.md"
    text = parent.read_text(encoding="utf-8")
    metadata, _ = text.split("---\n\n", 1)
    # The parent metadata is simple YAML-like key/value text; keep only fields
    # needed for links and traceability rather than introducing a YAML parser.
    values: dict[str, str] = {}
    for line in metadata.splitlines():
        match = re.match(r"([A-Za-z0-9_]+):\s*\"?(.*?)\"?$", line.strip())
        if match:
            values[match.group(1)] = match.group(2).strip('"')
    return parent, body(parent), values


def render(year: int, role: str, code: str, chunk: str, parent: Path, parent_body: str, values: dict) -> str:
    exam_id = values.get("exam_id", f"GK-NC3-{year}")
    parent_rel = parent.relative_to(ROOT).as_posix()
    pdf = values.get("source_pdf", "")
    mineru = values.get("source_mineru_md", "")
    clean = values.get("source_clean_md", "")
    source_role = role
    node_id = f"{exam_id}-Q007-{code}"
    return "\n".join([
        "---",
        'schema_version: "exam-question-subquestion-0.1"',
        f'canonical_question_id: "{exam_id}-Q007"',
        f'response_node_id: "{node_id}"',
        f'exam_id: "{exam_id}"',
        'question_id: 7',
        f'subquestion_code: "{code}"',
        f'source_role: "{source_role}"',
        'question_type_l1: "language_use"',
        'question_type_l2: "language_application"',
        'derivation_status: "derived_subquestion_boundary"',
        f'parent_segment: "{parent_rel}"',
        f'parent_segment_sha256: "{sha(parent_body)}"',
        f'source_pdf: "{pdf}"',
        f'source_mineru_md: "{mineru}"',
        f'source_clean_md: "{clean}"',
        'locator_status: "inherited_parent_page_level_fallback"',
        'review_status: "needs_manual_review"',
        "---",
        "",
        f"- 原始组题：[[{parent_rel}|Q007 原始题段]]",
        f"- 原始 MinerU：[[{mineru}|full.md]]",
        f"- 原始 PDF：[[{pdf}|PDF]]",
        f"- 清洗整卷：[[{clean}|clean.md]]",
        "- 该文件仅是从父题段切出的可逆候选小问边界；不改变父题段，不承担独立官方定位。",
        "",
        chunk,
        "",
    ])


def main() -> int:
    manifest: list[dict] = []
    for year, config in TARGETS.items():
        q_parent, q_body, q_values = read_parent(year, "question")
        a_parent, a_body, a_values = read_parent(year, "analysis")
        q_parts = split_parts(q_body)
        a_parts = split_parts(q7_section(a_body))
        if set(q_parts) != {"1", "2", "3"} or set(a_parts) != {"1", "2", "3"}:
            raise SystemExit(f"{year}: expected three subquestions, got question={sorted(q_parts)} analysis={sorted(a_parts)}")
        for code in ("1", "2", "3"):
            q_out = q_parent.parent / "subquestions" / f"Q007-{code}.md"
            a_out = a_parent.parent / "subquestions" / f"Q007-{code}.md"
            q_out.parent.mkdir(parents=True, exist_ok=True)
            a_out.parent.mkdir(parents=True, exist_ok=True)
            q_out.write_text(render(year, "question", code, q_parts[code], q_parent, q_body, q_values), encoding="utf-8")
            a_out.write_text(render(year, "analysis", code, a_parts[code], a_parent, a_body, a_values), encoding="utf-8")
            manifest.append({
                "exam_id": f"GK-NC3-{year}",
                "year": year,
                "subquestion_code": code,
                "candidate_subtype": config["subtypes"][code],
                "group_total": config["group_total"],
                "question_source": q_out.relative_to(ROOT).as_posix(),
                "analysis_source": a_out.relative_to(ROOT).as_posix(),
                "parent_question_source": q_parent.relative_to(ROOT).as_posix(),
                "parent_analysis_source": a_parent.relative_to(ROOT).as_posix(),
                "question_sha256": sha(body(q_out)),
                "analysis_sha256": sha(body(a_out)),
            })
    out = ROOT / "work/knowledge/exams/workbench/kp_batches/language_group_subquestion_split_2018_2020.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"schema_version": "exam-language-group-split-0.1", "status": "candidate", "records": manifest}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"record_count": len(manifest), "manifest": str(out.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
