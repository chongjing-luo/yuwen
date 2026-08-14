# SG-METHOD 评估协议（候选，2026-08-09）

状态：`protocol_ready_not_run`。本文件冻结评估规则，不代表方法通过，也不产生 `cutover_batch_id`。

## 1. 目的与适用范围

SG-METHOD 用于评估教材知识点提取方法是否能在未见生产输出的留出资料上稳定恢复教材事实、任务、知识点、标签、证据和关系，并支持固定教学查询。评估对象是方法输出，不是对现有 81 张卡、28 份单元图和 5 份册表的追溯性自评。

当前配置：`work/knowledge/_meta/sg_method_config_20260809.json`；观察 Schema：`work/knowledge/_meta/schemas/sg_method_observation.schema.json`；计分器：`scripts/score_sg_method_metrics.py`。

## 2. 污染边界与留出集

- 现有教材交付物已暴露于生产或历史评审，不能作为真正前瞻盲测 Gold。
- 新来源或新契约产生后，由协调者按 `book_code × material_type` 分层封存 12 张卡、4 份单元图和 1 份册表；在封存完成前，配置保持 `blocked/pending_new_source`。
- 生产者、查询评估者和外部教师不得读取 Gold；Gold 标注者不得读取生产输出；仲裁者须在两份独立原始标注封存后才可读取双方记录。
- 每个留出交付物保存来源版本、内容 SHA、封存时间和角色记录。任何揭盲、替换、缺失或重复都登记为 protocol deviation，并暂停该批次。

## 3. Gold 生成与一致性

两名独立标注者（A/B）分别标注事实、任务、KP 集合、标签、Claim—Evidence、quote span/locator 和关系边；第三人仅对分歧进行仲裁，生成 adjudicated Gold。Gold 记录使用 `sg_method_gold_record.schema.json`，模板不进入分母。

每个交付物的观察必须带 `gold_id` 与 Gold SHA，并与封存 Gold manifest SHA 对齐；Gold 记录还必须保存 annotator ID、封存时间、来源内容 SHA、标注 SHA 和 `independent_from_production`。仅在文字中声明“已双标”不构成可审计证据。

放行前最低一致性要求：

- 关键类别 Krippendorff α ≥ 0.80；
- KP 集合配对 F1 ≥ 0.85；
- 未达到要求时不得用平均值“修复”，应重训/重标并报告未通过批次。

## 4. 样本与指标硬门

按交付物聚类、按 `book_code × material_type` 分层；KP 与三类标签报告点估计和 95% bootstrap 区间，其余硬门指标报告点估计、分子/分母和逐交付物诊断。硬门如下：

计分输出同时保存每个 `book_code × material_type` 层的交付物数和点估计，避免总体聚合掩盖某一层的零分母或系统性漏项。

| 维度 | 通过标准 |
|---|---:|
| 关键事实召回率 | 100% |
| 关键任务召回率 | 100% |
| KP precision / recall / F1 | 各 ≥ 90% |
| 标签 macro-F1 | ≥ 85% |
| Claim—Evidence 支持准确率 | 100% |
| quote span / locator 准确率 | 100% |
| 关系边 precision | ≥ 90% |
| 未支持正式主张率 | 0% |
| 固定教学查询完成率 | ≥ 90% |
| 查询事实/证据准确率 | 100% |
| 120 秒内完成查询 | 至少 11/12 |
| 外部教师可用性中位数 | ≥ 4/5，至少 3 人 |
| 严重教学事实错误 | 0 |

标签 macro-F1 固定覆盖三个维度：`primary_dimension`（人文/语言）、`knowledge_type`（事实、概念、程序、策略、解释、价值辨析）和 `four_layer`（必备知识、关键能力、学科素养、核心价值）；全集写入配置，Gold 有支持的类别即使生产输出为零也进入分母，缺失维度不从均值中删除。

零分母统一输出 `N/A + reason`，不得把 0/0 转换为 100%。任何交付物的硬门指标出现 `N/A`，该批次不通过；不得删去无适用项来提高均值。Bootstrap 若任一重采样出现零分母，则区间报告 `N/A` 并保留无效重采样数。

Bootstrap 预登记：10,000 次、seed `20260809`、交付物为聚类单位、在每个 `book_code × material_type` 层内重采样。报告点估计、区间、层样本数和缺失分母。

## 5. 固定教学查询与教师检查

查询集冻结在 `sg_method_query_manifest_20260809.json`，必须恰好覆盖 `QRY-01` 至 `QRY-12`，不得重复、增删或换题。记录每条是否完成、事实/证据是否正确、秒数、评估者；报告 median 和 P90。

外部教师至少 3 人，使用 1—5 可用性评分并记录严重教学事实错误。项目成员不得冒充外部教师；少于 3 人只能报告 `blocked`。

## 6. 计分与状态机

计分器输出两个状态：

- `metric_status`：仅表示已登记观察数据是否满足全部指标硬门；
- `status`：只有在 `observation.status=complete` 且配置状态为 `pilot`/`passed`，并且 `metric_status=passed` 时才可为 `passed`。

此外，`status=passed` 还必须同时满足机器控制：评估集 `selection_status=sealed` 且交付物恰为 12 张卡、4 份单元图和 1 份册表；候选 ID 与观察 ID 一致；Gold manifest SHA、逐交付物 Gold SHA、双标角色和污染状态均闭合；查询清单 Schema、`frozen`、SHA、12 个 ID 和目标候选集均闭合；查询评估者、外部教师与配置角色一致且教师 ID 不重复。配置仍为 `blocked/pending_new_source` 或任一控制缺失时，即使 `metric_status=passed`，总体仍是 `blocked`。

因此，合成正例可用于验证计分逻辑，但不会改变当前配置的 `blocked` 状态。`not_run`、缺 Gold、缺查询、缺教师、零分母、污染或 Schema/语义校验失败均保持 `blocked`，不得写成“未发现问题”或“通过”。

失败时保留原始观察、计分输出和错误列表；只允许在新的批次、新的封存 Gold 和新的 SHA 回执下重跑。不得覆盖失败报告，不得把候选输出迁移进 canonical 教材层。

## 7. 当前执行结论

本协议、Schema、模板和计分器已完成机器回归；真实教材留出集尚未产生，Gold/查询/教师观察均为 `not_run`。因此当前结论固定为：`SG-METHOD = blocked (pending_new_source)`。
