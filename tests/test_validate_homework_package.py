# -*- coding: utf-8 -*-
"""作业包校验器测试（含对真实《氓》作业包的集成校验）。"""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_homework_package import validate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REAL_PACKAGE = ROOT / "work/teaching/选择性必修下册/氓/homework/homework_package.json"

# 《氓》重制期（教案先行）：真实包归档进 git 历史，数据落盘后用例自动恢复
_skip_real = "重制中：真实作业包已归档"
HAS_REAL_PACKAGE = REAL_PACKAGE.exists()


def real_package():
    if not HAS_REAL_PACKAGE:
        raise unittest.SkipTest(_skip_real)
    return json.loads(REAL_PACKAGE.read_text(encoding="utf-8"))


class RealPackageTest(unittest.TestCase):
    def test_real_homework_package_passes(self):
        errors, warnings = validate(real_package(), REAL_PACKAGE)
        self.assertEqual(errors, [], f"真实作业包应通过: {errors}")

    def test_real_package_mechanism_floor(self):
        pkg = real_package()
        modes = {i["retrieval_mode"] for i in pkg["items"]}
        tiers = {i["tier"] for i in pkg["items"]}
        self.assertIn("闭卷检索", modes, "K3/N-02 闭卷检索")
        self.assertIn("迁移", tiers, "U8 迁移变式")
        self.assertIn("延伸", tiers, "K4 跨册延伸")
        cross = pkg["lesson_ref"].get("cross_book_refs", [])
        self.assertTrue(any(c["card_id"] == "CARD-B1-REC-01" for c in cross), "延伸题应有跨册边")


class SyntheticPackageTest(unittest.TestCase):
    def setUp(self):
        self.pkg = real_package()

    def test_missing_closed_retrieval_detected(self):
        for item in self.pkg["items"]:
            if item["retrieval_mode"] == "闭卷检索":
                item["retrieval_mode"] = "开卷回证"
        errors, _ = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("闭卷检索" in e for e in errors))

    def test_missing_transfer_detected(self):
        self.pkg["items"] = [i for i in self.pkg["items"] if i["tier"] != "迁移"]
        errors, _ = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("迁移" in e for e in errors))

    def test_time_budget_exceeded(self):
        for item in self.pkg["items"]:
            item["time_budget_minutes"] = 30
        self.pkg["tiers"] = {"巩固": "必做"}
        errors, _ = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("上限" in e for e in errors))

    def test_unknown_kp_detected(self):
        self.pkg["items"][0]["kp_ids"] = ["KP-CARD-XX-U99-99-999"]
        errors, _ = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("未解析到知识卡" in e for e in errors))

    def test_uncovered_scope_kp_detected(self):
        self.pkg["kp_scope"]["kp_ids"].append("KP-CARD-X3-U01-01-009")
        errors, _ = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("既无作业覆盖也无 defer" in e for e in errors))

    def test_bad_page_ref_detected(self):
        self.pkg["items"][0]["page_refs"] = ["Z999"]
        errors, _ = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("page_ref 不在课程数据中" in e for e in errors))

    def test_frontstage_leak_in_prompt_detected(self):
        self.pkg["items"][0]["prompt"] = "本页意图：建立理解链（学生角色测试）"
        errors, _ = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("后台词" in e for e in errors))

    def test_missing_normal_path_detected(self):
        self.pkg["items"][0]["normal_path"] = ""
        errors, _ = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("normal_path" in e for e in errors))

    def test_missing_claim_boundary_warned(self):
        self.pkg["claim_boundary"] = "没有边界声明"
        _, warnings = validate(self.pkg, REAL_PACKAGE)
        self.assertTrue(any("两本账" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
