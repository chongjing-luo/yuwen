# 高考试卷结构化处理输出

本目录保存清洗副本、材料、题目级分割和题型索引。原始 PDF 与 MinerU 结果仍在上级目录，均为只读输入。

- 2008 校准切片：`GK-SC-2008/`
- 2009—2015 结构化批次：`GK-SC-2009/` … `GK-SC-2015/`
- 2016—2024 结构化批次：`GK-NC3-2016/` … `GK-NCA-2024/`
- 运行脚本：`scripts/split_sichuan_gaokao.py`
- 批次验证：`scripts/validate_sichuan_gaokao_batch.py`
- 处理协议：[试卷处理协议-v0.1](../../../work/knowledge/高考分析/试卷处理协议-v0.1.md)

`clean_md/` 是清洗副本，`segments/` 是题目级 canonical 文件，`materials/` 是材料对象，`answers/` 是解析卷候选答案/解析；其中 `answer_candidates.jsonl` 是从 `answer_index.jsonl` 可逆截取的候选层，不是官方答案或评分标准。`by_type/` 只保存双链索引，`ledger/` 和 `review/` 保存机器清单与异常。答案/评分来源审计见 `work/knowledge/高考分析/EXAM-ANSWER-SCORING-AUDIT-20260809.md`。

2009—2015 每年均已生成空白卷/解析卷各 21 个顶层题目；2016—2017 各 12 个、2018—2020 各 10 个、2021—2024 各 22 个。各年度对应的 `review/validation-YYYY.json` 均通过结构门禁；2022 空白卷 Q6、2024 解析卷 Q21/Q22 的文本层题号缺失已生成占位卡并标记 PDF 复核。解析卷中的答案/解析仍是本地未核验候选，OCR 疑点与材料边界保留在 review 清单中，尚未进入教材—真题 M1/M2 映射。

垂直切片完成后，跨年度题型归并队列见 `work/knowledge/高考分析/EXAM-TYPE-KP-REVIEW-QUEUE-20260809.md`；30 份题型页面对 359 个作答节点均显式链接题段、清洗整卷、原始 MinerU、原始 PDF 和解析候选（如有），便于从归并视图回溯而不改动原始材料。`scripts/validate_exam_type_review_queue.py` 同时校验四类来源路径与页面链接覆盖。该队列只提供人工清洗顺序和候选考点标签，正式知识点与教材映射仍需三方证据闭合。

已执行的小问级候选批次：

- 字音辨析（2008—2015）：`work/knowledge/高考分析/kp_batches/word_pronunciation_2008_2015.md`
- 字形、词语、病句（2009—2015）：`work/knowledge/高考分析/kp_batches/core_language_use_2009_2015.md`
- 文言实词、虚词（2009—2015）：`work/knowledge/高考分析/kp_batches/classical_language_2009_2015.md`
- 文言文内容概括/信息筛选（2009—2015）：`work/knowledge/高考分析/kp_batches/ancient_content_2009_2015.md`
- 文言文翻译（2009—2015）：`work/knowledge/高考分析/kp_batches/classical_translation_2009_2015.md`
- 名篇名句默写（2009—2015）：`work/knowledge/高考分析/kp_batches/classical_memorization_2009_2015.md`
- 古诗词鉴赏（2009—2015）：`work/knowledge/高考分析/kp_batches/poetry_appreciation_2009_2015.md`
- 现代文信息类阅读（2009—2015）：`work/knowledge/高考分析/kp_batches/modern_informational_2009_2015.md`
- 文学类文本阅读（2009—2015）：`work/knowledge/高考分析/kp_batches/literary_reading_2009_2015.md`
- 材料/命题作文（2009—2015）：`work/knowledge/高考分析/kp_batches/topic_writing_2009_2015.md`
- 语言文字综合表达（2009—2015）：`work/knowledge/高考分析/kp_batches/language_expression_2009_2015.md`

以上批次均保留题干—PDF—解析源双链，候选答案不等同于官方答案，且全部保持 `M0 / kp_id=N/A`。
