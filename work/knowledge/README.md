# 知识点提取执行区

本目录供教材与高考阶段按《语文备课系统：教材知识点提取与评价执行方案（V2.4）》协作。教材锁定记录为 `TEXTBOOK-LOCK-2.0-textbook`（81 卡、28 图、5 册表，共114项）；2008—2024 试卷已完成结构化批处理和 `SG-EXAM-CAL` 候选冻结，当前进入顶层节点→真实小问拆解与知识点抽取，教材—真题确定性映射仍保持 M0。

## 开始前

```bash
python scripts/validate_knowledge_base.py
```

只有基础校验为 `passed` 时才能领取任务。正式进度以 `_meta/deliverables.jsonl` 为准，不以聊天或文件数量为准。

## 目录

```text
work/knowledge/
├── _meta/
│   ├── sources.jsonl
│   ├── artifacts.jsonl
│   ├── source_relations.jsonl
│   ├── split_manifest.jsonl
│   ├── deliverables.jsonl
│   ├── taxonomy.yaml
│   ├── rubrics.json
│   ├── schemas/
│   └── validation_reports/
├── _templates/
├── _reviews/
├── 必修上册/ … 选择性必修下册/
├── 册级汇总/
├── 高考分析/
└── 全局总览/
```

## 2026-08-07 G2 校准状态

原定 10 张知识卡和 5 张单元图谱已完成双角色评分，所有评审均达到 92 分或以上且未触发 R01–R10；U06 补齐的 CARD-B1-U06-03/04 也已完成预门禁双评。评分记录位于 `_reviews/scores/g2_reviews_20260807.jsonl`，汇总位于 `_reviews/scores/g2_review_summary_20260807.md`。教材契约冻结记录见 `dev/knowledge-extraction-foundation/04_execution/contract_freeze_20260807.md`。

## 2026-08-06 首轮校准执行状态

教材 81 张卡、28 份图谱和 5 份册级总表已完成 `accepted` 并锁定；高考首轮已生成 310 个顶层题目节点，尚未将其误报为最终小问或 M1/M2 映射。

任务包位于 `dev/knowledge-extraction-foundation/05_task_packets/`；本轮覆盖必修上册 U02–U06。U06 图谱明确标出规划中的 U06-03、U06-04 尚未交付，U04 的真实学生实施材料也仍待补证。

其余批次仍须遵循 `drafted → linted → primary_reviewed → secondary_reviewed → accepted`；已冻结契约不得通过自由文本绕过门禁。教材 114 项已完成锁定；高考结构包和验证入口见 `work/knowledge/高考分析/SG-EXAM-CAL-RECEIPT.md`、`scripts/validate_exam_calibration_manifest.py` 和 `scripts/validate_exam_kp_extraction_drafts.py`。

## Agent执行协议

1. 协调者从 `deliverables.jsonl` 分配一个 `deliverable_id`，并生成一份 `agent_task_packet.md`；执行者不得自行抢占共享文件。
2. 执行者只修改任务包允许的输出文件；`_meta/*.jsonl`、受控词表、量表和其他agent文件只读。
3. 所有事实性内容先登记证据；MinerU产物只用于检索和定位，直接引文必须回看canonical PDF。
4. 输出必须使用对应V2模板。知识卡的任务群、状态、课程类型等只能使用 `taxonomy.yaml` 中的值。
5. 执行者完成自检后运行校验器。结构通过才可申请从`drafted`转为`linted`。
6. 评分写入独立评审文件，协调者审核后统一合并状态；不得由生产者把自己改成`accepted`。
7. 上游版本变化时，受影响下游必须进入`review_required`，不得继续沿用旧评分。

## 共享文件合并规则

- `sources.jsonl`、`artifacts.jsonl`、`source_relations.jsonl`、`split_manifest.jsonl`、`deliverables.jsonl`与`taxonomy.yaml`只由协调者合并。
- 每个执行者在任务返回中列出“请求合并的字段变化”，不直接并发修改共享账本。
- 一份交付文件同时只允许一个owner；评审者只写自己的评审记录。
- ID一经分配不得因标题、文件名或人员变化而修改。

## 当前边界

- 现有教材核心产物已全部锁定；任何上游变化仍需触发 `review_required`。
- 高考 17 年主批次已有本地 PDF/MinerU 快照并完成结构化；来源主体、下载 URL 和解析卷权威等级尚未全部核验，故当前只允许候选结构节点和 M0，不建立 M1/M2 映射。
- `TB2→B2`的`edition_match`当前为`unknown`，教师用书意见必须保留该边界。

## 基础设施命令

首次生成账本：

```bash
python scripts/bootstrap_knowledge_infrastructure.py
```

账本已存在时脚本会拒绝覆盖。只有协调者确认重建影响后才可使用：

```bash
python scripts/bootstrap_knowledge_infrastructure.py --force
```

完整测试：

```bash
python -m unittest discover -s tests -v
```
