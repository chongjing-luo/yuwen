---
document_type: lesson_schema_contract
scope: "课文无关的课程数据契约（S3 产出、S4/S5 消费的唯一数据形态）"
status: "active"
version: "1.0"
date: "2026-08-14"
enforced_by: scripts/validate_lesson_schema.py
mechanism_nodes: "K1 knowledge_refs/kp_scope · K2 literary_object · K4 relations · U1-U8 页面合同 · J1-J5 参与结构与节奏"
---

# 通用课程数据契约 lesson_schema v1.0

任何课文（现代文/文言文/诗词/整本书单元）的教学设计以同一形态进入构建与审计链。
《氓》V6.6 数据为前 schema 产物，向本契约迁移是登记在案的后续工作（见全流程地图）。

## 顶层字段

```jsonc
{
  "schema_version": "1.0",
  "lesson_id": "LES-X3-MENG-01",
  "lesson_title": "《氓》",
  "book_unit": {"card_refs": ["CARD-X3-U01-01"], "unit_ref": "UNIT-X3-U01"},   // K1：必须解析到真实卡片
  "text_contract": {                                                          // P-02/P-11：原文唯一可信源
    "source_path": "Data/textbook_extract/.../full.md",
    "source_sha256": "…",          // 绑定教材源包，防原文漂移
    "canonical_lines": ["氓之蚩蚩，抱布贸丝。", "…"],   // 教学涉及的全部原文句（构建与审计对照范围）
    "interpretation_boundaries": [{"line": "犹可说也", "allowed": "说=脱（教材注释）", "forbidden": "心理解读为话术"}]
  },
  "three_questions": ["…", "…", "…"],   // J4：学生视角真想知道的问题
  "kp_scope": {                                // K1：教什么以知识卡为准
    "kp_ids": ["KP-CARD-X3-U01-01-003", "…"],
    "deferred": [{"kp_id": "…", "reason": "…"}]
  },
  "relations": [                               // K4：知识网络边（可空但跨课单元必填）
    {"card_id": "CARD-B1-REC-01", "relation": "同出《诗经》，爱情开端与结局对照"}
  ],
  "pages": [ /* 见下 */ ],
  "rhythm_matrix": [                           // J5：五维节奏自检表（构建后生成亦可）
    {"page_id": "C101", "cognitive": "检索", "channel": "视觉", "social": "个人", "form": "清单", "affect": "低唤起"}
  ],
  "total_minutes": 280,
  "claim_boundary": "桌面设计；一切课堂效果待真实试教（P-12）"
}
```

## 页面字段（18 项合同，A-01）

每页必须完整且**非模板**（反样板：`scripts/checks/check_trace_evidence.py`）：

`page_id, title, minutes, literary_object(KP 绑定的具体词句), current_difficulty/unique_difficulty(须可归入手法库 17 类), unique_function, first_glance, information_state, student_action, artifact, wait_contract, bounded_feedback, revision, next_use(后页真实取回), normal_counterexample, visual_duty, first_person_reception, deletion_loss, story_return, script{teacher_spoken, timeboxes(秒和==分钟×60), branches≥2, listener_task, evidence_location, cut_line}`

可选：`kp_ids`（本页落点的 KP，K2）、`frontstage[]`（学生可见文字，过禁词扫描）、`illustration_eligibility`（V-02 准入五问）。

## 校验

```bash
python3 scripts/validate_lesson_schema.py --lesson-js <lesson.js>   # 或 --lesson-json <json>
```

校验项：knowledge_refs/kp_scope/relations 解析；三问在场；页面 18 字段非空且非样板；时间盒守恒；前台禁词；next_use 非空；claim_boundary 两本账声明。

## 与既有管线的关系

- 校验通过后进入 S4（yuwen-build-materials）与 S5（yuwen-audit-lesson）；
- 重型审计（六门/23 测试）继续由 `validate_meng_v6_page_audit.py` 系列承载，本契约是其输入格式的一般化；
- 新课文（如《沁园春·长沙》切片）从本契约起步，验证"脱离《氓》仍成立"。
