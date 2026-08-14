import json
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import audit_exam_answer_scoring_sources as audit
import extract_exam_answer_candidates as candidates
import validate_exam_answer_candidates as candidate_validator
import validate_exam_type_review_queue as queue_validator
import validate_word_pronunciation_kp_batch as pronunciation_validator
import validate_core_language_use_kp_batch as core_language_validator
import validate_classical_language_kp_batch as classical_language_validator
import validate_ancient_content_kp_batch as ancient_content_validator
import validate_classical_translation_kp_batch as classical_translation_validator
import validate_classical_translation_2021_2024_kp_batch as classical_translation_2021_2024_validator
import validate_classical_memorization_kp_batch as classical_memorization_validator
import validate_classical_memorization_2016_2024_kp_batch as classical_memorization_2016_2024_validator
import validate_poetry_appreciation_kp_batch as poetry_appreciation_validator
import validate_poetry_appreciation_2016_2024_kp_batch as poetry_appreciation_2016_2024_validator
import validate_modern_informational_kp_batch as modern_informational_validator
import validate_modern_informational_2016_2024_kp_batch as modern_informational_2016_2024_validator
import validate_literary_reading_kp_batch as literary_reading_validator
import validate_literary_reading_2016_2024_kp_batch as literary_reading_2016_2024_validator
import validate_topic_writing_kp_batch as topic_writing_validator
import validate_topic_writing_2016_2024_kp_batch as topic_writing_2016_2024_validator
import validate_practical_reading_2016_2024_kp_batch as practical_reading_2016_2024_validator
import validate_language_expression_kp_batch as language_expression_validator
import validate_remaining_language_kp_batch as remaining_language_validator
import validate_ancient_reading_2021_2024_kp_batch as ancient_reading_2021_2024_validator
import validate_language_application_2016_2017_kp_batch as language_application_2016_2017_validator
import validate_language_application_2021_2024_kp_batch as language_application_2021_2024_validator
import validate_language_group_subquestion_2018_2020_kp_batch as language_group_subquestion_validator
import validate_language_application_tasks_2018_2020_kp_batch as language_application_tasks_validator
import repair_2024_q009_boundary as q009_boundary_repair


class ExamAnswerAuditTests(unittest.TestCase):
    def test_current_corpus_is_conservative_and_complete(self):
        report = audit.build_audit()
        summary = report["summary"]
        self.assertEqual(summary["years"], 17)
        self.assertEqual(summary["expected_questions"], 310)
        self.assertEqual(summary["indexed_questions"], 118)
        self.assertEqual(summary["vertical_slice_nodes"], 359)
        # 2024 Q021/Q022 now have located local解析候选来源; they remain
        # unverified and M0, but are no longer source-missing placeholders.
        self.assertEqual(summary["vertical_candidate_source_nodes"], 336)
        self.assertEqual(summary["vertical_missing_source_nodes"], 23)
        self.assertEqual(summary["official_verified_questions"], 0)
        self.assertEqual(summary["scoring_official_questions"], 0)
        self.assertEqual(summary["status_counts"]["candidate_mixed_analysis"], 53)
        self.assertEqual(summary["status_counts"]["candidate_answer_only_or_short"], 21)
        self.assertEqual(summary["status_counts"]["missing_source"], 236)
        self.assertTrue(all(year["result"] == "passed_with_gaps" for year in report["years"]))

    def test_candidate_extraction_never_turns_nonempty_source_into_missing(self):
        candidate, method, notes = candidates.extract_candidate("题干\n解析文本，没有显式答案标记")
        self.assertEqual(candidate, "题干\n解析文本，没有显式答案标记")
        self.assertEqual(method, "raw_answer_field_unbounded")
        self.assertIn("manual_boundary_required", notes)
        empty, empty_method, empty_notes = candidates.extract_candidate("")
        self.assertEqual((empty, empty_method), ("", "none"))
        self.assertIn("answer_text_empty", empty_notes)

    def test_candidate_derivatives_match_upstream_hashes(self):
        base = candidate_validator.EXTRACT / "GK-SC-2008"
        result = candidate_validator.validate_exam(base)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["rows"], 21)

    def test_type_review_queue_is_traceable_and_m0_bounded(self):
        queue_rows = [
            line for line in queue_validator.QUEUE.read_text(encoding="utf-8").splitlines() if line.strip()
        ]
        self.assertEqual(len(queue_rows), 359)
        result = queue_validator.main()
        self.assertEqual(result, 0)

    def test_word_pronunciation_batch_preserves_authority_gap(self):
        result = pronunciation_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in pronunciation_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        row_2013 = next(row for row in rows if row["year"] == 2013)
        self.assertEqual(row_2013["answer_candidate"], "B")
        self.assertEqual(row_2013["manual_review_gate"], "source_authority_missing")
        self.assertEqual(row_2013["mapping_level"], "M0")

    def test_core_language_batch_has_balanced_coverage_and_m0_boundary(self):
        result = core_language_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in core_language_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 21)
        counts = {}
        for row in rows:
            counts[row["question_type_l2"]] = counts.get(row["question_type_l2"], 0) + 1
            self.assertEqual(row["mapping_level"], "M0")
            self.assertEqual(row["kp_id"], "N/A")
        self.assertEqual(counts, {"orthography": 7, "word_usage": 7, "sentence_grammar": 7})
        row_2013 = next(row for row in rows if row["year"] == 2013 and row["question_type_l2"] == "orthography")
        self.assertEqual(row_2013["manual_review_gate"], "source_authority_missing")

    def test_classical_language_batch_has_balanced_coverage_and_authority_gate(self):
        result = classical_language_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in classical_language_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 14)
        counts = {}
        for row in rows:
            counts[row["question_type_l2"]] = counts.get(row["question_type_l2"], 0) + 1
            self.assertEqual(row["mapping_level"], "M0")
            self.assertEqual(row["kp_id"], "N/A")
        self.assertEqual(counts, {"ancient_function_words": 7, "ancient_vocab": 7})
        for row in rows:
            if row["year"] == 2013:
                self.assertEqual(row["manual_review_gate"], "source_authority_missing")

    def test_ancient_content_batch_covers_2009_to_2015(self):
        result = ancient_content_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in ancient_content_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 7)
        self.assertEqual([row["year"] for row in rows], list(range(2009, 2016)))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        row_2013 = next(row for row in rows if row["year"] == 2013)
        self.assertEqual(row_2013["manual_review_gate"], "source_authority_missing")
        row_2015 = next(row for row in rows if row["year"] == 2015)
        self.assertEqual(row_2015["ability_level_candidate"], "C")
        self.assertNotIn("理解B", row_2015["knowledge_evidence_excerpt"])

    def test_classical_translation_batch_keeps_free_response_answers_unextracted(self):
        result = classical_translation_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in classical_translation_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 13)
        self.assertEqual(
            {year: sum(row["year"] == year for row in rows) for year in range(2009, 2016)},
            {2009: 2, 2010: 2, 2011: 2, 2012: 3, 2013: 2, 2014: 1, 2015: 1},
        )
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "free_response_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertTrue(all(row["manual_review_gate"] == "source_authority_missing" for row in rows if row["year"] == 2013))

    def test_classical_translation_2021_2024_keeps_shared_scope_and_m0(self):
        result = classical_translation_2021_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in classical_translation_2021_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 5)
        self.assertEqual(
            {year: sum(row["year"] == year for row in rows) for year in range(2021, 2025)},
            {2021: 1, 2022: 1, 2023: 1, 2024: 2},
        )
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["analysis_scope"] == "shared_top_level_analysis_segment" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertTrue(all("【答案】" not in (row["knowledge_evidence_excerpt"] or "") for row in rows))

    def test_classical_memorization_batch_keeps_fill_in_answers_unextracted(self):
        result = classical_memorization_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in classical_memorization_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 11)
        self.assertEqual(
            {year: sum(row["year"] == year for row in rows) for year in range(2009, 2016)},
            {2009: 2, 2010: 2, 2011: 2, 2012: 2, 2013: 1, 2014: 1, 2015: 1},
        )
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "fill_in_answer_not_auto_extracted" for row in rows))

    def test_classical_memorization_2016_2024_keeps_shared_scope_and_m0(self):
        result = classical_memorization_2016_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in classical_memorization_2016_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 13)
        self.assertEqual(
            {year: sum(row["year"] == year for row in rows) for year in range(2016, 2025)},
            {2016: 3, 2017: 1, 2018: 1, 2019: 1, 2020: 1, 2021: 1, 2022: 1, 2023: 1, 2024: 3},
        )
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["analysis_scope"] == "shared_top_level_analysis_segment" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))

    def test_poetry_appreciation_batch_declares_shared_analysis_and_m0(self):
        result = poetry_appreciation_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in poetry_appreciation_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 14)
        self.assertEqual({year: sum(row["year"] == year for row in rows) for year in range(2009, 2016)}, {year: 2 for year in range(2009, 2016)})
        self.assertTrue(all(row["analysis_scope"] == "shared_top_level_analysis_segment" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertTrue(all(row["manual_review_gate"] == "source_authority_missing" for row in rows if row["year"] == 2013))

    def test_poetry_appreciation_2016_2024_declares_shared_analysis_and_m0(self):
        result = poetry_appreciation_2016_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in poetry_appreciation_2016_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 15)
        self.assertEqual(
            {year: sum(row["year"] == year for row in rows) for year in range(2016, 2025)},
            {2016: 2, 2017: 2, 2018: 1, 2019: 1, 2020: 1, 2021: 2, 2022: 2, 2023: 2, 2024: 2},
        )
        self.assertTrue(all(row["analysis_scope"] == "shared_top_level_analysis_segment" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))

    def test_modern_informational_batch_keeps_objective_answers_unextracted(self):
        result = modern_informational_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in modern_informational_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 21)
        self.assertEqual({year: sum(row["year"] == year for row in rows) for year in range(2009, 2016)}, {year: 3 for year in range(2009, 2016)})
        self.assertTrue(all(row["analysis_scope"] == "question_segment_with_possible_related_context" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "objective_answer_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertTrue(all(row["manual_review_gate"] == "source_authority_missing" for row in rows if row["year"] == 2013))

    def test_modern_informational_2016_2024_keeps_objective_answers_unextracted(self):
        result = modern_informational_2016_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in modern_informational_2016_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 21)
        self.assertEqual(
            {year: sum(row["year"] == year for row in rows) for year in range(2016, 2025)},
            {2016: 3, 2017: 3, 2018: 1, 2019: 1, 2020: 1, 2021: 3, 2022: 3, 2023: 3, 2024: 3},
        )
        self.assertTrue(all(row["analysis_scope"] == "question_segment_with_possible_related_context" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "objective_answer_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))

    def test_literary_reading_batch_keeps_related_context_and_m0(self):
        result = literary_reading_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in literary_reading_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 28)
        self.assertEqual({year: sum(row["year"] == year for row in rows) for year in range(2009, 2016)}, {year: 4 for year in range(2009, 2016)})
        self.assertTrue(all(row["analysis_scope"] == "question_segment_with_possible_related_context" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "literary_response_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertTrue(all(row["manual_review_gate"] == "source_authority_missing" for row in rows if row["year"] == 2013))

    def test_literary_reading_2016_2024_keeps_related_context_and_m0(self):
        result = literary_reading_2016_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in literary_reading_2016_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 22)
        self.assertEqual(
            {year: sum(row["year"] == year for row in rows) for year in range(2016, 2025)},
            {2016: 4, 2017: 3, 2018: 1, 2019: 1, 2020: 1, 2021: 3, 2022: 3, 2023: 3, 2024: 3},
        )
        self.assertTrue(all(row["analysis_scope"] == "question_segment_with_possible_related_context" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "literary_response_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))

    def test_practical_reading_2016_2024_keeps_related_context_and_m0(self):
        result = practical_reading_2016_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in practical_reading_2016_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 22)
        self.assertEqual(
            {year: sum(row["year"] == year for row in rows) for year in range(2016, 2025)},
            {2016: 4, 2017: 3, 2018: 1, 2019: 1, 2020: 1, 2021: 3, 2022: 3, 2023: 3, 2024: 3},
        )
        self.assertTrue(all(row["analysis_scope"] == "question_segment_with_possible_related_context" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "practical_response_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))

    def test_ancient_reading_2021_2024_keeps_objective_answers_unextracted(self):
        result = ancient_reading_2021_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in ancient_reading_2021_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 12)
        self.assertEqual({year: sum(row["year"] == year for row in rows) for year in range(2021, 2025)}, {2021: 3, 2022: 3, 2023: 3, 2024: 3})
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "objective_answer_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))

    def test_topic_writing_batch_keeps_long_form_answers_unextracted(self):
        result = topic_writing_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in topic_writing_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 7)
        self.assertEqual([row["year"] for row in rows], list(range(2009, 2016)))
        self.assertTrue(all(row["analysis_scope"] == "top_level_exam_segment_with_possible_unrelated_context" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "writing_response_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertEqual(next(row for row in rows if row["year"] == 2013)["manual_review_gate"], "source_authority_missing")

    def test_topic_writing_2016_2024_keeps_long_form_answers_unextracted(self):
        result = topic_writing_2016_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in topic_writing_2016_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 9)
        self.assertEqual({year: sum(row["year"] == year for row in rows) for year in range(2016, 2025)}, {year: 1 for year in range(2016, 2025)})
        self.assertTrue(all(row["analysis_scope"] == "top_level_exam_segment_with_possible_unrelated_context" for row in rows))
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "writing_response_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))

    def test_language_expression_batch_covers_four_free_response_types(self):
        result = language_expression_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in language_expression_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 15)
        counts = {}
        for row in rows:
            counts[row["question_type_l2"]] = counts.get(row["question_type_l2"], 0) + 1
            self.assertEqual(row["answer_candidate"], None)
            self.assertEqual(row["answer_candidate_method"], "language_expression_not_auto_extracted")
            self.assertEqual(row["mapping_level"], "M0")
            self.assertEqual(row["kp_id"], "N/A")
        self.assertEqual(counts, {"parallelism_or_practical": 4, "practical_or_expansion": 3, "sentence_expansion": 4, "summary": 4})
        row_2013 = next(row for row in rows if row["year"] == 2013)
        self.assertEqual(row_2013["manual_review_gate"], "source_authority_missing")

    def test_remaining_language_batch_closes_six_uncovered_nodes(self):
        result = remaining_language_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in remaining_language_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 6)
        self.assertEqual(
            {row["question_type_l2"]: sum(item["question_type_l2"] == row["question_type_l2"] for item in rows) for row in rows},
            {"sentence_segmentation": 3, "summary_or_application": 3},
        )
        self.assertEqual(
            {row["exam_node_id"] for row in rows},
            {f"GK-SC-{year}-Q012-TOP" for year in (2013, 2014, 2015)}
            | {f"GK-SC-{year}-Q019-TOP" for year in (2013, 2014, 2015)},
        )
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "remaining_language_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertTrue(all(row["manual_review_gate"] == "source_authority_missing" for row in rows if row["year"] == 2013))

    def test_language_application_2016_2017_batch_covers_stable_q7_to_q11(self):
        result = language_application_2016_2017_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in language_application_2016_2017_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 10)
        self.assertEqual(
            {row["candidate_subtype"]: sum(item["candidate_subtype"] == row["candidate_subtype"] for item in rows) for row in rows},
            {
                "idiom_usage": 2,
                "sentence_error": 2,
                "discourse_connective_selection": 2,
                "completion": 2,
                "constructed_language_response": 2,
            },
        )
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "language_application_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertEqual(next(row for row in rows if row["exam_node_id"] == "GK-NC3-2017-Q009-TOP")["ocr_status"], "suspected_ocr_or_watermark_noise")

    def test_language_application_2021_2024_batch_covers_q17_to_q21(self):
        result = language_application_2021_2024_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in language_application_2021_2024_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 20)
        self.assertEqual({(row["year"], row["question_id"]) for row in rows}, {(year, qid) for year in (2021, 2022, 2023, 2024) for qid in range(17, 22)})
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "language_application_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        row_2024_q21 = next(row for row in rows if row["year"] == 2024 and row["question_id"] == 21)
        self.assertEqual(row_2024_q21["manual_review_gate"], "source_authority_missing")

    def test_language_group_subquestion_batch_preserves_parent_and_score_boundaries(self):
        result = language_group_subquestion_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in language_group_subquestion_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 9)
        self.assertEqual({(row["year"], row["subquestion_code"]) for row in rows}, {(year, code) for year in (2018, 2019, 2020) for code in ("1", "2", "3")})
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["answer_candidate_method"] == "language_group_not_auto_extracted" for row in rows))
        self.assertTrue(all(row["score_candidate"] is None and row["score_status"] == "group_total_only_not_allocated" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))

    def test_language_application_tasks_batch_preserves_q8_q9_boundaries(self):
        result = language_application_tasks_validator.main()
        self.assertEqual(result, 0)
        rows = [
            json.loads(line)
            for line in language_application_tasks_validator.BATCH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 14)
        self.assertEqual(
            {(row["year"], row["question_id"], row["task_code"]) for row in rows},
            {
                *((2018, 8, code) for code in ("1", "2", "3", "4", "5")),
                (2018, 9, "1"),
                *((2019, 8, code) for code in ("1", "2", "3")),
                (2019, 9, "1"),
                *((2020, 8, code) for code in ("1", "2", "3")),
                (2020, 9, "1"),
            },
        )
        self.assertTrue(all(row["answer_candidate"] is None for row in rows))
        self.assertTrue(all(row["score_candidate"] is None and row["score_status"] == "question_total_only_not_allocated" for row in rows))
        self.assertTrue(all(row["mapping_level"] == "M0" and row["kp_id"] == "N/A" for row in rows))
        self.assertTrue(any(row["year"] == 2020 and row["question_id"] == 8 and row["ocr_status"] == "suspected_ocr_or_watermark_noise" for row in rows))

    def test_2024_q009_boundary_repair_keeps_raw_prompt_and_trims_derivatives(self):
        for role in ("question", "analysis"):
            path = q009_boundary_repair.EXTRACT / "GK-NCA-2024" / "segments" / role / "Q009.md"
            _, _, body = q009_boundary_repair.split_markdown(path.read_text(encoding="utf-8"))
            self.assertNotIn(q009_boundary_repair.SEGMENT_MARKER, body)
        vertical = q009_boundary_repair.KP / "GK-NCA-2024-response_nodes_vertical_slice.jsonl"
        row = next(json.loads(line) for line in vertical.read_text(encoding="utf-8").splitlines() if '"GK-NCA-2024-Q009-TOP"' in line)
        self.assertIn(q009_boundary_repair.SEGMENT_MARKER, row["prompt_text_raw"])
        self.assertNotIn(q009_boundary_repair.SEGMENT_MARKER, row["prompt_text_for_extraction"])
        self.assertEqual(row["source_pdf_page_index_end"], 5)
        self.assertEqual(row["boundary_status"], "boundary_reviewed_trimmed")


if __name__ == "__main__":
    unittest.main()
