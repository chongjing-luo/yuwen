from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v6_stage" / "chapter_1" / "package"
LESSON = OUT / "02_氓_V6第一章教学母版.md"
WORKSHEET = OUT / "03_氓_V6第一章学习单.md"
SCRIPT = OUT / "04A_氓_V6第一章逐页无生试讲稿.md"
SNAPSHOT = OUT / "06_氓_V6第一章课程数据快照.json"
MANIFEST = OUT / "chapter1_package_manifest.json"
PAGE_IDS = [f"N{number:03d}" for number in range(13, 22)]


class MengV6Chapter1MarkdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            ["node", "scripts/build_meng_v6_chapter1_markdown.js"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.lesson = LESSON.read_text(encoding="utf-8")
        cls.worksheet = WORKSHEET.read_text(encoding="utf-8")
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_all_channels_share_nine_pages_and_thirty_eight_minutes(self):
        self.assertEqual(PAGE_IDS, self.snapshot["page_ids"])
        self.assertEqual(38, self.snapshot["total_minutes"])
        for page_id in PAGE_IDS:
            self.assertEqual(1, self.lesson.count(f"<!-- V6_PAGE:{page_id} -->"))
            self.assertEqual(1, self.script.count(f"<!-- V6_PAGE:{page_id} -->"))

    def test_script_is_a_complete_scene_for_every_page(self):
        for marker in (
            "【承接与场面】", "【教师实际说】", "【动作、等待与走位】", "【现场分支】",
            "【听者同时做什么】", "【留下什么】", "【怎样接下去】",
        ):
            self.assertEqual(9, self.script.count(marker), marker)
        for page in self.snapshot["pages"]:
            script = page["script"]
            self.assertGreaterEqual(len(script["teacher_spoken"]), 90)
            self.assertGreaterEqual(len(script["branches"]), 2)
            self.assertEqual(page["minutes"] * 60, sum(item["seconds"] for item in script["timeboxes"]))

    def test_worksheet_saves_attempt_revision_retrieval_and_first_impression(self):
        for phrase in (
            "我先说成的自然话", "换笔修订", "送行路线", "五步行动链",
            "诗里写着", "初读时我觉得", "现在还说不准", "第一章一句章意",
        ):
            self.assertIn(phrase, self.worksheet)
        self.assertNotIn("伪装", self.worksheet)
        self.assertNotIn("恋爱脑", self.worksheet)

    def test_line_glosses_are_in_teacher_material_but_not_prefilled_into_student_attempts(self):
        for phrase in ("忠厚的样子", "交易、交换", "拖延婚期", "愿、请"):
            self.assertIn(phrase, self.lesson)
        attempt_section = self.worksheet.split("## 二、逐句先说，再校准", 1)[1].split("## 三、", 1)[0]
        self.assertNotIn("忠厚的样子", attempt_section)
        self.assertNotIn("拖延婚期", attempt_section)

    def test_manifest_binds_exactly_four_generated_files(self):
        self.assertEqual(4, len(self.manifest["files"]))
        for item in self.manifest["files"]:
            self.assertTrue((OUT / item["name"]).is_file())

    def test_worksheet_frames_line_two_as_text_sequence_not_deception(self):
        self.assertIn("诗句先写的动作", self.worksheet)
        self.assertIn("女子随后说明的来意", self.worksheet)
        self.assertNotIn("表面上，他来", self.worksheet)
        self.assertNotIn("实际上，他来", self.worksheet)

    def test_worksheet_gives_distinct_controls_to_lines_one_four_and_five(self):
        for phrase in (
            "谁：", "怎样：", "拿什么：", "做什么：",
            "她在拒绝这门婚事", "她在说明此刻不能成婚的条件", "托住判断的原词",
            "她先在劝什么", "她又把什么定下来",
        ):
            self.assertIn(phrase, self.worksheet)


if __name__ == "__main__":
    unittest.main()
