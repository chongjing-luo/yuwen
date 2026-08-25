#!/usr/bin/env python3
"""Extract a reversible candidate-answer layer from answer indexes.

This is not answer verification.  It keeps the original answer-index row
untouched and copies only an exact, locally bounded excerpt into a new
derived JSONL file.  Candidate text remains ``candidate_unverified`` and
scoring remains unavailable until an independent rubric is found.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract"
OUT_REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-ANSWER-CANDIDATE-EXTRACTION-20260809.md"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def extract_candidate(text: str) -> tuple[str, str, list[str]]:
    """Return exact candidate text, method, and conservative notes."""
    clean = text.strip()
    if not clean:
        return "", "none", ["answer_text_empty"]
    if len(clean) <= 24 and not any(marker in clean for marker in ("答案", "解析", "分析")):
        return clean, "short_answer_field", ["short_field_requires_manual_confirmation"]
    matches = list(re.finditer(r"(?:^|\n)\s*(?:参考答案|答案)\s*[:：]?\s*", text))
    if not matches:
        # Keep the non-empty upstream field rather than relabeling it as
        # missing.  It may contain a full question/analysis block, but that
        # is still candidate evidence and must remain available for manual
        # adjudication.
        return clean, "raw_answer_field_unbounded", [
            "no_explicit_answer_marker",
            "manual_boundary_required",
            "candidate_unverified",
        ]
    # The last marker is normally the consolidated answer section; earlier
    # occurrences can be quoted inside the question or analysis.
    start = matches[-1].end()
    tail = text[start:]
    ends = []
    for pattern in (
        r"\n\s*【点评】",
        r"\n\s*【解析】",
        r"\n\s*【分析】",
        r"\n\s*##\s+",
    ):
        found = re.search(pattern, tail)
        if found:
            ends.append(found.start())
    end = min(ends) if ends else len(tail)
    candidate = tail[:end].strip()
    if not candidate:
        return "", "none", ["explicit_answer_marker_empty"]
    notes = ["exact_excerpt_from_last_answer_marker", "candidate_unverified"]
    if len(candidate) > 1200:
        notes.append("long_candidate_excerpt_review_before_use")
    return candidate, "explicit_answer_marker", notes


def process_exam(base: Path) -> dict:
    index = base / "answers" / "answer_index.jsonl"
    output = base / "answers" / "answer_candidates.jsonl"
    rows = read_jsonl(index)
    candidates: list[dict] = []
    for row in rows:
        raw = (row.get("answer_text") or "")
        candidate, method, notes = extract_candidate(raw)
        candidates.append({
            "schema_version": "exam-answer-candidate-0.1",
            "answer_pair_id": row.get("answer_pair_id"),
            "exam_id": row.get("exam_id"),
            "question_id": row.get("question_id"),
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified" if candidate else "missing",
            "candidate_extraction_method": method,
            "answer_candidate_text": candidate,
            "answer_candidate_sha256": sha256_text(candidate) if candidate else None,
            "raw_answer_text_sha256": sha256_text(raw) if raw else None,
            "source_status": row.get("source_status", "missing"),
            "source_pdf": row.get("source_pdf"),
            "source_mineru_md": row.get("source_mineru_md"),
            "source_answer_index": str(index.relative_to(ROOT)),
            "source_answer_bundle": row.get("answer_bundle_path"),
            "scoring_status": "not_available_as_official",
            "review_status": "needs_manual_review",
            "notes": notes,
        })
    if rows:
        output.write_text(
            "\n".join(json.dumps(row, ensure_ascii=False) for row in candidates) + "\n",
            encoding="utf-8",
        )
    elif output.exists():
        # Do not leave a stale derivative if an upstream index is deliberately
        # removed; this is a bounded generated file, not a source artifact.
        output.unlink()
    counts = {}
    for row in candidates:
        status = row["candidate_status"]
        counts[status] = counts.get(status, 0) + 1
    return {
        "exam_id": base.name,
        "index_present": index.exists(),
        "candidate_file": str(output.relative_to(ROOT)) if output.exists() else None,
        "index_rows": len(rows),
        "candidate_status_counts": counts,
    }


def render_report(reports: list[dict]) -> str:
    total = {}
    for report in reports:
        for key, value in report["candidate_status_counts"].items():
            total[key] = total.get(key, 0) + value
    lines = [
        "---",
        'schema_version: "exam-answer-candidate-extraction-0.1"',
        'status: "candidate_only"',
        'scoring_status: "not_available_as_official"',
        "---",
        "",
        "# 高考答案候选层抽取回执（2008—2024）",
        "",
        "> 本层是可逆派生物：从现有 `answer_index.jsonl` 的非空字段中截取原文，不修订原文、不补 OCR、不宣称官方答案，也不包含评分标准。",
        "",
        f"- 年度数：{len(reports)}；候选片段：{total.get('candidate_unverified', 0)}；缺失：{total.get('missing', 0)}。",
        "- 所有记录保留 `source_answer_index`、`source_answer_bundle`、原答案哈希和候选片段哈希；后续清洗必须在该层或其再派生层完成。",
        "",
        "| 试卷 | 索引行数 | 候选片段 | 缺失 | 输出 |",
        "|---|---:|---:|---:|---|",
    ]
    for report in reports:
        counts = report["candidate_status_counts"]
        lines.append(
            f"| {report['exam_id']} | {report['index_rows']} | "
            f"{counts.get('candidate_unverified', 0)} | {counts.get('missing', 0)} | "
            f"`{report['candidate_file'] or 'N/A'}` |"
        )
    lines += [
        "",
        "## 使用限制",
        "",
        "1. `candidate_unverified` 只用于检索和人工比对；不能写入 `official_verified`。",
        "2. `scoring_status=not_available_as_official` 固定不变，直到独立评分标准、发布主体、定位和复核回执同时具备。",
        "3. 长片段、题干与解析混入、OCR 异文和答案与评分点不分离的记录，必须先进入人工清洗队列。",
        "4. 在题文—答案/评分—教材 KP 三方证据闭合前，映射继续保持 `M0 / kp_id=N/A`。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| 执行脚本 | `scripts/extract_exam_answer_candidates.py` |",
        "| 审计总表 | `work/knowledge/_meta/exam_answer_scoring_audit_20260809.json` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=OUT_REPORT)
    args = parser.parse_args()
    bases = sorted(path for path in EXTRACT.iterdir() if path.is_dir())
    reports = [process_exam(base) for base in bases]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render_report(reports), encoding="utf-8")
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
