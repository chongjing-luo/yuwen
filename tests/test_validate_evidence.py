# -*- coding: utf-8 -*-
"""证据层校验器测试（fixtures 均为 synthetic，仅测试用，严禁拷入 _classes）。"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_evidence", ROOT / "scripts/validate_evidence.py")
ve = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ve)

FIX = ROOT / "tests/fixtures/evidence"
HOST_RELEASE_REGISTRY = {
    "schema_version": "external-host-release-registry.v1",
    "events": {
        "HOST-RELEASE-SYNTH-01": {
            "verified_by_host": True,
            "decision": "released",
            "lesson_id": "LES-SYNTH",
            "g4_audit_lock_sha256": "b" * 64,
            "locator": "host-release://synthetic/2099/01",
            "record_sha256": "c" * 64,
        }
    },
}
CURRENT_G4_AUDIT_LOCK = {
    "schema_version": "audit-lock.v1",
    "lesson_id": "LES-SYNTH",
    "status": "awaiting_host_release",
}
CURRENT_G4_AUDIT_LOCK_SHA256 = "b" * 64


def load(name):
    import json
    return [json.loads(l) for l in (FIX / name).read_text(encoding="utf-8").splitlines() if l.strip()]


class GoodRowsTest(unittest.TestCase):
    def test_valid_obs(self):
        errors = ve.validate_row(
            load("obs.jsonl")[0],
            "obs",
            1,
            host_release_registry=HOST_RELEASE_REGISTRY,
            current_g4_audit_lock=CURRENT_G4_AUDIT_LOCK,
            current_g4_audit_lock_sha256=CURRENT_G4_AUDIT_LOCK_SHA256,
        )
        self.assertEqual(errors, [])

    def test_valid_grd(self):
        errors = ve.validate_row(load("grd.jsonl")[0], "grd", 1)
        self.assertEqual(errors, [])

    def test_valid_mr(self):
        for row in load("mr.jsonl"):
            self.assertEqual(ve.validate_row(row, "mr", 1), [])

    def test_valid_ref(self):
        errors = ve.validate_row(load("ref.jsonl")[0], "ref", 1)
        self.assertEqual(errors, [])

    def test_valid_pr(self):
        errors = ve.validate_row(load("pr.jsonl")[0], "pr", 1)
        self.assertEqual(errors, [])


class BadRowsTest(unittest.TestCase):
    def test_bad_obs_detected(self):
        errors = ve.validate_row(load("obs.jsonl")[1], "obs", 2)
        self.assertTrue(any("前缀" in e for e in errors))
        self.assertTrue(any("node 非法" in e for e in errors))
        self.assertTrue(any("hex" in e for e in errors))

    def test_obs_without_verified_host_release_event_is_rejected(self):
        errors = ve.validate_row(load("obs.jsonl")[0], "obs", 1)
        self.assertTrue(any("宿主放行" in e for e in errors))

    def test_obs_cannot_use_registry_hash_without_current_g4_lock(self):
        errors = ve.validate_row(
            load("obs.jsonl")[0],
            "obs",
            1,
            host_release_registry=HOST_RELEASE_REGISTRY,
        )
        self.assertTrue(any("当前G4" in e for e in errors))

    def test_obs_current_g4_lock_hash_must_match_released_hash(self):
        errors = ve.validate_row(
            load("obs.jsonl")[0],
            "obs",
            1,
            host_release_registry=HOST_RELEASE_REGISTRY,
            current_g4_audit_lock=CURRENT_G4_AUDIT_LOCK,
            current_g4_audit_lock_sha256="d" * 64,
        )
        self.assertTrue(any("当前G4锁哈希" in e for e in errors))

    def test_bad_error_type_detected(self):
        errors = ve.validate_row(load("grd.jsonl")[1], "grd", 2)
        self.assertTrue(any("不可操作" in e for e in errors))

    def test_empty_evidence_ref_detected(self):
        errors = ve.validate_row(load("ref.jsonl")[1], "ref", 2)
        self.assertTrue(any("evidence_ref 为空" in e for e in errors))

    def test_bad_pr_detected(self):
        errors = ve.validate_row(load("pr.jsonl")[1], "pr", 2)
        self.assertTrue(any("trigger_evidence" in e for e in errors))
        self.assertTrue(any("change_type" in e for e in errors))

    def test_score_bounds(self):
        row = load("grd.jsonl")[0] | {"score": 3}
        errors = ve.validate_row(row, "grd", 1)
        self.assertTrue(any("score/max_score" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
