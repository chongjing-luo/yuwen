---
document_type: development_log
phase: 开发阶段
version: 4
date: "2026-08-15"
rule: "更新本文件时：旧版本整体移入 docs/devlog/archive/DEVLOG_<日期>_v<序号>.md（并在其头部标注各条目完成情况），本文件只保留最新内容；条目保持简要：方向 + 验收标准各一行"
---

# 开发日志（当前优化方向）

> 每轮工作从本文件开始；完成移入归档；路线总纲：docs/architecture/项目设计方案.md §10。

## 当前方向（按优先级）

1. **E3 剩余** — v66 构建器已引 lib/theme（0c352f6）；待：v62/v65 旧构建器归档（随其测试一并）、theme.json 正式化；验收：scripts/ 根 meng 构建器数量下降、全量测试绿。
2. **〔挂起〕《氓》内容工作** — 样板 462→188（剩 C5/C6/S 十九页）+ K2 锚定 21 处数组化；恢复条件：所有者指示。
3. **第二课文切片《沁园春·长沙》** — 复制 lesson.json 骨架→填内容→跑门禁（S2→S5 全链）；验收：零新建构建器。
4. **真实试教** — 课堂账唯一来源（L4 目前为零）；教师执行，系统采集。
5. **题-KP M0→M1/M2** — blocked 于官方答案源缺失；有新源时经 yuwen-intake 入册。
6. **〔进行中〕多省试卷库** — 版本2 采集包已入库（978 件/9.9GB，台账+裁决+映射表 EXMAP-V2 979 行落盘，组织约定 spec v1.0）；〔本批完成〕③④已收口：优先批 13 份全过四件契约门禁（MinerU 13/13、questions.jsonl 结构候选 26-44 题/卷、paper.json 含答案纪律、identity_check 检出并换正 XG2-2021 错版主件、OCR 伪影 2 卷已标注）；validate_exam_paper.py + extract_exam_questions.py 落地；catalog 161 实体（+13 PAPER +2 映射表）。待：转型年 40 件核验、题目语义细化（curate）、XG2-2020 漏检补全。
7. **L0 统一治理** — origin.pdf 双份 524MB 去重，需账本手术，专项另议。
