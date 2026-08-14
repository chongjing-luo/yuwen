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
WORKSHEET_A = OUTPUT_DIR / "03A_爱情与婚姻文学回忆单.md"
WORKSHEET_B = OUTPUT_DIR / "03B_氓_V6导入阅读卡.md"
WORKSHEET_C = OUTPUT_DIR / "03C_氓_V6初听后路标卡.md"
MATERIALS = OUTPUT_DIR / "03D_氓_V6导入物料包.md"
SCRIPT = OUTPUT_DIR / "04A_氓_V6导入切片逐页无生试讲稿.md"
SNAPSHOT = OUTPUT_DIR / "06_氓_V6导入切片课程数据快照.json"
MANIFEST = OUTPUT_DIR / "opening_package_manifest.json"
PACKAGE_REVIEW = PROJECT_ROOT / "scripts" / "meng_v6" / "reviews" / "opening_package.json"


def build(out: Path = OUTPUT_DIR) -> subprocess.CompletedProcess[str]:
    audit = subprocess.run(
        ["python", "scripts/build_meng_v6_opening.py", "--allow-pending-review"],
        cwd=PROJECT_ROOT, text=True, capture_output=True, check=False,
    )
    if audit.returncode:
        return audit
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
        cls.worksheet_c = WORKSHEET_C.read_text(encoding="utf-8")
        cls.materials = MATERIALS.read_text(encoding="utf-8")
        cls.worksheet = cls.worksheet_a + "\n" + cls.worksheet_b + "\n" + cls.worksheet_c
        cls.script = SCRIPT.read_text(encoding="utf-8")

    def test_all_three_markdown_channels_and_snapshot_share_the_same_eleven_pages(self):
        expected = ["N002", "N003", "N004", "N005", "N001", "N007", "N008", "N009", "N010", "N011", "N012"]
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

    def test_n011_two_physical_states_are_separate_authoritative_scenes(self):
        page = next(item for item in self.snapshot["pages"] if item["page_id"] == "N011")
        occurrences = page["physical_occurrences"]
        self.assertEqual(["N011_INPUT", "N011_RECALL"], [item["occurrence_id"] for item in occurrences])
        self.assertEqual([75, 45], [item["seconds"] for item in occurrences])
        self.assertEqual(120, sum(item["seconds"] for item in occurrences))
        self.assertIn("先把三块路标说清", occurrences[0]["teacher_spoken"])
        self.assertNotIn("屏幕上的答案已经收起", occurrences[0]["teacher_spoken"])
        self.assertIn("屏幕上的答案已经收起", occurrences[1]["teacher_spoken"])
        self.assertNotIn("先把三块路标说清", occurrences[1]["teacher_spoken"])
        self.assertNotIn("请再补全：她在回望自己的婚姻经历", occurrences[1]["teacher_spoken"])
        self.assertIn("听者不要报答案", occurrences[1]["teacher_spoken"])
        self.assertIn("### N011_INPUT｜给答态｜75秒", self.script)
        self.assertIn("### N011_RECALL｜撤答态｜45秒", self.script)

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
            "篇名＋它写了什么", "小组作品谱", "我未想到的一项", "连接",
            "卡号", "临时命名", "保留／改名／移回",
            "最想追踪的一问", "尚未找到", "同桌让我补记", "谁在回望什么", "谁做什么",
        ):
            self.assertIn(phrase, self.worksheet)
        for prefilled in (
            "相遇的欣悦，需要真实了解", "婚姻的选择，需要尊重与行动",
            "共同生活，需要平衡、支持与边界", "遇人不淑", "恋爱脑",
        ):
            self.assertNotIn(prefilled, self.worksheet)

    def test_contribution_cards_preserve_original_proposer_authorship(self):
        for phrase in ("组号", "原提议者号", "原提议者亲写", "原提议者签认"):
            self.assertIn(phrase, self.worksheet_a + "\n" + self.materials)
        n003 = next(item for item in self.snapshot["pages"] if item["page_id"] == "N003")
        self.assertIn("原提议者号", n003["student_visible_text"])
        self.assertIn("亲手写卡或在卡上签认", n003["script"]["teacher_spoken"])

    def test_late_scaffolds_are_on_a_separately_distributed_card(self):
        self.assertNotIn("三块最小路标", self.worksheet_a)
        self.assertNotIn("谁在回望什么", self.worksheet_a)
        self.assertNotIn("谁做什么", self.worksheet_a)
        self.assertIn('distribution_timing: "after_first_listening_and_mark"', self.worksheet_c)
        self.assertIn("三块最小路标", self.worksheet_c)
        self.assertIn("没有斜线的原句", self.worksheet_c)
        self.assertIn("《诗经》篇数：305篇", self.worksheet_c)
        self.assertIn("需要调整", self.worksheet_c)
        self.assertIn("原本读顺", self.worksheet_c)
        self.assertIn("教师说“看教材”", self.worksheet_c)
        self.assertIn("读者带着完整动作再读", self.worksheet_c)
        self.assertIn("四轮后，每人圈出最想带进全班的两项", self.worksheet_a)
        self.assertGreaterEqual(self.worksheet_a.count("□作品／主题"), 4)
        self.assertIn("□暂无新增", self.worksheet_a)

    def test_every_pre_reveal_student_channel_has_zero_meng_leakage(self):
        self.assertNotIn("氓", WORKSHEET_A.name)
        self.assertNotIn("氓", self.worksheet_a)
        self.assertNotIn("lesson:", self.worksheet_a)
        pre_reveal = self.snapshot["pages"][:4]
        for page in pre_reveal:
            self.assertNotIn("《氓》", page["student_visible_text"])
            self.assertNotIn("《氓》", page["script"]["teacher_spoken"])

    def test_material_pack_makes_the_recall_activity_physically_executable(self):
        for phrase in ("本班已学篇目目录索引", "只写篇名的提示条", "空白贡献卡", "磁贴", "拍照备份", "下节课"):
            self.assertIn(phrase, self.materials)

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
        self.assertEqual(36, self.snapshot["total_minutes"])
        for page in self.snapshot["pages"]:
            page_id = page["page_id"]
            self.assertIn(f"{page['minutes']}分钟", self.lesson.split(f"<!-- V6_PAGE:{page_id} -->", 1)[1].split("<!-- V6_PAGE:", 1)[0])
            self.assertEqual(page["artifact_location"], page["script"]["evidence_location"])
            self.assertEqual(page["channel_split"]["teacher"], page["script"]["teacher_spoken"])

    def test_manifest_binds_generated_files_and_validator_rejects_tampering(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(7, len(manifest["files"]))
        valid = subprocess.run(
            ["python", "scripts/validate_meng_v6_lesson_package.py", "--mode", "stage", "--through", "opening", "--allow-pending-review", "--input", str(OUTPUT_DIR)],
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
                ["python", "scripts/validate_meng_v6_lesson_package.py", "--mode", "stage", "--through", "opening", "--allow-pending-review", "--input", str(copy_dir)],
                cwd=PROJECT_ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(0, invalid.returncode)
            self.assertIn("PACKAGE_FILE_HASH_MISMATCH", invalid.stdout + invalid.stderr)

    def test_package_level_review_matches_the_frozen_semantics(self):
        spec = importlib.util.spec_from_file_location(
            "validate_meng_v6_lesson_package", PROJECT_ROOT / "scripts" / "validate_meng_v6_lesson_package.py",
        )
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        receipt = json.loads(PACKAGE_REVIEW.read_text(encoding="utf-8"))
        current_hash = module.reviewable_package_hash(OUTPUT_DIR)
        if current_hash != receipt["reviewed_package_sha256"]:
            self.assertNotEqual(current_hash, receipt["reviewed_package_sha256"])
            return
        self.assertEqual("pass", receipt["status"])
        self.assertEqual(0, receipt["p0"] + receipt["p1"] + receipt["p2"])


if __name__ == "__main__":
    unittest.main()
