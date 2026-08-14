# Agent task packet — B2 U01–U03 card batch

## Assignment

- Owner: `execution_design`
- Deliverables: `CARD-B2-U01-01`…`CARD-B2-U03-03`
- Scope: 必修下册 U01–U03；知识卡 9 张。图谱必须等9张卡全部 `accepted` 后另行领取。

## Allowed outputs

- `work/knowledge/必修下册/cards/CARD-B2-U01-01.md`
- `work/knowledge/必修下册/cards/CARD-B2-U01-02.md`
- `work/knowledge/必修下册/cards/CARD-B2-U01-03.md`
- `work/knowledge/必修下册/cards/CARD-B2-U02-01.md`
- `work/knowledge/必修下册/cards/CARD-B2-U02-02.md`
- `work/knowledge/必修下册/cards/CARD-B2-U02-03.md`
- `work/knowledge/必修下册/cards/CARD-B2-U03-01.md`
- `work/knowledge/必修下册/cards/CARD-B2-U03-02.md`
- `work/knowledge/必修下册/cards/CARD-B2-U03-03.md`

## Source bindings

- B2 U01: `SRC-PKG-B2-001`…`SRC-PKG-B2-004`
- B2 U02: `SRC-PKG-B2-005`…`SRC-PKG-B2-008`
- B2 U03: `SRC-PKG-B2-009`…`SRC-PKG-B2-012`
- 课程标准：`SRC-CURR-2020`
- 直接引文必须回看对应规范教材 PDF；MinerU 解析物仅作检索和定位。

## Execution constraints

- 使用冻结教材契约 `TEXTBOOK-CONTRACT-2.0-textbook`、V2模板和受控枚举。
- 每条事实性主张登记 EV-ID；未取得真题小问双向证据时，高考衔接只能保持 M0 且 KP/真题小问/双向证据字段为 N/A。
- 教师用书若未确认同版，只写 `edition_match=unknown`，不得把学生教材提示当教师用书意见。
- 先逐卡重写、运行 lint/validator 并落盘自审；不得先建图谱，不得修改 `_meta/*.jsonl`、量表、模板或他人文件。
- 完成后回报每卡版本、SHA-256、校验结果和请求协调者合并的账本字段；不得自行标记 `accepted`。

## Review handoff

- 主审：`evidence_design`；第二复审：`rubric_design`。
- 只有两位独立评审均 `pass`（各维度达门槛且 R01–R10/P0/P1/P2=0）后，协调者才合并 `deliverables.jsonl` 状态。
