# -*- coding: utf-8 -*-
"""catalog 生成器测试（最小版）。"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_catalog", ROOT / "scripts/build_catalog.py")
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)


class BuildCatalogTest(unittest.TestCase):
    def test_real_sources_build(self):
        rows, errors = bc.build()
        self.assertEqual(errors, [])
        self.assertGreater(len(rows), 100)  # 120 账本 + 题库/蓝图/teaching/手册

    def test_all_paths_resolve(self):
        rows, _ = bc.build()
        for r in rows:
            self.assertTrue((ROOT / r["path"]).exists(), f"{r['id']} 路径悬空: {r['path']}")

    def test_ids_unique_after_dedup(self):
        rows, _ = bc.build()
        ids = [r["id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields(self):
        rows, _ = bc.build()
        for r in rows:
            for field in ("id", "type", "title", "path", "updated", "summary"):
                self.assertIn(field, r)
            self.assertIn("last_consumed", r)

    def test_book_tag_added_for_cards(self):
        rows, _ = bc.build()
        cards = [r for r in rows if r["id"].startswith("CARD-X3")]
        self.assertTrue(cards)
        for r in cards:
            self.assertIn("选择性必修下册", r["tags"])

    def test_item_bank_rows_carry_type_tag(self):
        rows, _ = bc.build()
        items = [r for r in rows if r["type"] == "exam_item"]
        self.assertGreaterEqual(len(items), 7)
        m0 = [r for r in items if "M0未映射" in r["tags"]]
        self.assertTrue(m0, "candidate_only 条目应带 M0未映射 标签")

    def test_manuals_registered(self):
        rows, _ = bc.build()
        manuals = {r["id"] for r in rows if r["type"] == "manual"}
        self.assertTrue({"MANUAL-S0", "MANUAL-S4", "MANUAL-S9"} <= manuals)


if __name__ == "__main__":
    unittest.main()
