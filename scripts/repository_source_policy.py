#!/usr/bin/env python3
"""Resolve source references under the public/private repository boundary."""

from __future__ import annotations

from pathlib import Path, PurePosixPath


PRIVATE_SOURCE_SUFFIXES = {
    ".pdf",
    ".doc",
    ".docx",
    ".jpg",
    ".jpeg",
    ".png",
    ".rar",
    ".zip",
    ".html",
    ".htm",
    ".webp",
    ".gif",
    ".tif",
    ".tiff",
}


def _normalized_relative_path(relative_path: str | None) -> PurePosixPath | None:
    if not isinstance(relative_path, str) or not relative_path or "\\" in relative_path:
        return None
    path = PurePosixPath(relative_path)
    if path.is_absolute() or ".." in path.parts:
        return None
    return path


def is_private_source_reference(relative_path: str | None) -> bool:
    """Return whether one absent path is an intentionally local-only source."""
    path = _normalized_relative_path(relative_path)
    if path is None:
        return False
    value = path.as_posix()
    suffix = path.suffix.lower()

    if value.startswith("Data/textbook/") and suffix == ".pdf":
        return path.name.startswith("普通高中教科书") or "教师教学用书" in path.name
    if value.startswith("Data/textbook_extract/") and suffix == ".pdf":
        return True
    if value.startswith("Data/reference/teacher_books/") and suffix in {".pdf", ".doc", ".docx"}:
        return True
    if value.startswith("Data/reference/gaokao/"):
        if suffix == ".pdf" or value.startswith("Data/reference/gaokao/html/"):
            return True
        if value.startswith("Data/reference/gaokao/external/") and suffix in PRIVATE_SOURCE_SUFFIXES:
            return True
    if value.startswith("Data/2008-2024·（四川）语文高考真题/") and suffix == ".pdf":
        return True
    if value.startswith("work/knowledge/exams/papers/") and "/raw/" in value:
        return suffix in PRIVATE_SOURCE_SUFFIXES
    if value.startswith("work/knowledge/高考真题整理/") and suffix == ".pdf":
        return True
    return value == "work/teaching/选择性必修中册/记念刘和珍君/记念刘和珍君 用 2026.05.07.pptx"


def reference_is_available(project_root: str | Path, relative_path: str | None) -> bool:
    """Require public files while allowing declared private sources to be absent."""
    path = _normalized_relative_path(relative_path)
    if path is None:
        return False
    root = Path(project_root).resolve()
    target = (root / path.as_posix()).resolve()
    if not target.is_relative_to(root):
        return False
    if target.is_file():
        return True
    return is_private_source_reference(path.as_posix())
