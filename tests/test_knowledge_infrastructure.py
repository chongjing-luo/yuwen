import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import bootstrap_knowledge_infrastructure as bootstrap


class KnowledgeInventoryTests(unittest.TestCase):
    def test_real_package_inventory_has_expected_counts(self):
        packages = bootstrap.discover_packages(PROJECT_ROOT)
        counts = Counter(record["audience"] for record in packages)

        self.assertEqual(len(packages), 144)
        self.assertEqual(counts, {"student": 113, "teacher": 31})
        self.assertEqual(
            Counter(record["book_code"] for record in packages),
            {"B1": 27, "B2": 27, "X1": 18, "X2": 20, "X3": 21, "TB2": 31},
        )

    def test_deliverable_inventory_is_exact_and_dependency_closed(self):
        packages = bootstrap.discover_packages(PROJECT_ROOT)
        deliverables = bootstrap.build_deliverables(packages)
        type_counts = Counter(record["deliverable_type"] for record in deliverables)

        self.assertEqual(len(deliverables), 120)
        self.assertEqual(
            type_counts,
            {
                "knowledge_card": 81,
                "unit_graph": 28,
                "book_summary": 5,
                "exam_analysis": 4,
                "exam_kp_mapping": 1,
                "global_map": 1,
            },
        )
        ids = [record["deliverable_id"] for record in deliverables]
        self.assertEqual(len(ids), len(set(ids)))
        known = set(ids)
        for record in deliverables:
            self.assertTrue(set(record["upstream_deliverable_ids"]).issubset(known))

    def test_duplicate_x3_source_prefixes_receive_distinct_permanent_ids(self):
        packages = bootstrap.discover_packages(PROJECT_ROOT)
        duplicates = [
            record
            for record in packages
            if record["book_code"] == "X3" and Path(record["local_path"]).name.startswith("13_U3_")
        ]
        self.assertEqual(len(duplicates), 2)
        self.assertEqual(len({record["source_id"] for record in duplicates}), 2)

        deliverables = bootstrap.build_deliverables(packages)
        cards = [
            record
            for record in deliverables
            if record["deliverable_type"] == "knowledge_card"
            and any(source_id in {item["source_id"] for item in duplicates} for source_id in record["source_ids"])
        ]
        self.assertEqual(len(cards), 2)
        self.assertEqual(len({record["deliverable_id"] for record in cards}), 2)

    def test_existing_samples_are_imports_not_accepted_outputs(self):
        packages = bootstrap.discover_packages(PROJECT_ROOT)
        deliverables = bootstrap.build_deliverables(packages)
        imported = [record for record in deliverables if record["status"] == "draft_existing"]

        self.assertEqual(
            {record["deliverable_id"] for record in imported},
            {"CARD-B1-U01-01", "CARD-B1-U01-02", "CARD-B1-U01-03", "UNIT-B1-U01"},
        )
        self.assertFalse(any(record["status"] == "accepted" for record in deliverables))

    def test_page_range_match_is_one_based_and_must_be_unique(self):
        self.assertEqual(
            bootstrap.find_contiguous_range(["a", "b", "c", "d"], ["b", "c"]),
            (2, 3),
        )
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            bootstrap.find_contiguous_range(["a", "b", "a", "b"], ["a", "b"])

    def test_jsonl_writer_refuses_to_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "records.jsonl"
            destination.write_text('{"old": true}\n', encoding="utf-8")

            with self.assertRaises(FileExistsError):
                bootstrap.write_jsonl(destination, [{"new": True}], force=False)

            bootstrap.write_jsonl(destination, [{"new": True}], force=True)
            self.assertEqual(
                [json.loads(line) for line in destination.read_text(encoding="utf-8").splitlines()],
                [{"new": True}],
            )


class SourceRegistryIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packages = bootstrap.discover_packages(PROJECT_ROOT)
        cls.registries = bootstrap.build_source_registries(PROJECT_ROOT, cls.packages)

    def test_sources_and_canonical_artifacts_are_one_to_one(self):
        sources = self.registries["sources"]
        artifacts = self.registries["artifacts"]
        source_counts = Counter(record["source_kind"] for record in sources)

        self.assertEqual(
            source_counts,
            {"textbook_master": 6, "textbook_package": 144, "curriculum_standard": 2},
        )
        canonical_counts = Counter(record["source_id"] for record in artifacts if record["is_canonical"])
        self.assertEqual(set(canonical_counts), {record["source_id"] for record in sources})
        self.assertTrue(all(count == 1 for count in canonical_counts.values()))

    def test_artifact_repository_visibility_matches_public_distribution_boundary(self):
        artifacts = self.registries["artifacts"]

        self.assertEqual(
            Counter(record["repository_visibility"] for record in artifacts),
            {"public": 971, "private_local": 295},
        )
        self.assertEqual(
            {
                record["artifact_role"]
                for record in artifacts
                if record["repository_visibility"] == "private_local"
            },
            {"master_pdf", "split_pdf", "mineru_origin_pdf"},
        )

    def test_all_split_mappings_are_verified_and_page_exact(self):
        manifests = self.registries["split_manifest"]
        self.assertEqual(len(manifests), 144)
        for record in manifests:
            self.assertEqual(record["mapping_verification_status"], "verified")
            self.assertEqual(
                record["verification_method"],
                "normalized_text_with_render_fallback_all_pages_and_sequence",
            )
            self.assertEqual(
                record["original_page_end"] - record["original_page_start"] + 1,
                record["split_page_count"],
            )
            self.assertTrue(record["page_count_check"])

    def test_package_relations_and_teacher_edition_boundary_are_explicit(self):
        relations = self.registries["source_relations"]
        relation_counts = Counter(record["relation_type"] for record in relations)

        self.assertEqual(relation_counts["excerpt_of"], 144)
        edition = [record for record in relations if record["relation_type"] == "edition_match"]
        self.assertEqual(len(edition), 1)
        self.assertEqual(edition[0]["relation_status"], "unknown")


if __name__ == "__main__":
    unittest.main()
