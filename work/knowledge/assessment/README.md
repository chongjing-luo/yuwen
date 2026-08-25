# 命题与题库（S8 环节）

## 目录内容

| 文件 | 内容 |
|---|---|
| `item_bank.jsonl` | 题库：每行一题。`IB-AU-*` 为项目原创（绑定知识卡 KP，含评分点与反例路径）；`IB-SC-*` 为真题题型参照（保持 `candidate_only_M0` 状态与全量溯源字段，不进学生卷） |
| `blueprint_X3U01_poetry_slice.json` | 组卷蓝图示范：KP 权重 ← 单元图谱 + 课文重点；题型分布 ← 17 年真题语料统计；总分/时长/评分原则/诚实边界 |
| `学生卷_*.md` / `教师卷与评分量规_*.md` | 组卷器产物（同源生成，P-11） |

## 题库条目 schema

```jsonc
{
  "item_id": "IB-AU-002",            // IB-AU-* 原创 / IB-SC-* 真题参照
  "origin": "项目原创",
  "type": "默写 | 古诗鉴赏-简答 | 古诗鉴赏-选择 | ...",
  "score": 8, "time_minutes": 10,
  "kp_ids": ["KP-CARD-X3-U01-01-004"],   // 原创题必填且须解析到知识卡
  "stem": "…",
  "expected_evidence": "…",          // 什么证据出现算学会（先于评分，P-37）
  "scoring_points": [{"point": "…", "score": 4}],
  "normal_path": "…",                // 反例路径（U7 同样适用于测验）
  // 真题参照另含：
  "exam_node_id": "GK-NC3-2016-Q003-1", "exam_id": "…", "year": 2016,
  "prompt_source": "…", "analysis_source_sha256": "…",
  "kp_candidate": "…", "candidate_status": "candidate_only_M0"
}
```

## 蓝图 schema

见 `blueprint_X3U01_poetry_slice.json`。硬性纪律：

1. KP 权重必须给 `basis`（图谱定位或语料统计），不接受"感觉重要"（K1）；
2. 蓝图必须引用 `lesson_ref` 与 `homework_ref`——测评是四站闭环的第三站（K3）；
3. `candidate_only_M0` 条目只能作变式参照进教师卷（题—KP 映射未闭合前不进学生卷）；
4. 评分原则必须包含解释分层要求（U6：推断写成诗写可检出、可扣分）。

## 工具

```bash
python3 scripts/validate_assessment_package.py work/knowledge/assessment/blueprint_X3U01_poetry_slice.json
python3 scripts/build_assessment_paper.py work/knowledge/assessment/blueprint_X3U01_poetry_slice.json
```

## 边界

真题语料的题—KP 映射目前全部 M0（`work/knowledge/exams/workbench/` 登记在案）；官方答案与评分标准大多未取得。本目录的示范卷为桌面组卷，信度效度待真实施测。M0→M1/M2 映射的推进记录在 `dev/knowledge-extraction-foundation/PROJECT_INDEX.md`。
