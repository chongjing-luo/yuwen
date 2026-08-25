---
name: yuwen-flow
description: 语文项目G0-G4与S6-S9门禁执行器（工程轴）。当需要验证某一环节、检查上游变更是否使下游失效或做定向回归时使用；只报告结果，不生成、修复或审美判断教学内容。
---

# 环节门禁链（工程轴）

执行设计方案 §6 的门禁与血缘契约。教学门禁可校验当前K/U/J目标框架落点，S0资料门禁与全局工程门禁按各自契约执行；本工程skill不以“服务全部节点”作为自身准入依据。

需要解释锁字段或断点时读取 `../_shared/lesson-lineage-contracts.md`；本skill仍只执行验证，不负责补写锁内容。

## 输入

- 环节代号（S0-S9）+ 该环节涉及的实体路径

## 备课门禁链

| 门 | 对象 | 跑什么 |
|---|---|
| G0 / S2内部 | 证据清单 | `validate_lesson_evidence.py <evidence_manifest.json>` |
| G1 / S2教案 | 教案锁＋所有者回执 | `validate_lesson_plan.py <lesson_plan_lock.json>` |
| G2 / S3设计 | lesson.json＋design lock | `validate_lesson_schema.py --lesson-json <lesson.json> --strict`；反样板；`validate_lesson_lineage.py design <design_lock.json>` |
| G3 / S4物料 | manifest＋materials lock | 构建器测试；原则检查；`validate_lesson_lineage.py materials <materials_lock.json>` |
| G4 / S5终审 | `awaiting_host_release` audit lock＋冻结物料包 | G0—G3回归＋原则/反样板＋视觉/学生接收双审＋`validate_lesson_audit.py <audit_lock.json> --external-event-registry <宿主只读路径>`；只验本地候选，不代表宿主放行 |
| S6 / 课堂观察准入 | OBS记录＋当前G4锁＋宿主项目外放行注册表 | `validate_evidence.py <obs.jsonl> --type obs --host-release-registry <宿主只读路径>`；逐条核验课程、G4哈希与宿主事件 |
| S0资料 | catalog/知识库 | `build_catalog.py --check` + `validate_knowledge_base.py` |
| S7 作业 | `validate_homework_package.py <package.json>` |
| S8 命题/诊断 | `validate_assessment_package.py <blueprint>` / `analyze_mastery.py --check`（如有台账） |
| 全局 | `scripts/run_selfcheck.py`（注册库+底线+全量测试+覆盖） |

## 步骤

1. 从请求解析唯一门号与对象路径；G4必须从G0顺序回归，不能只跑最后一条命令，且必须使用项目目录外的宿主审查事件注册表；S6另须使用项目目录外的宿主放行事件注册表。
2. 逐条执行并记录命令、退出码、对象SHA-256和标准版本。
3. 失败只归因和指向责任阶段：证据→S2/G0，教案→S2/G1，课堂事件→S3，成品实现→S4；本skill不得代改教学内容。
4. 上游哈希变化时报告第一个断点，并把全部下游标为stale；不允许只改锁文件。
5. 输出只包含命令、退出码、对象哈希、冻结标准和第一个断点；消费登记属于`yuwen-catalog`，本skill不写catalog。

## 放行条件

- 该环节全部命令退出码 0；
- 涉及在审候选的，按收敛规则记录所用的 STANDARD 版本。
- “通过”只表示相应桌面门禁通过，不表示课堂效果发生。
- G4“通过”只表示`awaiting_host_release`候选结构已验；项目内不得生成`released`状态，宿主放行是项目外事件。
- S6只有在OBS逐条绑定宿主已核验放行事件和当前G4锁哈希后才可采集；项目内`host_release*.json`不能构成准入。

## 产出

- 门禁执行记录（退出码清单、对象哈希、标准版本和首个断点）；不生成教学内容、不修锁、不写catalog、不作宿主放行决定
