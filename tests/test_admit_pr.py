# -*- coding: utf-8 -*-
"""PR 准入器测试（synthetic）。"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("admit_pr", ROOT / "scripts/admit_pr.py")
ap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ap)

EIDS = {"REF-20990101-01", "OBS-20990101-01"}


def pr(**kw):
    base = {
        "id": "PR-20990101-99", "trigger_evidence": ["REF-20990101-01"], "node": "U7",
        "change_type": "new",
        "draft": {"title": "t", "statement": "s",
                  "enforcement": [{"type": "design_trace", "fields": ["normal_counterexample"]}]},
        "target_standard": "STANDARD-next", "status": "proposed",
    }
    base.update(kw)
    return base


class AdmitTest(unittest.TestCase):
    def test_valid_pr_admitted(self):
        errors, _ = ap.admit(pr(), EIDS)
        self.assertEqual(errors, [])

    def test_no_trigger_rejected(self):
        errors, _ = ap.admit(pr(trigger_evidence=[]), EIDS)
        self.assertTrue(any("触发证据" in e for e in errors))

    def test_missing_evidence_rejected(self):
        errors, _ = ap.admit(pr(trigger_evidence=["REF-NOPE"]), EIDS)
        self.assertTrue(any("证据不存在" in e for e in errors))

    def test_bad_node_rejected(self):
        errors, _ = ap.admit(pr(node="Z9"), EIDS)
        self.assertTrue(any("node 非法" in e for e in errors))

    def test_retire_needs_no_draft(self):
        errors, _ = ap.admit(pr(change_type="retire", draft={}), EIDS)
        self.assertEqual(errors, [])

    def test_machine_check_needs_rule(self):
        draft = {"title": "t", "statement": "s", "enforcement": [{"type": "machine_check", "checker": "x.py"}]}
        errors, _ = ap.admit(pr(draft=draft), EIDS)
        self.assertTrue(any("缺 rule" in e for e in errors))

    def test_current_standard_rejected(self):
        errors, _ = ap.admit(pr(target_standard="STANDARD-1.0"), EIDS)
        self.assertTrue(any("不追溯" in e or "下一版本" in e for e in errors))

    def test_emit_yaml_shape(self):
        y = ap.emit_yaml(pr())
        self.assertIn("nodes: [U7]", y)
        self.assertIn("design_trace", y)
        self.assertIn("status: proposed", y)


if __name__ == "__main__":
    unittest.main()
