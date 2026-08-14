import hashlib
import json
import re
import subprocess
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v62_stage" / "chapter_4"
PACKAGE = STAGE / "package"
PPTX_DIR = STAGE / "pptx"
PPTX = PPTX_DIR / "04_氓_V63第四章课堂课件.pptx"


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MengV63Chapter4BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = [
            PACKAGE / "06_氓_V63第四章课程数据快照.json",
            PACKAGE / "chapter4_package_manifest.json",
            PPTX,
            PPTX_DIR / "chapter4_pptx_manifest.json",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise AssertionError("build artifacts before read-only tests: " + ", ".join(missing))

    def test_contract(self):
        result = json.loads(run("node", "scripts/verify_meng_v62_chapter4.js").stdout)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual((6, 33), (result["pages"], result["total_minutes"]))

    def test_source_and_package_hashes(self):
        snapshot = json.loads((PACKAGE / "06_氓_V63第四章课程数据快照.json").read_text())
        self.assertEqual(
            sha256(ROOT / "scripts" / "meng_v62" / "content" / "chapter_4.js"),
            snapshot["source_sha256"],
        )
        manifest = json.loads((PACKAGE / "chapter4_package_manifest.json").read_text())
        for item in manifest["files"]:
            self.assertEqual(item["sha256"], sha256(PACKAGE / item["name"]))

    def test_progressive_material_and_real_revision(self):
        worksheet = (PACKAGE / "04D_氓_V63第四章渐进学习单_C401读后发.md").read_text()
        self.assertIn('distribution: "C401 after complete reading; reveal one section at a time"', worksheet)
        first_fold = worksheet.split("请先折到这里", 1)[0]
        for answer in ["男子行为前后不一", "女子没有差错", "二三其德", "桑叶象征青春"]:
            self.assertNotIn(answer, first_fold)
        for action in ["□保留", "□改写", "□撤回"]:
            self.assertIn(action, worksheet)

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

        self.assertEqual((6, 6), (len(slide_xml), len(notes_xml)))
        for page_id, xml in zip(["C401", "C402", "C403", "C404", "C405", "C406"], notes_xml):
            self.assertIn(page_id, xml)
            self.assertIn("教师逐字稿", xml)
            self.assertIn("删除本页会失去什么", xml)

        frontstage = "\n".join(slide_xml)
        self.assertNotIn("让原词替你作证", frontstage)
        for leaked_answer in ["女子的投入，不分担", "受伤者归责", "桑叶象征青春", "男子失信责任", "声音在哪一句变硬", "责任判断"]:
            self.assertNotIn(leaked_answer, frontstage)
        self.assertIn("他的行为多次改变", frontstage)
        self.assertIn("一句你听来像在判断的话", frontstage)
        self.assertIn("她最后怎样", frontstage)

        manifest = json.loads((PPTX_DIR / "chapter4_pptx_manifest.json").read_text())
        self.assertEqual(6, len(manifest["physical_slides"]))
        self.assertEqual(manifest["sha256"], sha256(PPTX))


if __name__ == "__main__":
    unittest.main()
