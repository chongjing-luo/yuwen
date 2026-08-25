---
schema_version: "exam-type-review-queue-0.1"
status: "candidate_queue"
mapping_status: "M0_only"
node_count: 359
---

# 跨年度题型—知识点人工清洗队列

> 输入为 2008—2024 垂直切片的 359 个作答节点。队列按 `question_type_l2` 归并；每个题型页面显式保留题干、清洗稿、原始 MinerU、原始 PDF 和解析候选（如有）的双链。它不修改上游，不宣称官方答案，不建立教材 KP 映射。

- 作答节点：359；题型数：30。
- 候选答案源：336；明确缺失：23。

> 补充批次说明：2018—2020 Q8/Q9 的 14 个任务单元已另行登记于 `kp_batches/language_application_tasks_2018_2020.jsonl`，不重复并入本 359 条顶层作答队列；其题干/解析派生文件、父题哈希和 M0 门禁见对应批次报告。

## 审核门分布

| 审核门 | 数量 | 处理含义 |
|---|---:|---|
| `candidate_ready_for_manual_kp_review` | 230 | 可进入小问级答案/评分与教材 KP 对照，但仍保持 M0 |
| `ocr_or_watermark_review` | 42 | 先处理 OCR/水印疑点，不得静默改写 |
| `conditional_content_review` | 64 | 先完成 PDF/边界条件复核 |
| `answer_source_missing` | 23 | 补来源或显式保持缺失 |
| `decomposition_review` | 0 | 先稳定小问边界 |

## 题型汇总

| 题型 | 节点数 | 候选考点描述 | 队列文件 |
|---|---:|---|---|
| `ancient_function_words` | 7 | 文言虚词意义和用法辨析 | [[work/knowledge/exams/workbench/type_review_queue/ancient_function_words.md|打开]] |
| `ancient_reading` | 12 | 文言文断句、文化常识与内容理解 | [[work/knowledge/exams/workbench/type_review_queue/ancient_reading.md|打开]] |
| `ancient_text_content` | 21 | 文言文内容概括与分析 | [[work/knowledge/exams/workbench/type_review_queue/ancient_text_content.md|打开]] |
| `ancient_text_evidence` | 1 | 文言文信息筛选与证据判断 | [[work/knowledge/exams/workbench/type_review_queue/ancient_text_evidence.md|打开]] |
| `ancient_vocab` | 8 | 文言实词语境释义 | [[work/knowledge/exams/workbench/type_review_queue/ancient_vocab.md|打开]] |
| `classical_memorization` | 26 | 名篇名句理解性默写 | [[work/knowledge/exams/workbench/type_review_queue/classical_memorization.md|打开]] |
| `classical_translation` | 20 | 文言句子翻译 | [[work/knowledge/exams/workbench/type_review_queue/classical_translation.md|打开]] |
| `completion` | 1 | 语句补写与语意连贯 | [[work/knowledge/exams/workbench/type_review_queue/completion.md|打开]] |
| `idiom_usage` | 1 | 成语语境使用辨析 | [[work/knowledge/exams/workbench/type_review_queue/idiom_usage.md|打开]] |
| `language_application` | 39 | 语言文字运用中的衔接、补写、辨析与表达 | [[work/knowledge/exams/workbench/type_review_queue/language_application.md|打开]] |
| `literary_reading` | 52 | 文学类文本形象、结构、语言与主题鉴赏 | [[work/knowledge/exams/workbench/type_review_queue/literary_reading.md|打开]] |
| `meaning_explanation` | 1 | 文学文本词句含义与表达效果 | [[work/knowledge/exams/workbench/type_review_queue/meaning_explanation.md|打开]] |
| `metaphor_series` | 1 | 修辞辨析与表达效果 | [[work/knowledge/exams/workbench/type_review_queue/metaphor_series.md|打开]] |
| `modern_reading_informational` | 45 | 现代文信息筛选、概括与推断 | [[work/knowledge/exams/workbench/type_review_queue/modern_reading_informational.md|打开]] |
| `orthography` | 7 | 现代汉字字形辨析 | [[work/knowledge/exams/workbench/type_review_queue/orthography.md|打开]] |
| `parallelism_or_practical` | 4 | 修辞组织与应用表达 | [[work/knowledge/exams/workbench/type_review_queue/parallelism_or_practical.md|打开]] |
| `poetry_appreciation` | 31 | 古代诗歌形象、情感与表达手法鉴赏 | [[work/knowledge/exams/workbench/type_review_queue/poetry_appreciation.md|打开]] |
| `practical_or_expansion` | 3 | 应用写作或语句扩展 | [[work/knowledge/exams/workbench/type_review_queue/practical_or_expansion.md|打开]] |
| `practical_reading` | 22 | 实用类文本信息、结构与表达目的分析 | [[work/knowledge/exams/workbench/type_review_queue/practical_reading.md|打开]] |
| `sentence_error` | 1 | 病句结构与语意辨析 | [[work/knowledge/exams/workbench/type_review_queue/sentence_error.md|打开]] |
| `sentence_expansion` | 4 | 仿写、扩写与修辞表达 | [[work/knowledge/exams/workbench/type_review_queue/sentence_expansion.md|打开]] |
| `sentence_grammar` | 7 | 病句结构与语意辨析 | [[work/knowledge/exams/workbench/type_review_queue/sentence_grammar.md|打开]] |
| `sentence_segmentation` | 3 | 文言文句读与断句 | [[work/knowledge/exams/workbench/type_review_queue/sentence_segmentation.md|打开]] |
| `sequence` | 1 | 语句衔接与语意连贯 | [[work/knowledge/exams/workbench/type_review_queue/sequence.md|打开]] |
| `structure_effect` | 1 | 文学文本结构作用与表达效果 | [[work/knowledge/exams/workbench/type_review_queue/structure_effect.md|打开]] |
| `summary` | 5 | 材料信息压缩与概括 | [[work/knowledge/exams/workbench/type_review_queue/summary.md|打开]] |
| `summary_or_application` | 3 | 信息概括与应用表达 | [[work/knowledge/exams/workbench/type_review_queue/summary_or_application.md|打开]] |
| `topic_writing` | 17 | 材料作文立意、构思与书面表达 | [[work/knowledge/exams/workbench/type_review_queue/topic_writing.md|打开]] |
| `word_pronunciation` | 8 | 现代汉语普通话字音辨析 | [[work/knowledge/exams/workbench/type_review_queue/word_pronunciation.md|打开]] |
| `word_usage` | 7 | 词语/熟语语境使用辨析 | [[work/knowledge/exams/workbench/type_review_queue/word_usage.md|打开]] |

## 放行规则

1. 题段、清洗稿、原始 MinerU、原始 PDF 和解析候选（如有）定位一致，才允许进入小问级知识点草拟。
2. 评分只能记录为题面候选或官方评分；没有独立评分材料时保持未核验。
3. `candidate_atomic_exam_point` 只是检索标签；`atomic_exam_point`、四层、四翼和教材 KP 关系仍不得写入正式节点。
4. 只有题文—答案/评分—教材 KP 三方证据闭合，才允许从 M0 升级 M1 以上。

| 产物 | 路径 |
|---|---|
| JSONL 队列 | `work/knowledge/exams/workbench/exam_type_review_queue.jsonl` |
| 题型目录 | `work/knowledge/exams/workbench/type_review_queue/` |
| 生成脚本 | `scripts/build_exam_type_review_queue.py` |
