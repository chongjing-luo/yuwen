---
schema_version: "exam-kp-extraction-draft-report-0.1"
status: "candidate_structural"
calibration_id: "SG-EXAM-CAL-2008-2024"
node_count: 310
mapping_status: "M0_only"
---

# 高考知识点抽取首轮草稿回执

> 本批次完成 2008—2024 的顶层题目节点提取。它是 EKP 的结构化首轮，不等于小问级知识点完成，也不建立教材—真题确定性映射。

| Exam | 顶层节点 | 期望 | 缺失源标记 | 草稿 |
|---|---:|---:|---|---|
| GK-SC-2008 | 21 | 21 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-SC-2008.md|打开]] |
| GK-SC-2009 | 21 | 21 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-SC-2009.md|打开]] |
| GK-SC-2010 | 21 | 21 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-SC-2010.md|打开]] |
| GK-SC-2011 | 21 | 21 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-SC-2011.md|打开]] |
| GK-SC-2012 | 21 | 21 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-SC-2012.md|打开]] |
| GK-SC-2013 | 21 | 21 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-SC-2013.md|打开]] |
| GK-SC-2014 | 21 | 21 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-SC-2014.md|打开]] |
| GK-SC-2015 | 21 | 21 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-SC-2015.md|打开]] |
| GK-NC3-2016 | 12 | 12 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NC3-2016.md|打开]] |
| GK-NC3-2017 | 12 | 12 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NC3-2017.md|打开]] |
| GK-NC3-2018 | 10 | 10 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NC3-2018.md|打开]] |
| GK-NC3-2019 | 10 | 10 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NC3-2019.md|打开]] |
| GK-NC3-2020 | 10 | 10 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NC3-2020.md|打开]] |
| GK-NCA-2021 | 22 | 22 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NCA-2021.md|打开]] |
| GK-NCA-2022 | 22 | 22 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NCA-2022.md|打开]] |
| GK-NCA-2023 | 22 | 22 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NCA-2023.md|打开]] |
| GK-NCA-2024 | 22 | 22 | 无 | [[work/knowledge/高考分析/exam_drafts/GK-NCA-2024.md|打开]] |

## 已完成的垂直切片

- 2008：已拆出 24 个作答节点，包含 1 个任选组/2 个分支，并复算总分 150；见 `EXAM-2008-SC-response_nodes.jsonl` 与对应验证报告。
- 2009—2012、2014—2015：各完成逐页 PDF 视觉复核和独立回执；2009/2010 文件名与PDF首页‘解析’标签冲突已显式保留。
- 2013：已拆出 23 个保守作答节点，复算总分 150；独立复核回执登记 OCR 与答案来源缺口。
- 2016：已拆出 27 个节点，按阅读二选一校正后复算 150；图示题保留图片源路径。
- 2017：已拆出 23 个保守作答节点，复算总分 150；Q6 保留为单一 5 分节点，Q11 的 OCR 残片显式标记；已完成逐页 PDF 视觉复核与独立视觉回执。
- 2018：已建立 10 个顶层保守作答节点，按卷面 Q1—Q10 总分复算 150；Q7 内部无稳定独立分值，暂不虚拆，并已完成逐页 PDF 视觉复核。
- 2019：已建立 10 个顶层保守作答节点，按卷面 Q1—Q10 总分复算 150；漫画材料保留图像源路径，并已完成逐页 PDF 视觉复核。
- 2020：已建立 10 个顶层保守作答节点，按卷面 Q1—Q10 总分复算 150；Q8 页码/OCR 残片已显式隔离，并已完成逐页 PDF 视觉复核。
- 2021—2023：各生成 22 个保守作答节点，逐页完成 PDF 视觉复核并复算 150；语言文字运用组总分保留在组首节点，未虚构小问分值。
- 2024：已生成 25 个保守作答节点，翻译/默写按稳定分值拆分；Q4 OCR缺字、Q6边界、Q9 后续文言文污染截断与缺失答案源均显式登记。

## 已执行的小问级候选批次

| 批次 | 范围 | 节点数 | 产物 |
|---|---|---:|---|
| 字音辨析 | 2008—2015 | 8 | `kp_batches/word_pronunciation_2008_2015.md` |
| 字形、词语、病句 | 2009—2015 | 21 | `kp_batches/core_language_use_2009_2015.md` |
| 文言实词、虚词 | 2009—2015 | 14 | `kp_batches/classical_language_2009_2015.md` |
| 文言文内容概括/信息筛选 | 2009—2015 | 7 | `kp_batches/ancient_content_2009_2015.md` |
| 文言文翻译 | 2009—2015 | 13 | `kp_batches/classical_translation_2009_2015.md` |
| 名篇名句默写 | 2009—2015 | 11 | `kp_batches/classical_memorization_2009_2015.md` |
| 古诗词鉴赏 | 2009—2015 | 14 | `kp_batches/poetry_appreciation_2009_2015.md` |
| 现代文信息类阅读 | 2009—2015 | 21 | `kp_batches/modern_informational_2009_2015.md` |
| 文学类文本阅读 | 2009—2015 | 28 | `kp_batches/literary_reading_2009_2015.md` |
| 材料/命题作文 | 2009—2015 | 7 | `kp_batches/topic_writing_2009_2015.md` |
| 语言文字综合表达 | 2009—2015 | 15 | `kp_batches/language_expression_2009_2015.md` |
| 剩余文言断句/概括应用 | 2013—2015 | 6 | `kp_batches/remaining_language_2009_2015.md` |
| 语言文字运用稳定小问 | 2016—2017 | 10 | `kp_batches/language_application_2016_2017.md` |
| 语言文字运用小问 | 2021—2024 | 20 | `kp_batches/language_application_2021_2024.md` |
| 2018—2020 语言运用组题小问 | 2018—2020 | 9 | `kp_batches/language_group_subquestion_2018_2020.md` |
| 2018—2020 语言运用 Q8/Q9 任务单元 | 2018—2020 | 14 | `kp_batches/language_application_tasks_2018_2020.md` |
| 文言文翻译 | 2021—2024 | 5 | `kp_batches/classical_translation_2021_2024.md` |
| 名篇名句默写 | 2016—2024 | 13 | `kp_batches/classical_memorization_2016_2024.md` |
| 古诗词鉴赏 | 2016—2024 | 15 | `kp_batches/poetry_appreciation_2016_2024.md` |
| 现代文信息类阅读 | 2016—2024 | 21 | `kp_batches/modern_informational_2016_2024.md` |
| 文学类文本阅读 | 2016—2024 | 22 | `kp_batches/literary_reading_2016_2024.md` |
| 实用类文本阅读 | 2016—2024 | 22 | `kp_batches/practical_reading_2016_2024.md` |
| 文言文基础阅读 | 2021—2024 | 12 | `kp_batches/ancient_reading_2021_2024.md` |
| 材料/命题作文 | 2016—2024 | 9 | `kp_batches/topic_writing_2016_2024.md` |

合计 337 个候选节点（含本批次新增 14 个任务单元）。它们均保留题干、PDF、解析源与 SHA-256 可追溯字段；候选答案不等同官方答案，教材映射仍为 `M0 / kp_id=N/A`。翻译、默写、诗歌鉴赏、现代文信息阅读、文学阅读、实用类阅读、文言文基础阅读、作文、语言表达和本批次的答案全部保持未自动抽取。

## 下一步人工批次

1. [x] 完成首轮答案/评分来源审计；见 [[work/knowledge/高考分析/EXAM-ANSWER-SCORING-AUDIT-20260809|答案/评分来源审计]]，机器清单见 `work/knowledge/_meta/exam_answer_scoring_audit_20260809.json`。
2. [x] 建立可逆候选答案层；见 [[work/knowledge/高考分析/EXAM-ANSWER-CANDIDATE-EXTRACTION-20260809|候选答案层回执]]。当前 310 个顶层题目中 74 个保留非空候选片段，官方核验数为 0；候选层哈希验证通过。
3. [x] 将 359 个垂直作答节点按 30 种题型归并为人工清洗队列；见 [[work/knowledge/高考分析/EXAM-TYPE-KP-REVIEW-QUEUE-20260809|题型—知识点清洗队列]]，队列验证通过。
4. [x] 完成首个小问级候选批次：字音辨析（2008—2015，8 个节点）；见 `work/knowledge/高考分析/kp_batches/word_pronunciation_2008_2015.md`。其中仅 2 个有未核验答案文本，1 个答案文本存在但权威状态缺失，4 个解析源无显式答案，1 个分析源缺失。
5. [x] 完成第二个小问级候选批次：字形、词语、病句（2009—2015，21 个节点）；见 `work/knowledge/高考分析/kp_batches/core_language_use_2009_2015.md`。显式候选答案仅 4 个，2013 年权威缺失门禁保留，全部保持 M0。
6. [x] 完成第三个小问级候选批次：文言实词、虚词（2009—2015，14 个节点）；见 `work/knowledge/高考分析/kp_batches/classical_language_2009_2015.md`。12 个解析源没有显式答案标记，2013 年 2 个节点保留 `source_authority_missing`，全部保持 M0。
7. [x] 完成第四个小问级候选批次：文言文内容概括/信息筛选（2009—2015，7 个节点）；见 `work/knowledge/高考分析/kp_batches/ancient_content_2009_2015.md`。6 个解析源没有显式答案标记，2013 年 1 个节点保留 `source_authority_missing`，全部保持 M0。
8. [x] 完成第五个小问级候选批次：文言文翻译（2009—2015，13 个节点）；见 `work/knowledge/高考分析/kp_batches/classical_translation_2009_2015.md`。自由作答答案均未自动抽取，2013 年 2 个节点保留 `source_authority_missing`，全部保持 M0。
9. [x] 完成第六个小问级候选批次：名篇名句默写（2009—2015，11 个节点）；见 `work/knowledge/高考分析/kp_batches/classical_memorization_2009_2015.md`。默写答案均未自动抽取，2013 年 1 个节点保留 `source_authority_missing`，全部保持 M0。
10. [x] 完成第七个小问级候选批次：古诗词鉴赏（2009—2015，14 个节点）；见 `work/knowledge/高考分析/kp_batches/poetry_appreciation_2009_2015.md`。共享解析段显式登记，答案均未自动抽取，2013 年 2 个节点保留 `source_authority_missing`，全部保持 M0。
11. [x] 完成第八个小问级候选批次：现代文信息类阅读（2009—2015，21 个节点）；见 `work/knowledge/高考分析/kp_batches/modern_informational_2009_2015.md`。老解析段可能含同组关联上下文，已显式登记，答案均未自动抽取，2013 年 3 个节点保留 `source_authority_missing`，全部保持 M0。
12. [x] 完成第九个小问级候选批次：文学类文本阅读（2009—2015，28 个节点）；见 `work/knowledge/高考分析/kp_batches/literary_reading_2009_2015.md`。老解析段可能含同组关联上下文，答案均未自动抽取，2013 年 4 个节点保留 `source_authority_missing`，全部保持 M0。
13. [x] 完成第十个小问级候选批次：材料/命题作文（2009—2015，7 个节点）；见 `work/knowledge/高考分析/kp_batches/topic_writing_2009_2015.md`。作文答案与评分均未自动抽取，2013 年 1 个节点保留 `source_authority_missing`，全部保持 M0。
14. [x] 完成第十一个小问级候选批次：语言文字综合表达（2009—2015，15 个节点）；见 `work/knowledge/高考分析/kp_batches/language_expression_2009_2015.md`。概括、仿写、修辞和应用表达答案均未自动抽取，2013 年 1 个节点保留 `source_authority_missing`，全部保持 M0。
15. [x] 补齐剩余语言表达节点（2013—2015，6 个节点）；见 `work/knowledge/高考分析/kp_batches/remaining_language_2009_2015.md`。其中 2013 年本批次 2 个节点保留 `source_authority_missing`，与上一批次 2013 Q020 合计 3 个语言类权威缺失节点；全部保持 M0。
16. [x] 完成 2016—2017 语言文字运用稳定小问批次（Q7—Q11，共 10 个节点）；见 `work/knowledge/高考分析/kp_batches/language_application_2016_2017.md`。2017 Q9/Q11 OCR 疑点随源字段保留，答案全部未自动抽取，全部保持 M0。
17. [x] 完成 2021—2024 语言文字运用小问批次（Q17—Q21，共 20 个节点）；见 `work/knowledge/高考分析/kp_batches/language_application_2021_2024.md`。2024 Q21 权威来源缺失门禁保留，答案全部未自动抽取，全部保持 M0。
18. [x] 将 2018—2020 Q7 组题拆成 9 个可逆小问文件并生成候选批次；见 `kp_batches/language_group_subquestion_2018_2020.md` 与 `kp_batches/language_group_subquestion_split_2018_2020.json`。父题组总分保留，小问分值保持 `N/A`，不臆分，全部 M0。
19. [x] 将 2018—2020 Q8/Q9 按稳定任务边界拆成 14 个可逆任务单元；见 `kp_batches/language_application_tasks_2018_2020.md` 与 `kp_batches/language_application_tasks_split_2018_2020.json`。2018 Q8 五处修改、2019/2020 Q8 三个补写空、三年 Q9 单一任务均不臆造分值，全部 M0；2020 OCR 残片和 2018 图示链路显式保留。
20. [x] 完成 2021—2024 文言文翻译候选批次（5 个节点）；见 `kp_batches/classical_translation_2021_2024.md`。2021—2023 共享题目级解析段保持显式，答案/评分未自动抽取，全部保持 M0。
21. [x] 完成 2016—2024 名篇名句默写候选批次（13 个节点）；见 `kp_batches/classical_memorization_2016_2024.md`。2016、2024 分支保留，答案/评分未自动抽取，全部保持 M0。
22. [x] 完成 2016—2024 古诗词鉴赏候选批次（15 个节点）；见 `kp_batches/poetry_appreciation_2016_2024.md`。2018—2020 组题保持题目级共享解析范围，答案/评分未自动抽取，全部保持 M0。
23. [x] 完成 2016—2024 现代文信息类阅读候选批次（21 个节点）；见 `kp_batches/modern_informational_2016_2024.md`。解析关联上下文显式保留，选择题答案未自动抽取，全部保持 M0。
24. [x] 完成 2016—2024 文学类文本阅读候选批次（22 个节点）；见 `kp_batches/literary_reading_2016_2024.md`。题目段关联上下文显式保留，答案/评分未自动抽取，全部保持 M0。
25. [x] 完成 2016—2024 实用类文本阅读候选批次（22 个节点）；见 `kp_batches/practical_reading_2016_2024.md`。图表/图文题保留原始链路，答案/评分未自动抽取，全部保持 M0。
26. [x] 完成 2021—2024 文言文基础阅读候选批次（12 个节点）；见 `kp_batches/ancient_reading_2021_2024.md`。断句/词语/内容题与翻译分批登记，答案未自动抽取，全部保持 M0。
27. [x] 完成 2016—2024 材料/命题作文候选批次（9 个节点）；见 `kp_batches/topic_writing_2016_2024.md`。不生成范文、立意答案或评分结论，全部保持 M0。
28. 对后续稳定题型补登记四层、四翼、情境、能力动作和原子考点，所有直接引文回看 PDF。
29. 仅在题文—答案/评分—教材KP三方证据闭合后建立 M1/M2 映射；其余继续保持 M0。
30. 继续细化其他尚未稳定的组内节点，并对已生成候选批次开展答案/评分与教材KP人工闭合复核。
