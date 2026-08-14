from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v6_stage" / "chapter_2" / "package"
LESSON = OUT / "02_氓_V6第二章教学母版.md"
WORKSHEET = OUT / "03_氓_V6第二章学习单.md"
SCRIPT = OUT / "04A_氓_V6第二章逐页无生试讲稿.md"
SNAPSHOT = OUT / "06_氓_V6第二章课程数据快照.json"
MANIFEST = OUT / "chapter2_package_manifest.json"
PAGE_IDS = [f"N{number:03d}" for number in range(22, 31)]


class MengV6Chapter2MarkdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            ["node", "scripts/build_meng_v6_chapter2_markdown.js"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.lesson = LESSON.read_text(encoding="utf-8")
        cls.worksheet = WORKSHEET.read_text(encoding="utf-8")
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_all_channels_share_nine_pages_and_thirty_nine_minutes(self):
        self.assertEqual(PAGE_IDS, self.snapshot["page_ids"])
        self.assertEqual(39, self.snapshot["total_minutes"])
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
            self.assertGreaterEqual(len(script["teacher_spoken"]), 100)
            self.assertGreaterEqual(len(script["branches"]), 2)
            self.assertEqual(page["minutes"] * 60, sum(item["seconds"] for item in script["timeboxes"]))

    def test_worksheet_saves_distinct_products_not_one_repeated_table(self):
        for phrase in (
            "视线线条", "两句对照", "我的朗读谱", "听者回执", "卜筮小注",
            "以尔／以我", "七词复位", "第二章一句章意",
        ):
            self.assertIn(phrase, self.worksheet)
        self.assertNotIn("体验/思考/收获", self.worksheet)

    def test_generation_regions_do_not_prefill_sightline_or_contrast_answers(self):
        sightline = self.worksheet.split("## 二、视线线条", 1)[1].split("## 三、", 1)[0]
        contrast = self.worksheet.split("## 三、两句对照", 1)[1].split("## 四、", 1)[0]
        self.assertNotIn("女子立于垝垣上", sightline)
        for prefilled in ("不见复关 | 泣涕", "既见复关 | 笑、言", "涟涟 |", "载……载……"):
            self.assertNotIn(prefilled, contrast)
        self.assertGreaterEqual(contrast.count("原词"), 3)

    def test_glosses_stay_in_teacher_material_until_students_attempt(self):
        for phrase in ("残破的墙", "泪流不断的样子", "占卜显示的兆象", "财物，这里指嫁妆"):
            self.assertIn(phrase, self.lesson)
        self.assertNotIn("证明婚姻幸福", self.lesson)

    def test_manifest_binds_exactly_four_generated_files(self):
        self.assertEqual(4, len(self.manifest["files"]))
        for item in self.manifest["files"]:
            self.assertTrue((OUT / item["name"]).is_file())


if __name__ == "__main__":
    unittest.main()
