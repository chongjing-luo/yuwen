# -*- coding: utf-8 -*-
"""学情诊断分析器测试（synthetic 数据，仅用于格式与逻辑验证，不入台账目录）。"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from analyze_mastery import analyze, load_entries, render_markdown, resolve_card  # noqa: E402


def entry(student, kp, score, max_score=2, error_type=None, date="2026-09-10"):
    data = {
        "date": date,
        "class_id": "SYNTHETIC-TEST",
        "student_id": student,
        "source": {"type": "quiz", "ref": "SYNTHETIC/格式验证"},
        "kp_id": kp,
        "score": score,
        "max_score": max_score,
    }
    if error_type:
        data["error_type"] = error_type
    return data


KP_A = "KP-CARD-X3-U01-01-004"  # 比兴（真实卡内 KP）
KP_B = "KP-CARD-X3-U01-01-003"  # 叙事链


class ResolveCardTest(unittest.TestCase):
    def test_resolve_real_kp(self):
        self.assertIsNotNone(resolve_card(KP_A))

    def test_reject_malformed_kp(self):
        self.assertIsNone(resolve_card("KP-XX"))
        self.assertIsNone(resolve_card("KP-CARD-ZZ-U99-99-999"))


class LoadEntriesTest(unittest.TestCase):
    def test_synthetic_ledger_loads(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as fh:
            for e in [entry("S1", KP_A, 0), entry("S1", KP_B, 2), entry("S2", KP_A, 1)]:
                fh.write(json.dumps(e, ensure_ascii=False) + "\n")
            path = fh.name
        entries = load_entries(Path(path))
        self.assertEqual(len(entries), 3)
        Path(path).unlink()

    def test_missing_field_rejected(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as fh:
            fh.write(json.dumps({"date": "2026-09-10", "student_id": "S1", "kp_id": KP_A, "score": 1, "max_score": 2}, ensure_ascii=False) + "\n")
            path = fh.name
        with self.assertRaises(ValueError):
            load_entries(Path(path))
        Path(path).unlink()

    def test_unknown_kp_rejected(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as fh:
            fh.write(json.dumps(entry("S1", "KP-CARD-ZZ-U99-99-999", 1), ensure_ascii=False) + "\n")
            path = fh.name
        with self.assertRaises(ValueError):
            load_entries(Path(path))
        Path(path).unlink()


class AnalyzeTest(unittest.TestCase):
    def test_reteach_threshold(self):
        entries = [entry(f"S{i}", KP_A, 0 if i % 2 == 0 else 1) for i in range(4)] + [entry(f"S{i}", KP_B, 2) for i in range(4)]
        analysis = analyze(entries, threshold=0.6)
        self.assertLess(analysis["kp"][KP_A]["rate"], 0.6)
        self.assertTrue(analysis["kp"][KP_A]["reteach"])
        self.assertFalse(analysis["kp"][KP_B]["reteach"])

    def test_error_types_aggregated(self):
        entries = [
            entry("S1", KP_A, 0, error_type="现代义干扰"),
            entry("S2", KP_A, 0, error_type="现代义干扰"),
            entry("S3", KP_A, 1, error_type="形近混淆"),
        ]
        analysis = analyze(entries, threshold=0.6)
        self.assertEqual(analysis["kp"][KP_A]["error_types"], {"现代义干扰": 2, "形近混淆": 1})

    def test_markdown_renders(self):
        entries = [entry("S1", KP_A, 0), entry("S1", KP_B, 2)]
        report = render_markdown(analyze(entries, 0.6), "SYNTHETIC-TEST")
        self.assertIn("回教", report)
        self.assertIn("SYNTHETIC", report)
        self.assertIn("真实作业", report)


if __name__ == "__main__":
    unittest.main()
