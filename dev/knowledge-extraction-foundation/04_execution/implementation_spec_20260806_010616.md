# Knowledge Extraction Foundation — Implementation Spec

## First-throughput path

```text
Data/textbook + Data/textbook_extract
  → discover source packages
  → normalize Source / Artifact / SplitManifest / Deliverable records
  → write JSONL registries under work/knowledge/_meta
  → validate contracts, counts, IDs, paths, hashes and dependency links
  → write one machine-readable validation report
```

The path uses real project files. It does not synthesize knowledge conclusions.

## Slice contracts

### `bootstrap_knowledge_infrastructure.py`

- Purpose: 从现有教材与解析目录生成基础账本和120项交付清单。
- Input: 项目根目录中的 `Data/textbook/`、`Data/textbook_extract/`。
- Input format: PDF、MinerU结果目录和文件名约定。
- Output: `_meta/*.jsonl`。
- Output format: UTF-8 JSON Lines，一行一条记录，键排序稳定。
- Side effects: 仅在目标文件不存在时原子写入；显式 `--force` 才可替换生成账本。
- Errors: 输入缺册、包计数不符、页码指纹无法唯一映射或目标已存在时非零退出。
- Split trigger: 若以后引入数据库或远程来源，应新增独立适配器，不在本脚本增加输出模式。

### `validate_knowledge_base.py`

- Purpose: 对基础账本、契约和已有交付物执行确定性一致性检查。
- Input: `work/knowledge/` 根目录。
- Input format: JSON/JSONL、Markdown模板及已存在交付文件。
- Output: 一份 JSON 校验报告和控制台摘要。
- Output format: 包含 `run_id`、计数、检查项、错误、警告和结果。
- Side effects: 原子写入 `_meta/validation_reports/latest.json`。
- Errors: 任一硬错误时退出码1；契约或输入不可读时退出码2。
- Split trigger: 内容质量、引文目视核验或语义评分出现时，另建人工评审工具。

## Data contracts

- `sources.jsonl`: 来源实体；Source 与本地 Artifact 分离。
- `artifacts.jsonl`: 文件载体、哈希、派生关系与真实性状态。
- `source_relations.jsonl`: 来源之间的 `excerpt_of`、`edition_match` 等受控关系。
- `split_manifest.jsonl`: 144 个切分包到6个规范主PDF的一基页码映射。
- `deliverables.jsonl`: 120 项核心业务产物、依赖、状态、负责人和目标路径。
- `taxonomy.yaml`: JSON-compatible YAML；所有受控枚举的唯一候选来源。
- `rubrics.json`: 六类成果的100分量表、单项门槛和总分门槛。
- `schemas/*.schema.json`: JSON Schema 2020-12 候选契约。

## Acceptance criteria

- 144 package sources = 113 student + 31 teacher；每包有唯一 canonical split PDF artifact。
- 144 条 split manifest 均满足页数恒等式，逐页规范化文本指纹（空文本页回退渲染指纹）与顺序连续性共同唯一回链主 PDF，并完整覆盖每册主文件。
- 120 deliverables = 81 cards + 28 unit graphs + 5 book summaries + 4 exams + 1 mapping + 1 global map。
- 两个重复 `13_` 的选择性必修下册源包拥有不同永久 Source、Artifact 和 Deliverable ID。
- 18 个任务群名称、状态机、课程类型、核心素养及学业质量使用边界均进入受控词表。
- 六套量表权重各为100，门槛与V2计划一致。
- 现有4个试产件只标记 `draft_existing`，不计入 `accepted`。
- 首通命令退出0并生成可复核报告；完整测试套件通过。

## Observability questions

1. 本次运行实际发现了多少学生包、教师包和交付项？
2. 哪个 Source、Artifact、页码映射或依赖首先失败？
3. 报告对应哪次运行、哪条命令和哪个代码提交？
4. 是否有凭证、签名URL或原文大段内容进入日志？（必须为否）

## Simplification debt

- `scaffold-simple:` 当前校验器只做结构、计数、ID、哈希、路径和状态检查；原因是语义评审必须由后续 agent 按量表执行。替换触发：G2 校准发现可机械判定的新规则。跟进责任：校准协调 agent。
- `scaffold-simple:` 未取得的外部规范来源使用显式缺失登记，不创建虚假记录。替换触发：原件进入 `Data/reference/`。跟进责任：来源治理 agent。
