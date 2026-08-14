#!/usr/bin/env python3
"""Validate calibration vertical-slice response nodes and score ledgers."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/knowledge/高考分析"
REPORT_DIR = ROOT / "work/knowledge/_meta/validation_reports"

SLICES = {
    "GK-SC-2008": {"questions": 21, "score": 150, "nodes": 24,
                   "choice_groups": {
                       "GK-SC-2008-Q013-OPTIONAL": {
                           "questions": [13], "raw_score_total": 10, "scored_score_total": 5,
                       },
                   }},
    "GK-SC-2013": {"questions": 21, "score": 150, "nodes": 23,
                   "choice_groups": {"GK-SC-2013-Q014-OPTIONAL": ([14], 6)}},
    "GK-NC3-2016": {"questions": 12, "score": 150, "nodes": 27,
                    "choice_groups": {"GK-NC3-2016-READING-CHOICE": ([5, 6], 1)}},
    "GK-NC3-2017": {"questions": 12, "score": 150, "nodes": 23,
                    "choice_groups": {}},
    "GK-NC3-2018": {"questions": 10, "score": 150, "nodes": 10,
                    "choice_groups": {}},
    "GK-NC3-2019": {"questions": 10, "score": 150, "nodes": 10,
                    "choice_groups": {}},
    "GK-NC3-2020": {"questions": 10, "score": 150, "nodes": 10,
                    "choice_groups": {}},
    "GK-NCA-2021": {"questions": 22, "score": 150, "nodes": 22,
                    "choice_groups": {}},
    "GK-NCA-2022": {"questions": 22, "score": 150, "nodes": 22,
                    "choice_groups": {}},
    "GK-NCA-2023": {"questions": 22, "score": 150, "nodes": 22,
                    "choice_groups": {}},
    "GK-NCA-2024": {"questions": 22, "score": 150, "nodes": 25,
                    "choice_groups": {}},
    "GK-SC-2009": {"questions": 21, "score": 150, "nodes": 24,
                    "choice_groups": {"GK-SC-2009-Q013-OPTIONAL": ([13, 13], 1)}},
    "GK-SC-2010": {"questions": 21, "score": 150, "nodes": 24,
                    "choice_groups": {"GK-SC-2010-Q013-OPTIONAL": ([13, 13], 1)}},
    "GK-SC-2011": {"questions": 21, "score": 150, "nodes": 24,
                    "choice_groups": {"GK-SC-2011-Q013-OPTIONAL": ([13, 13], 1)}},
    "GK-SC-2012": {"questions": 21, "score": 150, "nodes": 25,
                    "choice_groups": {"GK-SC-2012-Q013-OPTIONAL": ([13, 13], 1)}},
    "GK-SC-2014": {"questions": 21, "score": 150, "nodes": 22,
                    "choice_groups": {}},
    "GK-SC-2015": {"questions": 21, "score": 150, "nodes": 22,
                    "choice_groups": {}},
}

REQUIRED = [
    "response_node_id", "question_id", "subquestion_code", "prompt_text", "prompt_text_raw",
    "prompt_text_for_extraction", "prompt_cleaning_actions", "score",
    "source_question_segment", "source_pdf", "source_clean_md", "source_mineru_md",
    "source_pdf_page_index_start", "source_pdf_page_index_end", "source_locator_status",
    "locator_precision_note", "boundary_status", "ocr_status",
    "ability_action", "four_layer", "four_wings", "context_type", "atomic_exam_point",
    "answer_source_status", "evidence_ids", "decomposition_status", "kp_id",
    "mapping_level", "na_reason",
]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, object] = {}
    for exam_id, spec in SLICES.items():
        path = OUT / f"{exam_id}-response_nodes_vertical_slice.jsonl"
        if not path.exists():
            errors.append(f"{exam_id}: missing derived JSONL")
            continue
        rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        if len(rows) != spec["nodes"]:
            errors.append(f"{exam_id}: node count {len(rows)} != {spec['nodes']}")
        qids = sorted({int(r["question_id"]) for r in rows})
        if qids != list(range(1, spec["questions"] + 1)):
            errors.append(f"{exam_id}: question denominator {qids}")
        ids = [r.get("response_node_id") for r in rows]
        if len(ids) != len(set(ids)):
            errors.append(f"{exam_id}: duplicate response_node_id")
        for row in rows:
            rid = row.get("response_node_id", "?")
            for field in REQUIRED:
                if field not in row:
                    errors.append(f"{rid}: missing {field}")
            if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
                errors.append(f"{rid}: non-M0 mapping")
            if row.get("decomposition_status") != "response_nodes_derived":
                errors.append(f"{rid}: unexpected decomposition status")
            if __import__("re").search(r"##\s+[一二三四五六七八九十]+、", row.get("prompt_text", "")):
                errors.append(f"{rid}: next-section heading leaked into extraction prompt")
            pair = (int(row.get("question_id", -1)), row.get("subquestion_code"))
            # Check uniqueness below after collecting all pairs.
            if row.get("answer_source_status") == "missing":
                warnings.append(f"{rid}: answer source missing and explicitly marked")
            if row.get("boundary_status") == "boundary_trailing_heading":
                warnings.append(f"{rid}: trailing next-section heading was trimmed in extraction prompt")
            if row.get("ocr_status") == "suspected_ocr_or_watermark_noise":
                warnings.append(f"{rid}: suspected OCR/watermark noise retained or explicitly marked")
            if row.get("prompt_cleaning_actions"):
                warnings.extend(f"{rid}: {a}" for a in row["prompt_cleaning_actions"])
            for field in ("source_question_segment", "source_pdf", "source_clean_md", "source_mineru_md"):
                if row.get(field) and not (ROOT / row[field]).exists():
                    errors.append(f"{rid}: missing provenance file {field}")
            seg_path = ROOT / row["source_question_segment"]
            if seg_path.exists():
                seg_text = seg_path.read_text(encoding="utf-8")
                marker = 'segment_clean_sha256: "'
                if marker in seg_text:
                    expected_hash = seg_text.split(marker, 1)[1].split('"', 1)[0]
                    if expected_hash != row.get("segment_clean_sha256"):
                        errors.append(f"{rid}: segment_clean_sha256 mismatch with frontmatter")
            if not row.get("source_block_ids"):
                errors.append(f"{rid}: empty source_block_ids")
        pairs = [(int(r.get("question_id", -1)), r.get("subquestion_code")) for r in rows]
        if len(pairs) != len(set(pairs)):
            errors.append(f"{exam_id}: duplicate question_id+subquestion_code")
        raw_total = sum(int(r["score"]) for r in rows)
        adjusted = raw_total
        for gid, group_spec in spec["choice_groups"].items():
            explicit_totals = isinstance(group_spec, dict)
            if explicit_totals:
                questions = group_spec["questions"]
                raw_score_total = int(group_spec["raw_score_total"])
                scored_score_total = int(group_spec["scored_score_total"])
                scored_branches = None
            else:
                questions, scored_branches = group_spec
                raw_score_total = None
                scored_score_total = None
            branch_total = sum(int(r["score"]) for r in rows if r.get("choice_group_id") == gid)
            if branch_total == 0:
                errors.append(f"{exam_id}: choice group {gid} has no branch nodes")
            if explicit_totals:
                if branch_total != raw_score_total:
                    errors.append(f"{exam_id}: choice group {gid} raw score {branch_total} != {raw_score_total}")
                adjusted -= raw_score_total - scored_score_total
                continue
            # A single emitted node may already carry the aggregate score of
            # an internal "任选若干小题" group (e.g. 2013 Q14).  Only subtract
            # parallel branches when multiple scored branches are emitted.
            if len(questions) > 1:
                adjusted -= branch_total - branch_total * scored_branches // len(questions)
        if adjusted != spec["score"]:
            errors.append(f"{exam_id}: adjusted score {adjusted} != {spec['score']}")
        checks[exam_id] = {"node_count": len(rows), "raw_score_total": raw_total,
                           "adjusted_score_total": adjusted, "question_count": len(qids)}
    report = {"schema_version": "exam-vertical-slice-validation-0.1",
              "result": "passed" if not errors else "failed", "errors": errors,
              "warnings": warnings, "checks": checks}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / "exam_vertical_slices_validation.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
