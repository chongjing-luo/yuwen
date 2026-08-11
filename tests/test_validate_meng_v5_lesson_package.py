from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.validate_meng_v5_lesson_package import (
    EXPECTED_LINES,
    THREE_QUESTIONS,
    validate_data_contract,
    validate_markdown_contract,
    validate_pptx_contract,
)


def valid_notes(page: int) -> str:
    return (
        f"【页码与模块】P{page}｜模块一"
        "【承接上一页】教师指向刚才保留的原句，连接到本页。"
        "【教师原话】请先读眼前这一句，确认谁在做什么，再说明它让故事向哪里走。"
        "【学生动作与等待】学生默读二十秒，在原句下标出动作；教师保持安静并观察。"
        "【可能回应与接话】如果回答只有标签，教师请他补回原词；如果沉默，教师示范寻找动作。"
        "【可观察证据】一处原词标记和一句连续章意。"
        "【明确切页句】现在让现代汉语把这一步照亮，再切到下一页。"
    )


def valid_data() -> dict:
    modules = [
        {"id": "M1", "minutes": 47},
        {"id": "M2", "minutes": 49},
        {"id": "M3", "minutes": 52},
        {"id": "M4", "minutes": 45},
        {"id": "M5", "minutes": 37},
    ]
    slides = [
        {"id": "S01", "module": "M1", "phase": "opening", "kind": "question_overview", "visible": "关系过程｜现实处境｜责任与困境", "notes": valid_notes(1)},
        {"id": "S02", "module": "M1", "phase": "opening", "kind": "question", "question_index": 1, "visible": THREE_QUESTIONS[0], "notes": valid_notes(2)},
        {"id": "S03", "module": "M1", "phase": "opening", "kind": "question", "question_index": 2, "visible": THREE_QUESTIONS[1], "notes": valid_notes(3)},
        {"id": "S04", "module": "M1", "phase": "opening", "kind": "question", "question_index": 3, "visible": THREE_QUESTIONS[2], "notes": valid_notes(4)},
        {"id": "S05", "module": "M1", "phase": "opening", "kind": "first_full_read", "visible": "第一次完整听读", "notes": valid_notes(5)},
        {"id": "S06", "module": "M4", "phase": "return", "kind": "final_full_read", "visible": "再次完整朗读", "notes": valid_notes(6)},
        {"id": "S07", "module": "M4", "phase": "return", "kind": "question", "question_index": 1, "visible": THREE_QUESTIONS[0], "notes": valid_notes(7)},
        {"id": "S08", "module": "M4", "phase": "return", "kind": "question", "question_index": 2, "visible": THREE_QUESTIONS[1], "notes": valid_notes(8)},
        {"id": "S09", "module": "M5", "phase": "return", "kind": "question", "question_index": 3, "visible": THREE_QUESTIONS[2], "notes": valid_notes(9)},
        {"id": "S10", "module": "M5", "phase": "return", "kind": "responsibility_boundary", "visible": "困境线不能分担责任线中的责任", "notes": valid_notes(10)},
    ]
    return {
        "version": "5.0-text-spine",
        "total_minutes": 230,
        "modules": modules,
        "lines": [{"id": f"L{index:02d}", "original": line} for index, line in enumerate(EXPECTED_LINES, 1)],
        "meaning_units": [{"id": f"U{index:02d}"} for index in range(1, 13)],
        "three_questions": list(THREE_QUESTIONS),
        "causal_lines": {
            "responsibility": ["士贰其行", "二三其德", "至于暴矣", "不思其反"],
            "difficulty": ["初期信息有限", "情感和生活投入", "单边劳动", "支持缺失", "停止更加困难"],
            "links": [["士贰其行", "失信责任"], ["支持缺失", "停止更加困难"]],
        },
        "slides": slides,
    }


class DataContractTests(unittest.TestCase):
    def test_valid_v5_data_passes(self):
        self.assertEqual([], validate_data_contract(valid_data()))

    def test_missing_original_line_is_reported(self):
        data = valid_data()
        data["lines"] = data["lines"][:-1]

        errors = validate_data_contract(data)

        self.assertTrue(any("30组" in error or "亦已焉哉" in error for error in errors), errors)

    def test_total_minutes_must_be_230_and_match_modules(self):
        data = valid_data()
        data["total_minutes"] = 229

        errors = validate_data_contract(data)

        self.assertTrue(any("230" in error for error in errors), errors)

    def test_responsibility_and_difficulty_cannot_be_causally_linked(self):
        data = valid_data()
        data["causal_lines"]["links"].append(["情感和生活投入", "至于暴矣"])

        errors = validate_data_contract(data)

        self.assertTrue(any("责任线" in error and "困境线" in error for error in errors), errors)

    def test_three_questions_must_reappear_with_identical_wording(self):
        data = valid_data()
        data["slides"][8]["visible"] = "悲剧为何发生？"

        errors = validate_data_contract(data)

        self.assertTrue(any("第三问" in error and "同措辞" in error for error in errors), errors)

    def test_first_view_cannot_preannounce_modern_labels(self):
        data = valid_data()
        data["slides"][4]["visible"] = "警告信号与恋爱脑"

        errors = validate_data_contract(data)

        self.assertTrue(any("首次" in error and "恋爱脑" in error for error in errors), errors)

    def test_every_slide_requires_performable_notes(self):
        data = valid_data()
        data["slides"][2]["notes"] = "教师讲解第二问。"

        errors = validate_data_contract(data)

        self.assertTrue(any("S03" in error and "逐字稿" in error for error in errors), errors)


class MarkdownContractTests(unittest.TestCase):
    def valid_texts(self) -> dict[str, str]:
        all_lines = "\n".join(EXPECTED_LINES)
        questions = "\n".join(THREE_QUESTIONS)
        return {
            "lesson": f"V5 5.0-text-spine\n30组诗句\n12个意义句群\n230分钟\n责任线\n困境线\n{questions}\n{all_lines}",
            "worksheet": f"关系过程｜现实处境｜责任与困境\n原句证据｜现代生活转述｜解释边界\n{questions}",
            "script": "\n".join(valid_notes(page) for page in range(1, 11)),
            "audit": "桌面模拟，不是真实课堂数据\n可能体验\n可能思考\n可观察证据\n责任线\n困境线",
        }

    def test_valid_markdown_set_passes(self):
        self.assertEqual([], validate_markdown_contract(self.valid_texts()))

    def test_markdown_missing_explanation_boundary_is_reported(self):
        texts = self.valid_texts()
        texts["worksheet"] = texts["worksheet"].replace("解释边界", "标准答案")

        errors = validate_markdown_contract(texts)

        self.assertTrue(any("worksheet" in error and "解释边界" in error for error in errors), errors)


class PptxContractTests(unittest.TestCase):
    def make_pptx(self, path: Path, slide_count: int = 3, note_count: int = 3, forbidden: str = "") -> None:
        with zipfile.ZipFile(path, "w") as archive:
            for page in range(1, slide_count + 1):
                text = forbidden if page == 1 and forbidden else f"第{page}页"
                archive.writestr(f"ppt/slides/slide{page}.xml", f"<slide><text>{text}</text></slide>")
            for page in range(1, note_count + 1):
                archive.writestr(f"ppt/notesSlides/notesSlide{page}.xml", f"<notes>{valid_notes(page)}</notes>")

    def test_slide_note_count_mismatch_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "v5.pptx"
            self.make_pptx(path, slide_count=3, note_count=2)

            errors = validate_pptx_contract(path, expected_slide_count=3, first_view_pages={1})

            self.assertTrue(any("notes" in error and "count" in error for error in errors), errors)

    def test_first_view_forbidden_term_is_reported_in_pptx(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "v5.pptx"
            self.make_pptx(path, forbidden="初期伪装与警告信号")

            errors = validate_pptx_contract(path, expected_slide_count=3, first_view_pages={1})

            self.assertTrue(any("P1" in error and "伪装" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
