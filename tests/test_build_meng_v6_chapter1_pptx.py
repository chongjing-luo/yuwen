from __future__ import annotations

import json
import subprocess
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v6_stage" / "chapter_1" / "pptx"
PPTX = OUT / "04_氓_V6第一章课堂课件.pptx"
MANIFEST = OUT / "chapter1_pptx_manifest.json"
PAGE_IDS = [f"N{number:03d}" for number in range(13, 22)]


class MengV6Chapter1PptxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        package = subprocess.run(
            ["node", "scripts/build_meng_v6_chapter1_markdown.js"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if package.returncode:
            raise AssertionError(package.stderr or package.stdout)
        result = subprocess.run(
            ["node", "scripts/build_meng_v6_chapter1_pptx.js"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_nine_physical_slides_follow_the_logical_order(self):
        self.assertEqual(PAGE_IDS, [item["page_id"] for item in self.manifest["physical_slides"]])
        self.assertEqual(list(range(1, 10)), [item["physical_index"] for item in self.manifest["physical_slides"]])
        self.assertEqual("no_character_illustration_before_page_function_freeze", self.manifest["illustration_policy"])

    def test_pptx_passes_office_schema_validation(self):
        result = subprocess.run(
            ["python", "/home/ubuntu/.agents/skills/pptx/scripts/office/validate.py", str(PPTX)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("All validations PASSED", result.stdout)

    def test_each_slide_has_its_own_complete_notes(self):
        with zipfile.ZipFile(PPTX) as archive:
            notes = [archive.read(f"ppt/notesSlides/notesSlide{index}.xml").decode("utf-8") for index in range(1, 10)]
        for page_id, note in zip(PAGE_IDS, notes):
            self.assertIn(f"【V6页ID】{page_id}｜", note)
            for marker in ("教师逐字稿", "场面与走位", "时间盒", "现场分支", "听者同步任务", "证据位置", "自然切页句"):
                self.assertIn(marker, note)

    def test_line_two_visual_does_not_preload_surface_versus_reality(self):
        with zipfile.ZipFile(PPTX) as archive:
            line_two = archive.read("ppt/slides/slide3.xml").decode("utf-8")
        self.assertIn("诗句先写的动作", line_two)
        self.assertIn("女子随后说明的来意", line_two)
        self.assertNotIn("表面上", line_two)
        self.assertNotIn("实际上", line_two)

    def test_five_line_slides_keep_current_line_and_complete_chapter_track(self):
        with zipfile.ZipFile(PPTX) as archive:
            slides = [archive.read(f"ppt/slides/slide{index}.xml").decode("utf-8") for index in range(2, 7)]
        originals = [
            "氓之蚩蚩，抱布贸丝", "匪来贸丝，来即我谋", "送子涉淇，至于顿丘",
            "匪我愆期，子无良媒", "将子无怒，秋以为期",
        ]
        for slide, original in zip(slides, originals):
            self.assertIn(original, slide)
            for line in originals:
                self.assertIn(line, slide)
            self.assertIn("第一章", slide)
            self.assertIn("1 / 6", slide)

    def test_attempt_slides_do_not_show_finished_glosses_or_paraphrases(self):
        with zipfile.ZipFile(PPTX) as archive:
            line_slides = "\n".join(archive.read(f"ppt/slides/slide{index}.xml").decode("utf-8") for index in range(2, 7))
        for answer in (
            "忠厚的样子", "交易、交换", "他不是真来换丝，而是到我这里商量婚事",
            "不是我故意拖延婚期，是你没有合适的媒人",
        ):
            self.assertNotIn(answer, line_slides)

    def test_retrieval_and_first_impression_slides_do_not_leak_answers(self):
        with zipfile.ZipFile(PPTX) as archive:
            retrieval = archive.read("ppt/slides/slide7.xml").decode("utf-8")
            dossier = archive.read("ppt/slides/slide8.xml").decode("utf-8")
        self.assertIn("合上书", retrieval)
        self.assertNotIn("以贸丝姿态接近", retrieval)
        for phrase in ("诗里写着", "初读时我觉得", "现在还说不准"):
            self.assertIn(phrase, dossier)
        for token in ("伪装", "恋爱脑", "渣男"):
            self.assertNotIn(token, dossier)

    def test_reviewed_visual_regressions_are_prevented(self):
        namespaces = {
            "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        }

        def shape_texts(slide_xml: bytes) -> list[tuple[str, ET.Element]]:
            root = ET.fromstring(slide_xml)
            items = []
            for shape in root.findall(".//p:sp", namespaces):
                text = "".join(node.text or "" for node in shape.findall(".//a:t", namespaces))
                items.append((text, shape))
            return items

        with zipfile.ZipFile(PPTX) as archive:
            opening = shape_texts(archive.read("ppt/slides/slide1.xml"))
            line_five = shape_texts(archive.read("ppt/slides/slide6.xml"))
            close = "\n".join(text for text, _ in shape_texts(archive.read("ppt/slides/slide9.xml")))

        # N013's five-line poem is one centered reading field, rather than a
        # left-heavy block with unused visual weight on the right.
        for original in (
            "氓之蚩蚩，抱布贸丝。", "匪来贸丝，来即我谋。", "送子涉淇，至于顿丘。",
            "匪我愆期，子无良媒。", "将子无怒，秋以为期。",
        ):
            shape = next(shape for text, shape in opening if text == original)
            paragraph = shape.find(".//a:p/a:pPr", namespaces)
            self.assertIsNotNone(paragraph, original)
            self.assertEqual("ctr", paragraph.attrib.get("algn"), original)

        # N018's three operations must be physically separate text boxes.
        for instruction in ("她先在劝什么：________", "她又把什么定下来：________", "再标重音和停顿"):
            self.assertEqual(1, sum(text == instruction for text, _ in line_five), instruction)

        # N021 makes the two real actions legible without shrinking the poem.
        self.assertIn("完整重读", close)
        self.assertIn("合书讲30秒", close)

    def test_distinct_line_methods_are_physically_visible(self):
        with zipfile.ZipFile(PPTX) as archive:
            line_one = archive.read("ppt/slides/slide2.xml").decode("utf-8")
            line_four = archive.read("ppt/slides/slide5.xml").decode("utf-8")
        for phrase in ("谁", "怎样", "拿什么", "做什么", "只写眼前"):
            self.assertIn(phrase, line_one)
        for phrase in ("她在拒绝这门婚事", "她在说明此刻不能成婚的条件", "托住判断的原词"):
            self.assertIn(phrase, line_four)


if __name__ == "__main__":
    unittest.main()
