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
        ["python", str(BUILD)], cwd=PROJECT_ROOT, text=True, capture_output=True, check=False,
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
        visible = "\n".join(str(page.get("student_visible_text", "")) for page in pages)
        self.assertIn("写下1—3篇", visible)
        self.assertIn("每人15—20秒", visible)
        self.assertIn("贡献一篇尚未出现的作品", visible)
        question_page = next(page for page in pages if page["page_id"] == "N007")
        self.assertIn("今天再读一个更早的故事", question_page["previous_relation"])
        self.assertNotIn("今天再读一个更早的故事", visible)
        self.assertNotIn("《静女》｜相遇与等待", visible)
        self.assertNotIn("幸福或困境，取决于什么", visible)
        self.assertNotIn("相遇的欣悦，需要真实了解", visible)
        self.assertNotIn("婚姻的选择，需要尊重与行动", visible)

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
        self.assertIn("最多4分钟", " ".join(events["E_RECALL_CLASS"]["actions"]))

    def test_visual_review_failures_were_removed_not_downgraded(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        self.assertNotIn("N006", pages)
        self.assertIn("只写篇名的提示条", pages["N002"]["student_visible_text"])
        self.assertIn("先贴一张卡", pages["N004"]["student_visible_text"])
        self.assertIn("最多4分钟", pages["N004"]["student_visible_text"])
        self.assertIn("移动一张卡", pages["N005"]["student_visible_text"])
        self.assertEqual(4, pages["N005"]["time_value"]["minutes"])
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
        teacher_script = pages["N007"]["channel_split"]["teacher"]
        self.assertIn("今天再读一个更早的故事", teacher_script)
        self.assertIn("一位女子回望婚后的日子", teacher_script)
        self.assertIn("先别急着回答", teacher_script)

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

    def test_student_facing_or_heard_channels_include_honest_branch_and_peer_feedback(self):
        pages = {page["page_id"]: page for page in self.document["current_release_audit"]["pages"]}
        self.assertIn("听的人各勾一项", pages["N003"]["student_visible_text"])
        self.assertIn("尚未找到", pages["N010"]["channel_split"]["teacher"])
        self.assertIn("谁在回望什么", pages["N011"]["student_visible_text"])
        self.assertIn("谁做什么", pages["N012"]["student_visible_text"])

    def test_title_is_reused_when_the_class_returns_from_prior_works_to_meng(self):
        events = {event["event_id"]: event for event in self.document["current_release_audit"]["events"]}
        title_use = events["E_TITLE"]["next_use_contracts"][0]
        self.assertEqual("E_QUESTIONS", title_use["target_event_id"])
        self.assertIn("E_QUESTIONS#inputs", events["E_TITLE"]["gate_5"]["evidence_refs"])

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

    def test_current_slice_is_bound_to_two_independent_zero_defect_reviews(self):
        receipt = self.document["independent_structure_review"]
        self.assertEqual("pass", receipt["status"])
        self.assertEqual((0, 0, 0), (receipt["p0"], receipt["p1"], receipt["p2"]))
        for collection in ("pages", "events"):
            for item in self.document["current_release_audit"][collection]:
                review = item["review_status"]
                self.assertEqual("passed", review["consensus"])
                self.assertEqual("student_reception_qa", review["student_reception"]["reviewer"])
                self.assertEqual("ppt_visual_qa", review["visual"]["reviewer"])


if __name__ == "__main__":
    unittest.main()
