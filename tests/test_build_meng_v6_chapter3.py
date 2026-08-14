from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "meng_v6" / "content" / "chapter_3.js"
METHODS = ROOT / "scripts" / "meng_v6" / "methods.js"
NOTES = ROOT / "scripts" / "meng_v6" / "chapter3_notes.js"
BUILDER = ROOT / "scripts" / "build_meng_v6_chapter3_markdown.js"
PAGE_IDS = [f"N{number:03d}" for number in range(31, 39)]


def node_json(path: Path) -> dict:
    result = subprocess.run(
        ["node", str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return json.loads(result.stdout)


class MengV6Chapter3ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = node_json(SOURCE)
        cls.methods = node_json(METHODS)["methods"]
        cls.pages = cls.payload["pages"]

    def test_eight_pages_form_one_ordered_path(self):
        self.assertEqual(PAGE_IDS, [page["page_id"] for page in self.pages])
        self.assertEqual("E_CH3_WHOLE_READ", self.pages[0]["event_id"])
        self.assertEqual("E_CH3_KNOWLEDGE_SHELF", self.pages[-1]["event_id"])
        self.assertEqual(
            [page["event_id"] for page in self.pages[1:]],
            [page["next_event_id"] for page in self.pages[:-1]],
        )

    def test_every_third_chapter_line_is_taught_with_textbook_glosses(self):
        expected = {
            "L011": {"沃若": "润泽的样子"},
            "L012": {"于嗟": "感叹词，读xū jiē", "无": "同‘毋’，不要", "鸠": "斑鸠", "桑葚": "桑树的果实；旧说斑鸠吃多了会昏醉"},
            "L013": {"士": "这里指未婚男子", "耽": "沉溺、沉醉"},
            "L014": {"说": "读tuō，同‘脱’，摆脱、脱身", "犹可": "尚且可以"},
            "L015": {"说": "读tuō，同‘脱’，摆脱、脱身", "不可": "不能"},
        }
        taught = {}
        for page in self.pages:
            for line_id, glosses in page.get("line_glosses", {}).items():
                self.assertNotIn(line_id, taught)
                taught[line_id] = glosses
        self.assertEqual(expected, taught)

    def test_every_page_has_closed_function_contract_and_existing_method(self):
        method_ids = {method["method_id"] for method in self.methods}
        for page in self.pages:
            for field in (
                "unique_function", "student_action", "first_glance_contract", "observable_change",
                "artifact_location", "listener_task", "feedback_revision", "deletion_loss",
                "method_id", "teacher_script", "primary_visual_duty",
            ):
                self.assertTrue(page[field], f"{page['page_id']}:{field}")
            self.assertIn(page["method_id"], method_ids)
            self.assertGreaterEqual(len(page["teacher_script"]), 100, page["page_id"])

    def test_mulberry_is_hypothesis_not_fixed_password(self):
        mulberry = next(page for page in self.pages if page["page_id"] == "N032")
        combined = "\n".join((mulberry["visible"], mulberry["teacher_script"], mulberry["feedback_revision"]))
        self.assertIn("两种假设", combined)
        self.assertIn("第四章", combined)
        self.assertIn("可能", combined)
        for forbidden in ("桑叶就是青春", "唯一象征", "固定答案"):
            self.assertNotIn(forbidden, combined)

    def test_bixing_is_named_after_student_comparison(self):
        comparison = next(page for page in self.pages if page["page_id"] == "N035")
        script = comparison["teacher_script"]
        self.assertIn("第一组读A", script)
        self.assertIn("我们再给这种经验命名", script)
        self.assertLess(script.index("第一组读A"), script.index("我们再给这种经验命名"))
        self.assertNotIn("比兴", comparison["visible"])
        self.assertIn("删改句更直接", script)
        self.assertNotIn("A多带来的", comparison["visible"])

    def test_student_visible_text_hides_backstage_control_language(self):
        visible = "\n".join(page["visible"] for page in self.pages)
        for backstage_phrase in (
            "不解释比兴",
            "先留下三个初读落点",
            "先不急着写‘象征什么’",
            "只说诗中明写",
            "原因：后文待证",
            "先比较，再给经验命名",
            "不用活动名称",
            "听者找遗漏",
            "只给仍不稳",
        ):
            self.assertNotIn(backstage_phrase, visible)

    def test_n031_question_state_does_not_preannounce_its_discovery(self):
        opening = next(page for page in self.pages if page["page_id"] == "N031")
        frontstage = "\n".join((opening["title"], opening["visible"]))
        for leaked in ("声音为什么忽然停下", "换镜", "呼告对象", "一片桑叶先进入眼帘", "两声叹息"):
            self.assertNotIn(leaked, frontstage)
        before_student_generation = opening["teacher_script"].split("读后只写", 1)[0]
        for leaked in ("没有继续往前讲", "桑叶", "两声叹息"):
            self.assertNotIn(leaked, before_student_generation)

    def test_n033_question_state_does_not_name_the_relation(self):
        echo = next(page for page in self.pages if page["page_id"] == "N033")
        self.assertNotIn("由物及人", echo["visible"])
        self.assertIn("怎样接过去", echo["visible"])

    def test_n037_reconstructs_in_story_language(self):
        close = next(page for page in self.pages if page["page_id"] == "N037")
        for analysis_phrase in ("由物及人", "处境差异", "叙事为何停下"):
            self.assertNotIn(analysis_phrase, close["visible"])
        for story_prompt in ("眼前先出现什么", "两声劝告", "谁更难脱身"):
            self.assertIn(story_prompt, close["visible"])

    def test_n038_calls_back_specific_student_artifacts(self):
        shelf = next(page for page in self.pages if page["page_id"] == "N038")
        for artifact in ("桑叶假设", "两声记录", "脱身对照", "删句比较", "故事旁白"):
            self.assertIn(artifact, shelf["visible"])

    def test_exit_inequality_does_not_blame_the_woman_or_invent_cause(self):
        contrast = next(page for page in self.pages if page["page_id"] == "N034")
        combined = "\n".join((contrast["visible"], contrast["teacher_script"], contrast["feedback_revision"]))
        self.assertIn("后文待证", combined)
        self.assertIn("不能分担男子", combined)
        for forbidden in ("女子天生", "因为她沉溺所以男子", "她活该"):
            self.assertNotIn(forbidden, combined)

    def test_story_rail_and_activity_masking_check_are_real(self):
        opening = next(page for page in self.pages if page["page_id"] == "N031")
        retrieval = next(page for page in self.pages if page["page_id"] == "N036")
        close = next(page for page in self.pages if page["page_id"] == "N037")
        self.assertIn("故事走到这里", opening["visible"])
        self.assertIn("故事旁白", retrieval["visible"])
        self.assertIn("人物和处境", retrieval["teacher_script"])
        self.assertIn("初见议婚 → 等待迁嫁 →", close["visible"])
        self.assertEqual("E_CH3_VOICE_STAIRCASE", opening["deferred_use"]["target_event_id"])

    def test_retrieval_does_not_leak_finished_sequence(self):
        retrieval = next(page for page in self.pages if page["page_id"] == "N036")
        self.assertEqual("open_question", retrieval["answer_state"])
        self.assertIn("乱序", retrieval["visible"])
        self.assertNotIn("桑叶沃若 → 劝斑鸠勿食 → 劝女子勿耽 → 比较脱身处境", retrieval["visible"])
        self.assertIn("不报完整顺序", retrieval["teacher_script"])

    def test_knowledge_summary_is_last_and_reuses_student_records(self):
        shelf = self.pages[-1]
        self.assertEqual("N038", shelf["page_id"])
        self.assertEqual("teacher_consolidated", shelf["answer_state"])
        self.assertIn("不整页抄写", shelf["teacher_script"])
        self.assertIn("自己的学习单", shelf["visible"])

    def test_frontstage_avoids_ai_and_design_jargon(self):
        frontstage = "\n".join(page["visible"] for page in self.pages)
        for token in (
            "闭环", "抓手", "赋能", "链路", "颗粒度", "接收审计", "学生角色",
            "页面功能", "理解链", "知识碎片", "恋爱脑", "情绪价值", "P0", "P1", "P2",
        ):
            self.assertNotIn(token, frontstage)

    def test_notes_timeboxes_equal_declared_minutes(self):
        script = f"""
const chapter = require('./scripts/meng_v6/content/chapter_3.js');
const notes = require('./scripts/meng_v6/chapter3_notes.js');
const result = chapter.pages.map((page) => ({{
  id: page.page_id,
  expected: page.minutes * 60,
  actual: notes[page.page_id].timeboxes.reduce((s, item) => s + item[1], 0),
}}));
process.stdout.write(JSON.stringify(result));
"""
        result = subprocess.run(["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=True)
        for item in json.loads(result.stdout):
            self.assertEqual(item["expected"], item["actual"], item["id"])

    def test_markdown_builder_compiles_without_writing_in_test(self):
        script = f"""
const builder = require({json.dumps(str(BUILDER))});
const pages = builder.compilePages();
const lesson = builder.renderLesson(pages, 'test-sha');
const worksheet = builder.renderWorksheet();
const rehearsal = builder.renderScript(pages, 'test-sha');
process.stdout.write(JSON.stringify({{
  pageIds: pages.map(p => p.page_id),
  minutes: pages.reduce((s, p) => s + p.minutes, 0),
  hasStoryRail: worksheet.includes('故事轨道第三格'),
  hasAllScripts: pages.every(p => rehearsal.includes('V6_PAGE:' + p.page_id)),
  hasDeletionLoss: lesson.includes('删除损失'),
}}));
"""
        result = subprocess.run(["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=True)
        payload = json.loads(result.stdout)
        self.assertEqual(PAGE_IDS, payload["pageIds"])
        self.assertEqual(38, payload["minutes"])
        self.assertTrue(payload["hasStoryRail"])
        self.assertTrue(payload["hasAllScripts"])
        self.assertTrue(payload["hasDeletionLoss"])


if __name__ == "__main__":
    unittest.main()
