#!/usr/bin/env python3
"""Audit the acquired Qiqiwenku preview for scope contamination.

This source is intentionally evaluated as a candidate and can be blocked even
when the preview is technically complete.  The audit never edits the primary
exam answer index.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "Data/reference/gaokao/external/2013_qiqiwenku_answer"
REGISTRY = ROOT / "Data/reference/gaokao/registry"
REVIEW_JSONL = EXTERNAL / "candidate_review.jsonl"
REVIEW_MD = ROOT / "work/knowledge/exams/workbench/EXAM-2013-QIQIWENKU-CANDIDATE-REVIEW-20260809.md"
SOURCE_ID = "SRC-GK-2013-SC-QIQIWENKU-ANSWER"
ARTIFACT_ID = "ART-GK-2013-SC-QIQIWENKU-ANSWER"
QUESTION_SOURCE_ID = "SRC-GK-2013-SC-QUESTION"


def now_cn() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_jsonl(path: Path, row: dict) -> None:
    rows = []
    if path.exists():
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    key = row.get("source_id") or row.get("artifact_id") or row.get("relation_id")
    id_key = "source_id" if "source_id" in row else "artifact_id" if "artifact_id" in row else "relation_id"
    if not any(r.get(id_key) == key for r in rows):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    manifest = json.loads((EXTERNAL / "acquisition_manifest.json").read_text(encoding="utf-8"))
    text = (EXTERNAL / "full_preview.txt").read_text(encoding="utf-8")
    markers = {
        "jiangsu_answer_heading": "语文（江苏卷）参考答案" in text,
        "jiangsu_supplement_heading": "语文Ⅱ（附加题）参考答案" in text,
        "questions_beyond_sichuan_scope": any(f"{n}．" in text for n in range(22, 30)),
    }
    # Objective keys visible in the contaminated answer block.  They are
    # recorded only as observations, never as Sichuan answer candidates.
    observed = {1: "D", 2: "A", 3: "C", 4: "B", 5: "B", 6: "D", 12: "D", 15: "B", 16: "C", 18: "C", 19: "B"}
    sina_path = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidates.jsonl"
    sina = {r["question_id"]: r for r in (json.loads(x) for x in sina_path.read_text(encoding="utf-8").splitlines()) if r.get("question_id")}
    disagreements = {
        str(q): {"observed": value, "existing_unverified_candidate": sina[q].get("answer_candidate_text")}
        for q, value in observed.items()
        if q in sina and (sina[q].get("answer_candidate_text") or "").strip().upper().rstrip(".") != value
    }
    review = {
        "schema_version": "exam-reference-answer-source-review-0.1",
        "review_id": "GK-SC-2013-QIQIWENKU-SCOPE-CONTAMINATION-20260809",
        "exam_id": "GK-SC-2013",
        "source_registry_id": SOURCE_ID,
        "artifact_id": ARTIFACT_ID,
        "candidate_status": "blocked_contaminated",
        "source_authority_status": "unverified_third_party_reprint",
        "answer_source_status": "candidate_source_contaminated",
        "scoring_status": "not_available_as_official",
        "mapping_level": "M0",
        "kp_id": "N/A",
        "review_status": "blocked_before_question_level_transcription",
        "reviewed_at": now_cn(),
        "source_snapshot": "Data/reference/gaokao/external/2013_qiqiwenku_answer/full_preview.pdf",
        "source_snapshot_sha256": sha256(EXTERNAL / "full_preview.pdf"),
        "markers": markers,
        "observed_objective_keys_not_for_use": observed,
        "disagreements_with_existing_unverified_candidates": disagreements,
        "decision": "Do not create question-level answer candidates; do not update main answer_index; do not create official scoring material.",
        "notes": [
            "预览共 29 页，技术上完整，但答案段明确标注为江苏卷，并含 22—29 附加题。",
            "2013 四川卷主结构到 Q21；跨卷答案段与既有四川候选出现可观测冲突。",
            "保留完整快照供人工核查，当前仅作污染来源审计证据。",
        ],
    }
    REVIEW_JSONL.write_text(json.dumps(review, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    registry_entry_path = EXTERNAL / "registry_entry.json"
    registry_entry = json.loads(registry_entry_path.read_text(encoding="utf-8"))
    registry_entry.update({
        "metadata_status": "acquired_unverified_candidate_partial",
        "status": "blocked_contaminated",
        "authenticity_status": "unverified_third_party_reprint",
        "review_artifact": "Data/reference/gaokao/external/2013_qiqiwenku_answer/candidate_review.jsonl",
        "contamination_reason": "answer heading is 江苏卷 and includes out-of-scope附加题 Q22-Q29",
        "main_answer_index_mutated": False,
    })
    registry_entry_path.write_text(json.dumps(registry_entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    source_row = {
        "canonical_artifact_id": ARTIFACT_ID,
        "copyright_note": "仅作内部研究；原始内容版权归发布方/命题机构所有",
        "document_role": "answer",
        "metadata_status": "acquired_unverified_candidate_partial",
        "publisher_or_channel": "360文库转链/齐齐文库",
        "scope": "2013四川卷候选（已发现答案段跨卷污染）",
        "source_id": SOURCE_ID,
        "source_kind": "gaokao_answer_candidate",
        "source_level": "S3",
        "title": "2013年四川高考语文试题答案（齐齐文库第三方预览；跨卷污染）",
    }
    artifact_row = {
        "acquired_at": manifest["acquired_at"],
        "artifact_id": ARTIFACT_ID,
        "artifact_role": "answer",
        "authenticity_status": "unverified_third_party_reprint",
        "byte_size": (EXTERNAL / "full_preview.pdf").stat().st_size,
        "carrier_type": "第三方网页渲染PDF/JSONP预览",
        "derived_from": "Data/reference/gaokao/external/2013_qiqiwenku_answer/partner_source.html",
        "error": "答案区明确标注江苏卷并出现Q22-Q29附加题；阻断题目级四川答案使用",
        "html_byte_size": (EXTERNAL / "source.html").stat().st_size,
        "html_sha256": sha256(EXTERNAL / "source.html"),
        "image_urls": [],
        "is_canonical": False,
        "local_path": "Data/reference/gaokao/external/2013_qiqiwenku_answer/full_preview.pdf",
        "mineru_full_md": None,
        "mineru_processed_at": None,
        "mineru_result_dir": None,
        "original_url": manifest["source_url"],
        "page_count": manifest["page_count"],
        "sha256": sha256(EXTERNAL / "full_preview.pdf"),
        "source_id": SOURCE_ID,
        "status": "acquired_unverified_candidate_partial",
        "transform": "360动态接口+齐齐文库JSONP预览；pdfunite合并，仅保留第三方快照",
    }
    relation_row = {
        "relation_id": "REL-GK-2013-SC-QIQIWENKU-ANSWER",
        "relation_status": "candidate_only",
        "relation_type": "answer_of",
        "source_id_from": SOURCE_ID,
        "source_id_to": QUESTION_SOURCE_ID,
    }
    append_jsonl(REGISTRY / "sources.jsonl", source_row)
    append_jsonl(REGISTRY / "artifacts.jsonl", artifact_row)
    append_jsonl(REGISTRY / "source_relations.jsonl", relation_row)

    REVIEW_MD.write_text(
        f"""---
schema_version: \"exam-reference-answer-source-review-0.1\"
status: \"blocked_contaminated\"
reviewed_at: \"{review['reviewed_at']}\"
---

# 2013 四川卷齐齐文库候选来源复核

- 快照：`{review['source_snapshot']}`（29 页，SHA-256 `{review['source_snapshot_sha256']}`）。
- 来源：360 文库转链 `{manifest['source_url']}`；合作页 `{manifest['partner_url']}`。
- 结论：阻断，不建立题目级答案候选，不修改主 `answer_index.jsonl`。

## 阻断证据

1. 答案段标题明确写作“语文（江苏卷）参考答案”。
2. 文档继续出现“语文Ⅱ（附加题）参考答案”及 Q22—Q29；2013 四川卷本题范围到 Q21。
3. 可见客观键与既有四川第三方候选发生冲突，不能把版面中的键归因于四川卷。

## 门禁

- `official_verified=0`；`scoring_status=not_available_as_official`。
- 保留 PDF、文本、HTML、分块哈希和复核 JSONL，仅用于后续人工追溯。
- 不从该材料提取知识点、不生成评分标准、不升级教材映射；继续保持 `M0 / kp_id=N/A`。
""",
        encoding="utf-8",
    )
    print(json.dumps({"review": str(REVIEW_JSONL), "status": review["candidate_status"], "disagreements": len(disagreements)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
