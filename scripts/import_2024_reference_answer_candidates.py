#!/usr/bin/env python3
"""Register the partial 2024 reference answer PDF as an unverified layer.

The reference PDF is a third-party/web-rendered artifact and only contains
Q1--Q9 in the local MinerU output.  This script deliberately does not alter
the main 2024 answer_index.jsonl (whose 22 rows remain missing), and does not
grant official or scoring authority.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "Data/reference/gaokao/pdf/2024/2024_NCA_answer.pdf"
SOURCE_MD = ROOT / "Data/reference/gaokao/mineru_result/2024_NCA_answer/full.md"
OUT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/reference_answer_candidates.jsonl"
REPORT = ROOT / "work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2024.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_2024_20260809.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    raw = SOURCE_MD.read_text(encoding="utf-8")
    source_pdf_sha = sha_bytes(SOURCE_PDF.read_bytes())
    source_md_sha = sha(raw)
    g1 = re.search(r"【1\\~3题答案】.*?(?=## \(二）)", raw, re.S)
    g2 = re.search(r"## \(二）.*?【4\\~6题答案】.*?(?=## \(三\))", raw, re.S)
    g3 = re.search(r"## \(三\).*?【7\\~9题答案】.*?(?=## 二、)", raw, re.S)
    if not (g1 and g2 and g3):
        raise SystemExit("2024 reference answer groups Q1-Q9 not found")
    groups = {"Q1-Q3": g1.group(0), "Q4-Q6": g2.group(0), "Q7-Q9": g3.group(0)}
    answer_texts = {
        1: "C",
        2: "D",
        3: "B",
        4: "C",
        5: "①. 原柱 ②. 新柱 ③. 假柱",
        6: "①新柱如果没有原位替换原柱，可能会改变建筑原结构的受力和传力方式，影响整体的稳定性；\n②太和殿是中国最大的木构大殿，建造之初工匠们应该经过了精心的测量，原位替换才是最佳的解决方案\n③太和殿的修缮加固追求最大程度地保持文物原貌，节省工料不是优先考虑的因素",
        7: "D",
        8: "①面对生活的困境，有人经不起打击而败退，有人则迎难而上，开始了新生；②虽然前行艰难，但也要凭借坚韧和勇气勇敢踏上征程，寻找属于自己的新生活；③此句表达了作者在乌乡霜降夜的所见所感，表达了对生命坚韧精神的深刻理解，对乌乡人的赞美。",
        9: "①自然景象的描写中渗透着独特的生命感受：文章开头描写了乌乡清晨的霜景，草叶上的霜、萧条的桦树、寒星的隐逝、农家炊烟等细节，写出了霜降节气中自然的变化；通过写作者感受到风中对的含义，闻得到风中独特的味道，写出了生命的独特感受。②人与自然的互动：作者与农户们在院子里攀谈、品尝当地食物，展示了人与自然的密切联系；作者还写了霜降夜的景物变化与感受到的寒意，写了房东阿姨送毯子，谈论过冬的准备等细节，展现了乌乡人对节气的重视以及应对节气的方法，写出人与节气之间密切的关联。③情感的共鸣：作者在霜降夜中感受到乌乡人对生活的积极态度和对幸福的追求，产生了强烈的情感共鸣。特别是最后看到房东阿姨的小儿子离乡远行，作者感受到生命的流动和时间的变迁，进一步深化了对生命与节气之间联系的体验。",
    }
    group_for = {1: groups["Q1-Q3"], 2: groups["Q1-Q3"], 3: groups["Q1-Q3"], 4: groups["Q4-Q6"], 5: groups["Q4-Q6"], 6: groups["Q4-Q6"], 7: groups["Q7-Q9"], 8: groups["Q7-Q9"], 9: groups["Q7-Q9"]}
    rows = []
    for qid in range(1, 10):
        text = answer_texts[qid]
        rows.append({
            "schema_version": "exam-reference-answer-candidate-0.1",
            "candidate_id": f"GK-NCA-2024-Q{qid:03d}-REFERENCE-ANSWER",
            "exam_id": "GK-NCA-2024",
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified",
            "candidate_scope": "partial_q1_q9_only",
            "source_authority_status": "unverified_local_provided",
            "source_registry_id": "SRC-GK-2024-NCA-ANSWER",
            "source_status": "unverified_local_provided",
            "answer_source_status": "external_partial_candidate",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "answer_candidate_text": text,
            "answer_candidate_sha256": sha(text),
            "source_group_excerpt": group_for[qid],
            "source_group_excerpt_sha256": sha(group_for[qid]),
            "source_pdf": rel(SOURCE_PDF),
            "source_pdf_sha256": source_pdf_sha,
            "source_mineru_md": rel(SOURCE_MD),
            "source_mineru_md_sha256": source_md_sha,
            "source_reference_html": "Data/reference/gaokao/html/2024/answer.html",
            "source_answer_index": "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/answer_index.jsonl",
            "review_status": "needs_independent_review",
            "notes": [
                "中国教育在线网页渲染答案 PDF；registry authenticity_status=unverified。",
                "本地 MinerU full.md 只覆盖 Q1-Q9；Q10-Q22 仍缺失。",
                "不得将本候选层写回主 answer_index 或标记 official_verified。",
            ],
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.1"\n'
        'status: "candidate_only_partial"\n'
        'authority_status: "unverified_local_provided"\n'
        'coverage: "GK-NCA-2024 Q1-Q9 only"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2024 全国甲卷参考答案候选（部分）\n\n"
        "> 来源为中国教育在线网页渲染 PDF，登记状态为 `unverified`；该外部参考 PDF 的本地 MinerU 结果只有 Q1—Q9。另有一份从考试解析卷恢复的本地候选层，覆盖 Q1—Q22，但仍未核验。该层不改变主答案索引的 22 条 `missing`，不提供官方评分标准。\n\n"
        f"- 派生记录：9 条（Q1—Q9）；Q10—Q22：仍缺失。\n- PDF：`{rel(SOURCE_PDF)}`，SHA-256 `{source_pdf_sha}`。\n- MinerU：`{rel(SOURCE_MD)}`，SHA-256 `{source_md_sha}`。\n- 派生 JSONL：`{rel(OUT)}`。\n- 本地解析卷全量候选：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/reference_answer_candidates_local_analysis.jsonl`。\n- 本地解析卷候选报告：`work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2024-LOCAL-ANALYSIS.md`。\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.1",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-NCA-2024-20260809",
        "exam_id": "GK-NCA-2024",
        "source_registry_id": "SRC-GK-2024-NCA-ANSWER",
        "source_authority_status": "unverified_local_provided",
        "coverage": {"candidate_questions": list(range(1, 10)), "missing_questions": list(range(10, 23))},
        "output": rel(OUT),
        "output_sha256": sha_bytes(OUT.read_bytes()),
        "report": rel(REPORT),
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
