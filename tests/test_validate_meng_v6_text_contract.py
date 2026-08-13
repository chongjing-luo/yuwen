from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VERIFY = PROJECT_ROOT / "scripts" / "meng_v6" / "verify_text.js"


def run_verifier(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", str(VERIFY), *args],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def dump_contract() -> dict:
    result = run_verifier("--dump-json")
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return json.loads(result.stdout)


class MengV6TextContractTests(unittest.TestCase):
    def test_contract_freezes_six_chapters_and_ordered_thirty_lines(self):
        contract = dump_contract()
        self.assertEqual("1.0", contract["schema_version"])
        self.assertEqual(6, len(contract["chapters"]))
        lines = contract["lines"]
        self.assertEqual([f"L{number:03d}" for number in range(1, 31)], [line["line_id"] for line in lines])
        self.assertEqual([1, 2, 3, 4, 5] * 6, [line["chapter_line_order"] for line in lines])
        self.assertEqual(
            "氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。",
            "。".join(line["text"] for line in lines[:2]) + "。",
        )
        self.assertEqual("反是不思，亦已焉哉", lines[-1]["text"])
        self.assertTrue(all(line["source_ref"] == "TEXTBOOK#氓正文" for line in lines))

    def test_twelve_meaning_units_are_contiguous_disjoint_and_exhaustive(self):
        contract = dump_contract()
        units = contract["meaning_units"]
        self.assertEqual(12, len(units))
        covered = [line_id for unit in units for line_id in unit["line_ids"]]
        self.assertEqual([f"L{number:03d}" for number in range(1, 31)], covered)
        self.assertEqual(len(covered), len(set(covered)))
        for unit in units:
            numbers = [int(line_id[1:]) for line_id in unit["line_ids"]]
            self.assertEqual(list(range(numbers[0], numbers[-1] + 1)), numbers)
        self.assertEqual(["L006", "L007", "L008"], units[2]["line_ids"])
        self.assertEqual(["L013", "L014", "L015"], units[5]["line_ids"])

    def test_interpretive_boundaries_state_allowed_and_forbidden_claims(self):
        contract = dump_contract()
        boundaries = {item["boundary_id"]: item for item in contract["interpretive_boundaries"]}
        required = {
            "CHI_CHI_IMPRESSION", "TRADE_VS_PROPOSAL", "NO_ANGER_AMBIGUITY",
            "SANG_LEAF_OPENNESS", "VIOLENCE_SCOPE", "FAMILY_SUPPORT_BOUNDARY",
            "QI_BANK_MULTIPLE_READINGS", "STOP_JUDGMENT_BOUNDARY", "RESPONSIBILITY_CAUSE_SPLIT",
        }
        self.assertTrue(required.issubset(boundaries))
        for boundary_id in required:
            boundary = boundaries[boundary_id]
            self.assertTrue(boundary["evidence_line_ids"])
            self.assertTrue(boundary["allowed_claims"])
            self.assertTrue(boundary["forbidden_claims"])
        split = boundaries["RESPONSIBILITY_CAUSE_SPLIT"]
        self.assertIn("女子的投入、长期劳作或未及时停止，解释或分担了男子失信、反复和粗暴的责任", split["forbidden_claims"])
        stop = boundaries["STOP_JUDGMENT_BOUNDARY"]
        self.assertIn("诗没有写明她已经实际离家、怎样离开或后来怎样生活", stop["allowed_claims"])
        self.assertIn("诗已经写明她实际离家并获得新的生活", stop["forbidden_claims"])
        family = boundaries["FAMILY_SUPPORT_BOUNDARY"]
        self.assertIn("兄弟是诗中明确写出的家人；更广义的支持缺失只能标为处境推断", family["allowed_claims"])
        self.assertEqual(64, len(contract["source"]["textbook_sha256"]))
        self.assertEqual(64, len(contract["source"]["evidence_dossier_sha256"]))

    def test_verifier_rejects_line_drift_noncontiguous_units_and_boundary_loss(self):
        contract = dump_contract()
        mutations = []

        line_drift = copy.deepcopy(contract)
        line_drift["lines"][0]["text"] = "氓之蚩蚩，抱币贸丝"
        mutations.append((line_drift, "TEXT_LINE_MISMATCH"))

        unit_gap = copy.deepcopy(contract)
        unit_gap["meaning_units"][0]["line_ids"] = ["L001", "L003"]
        mutations.append((unit_gap, "MEANING_UNIT_COVERAGE_INVALID"))

        boundary_loss = copy.deepcopy(contract)
        boundary_loss["interpretive_boundaries"] = [
            item for item in boundary_loss["interpretive_boundaries"]
            if item["boundary_id"] != "RESPONSIBILITY_CAUSE_SPLIT"
        ]
        mutations.append((boundary_loss, "BOUNDARY_SET_INVALID"))

        action_drift = copy.deepcopy(contract)
        action_drift["chapters"][0]["action_chain"] = ["越界"] * 5
        mutations.append((action_drift, "CHAPTER_SEMANTICS_MISMATCH"))

        unit_semantic_drift = copy.deepcopy(contract)
        unit_semantic_drift["meaning_units"][0]["line_ids"] = ["L001"]
        unit_semantic_drift["meaning_units"][1]["line_ids"] = ["L002", "L003", "L004", "L005"]
        mutations.append((unit_semantic_drift, "MEANING_UNIT_SEMANTICS_MISMATCH"))

        boundary_reversal = copy.deepcopy(contract)
        boundary = next(item for item in boundary_reversal["interpretive_boundaries"] if item["boundary_id"] == "RESPONSIBILITY_CAUSE_SPLIT")
        boundary["allowed_claims"] = ["女子应承担男子粗暴的责任"]
        boundary["forbidden_claims"] = ["不得归责男子"]
        mutations.append((boundary_reversal, "BOUNDARY_SEMANTICS_MISMATCH"))

        source_redirect = copy.deepcopy(contract)
        source_redirect["source"]["textbook_path"] = source_redirect["source"]["evidence_dossier_path"]
        source_redirect["source"]["textbook_sha256"] = source_redirect["source"]["evidence_dossier_sha256"]
        mutations.append((source_redirect, "TEXT_SOURCE_IDENTITY_MISMATCH"))

        bad_schema = copy.deepcopy(contract)
        bad_schema["schema_version"] = "evil"
        mutations.append((bad_schema, "TEXT_CONTRACT_IDENTITY_MISMATCH"))

        bad_id = copy.deepcopy(contract)
        bad_id["contract_id"] = "OTHER"
        mutations.append((bad_id, "TEXT_CONTRACT_IDENTITY_MISMATCH"))

        bad_chapter_order = copy.deepcopy(contract)
        bad_chapter_order["lines"][0]["chapter_order"] = 99
        mutations.append((bad_chapter_order, "TEXT_LINE_MISMATCH"))

        for mutation, expected_code in mutations:
            with self.subTest(expected_code=expected_code):
                with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
                    json.dump(mutation, handle, ensure_ascii=False)
                    path = Path(handle.name)
                try:
                    result = run_verifier("--input", str(path))
                finally:
                    path.unlink(missing_ok=True)
                self.assertNotEqual(0, result.returncode)
                self.assertIn(expected_code, result.stderr)


if __name__ == "__main__":
    unittest.main()
