from __future__ import annotations

import json
import re
import subprocess
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v6_stage" / "opening" / "pptx"
PPTX = OUT / "04_氓_V6导入课堂课件.pptx"
MANIFEST = OUT / "opening_pptx_manifest.json"
PAGE_IDS = ["N002", "N003", "N004", "N005", "N001", "N007", "N008", "N009", "N010", "N011", "N011", "N012"]
DRAWING_NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def run_font_sizes(xml: str, phrase: str) -> set[int]:
    root = ET.fromstring(xml)
    sizes: set[int] = set()
    for run in root.findall(".//a:r", DRAWING_NS):
        text = "".join(node.text or "" for node in run.findall("a:t", DRAWING_NS))
        if phrase not in text:
            continue
        props = run.find("a:rPr", DRAWING_NS)
        if props is not None and props.get("sz"):
            sizes.add(int(props.get("sz")))
    return sizes


class MengV6OpeningPptxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        audit = subprocess.run(
            ["python", "scripts/build_meng_v6_opening.py", "--allow-pending-review"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if audit.returncode:
            raise AssertionError(audit.stderr or audit.stdout)
        package = subprocess.run(
            ["node", "scripts/build_meng_v6_markdown.js", "--through", "opening"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if package.returncode:
            raise AssertionError(package.stderr or package.stdout)
        result = subprocess.run(
            ["node", "scripts/build_meng_v6_opening_pptx.js"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_all_current_opening_pages_map_bijectively_to_physical_slides(self):
        self.assertEqual(PAGE_IDS, [item["page_id"] for item in self.manifest["physical_slides"]])
        self.assertEqual(list(range(1, 13)), [item["physical_index"] for item in self.manifest["physical_slides"]])
        self.assertEqual("rendered_opening_not_classroom_observed", self.manifest["claim_boundary"])

    def test_each_slide_has_complete_rehearsal_notes_and_no_backstage_leak(self):
        with zipfile.ZipFile(PPTX) as archive:
            slide_xml = "\n".join(
                archive.read(f"ppt/slides/slide{index}.xml").decode("utf-8") for index in range(1, 13)
            )
            notes_xml = "\n".join(
                archive.read(f"ppt/notesSlides/notesSlide{index}.xml").decode("utf-8") for index in range(1, 13)
            )
        for page_id in PAGE_IDS:
            expected_count = 2 if page_id == "N011" else 1
            self.assertEqual(expected_count, notes_xml.count(f"【V6页ID】{page_id}｜"), page_id)
        for marker in ("教师逐字稿", "场面与走位", "现场分支", "听者同步任务", "证据位置", "自然切页句"):
            self.assertEqual(12, notes_xml.count(marker), marker)
        self.assertNotRegex(slide_xml, re.compile(r"学生角色|林晓|设计意图|接收审计|页面功能|理解链|知识碎片"))

    def test_frontstage_preserves_each_pages_unique_student_action(self):
        with zipfile.ZipFile(PPTX) as archive:
            per_slide = [archive.read(f"ppt/slides/slide{index}.xml").decode("utf-8") for index in range(1, 13)]
        required = {
            "N001": ("氓", "诗经·卫风"),
            "N002": ("爱情或婚姻故事", "尽量多写", "至少一篇"),
            "N003": ("听见新内容就勾", "每组写两张贡献卡"),
            "N004": ("每组贴两张卡", "听众"),
            "N005": ("每人先连一组", "三位同学上台", "临时命名", "保留／改名／移回"),
            "N007": ("她经历了什么", "走到这一步"),
            "N008": ("第一章", "女之耽兮"),
            "N009": ("第四章", "亦已焉哉"),
            "N010": ("把第一次听见的《氓》留在纸上", "我想问"),
            "N011": (),
            "N012": ("无斜线原句", "原本读顺"),
        }
        for index, page_id in enumerate(PAGE_IDS):
            for phrase in required[page_id]:
                self.assertIn(phrase, per_slide[index], f"{page_id}: {phrase}")
        self.assertIn("305篇", per_slide[9])
        self.assertIn("女子第一人称", per_slide[9])
        self.assertNotIn("305篇", per_slide[10])
        self.assertIn("这是怎样的一部", per_slide[10])
        self.assertIn("诗歌总集", per_slide[10])

    def test_static_frontstage_does_not_leak_delayed_support_or_teacher_design_thought(self):
        with zipfile.ZipFile(PPTX) as archive:
            slide_1 = archive.read("ppt/slides/slide1.xml").decode("utf-8")
            first_four = "\n".join(archive.read(f"ppt/slides/slide{index}.xml").decode("utf-8") for index in range(1, 5))
        self.assertNotIn("翻教材目录", slide_1)
        self.assertNotIn("领取篇名提示条", slide_1)
        self.assertIn("先独立回想", slide_1)
        self.assertNotIn("暂不翻目录", slide_1)
        self.assertNotIn("《氓》", first_four)

    def test_honest_branches_are_visually_equal_not_hidden_in_footers(self):
        with zipfile.ZipFile(PPTX) as archive:
            n004 = archive.read("ppt/slides/slide3.xml").decode("utf-8")
            n010 = archive.read("ppt/slides/slide9.xml").decode("utf-8")
            n012 = archive.read("ppt/slides/slide12.xml").decode("utf-8")
        for phrase in ("卡墙还没有", "卡墙已有相同内容"):
            self.assertIn(phrase, n004)
        for phrase in ("有一句把我留住", "尚未找到"):
            self.assertIn(phrase, n010)
        for phrase in ("需要调整", "原本读顺"):
            self.assertIn(phrase, n012)
        with zipfile.ZipFile(PPTX) as archive:
            n003 = archive.read("ppt/slides/slide2.xml").decode("utf-8")
        self.assertTrue(run_font_sizes(n003, "每人圈两项"))
        self.assertTrue(run_font_sizes(n003, "暂无新增，也从作品谱选两项"))
        self.assertGreaterEqual(min(run_font_sizes(n003, "暂无新增，也从作品谱选两项")), 2200)
        for phrase in ("有新增", "暂无新增", "核对一张重复卡"):
            self.assertIn(phrase, n004)

    def test_n005_keeps_student_authorship_and_revision_visible(self):
        with zipfile.ZipFile(PPTX) as archive:
            n005 = archive.read("ppt/slides/slide4.xml").decode("utf-8")
        for phrase in ("每人先连一组", "三位同学上台", "临时命名", "保留／改名／移回"):
            self.assertIn(phrase, n005)
        for fixed_category in ("相遇的欢喜", "等待、错过、阻隔、相守与破裂"):
            self.assertNotIn(fixed_category, n005)

    def test_n003_contribution_cards_preserve_original_proposer_authorship(self):
        with zipfile.ZipFile(PPTX) as archive:
            n003 = archive.read("ppt/slides/slide2.xml").decode("utf-8")
            n003_notes = archive.read("ppt/notesSlides/notesSlide2.xml").decode("utf-8")
        for phrase in ("组号－卡号－原提议者号", "原提议者签认"):
            self.assertIn(phrase, n003)
        self.assertIn("原提议者写卡或签认", n003_notes)

    def test_n011_recall_state_preserves_the_three_card_color_mapping(self):
        with zipfile.ZipFile(PPTX) as archive:
            n011_recall = archive.read("ppt/slides/slide11.xml").decode("utf-8")
        for color in ("B18B52", "4E7480", "A84A3A"):
            self.assertIn(color, n011_recall)

    def test_n011_two_physical_states_have_distinct_occurrence_notes(self):
        with zipfile.ZipFile(PPTX) as archive:
            input_slide = archive.read("ppt/slides/slide10.xml").decode("utf-8")
            recall_slide = archive.read("ppt/slides/slide11.xml").decode("utf-8")
            input_notes = archive.read("ppt/notesSlides/notesSlide10.xml").decode("utf-8")
            recall_notes = archive.read("ppt/notesSlides/notesSlide11.xml").decode("utf-8")
        self.assertIn("先写下三个词｜下一屏撤答后再开口", input_slide)
        self.assertNotIn("同桌各用一句话说", input_slide)
        self.assertNotIn("写下三个词，再开口复述", input_slide)
        self.assertIn("扣住路标卡", recall_slide)
        self.assertIn("【物理状态】给答态｜75秒", input_notes)
        self.assertIn("先把三块路标说清", input_notes)
        self.assertNotIn("屏幕上的答案已经收起", input_notes)
        self.assertIn("【物理状态】撤答态｜45秒", recall_notes)
        self.assertIn("屏幕上的答案已经收起", recall_notes)
        self.assertNotIn("先把三块路标说清", recall_notes)
        self.assertNotIn("请再补全：她在回望自己的婚姻经历", recall_notes)
        self.assertIn("听者不要报答案", recall_notes)
        snapshot = json.loads((OUT.parent / "package" / "06_氓_V6导入切片课程数据快照.json").read_text(encoding="utf-8"))
        n011 = next(item for item in snapshot["pages"] if item["page_id"] == "N011")
        self.assertIn(n011["physical_occurrences"][0]["student_visible_prompt"], input_slide)
        self.assertIn(n011["physical_occurrences"][1]["student_visible_prompt"], recall_slide)
        self.assertIn(n011["physical_occurrences"][0]["teacher_spoken"], input_notes)
        self.assertIn(n011["physical_occurrences"][1]["teacher_spoken"], recall_notes)

    def test_manifest_records_one_visual_duty_and_one_unique_function_per_slide(self):
        for item in self.manifest["physical_slides"]:
            self.assertTrue(item["primary_visual_duty"])
            self.assertTrue(item["unique_function"])
            self.assertTrue(item["artifact_location"])
        self.assertEqual("no_character_illustration", self.manifest["illustration_policy"])


if __name__ == "__main__":
    unittest.main()
