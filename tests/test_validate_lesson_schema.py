# -*- coding: utf-8 -*-
"""通用课程数据校验器测试（synthetic lesson + 真实知识卡与教材源包）。"""
import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_lesson_schema import validate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Data/textbook_extract/选择性必修下册/mineru_result/01_U1_导语_课1_氓_离骚/full.md"
if not SOURCE.exists():
    candidates = list((ROOT / "Data/textbook_extract/选择性必修下册/mineru_result").glob("*/full.md"))
    SOURCE = candidates[0]


def synthetic_lesson():
    return {
        "schema_version": "1.0",
        "lesson_id": "LES-TEST-01",
        "book_unit": {"card_refs": ["CARD-X3-U01-01"], "unit_ref": "UNIT-X3-U01"},
        "text_contract": {
            "source_path": str(SOURCE.relative_to(ROOT)),
            "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "canonical_lines": ["氓之蚩蚩，抱布贸丝", "桑之未落，其叶沃若"],
            "interpretation_boundaries": [],
        },
        "three_questions": ["她经历了什么？"],
        "kp_scope": {
            "kp_ids": ["KP-CARD-X3-U01-01-003", "KP-CARD-X3-U01-01-004"],
            "deferred": [{"kp_id": "KP-CARD-X3-U01-01-007", "reason": "《离骚》属下一课"}],
        },
        "relations": [{"card_id": "CARD-B1-REC-01", "relation": "同出《诗经》"}],
        "pages": [
            {
                "page_id": "T01",
                "title": "我们把这句读清楚",
                "minutes": 5,
                "literary_object": "氓之蚩蚩，抱布贸丝",
                "unique_difficulty": "学生把贸丝当成经济活动描写，看不出求婚的借口功能。",
                "unique_function": "让学生由“抱布贸丝”的动作猜出这场相遇的真实目的。",
                "information_state": "首答态只给原句，贸丝的婚恋含义在学生猜测后揭示。",
                "student_action": ["用自己的话说这两句发生了什么"],
                "artifact": "一句自然话猜测",
                "next_use": "T02 的对照讨论取回各人猜测",
                "normal_counterexample": "猜不出的学生如实写“看不懂贸丝”，不编造。",
                "first_person_reception": "我说出了对这两句的猜测，并在揭示后知道了自己差在哪。",
                "deletion_loss": "失去学生自己的第一印象，后页对照无从比起。",
                "story_return": "由贸丝回到两人相遇的开端场景。",
                "script": {
                    "teacher_spoken": "…",
                    "timeboxes": [{"label": "首答", "seconds": 300}],
                    "branches": [{"kind": "沉默", "response": "再读一遍"}, {"kind": "越界", "response": "回原句"}],
                },
            }
        ],
        "claim_boundary": "桌面设计；课堂效果待真实试教（P-12）",
    }


class ValidateLessonSchemaTest(unittest.TestCase):
    def test_synthetic_lesson_passes(self):
        errors, warnings, stats = validate(synthetic_lesson(), strict=True)
        self.assertEqual(errors, [], f"synthetic lesson 应通过: {errors}")
        self.assertEqual(stats["boilerplate"], 0)
        self.assertEqual(stats["pages"], 1)

    def test_unresolvable_card_detected(self):
        lesson = synthetic_lesson()
        lesson["book_unit"]["card_refs"] = ["CARD-XX-U99-99"]
        errors, _, _ = validate(lesson, strict=False)
        self.assertTrue(any("card_ref 无法解析" in e for e in errors))

    def test_kp_out_of_card_detected(self):
        lesson = synthetic_lesson()
        lesson["kp_scope"]["kp_ids"].append("KP-CARD-X3-U01-02-001")
        errors, _, _ = validate(lesson, strict=False)
        self.assertTrue(any("未解析到引用卡片" in e for e in errors))

    def test_defer_without_reason_detected(self):
        lesson = synthetic_lesson()
        lesson["kp_scope"]["deferred"].append({"kp_id": "KP-CARD-X3-U01-01-006", "reason": ""})
        errors, _, _ = validate(lesson, strict=False)
        self.assertTrue(any("缺理由" in e for e in errors))

    def test_source_sha_drift_detected(self):
        lesson = synthetic_lesson()
        lesson["text_contract"]["source_sha256"] = "0" * 64
        errors, _, _ = validate(lesson, strict=False)
        self.assertTrue(any("原文漂移" in e for e in errors))

    def test_missing_page_field_detected(self):
        lesson = synthetic_lesson()
        del lesson["pages"][0]["story_return"]
        errors, _, _ = validate(lesson, strict=False)
        self.assertTrue(any("story_return" in e for e in errors))

    def test_timebox_and_branch_detected(self):
        lesson = synthetic_lesson()
        lesson["pages"][0]["script"]["timeboxes"] = [{"label": "首答", "seconds": 200}]
        lesson["pages"][0]["script"]["branches"] = [{"kind": "沉默", "response": "再读"}]
        errors, _, _ = validate(lesson, strict=False)
        self.assertTrue(any("时间盒" in e for e in errors))
        self.assertTrue(any("branches" in e for e in errors))

    def test_literary_object_outside_canonical_detected(self):
        lesson = synthetic_lesson()
        lesson["pages"][0]["literary_object"] = "不存在的句子"
        errors, _, _ = validate(lesson, strict=False)
        self.assertTrue(any("canonical_lines" in e for e in errors))

    def test_boilerplate_strict_fails_but_default_warns(self):
        lesson = synthetic_lesson()
        lesson["pages"][0]["story_return"] = "页面结束前由一句自然复述回到谁做了什么、人物处境怎样变化以及故事推进到哪里。"
        errors, warnings, stats = validate(lesson, strict=False)
        self.assertEqual(errors, [])
        self.assertEqual(stats["boilerplate"], 1)
        self.assertTrue(any("样板" in w for w in warnings))
        errors, _, _ = validate(lesson, strict=True)
        self.assertTrue(any("样板" in e for e in errors))

    def test_relation_unresolvable_detected(self):
        lesson = synthetic_lesson()
        lesson["relations"].append({"card_id": "CARD-ZZ-U99-99", "relation": "测试"})
        errors, _, _ = validate(lesson, strict=False)
        self.assertTrue(any("relations" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
