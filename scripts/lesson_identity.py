"""Shared LES-ID format and one-ID/one-course resolution checks."""
from __future__ import annotations

import json
import re
from pathlib import Path

LESSON_ID_PATTERN = re.compile(
    r"^LES-(?:(?:B1|B2|X1|X2|X3|REC)-[A-Z0-9]+-\d{2}|TEST-\d{2})$"
)
LESSON_IDENTITY_FILENAMES = {
    "lesson.json",
    "evidence_manifest.json",
    "lesson_plan_candidate.json",
    "lesson_plan_lock.json",
}


def course_dir_for_identity(path: Path) -> Path:
    return path.parent.parent.resolve() if path.parent.name == "_meta" else path.parent.resolve()


def resolve_metadata_course(
    source_path: Path,
    root: Path,
    *,
    required_name: str,
    label: str,
    errors: list[str],
) -> Path | None:
    resolved = (source_path if source_path.is_absolute() else root / source_path).resolve()
    expected_tree = (root / "work/teaching").resolve()
    try:
        resolved.relative_to(expected_tree)
    except ValueError:
        errors.append(f"{label}必须位于课程目录的_meta并使用规定文件名")
        return None
    if resolved.name != required_name or resolved.parent.name != "_meta":
        errors.append(f"{label}必须位于课程目录的_meta并使用规定文件名")
        return None
    return resolved.parent.parent


def check_lesson_id_registry(
    lesson_id: str,
    course_dir: Path | None,
    root: Path,
    errors: list[str],
) -> None:
    """Enforce the registered LES ID -> one course directory rule."""
    if not lesson_id or course_dir is None:
        return
    teaching_root = root / "work/teaching"
    if not teaching_root.is_dir():
        return

    ids_by_course: dict[Path, set[str]] = {}
    courses_by_id: dict[str, set[Path]] = {}
    for identity_path in teaching_root.rglob("*.json"):
        if identity_path.name not in LESSON_IDENTITY_FILENAMES:
            continue
        try:
            payload = json.loads(identity_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        registered_id = payload.get("lesson_id")
        if not isinstance(registered_id, str) or not registered_id.strip():
            continue
        registered_id = registered_id.strip()
        registered_course = course_dir_for_identity(identity_path)
        ids_by_course.setdefault(registered_course, set()).add(registered_id)
        courses_by_id.setdefault(registered_id, set()).add(registered_course)

    current_course = course_dir.resolve()
    resolved_courses = courses_by_id.get(lesson_id, set()) | {current_course}
    if len(resolved_courses) > 1:
        root_resolved = root.resolve()
        relative_courses = []
        for path in sorted(resolved_courses):
            try:
                relative_courses.append(str(path.relative_to(root_resolved)))
            except ValueError:
                relative_courses.append(str(path))
        errors.append(f"lesson_id解析到多个课程目录: {lesson_id} -> {relative_courses}")
    course_ids = ids_by_course.get(current_course, set()) | {lesson_id}
    if len(course_ids) > 1:
        errors.append(f"同一课程目录登记了多个lesson_id: {sorted(course_ids)}")
