---
schema_version: "exam-analysis-0.3-corpus"
deliverable_id: "EXAM-2008-2024-SC-CORPUS"
status: "structural_gate_passed_manual_review_pending"
coverage: "2008-2024"
pdf_count: 34
exam_count: 17
source_status: "unverified_local_provided"
mapping_status: "M0"
textbook_lock_id: "TEXTBOOK-LOCK-2.0-textbook"
textbook_deliverables_sha256: "63a2974acd668e6b9a4b55f4c0a12b4adc42fb9e4df806e0a0a2d336fb723baa"
---

# 2008—2024 四川适用高考语文结构化语料总回执

## 年份结构

| 年份 | 卷码 | 顶层题数 | 题目目录 | 状态 |
|---|---|---:|---|---|
| 2008—2015 | SC | 21 | `GK-SC-YYYY/` | 结构门禁通过 |
| 2016—2020 | NC3 | 12（2016—17）/10（2018—20） | `GK-NC3-YYYY/` | 结构门禁通过 |
| 2021—2024 | NCA | 22 | `GK-NCA-YYYY/` | 结构门禁通过 |

每个年度包含空白卷与解析卷的清洗稿、题目级段落、材料对象、题型索引、机器账本和异常记录。源 PDF 与 MinerU `full.md` 未改写；题目段落通过清洗稿、原始 MinerU 和 PDF 双链回溯。

## 特殊缺失项

- 2022 空白卷 Q6：MinerU 文本层未出现可定位题号/题文，已生成 `Q006.md` 占位卡，`segmentation_status=missing_source_marker`；
- 2024 解析卷 Q21、Q22：文本层未出现可定位题号/题文，已生成占位卡并列入 PDF 复核；
- 以上占位卡不被当作已提取正文，必须完成 PDF 回看后再进入答案或知识点抽取。

## 机器验收

`scripts/validate_sichuan_gaokao_batch.py` 对 2008—2024 年度逐一运行，全部 `result=passed`。硬门禁包括：manifest 双角色、原始哈希、题号集合和题段数、清洗广告隔离、题目—清洗稿—MinerU—PDF 双链、段落哈希、材料目标存在。缺失题号仅作为 warning，不绕过人工复核。

## 尚未完成

1. 双人 PDF/OCR 逐页抽检；2022 空白卷 Q006 的手工定位已登记，2024 解析卷 Q021/Q022 占位卡仍待回填；
2. 解析卷发布主体、答案/评分参考的来源等级核验；
3. `source_locator_status=page_level_fallback` 到题级 bbox 的人工仲裁；
4. 2008—2017、2024 十一个切片已完成候选作答节点拆解（263 个节点）；题级 PDF 视觉复核与独立第二复审仍待闭合；
5. 依据课程标准与教材知识卡建立逐小问证据链。当前教材—真题关系保持 `N/A | M0 | N/A`。

## 派生复核元数据同步边界

- `ledger/questions-question.jsonl` 继续作为题目分割与原始清洗账本，保留题段原文、原始哈希和 MinerU/PDF 页级定位；不把垂直切片的派生修复字段回写成“原始题文”。
- 2016 Q011 的图像哈希、尺寸、MinerU 图像块定位，以及 2024 Q004 的 OCR 缺段视觉修复，已登记在对应垂直切片节点和复核回执中；账本中的 `raw_text/clean_text` 保持其清洗账本语义。
- 2008 Q006 已经高分辨率 PDF 复核：卷面确实印有“那么可以32%的汽油……”，因此只更新派生节点的复核说明，不补写“得到”；原始 PDF、MinerU 和清洗稿均不改写。

## 入口

- [试卷输出](../../../Data/2008-2024·（四川）语文高考真题/exam_extract/README.md)
- [处理协议](试卷处理协议-v0.1.md)
- [批次验证脚本](../../../scripts/validate_sichuan_gaokao_batch.py)
- [全量题数/缺失标记配置](exam_expectations_2008_2024.json)
- [2009—2015 章节/题型配置](exam_expectations_2009_2015.json)
