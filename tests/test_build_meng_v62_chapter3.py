import hashlib
import json
import re
import subprocess
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v62_stage" / "chapter_3"
PACKAGE = STAGE / "package"
PPTX_DIR = STAGE / "pptx"
PPTX = PPTX_DIR / "04_氓_V63第三章课堂课件.pptx"


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MengV63Chapter3BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = [
            PACKAGE / "06_氓_V63第三章课程数据快照.json",
            PACKAGE / "chapter3_package_manifest.json",
            PPTX,
            PPTX_DIR / "chapter3_pptx_manifest.json",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise AssertionError("build artifacts before read-only tests: " + ", ".join(missing))

    def test_contract(self):
        result = json.loads(run("node", "scripts/verify_meng_v62_chapter3.js").stdout)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual((5, 30), (result["pages"], result["total_minutes"]))

    def test_source_and_package_hashes(self):
        snapshot = json.loads((PACKAGE / "06_氓_V63第三章课程数据快照.json").read_text())
        self.assertEqual(
            sha256(ROOT / "scripts" / "meng_v62" / "content" / "chapter_3.js"),
            snapshot["source_sha256"],
        )
        manifest = json.loads((PACKAGE / "chapter3_package_manifest.json").read_text())
        for item in manifest["files"]:
            self.assertEqual(item["sha256"], sha256(PACKAGE / item["name"]))

    def test_progressive_material_does_not_preempt_discovery(self):
        worksheet = (PACKAGE / "03C_氓_V63第三章渐进学习单_C301读后发.md").read_text()
        self.assertIn('distribution: "C301 after complete reading; reveal one section at a time"', worksheet)
        first_fold = worksheet.split("请先折到这里", 1)[0]
        for answer in ["比兴", "由物及人", "女子不可脱身", "桑叶象征青春"]:
            self.assertNotIn(answer, first_fold)

    def test_pptx_notes_order_and_frontstage(self):
        with zipfile.ZipFile(PPTX) as archive:
            slides = sorted(
                [name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)],
                key=lambda name: int(re.search(r"\d+", Path(name).stem).group()),
            )
            notes = sorted(
                [name for name in archive.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", name)],
                key=lambda name: int(re.search(r"\d+", Path(name).stem).group()),
            )
            slide_xml = [archive.read(name).decode() for name in slides]
            notes_xml = [archive.read(name).decode() for name in notes]

        self.assertEqual((5, 5), (len(slide_xml), len(notes_xml)))
        for page_id, xml in zip(["C301", "C302", "C303", "C305", "C306"], notes_xml):
            self.assertIn(page_id, xml)
            self.assertIn("教师逐字稿", xml)
            self.assertIn("删除本页会失去什么", xml)

        frontstage = "\n".join(slide_xml)
        for leaked_answer in ["桑叶象征青春", "女子的投入导致", "男子已实际离开", "标准答案"]:
            self.assertNotIn(leaked_answer, frontstage)

        manifest = json.loads((PPTX_DIR / "chapter3_pptx_manifest.json").read_text())
        self.assertEqual(5, len(manifest["physical_slides"]))
        self.assertEqual(manifest["sha256"], sha256(PPTX))


if __name__ == "__main__":
    unittest.main()
