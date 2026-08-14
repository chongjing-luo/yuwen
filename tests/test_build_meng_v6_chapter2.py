from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "meng_v6" / "content" / "chapter_2.js"
METHODS = ROOT / "scripts" / "meng_v6" / "methods.js"
NOTES = ROOT / "scripts" / "meng_v6" / "chapter2_notes.js"
PAGE_IDS = [f"N{number:03d}" for number in range(22, 31)]


def node_json(path: Path) -> dict:
    result = subprocess.run(
        ["node", str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return json.loads(result.stdout)


class MengV6Chapter2ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = node_json(SOURCE)
        cls.methods = node_json(METHODS)["methods"]
        cls.pages = cls.payload["pages"]

    def test_nine_pages_form_one_ordered_chapter_path(self):
        self.assertEqual(PAGE_IDS, [page["page_id"] for page in self.pages])
        self.assertEqual("E_CH2_WHOLE_READ", self.pages[0]["event_id"])
        self.assertEqual("E_CH2_CHAPTER_RETELL", self.pages[-1]["event_id"])
        self.assertEqual(
            [page["event_id"] for page in self.pages[1:]],
            [page["next_event_id"] for page in self.pages[:-1]],
        )

    def test_every_second_chapter_line_is_taught_with_exact_glosses(self):
        expected = {
            "L006": {"乘": "登上", "垝垣": "残破的墙", "复关": "卫国地名，氓所住的地方；诗中借所居之地代指氓", "以": "来、用来"},
            "L007": {"泣涕": "哭泣流泪", "涟涟": "泪流不断的样子"},
            "L008": {"既": "已经", "载": "助词，加强语气"},
            "L009": {"卜": "用火烧龟板，根据裂纹推断吉凶祸福", "筮": "用蓍草的茎占卦", "体": "占卜显示的兆象", "咎言": "不祥之语"},
            "L010": {"贿": "财物，这里指嫁妆", "迁": "迁往男子家"},
        }
        taught = {}
        for page in self.pages:
            for line_id, glosses in page.get("line_glosses", {}).items():
                self.assertNotIn(line_id, taught)
                taught[line_id] = glosses
        self.assertEqual(expected, taught)

    def test_contrast_pair_keeps_two_lines_together(self):
        pair = next(page for page in self.pages if page["page_id"] == "N024")
        self.assertEqual(["L007", "L008"], pair["source_line_refs"])
        self.assertIn("不见复关，泣涕涟涟", pair["visible"])
        self.assertIn("既见复关，载笑载言", pair["visible"])
        self.assertIn("不见｜既见", pair["contrast_keys"])
        self.assertIn("泣涕｜笑言", pair["contrast_keys"])

    def test_student_generation_pages_do_not_show_finished_products(self):
        sightline = next(page for page in self.pages if page["page_id"] == "N023")
        contrast = next(page for page in self.pages if page["page_id"] == "N024")
        self.assertNotIn("女子立于垝垣上", sightline["visible"])
        self.assertNotIn("由此望向复关", sightline["visible"])
        for finished_pair in ("不见　↕　既见", "泣涕　↕　笑言", "涟涟　↕　载｜载"):
            self.assertNotIn(finished_pair, contrast["visible"])

    def test_reading_design_and_listener_test_are_separate_learning_changes(self):
        design = next(page for page in self.pages if page["page_id"] == "N025")
        listening = next(page for page in self.pages if page["page_id"] == "N026")
        self.assertEqual("M_READING_SCORE_DESIGN", design["method_id"])
        self.assertEqual("M_LISTENER_READING_TEST", listening["method_id"])
        self.assertIn("朗读谱", design["artifact_location"])
        self.assertIn("听者回执", listening["artifact_location"])
        self.assertNotEqual(design["observable_change"], listening["observable_change"])

    def test_culture_page_explains_divination_without_promising_marital_outcome(self):
        culture = next(page for page in self.pages if page["page_id"] == "N027")
        combined = "\n".join(
            [culture["visible"], culture["teacher_script"], culture["natural_paraphrases"]["L009"]]
        )
        self.assertIn("此次占问没有显示不祥", combined)
        self.assertIn("不能替后来长期相处作保证", combined)
        for forbidden in ("证明婚姻幸福", "保证婚后幸福", "证明男子可靠"):
            self.assertNotIn(forbidden, combined)

    def test_scrambled_sequence_does_not_leak_finished_order(self):
        retrieval = next(page for page in self.pages if page["page_id"] == "N029")
        self.assertEqual("open_question", retrieval["answer_state"])
        self.assertIn("乱序", retrieval["visible"])
        self.assertNotIn("望 → 不见 → 泣 → 既见 → 笑言 → 卜筮 → 迁", retrieval["visible"])
        self.assertIn("换笔修订", retrieval["visible"])

    def test_every_page_has_a_closed_learning_contract(self):
        method_ids = {method["method_id"] for method in self.methods}
        for page in self.pages:
            for field in (
                "unique_function", "student_action", "first_glance_contract", "observable_change",
                "artifact_location", "listener_task", "feedback_revision", "deletion_loss",
                "method_id", "teacher_script", "primary_visual_duty",
            ):
                self.assertTrue(page[field], f"{page['page_id']}:{field}")
            self.assertIn(page["method_id"], method_ids)
            self.assertGreaterEqual(len(page["teacher_script"]), 100, page["page_id"])

    def test_primary_visual_duty_matches_each_page_function(self):
        expected = {
            "N022": "全文/章内整读",
            "N023": "原文批注",
            "N024": "文本比较/关系图",
            "N025": "活动界面",
            "N026": "活动界面",
            "N027": "原文批注",
            "N028": "文本比较/关系图",
            "N029": "活动界面",
            "N030": "全文/章内整读",
        }
        self.assertEqual(expected, {page["page_id"]: page["primary_visual_duty"] for page in self.pages})

    def test_frontstage_uses_literary_classroom_language_without_ai_or_design_terms(self):
        frontstage = "\n".join(page["visible"] for page in self.pages)
        for token in (
            "闭环", "抓手", "赋能", "链路", "颗粒度", "接收审计", "学生角色",
            "页面功能", "理解链", "知识碎片", "恋爱脑", "情绪价值",
        ):
            self.assertNotIn(token, frontstage)

    def test_whole_read_accepts_crying_and_laughing_as_valid_character_actions(self):
        """A valid initial action pulse must not be corrected merely for using 泣/笑."""
        opening = next(page for page in self.pages if page["page_id"] == "N022")
        self.assertIn("带着感受的动作也可以写", opening["visible"])
        self.assertNotIn("望、泣、笑也算动作", opening["visible"])
        self.assertNotIn("‘望、泣、笑’都可以算动作", opening["teacher_script"])
        notes_text = NOTES.read_text(encoding="utf-8")
        self.assertNotIn("只写哭、笑而没有动作", notes_text)
        self.assertIn("望、泣、笑本身都是动作", notes_text)

    def test_divination_boundary_is_generated_before_teacher_calibration(self):
        """Students must first separate the present omen from the unknown future."""
        culture = next(page for page in self.pages if page["page_id"] == "N027")
        script = culture["teacher_script"]
        self.assertIn("停四十五秒", script)
        self.assertIn("先各写一句", script)
        self.assertLess(script.index("先各写一句"), script.index("此次占问没有显示不祥"))
        self.assertLess(script.index("停四十五秒"), script.index("此次占问没有显示不祥"))
        self.assertNotIn("兆象没有不祥。现在把两件事分开写", script)

    def test_chapter_opening_action_pulse_is_reused_in_retrieval(self):
        opening = next(page for page in self.pages if page["page_id"] == "N022")
        retrieval = next(page for page in self.pages if page["page_id"] == "N029")
        self.assertEqual("E_CH2_RETRIEVAL", opening["deferred_use"]["target_event_id"])
        self.assertIn("章首三个动作", retrieval["visible"])
        self.assertIn("章首写下的三个动作", retrieval["teacher_script"])
        self.assertIn("望", retrieval["visible"])

    def test_retrieval_keeps_valid_opening_actions_that_are_not_in_the_seven_prompts(self):
        retrieval = next(page for page in self.pages if page["page_id"] == "N029")
        combined = "\n".join((retrieval["visible"], retrieval["teacher_script"], retrieval["feedback_revision"]))
        self.assertIn("没有出现的照样保留", combined)
        self.assertNotIn("完整的七步", combined)
        self.assertIn("七个关键节点", combined)

    def test_listener_test_preserves_an_honest_still_needs_adjustment_path(self):
        listening = next(page for page in self.pages if page["page_id"] == "N026")
        self.assertIn("仍需调整", listening["visible"])
        self.assertIn("待调整", listening["teacher_script"])
        notes_text = NOTES.read_text(encoding="utf-8")
        self.assertIn("待调整", notes_text)
        self.assertNotIn("声音的转折已经经得住耳朵", notes_text)

    def test_retrieval_uses_one_clear_turn_marker_not_undefined_voice_traces(self):
        retrieval = next(page for page in self.pages if page["page_id"] == "N029")
        combined = "\n".join((retrieval["visible"], retrieval["student_action"], retrieval["teacher_script"]))
        self.assertNotIn("声纹", combined)
        self.assertIn("转折线", combined)
        self.assertIn("七词复位", combined)
        self.assertIn("在你排好的七词中", retrieval["visible"])
        self.assertNotIn("在‘不见｜既见’之间画", retrieval["visible"])


if __name__ == "__main__":
    unittest.main()
