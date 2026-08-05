---
schema_version: "2.0-candidate"
mapping_id: "MAP-EXAM-KP"
status: "drafted"
upstream_exam_ids: []
upstream_card_ids: []
producer: "<agent-id>"
reviewers: []
version: "0.1.0"
---

# 高考考点映射总表

## 1. 真题小问→KP关系

| Relation-ID | Question-ID | M等级 | KP-ID或N/A | 相同能力动作/直接调用点 | 真题证据 | 教材证据 | 推理与边界 |
|---|---|---|---|---|---|---|---|

M0记录不得携带KP；M1/M2必须具备真题与教材双向证据。

## 2. 81张知识卡反向核对

| Card-ID | 关联小问 | 最高M等级 | 无映射说明 |
|---|---|---|---|

## 3. 跨年比较

| 口径 | 分子 | 分母 | 频次/结果 | 可复算方法 |
|---|---:|---:|---:|---|

## 4. 冲突、不确定性与版本

| Issue-ID | 对象 | 问题 | 状态 | 处理 |
|---|---|---|---|---|
