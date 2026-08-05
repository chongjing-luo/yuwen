# Knowledge Extraction Foundation — Project Index

- Task slug: `knowledge-extraction-foundation`
- Objective: 为其他 agent 建立可直接执行的知识点提取基础设施，不生产正式知识卡。
- Canonical execution baseline: `../../work/语文备课系统_知识点提取研究计划.md`
- Architecture/design reference: `../../docs/superpowers/specs/2026-08-05-curriculum-mineru-work-integration-design.md`
- User approval recorded: 2026-08-06，用户指令“先搭建好基础设置，我会由其他agent执行”。

## Scope

In scope:

- 144 个教材解析源包及其载体、页码映射账本；
- 120 项核心交付清单；
- 候选 V2 Schema、受控词表、评分量表和模板；
- 自动校验器及一条真实记录的首通验证；
- 供其他 agent 使用的运行与交接说明。
- 首轮校准吞吐的 10 张卡 + 5 张图草稿及其证据记录（不计正式验收）。

Out of scope:

- 正式知识卡、单元图谱、册表、真题解构和全局地图的内容生产；
- 对尚未取得的高考评价体系、初中教材、四川政策和真题作事实性补写；
- 改写或迁移现有 3 张样卡和 1 份样板图谱。

## Artifact registry

| Artifact family | Active artifact | Status | Result | Approval |
|---|---|---|---|---|
| `01-requirements` | `../../work/语文备课系统_知识点提取研究计划.md` | complete | execution-ready baseline | approved 2026-08-06 |
| `03-architecture` | `../../work/语文备课系统_知识点提取研究计划.md` §3–§8 | complete | data contracts and gates defined | approved 2026-08-06 |
| `04-implementation-spec` | `04_execution/implementation_spec_20260806_010616.md` | complete | implemented | approved 2026-08-06 |
| `04-first-throughput-evidence` | `04_execution/first_throughput_evidence_20260806_013226.md` | complete | passed | approved 2026-08-06 |
| `04-calibration-throughput` | `04_execution/calibration_throughput_20260806_061159.md` | complete | 10 cards + 5 graphs drafted; G2 pending | coordinator merged 2026-08-06 |

## Open questions and blockers

- 高考评价体系官方原件、初中关联依据、四川用卷政策及 2023—2026 真题/答案/评分材料尚未完整登记；基础设施只创建入口和缺失状态。
- `TB2` 与必修下学生教材的版次配套关系仍为 `unknown`，不得提前标成已验证。
- 候选 Schema、词表和量表必须经过 10 卡 + 5 图校准后才能从 `candidate` 冻结为 `frozen`。

## Change impact assessment

- Affected downstream stages: 知识卡校准、单元图谱校准、批量生产、真题映射。
- Suggested action: 其他 agent 先运行基础校验，再领取单一 `deliverable_id`；校准反馈统一回写候选契约。
- Approval reset: 下游批量生产保持 `pending`，直至 G2 校准门禁通过。
