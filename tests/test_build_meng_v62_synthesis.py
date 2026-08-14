import hashlib
import json
import re
import subprocess
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v62_stage" / "synthesis"
PACKAGE = STAGE / "package"
PPTX_DIR = STAGE / "pptx"
PPTX = PPTX_DIR / "04_氓_V64全文综合课堂课件.pptx"


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MengV64SynthesisBuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = [
            PACKAGE / "06_氓_V64全文综合课程数据快照.json",
            PACKAGE / "synthesis_v64_package_manifest.json",
            PPTX,
            PPTX_DIR / "synthesis_v64_pptx_manifest.json",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise AssertionError("missing: " + ", ".join(missing))

    def test_contract_is_eight_events_and_seventy_nine_minutes(self):
        report = json.loads(run("node", "scripts/verify_meng_v62_synthesis.js").stdout)
        self.assertTrue(report["ok"], report["errors"])
        self.assertEqual((8, 79), (report["pages"], report["total_minutes"]))

    def test_source_and_package_hashes(self):
        snapshot = json.loads((PACKAGE / "06_氓_V64全文综合课程数据快照.json").read_text())
        self.assertEqual(sha(ROOT / "scripts" / "meng_v62" / "content" / "synthesis.js"), snapshot["source_sha256"])
        manifest = json.loads((PACKAGE / "synthesis_v64_package_manifest.json").read_text())
        for item in manifest["files"]:
            self.assertEqual(item["sha256"], sha(PACKAGE / item["name"]))

    def test_student_materials_close_all_reuse_chains(self):
        worksheet = (PACKAGE / "07G_氓_V64全文综合学习包.md").read_text()
        for expected in [
            "六张章末卡", "若没有断点", "可配回，无需改", "直接伤害责任", "诗中不能断言",
            "开课主题原话", "补充　□修正　□保留", "进入S07的一项", "同桌用另一组原句检验",
            "我的语文知识书页", "我仍愿继续追问", "可留白", "边界准确，无需改",
        ]:
            self.assertIn(expected, worksheet)
        for forbidden in ["五根纸梁", "鱼缸", "每组只贴一个", "必须保留一个分歧", "四张公开争议卡"]:
            self.assertNotIn(forbidden, worksheet)

    def test_pptx_has_eight_slides_complete_notes_and_new_order(self):
        with zipfile.ZipFile(PPTX) as archive:
            slide_names = sorted(
                [name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)],
                key=lambda name: int(re.search(r"\d+", Path(name).stem).group()),
            )
            notes_names = sorted(
                [name for name in archive.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", name)],
                key=lambda name: int(re.search(r"\d+", Path(name).stem).group()),
            )
            slides = [archive.read(name).decode() for name in slide_names]
            notes = [archive.read(name).decode() for name in notes_names]
        self.assertEqual((8, 8), (len(slides), len(notes)))
        for page_id, xml in zip(["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08"], notes):
            self.assertIn(page_id, xml)
            self.assertIn("教师逐字稿", xml)
            self.assertIn("删除本页会失去什么", xml)
        self.assertIn("O03真实主题谱照片", notes[3])
        self.assertIn("S05", notes[6])
        self.assertIn("S06", notes[6])
        self.assertIn("完整读到", notes[7])

    def test_frontstage_has_literary_objects_without_backend_procedures(self):
        with zipfile.ZipFile(PPTX) as archive:
            visible = "\n".join(
                archive.read(name).decode()
                for name in archive.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            )
        for expected in [
            "哪一步，改变了下一步", "找回原诗", "谁直接造成了伤害", "替当时的自己补上哪一句", "爱情与婚姻主题",
            "离开注释还认得吗", "分哪三类", "任选一组", "为什么非得这样写", "我的语文知识书页", "我仍愿继续追问", "可留白",
        ]:
            self.assertIn(expected, visible)
        for forbidden in [
            "鱼缸", "五根纸梁", "结构梁", "必须保留", "每组只贴", "固定争议", "生活分镜",
            "学生画像", "教学目标", "理解链", "知识收纳", "真实分歧", "课堂打开真实照片",
            "风·雅·颂", "《卫风·氓》",
        ]:
            self.assertNotIn(forbidden, visible)
        manifest = json.loads((PPTX_DIR / "synthesis_v64_pptx_manifest.json").read_text())
        self.assertEqual(8, len(manifest["physical_slides"]))
        self.assertEqual(manifest["sha256"], sha(PPTX))


if __name__ == "__main__":
    unittest.main()
