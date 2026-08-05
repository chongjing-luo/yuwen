# 知识点提取执行区

本目录供多个 agent 按《语文备课系统：教材知识点提取与评价执行方案（V2.0）》协作。当前契约状态为 `2.0-candidate`；只有通过10卡+5图校准门禁后，协调者才能改为 `frozen`。

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

- 现有3张卡和1份图谱为`draft_existing`，须按V2返修后重新校验评分。
- 高考评价体系、初中材料、四川政策和四年真题尚未全部取得；相关交付保持`planned`，不得用网络二手材料填补。
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
