# -*- coding: utf-8 -*-
"""反样板自证检查测试：含与 meng_v66/lesson.js 默认串的同步保护。"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "checks"))

from check_trace_evidence import (  # noqa: E402
    BOILERPLATE_EXACT,
    BOILERPLATE_FAILURE_SIGNALS,
    BOILERPLATE_PATTERNS,
    scan_lesson,
)

# 默认串的宿主已从 lesson.js（现为加载器）迁移为 canonical lesson.json
LESSON_SOURCE = Path(__file__).resolve().parents[1] / "work/teaching/选择性必修下册/氓/lesson.json"


def page(**kwargs):
    base = {"page_id": "T01", "title": "测试页"}
    base.update(kwargs)
    return base


class ScanLessonTest(unittest.TestCase):
    def test_exact_defaults_flagged(self):
        lesson = {"pages": [page(**{field: value for field, value in BOILERPLATE_EXACT.items()})]}
        findings = scan_lesson(lesson)
        fields = {f["field"] for f in findings}
        self.assertEqual(fields, set(BOILERPLATE_EXACT))

    def test_pattern_defaults_flagged(self):
        lesson = {
            "pages": [
                page(
                    literary_object="氓之蚩蚩",
                    unique_difficulty="学生容易看见“氓之蚩蚩”，却不能把它准确接回人物和前后故事。",
                    prior_input="学生已经完成前页任务，手中保留与“氓之蚩蚩”有关的原词或初稿。",
                    first_person_reception="我刚才面对“氓之蚩蚩”，留下了行动链；我能用原词说清自己新增或修正的理解。",
                    adjacent_counterproof="相邻页不同时处理“抱布贸丝的物象与语气”；合并会挤掉必要首答、校准或故事回接。",
                )
            ]
        }
        findings = scan_lesson(lesson)
        # adjacent_counterproof 换了具体内容仍命中模式——它同样是无逐页举证的句式替换
        fields = {f["field"] for f in findings}
        self.assertEqual(fields, {"unique_difficulty", "prior_input", "first_person_reception", "adjacent_counterproof"})

    def test_specific_content_not_flagged(self):
        lesson = {
            "pages": [
                page(
                    literary_object="犹可说也",
                    unique_difficulty="学生常把“说”读成说话，无法解释为何士之耽可脱而女之耽不可脱。",
                    prior_input="学生已在前页圈出两处“耽”字，但对“说”的字面还停留在现代义。",
                    info_state="首答态仅呈现原句与“说”字，脱的解释在学生猜词后揭示。",
                    teacher_role="先收学生的自然话猜测，再给出“说=脱”的释义并回到两句对照。",
                    story_return="由“可脱/不可脱”的对照回到女子发现自己没有退出余地这一处境变化。",
                    failure_signals=["学生把“说”翻译为说话且未修订", "对照页无学生修订痕迹"],
                )
            ]
        }
        findings = scan_lesson(lesson)
        self.assertEqual(findings, [])

    def test_literary_ellipsis_inside_specific_sentence_is_not_a_placeholder(self):
        lesson = {
            "pages": [
                page(
                    story_return="教师追问“后来呢……”，再回到女子临行前的最后一句。",
                )
            ]
        }
        self.assertEqual(scan_lesson(lesson), [])

    def test_failure_signals_default_list_flagged(self):
        lesson = {"pages": [page(failure_signals=list(BOILERPLATE_FAILURE_SIGNALS))]}
        findings = scan_lesson(lesson)
        self.assertEqual([f["field"] for f in findings], ["failure_signals"])

    def test_v25_nested_visual_placeholder_is_detected(self):
        lesson = {
            "schema_version": "2.5",
            "pages": [
                page(
                    slide_design={
                        "physical_screens": [
                            {"image_plan": {"content_brief": "待补充教材配图规格"}}
                        ]
                    }
                )
            ],
        }
        findings = scan_lesson(lesson)
        self.assertTrue(
            any(
                finding["kind"] == "placeholder"
                and "physical_screens" in finding["field"]
                for finding in findings
            )
        )

    def test_empty_pages(self):
        self.assertEqual(scan_lesson({"pages": []}), [])


@unittest.skipUnless(LESSON_SOURCE.exists(), "《氓》课程数据重制中（教案先行）；数据落盘后守卫自动恢复")
class LessonJsSyncTest(unittest.TestCase):
    """真数据必须保持零默认串：模板标记若再现即样板回潮（462→0 清零守卫）。"""

    def test_lesson_source_defaults_absent(self):
        source = LESSON_SOURCE.read_text(encoding="utf-8")
        for marker in [
            "学生容易看见",
            "却不能把它准确接回人物和前后故事",
            "学生已经完成前页任务",
            "首答前只给原诗、必要字面和一个自然问题",
            "个人先形成；需要交流时并行同桌或四人轮说",
            "准确释词、引用真实回答、追问原词、后置归纳并守住解释边界",
            "逐字稿内有首答等待、限定反馈和本人修订的明确时间",
            "学生依据原词、同伴追问或教师校准",
            "想不起、无新增、已经准确、不同意或暂时沉默均有诚实完成路径",
            "页面结束前由一句自然复述回到谁做了什么",
            "学生只能复述活动手续，不能复述诗意",
        ]:
            self.assertNotIn(marker, source, f"样板默认串回潮，请改写为该页具体陈述: {marker}")


if __name__ == "__main__":
    unittest.main()
