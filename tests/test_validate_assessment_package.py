# -*- coding: utf-8 -*-
"""命题组卷校验器测试。"""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_assessment_package import load_bank, validate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_PATH = ROOT / "work/knowledge/assessment/blueprint_X3U01_poetry_slice.json"


def real_blueprint():
    return json.loads(BLUEPRINT_PATH.read_text(encoding="utf-8"))


class RealPackageTest(unittest.TestCase):
    def test_real_blueprint_passes(self):
        errors, warnings = validate(real_blueprint(), load_bank())
        self.assertEqual(errors, [], f"真实蓝图应通过: {errors}")

    def test_bank_has_authored_and_reference_items(self):
        bank = load_bank()
        self.assertTrue(any(i["item_id"].startswith("IB-AU") for i in bank.values()))
        refs = [i for i in bank.values() if i.get("candidate_status") == "candidate_only_M0"]
        self.assertGreaterEqual(len(refs), 4)
        for item in refs:
            self.assertTrue(item.get("prompt_source") and item.get("analysis_source_sha256"))


class SyntheticBlueprintTest(unittest.TestCase):
    def setUp(self):
        self.bp = real_blueprint()
        self.bank = load_bank()

    def test_score_conservation_detected(self):
        self.bp["total_score"] = 99
        errors, _ = validate(self.bp, self.bank)
        self.assertTrue(any("总分不守恒" in e for e in errors))

    def test_type_distribution_mismatch_detected(self):
        self.bp["type_distribution"][0]["count"] = 2
        errors, _ = validate(self.bp, self.bank)
        self.assertTrue(any("题型分布" in e or "实际" in e for e in errors))

    def test_uncovered_kp_weight_detected(self):
        self.bp["kp_weights"].append({"kp_id": "KP-CARD-X3-U01-01-009", "weight": 1, "basis": "测试"})
        errors, _ = validate(self.bp, self.bank)
        self.assertTrue(any("无学生卷题目覆盖" in e for e in errors))

    def test_candidate_item_in_student_paper_detected(self):
        for entry in self.bp["items"]:
            if entry["bank_ref"] == "IB-SC-001":
                entry["in_student_paper"] = True
        errors, _ = validate(self.bp, self.bank)
        self.assertTrue(any("candidate_only" in e for e in errors))

    def test_missing_homework_ref_detected(self):
        del self.bp["scope"]["homework_ref"]
        errors, _ = validate(self.bp, self.bank)
        self.assertTrue(any("homework_ref" in e for e in errors))

    def test_missing_layering_principle_detected(self):
        self.bp["scoring_principles"] = ["按点给分"]
        errors, _ = validate(self.bp, self.bank)
        self.assertTrue(any("解释分层" in e for e in errors))

    def test_scoring_points_sum_detected(self):
        bank = copy.deepcopy(self.bank)
        bank["IB-AU-002"]["scoring_points"][0]["score"] = 5
        errors, _ = validate(self.bp, bank)
        self.assertTrue(any("scoring_points 合计" in e for e in errors))

    def test_frontstage_leak_detected(self):
        bank = copy.deepcopy(self.bank)
        bank["IB-AU-001"]["stem"] = "本页意图：建立理解链"
        errors, _ = validate(self.bp, bank)
        self.assertTrue(any("后台词" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
