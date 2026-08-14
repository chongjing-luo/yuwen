#!/usr/bin/env python3
"""Derive conservative response-node slices for calibration review.

This script never edits source PDFs, MinerU full.md, clean_md, or the TOP
node ledger.  It emits slice-specific JSONL plus a review receipt.  Scores
are limited to the printed section totals visually checked in the source
PDFs; unresolved answer authority remains candidate_unverified/missing.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract"
OUT = ROOT / "work/knowledge/高考分析"
RECEIPTS = ROOT / "work/knowledge/_reviews/receipts"


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


CONFIG = {
    "GK-SC-2013": {
        "year": 2013, "paper_code": "SC", "expected_total": 150,
        "score": {**{q: 3 for q in range(1, 10)}, 10: 8, 11: 5, 12: 4,
                   13: 8, 14: 6, 15: 4, 16: 6, 17: 6, 18: 6,
                   19: 4, 20: 6, 21: 60},
        "split": {10: [("1", 4), ("2", 4)],
                  13: [("1", 4), ("2", 4)]},
        "optional": {14: {"branch_count": 8, "scored_branch_count": 6}},
        "visual_pages": [1, 2, 3, 4, 5, 6],
        "visual_notes": [
            "第I卷页眉列明一至三题分值为12、9、6；第II卷列明非选择题123分。",
            "Q10两句各4分，Q11 5分；Q12限划9处4分；Q13两问各4分；Q14限选6小题共6分。",
            "原卷存在可见水印，清洗稿与原卷保持双链，未改写原始内容。",
        ],
        "ocr_annotations": {
            14: "Q14 第(3)处出现孤立字符“Y”，疑为水印/OCR残片；不静默改写，待回看原卷留证。",
        },
    },
    "GK-NC3-2016": {
        "year": 2016, "paper_code": "NC3", "expected_total": 150,
        "score": {1: 9, 2: 19, 3: 11, 4: 6, 5: 25, 6: 25,
                   7: 3, 8: 3, 9: 3, 10: 5, 11: 6, 12: 60},
        "split": {
            1: [("1", 3), ("2", 3), ("3", 3)],
            2: [("1", 3), ("2", 3), ("3", 3), ("4-1", 5), ("4-2", 5)],
            3: [("1", 5), ("2", 6)],
            4: [("1", 2), ("2", 2), ("3", 2)],
            5: [("1", 5), ("2", 6), ("3", 6), ("4", 8)],
            6: [("1", 5), ("2", 6), ("3", 6), ("4", 8)],
        },
        # The source paper presents literary and practical text reading as
        # parallel 25-point alternatives; a candidate answers one branch.
        "choice_groups": [{"id": "GK-NC3-2016-READING-CHOICE",
                            "questions": [5, 6], "scored_branch_count": 1}],
        "visual_pages": [1, 3, 5, 6, 9, 12, 13, 14],
        "visual_notes": [
            "原卷页眉列明现代文9分、古诗文36分、文学类25分、语言文字运用20分、作文60分。",
            "Q2文言文19分由断句/常识/概括各3分与翻译两句各5分构成。",
            "Q5、Q6均按题面四个作答单元拆分；Q4三处默写各2分。",
            "原卷存在可见水印，图示题 Q11 保留原题段链接，不将图形内容臆补为文字。",
        ],
        "boundary_annotations": {
            5: "题段正文后带下一节标题“## 四、实用类文本阅读”；正文小问边界已截断，源段不改写。",
            6: "题段正文后带下一节标题“## 五、语言文字运用（20分）”；正文小问边界已截断，源段不改写。",
        },
        "ocr_annotations": {
            1: "Q1 选项 D 末尾含孤立字符“YY”，疑为水印/OCR 残片；PDF 视觉核对未见该字符，不静默改写。",
            5: "Q5 文本含“盯肴电杆”“在酒店挂伤”等疑似 OCR 词；不静默改写。",
            6: "Q6 标题/正文含“## ·代通儒顾炎武”“肇城志”“潘未”及选项末尾推广残片“🌙”；不静默改写。",
        },
        "material_annotations": [
            "MAT-2016-SC-04/05 继承题段尾/首下一节标题污染；现已建立 materials_clean/ 清洗副本并记录 OCR 修订，后续抽取仅使用副本，原始材料仍只读。",
        ],
        "image_annotations": {
            11: {
                "status": "available_in_mineru_source_unlinked",
                "path": "Data/2008-2024·（四川）语文高考真题/mineru_result/2016年高考语文试卷（新课标Ⅲ卷）（空白卷）/images/752f39a279c01b1d987448677a9c322c3cd7838c57e6e71ade7aa80dc614908d.jpg",
                "note": "题段保留图示 Markdown 链接；派生 segments/images 未复制该资源，使用源 MinerU 图片路径，禁止臆补图中文字。",
            }
        },
    },
    "GK-NCA-2024": {
        "year": 2024, "paper_code": "NCA", "expected_total": 150,
        "score": {1: 3, 2: 3, 3: 3, 4: 3, 5: 4, 6: 5, 7: 3, 8: 6,
                   9: 6, 10: 3, 11: 3, 12: 3, 13: 10, 14: 3, 15: 6,
                   16: 6, 17: 3, 18: 4, 19: 3, 20: 4, 21: 6, 22: 60},
        "split": {13: [("1", 5), ("2", 5)],
                  16: [("1", 2), ("2", 2), ("3", 2)]},
        "visual_pages": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "visual_notes": [
            "原卷首页明确满分150分；现代文36、古代诗文34、语言文字运用20、作文60。",
            "实用类文本12分按Q4 3分、Q5 4分、Q6 5分登记；该分配以题组总分与题面作答量为校准假设，待正式评分资料复核。",
            "Q13两句翻译各5分；Q16三组默写各2分；语言运用Q17-Q20按3/4/3/4分登记。",
            "原卷存在可见水印；解析 PDF 第17—20页含 Q21/Q22 的本地解析候选，第21页为推广页。候选内容不等于官方答案或评分标准。",
        ],
        "missing_answer_questions": [],
        "boundary_annotations": {
            6: "独立 PDF 复核：Q006 正文/解析止于实用类文本第6题；‘（三）文学类文本’及其后内容不属于 Q006。",
            9: "独立 PDF 复核：Q009 正文/解析止于文学类文本第9题；‘二、古代诗文阅读’及其后内容归入 Q010 起，不并入 Q009。",
            21: "题段正文后带下一节标题“## 四、作文（60分）”；正文小问边界已截断，源段不改写。",
        },
        "boundary_status_by_question": {
            6: "boundary_reviewed_trimmed",
            9: "boundary_reviewed_trimmed",
            21: "boundary_reviewed_trimmed",
        },
    },
    "GK-SC-2009": {
        "year": 2009, "paper_code": "SC", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-SC-2009_20260809.json",
        "score": {**{q: 3 for q in range(1, 11)}, 11: 10, 12: 8, 13: 5,
                   14: 4, 15: 4, 16: 8, 17: 6, 18: 6, 19: 4, 20: 5, 21: 60},
        "split": {11: [("1", 4), ("2", 6)], 12: [("1", 2), ("2", 6)], 13: [("1", 5), ("2", 5)]},
        "choice_groups": [{"id": "GK-SC-2009-Q013-OPTIONAL", "questions": [13, 13], "scored_branch_count": 1}],
        "prompt_source_question": {14: 17, 15: 17, 16: 17, 17: 17},
        "answer_source_question": {14: 17, 15: 17, 16: 17, 17: 17},
        "embedded_prompt_questions": [14, 15, 16, 17],
        "visual_check_status": "passed_with_source_label_conflict",
        "visual_pages": list(range(1, 10)),
        "visual_notes": [
            "2009 四川自主命题卷；已逐页核对第1—8页考试正文，第9页为资料广告页。PDF首页标题含‘解析’字样，文件名虽标‘空白卷’，来源标签冲突已显式登记。",
            "Q11 两句翻译 4/6 分，Q12 两问 2/6 分；Q13 两个名句分支任选一题。",
            "Q14—Q17 的题干集中出现在 Q17 题段；派生节点保留 canonical_question_segment 与 source_prompt_segment 双链。",
        ],
        "ocr_annotations": {
            13: "Q13 第二个名句分支末尾出现孤立字符“CC”，疑为 OCR/版面残片；不静默删除。",
        },
    },
    "GK-SC-2010": {
        "year": 2010, "paper_code": "SC", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-SC-2010_20260809.json",
        "score": {**{q: 3 for q in range(1, 11)}, 11: 10, 12: 8, 13: 5,
                   14: 4, 15: 6, 16: 6, 17: 6, 18: 5, 19: 6, 20: 4, 21: 60},
        "split": {11: [("1", 4), ("2", 6)], 12: [("1", 4), ("2", 4)], 13: [("1", 5), ("2", 5)]},
        "choice_groups": [{"id": "GK-SC-2010-Q013-OPTIONAL", "questions": [13, 13], "scored_branch_count": 1}],
        "visual_check_status": "passed_with_source_label_conflict",
        "visual_pages": list(range(1, 10)),
        "visual_notes": [
            "2010 四川自主命题卷；已逐页核对第1—8页考试正文，第9页为资料广告页。PDF首页标题含‘试题解析’字样，文件名虽标‘空白卷’，来源标签冲突已显式登记。",
            "Q11 两句翻译 4/6 分，Q12 两问 4/4 分；Q13 两个名句分支任选一题。",
            "第六大题合计 15 分，Q18/Q19/Q20 按 5/6/4 分登记；Q20 题段尾部带作文分节标题，清洗提示中截断。",
        ],
        "ocr_annotations": {
            14: "Q14 答题占位处保留孤立字符“Y”，疑为 OCR/水印残片；不静默删除。",
        },
    },
    "GK-SC-2011": {
        "year": 2011, "paper_code": "SC", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-SC-2011_20260809.json",
        "score": {**{q: 3 for q in range(1, 11)}, 11: 10, 12: 8, 13: 5,
                   14: 4, 15: 6, 16: 6, 17: 6, 18: 4, 19: 5, 20: 6, 21: 60},
        "split": {11: [("1", 5), ("2", 5)], 12: [("1", 3), ("2", 5)], 13: [("1", 5), ("2", 5)]},
        "choice_groups": [{"id": "GK-SC-2011-Q013-OPTIONAL", "questions": [13, 13], "scored_branch_count": 1}],
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 9)),
        "visual_notes": [
            "2011 四川自主命题卷；已逐页核对第1—7页考试正文，第8页为资料广告页。",
            "Q11 两句翻译 5/5 分，Q12 两问 3/5 分；Q13 两个名句分支任选一题。",
            "第六大题合计 15 分，Q18/Q19/Q20 按 4/5/6 分登记。",
        ],
        "ocr_annotations": {
            13: "Q13 第一分支末尾出现孤立字符“0”，疑为 OCR/版面残片；不静默删除。",
        },
    },
    "GK-SC-2012": {
        "year": 2012, "paper_code": "SC", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-SC-2012_20260809.json",
        "score": {**{q: 3 for q in range(1, 11)}, 11: 10, 12: 8, 13: 5,
                   14: 5, 15: 6, 16: 5, 17: 6, 18: 4, 19: 5, 20: 6, 21: 60},
        "split": {11: [("1", 3), ("2", 3), ("3", 4)], 12: [("1", 3), ("2", 5)], 13: [("1", 5), ("2", 5)]},
        "choice_groups": [{"id": "GK-SC-2012-Q013-OPTIONAL", "questions": [13, 13], "scored_branch_count": 1}],
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 8)),
        "visual_notes": [
            "2012 四川自主命题卷；已逐页核对第1—6页考试正文，第7页为资料广告页。",
            "Q11 三句翻译 3/3/4 分，Q12 两问 3/5 分；Q13 两个名句分支任选一题。",
            "Q14—Q17 文学阅读按 5/6/5/6 分登记，第六大题 Q18/Q19/Q20 按 4/5/6 分登记。",
        ],
        "ocr_annotations": {
            6: "Q6 题段中出现孤立字符“0.”，疑为 OCR/版面残片；不静默删除。",
        },
    },
    "GK-SC-2014": {
        "year": 2014, "paper_code": "SC", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-SC-2014_20260809.json",
        "score": {**{q: 3 for q in range(1, 10)}, 10: 8, 11: 5, 12: 4, 13: 8,
                   14: 6, 15: 4, 16: 6, 17: 6, 18: 6, 19: 4, 20: 6, 21: 60},
        "split": {13: [("1", 3), ("2", 5)]},
        "optional": {14: {"branch_count": 8, "scored_branch_count": 6}},
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 9)),
        "visual_notes": [
            "2014 四川自主命题卷；已逐页核对第1—7页考试正文，第8页为资料广告页。",
            "Q13 两问 3/5 分；Q14 限选 6 小题；Q15—Q18 文学阅读与开放题按题面分值登记。",
        ],
        "ocr_annotations": {
            15: "Q15 选项末尾出现孤立字符“人”，疑为 OCR/版面残片；不静默删除。",
        },
    },
    "GK-SC-2015": {
        "year": 2015, "paper_code": "SC", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-SC-2015_20260809.json",
        "score": {**{q: 3 for q in range(1, 10)}, 10: 8, 11: 5, 12: 4, 13: 8,
                   14: 6, 15: 4, 16: 6, 17: 6, 18: 6, 19: 4, 20: 6, 21: 60},
        "split": {13: [("1", 3), ("2", 5)]},
        "optional": {14: {"branch_count": 8, "scored_branch_count": 6}},
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 9)),
        "visual_notes": [
            "2015 四川自主命题卷；已逐页核对第1—7页考试正文，第8页为资料广告页。",
            "Q13 两问 3/5 分；Q14 限选 6 小题；Q15—Q18 文学阅读与开放题按题面分值登记。",
        ],
        "ocr_annotations": {
            15: "Q15 选项末尾出现孤立字符“K”，疑为 OCR/版面残片；不静默删除。",
        },
    },
    "GK-NC3-2017": {
        "year": 2017, "paper_code": "NC3", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-NC3-2017_20260809.json",
        "score": {1: 9, 2: 14, 3: 12, 4: 19, 5: 11, 6: 5,
                   7: 3, 8: 3, 9: 3, 10: 6, 11: 5, 12: 60},
        # Keep only explicitly stable scoring units.  Q6 remains one
        # five-point node because the OCR loses the individual blank markers.
        "split": {
            1: [("1", 3), ("2", 3), ("3", 3)],
            2: [("1", 3), ("2", 5), ("3", 6)],
            3: [("1", 3), ("2", 5), ("3", 4)],
            4: [("1", 3), ("2", 3), ("3", 3), ("4-1", 5), ("4-2", 5)],
            5: [("1", 5), ("2", 6)],
        },
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 15)),
        "visual_notes": [
            "2017 新课标Ⅲ卷；已对空白卷 14 页逐页完成高分辨率 PDF 视觉复核，原始 PDF、MinerU full.md 均保持只读。",
            "Q1 论述类 9 分；Q2 文学类 14 分；Q3 实用类 12 分；Q4 文言文 19 分；Q5 古诗 11 分；Q6 默写 5 分。",
            "Q4 翻译两句各 5 分；Q6 源卷可见 3+2 个空格，但清洗/OCR 文本未稳定保留空格对应的完整句段与独立评分依据，仍保留一个 5 分节点。",
            "Q3 材料二图表已与 PDF 视觉比对；节点保留 MinerU 图片源路径，未臆补图中文字或数值。",
            "Q1/Q3/Q9/Q11 的孤立字符仅出现在 OCR/版面派生文本中，PDF 卷面未见对应正文；派生提示继续保留可追溯清洗动作。",
            "Q11/Q12 的 MinerU block_ids 为空，使用 P13-PAGE-FALLBACK；不宣称题级 bbox 或精确块定位。",
        ],
        "ocr_annotations": {
            1: "Q1 题段末尾出现孤立“众 人”并黏连下一小问标记，疑为 OCR/排版污染；派生提示截断该残片，原始题段不改写。",
            3: "Q3 选项 C/D 末尾出现孤立字符“W”“A”，疑为 OCR/解析标记污染；派生提示移除孤立标记，原始题段不改写。",
            9: "Q9 选项 A 前出现孤立字符“V”，疑为 OCR/排版污染；派生提示移除该标记，原始题段不改写。",
            11: "Q11 题面②、③位置出现孤立字符“0”，疑为 OCR/水印残片；派生提示显式标记，原始题段不改写。",
        },
        "image_annotations": {
            3: {
                "status": "present_watermarked",
                "path": "Data/2008-2024·（四川）语文高考真题/mineru_result/2017年高考语文试卷（新课标Ⅲ卷）（空白卷）/images/bce37a2c1b6b97e6d117c73aa621d3ba5522afebe3fda692be139afcde0514f1.jpg",
                "note": "Q3 材料二图表来自 MinerU 图片资源；图中数值未在本批次臆补或转写，待 PDF 视觉复核。",
            },
        },
    },
    "GK-NC3-2018": {
        "year": 2018, "paper_code": "NC3", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-NC3-2018_20260809.json",
        # The 2018 source prints stable totals only at the question/group
        # level.  Q7's 20 points cover three language-use tasks without
        # independent printed scores, so keep all ten top-level nodes intact.
        "score": {1: 9, 2: 15, 3: 12, 4: 19, 5: 9, 6: 6, 7: 20, 8: 4, 9: 6, 10: 50},
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 16)),
        "visual_notes": [
            "2018 新课标Ⅲ卷；已对空白卷 15 页逐页完成高分辨率 PDF 视觉复核，考试正文为印刷第1—12页，PDF 第13—14页为空白水印页，第15页为广告页。",
            "卷面稳定总分为 Q1—Q10：9/15/12/19/9/6/20/4/6/50，共 150 分；Q7 的 20 分为语言文字运用题组总分，未将无独立印刷分值的三个小问虚拆。",
            "Q1 原始 OCR 中 BA/公/WD 等行间残片在 PDF 卷面不存在；Q5 小问末尾孤立‘1’在 PDF 卷面不存在，清洗稿保留双链与异常登记。",
            "Q3 材料二两幅图表已与 PDF 视觉比对；Q9 构思框架图已确认存在，节点保留 MinerU 图片源路径，不臆补图中文字。",
            "原始 PDF 各考试页可见资料站水印；水印、空白页与广告页不进入题文清洗正文。",
        ],
        "ocr_annotations": {
            1: "原始 exceptions 登记 BA/公/WD 等行间 OCR/水印残片；PDF 视觉核对未见对应正文，清洗副本保留异常记录，不改写原始 full.md。",
            5: "原始 exceptions 登记小问末尾孤立字符‘1’；PDF 视觉核对未见该字符，清洗副本已隔离该残片，原始 full.md 不改写。",
        },
        "image_annotations": {
            3: {
                "status": "present_watermarked",
                "path": "Data/2008-2024·（四川）语文高考真题/mineru_result/2018年高考语文试卷（新课标Ⅲ卷）（空白卷）/images/3476c9bf07a6885d47b8793dd3405fee6acaa484094871f035f9c456622f8640.jpg",
                "note": "Q3 材料二两幅图表来自 MinerU 图片资源（第二幅：images/7117c36df2c638d75a99e73c132d7bbc847c9b43dbea7c5cfea9162eeef94b27.jpg）；已与 PDF 视觉比对，未臆补图中文字或数值。",
            },
            9: {
                "status": "present_watermarked",
                "path": "Data/2008-2024·（四川）语文高考真题/mineru_result/2018年高考语文试卷（新课标Ⅲ卷）（空白卷）/images/55707b4432b95b256d9040b99d07b4240392ced4b15ece866723a71ebbc8a6dd.jpg",
                "note": "Q9 构思框架图已在 PDF 第12页视觉确认；保留 MinerU 图片源路径，不把图示臆转写为答案。",
            },
        },
    },
    "GK-NC3-2019": {
        "year": 2019, "paper_code": "NC3", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-NC3-2019_20260809.json",
        # Stable printed totals are available only at the top-level question
        # scale in this source; preserve the ten nodes until sub-score sources
        # are independently verified.
        "score": {1: 9, 2: 12, 3: 15, 4: 19, 5: 9, 6: 6, 7: 9, 8: 6, 9: 5, 10: 60},
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 14)),
        "visual_notes": [
            "2019 新课标Ⅲ卷；已对空白卷 13 页逐页完成高分辨率 PDF 视觉复核，考试正文为印刷第1—11页，PDF 第12页为空白水印页，第13页为广告页。",
            "卷面稳定总分为 Q1—Q10：9/12/15/19/9/6/9/6/5/60，共 150 分；当前保持十个顶层节点，不把未印独立小问分值的题组虚拆。",
            "Q1—Q9 题干、文言断句/翻译、诗歌与语言文字运用边界均与 PDF 一致，未发现需静默修正的题卷 OCR 残片。",
            "Q10 漫画材料已在 PDF 第11页确认，节点保留 MinerU 图片源路径，不臆补漫画文字或寓意答案。",
            "原始 PDF 考试页可见资料站水印；空白水印页与广告页不进入题文清洗正文。",
        ],
        "image_annotations": {
            10: {
                "status": "present_watermarked",
                "path": "Data/2008-2024·（四川）语文高考真题/mineru_result/2019年高考语文试卷（新课标Ⅲ卷）（空白卷）/images/2256fa9acb8a625276ee4047862cee4c30b0900e06c09c620b43077eef009438.jpg",
                "note": "Q10 漫画材料已在 PDF 第11页视觉确认；保留 MinerU 图片源路径，不将图像内容臆转写为答案。",
            },
        },
    },
    "GK-NC3-2020": {
        "year": 2020, "paper_code": "NC3", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-NC3-2020_20260809.json",
        "score": {1: 9, 2: 12, 3: 15, 4: 19, 5: 9, 6: 6, 7: 9, 8: 6, 9: 5, 10: 60},
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 14)),
        "visual_notes": [
            "2020 新课标Ⅲ卷；已对空白卷 13 页逐页完成高分辨率 PDF 视觉复核，考试正文为印刷第1—11页，PDF 第12页为空白水印页，第13页为广告页。",
            "卷面稳定总分为 Q1—Q10：9/12/15/19/9/6/9/6/5/60，共 150 分；当前保持十个顶层节点，不把未印独立小问分值的题组虚拆。",
            "Q8 题段开头派生 OCR 的孤立‘11’在 PDF 卷面不存在；清洗提示仅隔离该残片，原始 full.md 与清洗源段不改写。",
            "Q1—Q10 题干边界、默写空格、语言文字运用和作文材料均与 PDF 对齐；原始水印、空白页和广告页不进入题文清洗正文。",
        ],
        "ocr_annotations": {
            8: "Q8 题段开头出现孤立字符‘11’，疑为页码/OCR残片；PDF 视觉核对未见该字符，派生提示隔离，原始题段不改写。",
        },
    },
    "GK-NCA-2021": {
        "year": 2021, "paper_code": "NCA", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-NCA-2021_20260809.json",
        # The source prints reliable section totals.  The 12/15-point
        # reading groups have conventional question weights, but the paper
        # does not print independent scores beside every small question;
        # retain those allocations as candidates.  Language-use subgroups
        # are deliberately kept as aggregate totals (9 + 11) and are not
        # falsely split into per-question scores.
        "score": {1: 3, 2: 3, 3: 3, 4: 3, 5: 4, 6: 5,
                   7: 3, 8: 6, 9: 6, 10: 3, 11: 3, 12: 3,
                   13: 10, 14: 3, 15: 6, 16: 6,
                   17: 9, 18: 0, 19: 0, 20: 11, 21: 0, 22: 60},
        "score_groups": [
            {"id": "GK-NCA-2021-Q004-Q006", "questions": [4, 5, 6],
             "total": 12, "allocation": "candidate_3_4_5"},
            {"id": "GK-NCA-2021-Q007-Q009", "questions": [7, 8, 9],
             "total": 15, "allocation": "candidate_3_6_6"},
            {"id": "GK-NCA-2021-Q017-Q019", "questions": [17, 18, 19],
             "total": 9, "allocation": "aggregate_only", "lead_question": 17},
            {"id": "GK-NCA-2021-Q020-Q021", "questions": [20, 21],
             "total": 11, "allocation": "aggregate_only", "lead_question": 20},
        ],
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 12)),
        "visual_notes": [
            "2021 全国甲卷空白卷共11页；已逐页核对考试正文，PDF第10页为作文正文，第11页为广告页，不纳入题文。",
            "卷面分区总分稳定为现代文36、古代诗文34、语言文字运用20、作文60，共150分。",
            "实用类阅读Q4—Q6题组总分12，文学类阅读Q7—Q9题组总分15；采用3/4/5与3/6/6作为结构候选并显式标记，不宣称题面独立印刷分值。",
            "语言文字运用分为Q17—Q19（9分）与Q20—Q21（11分）；仅保留组总分，Q18/Q19/Q21节点记0分占位，禁止把0解释为正式小题分值。",
            "原始卷面可见水印；清洗稿仅去除下一节标题污染，原始PDF、MinerU full.md保持只读。",
        ],
        "score_notes": {
            "aggregate_only": "语言文字运用子组分值仅登记在组首节点；同组其余节点为结构占位(score=0)，不构成正式评分分配。",
            "candidate_allocation": "Q4—Q6、Q7—Q9的分配用于总分复算和检索排序，待正式评分资料核验。",
        },
    },
    "GK-NCA-2022": {
        "year": 2022, "paper_code": "NCA", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-NCA-2022_20260809.json",
        "score": {1: 3, 2: 3, 3: 3, 4: 3, 5: 4, 6: 5,
                   7: 3, 8: 6, 9: 6, 10: 3, 11: 3, 12: 3,
                   13: 10, 14: 3, 15: 6, 16: 6,
                   17: 11, 18: 0, 19: 0, 20: 9, 21: 0, 22: 60},
        "score_groups": [
            {"id": "GK-NCA-2022-Q004-Q006", "questions": [4, 5, 6],
             "total": 12, "allocation": "candidate_3_4_5"},
            {"id": "GK-NCA-2022-Q007-Q009", "questions": [7, 8, 9],
             "total": 15, "allocation": "candidate_3_6_6"},
            {"id": "GK-NCA-2022-Q017-Q019", "questions": [17, 18, 19],
             "total": 11, "allocation": "aggregate_only", "lead_question": 17},
            {"id": "GK-NCA-2022-Q020-Q021", "questions": [20, 21],
             "total": 9, "allocation": "aggregate_only", "lead_question": 20},
        ],
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 13)),
        "visual_notes": [
            "2022 全国甲卷空白卷共12页；考试正文为第1—10页，第11页为空白水印页，第12页为广告页。",
            "卷面分区总分稳定为现代文36、古代诗文34、语言文字运用20、作文60，共150分。",
            "实用类阅读Q4—Q6题组总分12，文学类阅读Q7—Q9题组总分15；采用3/4/5与3/6/6作为结构候选并显式标记。",
            "语言文字运用分为Q17—Q19（11分）与Q20—Q21（9分）；仅保留组总分，Q18/Q19/Q21节点记0分占位，禁止把0解释为正式小题分值。",
            "Q4图示已与PDF核对；原始水印、空白页和广告页不进入题文清洗正文。",
        ],
        "score_notes": {
            "aggregate_only": "语言文字运用子组分值仅登记在组首节点；同组其余节点为结构占位(score=0)，不构成正式评分分配。",
            "candidate_allocation": "Q4—Q6、Q7—Q9的分配用于总分复算和检索排序，待正式评分资料核验。",
        },
        "ocr_annotations": {
            2: "Q2选项B末尾出现孤立字符‘传V播’，疑为OCR/水印残片；不静默改写。",
            10: "Q10选项存在‘诺/诸’等OCR异文，保留清洗源原样，待独立来源复核。",
            13: "Q13译文题中‘日/曰’等OCR异文保留，不静默改写。",
        },
    },
    "GK-NCA-2023": {
        "year": 2023, "paper_code": "NCA", "expected_total": 150,
        "visual_review_receipt": "work/knowledge/_reviews/receipts/exam_visual_review_GK-NCA-2023_20260809.json",
        "score": {1: 3, 2: 3, 3: 3, 4: 3, 5: 4, 6: 5,
                   7: 3, 8: 6, 9: 6, 10: 3, 11: 3, 12: 4,
                   13: 9, 14: 3, 15: 6, 16: 6,
                   17: 20, 18: 0, 19: 0, 20: 0, 21: 0, 22: 60},
        "score_groups": [
            {"id": "GK-NCA-2023-Q004-Q006", "questions": [4, 5, 6],
             "total": 12, "allocation": "candidate_3_4_5"},
            {"id": "GK-NCA-2023-Q007-Q009", "questions": [7, 8, 9],
             "total": 15, "allocation": "candidate_3_6_6"},
            {"id": "GK-NCA-2023-Q010-Q013", "questions": [10, 11, 12, 13],
             "total": 19, "allocation": "candidate_3_3_4_9"},
            {"id": "GK-NCA-2023-Q017-Q021", "questions": [17, 18, 19, 20, 21],
             "total": 20, "allocation": "aggregate_only", "lead_question": 17},
        ],
        "visual_check_status": "passed",
        "visual_pages": list(range(1, 12)),
        "visual_notes": [
            "2023 全国甲卷空白卷共11页；考试正文为第1—8页，第9—10页为空白水印页，第11页为广告页。",
            "卷面分区总分按150分复核为现代文36、古代诗文34、语言文字运用20、作文60；但题面同时印有文言文20分与诗歌9分，产生1分算术冲突。为不静默修订，文言文小问暂登记3/3/4/9候选并保留冲突警告。",
            "实用类阅读Q4—Q6题组总分12，文学类阅读Q7—Q9题组总分15；采用3/4/5与3/6/6作为结构候选并显式标记。",
            "语言文字运用Q17—Q21统一为20分题组；仅保留组总分，Q18—Q21节点记0分占位，禁止把0解释为正式小题分值。",
            "原始水印、空白页和广告页不进入题文清洗正文；原始PDF、MinerU full.md保持只读。",
        ],
        "score_notes": {
            "aggregate_only": "语言文字运用题组分值仅登记在组首节点；同组其余节点为结构占位(score=0)，不构成正式评分分配。",
            "candidate_allocation": "阅读/文言小问的3/4/5、3/6/6、3/3/4/9分配用于总分复算和检索排序；2023卷面分区与题组标题存在1分冲突，待正式评分资料核验。",
        },
    },
}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalized_body(text: str) -> str:
    # Prefer clean ledger text; remove trailing section headings that belong
    # to the next top-level question only for prompt excerpts.
    return re.sub(r"\s+", " ", text).strip()


def trim_next_heading(text: str) -> str:
    # Segment files may include the next section heading after the final
    # subquestion.  It is a locator artifact, not part of the prompt.
    cuts = [m.start() for m in re.finditer(r"\n#{1,6}\s", text)]
    if cuts:
        text = text[: min(cuts)]
    return text


def clean_prompt_candidate(exam_id: str, q: int, text: str) -> tuple[str, list[str]]:
    """Make a traceable extraction prompt without silently correcting OCR."""
    actions: list[str] = []
    cleaned = trim_next_heading(text)
    if cleaned != text:
        actions.append("截去题段末尾下一节标题；原始题段保持不变。")
    if exam_id == "GK-SC-2013" and q == 14:
        replaced = re.sub(r"(?<![A-Za-z])Y(?![A-Za-z])", "[OCR疑似污染：Y]", cleaned)
        if replaced != cleaned:
            cleaned = replaced
            actions.append("将孤立字符 Y 显式标记为 OCR/水印疑点，不作语义纠正。")
    if exam_id == "GK-NC3-2016" and q == 1 and re.search(r"(?<![A-Za-z])YY(?![A-Za-z])", cleaned):
        cleaned = re.sub(r"(?<![A-Za-z])YY(?![A-Za-z])", "[OCR疑似污染：YY]", cleaned)
        actions.append("将选项末尾孤立字符 YY 显式标记为 OCR/水印疑点，不作语义纠正。")
    if exam_id == "GK-NC3-2016" and q == 6 and "🌙" in cleaned:
        cleaned = cleaned.replace("🌙", "")
        actions.append("隔离选项末尾推广残片 🌙；不进入题文正文。")
    if exam_id == "GK-NC3-2016" and q in (5, 6):
        actions.append("保留疑似 OCR 异文原样，待 PDF/独立来源复核后再修订。")
    if exam_id == "GK-NC3-2017" and q == 11:
        replaced = re.sub(r"(?<![A-Za-z0-9])0(?![A-Za-z0-9])", "[OCR疑似污染：0]", cleaned)
        if replaced != cleaned:
            cleaned = replaced
            actions.append("将孤立字符 0 显式标记为 OCR/水印疑点，不作语义纠正。")
    if exam_id == "GK-NC3-2017" and q == 1 and "众 人" in cleaned:
        cleaned = cleaned.split("众 人", 1)[0].rstrip()
        actions.append("截去题段末尾黏连的孤立字符‘众 人’及下一小问起始残片；原始题段保持不变。")
    if exam_id == "GK-NC3-2017" and q == 3:
        replaced = re.sub(r"(?<=。)\s*[WA](?=\s*(?:D\.|$))", "", cleaned)
        if replaced != cleaned:
            cleaned = replaced
            actions.append("移除选项末尾孤立字符 W/A（疑似 OCR/解析标记）；原始题段保持不变。")
    if exam_id == "GK-NC3-2017" and q == 9:
        replaced = cleaned.replace("（ VA．", "（A．").replace("( VA.", "(A.")
        if replaced != cleaned:
            cleaned = replaced
            actions.append("移除选项 A 前孤立字符 V（疑似 OCR/排版污染）；原始题段保持不变。")
    if exam_id == "GK-NC3-2020" and q == 8:
        replaced = re.sub(r"(?<![A-Za-z0-9])11\s+(?=食物的基本功能)", "", cleaned)
        if replaced != cleaned:
            cleaned = replaced
            actions.append("移除题段开头孤立字符 11（疑似页码/OCR残片）；原始题段保持不变。")
    return cleaned, actions


def numbered_parts(text: str) -> dict[str, str]:
    """Extract fullwidth/ASCII parenthesized parts in OCR-clean text."""
    matches = list(re.finditer(r"(?<!\d)[（(]([1-9][0-9]*)[）)]\s*", text))
    parts: dict[str, str] = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        parts[m.group(1)] = normalized_body(trim_next_heading(text[m.end():end]))
    return parts


def circled_parts(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"([①②③④⑤⑥⑦⑧])\s*", text))
    parts: dict[str, str] = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        parts[str("①②③④⑤⑥⑦⑧".index(m.group(1)) + 1)] = normalized_body(trim_next_heading(text[m.end():end]))
    return parts


def embedded_question_prompt(text: str, question_id: int) -> str:
    """Extract an embedded old-paper prompt from a shared final segment.

    Some 2009 segments place the literary material in Q14–Q16 and all four
    prompts at the end of Q17.  Choose the last occurrence of the target
    number (the prompt, not the material dialogue), then stop at the next
    numbered prompt.
    """
    marker = re.compile(rf"(?<!\d){question_id}\s*[、．.)）]\s*")
    hits = list(marker.finditer(text))
    if not hits:
        return normalized_body(text)
    start = hits[-1].end()
    next_marker = re.compile(r"(?<!\d)(?:14|15|16|17)\s*[、．.)）]\s*")
    end = len(text)
    for match in next_marker.finditer(text, start):
        if match.start() > hits[-1].start():
            end = match.start()
            break
    return normalized_body(trim_next_heading(text[start:end]))


def prompt_for(text: str, code: str) -> str:
    if "-" in code:
        outer, inner = code.split("-", 1)
        outer_parts = numbered_parts(text)
        outer_text = outer_parts.get(outer, text)
        circled = circled_parts(outer_text)
        if inner in circled:
            return circled[inner]
        nested = numbered_parts(outer_text)
        return nested.get(inner, outer_text)
    parts = numbered_parts(text)
    return parts.get(code, normalized_body(text))


def source_for(exam_id: str, q: int, role: str) -> dict | None:
    path = EXTRACT / exam_id / "ledger" / f"questions-{role}.jsonl"
    if not path.exists():
        return None
    for row in load_jsonl(path):
        if int(row.get("question_id", -1)) == q:
            return row
    return None


def score_group_for(exam_id: str, q: int) -> dict | None:
    """Return an explicit score-group declaration for a top-level question."""
    for group in CONFIG[exam_id].get("score_groups", []):
        if q in group.get("questions", []):
            return group
    return None


def segment_hash_anchor(segment_path: str, fallback: str | None) -> str | None:
    """Prefer the hash declared by the immutable segment frontmatter.

    A repaired ledger can temporarily lag a segment's own provenance field;
    the emitted node must be verifiable against the segment it links to.
    """
    path = ROOT / segment_path
    if path.exists():
        head = path.read_text(encoding="utf-8", errors="replace")[:5000]
        match = re.search(r'segment_clean_sha256:\s*"([0-9a-f]{64})"', head)
        if match:
            return match.group(1)
    return fallback


def base_top(exam_id: str, q: int) -> dict:
    top_path = OUT / "exam_response_nodes_top_level.jsonl"
    for row in load_jsonl(top_path):
        if row.get("exam_id") == exam_id and int(row.get("question_id", -1)) == q:
            return row
    raise KeyError(f"missing TOP node {exam_id} Q{q}")


def make_node(exam_id: str, q: int, code: str, score: int, prompt: str,
              qrow: dict, arow: dict | None, top: dict, missing: bool,
              choice_group: dict | None = None) -> dict:
    source_segment = qrow["segment_path"]
    answer_segment = arow.get("segment_path") if arow else None
    source_warning = []
    answer_status = "candidate_unverified"
    if missing or not arow or arow.get("segmentation_status") == "missing_source_marker":
        answer_status = "missing"
        source_warning.append("解析卷该题没有可定位题文/答案源；不把解析 PDF 推广页视为答案或评分标准。")
    evidence = [f"EV-EXAM-{exam_id}-Q{q:03d}-{code}-QUESTION-PDF",
                f"EV-EXAM-{exam_id}-Q{q:03d}-{code}-CLEAN-MD"]
    if answer_segment and answer_status != "missing":
        evidence.append(f"EV-EXAM-{exam_id}-Q{q:03d}-{code}-ANALYSIS-CANDIDATE")
    else:
        evidence.append(f"EV-EXAM-{exam_id}-Q{q:03d}-{code}-ANSWER-SOURCE-MISSING")
    # Keep the raw source span in ``prompt_text_raw`` for auditability.  The
    # extraction prompt is cleaned separately, so reviewed trailing headings
    # (e.g. 2024 Q009/Q021) remain visible only in the raw field.
    raw_prompt = prompt
    if code == "TOP" and qrow.get("raw_text"):
        raw_prompt = str(qrow["raw_text"])
    cleaned_prompt, prompt_actions = clean_prompt_candidate(exam_id, q, raw_prompt)
    source_blocks = qrow.get("source_block_ids", [])
    if not source_blocks:
        # Some MinerU ledgers have a valid page range but no layout blocks.
        # Use an explicit page-fallback token rather than inventing a block
        # bbox; downstream reviewers must not treat it as precise geometry.
        page = qrow.get("source_pdf_page_start") or (qrow.get("source_pdf_page_index_start", 0) + 1)
        source_blocks = [f"P{page}-PAGE-FALLBACK"]
    score_group = score_group_for(exam_id, q)
    score_basis = ("printed_section_total_visual_check"
                   if CONFIG[exam_id].get("visual_check_status", "passed") == "passed"
                   else "printed_prompt_score_candidate")
    score_allocation_status = "question_level_candidate"
    if score_group:
        if score_group.get("allocation") == "aggregate_only":
            score_basis = "printed_group_total_aggregate_only"
            score_allocation_status = "aggregate_group_lead" if q == score_group.get("lead_question") else "aggregate_group_placeholder"
        else:
            score_basis = "printed_group_total_candidate_allocation"
            score_allocation_status = "candidate_group_allocation"
    node = {
        "response_node_id": f"{exam_id}-Q{q:03d}-{code}",
        "exam_id": exam_id, "year": int(top["year"]), "paper_code": top["paper_code"],
        "question_id": q, "subquestion_code": code,
        "prompt_text_raw": raw_prompt[:4000],
        "prompt_text": cleaned_prompt[:4000], "prompt_text_for_extraction": cleaned_prompt[:4000],
        "prompt_excerpt": cleaned_prompt[:500], "prompt_cleaning_actions": prompt_actions,
        "score": score,
        "score_basis": score_basis,
        "score_allocation_status": score_allocation_status,
        "source_question_segment": source_segment,
        "source_analysis_segment": answer_segment,
        "source_pdf": qrow["source_pdf"], "source_mineru_md": qrow["source_mineru_md"],
        "source_clean_md": qrow["source_clean_md"],
        "source_pdf_page_index_start": qrow["source_pdf_page_index_start"],
        "source_pdf_page_index_end": qrow["source_pdf_page_index_end"],
        "source_locator_status": qrow.get("source_locator_status", "page_level_fallback"),
        "locator_precision_note": "当前仅页级回退定位；source_block_ids/bbox 不视为题级精确框。",
        "source_block_ids": source_blocks,
        "section_id": qrow.get("section_id"), "question_type_l1": qrow.get("question_type_l1"),
        "question_type_l2": qrow.get("question_type_l2"), "material_id": qrow.get("material_id"),
        "segment_clean_sha256": segment_hash_anchor(source_segment, qrow.get("segment_clean_sha256")),
        "raw_segment_sha256": qrow.get("raw_segment_sha256"),
        "ability_action": top.get("ability_action_candidate", "N/A"),
        "four_layer": "N/A", "four_wings": "N/A", "context_type": "N/A",
        "atomic_exam_point": "N/A",
        "answer_source_status": answer_status, "evidence_ids": evidence,
        "evidence_id": evidence[0], "decomposition_status": "response_nodes_derived",
        "kp_id": "N/A", "mapping_level": "M0",
        "na_reason": "校准切片仅完成作答节点与分值结构；教材双向证据和正式评分权威尚未核验。",
        "review_status": "needs_manual_review" if source_warning else "calibration_derived",
        "choice_group": False, "source_warnings": source_warning,
    }
    if score_group:
        node["score_group_id"] = score_group["id"]
        node["score_group_questions"] = score_group["questions"]
        node["score_group_total"] = score_group["total"]
        node["score_group_allocation"] = score_group["allocation"]
        if score_group.get("allocation") == "aggregate_only":
            node["source_warnings"].append(
                "该语言文字运用题组仅有卷面组总分；本节点分值为组首登记或0分结构占位，不代表正式小题分值。"
            )
            node["review_status"] = "needs_manual_review"
    if q in CONFIG[exam_id].get("boundary_annotations", {}):
        node["boundary_status"] = CONFIG[exam_id].get("boundary_status_by_question", {}).get(
            q, "boundary_trailing_heading"
        )
        node["boundary_note"] = CONFIG[exam_id]["boundary_annotations"][q]
        node["source_warnings"].append(node["boundary_note"])
        node["review_status"] = "needs_manual_review"
    else:
        node["boundary_status"] = "clean_or_trimmed"
    if q in CONFIG[exam_id].get("ocr_annotations", {}):
        node["ocr_status"] = "suspected_ocr_or_watermark_noise"
        node["ocr_note"] = CONFIG[exam_id]["ocr_annotations"][q]
        node["source_warnings"].append(node["ocr_note"])
        node["review_status"] = "needs_manual_review"
    else:
        node["ocr_status"] = "not_flagged_in_slice_review"
    image_annotation = CONFIG[exam_id].get("image_annotations", {}).get(q)
    if image_annotation:
        node["image_asset_status"] = image_annotation["status"]
        node["image_asset_path"] = image_annotation["path"]
        node["image_asset_note"] = image_annotation["note"]
        node["source_warnings"].append(image_annotation["note"])
        node["review_status"] = "needs_manual_review"
    node["content_acceptance"] = "conditional_review" if node["source_warnings"] or prompt_actions else "structural_slice_ready"
    return node


def apply_choice_group(node: dict, group: dict) -> None:
    node["choice_group"] = True
    node["choice_group_id"] = group["id"]
    node["choice_branch_count"] = len(group["questions"])
    node["scored_branch_count"] = group["scored_branch_count"]
    node["choice_group_note"] = "并列阅读文本二选一；节点分值保留各分支，卷面总分只计一支。"


def run_exam(exam_id: str) -> dict:
    cfg = CONFIG[exam_id]
    qrows = {int(r["question_id"]): r for r in load_jsonl(EXTRACT / exam_id / "ledger/questions-question.jsonl")}
    nodes: list[dict] = []
    errors: list[str] = []
    for q in sorted(cfg["score"]):
        canonical_qrow = qrows[q]
        prompt_q = cfg.get("prompt_source_question", {}).get(q, q)
        answer_q = cfg.get("answer_source_question", {}).get(q, q)
        qrow = qrows[prompt_q] if prompt_q in qrows else canonical_qrow
        arow = source_for(exam_id, answer_q, "analysis")
        top = base_top(exam_id, q)
        if q in cfg.get("split", {}):
            parts = numbered_parts(qrow.get("clean_text", ""))
            circled = circled_parts(qrow.get("clean_text", ""))
            for code, score in cfg["split"][q]:
                prompt = prompt_for(qrow.get("clean_text", ""), code)
                if not prompt or prompt == normalized_body(qrow.get("clean_text", "")):
                    # A nested translation item is often marked ①/②.
                    if "-" in code and code.split("-", 1)[1] in circled:
                        prompt = circled[code.split("-", 1)[1]]
                node = make_node(exam_id, q, code, score, prompt, qrow, arow,
                                 top, q in cfg.get("missing_answer_questions", []))
                for group in cfg.get("choice_groups", []):
                    if q in group["questions"]:
                        apply_choice_group(node, group)
                nodes.append(node)
        else:
            prompt_text = qrow.get("clean_text", "")
            if prompt_q != q or q in cfg.get("embedded_prompt_questions", []):
                prompt_text = embedded_question_prompt(prompt_text, q)
            node = make_node(exam_id, q, "TOP", cfg["score"][q],
                             prompt_text,
                             qrow, arow, top, q in cfg.get("missing_answer_questions", []))
            if prompt_q != q:
                node["canonical_question_segment"] = canonical_qrow["segment_path"]
                node["source_prompt_segment"] = qrow["segment_path"]
                node["source_prompt_question_id"] = prompt_q
            if q in cfg.get("optional", {}):
                opt = cfg["optional"][q]
                node["choice_group"] = True
                node["choice_group_id"] = f"{exam_id}-Q{q:03d}-OPTIONAL"
                node["choice_branch_count"] = opt["branch_count"]
                node["scored_branch_count"] = opt["scored_branch_count"]
                node["choice_group_note"] = "任选题保留一个计分节点，另行登记分支数与计分支数。"
            nodes.append(node)
    score_total = sum(int(n["score"]) for n in nodes)
    for group in cfg.get("choice_groups", []):
        # All branch nodes are emitted for retrieval; reconcile the scored
        # total by subtracting unselected alternatives.
        branch_total = sum(int(n["score"]) for n in nodes if n.get("choice_group_id") == group["id"])
        selected_total = branch_total * group["scored_branch_count"] // len(group["questions"])
        score_total -= branch_total - selected_total
    if score_total != cfg["expected_total"]:
        errors.append(f"score total {score_total} != {cfg['expected_total']}")
    expected_ids = set(cfg["score"])
    if set(qrows) != expected_ids:
        errors.append(f"question denominator mismatch: {sorted(qrows)}")
    out_jsonl = OUT / f"{exam_id}-response_nodes_vertical_slice.jsonl"
    out_jsonl.write_text("\n".join(json.dumps(n, ensure_ascii=False) for n in nodes) + "\n", encoding="utf-8")
    receipt = {
        "schema_version": "exam-vertical-review-receipt-0.1",
        "receipt_id": f"EXAM-VERTICAL-{exam_id}-20260809",
        "exam_id": exam_id, "calibration_id": "SG-EXAM-CAL-2008-2024",
        "generated_at": now_text(), "status": "structural_pass" if not errors else "failed",
        "acceptance": "conditional_review" if any(n.get("source_warnings") or n.get("prompt_cleaning_actions") for n in nodes) else "ready",
        "scope": "response_node_decomposition_and_score_reconciliation",
        "source_policy": {
            "question_pdf_visual_check": cfg.get("visual_check_status", "passed"),
            "source_pdf_read_only": True, "mineru_full_md_read_only": True,
            "answer_authority": "candidate_unverified_or_missing",
            "mapping_boundary": "M0_only",
        },
        "visual_check": {"pages_checked": cfg["visual_pages"], "notes": cfg["visual_notes"]},
        **({"visual_review_receipt": cfg["visual_review_receipt"]}
           if cfg.get("visual_review_receipt") else {}),
        "node_count": len(nodes), "question_count": len(cfg["score"]),
        "score_total": score_total, "expected_score_total": cfg["expected_total"],
        "choice_groups": ([{"id": g["id"], "questions": g["questions"],
                             "scored_branch_count": g["scored_branch_count"]}
                            for g in cfg.get("choice_groups", [])] +
                           [{"id": f"{exam_id}-Q{q:03d}-OPTIONAL",
                            "questions": [q], "branch_count": opt["branch_count"],
                            "scored_branch_count": opt["scored_branch_count"]}
                            for q, opt in cfg.get("optional", {}).items()]),
        "score_groups": cfg.get("score_groups", []),
        "score_notes": cfg.get("score_notes", {}),
        "missing_answer_source_questions": cfg.get("missing_answer_questions", []),
        "source_hash_anchors": {"question_pdf": {q: sha256(ROOT / r["source_pdf"]) for q, r in qrows.items()}},
        "derived_jsonl": str(out_jsonl.relative_to(ROOT)), "errors": errors,
        "warnings": ([w for n in nodes for w in n.get("source_warnings", [])] +
                      [a for n in nodes for a in n.get("prompt_cleaning_actions", [])] +
                      cfg.get("material_annotations", []) +
                      list(cfg.get("score_notes", {}).values())),
    }
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPTS / f"exam_vertical_{exam_id}_20260809.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = OUT / f"EXAM-{exam_id}-VERTICAL-SLICE.md"
    lines = ["---", "schema_version: \"exam-vertical-review-0.1\"", f"exam_id: \"{exam_id}\"",
             "status: \"" + receipt["status"] + "\"", "acceptance: \"" + receipt["acceptance"] + "\"", "mapping_status: \"M0_only\"", "---", "",
             f"# {exam_id} 垂直切片复核", "", 
             f"- 作答节点：{len(nodes)}；顶层题：{len(cfg['score'])}；分值复算：{score_total}/{cfg['expected_total']}。",
             "- 题干来自空白卷；解析卷仅作为候选来源，未宣称官方答案或评分标准。",
             "- 原始 PDF、MinerU full.md 未改写；清洗段与原卷保持双链。", "",
             "## 节点概览", "", "| 节点 | 分值 | 题型 | 答案源 | 状态 |", "|---|---:|---|---|---|"]
    for n in nodes:
        lines.append(f"| {n['response_node_id']} | {n['score']} | {n['question_type_l2']} | {n['answer_source_status']} | {n['decomposition_status']} |")
    lines += ["", "## 视觉核对", ""] + [f"- {x}" for x in cfg["visual_notes"]]
    if cfg.get("score_groups"):
        lines += ["", "## 分值登记边界", "", "- 本切片区分卷面组总分、候选分配和组首/占位登记；`score=0` 仅表示未分配占位，不表示该小题正式得0分。", "", "| 分组 | 题号 | 卷面总分 | 登记方式 |", "|---|---|---:|---|"]
        for group in cfg["score_groups"]:
            lines.append(f"| {group['id']} | {','.join('Q'+str(q) for q in group['questions'])} | {group['total']} | {group['allocation']} |")
    if cfg.get("missing_answer_questions"):
        lines += ["", "## 缺失来源", "", "- " + "、".join(f"Q{q:02d}" for q in cfg["missing_answer_questions"]) + " 的解析题文/评分来源缺失；只保留题干节点，不能视为解析完成。"]
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="生成指定高考年度的保守垂直切片")
    parser.add_argument("--exam-id", action="append", choices=sorted(CONFIG),
                        help="只运行指定 exam_id；可重复传入，默认运行全部配置")
    args = parser.parse_args()
    exam_ids = args.exam_id or list(CONFIG)
    reports = [run_exam(eid) for eid in exam_ids]
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0 if all(r["status"] == "structural_pass" for r in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
