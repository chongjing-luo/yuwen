from __future__ import annotations

import json
import subprocess
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v6_stage" / "chapter_2" / "pptx"
PPTX = OUT / "04_氓_V6第二章课堂课件.pptx"
MANIFEST = OUT / "chapter2_pptx_manifest.json"
PAGE_IDS = [f"N{number:03d}" for number in range(22, 31)]


class MengV6Chapter2PptxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        package = subprocess.run(
            ["node", "scripts/build_meng_v6_chapter2_markdown.js"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if package.returncode:
            raise AssertionError(package.stderr or package.stdout)
        result = subprocess.run(
            ["node", "scripts/build_meng_v6_chapter2_pptx.js"], cwd=ROOT,
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
            for marker in (
                "教师逐字稿", "场面与走位", "时间盒", "现场分支", "听者同步任务",
                "证据位置", "自然切页句",
            ):
                self.assertIn(marker, note)

    def test_two_contrast_lines_and_two_reading_states_are_physical(self):
        with zipfile.ZipFile(PPTX) as archive:
            contrast = archive.read("ppt/slides/slide3.xml").decode("utf-8")
            design = archive.read("ppt/slides/slide4.xml").decode("utf-8")
            listening = archive.read("ppt/slides/slide5.xml").decode("utf-8")
        for line in ("不见复关，泣涕涟涟", "既见复关，载笑载言"):
            self.assertIn(line, contrast)
            self.assertIn(line, design)
            self.assertIn(line, listening)
        self.assertIn("先写朗读谱", design)
        self.assertIn("让听者闭眼", listening)

    def test_sightline_starts_with_the_woman_already_on_top_of_the_wall(self):
        """The generation state must not show a completed position-and-gaze answer."""
        with zipfile.ZipFile(PPTX) as archive:
            sightline = archive.read("ppt/slides/slide2.xml").decode("utf-8")
        self.assertNotIn("女子立于垝垣上", sightline)
        self.assertNotIn("女子所在处", sightline)
        self.assertNotIn('prst="chevron"', sightline)

    def test_contrast_generation_state_does_not_show_finished_alignment(self):
        with zipfile.ZipFile(PPTX) as archive:
            contrast = archive.read("ppt/slides/slide3.xml").decode("utf-8")
        for finished_pair in ("不见　↕　既见", "泣涕　↕　笑言", "涟涟　↕　载｜载"):
            self.assertNotIn(finished_pair, contrast)
        self.assertEqual(3, contrast.count("____  ↕  ____"))

    def test_generation_instructions_are_physical_and_do_not_use_backstage_labels(self):
        with zipfile.ZipFile(PPTX) as archive:
            sightline = archive.read("ppt/slides/slide2.xml").decode("utf-8")
            contrast = archive.read("ppt/slides/slide3.xml").decode("utf-8")
        self.assertIn("□ 目光", sightline)
        self.assertIn("□ 行走路线", sightline)
        self.assertNotIn("□ 目光　□ 行走路线", sightline)
        self.assertIn("独立填三组", contrast)
        self.assertNotIn("学生填写", contrast)

    def test_culture_and_parallel_pages_do_not_leak_overclaims(self):
        with zipfile.ZipFile(PPTX) as archive:
            visible = "\n".join(
                archive.read(f"ppt/slides/slide{index}.xml").decode("utf-8") for index in (6, 7)
            )
        for forbidden in ("证明婚姻幸福", "保证婚后幸福", "双方从此幸福"):
            self.assertNotIn(forbidden, visible)
        for required in ("尔卜尔筮，体无咎言", "以尔车来，以我贿迁"):
            self.assertIn(required, visible)

    def test_scrambled_retrieval_slide_does_not_show_finished_chain(self):
        with zipfile.ZipFile(PPTX) as archive:
            retrieval = archive.read("ppt/slides/slide8.xml").decode("utf-8")
        self.assertIn("七词复位", retrieval)
        self.assertNotIn("望 → 不见 → 泣 → 既见 → 笑言 → 卜筮 → 迁", retrieval)
        self.assertIn("换笔修订", retrieval)

    def test_culture_term_cards_keep_each_term_and_gloss_in_separate_boxes(self):
        namespaces = {
            "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        }
        with zipfile.ZipFile(PPTX) as archive:
            root = ET.fromstring(archive.read("ppt/slides/slide6.xml"))
        text_shapes = []
        for shape in root.findall(".//p:sp", namespaces):
            text = "".join(node.text or "" for node in shape.findall(".//a:t", namespaces))
            text_shapes.append((text, shape))
        texts = [text for text, _ in text_shapes]
        for term in ("卜", "筮", "体", "无咎言"):
            self.assertEqual(1, texts.count(term), term)
        for gloss in ("龟板", "蓍草", "兆象", "没有不祥之语"):
            self.assertEqual(1, texts.count(gloss), gloss)
        no_omen_shape = next(shape for text, shape in text_shapes if text == "无咎言")
        extent = no_omen_shape.find("./p:spPr/a:xfrm/a:ext", namespaces)
        self.assertIsNotNone(extent)
        self.assertGreaterEqual(int(extent.attrib["cx"]) / 914400, 1.35)


if __name__ == "__main__":
    unittest.main()
