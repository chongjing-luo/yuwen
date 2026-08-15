---
name: yuwen-organize
description: 高中语文资料无损整理（资料轴）。当需要把原件转换为整理件（PDF解析/切分/清洗/OCR）时使用；教材与试卷已有既定管线，新类型按配方扩展。
---

# 无损整理（资料轴 · S0）

服务机制节点：**K1**。规则：MM-S0-05（P0）、MM-S0-09（P0）。

## 输入

- L0 原件（或经 intake 裁决为 process_only 的 inbox 件）+ 类型配方（教材/试卷/文献…）

## 步骤

1. 选配方：教材 → MinerU 解析 + 按课切分（既有 `mineru_client.py`/`split_by_lesson.py` 管线）；试卷 → 切分结构化（`split_sichuan_gaokao.py` 系）；新类型 → 先在 S0 手册登记配方参数再执行。
2. 执行确定性转换：同输入同输出，中间产物只落 `Tmp/work/`（随时可删）【MM-S0-05】。
3. 命名与登记：整理件按 ID+后缀命名（如 `SRC-PKG-X3-001_氓离骚`），头部补 front matter 五件套，登记 sources/artifacts/split_manifest 账本【MM-S0-09】。
4. catalog 增量【MM-S0-04】。

## 门禁（放行条件）

- 抽样删除一个整理件后重跑管线可逐字节重建（SHA 核对）【MM-S0-05 判据】；
- front matter 五件套齐全；账本（validate_knowledge_base）仍 passed。

## 产出

- 整理件（登记入册）+ 账本增量 + catalog 增量
