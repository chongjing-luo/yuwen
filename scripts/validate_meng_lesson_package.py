#!/usr/bin/env python3
"""Validate the evidence, lesson plan, worksheet, DOCX and PPTX for 《氓》.

The validator checks deterministic package contracts.  It does not claim that
the lesson has been classroom-tested or that qualitative judgments are proven
by machine checks.
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / "work/备课/选择性必修下册/氓"
REPORT = LESSON_DIR / "06_机器校验报告.json"

CONTENT_FILES = {
    "evidence": LESSON_DIR / "01_文本研究与证据档案.md",
    "lesson": LESSON_DIR / "02_氓_2+1课时教案.md",
    "worksheet": LESSON_DIR / "03_学生学习单.md",
    "quality": LESSON_DIR / "05_质量评估与迭代记录.md",
}

FINAL_FILES = {
    "lesson_docx": LESSON_DIR / "02_氓_2+1课时教案.docx",
    "worksheet_docx": LESSON_DIR / "03_学生学习单.docx",
    "slides": LESSON_DIR / "04_氓_课堂教学课件.pptx",
}

SOURCE_FILES = [
    ROOT / "Data/textbook_extract/选择性必修下册/01_U1_导语_课1_氓_离骚.pdf",
    ROOT / "Data/textbook_extract/选择性必修下册/05_U1_单元研习任务.pdf",
    ROOT / "Data/reference/curriculum/普通高中语文课程标准（2017年版2020年修订）_教育部官方版.pdf",
    ROOT / "work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md",
    ROOT / "work/knowledge/选择性必修下册/units/UNIT-X3-U01.md",
]

REQUIRED_QUOTES = [
    "氓之蚩蚩，抱布贸丝",
    "桑之未落，其叶沃若",
    "桑之落矣，其黄而陨",
    "女也不爽，士贰其行",
    "信誓旦旦，不思其反",
    "反是不思，亦已焉哉",
]

FORBIDDEN_CLAIMS = [
    "全诗分三章",
    "中国文学史上第一个说“不”的女性",
    "中国文学史上第一个说'不'的女性",
    "教材要求背诵《氓》全文",
    "官方标准答案",
]


def load_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        errors.append(f"empty file: {path.relative_to(ROOT)}")
    return text


def require(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(f"{label}: missing required text: {needle}")


def numeric_marker(text: str, marker: str, errors: list[str]) -> int | None:
    match = re.search(rf"^{re.escape(marker)}:\s*(\d+)\s*$", text, re.MULTILINE)
    if not match:
        errors.append(f"lesson: missing numeric marker {marker}")
        return None
    return int(match.group(1))


def validate_content(errors: list[str]) -> dict[str, object]:
    texts = {name: load_text(path, errors) for name, path in CONTENT_FILES.items()}
    evidence = texts["evidence"]
    lesson = texts["lesson"]
    worksheet = texts["worksheet"]
    combined_delivery = "\n".join((evidence, lesson, worksheet))

    for source in SOURCE_FILES:
        if not source.exists():
            errors.append(f"missing source: {source.relative_to(ROOT)}")

    for quote in REQUIRED_QUOTES:
        require(evidence, quote, "evidence", errors)

    for claim in FORBIDDEN_CLAIMS:
        if claim in combined_delivery:
            errors.append(f"forbidden claim present: {claim}")

    for label, text in (("evidence", evidence), ("lesson", lesson), ("worksheet", worksheet)):
        if re.search(r"\b(?:TBD|TODO|FIXME)\b|待补|待定", text, re.IGNORECASE):
            errors.append(f"{label}: unresolved placeholder")

    for objective in ("O1", "O2", "O3", "O4", "O5"):
        require(lesson, objective, "lesson", errors)
    for concept in (
        "六章",
        "主张—诗句—形式—判断",
        "可选第三课时",
        "不要求学生公开讲述个人",
        "12分",
    ):
        require(lesson, concept, "lesson", errors)
    for section in (
        "课前诊断",
        "六章叙事证据图",
        "形式—作用证据表",
        "主张—证据卡",
        "微评论",
        "比较矩阵",
    ):
        require(worksheet, section, "worksheet", errors)

    session_1 = numeric_marker(lesson, "CORE_SESSION_1_MINUTES", errors)
    session_2 = numeric_marker(lesson, "CORE_SESSION_2_MINUTES", errors)
    practice = numeric_marker(lesson, "STUDENT_LANGUAGE_PRACTICE_MINUTES", errors)
    if session_1 is not None and session_1 != 45:
        errors.append(f"lesson: session 1 minutes={session_1}, expected=45")
    if session_2 is not None and session_2 != 45:
        errors.append(f"lesson: session 2 minutes={session_2}, expected=45")
    practice_ratio = None
    if practice is not None:
        practice_ratio = practice / 90
        if practice_ratio < 0.55:
            errors.append(f"lesson: student language practice ratio={practice_ratio:.3f}, expected>=0.55")

    return {
        "content_files_present": all(path.exists() and path.stat().st_size > 0 for path in CONTENT_FILES.values()),
        "source_files_present": all(path.exists() for path in SOURCE_FILES),
        "session_1_minutes": session_1,
        "session_2_minutes": session_2,
        "student_language_practice_minutes": practice,
        "student_language_practice_ratio": practice_ratio,
    }


def validate_final(errors: list[str]) -> dict[str, object]:
    result: dict[str, object] = {}
    for name, path in FINAL_FILES.items():
        present = path.exists() and path.stat().st_size > 0
        result[f"{name}_present"] = present
        if not present:
            errors.append(f"missing final file: {path.relative_to(ROOT)}")
            continue
        valid_zip = zipfile.is_zipfile(path)
        result[f"{name}_valid_zip"] = valid_zip
        if not valid_zip:
            errors.append(f"invalid Office package: {path.relative_to(ROOT)}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("content", "final"), default="final")
    args = parser.parse_args()

    errors: list[str] = []
    checks = validate_content(errors)
    if args.stage == "final":
        checks.update(validate_final(errors))

    report = {
        "schema_version": "meng-lesson-package-validation-1.0",
        "stage": args.stage,
        "result": "passed" if not errors else "failed",
        "errors": errors,
        "checks": checks,
        "limits": [
            "Machine checks do not prove classroom effectiveness.",
            "Visual and pedagogical quality require the recorded manual audits.",
        ],
    }
    LESSON_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
