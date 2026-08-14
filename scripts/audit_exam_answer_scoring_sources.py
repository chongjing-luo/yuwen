#!/usr/bin/env python3
"""Audit answer and scoring provenance for the 2008--2024 exam corpus.

The audit is deliberately conservative.  A local ``解析卷`` can supply a
candidate answer, but it is not an official answer key or scoring rubric.
This script reads derived answer indexes only; PDFs, MinerU ``full.md`` files,
and cleaned source files are never modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Data" / "2008-2024·（四川）语文高考真题"
EXTRACT = CORPUS / "exam_extract"
SLICE_DIR = ROOT / "work/knowledge/高考分析"
REGISTRY_DIR = ROOT / "Data/reference/gaokao/registry"
OUT_JSON = ROOT / "work/knowledge/_meta/exam_answer_scoring_audit_20260809.json"
OUT_MD = ROOT / "work/knowledge/高考分析/EXAM-ANSWER-SCORING-AUDIT-20260809.md"

EXPECTED = {
    **{y: 21 for y in range(2008, 2016)},
    **{y: 12 for y in range(2016, 2018)},
    **{y: 10 for y in range(2018, 2021)},
    **{y: 22 for y in range(2021, 2025)},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{lineno}: expected object")
        rows.append(row)
    return rows


def external_candidate_sources() -> list[dict]:
    """Return third-party candidate sources registered outside main indexes."""
    return [
        row for row in read_jsonl(REGISTRY_DIR / "sources.jsonl")
        if row.get("source_kind") == "gaokao_answer_candidate"
    ]


def exam_id(year: int) -> str:
    if year <= 2015:
        return f"GK-SC-{year}"
    if year <= 2020:
        return f"GK-NC3-{year}"
    return f"GK-NCA-{year}"


def classify_row(row: dict, *, index_present: bool) -> tuple[str, list[str]]:
    """Return an audit status and evidence flags for one indexed question."""
    flags: list[str] = []
    text = (row.get("answer_text") or "").strip()
    source_status = row.get("source_status")
    answer_status = row.get("answer_status")
    if not index_present:
        return "missing_source", ["answer_index_absent"]
    if answer_status == "official_verified" or source_status == "official_verified":
        # This state is intentionally not accepted merely because a producer
        # wrote the string.  The current corpus has no independent authority
        # receipt, so it is reported as a conflict for manual adjudication.
        flags.append("official_label_without_independent_authority_receipt")
        return "conflict", flags
    if answer_status == "missing" or source_status == "missing" or not text:
        if not text:
            flags.append("answer_text_empty")
        if answer_status == "missing" or source_status == "missing":
            flags.append("explicit_missing_status")
        return "missing_source", flags
    if source_status != "unverified_local_provided":
        flags.append(f"unexpected_source_status:{source_status}")
    # A candidate may be a bare option or a long explanation.  Both remain
    # unverified; the shape is useful for deciding what to clean next.
    if any(marker in text for marker in ("【分析】", "【解答】", "【解析】", "答案：", "答案:")):
        flags.append("mixed_question_analysis_text")
        return "candidate_mixed_analysis", flags
    flags.append("candidate_text_present")
    return "candidate_answer_only_or_short", flags


def audit_year(year: int) -> dict:
    eid = exam_id(year)
    base = EXTRACT / eid
    expected = EXPECTED[year]
    index = base / "answers" / "answer_index.jsonl"
    bundle = base / "answers" / "answer_bundle.md"
    index_present = index.exists()
    rows = read_jsonl(index)
    errors: list[str] = []
    warnings: list[str] = []
    if index_present and len(rows) != expected:
        errors.append(f"index_rows={len(rows)} expected={expected}")
    if index_present:
        ids = sorted(int(r.get("question_id")) for r in rows if str(r.get("question_id", "")).isdigit())
        if ids != list(range(1, expected + 1)):
            errors.append(f"index_question_ids={ids} expected=1..{expected}")
    if index_present != bundle.exists():
        errors.append(f"bundle/index_pair_mismatch bundle={bundle.exists()} index={index_present}")
    if bundle.exists():
        bundle_hash = sha256(bundle)
    else:
        bundle_hash = None
    statuses: Counter[str] = Counter()
    flags: Counter[str] = Counter()
    audited_rows: list[dict] = []
    for row in rows:
        status, row_flags = classify_row(row, index_present=index_present)
        statuses[status] += 1
        flags.update(row_flags)
        source_pdf = row.get("source_pdf")
        source_md = row.get("source_mineru_md")
        source_checks = {
            "source_pdf_exists": bool(source_pdf and (ROOT / source_pdf).exists()),
            "source_mineru_md_exists": bool(source_md and (ROOT / source_md).exists()),
        }
        if index_present and not source_checks["source_pdf_exists"] and status.startswith("candidate"):
            warnings.append(f"Q{row.get('question_id')}: source PDF missing")
        if index_present and not source_checks["source_mineru_md_exists"] and status.startswith("candidate"):
            warnings.append(f"Q{row.get('question_id')}: source MinerU full.md missing")
        audited_rows.append({
            "question_id": row.get("question_id"),
            "audit_status": status,
            "answer_status": row.get("answer_status"),
            "source_status": row.get("source_status"),
            "scoring_status": "not_available_as_official",
            "source_checks": source_checks,
            "flags": row_flags,
        })
    if not index_present:
        statuses["missing_source"] = expected
        flags["answer_index_absent"] = expected
        warnings.append("no answer bundle/index; all questions remain missing for answer/scoring purposes")
    # Even a complete candidate index does not prove scoring availability.
    if any(s.startswith("candidate") for s in statuses):
        warnings.append("candidate answer text is not an official key and carries no verified scoring rubric")
    vertical_path = SLICE_DIR / f"{eid}-response_nodes_vertical_slice.jsonl"
    vertical_rows = read_jsonl(vertical_path)
    vertical_candidate = sum(1 for row in vertical_rows if row.get("answer_source_status") == "candidate_unverified")
    vertical_missing = sum(1 for row in vertical_rows if row.get("answer_source_status") == "missing")
    return {
        "exam_id": eid,
        "year": year,
        "expected_question_count": expected,
        "answer_bundle_present": bundle.exists(),
        "answer_index_present": index_present,
        "answer_bundle_sha256": bundle_hash,
        "index_row_count": len(rows),
        "vertical_slice_node_count": len(vertical_rows),
        "vertical_candidate_source_count": vertical_candidate,
        "vertical_missing_source_count": vertical_missing,
        "status_counts": dict(sorted(statuses.items())),
        "flag_counts": dict(sorted(flags.items())),
        "scoring_status": "not_available_as_official",
        "rows": audited_rows,
        "errors": errors,
        "warnings": warnings,
        "result": "failed" if errors else "passed_with_gaps",
    }


def build_audit() -> dict:
    years = [audit_year(year) for year in sorted(EXPECTED)]
    total = Counter()
    for report in years:
        total.update(report["status_counts"])
    vertical_nodes = sum(report["vertical_slice_node_count"] for report in years)
    vertical_candidate = sum(report["vertical_candidate_source_count"] for report in years)
    vertical_missing = sum(report["vertical_missing_source_count"] for report in years)
    external_sources = external_candidate_sources()
    return {
        "schema_version": "exam-answer-scoring-audit-0.1",
        "audit_id": "EXAM-ANSWER-SCORING-2008-2024-20260809",
        "corpus": "Data/2008-2024·（四川）语文高考真题",
        "policy": {
            "official_claim_requires": [
                "independent publisher or examination-authority provenance",
                "stable source locator",
                "answer/scoring artifact separated from question paper",
                "independent review receipt",
            ],
            "current_corpus_default": "candidate_unverified_or_missing",
            "scoring_default": "not_available_as_official",
            "raw_source_mutation": "forbidden",
        },
        "summary": {
            "years": len(years),
            "expected_questions": sum(EXPECTED.values()),
            "answer_bundles_present": sum(1 for r in years if r["answer_bundle_present"]),
            "answer_bundles_absent": sum(1 for r in years if not r["answer_bundle_present"]),
            "indexed_questions": sum(r["index_row_count"] for r in years),
            "vertical_slice_nodes": vertical_nodes,
            "vertical_candidate_source_nodes": vertical_candidate,
            "vertical_missing_source_nodes": vertical_missing,
            "status_counts": dict(sorted(total.items())),
            "official_verified_questions": total.get("official_verified", 0),
            "scoring_official_questions": 0,
            "external_candidate_sources": len(external_sources),
            "external_candidate_source_ids": [row.get("source_id") for row in external_sources],
        },
        "years": years,
    }


def render_markdown(audit: dict) -> str:
    summary = audit["summary"]
    lines = [
        "---",
        'schema_version: "exam-answer-scoring-audit-0.1"',
        'status: "passed_with_gaps"',
        'audit_id: "EXAM-ANSWER-SCORING-2008-2024-20260809"',
        'scoring_status: "not_available_as_official"',
        "---",
        "",
        "# 2008—2024 高考语文答案/评分来源审计",
        "",
        "> 本清单只审计派生答案索引，不修改原始 PDF、MinerU `full.md` 或清洗源。`candidate` 只表示本地解析文本可被检索，不表示官方答案；当前没有任何题目可以宣布具备官方评分标准。",
        "",
        "## 总结",
        "",
        f"- 覆盖 {summary['years']} 年、{summary['expected_questions']} 个顶层题目。",
        f"- bundle/index 层：有 bundle/index 的年份 {summary['answer_bundles_present']}，已索引题目 {summary['indexed_questions']}；其中候选答案文本 {summary['status_counts'].get('candidate_answer_only_or_short', 0) + summary['status_counts'].get('candidate_mixed_analysis', 0)}。",
        f"- 垂直切片层：{summary['vertical_slice_nodes']} 个作答节点中 {summary['vertical_candidate_source_nodes']} 个有本地解析候选，{summary['vertical_missing_source_nodes']} 个显式缺失。两层口径不同，不能互相替代。",
        f"- bundle/index 层缺失或空答案：{summary['status_counts'].get('missing_source', 0)}；官方核验：0。",
        f"- 独立第三方候选登记：{summary['external_candidate_sources']} 个 Source；不计入 bundle/index 答案覆盖，也不改变官方核验/评分计数。",
        "- 所有题目的 `scoring_status` 固定为 `not_available_as_official`，直到独立评分材料和复核回执闭合。",
        "",
        "## 年度清单",
        "",
        "| 年份/试卷 | 顶层题数 | bundle/index | bundle候选 | bundle缺失 | 垂直候选 | 垂直缺失 | 评分状态 |",
        "|---|---:|---|---:|---:|---:|---:|---|",
    ]
    for report in audit["years"]:
        counts = report["status_counts"]
        lines.append(
            f"| {report['exam_id']} | {report['expected_question_count']} | "
            f"{'有' if report['answer_bundle_present'] and report['answer_index_present'] else '缺失'} | "
            f"{counts.get('candidate_answer_only_or_short', 0) + counts.get('candidate_mixed_analysis', 0)} | "
            f"{counts.get('missing_source', 0)} | {report['vertical_candidate_source_count']} | "
            f"{report['vertical_missing_source_count']} | `not_available_as_official` |"
        )
    lines += [
        "",
        "## 状态解释",
        "",
        "- `candidate_answer_only_or_short`：索引中有非空答案片段，但来源仍是 `unverified_local_provided`。",
        "- `candidate_mixed_analysis`：答案字段混入题干、分析、解析或例文，不能直接当作干净答案/评分点。",
        "- `missing_source`：没有答案索引，或索引明确缺失/答案为空。",
        "- `conflict`：字段声称官方但没有独立权威来源回执；当前应退回人工核验。",
        "",
        "## 放行门槛",
        "",
        "1. 题干、答案、评分标准分离登记，分别有稳定定位。",
        "2. 来源发布主体/原始 URL 或考试机构文件可核验，并保留 SHA-256。",
        "3. 至少一次独立 PDF/页面复核；OCR 异文写入问题回执，不覆盖原文。",
        "4. 在上述三项及教材 KP 双向证据完成前，知识点节点保持 `M0 / kp_id=N/A`。",
        "",
        "## 下一批执行顺序",
        "",
        "0. GK-SC-2013 已完成新浪图像候选与本地解析候选逐题交叉比对；Q3/Q10/Q11/Q13 保持混合解析边界，Q16—Q20 保持差异复核，Q21 仍缺失。",
        "0.5. GK-NCA-2023 已登记中国教育在线 Q1—Q3、Q6—Q10 部分外部候选，并完成本地共享答案块切分与逐题比对；Q4/Q5/Q11—Q22 的外部缺失保持显式。",
        "0.75. GK-SC-2015 已登记高考网转载/新东方教研组 DOC 的 Q1—Q20 答案或作答指导候选；Q21 仅作文审题指导，所有记录仍是第三方候选。",
        "0.8. GK-SC-2014 已登记高考网/中学学科网带水印图 Q1—Q9 候选；Q10—Q18 的分页图失链，继续保持显式缺失。",
        "0.85. GK-SC-2012 高考网 RAR/DOC 已核验为题卷文本而非答案材料，登记为 blocked_no_answer_content，不生成候选层。",
        "0.9. GK-SC-2010 高考网 RAR/DOC 已登记 Q1、Q2、Q4、Q8、Q9 的明确答案标记候选；其余题号保持缺失，不由混合文本推断。",
        "1. 对 2009—2012、2014—2015、2021—2023 其余已有垂直解析候选的节点，补建独立候选索引；找不到评分源时保留显式缺失，不用搜索摘要替代。",
        "2. 对 2008、2016—2020 的候选文本做题号级清洗，保留原解析文本双链，并单独抽取 `answer_candidate`；不写入 `official_verified`。",
        "3. 2024 解析卷本地候选层已建立；Q8/Q9 圈码 OCR、Q12 选项冲突、Q16 重复答案串与 OCR 残片继续留在独立复核队列，不提升为官方答案。",
        "4. 只有答案/评分来源审计通过后，才进入教材 KP 三方证据闭合和 M1 以上映射。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| 机器审计 | `work/knowledge/_meta/exam_answer_scoring_audit_20260809.json` |",
        "| 本报告 | `work/knowledge/高考分析/EXAM-ANSWER-SCORING-AUDIT-20260809.md` |",
        "| 候选答案层 | `work/knowledge/高考分析/EXAM-ANSWER-CANDIDATE-EXTRACTION-20260809.md` |",
        "| 题型清洗队列 | `work/knowledge/高考分析/EXAM-TYPE-KP-REVIEW-QUEUE-20260809.md` |",
        "| 执行脚本 | `scripts/audit_exam_answer_scoring_sources.py` |",
        "| 2013 候选交叉比对 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidate_comparison.jsonl` |",
        "| 2013 比对报告 | `work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATE-COMPARISON-2013.md` |",
        "| 2013 比对验证 | `scripts/validate_2013_candidate_comparison.py` |",
        "| 2023 外部部分候选 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/reference_answer_candidates.jsonl` |",
        "| 2023 本地共享答案切分 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/local_analysis_group_candidates.jsonl` |",
        "| 2023 候选比对 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/reference_answer_candidate_comparison.jsonl` |",
        "| 2023 候选验证 | `scripts/validate_2023_candidate_comparison.py` |",
        "| 2015 外部候选 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/answers/reference_answer_candidates.jsonl` |",
        "| 2015 候选验证 | `scripts/validate_2015_reference_answer_candidates.py` |",
        "| 2014 外部部分候选 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/answers/reference_answer_candidates.jsonl` |",
        "| 2014 候选验证 | `scripts/validate_2014_reference_answer_candidates.py` |",
        "| 2010 外部部分候选 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/answers/reference_answer_candidates.jsonl` |",
        "| 2010 候选验证 | `scripts/validate_2010_reference_answer_candidates.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, default=OUT_JSON)
    parser.add_argument("--markdown", type=Path, default=OUT_MD)
    args = parser.parse_args()
    audit = build_audit()
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(render_markdown(audit), encoding="utf-8")
    print(json.dumps(audit["summary"], ensure_ascii=False, indent=2))
    return 1 if any(report["errors"] for report in audit["years"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
