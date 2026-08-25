import json

from scripts.checks.validate_storage_layout import ROOT, validate
from scripts.split_paper_questions import TYPE_VIEW


def test_repository_uses_only_canonical_storage_roots():
    assert validate(ROOT) == []


def test_exam_type_view_generator_targets_canonical_view_root():
    assert TYPE_VIEW == ROOT / "work/knowledge/exams/views/by_type"


def test_storage_contract_does_not_require_lesson_goal_nodes(tmp_path):
    contract = tmp_path / "docs/architecture/storage-layout.json"
    contract.parent.mkdir(parents=True)
    contract.write_text(
        json.dumps(
            {
                "schema_version": "1.1",
                "status": "active",
                "canonical_roots": {},
                "legacy_roots": [],
                "important_paths": [],
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "AGENTS.md").write_text("# test\n", encoding="utf-8")

    assert validate(tmp_path) == []
