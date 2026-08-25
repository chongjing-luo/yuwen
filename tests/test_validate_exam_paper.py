# -*- coding: utf-8 -*-
"""试卷校验器测试（synthetic PAPER 目录 + 真实优先批集成）。"""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vep", ROOT / "scripts/validate_exam_paper.py")
vep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vep)


def make_paper(tmp: Path, name="PAPER-XG1-2020_新高考一卷", *, full=True, readme=True, questions=None, meta=None):
    d = tmp / name
    raw = d / "raw"
    raw.mkdir(parents=True)
    (raw / f"{name.split('_')[0]}.pdf").write_bytes(b"%PDF-1.4 " * 300)
    if readme:
        (raw / "README.md").write_text("原件：`Data/x.pdf`（SHA256 `abc123…`，采集渠道：广东）", encoding="utf-8")
    if full:
        out = d / "mineru_result" / name.split("_")[0]
        out.mkdir(parents=True)
        (out / "full.md").write_text("试卷正文" * 500, encoding="utf-8")
    if questions is not None:
        (d / "questions.jsonl").write_text(
            "\n".join(json.dumps(q, ensure_ascii=False) for q in questions) + "\n", encoding="utf-8")
    if meta is not None:
        (d / "paper.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return d


class SyntheticTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_valid_paper_passes(self):
        d = make_paper(self.tmp, questions=[
            {"question_id": "PAPER-XG1-2020-Q1", "question_type": "poetry_appreciation", "page_ref": 4}],
            meta={"paper_id": "PAPER-XG1-2020", "authority": "S1待核验", "answer_source_status": "missing"})
        self.assertEqual(vep.validate_paper(d, require_questions=True), [])

    def test_missing_full_detected(self):
        d = make_paper(self.tmp, full=False)
        errs = vep.validate_paper(d, require_questions=False)
        self.assertTrue(any("full.md" in e for e in errs))

    def test_missing_readme_detected(self):
        d = make_paper(self.tmp, readme=False)
        errs = vep.validate_paper(d, require_questions=False)
        self.assertTrue(any("README" in e for e in errs))

    def test_bad_question_prefix_detected(self):
        d = make_paper(self.tmp, questions=[
            {"question_id": "Q1", "question_type": "x", "page_ref": 1}])
        errs = vep.validate_paper(d, require_questions=True)
        self.assertTrue(any("前缀错误" in e for e in errs))

    def test_bad_answer_status_detected(self):
        d = make_paper(self.tmp, meta={"paper_id": "PAPER-XG1-2020", "authority": "S1待核验",
                                       "answer_source_status": "官方"})
        errs = vep.validate_paper(d, require_questions=False)
        self.assertTrue(any("answer_source_status" in e for e in errs))

    def test_bad_dirname_detected(self):
        d = make_paper(self.tmp, name="随便一个目录")
        errs = vep.validate_paper(d, False)
        self.assertTrue(any("目录名" in e for e in errs))


class IntegrationTest(unittest.TestCase):
    def test_priority_batch_present_and_valid(self):
        base = ROOT / "work/knowledge/exams/papers"
        papers = sorted(d for d in base.iterdir() if d.is_dir() and vep.PAPER_DIR_RE.match(d.name))
        if not papers:
            self.skipTest("优先批尚未落地（MinerU 运行中）")
        for p in papers:
            errs = vep.validate_paper(p, require_questions=False)
            self.assertEqual(errs, [], f"{p.name}: {errs}")


if __name__ == "__main__":
    unittest.main()
