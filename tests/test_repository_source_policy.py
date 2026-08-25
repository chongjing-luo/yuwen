import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from repository_source_policy import reference_is_available


def test_declared_private_exam_pdf_may_be_absent(tmp_path: Path):
    path = "Data/2008-2024·（四川）语文高考真题/2014年高考语文试卷（四川）（空白卷）.pdf"

    assert reference_is_available(tmp_path, path)


def test_declared_private_textbook_pdf_may_be_absent(tmp_path: Path):
    path = "Data/textbook/普通高中教科书·语文必修 上册.pdf"

    assert reference_is_available(tmp_path, path)


def test_public_processed_source_must_exist(tmp_path: Path):
    path = "work/knowledge/exams/papers/PAPER-SCZ-2014/raw/README.md"

    assert not reference_is_available(tmp_path, path)
    target = tmp_path / path
    target.parent.mkdir(parents=True)
    target.write_text("来源登记\n", encoding="utf-8")
    assert reference_is_available(tmp_path, path)


def test_public_curriculum_pdf_is_not_treated_as_private(tmp_path: Path):
    path = "Data/reference/curriculum/普通高中语文课程标准.pdf"

    assert not reference_is_available(tmp_path, path)


def test_absolute_and_parent_traversal_paths_are_rejected(tmp_path: Path):
    assert not reference_is_available(tmp_path, "/etc/passwd")
    assert not reference_is_available(tmp_path, "../private.pdf")
