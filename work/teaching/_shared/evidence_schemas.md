# 证据层 schema 约定（L4 · 只追加）

四类记录 + 一类提案。通用铁律（设计方案 §3.5）：每条绑定 `lesson_version_sha`（或来源版本）+ 机制节点；只追加不改写；synthetic 测试数据只准存在于 `tests/fixtures/`，严禁写入本目录。

## OBS 课堂观察（observations.jsonl）

```json
{"id":"OBS-20260910-01","date":"2026-09-10","lesson_id":"LES-X3-MENG-01","lesson_version_sha":"<16+hex>","g4_audit_lock_sha256":"<64hex>","host_release_event_id":"HRE-20260909-01","host_release_source":{"locator":"host://reviews/HRE-20260909-01","record_sha256":"<64hex>"},"page_id":"O07","node":"U1","signal":"首答非空白抽样率","value":"34/38","students":["全班"],"source":{"type":"observation","ref":"观察表P3"}}
```

必填：id/date/lesson_id/lesson_version_sha/g4_audit_lock_sha256/host_release_event_id/host_release_source/node/signal/value/source。`node` ∈ K1-K5/U1-U8/J1-J7；`value`只记事实（人次/原话/动作），不记评价。每条OBS必须绑定项目外宿主放行事件与项目内当前`_meta/audit_lock.json`的真实字节哈希。

## GRD 批改记录（grading.jsonl）

```json
{"id":"GRD-20260911-01","date":"2026-09-11","class_id":"高2026级3班","student_id":"S07","homework_id":"HW-MENG-V66-01","item_id":"HW-02","kp_id":"KP-CARD-X3-U01-01-003","score":2,"max_score":2,"evidence_quote":"学生原文一句","error_type":null,"node":"K3"}
```

必填：id/date/class_id/student_id/homework_id/item_id/kp_id/score/max_score/node；`error_type` 可空但须可操作（现代义干扰/推断当诗写……禁"粗心"）。

## MR 掌握记录（mastery_ledger.jsonl，与 analyze_mastery.py 兼容）

```json
{"id":"MR-20260911-01","date":"2026-09-11","class_id":"高2026级3班","student_id":"S07","source":{"type":"homework","ref":"HW-MENG-V66-01/HW-02"},"kp_id":"KP-CARD-X3-U01-01-003","score":2,"max_score":2,"error_type":null}
```

analyze_mastery 既有校验全部保留；新增 id 可选（存量兼容）、node 可选。

## REF 课后反思（reflections/reflections.jsonl）

```json
{"id":"REF-20260910-01","date":"2026-09-10","lesson_id":"LES-X3-MENG-01","lesson_version_sha":"<hex>","node":"U7","evidence_ref":["OBS-20260910-03","GRD-20260911-05"],"phenomenon":"沉默学生 6 人中 4 人走了纸面路径","cause":"normal_counterexample 在纸面更可见","revision_target":"lesson.json:O07.normal_counterexample 增加口头入口","proposal":null}
```

必填：id/date/lesson_id/lesson_version_sha/node/evidence_ref（≥1）/phenomenon/cause/revision_target；无证据的判断不收（MM-S9-01）。

## PR 原则修订提案（reflections/proposals/PR-*.json）

```json
{"id":"PR-20260910-01","date":"2026-09-10","trigger_evidence":["REF-20260910-01"],"node":"U7","change_type":"new","draft":{"title":"…","statement":"…","enforcement":[{"type":"design_trace","fields":["normal_counterexample"]}]},"target_standard":"STANDARD-next","status":"proposed"}
```

必填：id/trigger_evidence(≥1)/node/change_type∈{new,modify,retire}/draft/target_standard/status；准入过收敛规则§四（触发证据+节点+强制方式）。

## 校验

```bash
# OBS默认失败关闭：两项外部/当前对象参数均必需
python3 scripts/validate_evidence.py <observations.jsonl> --type obs \
  --host-release-registry <项目目录外宿主只读注册表> \
  --audit-lock work/teaching/<册>/<课>/_meta/audit_lock.json

# 其余证据类型
python3 scripts/validate_evidence.py <file> --type grd|mr|ref|pr
```
