from __future__ import annotations

import json
import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v6_stage" / "opening" / "package"
LESSON = OUTPUT_DIR / "02_氓_V6导入切片教学母版.md"
WORKSHEET_A = OUTPUT_DIR / "03A_氓_V6导入学习单A_旧故事与初听.md"
WORKSHEET_B = OUTPUT_DIR / "03B_氓_V6导入学习单B_初听后路标卡.md"
SCRIPT = OUTPUT_DIR / "04A_氓_V6导入切片逐页无生试讲稿.md"
SNAPSHOT = OUTPUT_DIR / "06_氓_V6导入切片课程数据快照.json"
MANIFEST = OUTPUT_DIR / "opening_package_manifest.json"
PACKAGE_REVIEW = PROJECT_ROOT / "scripts" / "meng_v6" / "reviews" / "opening_package.json"


def build(out: Path = OUTPUT_DIR) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", "scripts/build_meng_v6_markdown.js", "--through", "opening", "--out", str(out)],
        cwd=PROJECT_ROOT, text=True, capture_output=True, check=False,
    )


class MengV6OpeningMarkdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = build()
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        cls.lesson = LESSON.read_text(encoding="utf-8")
        cls.worksheet_a = WORKSHEET_A.read_text(encoding="utf-8")
        cls.worksheet_b = WORKSHEET_B.read_text(encoding="utf-8")
        cls.worksheet = cls.worksheet_a + "\n" + cls.worksheet_b
        cls.script = SCRIPT.read_text(encoding="utf-8")

    def test_all_three_markdown_channels_and_snapshot_share_the_same_eleven_pages(self):
        expected = ["N001", "N002", "N003", "N004", "N005", "N007", "N008", "N009", "N010", "N011", "N012"]
        self.assertEqual(expected, self.snapshot["page_ids"])
        self.assertEqual(expected, [item["page_id"] for item in self.snapshot["pages"]])
        for page_id in expected:
            self.assertEqual(1, self.lesson.count(f"<!-- V6_PAGE:{page_id} -->"))
            self.assertEqual(1, self.script.count(f"<!-- V6_PAGE:{page_id} -->"))
        self.assertEqual(11, self.lesson.count("<!-- V6_PAGE:"))
        self.assertEqual(11, self.script.count("<!-- V6_PAGE:"))

    def test_each_page_has_a_performable_script_not_a_dry_outline(self):
        for page in self.snapshot["pages"]:
            note = page["script"]
            self.assertGreaterEqual(len(note["teacher_spoken"]), 45, page["page_id"])
            self.assertGreaterEqual(len(note["branches"]), 2, page["page_id"])
            self.assertTrue(note["stage_directions"], page["page_id"])
            self.assertTrue(note["listener_task"], page["page_id"])
            self.assertTrue(note["evidence_location"], page["page_id"])
            self.assertTrue(note["cut_line"], page["page_id"])
            self.assertEqual(
                page["minutes"] * 60,
                sum(item["seconds"] for item in note["timeboxes"]),
                page["page_id"],
            )
        for marker in ("【承接与场面】", "【教师实际说】", "【动作、等待与走位】", "【现场分支】", "【听者同时做什么】", "【留下什么】", "【怎样接下去】"):
            self.assertIn(marker, self.script)

    def test_required_real_classroom_branches_are_present(self):
        branch_kinds = {
            branch["kind"]
            for page in self.snapshot["pages"]
            for branch in page["script"]["branches"]
        }
        self.assertTrue({
            "memory_blank", "film_or_tv", "duplicate_work", "silence",
            "time_overrun", "no_initial_mark", "overinterpretation",
        }.issubset(branch_kinds))

    def test_worksheet_saves_every_opening_artifact_without_prefilled_answers(self):
        for phrase in (
            "篇名＋它写了什么", "小组作品谱", "我未想到的一项", "相近或不同",
            "最想追踪的一问", "尚未找到", "同桌让我补记", "谁在回望什么", "谁做什么",
        ):
            self.assertIn(phrase, self.worksheet)
        for prefilled in (
            "相遇的欣悦，需要真实了解", "婚姻的选择，需要尊重与行动",
            "共同生活，需要平衡、支持与边界", "遇人不淑", "恋爱脑",
        ):
            self.assertNotIn(prefilled, self.worksheet)

    def test_late_scaffolds_are_on_a_separately_distributed_card(self):
        self.assertNotIn("三块最小路标", self.worksheet_a)
        self.assertNotIn("谁在回望什么", self.worksheet_a)
        self.assertNotIn("谁做什么", self.worksheet_a)
        self.assertIn('distribution_timing: "after_first_listening_and_mark"', self.worksheet_b)
        self.assertIn("三块最小路标", self.worksheet_b)
        self.assertIn("没有斜线的原句", self.worksheet_b)
        self.assertIn("《诗经》篇数：305篇", self.worksheet_b)
        self.assertIn("我写下重读后改动的一处", self.worksheet_b)

    def test_student_frontstage_has_no_design_or_audit_language(self):
        banned = (
            "学生角色", "林晓", "设计意图", "硬门", "接收审计", "理解链", "知识碎片",
            "页面功能", "不填表", "不概括",
        )
        student_frontstage = self.worksheet + "\n" + "\n".join(
            page["student_visible_text"] for page in self.snapshot["pages"]
        )
        for token in banned:
            self.assertNotIn(token, student_frontstage)

    def test_lesson_worksheet_script_and_audit_agree_on_time_and_artifact_locations(self):
        self.assertEqual(29, self.snapshot["total_minutes"])
        for page in self.snapshot["pages"]:
            page_id = page["page_id"]
            self.assertIn(f"{page['minutes']}分钟", self.lesson.split(f"<!-- V6_PAGE:{page_id} -->", 1)[1].split("<!-- V6_PAGE:", 1)[0])
            self.assertEqual(page["artifact_location"], page["script"]["evidence_location"])
            self.assertEqual(page["channel_split"]["teacher"], page["script"]["teacher_spoken"])

    def test_manifest_binds_generated_files_and_validator_rejects_tampering(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(5, len(manifest["files"]))
        valid = subprocess.run(
            ["python", "scripts/validate_meng_v6_lesson_package.py", "--mode", "stage", "--through", "opening", "--input", str(OUTPUT_DIR)],
            cwd=PROJECT_ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, valid.returncode, valid.stderr)
        self.assertIn("PACKAGE_OK", valid.stdout)
        with tempfile.TemporaryDirectory(prefix="meng_v6_opening_package_", dir=PROJECT_ROOT) as temp:
            copy_dir = Path(temp) / "package"
            shutil.copytree(OUTPUT_DIR, copy_dir)
            target = copy_dir / LESSON.name
            target.write_text(target.read_text(encoding="utf-8") + "\n篡改\n", encoding="utf-8")
            invalid = subprocess.run(
                ["python", "scripts/validate_meng_v6_lesson_package.py", "--mode", "stage", "--through", "opening", "--input", str(copy_dir)],
                cwd=PROJECT_ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(0, invalid.returncode)
            self.assertIn("PACKAGE_FILE_HASH_MISMATCH", invalid.stdout + invalid.stderr)

    def test_package_level_independent_review_binds_actual_semantic_materials(self):
        spec = importlib.util.spec_from_file_location(
            "validate_meng_v6_lesson_package", PROJECT_ROOT / "scripts" / "validate_meng_v6_lesson_package.py",
        )
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        receipt = json.loads(PACKAGE_REVIEW.read_text(encoding="utf-8"))
        self.assertEqual(module.reviewable_package_hash(OUTPUT_DIR), receipt["reviewed_package_sha256"])
        self.assertEqual((0, 0, 0), (receipt["p0"], receipt["p1"], receipt["p2"]))
        self.assertEqual("pass", receipt["status"])


if __name__ == "__main__":
    unittest.main()
