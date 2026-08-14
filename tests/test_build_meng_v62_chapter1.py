import hashlib
import json
import re
import subprocess
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v62_stage" / "chapter_1"
PACKAGE = STAGE / "package"
PPTX_DIR = STAGE / "pptx"
PPTX = PPTX_DIR / "04_氓_V62第一章课堂课件.pptx"


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MengV62Chapter1BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = [
            PACKAGE / "06_氓_V62第一章课程数据快照.json",
            PACKAGE / "chapter1_package_manifest.json",
            PPTX,
            PPTX_DIR / "chapter1_pptx_manifest.json",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise AssertionError(
                "build artifacts before running this read-only test suite: " + ", ".join(missing)
            )

    def test_contract_is_five_events_and_twenty_seven_minutes(self):
        result = run("node", "scripts/verify_meng_v62_chapter1.js")
        report = json.loads(result.stdout)
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual(5, report["pages"])
        self.assertEqual(27, report["total_minutes"])

    def test_markdown_outputs_are_source_synchronized(self):
        snapshot = json.loads((PACKAGE / "06_氓_V62第一章课程数据快照.json").read_text())
        source_sha = sha256(ROOT / "scripts" / "meng_v62" / "content" / "chapter_1.js")
        self.assertEqual(source_sha, snapshot["source_sha256"])
        master = (PACKAGE / "02_氓_V62第一章教学母版.md").read_text()
        script = (PACKAGE / "04A_氓_V62第一章逐页无生试讲稿.md").read_text()
        for page_id in ["C101", "C102", "C103", "C104", "C105"]:
            self.assertEqual(1, master.count(f"<!-- V62_PAGE:{page_id} -->"))
            self.assertEqual(1, script.count(f"<!-- V62_PAGE:{page_id} -->"))
        manifest = json.loads((PACKAGE / "chapter1_package_manifest.json").read_text())
        for item in manifest["files"]:
            self.assertEqual(item["sha256"], sha256(PACKAGE / item["name"]))

    def test_student_material_distribution_and_no_prefilled_answers(self):
        card_a = (PACKAGE / "03A_氓_V62第一章初读卡_C101发.md").read_text()
        card_b = (PACKAGE / "03B_氓_V62第一章细读与故事轨道_C102发.md").read_text()
        self.assertIn('distribution: "C101 only"', card_a)
        self.assertIn('distribution: "C102 only;', card_b)
        combined = card_a + "\n" + card_b
        for forbidden in [
            "男子看起来忠厚，抱着布来换丝", "女子送男子渡过淇水，一直送到顿丘",
            "不是我有意拖延婚期", "请你不要生气，就把秋天定作婚期",
            "婚后粗暴", "背叛", "压榨",
        ]:
            self.assertNotIn(forbidden, combined)
        self.assertNotIn("全文后再回看的原词或问号", card_b)
        self.assertNotIn("我想留到全文后再看的原词或问号", card_b)
        self.assertIn("将在第五章C503", card_b)

    def test_pptx_has_five_slides_complete_notes_and_expected_order(self):
        with zipfile.ZipFile(PPTX) as zf:
            slide_names = sorted(
                [name for name in zf.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)],
                key=lambda name: int(re.search(r"\d+", Path(name).stem).group()),
            )
            notes_names = sorted(
                [name for name in zf.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", name)],
                key=lambda name: int(re.search(r"\d+", Path(name).stem).group()),
            )
            self.assertEqual(5, len(slide_names))
            self.assertEqual(5, len(notes_names))
            slide_xml = [zf.read(name).decode("utf-8") for name in slide_names]
            notes_xml = [zf.read(name).decode("utf-8") for name in notes_names]
        titles = ["两个人怎样走近婚事", "抱布而来，是为了什么", "她把他送了多远", "她怎样把婚事继续说下去", "把这场相遇讲完整"]
        for expected, xml in zip(titles, slide_xml):
            self.assertIn(expected, xml)
        for page_id, xml in zip(["C101", "C102", "C103", "C104", "C105"], notes_xml):
            self.assertIn(page_id, xml)
            self.assertIn("教师逐字稿", xml)
            self.assertIn("本页不可替代的意义", xml)
            self.assertIn("删除本页会失去什么", xml)
            self.assertIn("自然切页句", xml)
        self.assertIn("按B键熄暗屏幕", notes_xml[4])
        self.assertIn("03A初读卡和03B细读单一起翻到背面", notes_xml[4])
        self.assertIn("一人读，一人听；交换，再读", slide_xml[3])
        self.assertIn("这四小句，各在做什么", slide_xml[3])
        self.assertNotIn("她先解释什么", slide_xml[3])
        self.assertNotIn("又在安抚什么", slide_xml[3])
        self.assertNotIn("最后，把什么定了下来", slide_xml[3])
        self.assertIn("看她怎样把话继续说下去", notes_xml[2])
        self.assertNotIn("请听她怎样解释、安抚，又怎样约定", notes_xml[2])

    def test_pptx_frontstage_has_no_answer_leaks_or_retired_nine_page_controls(self):
        with zipfile.ZipFile(PPTX) as zf:
            slide_text = "\n".join(
                zf.read(name).decode("utf-8")
                for name in zf.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            )
        for forbidden in [
            "男子看起来忠厚，抱着布来换丝", "女子送男子渡过淇水，一直送到顿丘",
            "不是我有意拖延婚期", "拒婚", "装老实欺骗", "签认", "查重", "回执",
        ]:
            self.assertNotIn(forbidden, slide_text)
        manifest = json.loads((PPTX_DIR / "chapter1_pptx_manifest.json").read_text())
        self.assertEqual(5, len(manifest["physical_slides"]))
        self.assertEqual(manifest["sha256"], sha256(PPTX))


if __name__ == "__main__":
    unittest.main()
