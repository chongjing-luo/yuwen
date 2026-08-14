import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class ReferenceAnswerCandidateTests(unittest.TestCase):
    def test_2020_q002_nested_answer_marker_has_derived_boundary_only(self):
        base = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/answers"
        rows = read_jsonl(base / "answer_clean_candidates.jsonl")
        row = next(r for r in rows if r["question_id"] == 2)
        self.assertEqual(row["cleaning_status"], "derived_answer_boundary_without_analysis")
        self.assertEqual(row["marker_separation_status"], "derived_answer_boundary_with_nested_answer_key")
        self.assertEqual(row["answer_boundary_status"], "resolved_in_derived_layer")
        self.assertEqual(row["manual_boundary"]["marker"], "【解答】")
        self.assertEqual(row["manual_boundary"]["answer_key_marker"], "答案：")
        self.assertEqual(row["scoring_status"], "not_available_as_official")
        self.assertEqual((row["mapping_level"], row["kp_id"]), ("M0", "N/A"))
        receipt = ROOT / "work/knowledge/_reviews/receipts/exam_answer_boundary_GK-NC3-2020-Q002_20260809.json"
        self.assertTrue(receipt.exists())
        receipt_data = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(receipt_data["status"], "resolved_in_derived_layer")
        self.assertFalse(receipt_data["source_mutation"])

    def test_2016_q006_candidate_is_isolated_and_m0(self):
        base = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers"
        rows = read_jsonl(base / "reference_answer_candidates_q006_gzywtk.jsonl")
        self.assertEqual([r["question_id"] for r in rows], [6])
        row = rows[0]
        self.assertEqual(row["candidate_status"], "candidate_unverified")
        self.assertEqual(row["source_authority_status"], "unverified_third_party_reprint")
        self.assertEqual(row["scoring_status"], "not_available_as_official")
        self.assertEqual((row["mapping_level"], row["kp_id"]), ("M0", "N/A"))
        self.assertEqual(row["answer_candidate_sha256"], hashlib.sha256(row["answer_candidate_text"].encode()).hexdigest())
        main = next(r for r in read_jsonl(base / "answer_index.jsonl") if r["question_id"] == 6)
        self.assertEqual(main["answer_status"], "N/A")
        self.assertFalse(main["answer_text"])

    def test_2016_q006_local_recovery_is_separate_and_cross_source_only(self):
        base = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers"
        rows = read_jsonl(base / "reference_answer_candidates_q006_local_analysis.jsonl")
        self.assertEqual([r["question_id"] for r in rows], [6])
        row = rows[0]
        self.assertEqual(row["candidate_scope"], "local_analysis_segment_q006")
        self.assertEqual(row["source_authority_status"], "unverified_local_provided")
        self.assertEqual(row["scoring_status"], "not_available_as_official")
        self.assertEqual((row["mapping_level"], row["kp_id"]), ("M0", "N/A"))
        self.assertTrue(row["external_comparison"]["third_party_candidate_id"])
        self.assertFalse(row["external_comparison"]["exact_text_match"])
        main = next(r for r in read_jsonl(base / "answer_index.jsonl") if r["question_id"] == 6)
        self.assertEqual(main["answer_status"], "N/A")
        self.assertFalse(main["answer_text"])

    def test_2024_meipian_candidate_has_full_coverage_and_guidance_boundary(self):
        base = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers"
        rows = read_jsonl(base / "reference_answer_candidates_meipian.jsonl")
        self.assertEqual([r["question_id"] for r in rows], list(range(1, 23)))
        self.assertEqual(rows[-1]["candidate_content_type"], "writing_guidance_candidate")
        self.assertTrue(all(r["mapping_level"] == "M0" and r["kp_id"] == "N/A" for r in rows))
        self.assertTrue(all(r["scoring_status"] == "not_available_as_official" for r in rows))
        self.assertEqual(len([r for r in read_jsonl(base / "answer_index.jsonl") if not r["answer_text"]]), 22)

    def test_2024_local_analysis_candidate_preserves_conflict_and_ocr_gates(self):
        base = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers"
        rows = read_jsonl(base / "reference_answer_candidates_local_analysis.jsonl")
        self.assertEqual([r["question_id"] for r in rows], list(range(1, 23)))
        q1 = rows[0]
        self.assertEqual(q1["candidate_extraction_method"], "derived_from_analysis_conclusion")
        q12 = next(r for r in rows if r["question_id"] == 12)
        self.assertEqual(q12["answer_candidate_text"], "A")
        self.assertEqual(q12["external_comparison"]["adjudication"], "conflict_requires_independent_verification")
        q16 = next(r for r in rows if r["question_id"] == 16)
        self.assertEqual(q16["q16_duplicate_symbol_counts"], {"①": 2, "②": 2, "③": 2, "④": 2, "⑤": 2, "⑥": 2})
        self.assertIn("o崖", q16["answer_candidate_text"])
        self.assertEqual(q16["scoring_status"], "not_available_as_official")
        self.assertEqual((q16["mapping_level"], q16["kp_id"]), ("M0", "N/A"))
        q22 = rows[-1]
        self.assertEqual(q22["candidate_content_type"], "writing_model_essay_candidate")
        self.assertEqual(q22["external_comparison"]["adjudication"], "not_comparable_writing_artifact")

    def test_2013_candidate_comparison_is_cross_source_only(self):
        base = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers"
        rows = read_jsonl(base / "reference_answer_candidate_comparison.jsonl")
        self.assertEqual([r["question_id"] for r in rows], list(range(1, 22)))
        self.assertEqual(rows[0]["comparison_status"], "textually_consistent_unverified")
        self.assertEqual(next(r for r in rows if r["question_id"] == 3)["comparison_status"], "local_mixed_analysis_no_explicit_answer")
        self.assertEqual(next(r for r in rows if r["question_id"] == 16)["comparison_status"], "ocr_or_format_difference_requires_review")
        self.assertEqual(next(r for r in rows if r["question_id"] == 20)["comparison_status"], "coverage_difference_requires_review")
        self.assertEqual(rows[-1]["comparison_status"], "both_sources_missing")
        self.assertTrue(all(r["adjudication"] == "not_adjudicated" for r in rows))
        self.assertTrue(all(r["scoring_status"] == "not_available_as_official" for r in rows))
        self.assertTrue(all((r["mapping_level"], r["kp_id"]) == ("M0", "N/A") for r in rows))
        validation = ROOT / "work/knowledge/_meta/reference_answer_candidate_comparison_validation_2013_20260809.json"
        self.assertEqual(json.loads(validation.read_text(encoding="utf-8"))["result"], "passed")

    def test_2023_partial_external_and_group_split_remain_conservative(self):
        base = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers"
        external = read_jsonl(base / "reference_answer_candidates.jsonl")
        self.assertEqual([r["question_id"] for r in external], [1, 2, 3, 6, 7, 8, 9, 10])
        self.assertTrue(all(r["source_authority_status"] == "unverified_third_party_reprint" for r in external))
        self.assertTrue(all(r["scoring_status"] == "not_available_as_official" for r in external))
        local = read_jsonl(base / "local_analysis_group_candidates.jsonl")
        self.assertEqual([r["question_id"] for r in local], list(range(1, 23)))
        self.assertEqual(next(r for r in local if r["question_id"] == 1)["source_group_question_id"], 3)
        self.assertEqual(next(r for r in local if r["question_id"] == 22)["candidate_status"], "candidate_writing_artifact")
        comparison = read_jsonl(base / "reference_answer_candidate_comparison.jsonl")
        self.assertEqual([r["question_id"] for r in comparison], list(range(1, 23)))
        self.assertEqual(comparison[0]["comparison_status"], "textually_consistent_unverified")
        self.assertEqual(next(r for r in comparison if r["question_id"] == 10)["comparison_status"], "local_mixed_analysis_no_explicit_answer")
        self.assertEqual(comparison[-1]["comparison_status"], "writing_artifact_no_external")
        self.assertTrue(all(r["adjudication"] == "not_adjudicated" for r in comparison))
        validation = ROOT / "work/knowledge/_meta/reference_answer_candidate_comparison_validation_2023_20260809.json"
        self.assertEqual(json.loads(validation.read_text(encoding="utf-8"))["result"], "passed")


if __name__ == "__main__":
    unittest.main()
