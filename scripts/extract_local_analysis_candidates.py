#!/usr/bin/env python3
"""Extract a separate, non-authoritative candidate layer from local analysis segments.

The 2013 Sichuan analysis PDF contains answer/analysis text, but the separately
registered answer artifact is unavailable.  This script therefore creates a
reversible *local-analysis-only* derivative without changing the answer index,
answer-source status, scoring status, or M0 mapping fields.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from extract_exam_answer_candidates import extract_candidate

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract"
DEFAULT_EXAM_ID = "GK-SC-2013"
DEFAULT_REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-LOCAL-ANALYSIS-CANDIDATES-20260809.md"
DEFAULT_RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_answer_GK-SC-2013_local_analysis_candidates_20260809.json"


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf'(?m)^{re.escape(key)}:\s*(?:"([^"]*)"|([^\n]+))$', text)
    if not match:
        return None
    return (match.group(1) or match.group(2) or "").strip()


def segment_body(text: str) -> str:
    """Return only the derived segment body, excluding frontmatter and links."""
    first = text.split("\n---\n\n", 1)
    if len(first) != 2:
        raise ValueError("segment missing frontmatter/body separator")
    after_links = first[1]
    second = after_links.find("\n---\n\n")
    if second < 0:
        raise ValueError("segment missing provenance/body separator")
    body = after_links[second + len("\n---\n\n"):].strip()
    return body


def extract_local_candidate(text: str) -> tuple[str, str, list[str]]:
    """Handle both plain and MinerU-preserved ``【答案】`` markers."""
    matches = list(re.finditer(
        r"(?:^|\n)\s*(?:#+\s*)?(?:【\s*(?:参考)?答案\s*】|(?:参考)?答案)\s*[:：]?\s*",
        text,
    ))
    if not matches:
        candidate, method, notes = extract_candidate(text)
        return candidate, method, notes
    tail = text[matches[-1].end():]
    ends = []
    for pattern in (
        r"\n\s*【\s*(?:点评|解析|分析)\s*】",
        r"\n\s*##\s+",
    ):
        found = re.search(pattern, tail)
        if found:
            ends.append(found.start())
    end = min(ends) if ends else len(tail)
    candidate = tail[:end].strip()
    if not candidate:
        return "", "explicit_answer_marker_empty", ["explicit_answer_marker_empty"]
    notes = ["exact_excerpt_from_local_analysis_answer_marker", "candidate_unverified"]
    return candidate, "local_analysis_answer_marker", notes


def process_exam(exam_id: str, output: Path, report: Path, receipt: Path) -> dict[str, object]:
    base = EXTRACT / exam_id
    segdir = base / "segments/analysis"
    paths = sorted(segdir.glob("Q*.md"))
    if not paths:
        raise FileNotFoundError(f"no analysis segments: {segdir}")
    rows: list[dict[str, object]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        body = segment_body(text)
        candidate, method, notes = extract_local_candidate(body)
        if method in {"raw_answer_field_unbounded", "none"}:
            candidate_status = "candidate_mixed_analysis"
            candidate_kind = "analysis_excerpt_without_explicit_answer_marker"
            analysis_text = body
            answer_candidate = ""
        elif candidate:
            candidate_status = "candidate_unverified"
            candidate_kind = "answer_excerpt_from_local_analysis"
            analysis_text = None
            answer_candidate = candidate
        else:
            candidate_status = "missing"
            candidate_kind = "none"
            analysis_text = body
            answer_candidate = ""
        row = {
            "schema_version": "exam-local-analysis-candidate-0.1",
            "candidate_id": f"{exam_id}-{path.stem}-LOCAL-ANALYSIS",
            "exam_id": exam_id,
            "question_id": int(path.stem[1:]),
            "source_role": "answer_scoring_candidate",
            "candidate_status": candidate_status,
            "candidate_kind": candidate_kind,
            "candidate_extraction_method": method,
            "candidate_text": answer_candidate,
            "candidate_text_sha256": sha256_text(answer_candidate) if answer_candidate else None,
            "analysis_excerpt": analysis_text,
            "analysis_excerpt_sha256": sha256_text(analysis_text) if analysis_text else None,
            "source_authority_status": "unverified_local_provided",
            "answer_source_status": "missing_separate_answer_bundle",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "source_analysis_segment": str(path.relative_to(ROOT)),
            "source_analysis_pdf": frontmatter_value(text, "source_pdf"),
            "source_analysis_mineru_md": frontmatter_value(text, "source_mineru_md"),
            "source_clean_md": frontmatter_value(text, "source_clean_md"),
            "source_segment_clean_sha256": frontmatter_value(text, "segment_clean_sha256"),
            "source_segment_file_sha256": sha256_file(path),
            "source_answer_bundle": str((base / "answers/answer_bundle.md").relative_to(ROOT)),
            "source_answer_index": str((base / "answers/answer_index.jsonl").relative_to(ROOT)),
            "review_status": "needs_manual_review",
            "notes": [
                "解析卷仅作为本地候选，不是独立答案或评分材料。",
                "原始解析段、题卷和 PDF 保持双链；不修改 source/prompt_text_raw。",
                *notes,
            ],
        }
        rows.append(row)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row["candidate_status"])
        counts[key] = counts.get(key, 0) + 1
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render_report(exam_id, output, rows, counts), encoding="utf-8")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps({
        "schema_version": "exam-local-analysis-candidate-receipt-0.1",
        "receipt_id": f"EXAM-ANSWER-{exam_id}-LOCAL-ANALYSIS-20260809",
        "generated_at": now_text(),
        "exam_id": exam_id,
        "status": "candidate_only",
        "source_authority_status": "unverified_local_provided",
        "answer_source_status": "missing_separate_answer_bundle",
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "rows": len(rows),
        "candidate_status_counts": counts,
        "output": str(output.relative_to(ROOT)),
        "output_sha256": sha256_file(output),
        "report": str(report.relative_to(ROOT)),
        "policy": "仅用于检索和人工比对；不得升级为官方答案、评分标准或 M1+ 映射。",
        "raw_source_mutation": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {
        "exam_id": exam_id,
        "rows": len(rows),
        "candidate_status_counts": counts,
        "output": str(output.relative_to(ROOT)),
        "output_sha256": sha256_file(output),
        "report": str(report.relative_to(ROOT)),
        "receipt": str(receipt.relative_to(ROOT)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def render_report(exam_id: str, output: Path, rows: list[dict[str, object]], counts: dict[str, int]) -> str:
    lines = [
        "---",
        'schema_version: "exam-local-analysis-candidate-0.1"',
        'status: "candidate_only"',
        'answer_source_status: "missing_separate_answer_bundle"',
        'scoring_status: "not_available_as_official"',
        'mapping_status: "M0 | kp_id=N/A"',
        "---",
        "",
        f"# {exam_id} 本地解析候选层",
        "",
        "> 该层从解析卷题目段提取可定位候选片段。解析卷不是独立答案/评分材料；本层不改变原答案索引，不提供官方性结论，也不升级教材映射。",
        "",
        f"- 题目段：{len(rows)}；明确答案片段：{counts.get('candidate_unverified', 0)}；混合题干/解析候选：{counts.get('candidate_mixed_analysis', 0)}；空缺：{counts.get('missing', 0)}。",
        f"- 派生 JSONL：`{output.relative_to(ROOT)}`。",
        "- 所有记录保留解析段路径、PDF/MinerU/清洗稿链路、源段哈希和候选文本哈希。",
        "",
        "## 使用边界",
        "",
        "1. `candidate_unverified` 只表示解析段存在显式答案片段，不等于官方答案。",
        "2. `candidate_mixed_analysis` 可能混入题干、解析或学科网考点定位，必须人工分离。",
        "3. 独立答案/评分源缺失时，原 `answer_source_status` 继续为 `missing`；评分状态固定 `not_available_as_official`。",
        "4. 题文—答案/评分—教材 KP 三方证据闭合前，所有映射保持 `M0 / kp_id=N/A`。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exam-id", default=DEFAULT_EXAM_ID)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    args = parser.parse_args()
    # Normalize caller-supplied paths before rendering relative provenance
    # links.  This keeps the CLI safe for both relative and absolute paths.
    output = (args.output or (EXTRACT / args.exam_id / "answers/local_analysis_candidates.jsonl")).resolve()
    report = args.report.resolve()
    receipt = args.receipt.resolve()
    process_exam(args.exam_id, output, report, receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
