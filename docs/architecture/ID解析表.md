# ID 解析表（设计方案 §3.8：机器寻址的唯一规则）

每个 ID 族一条确定性路径规则。文件名 = ID 打头 + 可选人类可读后缀（`CARD-X3-U01-01_氓.md`），**解析一律用前缀匹配**，引用只写 ID。

## 册代码映射

B1=必修上册 · B2=必修下册 · X1=选择性必修上册 · X2=选择性必修中册 · X3=选择性必修下册 · REC=古诗词诵读

## 路径规则

| ID 族 | 解析规则 | 层 |
|---|---|---|
| `CARD-{册}-{U}-{nn}` | `work/knowledge/{册全名}/cards/{ID}*.md` | L1 |
| `UNIT-{册}-{U}` / `BOOK-{册}` | `work/knowledge/{册全名}/units/{ID}*.md` / `册级汇总/` | L1 |
| `KP-CARD-*` | 宿主卡片文件内（表格行） | L1 |
| `IB-*` | `work/knowledge/assessment/item_bank.jsonl` 按 `item_id` 字段查行 | L1 |
| `BP-*` | `work/knowledge/assessment/blueprint_*.json` 按 `blueprint_id` | L2 |
| `HW-*` | `work/teaching/{册}/{课}/homework/homework_package.json` 按 `homework_id`；产物 `学生作业单_{ID}*.md` | L2→L3 |
| `LES-*` | `work/teaching/{册}/{课}/lesson.json` | L2 |
| `TR-*` / `UP-*` | `work/teaching/{册}/{课}/01_文本研究*.md` / `work/teaching/{册}/{单元}/unit_plan.md` | L2 |
| `MAT-*` | `work/knowledge/materials/{ID}*.md` | L1 |
| `SRC-*` / `SRC-PKG-*` | `work/knowledge/_meta/{sources,split_manifest}.jsonl`；解析包实体在 `Data/textbook_extract/` | L0 |
| `GK-*` | `Data/2008-2024·（四川）语文高考真题/exam_extract/{exam-id}/` | L0/L1 |
| `OBS-*` / `GRD-*` | `work/teaching/_classes/{班级}/observations.jsonl` / `grading.jsonl` 按行 `id` 字段 | L4 |
| `MR-*` | `work/teaching/_classes/{班级}/mastery_ledger.jsonl` | L4 |
| `REF-*` / `PR-*` | `work/teaching/_classes/{班级}/reflections/` | L4 |
| `LRN-*` | `.learnings/LEARNINGS.md` 条目 | L4 |
| `MM-{S环节}-{nn}` | `work/manuals/S{环节}-*手册.md` 条目 | 手册层 |
| `TW-*`（工作项） | 设计方案 §6.0 归属表 | — |

新增 ID 族必须先在本表登记规则，再产生数据（否则不可解析 = 不可找）。
