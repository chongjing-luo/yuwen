#!/usr/bin/env python3
"""Validate the staged V6 opening Markdown package and its hash manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_REVIEW_RECEIPT = PROJECT_ROOT / "scripts" / "meng_v6" / "reviews" / "opening_package.json"

EXPECTED_FILES = {
    "02_氓_V6导入切片教学母版.md",
    "03A_氓_V6导入学习单A_旧故事与初听.md",
    "03B_氓_V6导入学习单B_初听后路标卡.md",
    "04A_氓_V6导入切片逐页无生试讲稿.md",
    "06_氓_V6导入切片课程数据快照.json",
}
EXPECTED_PAGE_IDS = ["N001", "N002", "N003", "N004", "N005", "N007", "N008", "N009", "N010", "N011", "N012"]
BANNED_FRONTSTAGE = ("学生角色", "林晓", "设计意图", "硬门", "接收审计", "理解链", "知识碎片", "页面功能", "不填表", "不概括")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reviewable_package_hash(package_dir: Path) -> str:
    """Bind pedagogical package semantics without hashing self-referential audit IDs."""
    snapshot = json.loads((package_dir / "06_氓_V6导入切片课程数据快照.json").read_text(encoding="utf-8"))
    snapshot.pop("source_audit_sha256", None)
    texts: dict[str, str] = {}
    for name in (
        "02_氓_V6导入切片教学母版.md",
        "03A_氓_V6导入学习单A_旧故事与初听.md",
        "03B_氓_V6导入学习单B_初听后路标卡.md",
        "04A_氓_V6导入切片逐页无生试讲稿.md",
    ):
        value = (package_dir / name).read_text(encoding="utf-8")
        value = re.sub(r'^audit_sha256: "[0-9a-f]{64}"\n', "", value, flags=re.MULTILINE)
        texts[name] = value
    payload = json.dumps(
        {"snapshot": snapshot, "texts": texts}, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(unicodedata.normalize("NFC", payload).encode("utf-8")).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("stage",), default="stage")
    parser.add_argument("--through", choices=("opening",), required=True)
    parser.add_argument("--input", type=Path, required=True)
    return parser.parse_args()


def validate(package_dir: Path) -> list[tuple[str, str]]:
    errors: list[tuple[str, str]] = []
    manifest_path = package_dir / "opening_package_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return [("PACKAGE_MANIFEST_INVALID", str(manifest_path))]
    files = manifest.get("files")
    if not isinstance(files, list) or {item.get("name") for item in files if isinstance(item, dict)} != EXPECTED_FILES:
        errors.append(("PACKAGE_FILE_SET_INVALID", "manifest files do not equal the fixed opening package"))
        files = []
    for item in files:
        target = package_dir / str(item.get("name"))
        if not target.is_file() or sha256(target) != item.get("sha256"):
            errors.append(("PACKAGE_FILE_HASH_MISMATCH", str(target)))
    try:
        review = json.loads(PACKAGE_REVIEW_RECEIPT.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        review = {}
        errors.append(("PACKAGE_REVIEW_RECEIPT_INVALID", str(PACKAGE_REVIEW_RECEIPT)))
    snapshot_path = package_dir / "06_氓_V6导入切片课程数据快照.json"
    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        snapshot = {}
        errors.append(("PACKAGE_SNAPSHOT_INVALID", str(snapshot_path)))
    pages = snapshot.get("pages") if isinstance(snapshot, dict) else None
    if (snapshot.get("page_ids") != EXPECTED_PAGE_IDS or not isinstance(pages, list)
            or [item.get("page_id") for item in pages if isinstance(item, dict)] != EXPECTED_PAGE_IDS
            or snapshot.get("total_minutes") != 29):
        errors.append(("PACKAGE_SNAPSHOT_INVALID", "page IDs/order/time do not match the opening contract"))
        pages = []
    lesson_path = package_dir / "02_氓_V6导入切片教学母版.md"
    worksheet_a_path = package_dir / "03A_氓_V6导入学习单A_旧故事与初听.md"
    worksheet_b_path = package_dir / "03B_氓_V6导入学习单B_初听后路标卡.md"
    script_path = package_dir / "04A_氓_V6导入切片逐页无生试讲稿.md"
    try:
        lesson = lesson_path.read_text(encoding="utf-8")
        worksheet_a = worksheet_a_path.read_text(encoding="utf-8")
        worksheet_b = worksheet_b_path.read_text(encoding="utf-8")
        script = script_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        errors.append(("PACKAGE_MARKDOWN_INVALID", str(package_dir)))
        return errors
    try:
        expected_review_hash = reviewable_package_hash(package_dir)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        expected_review_hash = ""
        errors.append(("PACKAGE_REVIEW_HASH_INVALID", str(package_dir)))
    if (
        review.get("reviewed_package_sha256") != expected_review_hash
        or review.get("status") != "pass"
        or any(review.get(key) != 0 for key in ("p0", "p1", "p2"))
        or review.get("student_reception", {}).get("reviewer") != "student_reception_qa"
        or review.get("visual", {}).get("reviewer") != "ppt_visual_qa"
    ):
        errors.append(("PACKAGE_REVIEW_RECEIPT_STALE", expected_review_hash))
    for page_id in EXPECTED_PAGE_IDS:
        marker = f"<!-- V6_PAGE:{page_id} -->"
        if lesson.count(marker) != 1 or script.count(marker) != 1:
            errors.append(("PACKAGE_PAGE_COVERAGE_INVALID", page_id))
    frontstage = worksheet_a + "\n" + worksheet_b + "\n" + "\n".join(
        str(item.get("student_visible_text", "")) for item in pages if isinstance(item, dict)
    )
    for token in BANNED_FRONTSTAGE:
        if token in frontstage:
            errors.append(("PACKAGE_FRONTSTAGE_LEAK", token))
    required_script_markers = (
        "【承接与场面】", "【教师实际说】", "【动作、等待与走位】", "【现场分支】",
        "【听者同时做什么】", "【留下什么】", "【怎样接下去】",
    )
    for marker in required_script_markers:
        if script.count(marker) != len(EXPECTED_PAGE_IDS):
            errors.append(("PACKAGE_SCRIPT_INCOMPLETE", marker))
    for item in pages:
        if not isinstance(item, dict):
            continue
        script_contract = item.get("script")
        if not isinstance(script_contract, dict):
            errors.append(("PACKAGE_SCRIPT_CONTRACT_INVALID", str(item.get("page_id"))))
            continue
        timeboxes = script_contract.get("timeboxes")
        if (not isinstance(timeboxes, list)
                or sum(box.get("seconds", 0) for box in timeboxes if isinstance(box, dict)) != item.get("minutes", 0) * 60
                or len(script_contract.get("branches", [])) < 2
                or script_contract.get("teacher_spoken") != item.get("channel_split", {}).get("teacher")
                or script_contract.get("evidence_location") != item.get("artifact_location")):
            errors.append(("PACKAGE_SCRIPT_CONTRACT_INVALID", str(item.get("page_id"))))
    page_markers = re.findall(r"<!-- V6_PAGE:(N\d{3}) -->", script)
    if page_markers != EXPECTED_PAGE_IDS:
        errors.append(("PACKAGE_SCRIPT_ORDER_INVALID", ",".join(page_markers)))
    return errors


def main() -> int:
    args = parse_args()
    errors = validate(args.input.resolve())
    if errors:
        for code, detail in errors:
            print(f"{code}: {detail}")
        return 1
    print(f"PACKAGE_OK pages={len(EXPECTED_PAGE_IDS)} input={args.input.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
