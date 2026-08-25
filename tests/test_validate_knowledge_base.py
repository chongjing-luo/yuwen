import copy
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import bootstrap_knowledge_infrastructure as bootstrap
import validate_knowledge_base as validator


def _registry_fixture(repository_visibility):
    source = {
        "source_id": "SRC-TEST",
        "source_kind": "curriculum_standard",
        "canonical_artifact_id": "ART-TEST",
    }
    artifact = {
        "artifact_id": "ART-TEST",
        "source_id": "SRC-TEST",
        "artifact_role": "test_pdf",
        "carrier_type": "正式电子版",
        "local_path": "private/missing.pdf",
        "byte_size": 1,
        "sha256": "0" * 64,
        "authenticity_status": "verified",
        "is_canonical": True,
        "repository_visibility": repository_visibility,
    }
    return [source], [artifact]


class KnowledgeContractValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.taxonomy = validator.load_json(PROJECT_ROOT / "work/knowledge/_meta/taxonomy.yaml")
        cls.rubrics = validator.load_json(PROJECT_ROOT / "work/knowledge/_meta/rubrics.json")
        cls.packages = bootstrap.load_registered_packages(PROJECT_ROOT)
        cls.deliverables = bootstrap.build_deliverables(cls.packages)

    def test_candidate_taxonomy_and_rubrics_are_valid(self):
        self.assertEqual(validator.validate_taxonomy(self.taxonomy), [])
        self.assertEqual(validator.validate_rubrics(self.rubrics), [])

    def test_rubric_weight_drift_is_rejected(self):
        broken = copy.deepcopy(self.rubrics)
        broken["rubrics"]["knowledge_card"]["dimensions"][0]["weight"] = 24

        errors = validator.validate_rubrics(broken)
        self.assertTrue(any("knowledge_card" in error and "99" in error for error in errors))

    def test_noncanonical_task_group_is_rejected(self):
        broken = copy.deepcopy(self.taxonomy)
        broken["task_groups"][0]["name"] = "整本书阅读与探讨"

        errors = validator.validate_taxonomy(broken)
        self.assertTrue(any("任务群" in error for error in errors))

    def test_deliverable_dependency_and_source_breaks_are_rejected(self):
        known_sources = {record["source_id"] for record in self.packages}
        broken = copy.deepcopy(self.deliverables)
        broken[0]["upstream_deliverable_ids"] = ["CARD-NOT-FOUND"]
        broken[0]["source_ids"] = ["SRC-NOT-FOUND"]

        errors = validator.validate_deliverables(broken, known_sources, self.taxonomy)
        self.assertTrue(any("CARD-NOT-FOUND" in error for error in errors))
        self.assertTrue(any("SRC-NOT-FOUND" in error for error in errors))

    def test_valid_deliverable_inventory_has_no_contract_errors(self):
        known_sources = {record["source_id"] for record in self.packages}
        self.assertEqual(
            validator.validate_deliverables(self.deliverables, known_sources, self.taxonomy),
            [],
        )

    def test_all_schema_and_template_contract_files_are_readable(self):
        self.assertEqual(
            validator.validate_contract_files(PROJECT_ROOT / "work/knowledge"),
            [],
        )

    def test_private_local_artifact_may_be_absent_from_public_checkout(self):
        sources, artifacts = _registry_fixture("private_local")
        with tempfile.TemporaryDirectory() as temp_dir:
            errors = validator.validate_registry_links(
                temp_dir,
                sources,
                artifacts,
                [],
                [],
            )

        self.assertFalse(any("ART-TEST文件不存在" in error for error in errors))

    def test_public_artifact_must_exist_in_public_checkout(self):
        sources, artifacts = _registry_fixture("public")
        with tempfile.TemporaryDirectory() as temp_dir:
            errors = validator.validate_registry_links(
                temp_dir,
                sources,
                artifacts,
                [],
                [],
            )

        self.assertTrue(any("ART-TEST文件不存在" in error for error in errors))

    def test_artifact_repository_visibility_is_required(self):
        sources, artifacts = _registry_fixture(None)
        with tempfile.TemporaryDirectory() as temp_dir:
            errors = validator.validate_registry_links(
                temp_dir,
                sources,
                artifacts,
                [],
                [],
            )

        self.assertTrue(any("ART-TEST repository_visibility非法" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
