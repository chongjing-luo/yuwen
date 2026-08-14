# SG-METHOD 独立审查与迭代记录（2026-08-09）

审查方式：一名未参与本轮计分器编写的 reviewer 只读检查协议、Schema、计分器和回归夹具；未改动 canonical 教材或试卷文件。

## 发现与处理

| 审查发现 | 处理结果 |
|---|---|
| `pilot` 状态可绕过未封存样本，且未校验 12 卡/4 图/1 册表 | 已接入 `selection_status=sealed`、候选 ID 完整匹配和 12/4/1 数量门；当前配置仍 `pending_new_source`，不能放行。 |
| Gold 双标、仲裁和污染边界只写在文字里 | 已加入 Gold manifest SHA、逐交付物 Gold SHA、双标角色、α、KP 配对 F1、sealed 和 contamination 状态控制；缺任一项保持 blocked。 |
| Gold 记录自身缺少来源/标注血缘字段 | Gold Schema 已增加 annotator ID、封存时间、来源内容 SHA、标注 SHA 和独立生产声明字段；模板仍明确为非 Gold。 |
| `F1(0,1,1)` 被错误记为 N/A | 已修正为计算值 0；仅分母为 0 时记 N/A。 |
| 标签宏 F1 可遗漏 Gold 类别 | 已固定三维标签全集并要求每个交付物登记类别计数；输出分维度和总 macro-F1。 |
| 查询清单可被替换或未冻结，目标 Artifact 未绑定候选集 | 已校验 manifest Schema、frozen、ID 唯一性、SHA 和目标候选 ID；配置缺 hash 时不放行。 |
| 未完成查询可被计入事实准确率；教师可重复计数 | 事实/证据正确必须同时完成；教师 evaluator ID 去重并与 roles 绑定。 |
| `correct > total` 等计数异常可产生超过 100% | 已加入 claim-evidence、quote、事实/任务和 unsupported claim 的语义上界检查。 |
| 总体聚合可能掩盖某一层零分母 | 已输出逐交付物与 `book_code × material_type` 分层点估计；任一硬门分母 N/A 会阻断。Bootstrap 零分母则区间显式 N/A。 |

## 保留的限制

- 当前没有新来源留出集，因此没有真实 Gold、教师观察或方法结果；合成正/负夹具只测试计分边界。
- Krippendorff α 和 KP 配对 F1 由封存 Gold 控制记录提供，尚未在真实双标原始记录上计算；达到真实留出集阶段前不得填入占位通过值。
- Bootstrap 区间按研究计划只覆盖 KP 和三类标签；其余硬门使用点估计和逐交付物分母诊断。

## 审查结论

修正后的机器回归为 `9 passed`，全量项目回归为 `69 passed`。SG-METHOD 仍为 `blocked (pending_new_source)`，没有生成 `cutover_batch_id`，也没有把合成结果写入 canonical 层。
