# -*- coding: utf-8 -*-
"""通用原则检查执行器测试。"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "checks"))

from run_principle_checks import check_config_drift, load_lesson, run_checks  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "work/principles/enforcement_config.json").read_text(encoding="utf-8"))


def lesson(pages, **extra):
    data = {"pages": pages, "three_questions": ["问一", "问二", "问三"], "target_natural_minutes": None}
    data.update(extra)
    return data


class ConfigDriftTest(unittest.TestCase):
    def test_current_config_has_no_drift(self):
        self.assertEqual(check_config_drift(CONFIG), [])

    def test_missing_key_detected(self):
        dropped = {k: v for k, v in CONFIG.items() if k != "frontstage_banned_v6"}
        errors = check_config_drift(dropped)
        self.assertTrue(any("词表缺失或为空" in e and "frontstage_banned_v6" in e for e in errors))

    def test_duplicate_word_detected(self):
        duplicated = dict(CONFIG)
        duplicated["note_banned_v5"] = duplicated["note_banned_v5"] + [duplicated["note_banned_v5"][0]]
        errors = check_config_drift(duplicated)
        self.assertTrue(any("词表重复词条" in e for e in errors))


class RunChecksTest(unittest.TestCase):
    def test_json_course_data_can_be_loaded(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lesson.json"
            expected = lesson([])
            path.write_text(json.dumps(expected, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(load_lesson(None, str(path)), expected)

    def test_clean_lesson_passes(self):
        result = run_checks(
            lesson(
                [
                    {
                        "page_id": "T01",
                        "title": "我们把这句读清楚",
                        "frontstage": ["氓之蚩蚩，抱布贸丝"],
                        "minutes": 5,
                        "script": {"timeboxes": [{"label": "读", "seconds": 300}]},
                        "unique_difficulty": "学生把贸丝当成经济活动描写，看不出求婚的借口功能。",
                    }
                ]
            ),
            CONFIG,
            strict=False,
        )
        for name, check in result.items():
            if name == "boilerplate_trace":
                self.assertEqual(check["count"], 0)
            else:
                self.assertTrue(check["ok"], f"{name} 应通过: {check}")

    def test_frontstage_banned_word_detected(self):
        result = run_checks(
            lesson(
                [
                    {
                        "page_id": "T02",
                        "title": "本页意图：建立理解链",
                        "minutes": 3,
                        "script": {"timeboxes": [{"label": "读", "seconds": 180}]},
                    }
                ]
            ),
            CONFIG,
            strict=False,
        )
        check = result["frontstage_banned"]
        self.assertFalse(check["ok"])
        words = {f["word"] for f in check["findings"]}
        self.assertIn("本页意图", words)
        self.assertIn("建立理解链", words)

    def test_timebox_mismatch_detected(self):
        result = run_checks(
            lesson(
                [
                    {
                        "page_id": "T03",
                        "title": "标题",
                        "minutes": 5,
                        "script": {"timeboxes": [{"label": "读", "seconds": 240}]},
                    }
                ]
            ),
            CONFIG,
            strict=False,
        )
        self.assertFalse(result["timebox_conservation"]["ok"])

    def test_total_minutes_mismatch_detected(self):
        result = run_checks(
            lesson(
                [
                    {
                        "page_id": "T04",
                        "title": "标题",
                        "minutes": 5,
                        "script": {"timeboxes": [{"label": "读", "seconds": 300}]},
                    }
                ],
                target_natural_minutes=6,
            ),
            CONFIG,
            strict=False,
        )
        self.assertFalse(result["total_minutes"]["ok"])

    def test_boilerplate_counted_but_not_failed(self):
        result = run_checks(
            lesson(
                [
                    {
                        "page_id": "T05",
                        "title": "标题",
                        "minutes": 4,
                        "script": {"timeboxes": [{"label": "读", "seconds": 240}]},
                        "story_return": "页面结束前由一句自然复述回到谁做了什么、人物处境怎样变化以及故事推进到哪里。",
                    }
                ]
            ),
            CONFIG,
            strict=False,
        )
        self.assertEqual(result["boilerplate_trace"]["count"], 1)
        self.assertIn("收敛规则", result["boilerplate_trace"]["note"])

    def test_empty_guiding_question_projection_is_valid(self):
        result = run_checks(lesson([{"page_id": "T06", "title": "标题", "minutes": 2, "script": {"timeboxes": [{"label": "读", "seconds": 120}]}}], three_questions=[]), CONFIG, strict=False)
        self.assertTrue(result["guiding_questions_well_formed"]["ok"])

    def test_nonempty_guiding_questions_cannot_contain_blank_items(self):
        result = run_checks(lesson([], three_questions=["有效问题", " "]), CONFIG, strict=False)
        self.assertFalse(result["guiding_questions_well_formed"]["ok"])


if __name__ == "__main__":
    unittest.main()
