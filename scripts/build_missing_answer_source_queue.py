#!/usr/bin/env python3
"""Build an auditable queue for vertical nodes with no answer source.

This queue is deliberately a *research/review* layer.  It does not promote
local analysis or third-party reprints into the main answer index, does not
create scoring standards, and does not change any exam source files.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM_ID = "GK-SC-2013"
VERTICAL = ROOT / "work/knowledge/exams/workbench/GK-SC-2013-response_nodes_vertical_slice.jsonl"
ANSWER_DIR = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers"
INDEX = ANSWER_DIR / "answer_index.jsonl"
LOCAL = ANSWER_DIR / "local_analysis_candidates.jsonl"
EXTERNAL = ANSWER_DIR / "reference_answer_candidates.jsonl"
COMPARISON = ANSWER_DIR / "reference_answer_candidate_comparison.jsonl"
OUT_JSONL = ROOT / "work/knowledge/exams/workbench/EXAM-MISSING-SOURCE-REVIEW-QUEUE-20260809.jsonl"
OUT_MD = ROOT / "work/knowledge/exams/workbench/EXAM-MISSING-SOURCE-REVIEW-QUEUE-20260809.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_missing_source_queue_20260809.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def candidate_map(rows: list[dict], id_key: str) -> dict[tuple[int, str], dict]:
    result: dict[tuple[int, str], dict] = {}
    for row in rows:
        qid = int(row.get("question_id", -1))
        if id_key == "local":
            sub = str(row.get("subquestion_code", "TOP"))
        else:
            sub = "TOP"
        result[(qid, sub)] = row
    return result


def main() -> int:
    required = [VERTICAL, INDEX, LOCAL, EXTERNAL, COMPARISON]
    missing = [rel(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("missing queue input(s): " + ", ".join(missing))

    vertical_rows = load_jsonl(VERTICAL)
    index_rows = load_jsonl(INDEX)
    local_rows = load_jsonl(LOCAL)
    external_rows = load_jsonl(EXTERNAL)
    comparison_rows = load_jsonl(COMPARISON)
    index_by_qid = {int(row["question_id"]): row for row in index_rows}
    local_by_qid = candidate_map(local_rows, "local")
    external_by_qid = {int(row["question_id"]): row for row in external_rows}
    comparison_by_qid = {int(row["question_id"]): row for row in comparison_rows}

    missing_nodes = [row for row in vertical_rows if row.get("answer_source_status") == "missing"]
    if len(missing_nodes) != 23:
        raise RuntimeError(f"expected 23 missing vertical nodes, found {len(missing_nodes)}")

    queue_rows: list[dict] = []
    for node in missing_nodes:
        node_id = node["response_node_id"]
        qid = int(node["question_id"])
        sub = str(node.get("subquestion_code", "TOP"))
        index = index_by_qid.get(qid, {})
        local = local_by_qid.get((qid, sub)) or local_by_qid.get((qid, "TOP"))
        external = external_by_qid.get(qid)
        comparison = comparison_by_qid.get(qid)
        queue_rows.append({
            "schema_version": "exam-missing-answer-source-queue-0.1",
            "queue_item_id": f"MISSING-SOURCE-{node_id}",
            "exam_id": EXAM_ID,
            "response_node_id": node_id,
            "question_id": qid,
            "subquestion_code": sub,
            "question_type_l1": node.get("question_type_l1"),
            "question_type_l2": node.get("question_type_l2"),
            "score": node.get("score"),
            "queue_status": "open_missing_authoritative_source",
            "current_answer_status": index.get("answer_status", "missing"),
            "current_source_status": index.get("source_status", "missing"),
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_layers": {
                "local_analysis_candidate": bool(local),
                "external_third_party_candidate": bool(external),
                "candidate_comparison": bool(comparison),
                "local_candidate_id": local.get("candidate_id") if local else None,
                "external_candidate_id": external.get("candidate_id") if external else None,
                "comparison_id": comparison.get("comparison_id") if comparison else None,
            },
            "required_next_evidence": [
                "可核验的考试机构/教育行政部门答案或评分材料，或可独立确认出处的原始发布物",
                "来源 URL/文件、发布主体、获取时间和 SHA-256",
                "逐题/逐小问边界复核；主观题须有评分点或明确标注评分材料缺失",
            ],
            "allowed_actions": [
                "检索官方站点、官方存档或可核验的原始发布物",
                "将第三方重印材料登记为 candidate_only 并保留快照与哈希",
                "对题卷、答案、评分材料分别建立双链和独立审查回执",
            ],
            "prohibited_actions": [
                "不得从本地解析、搜索摘要、教师指导或范文推断官方答案",
                "不得把 candidate 标为 official_verified",
                "不得把作文指导/示例答案当作评分标准",
                "不得修改原始 PDF、MinerU full.md、清洗原稿或主 answer_index.jsonl",
            ],
            "question_source": node.get("source_question_segment"),
            "analysis_source": node.get("source_analysis_segment"),
            "source_pdf": node.get("source_pdf"),
            "source_mineru_md": node.get("source_mineru_md"),
            "evidence_ids": node.get("evidence_ids", []),
            "review_status": "needs_independent_source_review",
            "notes": [
                "该节点属于 2013 四川卷垂直切片的显式缺失源；存在本地解析候选不代表答案/评分已核验。",
                "候选层与主 answer_index 分离；在三方证据闭合前保持 M0 / kp_id=N/A。",
            ],
        })

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in queue_rows) + "\n",
        encoding="utf-8",
    )
    lines = [
        "---",
        'schema_version: "exam-missing-answer-source-queue-0.1"',
        'status: "open_missing_authoritative_source"',
        f'exam_id: "{EXAM_ID}"',
        f'generated_at: "{now_text()}"',
        "authority_gate: `official_verified=0`",
        "scoring_gate: `not_available_as_official`",
        "mapping_gate: `M0 | kp_id=N/A`",
        "---",
        "",
        "# 2013 四川卷显式缺失答案/评分来源复核队列",
        "",
        "> 本队列只登记待检索节点，不补答案、不生成评分标准，不改变主答案索引。已有本地解析或第三方候选时，仍按 `candidate_only` 处理。",
        "",
        f"- 队列节点：`{len(queue_rows)}` 个垂直作答节点。",
        f"- 题目级范围：Q1—Q21；Q10、Q13 各含两个作答节点。",
        f"- JSONL：`{rel(OUT_JSONL)}`。",
        f"- 主答案索引：`{rel(INDEX)}`，保持显式 `missing`，不得回写。",
        "",
        "## 节点清单",
        "",
        "| 节点 | 题型 | 分值 | 本地候选 | 第三方候选 | 当前动作 |",
        "|---|---|---:|---|---|---|",
    ]
    for row in queue_rows:
        c = row["candidate_layers"]
        lines.append(
            f"| `{row['response_node_id']}` | `{row['question_type_l2']}` | {row['score']} | "
            f"{'有' if c['local_analysis_candidate'] else '无'} | "
            f"{'有' if c['external_third_party_candidate'] else '无'} | "
            "检索独立答案/评分材料；无可靠来源则保留 missing |"
        )
    lines.extend([
        "",
        "## 执行门禁",
        "",
        "1. 先确认发布主体、原始 URL/文件和来源快照，再建立候选记录。",
        "2. 客观题只可记录明确答案键；主观题必须区分示例答案、解析和评分点。",
        "3. 每条来源保留 SHA-256、题号边界、题卷双链和复核人/时间。",
        "4. 找不到权威答案或评分材料时，写明检索范围与缺失原因，继续保持 `missing`。",
        "5. 未完成题文—答案/评分—教材 KP 三方证据闭合和独立二审前，禁止 M1+ 映射。",
        "",
        "## 既有输入证据",
        "",
        f"- 垂直节点：`{rel(VERTICAL)}`（SHA-256 `{sha(VERTICAL)}`）。",
        f"- 主答案索引：`{rel(INDEX)}`（SHA-256 `{sha(INDEX)}`）。",
        f"- 本地候选：`{rel(LOCAL)}`（SHA-256 `{sha(LOCAL)}`）。",
        f"- 第三方候选：`{rel(EXTERNAL)}`（SHA-256 `{sha(EXTERNAL)}`）。",
        f"- 候选比对：`{rel(COMPARISON)}`（SHA-256 `{sha(COMPARISON)}`）。",
        "",
        "## 与主索引的关系",
        "",
        "本队列是下游检索任务，不是答案索引。任何新增来源必须先进入独立 registry 和候选 JSONL，经来源权威性审查后，才可讨论是否更新主索引；当前阶段不自动升级任何记录。",
        "",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    receipt = {
        "schema_version": "exam-missing-answer-source-queue-receipt-0.1",
        "receipt_id": "EXAM-MISSING-SOURCE-QUEUE-GK-SC-2013-20260809",
        "generated_at": now_text(),
        "exam_id": EXAM_ID,
        "queue_rows": len(queue_rows),
        "question_ids": sorted({row["question_id"] for row in queue_rows}),
        "response_node_ids": [row["response_node_id"] for row in queue_rows],
        "inputs": {rel(path): sha(path) for path in required},
        "outputs": {rel(OUT_JSONL): sha(OUT_JSONL), rel(OUT_MD): sha(OUT_MD)},
        "main_answer_index_mutation": False,
        "raw_source_mutation": False,
        "authority_gate": "official_verified=0",
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "队列只登记缺失源检索任务；不从本地解析、摘要、范文或教师指导推断答案/评分。",
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(queue_rows), "jsonl": rel(OUT_JSONL), "markdown": rel(OUT_MD), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
