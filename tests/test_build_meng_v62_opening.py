import hashlib
import json
import re
import subprocess
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v62_stage" / "opening"
PACKAGE = STAGE / "package"
PPTX_DIR = STAGE / "pptx"
PPTX = PPTX_DIR / "04_氓_V62导入课堂课件.pptx"


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MengV62OpeningBuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = [
            PACKAGE / "06_氓_V62导入课程数据快照.json",
            PACKAGE / "opening_package_manifest.json",
            PPTX,
            PPTX_DIR / "opening_pptx_manifest.json",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise AssertionError("build artifacts before read-only tests: " + ", ".join(missing))

    def test_contract(self):
        report = json.loads(run("node", "scripts/verify_meng_v62_opening.js").stdout)
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual((9, 31), (report["pages"], report["total_minutes"]))

    def test_source_sync(self):
        snapshot = json.loads((PACKAGE / "06_氓_V62导入课程数据快照.json").read_text())
        source = ROOT / "scripts" / "meng_v62" / "content" / "opening.js"
        self.assertEqual(sha256(source), snapshot["source_sha256"])
        manifest = json.loads((PACKAGE / "opening_package_manifest.json").read_text())
        for item in manifest["files"]:
            self.assertEqual(item["sha256"], sha256(PACKAGE / item["name"]))

    def test_opening_breadth_and_no_prefilled_theme(self):
        recall = (PACKAGE / "03A_爱情与婚姻文学回忆单_O01发.md").read_text()
        self.assertIn("篇名", recall)
        self.assertIn("一句话唤回故事", recall)
        self.assertIn("它让我想到什么", recall)
        self.assertIn("从小学一直想到高中", recall)
        for answer in ["等待、错过、相守、选择", "背叛", "恋爱脑", "沉没成本"]:
            self.assertNotIn(answer, recall)

    def test_pptx_notes_and_frontstage(self):
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
        self.assertEqual((9, 9), (len(slide_xml), len(notes_xml)))
        for page_id, xml in zip([f"O{index:02d}" for index in range(1, 10)], notes_xml):
            self.assertIn(page_id, xml)
            self.assertIn("教师逐字稿", xml)
            self.assertIn("删除本页会失去什么", xml)
        visible = "\n".join(slide_xml[:3])
        for text in ["等待、错过、相守、选择", "学生画像", "从黑板上的旧故事"]:
            self.assertNotIn(text, visible)
        manifest = json.loads((PPTX_DIR / "opening_pptx_manifest.json").read_text())
        self.assertEqual(9, len(manifest["physical_slides"]))
        self.assertEqual(manifest["sha256"], sha256(PPTX))


if __name__ == "__main__":
    unittest.main()
