# -*- coding: utf-8 -*-
"""原则注册库校验器测试。"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "checks"))

from validate_principle_registry import (  # noqa: E402
    REGISTRY_PATH,
    build_report,
    load_registry,
    validate,
)

import yaml  # noqa: E402


def real_registry():
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))


class ValidatePrincipleRegistryTest(unittest.TestCase):
    def test_real_registry_passes(self):
        errors, warnings = validate(real_registry())
        self.assertEqual(errors, [], f"注册库应通过自检: {errors}")
        # 全部 20 个节点的强制均已落地（K1/K3/K4 于 Phase C/E 激活）
        self.assertEqual(warnings, [])

    def test_real_registry_shape(self):
        registry = real_registry()
        self.assertEqual(len(registry["nodes"]), 20)
        self.assertEqual(len(registry["principles"]), 112)
        report = build_report(registry)
        # 每个节点都有原则覆盖
        for nid, entry in report["by_node"].items():
            self.assertTrue(entry["principles"], f"节点 {nid} 无原则覆盖")
        # 三个目标都有映射
        for goal, stats in report["by_goal"].items():
            self.assertGreater(stats["principles"], 0)

    def test_duplicate_id_detected(self):
        registry = real_registry()
        registry["principles"].append(copy.deepcopy(registry["principles"][0]))
        errors, _ = validate(registry)
        self.assertTrue(any("ID 重复" in e for e in errors))

    def test_principle_without_node_or_meta_rejected(self):
        registry = real_registry()
        registry["principles"].append(
            {
                "id": "N-99",
                "title": "无节点原则",
                "statement": "测试",
                "domain": "通用",
                "stages": ["S3"],
                "nodes": [],
                "anchor": {"doc": "work/备课基本原则.md", "heading": "### 1. 学生接收优先于教师发送"},
                "enforcement": [{"type": "review_gate", "gate": "测试"}],
            }
        )
        errors, _ = validate(registry)
        self.assertTrue(any("N-99" in e and "机制节点" in e for e in errors))

    def test_meta_requires_justification(self):
        registry = real_registry()
        registry["principles"].append(
            {
                "id": "N-98",
                "title": "meta 无理由",
                "statement": "测试",
                "domain": "通用",
                "stages": ["S3"],
                "nodes": [],
                "role": "meta",
                "anchor": {"doc": "work/备课基本原则.md", "heading": "### 1. 学生接收优先于教师发送"},
                "enforcement": [{"type": "meta", "rule": "测试"}],
            }
        )
        errors, _ = validate(registry)
        self.assertTrue(any("N-98" in e and "justification" in e for e in errors))

    def test_unknown_node_rejected(self):
        registry = real_registry()
        registry["principles"][0]["nodes"] = ["Z9"]
        errors, _ = validate(registry)
        self.assertTrue(any("未定义机制节点" in e for e in errors))

    def test_uncovered_node_rejected(self):
        registry = real_registry()
        registry["nodes"]["K9"] = {"name": "临时节点", "goal": "知识学习"}
        errors, _ = validate(registry)
        self.assertTrue(any("K9" in e and "无任何原则覆盖" in e for e in errors))

    def test_bad_anchor_heading_rejected(self):
        registry = real_registry()
        registry["principles"][0]["anchor"]["heading"] = "### 不存在的标题"
        errors, _ = validate(registry)
        self.assertTrue(any("anchor heading" in e for e in errors))

    def test_missing_checker_rejected(self):
        registry = real_registry()
        registry["principles"][0]["enforcement"].append(
            {"type": "machine_check", "checker": "scripts/does_not_exist.py", "rule": "x"}
        )
        errors, _ = validate(registry)
        self.assertTrue(any("checker 不存在" in e for e in errors))

    def test_planned_checker_exemption(self):
        registry = real_registry()
        registry["principles"][0]["enforcement"].append(
            {"type": "machine_check", "checker": "scripts/does_not_exist.py", "rule": "x", "status": "planned"}
        )
        errors, _ = validate(registry)
        self.assertFalse(any("checker 不存在" in e for e in errors))

    def test_load_registry_is_callable(self):
        registry = load_registry()
        self.assertIn("principles", registry)


if __name__ == "__main__":
    unittest.main()
