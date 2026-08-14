from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "meng_v6" / "content" / "chapter_1.js"
METHODS = ROOT / "scripts" / "meng_v6" / "methods.js"
PAGE_IDS = [f"N{number:03d}" for number in range(13, 22)]


def node_json(path: Path) -> dict:
    result = subprocess.run(
        ["node", str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return json.loads(result.stdout)


class MengV6Chapter1ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = node_json(SOURCE)
        cls.methods = node_json(METHODS)["methods"]
        cls.pages = cls.payload["pages"]

    def test_nine_pages_form_one_ordered_chapter_path(self):
        self.assertEqual(PAGE_IDS, [page["page_id"] for page in self.pages])
        self.assertEqual("E_CH1_WHOLE_READ", self.pages[0]["event_id"])
        self.assertEqual("E_CH1_CHAPTER_RETELL", self.pages[-1]["event_id"])
        self.assertEqual(
            [page["event_id"] for page in self.pages[1:]],
            [page["next_event_id"] for page in self.pages[:-1]],
        )

    def test_five_line_pages_cover_every_first_chapter_line_once(self):
        line_pages = self.pages[1:6]
        self.assertEqual(
            ["L001", "L002", "L003", "L004", "L005"],
            [page["source_line_refs"][0] for page in line_pages],
        )
        self.assertTrue(all(len(page["source_line_refs"]) == 1 for page in line_pages))
        originals = "\n".join(page["original_text"] for page in line_pages)
        for phrase in (
            "氓之蚩蚩，抱布贸丝", "匪来贸丝，来即我谋", "送子涉淇，至于顿丘",
            "匪我愆期，子无良媒", "将子无怒，秋以为期",
        ):
            self.assertEqual(1, originals.count(phrase), phrase)

    def test_every_line_page_has_exact_gloss_and_a_natural_paraphrase(self):
        expected_glosses = {
            "L001": {"氓": "民，这里指诗中的男主人公", "蚩蚩": "忠厚的样子", "贸": "交易、交换"},
            "L002": {"匪": "不是", "即": "就、靠近", "谋": "谋划、商量，这里指商量婚事"},
            "L003": {"涉": "渡过", "淇": "淇水", "顿丘": "地名"},
            "L004": {"愆期": "拖延婚期", "良媒": "合适的媒人"},
            "L005": {"将": "愿、请", "无": "同‘毋’，不要", "以……为期": "把……定作婚期"},
        }
        for page in self.pages[1:6]:
            line_id = page["source_line_refs"][0]
            self.assertEqual(expected_glosses[line_id], page["glosses"])
            self.assertGreaterEqual(len(page["natural_paraphrase"]), 12)
            self.assertNotIn("意为", page["natural_paraphrase"])

    def test_every_page_proves_action_artifact_feedback_and_reuse(self):
        method_ids = {method["method_id"] for method in self.methods}
        for page in self.pages:
            for field in (
                "unique_function", "student_action", "first_glance_contract", "artifact_location",
                "listener_task", "feedback_revision", "deletion_loss", "method_id", "teacher_script",
            ):
                self.assertTrue(page[field], f"{page['page_id']}:{field}")
            self.assertIn(page["method_id"], method_ids)
            self.assertGreaterEqual(len(page["teacher_script"]), 90, page["page_id"])

    def test_primary_visual_duty_matches_each_page_function(self):
        expected = {
            "N013": "全文/章内整读",
            "N014": "原文批注",
            "N015": "原文批注",
            "N016": "原文批注",
            "N017": "原文批注",
            "N018": "原文批注",
            "N019": "活动界面",
            "N020": "活动界面",
            "N021": "全文/章内整读",
        }
        self.assertEqual(expected, {page["page_id"]: page["primary_visual_duty"] for page in self.pages})

    def test_method_library_routes_difficulty_to_a_revised_text_product(self):
        used = {page["method_id"] for page in self.pages}
        registry = {method["method_id"]: method for method in self.methods}
        self.assertTrue(used.issubset(registry))
        for method_id in used:
            for field in ("reading_difficulty", "student_action", "artifact", "feedback_revision", "return_to_text"):
                self.assertTrue(registry[method_id][field], f"{method_id}:{field}")

    def test_first_impression_is_saved_without_hindsight_or_victim_blame(self):
        dossier = next(page for page in self.pages if page["page_id"] == "N020")
        self.assertEqual(["诗里写着", "初读时我觉得", "现在还说不准"], dossier["artifact_columns"])
        self.assertEqual("E_CHAPTER1_RETURN", dossier["deferred_use"]["target_event_id"])
        self.assertEqual("deferred", dossier["next_use_status"])
        frontstage = "\n".join(page["visible"] for page in self.pages)
        for token in ("伪装", "恋爱脑", "渣男", "婚前暴力", "遇人不淑"):
            self.assertNotIn(token, frontstage)

    def test_retrieval_page_hides_the_finished_action_chain_until_revision(self):
        retrieval = next(page for page in self.pages if page["page_id"] == "N019")
        self.assertEqual("open_question", retrieval["answer_state"])
        self.assertIn("合上书", retrieval["visible"])
        self.assertNotIn("以贸丝姿态接近 → 说明求婚来意", retrieval["visible"])
        self.assertIn("换笔修订", retrieval["visible"])

    def test_chapter_closes_with_full_text_rereading_and_thirty_second_retell(self):
        close = self.pages[-1]
        self.assertIn("第一章全文", close["visible"])
        self.assertIn("30秒", close["visible"])
        self.assertIn("男子怎样来", close["retell_criteria"])
        self.assertIn("女子怎样回应", close["retell_criteria"])
        self.assertIn("婚期怎样定", close["retell_criteria"])

    def test_student_frontstage_contains_no_project_management_or_ai_language(self):
        frontstage = "\n".join(page["visible"] for page in self.pages)
        for token in (
            "闭环", "抓手", "赋能", "链路", "颗粒度", "接收审计", "学生角色", "页面功能",
            "不收集知识碎片", "建立理解链",
        ):
            self.assertNotIn(token, frontstage)

    def test_line_two_does_not_preload_a_deception_frame(self):
        line_two = next(page for page in self.pages if page["page_id"] == "N015")
        combined = "\n".join((
            line_two["visible"], line_two["unique_function"], line_two["teacher_script"],
        ))
        for loaded_phrase in ("表面上", "实际上", "表面来意", "真实来意", "表里来意"):
            self.assertNotIn(loaded_phrase, combined)
        for grounded_phrase in ("诗句先写的动作", "女子随后说明的来意"):
            self.assertIn(grounded_phrase, combined)

    def test_lines_four_and_five_require_attempts_before_teacher_calibration(self):
        line_four = next(page for page in self.pages if page["page_id"] == "N017")
        line_five = next(page for page in self.pages if page["page_id"] == "N018")
        self.assertIn("停四十五秒", line_four["teacher_script"])
        self.assertLess(line_four["teacher_script"].index("停四十五秒"), line_four["teacher_script"].index("‘愆期’是"))
        self.assertIn("停四十五秒", line_five["teacher_script"])
        self.assertLess(line_five["teacher_script"].index("停四十五秒"), line_five["teacher_script"].index("‘将’是愿、请"))
        self.assertIn("两种读法", line_four["visible"])
        self.assertIn("她先在劝什么", line_five["visible"])


if __name__ == "__main__":
    unittest.main()
