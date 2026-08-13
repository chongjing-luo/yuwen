from __future__ import annotations

import json
import re
import subprocess
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v6_stage" / "prototypes"
PPTX = OUT / "04P_氓_V6三类页面视觉原型.pptx"
MANIFEST = OUT / "prototype_manifest.json"


class MengV6PrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            ["node", "scripts/build_meng_v6_prototypes.js"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_three_visual_duties_are_bound_to_three_physical_slides(self):
        self.assertEqual(
            [("N003", "活动界面"), ("N008", "全文/章内整读"), ("N012", "原文批注")],
            [(item["page_id"], item["primary_visual_duty"]) for item in self.manifest["physical_slides"]],
        )
        self.assertEqual("rendered_prototype_not_classroom_observed", self.manifest["claim_boundary"])

    def test_pptx_contains_exact_student_frontstage_and_complete_speaker_notes(self):
        with zipfile.ZipFile(PPTX) as archive:
            slide_xml = "\n".join(
                archive.read(f"ppt/slides/slide{index}.xml").decode("utf-8") for index in range(1, 4)
            )
            notes_xml = "\n".join(
                archive.read(f"ppt/notesSlides/notesSlide{index}.xml").decode("utf-8") for index in range(1, 4)
            )
        for phrase in (
            "自定1号", "按号轮说", "轮到我", "听别人", "听见新内容就勾", "暂无新增，从作品谱圈一项", "第一次完整听读", "女之耽兮",
            "先借四言节奏走进声音", "无斜线原句", "听者问", "读者带着完整动作再读",
            "在路标卡写下重读后改动的一处",
        ):
            self.assertIn(phrase, slide_xml)
        for page_id in ("N003", "N008", "N012"):
            self.assertIn(page_id, notes_xml)
        for marker in ("教师逐字稿", "场面与走位", "现场分支", "听者同步任务", "证据位置", "自然切页句"):
            self.assertIn(marker, notes_xml)
        self.assertNotRegex(slide_xml, re.compile(r"学生角色|设计意图|接收审计|页面功能"))


if __name__ == "__main__":
    unittest.main()
