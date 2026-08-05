# 首轮校准吞吐证据（2026-08-06）

## 执行结果

- 批次：必修上册 U02–U06
- 产出：10 张知识卡、5 张单元图谱
- 账本状态：15 项从 `planned` 合并为 `drafted`
- 正式验收：0 张卡、0 张图谱进入 `accepted`
- 契约：`2.0-candidate`，尚未通过 G2 冻结门

## 分工与文件范围

| Owner | 知识卡 | 单元图谱 |
|---|---|---|
| `execution_design` | U02-01、U02-02、U02-03 | U02 |
| `evidence_design` | U03-01、U03-02、U03-03、U04-01 | U03、U04 |
| `rubric_design` | U05-01、U06-01、U06-02 | U05、U06 |

所有文件均使用 V2 模板，保留证据表、来源回链、M0 边界和未验收标记。U06 图谱特别标出 U06-03、U06-04 尚未交付；U04 真实学生实施材料尚未取得。

## 验证

```text
python scripts/validate_knowledge_base.py
result: passed
run_id: VAL-20260806-061159+0800
errors: 0
python -m unittest discover -s tests -v
Ran 21 tests — OK
```

## 下一道门

协调者需为这 15 项建立独立 review 记录，依据 `rubrics.json` 完成评分与 R01–R10 否决项检查；只有达到 G2 的 10 卡 + 5 图校准要求，才可将候选 taxonomy、schema 和量表冻结，并继续批量生产。
