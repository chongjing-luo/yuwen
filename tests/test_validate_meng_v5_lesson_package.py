from __future__ import annotations

import tempfile
import unittest
import zipfile
import json
from pathlib import Path

from scripts.validate_meng_v5_lesson_package import (
    EXPECTED_LINES,
    THREE_QUESTIONS,
    validate_data_contract,
    validate_markdown_contract,
    validate_pptx_contract,
)


ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / "work" / "备课" / "选择性必修下册" / "氓"
SNAPSHOT = LESSON_DIR / "06_氓_V5课程数据快照.json"
PPT_MASTER = LESSON_DIR / "04_氓_V5全文逐句课堂课件_完整母版.pptx"
MODULE_PPTX = {
    "M1": LESSON_DIR / "04B1_氓_V5模块一_从旧故事走进初见.pptx",
    "M2": LESSON_DIR / "04B2_氓_V5模块二_等待与回望中的劝诫.pptx",
    "M3": LESSON_DIR / "04B3_氓_V5模块三_婚后事实与长期处境.pptx",
    "M4": LESSON_DIR / "04B4_氓_V5模块四_回望六章把她的日子讲出来.pptx",
    "M5": LESSON_DIR / "04B5_氓_V5模块五_辨明伤害把提醒留给后来人.pptx",
}
MARKDOWN_FILES = {
    "lesson": LESSON_DIR / "02_氓_V5全文逐句教学母版.md",
    "worksheet": LESSON_DIR / "03_氓_V5学生学习单.md",
    "script": LESSON_DIR / "04A_氓_V5逐页无生试讲稿.md",
    "audit": LESSON_DIR / "08_氓_V5学生接收桌面审计.md",
}


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
        {"id": "M4", "minutes": 69},
        {"id": "M5", "minutes": 57},
    ]
    slides = [
        {"id": "S01", "module": "M1", "phase": "opening", "kind": "question_overview", "visible": "她经历了什么｜她的日子苦在哪里｜这场婚姻为什么走到这一步", "notes": valid_notes(1)},
        {"id": "S02", "module": "M1", "phase": "opening", "kind": "question", "question_index": 1, "visible": THREE_QUESTIONS[0], "notes": valid_notes(2)},
        {"id": "S03", "module": "M1", "phase": "opening", "kind": "question", "question_index": 2, "visible": THREE_QUESTIONS[1], "notes": valid_notes(3)},
        {"id": "S04", "module": "M1", "phase": "opening", "kind": "question", "question_index": 3, "visible": THREE_QUESTIONS[2], "notes": valid_notes(4)},
        {"id": "S05", "module": "M1", "phase": "opening", "kind": "first_full_read", "visible": "第一次完整听读", "notes": valid_notes(5)},
        {"id": "S06", "module": "M4", "phase": "return", "kind": "final_full_read", "visible": "再次完整朗读", "notes": valid_notes(6)},
        {"id": "S07", "module": "M4", "phase": "return", "kind": "question", "question_index": 1, "visible": THREE_QUESTIONS[0], "notes": valid_notes(7)},
        {"id": "S08", "module": "M4", "phase": "return", "kind": "question", "question_index": 2, "visible": THREE_QUESTIONS[1], "notes": valid_notes(8)},
        {"id": "S09", "module": "M5", "phase": "return", "kind": "question", "question_index": 3, "visible": THREE_QUESTIONS[2], "notes": valid_notes(9)},
        {"id": "S10", "module": "M4", "phase": "question", "kind": "story_prepare", "visible": "六章，六位讲述者", "notes": valid_notes(10) + "学生独立准备，小组共同讲述。"},
        {"id": "S11", "module": "M4", "phase": "question", "kind": "story_relay", "visible": "把她的一生讲出来", "notes": valid_notes(11) + "六组接力，听众记录故事空缺。"},
        {"id": "S12", "module": "M4", "phase": "question", "kind": "story_turning", "visible": "哪一步真正改变了她的命运？", "notes": valid_notes(12) + "每名学生独立写出转折判断，再向全班表达。"},
        {"id": "S13", "module": "M4", "phase": "return", "kind": "story_revise", "visible": "她从淇水这边走到淇水那边", "notes": valid_notes(13) + "学生个人依据同伴追问完成修订。"},
        {"id": "S14", "module": "M4", "phase": "question", "kind": "scene_choose", "visible": "让诗句重新长成日子", "notes": valid_notes(14) + "每名学生先选择生活时刻，再进入小组。"},
        {"id": "S15", "module": "M4", "phase": "question", "kind": "scene_build", "visible": "把这一幕讲给今天的人听", "notes": valid_notes(15) + "小组共同排演生活镜头。"},
        {"id": "S16", "module": "M4", "phase": "question", "kind": "scene_present", "visible": "哪一句诗托住了这一幕？", "notes": valid_notes(16) + "听众回到诗句，并指出合理想象。"},
        {"id": "S17", "module": "M4", "phase": "question", "kind": "scene_reflect", "visible": "她的苦，不只是一件事", "notes": valid_notes(17) + "学生独立写一句总结，再与同桌互读。"},
        {"id": "S18", "module": "M4", "phase": "return", "kind": "scene_revise", "visible": "她的日子，原来这样沉重", "notes": valid_notes(18) + "学生个人根据全班讲述完成修改和修订。"},
        {"id": "S19", "module": "M5", "phase": "question", "kind": "responsibility_choose", "visible": "先把责任说清", "notes": valid_notes(19) + "每名学生独立选择诗句，再与小组交换。"},
        {"id": "S20", "module": "M5", "phase": "question", "kind": "responsibility_challenge", "visible": "你说的是诗中事实，还是补写的动机？", "notes": valid_notes(20) + "另一组追问，发言者回到原句和诗句。"},
        {"id": "S21", "module": "M5", "phase": "question", "kind": "difficulty_discuss", "visible": "她要停下这段关系，会面对什么？", "notes": valid_notes(21) + "四个小组分别寻找诗句。"},
        {"id": "S22", "module": "M5", "phase": "question", "kind": "difficulty_present", "visible": "哪些东西绊住了她的脚步？", "notes": valid_notes(22) + "各组呈现，听众补充、质疑并推动修改。"},
        {"id": "S23", "module": "M5", "phase": "question", "kind": "marriage_write", "visible": "把一句提醒留给后来人", "notes": valid_notes(23) + "每名学生独立写一句提醒，并补一处原诗。"},
        {"id": "S24", "module": "M5", "phase": "question", "kind": "marriage_share", "visible": "让彼此的句子被听见", "notes": valid_notes(24) + "同桌互读，再向全班分享。"},
        {"id": "S25", "module": "M5", "phase": "return", "kind": "marriage_after", "visible": "诗没有替后来人写完答案", "notes": valid_notes(25) + "教师依据学生原话收束，学生完成最后修订。"},
    ]
    return {
        "version": "5.3-literary-participation",
        "total_minutes": 274,
        "modules": modules,
        "lines": [{"id": f"L{index:02d}", "original": line} for index, line in enumerate(EXPECTED_LINES, 1)],
        "meaning_units": [{"id": f"U{index:02d}"} for index in range(1, 13)],
        "three_questions": list(THREE_QUESTIONS),
        "causal_lines": {
            "responsibility": ["士贰其行", "二三其德", "至于暴矣", "不思其反"],
            "difficulty": ["初期信息有限", "情感和生活投入", "单边劳动", "支持缺失", "性别与时代处境", "停止更加困难"],
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

    def test_total_minutes_must_be_274_and_match_modules(self):
        data = valid_data()
        data["total_minutes"] = 273

        errors = validate_data_contract(data)

        self.assertTrue(any("274" in error for error in errors), errors)

    def test_three_questions_use_literary_spoken_wording(self):
        self.assertEqual(
            (
                "她怎样从“送子涉淇”一步步走到“亦已焉哉”？",
                "她婚后的日子，究竟苦在哪里？",
                "这场婚姻为什么会走到这一步？谁应为伤害负责？当她说出“亦已焉哉”，还要面对哪些阻力？",
            ),
            THREE_QUESTIONS,
        )

    def test_all_three_synthesis_activities_require_real_participation_stages(self):
        data = valid_data()
        data["slides"] = [slide for slide in data["slides"] if slide["kind"] != "scene_present"]

        errors = validate_data_contract(data)

        self.assertTrue(any("scene_present" in error and "真实参与" in error for error in errors), errors)

    def test_student_frontstage_rejects_project_management_language(self):
        data = valid_data()
        data["slides"][9]["visible"] = "建立责任线与困境线，完成共同回收"

        errors = validate_data_contract(data)

        self.assertTrue(any("frontstage" in error and "责任线" in error for error in errors), errors)

    def test_repeated_ai_checking_template_is_rejected(self):
        data = valid_data()
        data["slides"][9]["notes"] += "保留一处，修正一处，并为修改补回原句。"

        errors = validate_data_contract(data)

        self.assertTrue(any("AI式核对模板" in error for error in errors), errors)

    def test_frontstage_rejects_deterministic_turning_point_and_analysis_jargon(self):
        data = valid_data()
        data["slides"][9]["visible"] = "找出真正的转折，再完成两类判断"

        errors = validate_data_contract(data)

        self.assertTrue(any("真正的转折" in error for error in errors), errors)
        self.assertTrue(any("两类判断" in error for error in errors), errors)

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

    def test_student_persona_must_remain_backstage(self):
        data = valid_data()
        data["slides"][1]["visible"] = "学生角色林晓今天要完成三问"

        errors = validate_data_contract(data)

        self.assertTrue(any("S02" in error and "林晓" in error for error in errors), errors)

    def test_every_slide_requires_performable_notes(self):
        data = valid_data()
        data["slides"][2]["notes"] = "教师讲解第二问。"

        errors = validate_data_contract(data)

        self.assertTrue(any("S03" in error and "逐字稿" in error for error in errors), errors)

    def test_q3_difficulty_line_must_include_era_conditions(self):
        data = valid_data()
        data["causal_lines"]["difficulty"] = ["初期信息有限", "情感和生活投入", "支持缺失", "停止更加困难"]

        errors = validate_data_contract(data)

        self.assertTrue(any("时代条件" in error for error in errors), errors)

    def test_q1_sorting_prompt_cannot_reveal_correct_order(self):
        data = valid_data()
        data["slides"].append({
            "id": "S11", "module": "M4", "phase": "question", "kind": "q1_activity",
            "items": ["相识议婚", "等待成婚", "迁嫁食贫", "长期劳作", "失信粗暴", "家人不解", "核验誓言", "停止判断"],
            "visible": "排序", "notes": valid_notes(11),
        })

        errors = validate_data_contract(data)

        self.assertTrue(any("排序问题页" in error and "泄漏" in error for error in errors), errors)

    def test_result_line_requires_prior_build_page(self):
        data = valid_data()
        data["slides"].append({
            "id": "S11", "module": "M5", "phase": "return", "kind": "responsibility_line",
            "visible": "责任线", "notes": valid_notes(11),
        })

        errors = validate_data_contract(data)

        self.assertTrue(any("责任线" in error and "问题态" in error for error in errors), errors)

    def test_synthesis_prompt_timing_and_script_must_match_task(self):
        data = valid_data()
        data["slides"].append({
            "id": "S11", "module": "M5", "phase": "question", "kind": "responsibility_build",
            "minutes": 2, "visible": "先画责任线", "notes": valid_notes(11),
        })

        errors = validate_data_contract(data)

        self.assertTrue(any("标称2分钟" in error for error in errors), errors)
        self.assertTrue(any("专用脚本" in error and "责任" in error for error in errors), errors)


class MarkdownContractTests(unittest.TestCase):
    def valid_texts(self) -> dict[str, str]:
        all_lines = "\n".join(EXPECTED_LINES)
        questions = "\n".join(THREE_QUESTIONS)
        return {
            "lesson": f"V5 5.3-literary-participation\n30组诗句\n12个意义句群\n274分钟\n接力讲述\n生活镜头\n婚姻圆桌\n{questions}\n{all_lines}",
            "worksheet": f"把她的一生讲出来\n我认为最重要的转折是\n让诗句重新长成日子\n先把责任说清\n把一句提醒留给后来人\n{questions}",
            "script": "三问重新回来了。下一页，先把第一问读完整\n" + "\n".join(valid_notes(page) for page in range(1, 11)),
            "audit": "桌面模拟，不是真实课堂数据\n学生角色：林晓\n接收到了什么信息\n参加了什么活动\n可能怎样思考\n形成了什么收获\n可观察证据\n接力讲述\n生活镜头\n婚姻圆桌",
        }

    def test_valid_markdown_set_passes(self):
        self.assertEqual([], validate_markdown_contract(self.valid_texts()))

    def test_markdown_missing_marriage_roundtable_is_reported(self):
        texts = self.valid_texts()
        texts["worksheet"] = texts["worksheet"].replace("把一句提醒留给后来人", "标准答案")

        errors = validate_markdown_contract(texts)

        self.assertTrue(any("worksheet" in error and "把一句提醒留给后来人" in error for error in errors), errors)


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


class GeneratedPackageIntegrationTests(unittest.TestCase):
    def test_generated_data_and_markdown_satisfy_v5_contracts(self):
        self.assertTrue(SNAPSHOT.exists(), SNAPSHOT)
        data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        self.assertEqual([], validate_data_contract(data))

        texts = {}
        for label, path in MARKDOWN_FILES.items():
            self.assertTrue(path.exists(), path)
            texts[label] = path.read_text(encoding="utf-8")
        self.assertEqual([], validate_markdown_contract(texts))

    def test_worksheet_and_p89_transition_keep_the_repaired_wording(self):
        worksheet = MARKDOWN_FILES["worksheet"].read_text(encoding="utf-8")
        script = MARKDOWN_FILES["script"].read_text(encoding="utf-8")

        self.assertIn("我认为最重要的转折是", worksheet)
        self.assertNotIn("真正改变她命运", worksheet)
        self.assertNotIn("她转身时面对的阻力", worksheet)
        self.assertIn("三问重新回来了。下一页，先把第一问读完整", script)

    def test_generated_slide_count_stays_within_approved_range(self):
        self.assertTrue(SNAPSHOT.exists(), SNAPSHOT)
        data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["slides"]), 120)
        self.assertLessEqual(len(data["slides"]), 130)

    def test_generated_master_and_module_pptx_satisfy_note_contracts(self):
        self.assertTrue(SNAPSHOT.exists(), SNAPSHOT)
        data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))

        self.assertTrue(PPT_MASTER.exists(), PPT_MASTER)
        master_first_pages = {
            index for index, slide in enumerate(data["slides"], 1)
            if slide["phase"] == "opening" or slide["kind"] == "first_full_read"
        }
        self.assertEqual(
            [],
            validate_pptx_contract(PPT_MASTER, len(data["slides"]), master_first_pages),
        )

        for module_id, path in MODULE_PPTX.items():
            self.assertTrue(path.exists(), path)
            module_slides = [slide for slide in data["slides"] if slide["module"] == module_id]
            local_first_pages = {
                index for index, slide in enumerate(module_slides, 1)
                if slide["phase"] == "opening" or slide["kind"] == "first_full_read"
            }
            self.assertEqual(
                [],
                validate_pptx_contract(path, len(module_slides), local_first_pages),
                module_id,
            )


if __name__ == "__main__":
    unittest.main()
