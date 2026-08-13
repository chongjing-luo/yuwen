from __future__ import annotations

import copy
import hashlib
import json
import unittest

from scripts.build_meng_v6_audit import (
    BATCHES,
    JSON_OUTPUT,
    batch_documents,
    build_stage_document,
    json_text,
    page_skeletons,
    render_markdown,
    serialized_sha256,
)
from scripts.validate_meng_v6_page_audit import validate_audit_document


def snapshot() -> dict:
    slides = []
    for number in range(1, 128):
        slides.append({
            "id": f"S{number:03d}",
            "module": "MASTER" if number == 1 else f"M{min(5, (number - 2) // 26 + 1)}",
            "phase": "teacher" if number == 1 else "chapter",
            "kind": "teacher_index" if number == 1 else "line",
            "minutes": 0 if number == 1 else 2,
            "title": f"旧页{number}",
            "visible": f"旧页{number}的学生可见文字",
            "experience": "旧模板体验字段",
            "thought": "旧模板思考字段",
            "learning": "旧模板学习字段",
        })
    return {"version": "5.3-literary-participation", "generated_at": "2026-08-11", "slides": slides}


class MengV6AuditSkeletonTests(unittest.TestCase):
    def fixture_document(self, pages: list[dict]) -> dict:
        return build_stage_document(
            pages,
            "a" * 64,
            "b" * 64,
            document_status="structure_in_progress",
        )

    def test_batch_ranges_cover_exactly_s001_to_s127(self):
        covered = [number for batch in BATCHES for number in range(batch.start, batch.end + 1)]
        self.assertEqual(list(range(1, 128)), covered)

    def test_page_skeleton_imports_only_stable_facts_and_pending_audit_state(self):
        pages = page_skeletons(snapshot(), "a" * 64)
        self.assertEqual(127, len(pages))
        self.assertEqual([f"S{number:03d}" for number in range(1, 128)], [page["page_id"] for page in pages])
        self.assertFalse(pages[0]["legacy_student_visible"])
        self.assertTrue(pages[1]["legacy_student_visible"])
        self.assertEqual({"pending"}, {
            gate["gate_status"] for page in pages for gate in page["gates"]
        })
        self.assertEqual({"pending"}, {page["audit_scope"] for page in pages})
        self.assertEqual({"pending"}, {
            page["review_status"][role]["status"]
            for page in pages
            for role in ("self_review", "student_reception", "visual")
        })
        serialized = repr(pages)
        self.assertNotIn("experience", serialized)
        self.assertNotIn("thought", serialized)
        self.assertNotIn("learning\'", serialized)
        self.assertNotIn("decision", serialized)

    def test_missing_duplicate_out_of_order_or_prefilled_source_is_rejected(self):
        bad = snapshot()
        bad["slides"].pop()
        with self.assertRaisesRegex(ValueError, "S001-S127"):
            page_skeletons(bad, "a" * 64)

        bad = snapshot()
        bad["slides"][1]["id"] = "S001"
        with self.assertRaisesRegex(ValueError, "S001-S127"):
            page_skeletons(bad, "a" * 64)

        bad = snapshot()
        bad["slides"][0]["decision"] = "保留"
        with self.assertRaisesRegex(ValueError, "prefilled audit conclusion"):
            page_skeletons(bad, "a" * 64)

    def test_empty_current_v6_structure_is_valid_only_in_stage(self):
        document = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(document["pages"], document["legacy_initial_audit"])
        self.assertEqual([], validate_audit_document(document, mode="stage"))
        freeze_codes = {item["code"] for item in validate_audit_document(document, mode="freeze")}
        self.assertIn("CURRENT_TERMINAL_INVALID", freeze_codes)

    def test_top_level_pages_is_a_required_exact_derived_view(self):
        pages = page_skeletons(snapshot(), "a" * 64)
        document = self.fixture_document(pages)
        document["pages"] = document["pages"][:-1]
        codes = {item["code"] for item in validate_audit_document(document, mode="stage")}
        self.assertIn("LEGACY_PAGE_VIEW_MISMATCH", codes)

        document = self.fixture_document(pages)
        document["pages"] = copy.deepcopy(document["pages"])
        document["pages"][0]["source_title"] = "drifted title"
        codes = {item["code"] for item in validate_audit_document(document, mode="stage")}
        self.assertIn("LEGACY_PAGE_VIEW_MISMATCH", codes)

        document = self.fixture_document(pages)
        del document["pages"]
        codes = {item["code"] for item in validate_audit_document(document, mode="stage")}
        self.assertIn("LEGACY_PAGE_VIEW_MISMATCH", codes)

    def test_stage_validator_reloads_snapshot_index_and_batch_sources(self):
        document = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
        original_module = document["legacy_initial_audit"][0]["source_module"]
        document["legacy_initial_audit"] = copy.deepcopy(document["legacy_initial_audit"])
        document["pages"] = copy.deepcopy(document["legacy_initial_audit"])
        document["legacy_effective_view"] = copy.deepcopy(document["legacy_initial_audit"])
        self.assertNotEqual("TAMPERED", original_module)
        for field in ("legacy_initial_audit", "pages", "legacy_effective_view"):
            document[field][0]["source_module"] = "TAMPERED"
        document["effective_legacy_hash"] = hashlib.sha256(
            json.dumps(document["legacy_effective_view"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        codes = {item["code"] for item in validate_audit_document(document, mode="stage")}
        self.assertIn("LEGACY_STAGE_SOURCE_MISMATCH", codes)

    def test_document_status_cannot_disable_stage_source_or_page_view_checks(self):
        document = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
        for field in ("legacy_initial_audit", "pages", "legacy_effective_view"):
            document[field][0]["source_module"] = "SYNC_TAMPER"
        document["effective_legacy_hash"] = hashlib.sha256(
            json.dumps(document["legacy_effective_view"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        document["document_status"] = "pending_review"
        codes = {item["code"] for item in validate_audit_document(document, mode="stage")}
        self.assertIn("AUDIT_DOCUMENT_STATUS_INVALID", codes)
        self.assertIn("AUDIT_DOCUMENT_STATUS_SHAPE_INVALID", codes)

        document = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
        document["document_status"] = "pending_review"
        document["pages"] = document["pages"][:-1]
        codes = {item["code"] for item in validate_audit_document(document, mode="stage")}
        self.assertIn("AUDIT_DOCUMENT_STATUS_INVALID", codes)
        self.assertIn("LEGACY_PAGE_VIEW_MISMATCH", codes)

    def test_page_scope_mutation_cannot_disable_task3_source_reload(self):
        document = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
        for field in ("legacy_initial_audit", "pages", "legacy_effective_view"):
            document[field][0]["source_module"] = "SYNC_TAMPER"
            document[field][0]["audit_scope"] = "review_complete"
        document["effective_legacy_hash"] = hashlib.sha256(
            json.dumps(document["legacy_effective_view"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        document["document_status"] = "structure_in_progress"
        codes = {item["code"] for item in validate_audit_document(document, mode="stage")}
        self.assertIn("AUDIT_DOCUMENT_STATUS_SHAPE_INVALID", codes)
        self.assertIn("LEGACY_AUDIT_SCOPE_INVALID", codes)
        self.assertIn("LEGACY_STAGE_SOURCE_MISMATCH", codes)

    def test_nonobject_current_placeholders_cannot_disable_task3_source_reload(self):
        variants = (("pages", None), ("events", None), ("pages", "junk"), ("events", 0))
        for field, placeholder in variants:
            with self.subTest(field=field, placeholder=placeholder):
                document = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
                for mirror in ("legacy_initial_audit", "pages", "legacy_effective_view"):
                    document[mirror][0]["source_module"] = "SYNC_TAMPER"
                document["effective_legacy_hash"] = hashlib.sha256(
                    json.dumps(document["legacy_effective_view"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest()
                document["document_status"] = "structure_in_progress"
                document["current_release_audit"][field] = [placeholder]
                codes = {item["code"] for item in validate_audit_document(document, mode="stage")}
                self.assertIn("AUDIT_DOCUMENT_STATUS_SHAPE_INVALID", codes)
                self.assertIn("CURRENT_AUDIT_NODE_TYPE_INVALID", codes)
                self.assertIn("LEGACY_STAGE_SOURCE_MISMATCH", codes)

    def test_markdown_is_a_review_ledger_not_a_claim_of_completion(self):
        pages = page_skeletons(snapshot(), "a" * 64)
        markdown = render_markdown(pages, "a" * 64)
        self.assertIn("127页", markdown)
        self.assertIn("S001—S016", markdown)
        self.assertIn("待审，不代表保留、删除或关闭", markdown)
        self.assertIn("旧页1的学生可见文字", markdown)
        self.assertNotIn("decision: 保留", markdown)

    def test_batch_index_hashes_the_exact_serialized_source_files(self):
        pages = page_skeletons(snapshot(), "a" * 64)
        index, sources = batch_documents(pages, "a" * 64)
        for batch in index["batches"]:
            self.assertEqual(
                hashlib.sha256(json_text(sources[batch["initial_source"]]).encode("utf-8")).hexdigest(),
                batch["initial_sha256"],
            )
            self.assertEqual(
                hashlib.sha256(json_text(sources[batch["disposition_source"]]).encode("utf-8")).hexdigest(),
                batch["disposition_sha256"],
            )
            disposition = sources[batch["disposition_source"]]
            initial = sources[batch["initial_source"]]
            self.assertEqual(serialized_sha256(initial), disposition["based_on_initial_sha256"])


if __name__ == "__main__":
    unittest.main()
