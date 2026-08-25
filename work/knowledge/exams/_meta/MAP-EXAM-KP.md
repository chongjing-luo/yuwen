---
schema_version: "exam-kp-map-0.2-candidate"
deliverable_id: "MAP-EXAM-KP"
status: "drafted"
calibration_id: "SG-EXAM-CAL-2008-2024"
structural_node_manifest: "work/knowledge/exams/workbench/exam_response_nodes_top_level.jsonl"
structural_validation: "work/knowledge/_meta/validation_reports/exam_kp_extraction_validation.json"
source_ids: []
textbook_lock_id: "TEXTBOOK-LOCK-2.0-textbook"
textbook_deliverables_sha256: "63a2974acd668e6b9a4b55f4c0a12b4adc42fb9e4df806e0a0a2d336fb723baa"
textbook_validator_run_id: "VAL-20260809-025336+0800"
textbook_validator_sha256: "9ac9195f15aadddcaadb45f92fc31f93867e4daa22cb6c25568130a2dbb2ed58"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
producer: "throughput_generator"
reviewers: []
version: "0.4.0"
---

# 高考考点映射总表

> 当前采用保守映射：全量已生成 310 个稳定顶层题目节点；其中 2008—2016、2024 十个年度已进一步生成 240 个候选作答节点。没有答案/评分标准和教材 KP 双向证据时，统一记为 M0。

## 1. 覆盖状态

| 资源 | 数量 | 状态 |
|---|---:|---|
| 教材知识卡 | 81 | accepted；已纳入 `TEXTBOOK-LOCK-2.0-textbook` |
| 高考年度结构包 | 17 | 2008—2024；结构验证 17/17 通过 |
| 顶层题目节点 | 310 | 全量结构节点，均保留 M0 |
| 已拆作答节点 | 240 | 2008—2016、2024 十年；候选结构，均 M0 |
| 尚未拆作答节点（TOP 占位） | 108 | 2017—2023 其余年度仍仅有 TOP 节点；此处按 TOP 题目节点计，不与 240 个作答节点混算 |
| 已登记小问级候选批次 | 337 | 2008—2024 首轮批次（含 2018—2020 Q7 组题可逆小问拆分、Q8/Q9 任务单元、2021—2024 文言文翻译、2016—2024 名篇名句默写、古诗词鉴赏、现代文信息类阅读、文学类文本阅读、实用类文本阅读、文言文基础阅读及材料/命题作文）；答案/评分未独立核验，均 M0 |
| M1/M2/M3 关系 | 0 | 禁止在来源和双向证据未核验前生成 |

## 2. 映射表

| Exam | 节点/小问ID | KP-ID | 等级 | 证据状态 |
|---|---|---|---|---|
| 2008—2024 结构化节点 | 310 个 `…-Qxxx-TOP` | N/A | M0 | 见 `exam_response_nodes_top_level.jsonl`；TOP 不是最终小问ID |
| 十年候选作答节点 | 240 | N/A | M0 | 见各年度 `*-response_nodes_vertical_slice.jsonl`；仍待正式答案/评分和双向证据 |
| 其余年度作答节点 | 108 个顶层节点 | N/A | M0 | 尚未进入垂直拆解批次，不把 TOP 当最终小问ID |

## 3. 允许升级条件

1. 题卷、答案和评分标准来源均可核验。
2. 小问ID稳定且题干动作清楚。
3. 教材KP为accepted并有双向证据。
4. M1仅用于明确调用相同教材动作；一般题型相似性保持M0。

## 4. 当前首轮产物

- [顶层节点 JSONL](exam_response_nodes_top_level.jsonl)
- [抽取草稿总回执](EXAM-KP-EXTRACTION-DRAFT-REPORT.md)
- [小问级候选批次与剩余节点回执](EXAM-KP-EXTRACTION-DRAFT-REPORT.md#已执行的小问级候选批次)
- [节点验证报告](../../work/knowledge/_meta/validation_reports/exam_kp_extraction_validation.json)
- [SG-EXAM-CAL 回执](SG-EXAM-CAL-RECEIPT.md)

| 版本 | 日期 | 修改者 | 变更 |
|---|---|---|---|
| 0.1.0 | 2026-08-06 | throughput_generator | 建立全量M0映射骨架 |
| 0.2.0 | 2026-08-09 | coordinator | 接入2008—2024结构校准、310个TOP节点和M0边界；保留小问级与M1/M2为待办 |
| 0.3.0 | 2026-08-09 | coordinator | 新增2009—2011三年、72个候选作答节点；七年切片共171节点，仍为M0 |
| 0.4.0 | 2026-08-09 | coordinator | 新增2012、2014、2015四年批次中的三年、69个候选作答节点；十年切片共240节点，仍为M0 |
| 0.5.0 | 2026-08-09 | coordinator | 新增 2016—2017 语言文字运用稳定小问候选批次 10 条；小问级候选批次累计 175 条，仍为 M0 |
| 0.6.0 | 2026-08-09 | coordinator | 新增 2021—2024 语言文字运用小问候选批次 20 条；小问级候选批次累计 195 条，2024 Q21 权威缺失门禁保留 |
| 0.7.0 | 2026-08-09 | coordinator | 将 2018—2020 Q7 组题拆为 9 个可逆小问候选节点；小问分值保持 N/A，累计 204 条，仍为 M0 |
| 0.8.0 | 2026-08-09 | coordinator | 新增 2021—2024 文言文翻译候选批次 5 条；2021—2023 共享解析范围显式保留，累计 209 条，仍为 M0 |
| 0.9.0 | 2026-08-09 | coordinator | 新增 2016—2024 名篇名句默写候选批次 13 条；2016、2024 分支保留，累计 222 条，仍为 M0 |
| 1.0.0 | 2026-08-09 | coordinator | 新增 2016—2024 古诗词鉴赏候选批次 15 条；2018—2020 组题共享解析范围显式保留，累计 237 条，仍为 M0 |
| 1.1.0 | 2026-08-09 | coordinator | 新增 2016—2024 现代文信息类阅读候选批次 21 条；关联解析范围显式保留，累计 258 条，仍为 M0 |
| 1.2.0 | 2026-08-09 | coordinator | 新增 2016—2024 文学类文本阅读候选批次 22 条；关联解析范围显式保留，累计 280 条，仍为 M0 |
| 1.3.0 | 2026-08-09 | coordinator | 新增 2016—2024 实用类文本阅读候选批次 22 条；图表/图文原始链路保留，累计 302 条，仍为 M0 |
| 1.4.0 | 2026-08-09 | coordinator | 新增 2021—2024 文言文基础阅读候选批次 12 条；断句/词语/内容题与翻译分开登记，累计 314 条，仍为 M0 |
| 1.5.0 | 2026-08-09 | coordinator | 新增 2016—2024 材料/命题作文候选批次 9 条；作文答案/评分不自动抽取，累计 323 条，仍为 M0 |
| 1.6.0 | 2026-08-09 | coordinator | 新增 2018—2020 Q8/Q9 任务单元候选批次 14 条；小问分值保持 N/A，2020 OCR 与 2018 图示链路显式保留，累计 337 条，仍为 M0 |
| 1.7.0 | 2026-08-09 | coordinator | 按独立 PDF 复核修复 2024 Q009 题干/解析的后续文言文污染；原始 prompt_text_raw、MinerU 和 PDF 保留，更新派生哈希与队列索引 |
