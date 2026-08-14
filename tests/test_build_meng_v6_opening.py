from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUILD = PROJECT_ROOT / "scripts" / "build_meng_v6_opening.py"
OUTPUT = PROJECT_ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v6_stage" / "opening" / "opening_audit.json"


def build() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(BUILD), "--allow-pending-review"], cwd=PROJECT_ROOT,
        text=True, capture_output=True, check=False,
    )


class MengV6OpeningAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = build()
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.document = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_old_s001_s016_all_have_completed_self_diagnosis_without_seal(self):
        legacy = self.document["legacy_initial_audit"][:16]
        self.assertEqual([f"S{number:03d}" for number in range(1, 17)], [page["page_id"] for page in legacy])
        self.assertTrue(all(page["audit_scope"] in {"learning_page", "event_carrier"} for page in legacy))
        self.assertNotIn("pending", {gate["gate_status"] for page in legacy for gate in page["gates"]})
        self.assertTrue(all(page["review_status"]["self_review"]["status"] == "pass" for page in legacy))
        self.assertTrue(all(page["review_status"]["student_reception"]["status"] == "pending" for page in legacy))
        self.assertTrue(all(page["review_status"]["visual"]["status"] == "pending" for page in legacy))
        self.assertEqual([], self.document["initial_audit_seals"])
        self.assertEqual([], self.document["legacy_disposition_closure"])

    def test_legacy_diagnosis_records_known_opening_failures_and_does_not_rewrite_them(self):
        legacy = {page["page_id"]: page for page in self.document["legacy_initial_audit"][:16]}
        failures = {
            page_id: {gate["failure_code"] for gate in page["gates"] if gate["gate_status"] == "fail"}
            for page_id, page in legacy.items()
        }
        self.assertIn("G1_PREREQ_MISSING", failures["S004"])
        self.assertIn("G4_CHANGE_UNOBSERVABLE", failures["S005"])
        self.assertIn("G1_PREREQ_MISSING", failures["S007"])
        self.assertIn("G2_FUNCTION_DUPLICATE", failures["S008"])
        self.assertIn("G2_ROLE_MULTIPLE", failures["S009"])
        self.assertIn("G5_OUTPUT_ORPHAN", failures["S012"])
        self.assertIn("G3_COVERAGE_FALSE", failures["S015"])
        self.assertIn("G6_MERGEABLE", failures["S016"])
        self.assertEqual("P1", next(item for item in self.document["defect_registry"] if item["defect_id"] == "A-S004-G1")["severity"])
        self.assertEqual("P2", next(item for item in self.document["defect_registry"] if item["defect_id"] == "A-S005-G4")["severity"])

    def test_current_opening_is_broad_recall_then_text_not_three_prefilled_examples(self):
        pages = self.document["current_release_audit"]["pages"]
        self.assertEqual(
            ["N002", "N003", "N004", "N005", "N001", "N007", "N008", "N009", "N010", "N011", "N012"],
            [page["page_id"] for page in pages],
        )
        visible = "\n".join(str(page.get("student_visible_text", "")) for page in pages)
        self.assertIn("尽量多写，至少一篇", visible)
        self.assertIn("轮到我｜15—20秒", visible)
        self.assertIn("全组留下｜两张不同的", visible)
        self.assertIn("每组先贴两张卡", visible)
        self.assertIn("卡墙还没有", visible)
        self.assertIn("卡墙已有相同内容", visible)
        question_page = next(page for page in pages if page["page_id"] == "N007")
        self.assertIn("今天再读一个更早的故事", question_page["previous_relation"])
        self.assertNotIn("今天再读一个更早的故事", visible)
        self.assertNotIn("《静女》｜相遇与等待", visible)
        self.assertNotIn("幸福或困境，取决于什么", visible)
        self.assertNotIn("相遇的欣悦，需要真实了解", visible)
        self.assertNotIn("婚姻的选择，需要尊重与行动", visible)

    def test_n005_theme_map_is_student_authored_and_teacher_cannot_supply_fixed_categories(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        n005 = pages["N005"]
        visible = n005["student_visible_text"]
        teacher = n005["channel_split"]["teacher"]
        self.assertIn("每人先连一组", visible)
        self.assertIn("三位同学上台", visible)
        self.assertIn("临时命名", visible)
        self.assertIn("保留／改名／移回", visible)
        self.assertIn("只复述现场已经出现", teacher)
        self.assertIn("如果现场只有两条", teacher)
        for prewritten_category in ("相遇的欢喜", "等待、错过、阻隔、相守与破裂"):
            self.assertNotIn(prewritten_category, teacher)
        self.assertIn("三名学生", n005["student_action"]["action"])
        self.assertIn("卡号", n005["artifact_location"])

    def test_every_opening_page_exposes_the_non_negotiable_value_chain_contract(self):
        for page in self.document["current_release_audit"]["pages"]:
            self.assertTrue(page["previous_artifact_input"], page["page_id"])
            self.assertTrue(page["unique_transformation"], page["page_id"])
            self.assertTrue(page["individual_minimum_action"], page["page_id"])
            self.assertTrue(page["minimum_acceptance_criterion"], page["page_id"])
            self.assertTrue(page["bounded_feedback"], page["page_id"])
            self.assertTrue(page["revision_evidence"], page["page_id"])
            self.assertTrue(page["named_consumer"], page["page_id"])
            self.assertIn(page["consumer_status"], {"implemented", "declared"}, page["page_id"])
            self.assertTrue(page["participation_denominator"], page["page_id"])
            self.assertTrue(page["artifact_authorship"], page["page_id"])
            self.assertIn("seen", page["student_reception_contract"])
            self.assertIn("heard", page["student_reception_contract"])
            self.assertIn("action", page["student_reception_contract"])
            self.assertIn("artifact", page["student_reception_contract"])
            self.assertIn("next_use", page["student_reception_contract"])

    def test_deferred_consumers_are_declared_not_misrepresented_as_verified(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        for page_id in ("N005", "N010", "N012"):
            self.assertEqual("declared", pages[page_id]["consumer_status"])
            self.assertEqual("provisional", pages[page_id]["release_status"])
        self.assertEqual("implemented", pages["N003"]["consumer_status"])

    def test_participation_events_have_all_student_entry_listener_work_and_saved_reuse(self):
        events = {event["event_id"]: event for event in self.document["current_release_audit"]["events"]}
        for event_id in ("E_RECALL_PERSONAL", "E_RECALL_GROUP", "E_RECALL_CLASS", "E_THEME_MAP", "E_FIRST_LISTEN", "E_FIRST_MARK"):
            event = events[event_id]
            self.assertEqual("learning_event", event["audit_scope"])
            self.assertTrue(event["participation_contract"]["all_students_have_entry"])
            self.assertTrue(event["participation_contract"]["listener_task"])
            self.assertTrue(event["artifacts"])
            self.assertTrue(event["artifact_locations"])
            self.assertTrue(event["next_uses"])
        self.assertIn("每人", " ".join(events["E_RECALL_GROUP"]["actions"]))
        self.assertIn("共6分钟", " ".join(events["E_RECALL_CLASS"]["actions"]))

    def test_visual_review_failures_were_removed_not_downgraded(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        self.assertNotIn("N006", pages)
        self.assertNotIn("提示条", pages["N002"]["student_visible_text"])
        self.assertIn("卡墙还没有", pages["N004"]["student_visible_text"])
        self.assertIn("卡墙已有相同内容", pages["N004"]["student_visible_text"])
        self.assertIn("6分钟", pages["N004"]["student_visible_text"])
        self.assertIn("三位同学上台｜移动卡片", pages["N005"]["student_visible_text"])
        self.assertIn("原提议者当场保留／改名／移回", pages["N005"]["student_visible_text"])
        self.assertIn("原提议者号", pages["N003"]["student_visible_text"])
        self.assertIn("原提议者书写或签认", pages["N003"]["supporting_move"])
        self.assertNotIn("教师据此", pages["N005"]["student_visible_text"])
        self.assertEqual("信息路标", pages["N011"]["primary_visual_duty"])
        self.assertIn("第一章开头的无斜线原句", pages["N012"]["student_visible_text"])
        self.assertIn("听者问", pages["N012"]["student_visible_text"])
        self.assertIn("读者带着完整动作再读", pages["N012"]["student_visible_text"])
        self.assertEqual(7, pages["N005"]["time_value"]["minutes"])
        self.assertNotIn("赋、比、兴", pages["N012"]["student_visible_text"])

    def test_cover_borrows_event_change_and_transition_is_actually_heard(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        events = {event["event_id"]: event for event in self.document["current_release_audit"]["events"]}
        cover = pages["N001"]
        self.assertEqual("event_carrier", cover["audit_scope"])
        self.assertEqual("E_TITLE", cover["owner_event_id"])
        self.assertIn("N001", events["E_TITLE"]["carrier_ids"])
        cover_gates = {gate["gate_id"]: gate for gate in cover["gates"]}
        self.assertEqual("na", cover_gates["G4"]["gate_status"])
        self.assertEqual("na", cover_gates["G5"]["gate_status"])
        title_script = pages["N001"]["channel_split"]["teacher"]
        question_script = pages["N007"]["channel_split"]["teacher"]
        self.assertIn("更早的讲述者", title_script)
        self.assertIn("《诗经·卫风》", title_script)
        self.assertIn("不要抢答", question_script)

    def test_event_g5_points_to_real_target_input_or_stays_deferred(self):
        events = {event["event_id"]: event for event in self.document["current_release_audit"]["events"]}
        for event_id in (
            "E_TITLE", "E_RECALL_PERSONAL", "E_RECALL_GROUP", "E_RECALL_CLASS",
            "E_QUESTIONS", "E_FIRST_LISTEN", "E_CONTEXT",
        ):
            event = events[event_id]
            self.assertEqual("pass", event["gate_5"]["gate_status"])
            target_id = event["next_use_contracts"][0]["target_event_id"]
            self.assertIn(f"{target_id}#inputs", event["gate_5"]["evidence_refs"])
        for event_id, target_id in (
            ("E_THEME_MAP", "E_MARRIAGE_ROUND_TABLE"),
            ("E_FIRST_MARK", "E_FULL_TEXT_RETURN"),
            ("E_RHYTHM", "E_CHAPTER1_START"),
        ):
            event = events[event_id]
            self.assertEqual("deferred", event["gate_5"]["gate_status"])
            self.assertEqual("provisional", event["release_status"])
            self.assertEqual(target_id, event["gate_5"]["target_event_id"])
        full_return = events["E_FULL_TEXT_RETURN"]
        self.assertEqual("E_THREE_QUESTION_RETURN", full_return["next_use_contracts"][0]["target_event_id"])
        three_return = events["E_THREE_QUESTION_RETURN"]
        self.assertTrue(any(item.get("source_node_id") == "N007" for item in three_return["inputs"]))
        round_table = events["E_MARRIAGE_ROUND_TABLE"]
        self.assertTrue(any(item.get("source_node_id") == "N005" for item in round_table["inputs"]))
        self.assertTrue(any(item.get("source_node_id") == "E_THREE_QUESTION_RETURN" for item in round_table["inputs"]))

    def test_student_facing_or_heard_channels_include_honest_branch_and_peer_feedback(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        self.assertIn("1 → 2 → 3 → 4", pages["N003"]["student_visible_text"])
        self.assertIn("听见新内容就勾", pages["N003"]["student_visible_text"])
        self.assertIn("暂无新增，也从作品谱选两项", pages["N003"]["student_visible_text"])
        self.assertIn("尚未找到", pages["N010"]["student_visible_text"])
        self.assertIn("谁在回望什么", pages["N011"]["student_visible_text"])
        self.assertIn("谁做什么", pages["N012"]["student_visible_text"])
        self.assertIn("不可说也", pages["N008"]["channel_split"]["teacher"])
        self.assertIn("不齐读", pages["N008"]["student_visible_text"])
        self.assertIn("用笔在教材原句旁留一点", pages["N008"]["student_visible_text"])
        self.assertIn("第一章", pages["N008"]["student_visible_text"])
        self.assertIn("第六章", pages["N009"]["student_visible_text"])
        self.assertIn("看教材", pages["N012"]["student_visible_text"])
        self.assertIn("第一章开头", pages["N012"]["student_visible_text"])

    def test_n004_gives_listeners_an_equal_honest_route_when_nothing_is_new(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        events = {event["event_id"]: event for event in self.document["current_release_audit"]["events"]}
        visible = pages["N004"]["student_visible_text"]
        teacher = pages["N004"]["channel_split"]["teacher"]
        listener = pages["N004"]["listener_task"]["task"]
        self.assertIn("有新增", visible)
        self.assertIn("暂无新增", visible)
        self.assertIn("核对一张重复卡", visible)
        self.assertIn("暂无新增", listener)
        self.assertIn("核对一张重复卡", teacher)
        event_listener = events["E_RECALL_CLASS"]["participation_contract"]["listener_task"]
        self.assertIn("暂无新增", event_listener)
        self.assertIn("核对", event_listener)

    def test_title_is_revealed_only_after_the_live_theme_map(self):
        events = {event["event_id"]: event for event in self.document["current_release_audit"]["events"]}
        title_use = events["E_TITLE"]["next_use_contracts"][0]
        self.assertEqual("E_QUESTIONS", title_use["target_event_id"])
        self.assertIn("E_QUESTIONS#inputs", events["E_TITLE"]["gate_5"]["evidence_refs"])
        pages = self.document["current_release_audit"]["pages"]
        title_index = next(index for index, page in enumerate(pages) if page["page_id"] == "N001")
        self.assertEqual(4, title_index)
        for page in pages[:title_index]:
            self.assertNotIn("《氓》", page["student_visible_text"])
            self.assertNotIn("《氓》", page["channel_split"]["teacher"])

    def test_listening_has_two_carriers_one_event_and_word_dump_is_removed(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        event = next(item for item in self.document["current_release_audit"]["events"] if item["event_id"] == "E_FIRST_LISTEN")
        self.assertEqual(2, len(event["carrier_ids"]))
        for page_id in event["carrier_ids"]:
            self.assertEqual("event_carrier", pages[page_id]["audit_scope"])
            self.assertEqual("E_FIRST_LISTEN", pages[page_id]["owner_event_id"])
            gates = {gate["gate_id"]: gate for gate in pages[page_id]["gates"]}
            self.assertEqual("na", gates["G4"]["gate_status"])
            self.assertEqual("na", gates["G5"]["gate_status"])
        visible = "\n".join(str(page.get("student_visible_text", "")) for page in pages.values())
        self.assertNotIn("愆 qiān｜将 qiāng｜垝垣", visible)
        self.assertNotIn("赋、比、兴，等诗句出现后再命名", visible)
        self.assertIn("不集中倾倒十词", pages["N012"]["framework_cost"])

    def test_stage_validator_accepts_opening_slice_without_pretending_future_completion(self):
        result = subprocess.run(
            [
                "python", "scripts/validate_meng_v6_page_audit.py", "--mode", "stage",
                "--input", str(OUTPUT),
            ],
            cwd=PROJECT_ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("AUDIT_OK", result.stdout)
        self.assertEqual("desktop_design_scaffold_only", self.document["claim_boundary"])
        self.assertEqual("structure_in_progress", self.document["document_status"])
        self.assertTrue(any(
            gate["gate_status"] == "deferred"
            for page in self.document["current_release_audit"]["pages"]
            for gate in page["gates"]
        ))

    def test_current_review_receipt_is_applied_only_to_the_matching_slice(self):
        review = self.document["independent_structure_review"]
        if review is None:
            for collection in ("pages", "events"):
                for item in self.document["current_release_audit"][collection]:
                    review_status = item["review_status"]
                    self.assertEqual("pending", review_status["consensus"])
                    self.assertEqual("pending", review_status["student_reception"]["status"])
                    self.assertEqual("pending", review_status["visual"]["status"])
            return
        self.assertEqual("pass", review["status"])
        self.assertEqual(0, review["p0"] + review["p1"] + review["p2"])
        for collection in ("pages", "events"):
            for item in self.document["current_release_audit"][collection]:
                review_status = item["review_status"]
                self.assertEqual("passed", review_status["consensus"])
                self.assertEqual("pass", review_status["student_reception"]["status"])
                self.assertEqual("pass", review_status["visual"]["status"])


if __name__ == "__main__":
    unittest.main()
