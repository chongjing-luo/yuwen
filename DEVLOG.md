---
document_type: development_log
phase: 开发阶段
version: 3
date: "2026-08-15"
rule: "更新本文件时：旧版本整体移入 docs/devlog/archive/DEVLOG_<日期>_v<序号>.md（并在其头部标注各条目完成情况），本文件只保留最新内容；条目保持简要：方向 + 验收标准各一行"
---

# 开发日志（当前优化方向）

> 开发阶段的每轮工作从本文件开始。完成的方向在下次更新时移入归档并标注结果，此处只留最新清单。历史见 `docs/devlog/archive/`。路线总纲：`docs/architecture/项目设计方案.md` §10。

## 当前方向（按优先级）

1. **catalog 最小版实装（本轮）** — build_catalog.py + INDEX/交叉视图 + 消费登记；验收：视图与账本一致、零消费体检可跑。
2. **资料轴 skill ×4 + yuwen-flow（本轮）** — intake/organize/curate/catalog 四 skill 步骤引用 MM-S0 条目；验收：每个 skill 声明读/门禁/写三件套。
3. **S0 手册补全（本轮）** — MM-S0-05..09 从 §3.8 编译（无损整理/语义加工/视图生成/消费登记/命名细则）；验收：条目六字段齐。
4. **〔完成〕手册编译** — 十册 75 条首轮编译完成（S3 12/S4 10/S5 10 迁移 + 六册充实），全部六字段格式。
5. **〔完成〕证据轴** — 五类 schema + validate_evidence.py（10 测试）+ admit_pr.py 回流边②准入器（8 测试：触发证据存在性/节点/强制方式/下一版本）；回流边①③已由 analyze_mastery 回教段与 L1 状态机承载。
6. **〔挂起〕《氓》内容工作** — 样板清零暂停于 462→188（O/C1-C4 已清，剩 C5/C6/S 共 19 页）；lesson.json 迁移已完成；K2 锚定 21 处待数组化。恢复条件：所有者指示。
7. **〔完成〕E1 依赖基建 + CI** — package.json/requirements.txt 入库，本地安装验证全量 453 测试绿；.github/workflows/ci.yml（push 跑全量 selfcheck）。旧构建器的 /usr/local 全局路径回退保留但本地依赖优先（清除随 E3 旧构建器归档）。
8. **随路线推进** — 文件名后缀迁移（§3.8）、lib/theme 引擎化（E3）、第二课文切片、真实试教、题-KP M0→M1、新源预处理接入、L0 统一治理（设计方案 §10）。
