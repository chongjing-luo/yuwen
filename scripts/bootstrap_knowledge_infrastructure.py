#!/usr/bin/env python3
"""Build deterministic knowledge-extraction registries from local textbook assets.

Purpose: discover the fixed local textbook corpus and materialize JSONL registries.
Input: one project root containing Data/textbook and Data/textbook_extract.
Output: JSONL files under work/knowledge/_meta.
Side effects: atomically creates registry files; replacement requires --force.
Errors: missing books, count drift, ambiguous page mappings, or existing outputs fail loudly.
Split trigger: add a separate adapter if a non-filesystem source is introduced.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


BOOKS = {
    "B1": {
        "name": "必修上册",
        "audience": "student",
        "master": "普通高中教科书·语文必修 上册.pdf",
        "expected_packages": 27,
        "expected_cards": 20,
        "units": 8,
        "course_type": "必修",
    },
    "B2": {
        "name": "必修下册",
        "audience": "student",
        "master": "普通高中教科书·语文必修 下册.pdf",
        "expected_packages": 27,
        "expected_cards": 19,
        "units": 8,
        "course_type": "必修",
    },
    "X1": {
        "name": "选择性必修上册",
        "audience": "student",
        "master": "普通高中教科书·语文选择性必修 上册.pdf",
        "expected_packages": 18,
        "expected_cards": 13,
        "units": 4,
        "course_type": "选择性必修",
    },
    "X2": {
        "name": "选择性必修中册",
        "audience": "student",
        "master": "普通高中教科书·语文选择性必修 中册.pdf",
        "expected_packages": 20,
        "expected_cards": 14,
        "units": 4,
        "course_type": "选择性必修",
    },
    "X3": {
        "name": "选择性必修下册",
        "audience": "student",
        "master": "普通高中教科书·语文选择性必修 下册.pdf",
        "expected_packages": 21,
        "expected_cards": 15,
        "units": 4,
        "course_type": "选择性必修",
    },
    "TB2": {
        "name": "必修下册教师用书",
        "audience": "teacher",
        "master": "统编本高中语文必修下册 教师教学用书.pdf",
        "expected_packages": 31,
        "expected_cards": 0,
        "units": 8,
        "course_type": "教师参考",
    },
}

BOOK_ORDER = tuple(BOOKS)
EXAMS = (
    ("EXAM-2023-NCA", "2023年全国甲卷"),
    ("EXAM-2024-NCA", "2024年全国甲卷"),
    ("EXAM-2025-NC2", "2025年新课标II卷"),
    ("EXAM-2026-NC2", "2026年新课标II卷"),
)
EXISTING_DELIVERABLES = {
    "CARD-B1-U01-01": "work/knowledge/必修上册/知识点卡_01_U1_沁园春长沙.md",
    "CARD-B1-U01-02": "work/knowledge/必修上册/知识点卡_02_U1_立在地球边上放号_红烛_峨日朵雪峰之侧_致云雀.md",
    "CARD-B1-U01-03": "work/knowledge/必修上册/知识点卡_03_U1_百合花_哦香雪.md",
    "UNIT-B1-U01": "work/knowledge/必修上册/单元图谱_U1.md",
}


def _package_sort_key(path):
    match = re.match(r"^(\d+)_", path.name)
    return (int(match.group(1)) if match else 999, path.name)


def _package_role(filename, audience):
    if audience == "teacher":
        if "前言" in filename:
            return "reference_preface"
        if "导引_目标_意图_指导" in filename:
            return "reference_guide"
        if re.search(r"_L\d+_", filename):
            return "reference_lesson"
        if "整本书阅读" in filename or "信息时代的语文生活" in filename:
            return "reference_special"
        return "reference_unit"
    if "前言" in filename:
        return "preface"
    if "单元学习任务" in filename or "单元研习任务" in filename:
        return "unit_task"
    if "后记" in filename:
        return "afterword"
    if "古诗词诵读" in filename:
        return "recitation"
    if "整本书阅读" in filename:
        return "whole_book"
    if "家乡文化生活" in filename or "信息时代的语文生活" in filename:
        return "activity"
    if "词语积累与词语解释" in filename or "逻辑的力量" in filename:
        return "language_topic"
    return "lesson"


def _unit_number(filename):
    match = re.search(r"_U(\d+)_", filename)
    return int(match.group(1)) if match else None


def _title_from_filename(filename):
    stem = Path(filename).stem
    stem = re.sub(r"^\d+_", "", stem)
    stem = re.sub(r"^U\d+_", "", stem)
    return stem.replace("_", " / ")


def discover_packages(project_root):
    """Return 144 normalized package records from the fixed local corpus."""
    root = Path(project_root).resolve()
    records = []
    for book_code in BOOK_ORDER:
        config = BOOKS[book_code]
        package_dir = root / "Data" / "textbook_extract" / config["name"]
        paths = sorted(package_dir.glob("*.pdf"), key=_package_sort_key)
        if len(paths) != config["expected_packages"]:
            raise ValueError(
                f"{book_code} package count drift: expected "
                f"{config['expected_packages']}, found {len(paths)}"
            )
        for sequence, path in enumerate(paths):
            relative = path.relative_to(root).as_posix()
            records.append(
                {
                    "source_id": f"SRC-PKG-{book_code}-{sequence:03d}",
                    "source_kind": "textbook_package",
                    "book_code": book_code,
                    "book_name": config["name"],
                    "audience": config["audience"],
                    "package_sequence": sequence,
                    "title": _title_from_filename(path.name),
                    "unit_number": _unit_number(path.name),
                    "material_type": _package_role(path.name, config["audience"]),
                    "local_path": relative,
                }
            )
    counts = Counter(record["audience"] for record in records)
    if len(records) != 144 or counts != {"student": 113, "teacher": 31}:
        raise ValueError(f"package inventory invariant failed: total={len(records)}, {dict(counts)}")
    return records


def _deliverable_record(deliverable_id, deliverable_type, title, output_path, **extra):
    legacy_path = EXISTING_DELIVERABLES.get(deliverable_id)
    return {
        "schema_version": "2.0-candidate",
        "deliverable_id": deliverable_id,
        "deliverable_type": deliverable_type,
        "title": title,
        "status": "draft_existing" if legacy_path else "planned",
        "output_path": output_path,
        "legacy_path": legacy_path,
        "source_ids": extra.pop("source_ids", []),
        "upstream_deliverable_ids": extra.pop("upstream_deliverable_ids", []),
        "owner": "",
        "reviewers": [],
        "version": "0.1.0",
        **extra,
    }


def build_deliverables(packages):
    """Return the fixed 120-item dependency-closed deliverable inventory."""
    content_roles = {"lesson", "activity", "whole_book", "language_topic", "recitation"}
    cards = []
    card_by_book_unit = defaultdict(list)
    package_by_book_unit_role = defaultdict(list)

    for package in packages:
        key = (package["book_code"], package["unit_number"], package["material_type"])
        package_by_book_unit_role[key].append(package)

    for book_code in BOOK_ORDER:
        config = BOOKS[book_code]
        if config["audience"] != "student":
            continue
        per_unit_sequence = defaultdict(int)
        book_packages = [item for item in packages if item["book_code"] == book_code]
        for package in book_packages:
            if package["material_type"] not in content_roles:
                continue
            if package["material_type"] == "recitation":
                unit_code = "REC"
            else:
                unit_code = f"U{package['unit_number']:02d}"
            per_unit_sequence[unit_code] += 1
            card_id = f"CARD-{book_code}-{unit_code}-{per_unit_sequence[unit_code]:02d}"
            output_path = f"work/knowledge/{config['name']}/cards/{card_id}.md"
            card = _deliverable_record(
                card_id,
                "knowledge_card",
                package["title"],
                output_path,
                book_code=book_code,
                book_name=config["name"],
                course_type=config["course_type"],
                unit=unit_code,
                material_type=package["material_type"],
                source_ids=[package["source_id"]],
            )
            cards.append(card)
            card_by_book_unit[(book_code, unit_code)].append(card_id)
        found = sum(1 for card in cards if card["book_code"] == book_code)
        if found != config["expected_cards"]:
            raise ValueError(f"{book_code} card count drift: expected {config['expected_cards']}, found {found}")

    unit_graphs = []
    for book_code in BOOK_ORDER:
        config = BOOKS[book_code]
        if config["audience"] != "student":
            continue
        for unit_number in range(1, config["units"] + 1):
            unit_code = f"U{unit_number:02d}"
            unit_id = f"UNIT-{book_code}-{unit_code}"
            task_sources = package_by_book_unit_role[(book_code, unit_number, "unit_task")]
            unit_graphs.append(
                _deliverable_record(
                    unit_id,
                    "unit_graph",
                    f"{config['name']} {unit_code} 单元图谱",
                    f"work/knowledge/{config['name']}/units/{unit_id}.md",
                    book_code=book_code,
                    book_name=config["name"],
                    course_type=config["course_type"],
                    unit=unit_code,
                    source_ids=[item["source_id"] for item in task_sources],
                    upstream_deliverable_ids=card_by_book_unit[(book_code, unit_code)],
                )
            )

    book_summaries = []
    for book_code in BOOK_ORDER:
        config = BOOKS[book_code]
        if config["audience"] != "student":
            continue
        upstream = [item["deliverable_id"] for item in unit_graphs if item["book_code"] == book_code]
        upstream.extend(card_by_book_unit[(book_code, "REC")])
        book_summaries.append(
            _deliverable_record(
                f"BOOK-{book_code}",
                "book_summary",
                f"{config['name']}知识总表",
                f"work/knowledge/册级汇总/BOOK-{book_code}.md",
                book_code=book_code,
                book_name=config["name"],
                course_type=config["course_type"],
                upstream_deliverable_ids=upstream,
            )
        )

    exams = [
        _deliverable_record(
            exam_id,
            "exam_analysis",
            title,
            f"work/knowledge/exams/workbench/{exam_id}.md",
            source_status="missing_official_artifacts",
        )
        for exam_id, title in EXAMS
    ]
    mapping = _deliverable_record(
        "MAP-EXAM-KP",
        "exam_kp_mapping",
        "高考考点映射总表",
        "work/knowledge/exams/_meta/MAP-EXAM-KP.md",
        upstream_deliverable_ids=[item["deliverable_id"] for item in exams + cards],
    )
    global_map = _deliverable_record(
        "GLOBAL-YUWEN",
        "global_map",
        "高中语文知识体系总览",
        "work/knowledge/全局总览/GLOBAL-YUWEN.md",
        upstream_deliverable_ids=[item["deliverable_id"] for item in book_summaries] + [mapping["deliverable_id"]],
    )
    records = cards + unit_graphs + book_summaries + exams + [mapping, global_map]
    if len(records) != 120:
        raise ValueError(f"deliverable inventory invariant failed: {len(records)}")
    return records


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _pdf_page_fingerprints(path):
    """Return normalized text fingerprints with render fallback for empty pages."""
    path = Path(path)
    expected = _pdf_page_count(path)
    text_result = subprocess.run(
        ["/usr/bin/pdftotext", "-layout", str(path), "-"],
        capture_output=True,
        text=True,
    )
    if text_result.returncode != 0:
        raise RuntimeError(f"pdftotext failed for {path.name}: {text_result.stderr[:300]}")
    text_pages = text_result.stdout.split("\f")
    if text_pages and not text_pages[-1].strip():
        text_pages.pop()
    if len(text_pages) != expected:
        raise RuntimeError(f"text page count mismatch for {path.name}: {len(text_pages)} != {expected}")
    normalized = [
        re.sub(r"\s+", " ", unicodedata.normalize("NFC", page)).strip()
        for page in text_pages
    ]
    if all(normalized):
        return ["TEXT:" + hashlib.sha256(page.encode("utf-8")).hexdigest() for page in normalized]

    with tempfile.TemporaryDirectory() as temp_dir:
        prefix = Path(temp_dir) / "page"
        result = subprocess.run(
            ["/usr/bin/pdftoppm", "-gray", "-r", "18", str(path), str(prefix)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"pdftoppm failed for {path.name}: {result.stderr[:300]}")
        pages = sorted(Path(temp_dir).glob("page-*.pgm"))
        if len(pages) != expected:
            raise RuntimeError(f"render count mismatch for {path.name}: {len(pages)} != {expected}")
        return [
            "TEXT:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
            if text
            else "RENDER:" + _sha256(page)
            for text, page in zip(normalized, pages)
        ]


def _pdf_page_count(path):
    result = subprocess.run(
        ["/usr/bin/pdfinfo", str(path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdfinfo failed for {Path(path).name}: {result.stderr[:300]}")
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"pdfinfo did not report pages for {Path(path).name}")
    return int(match.group(1))


def _artifact_record(
    root,
    artifact_id,
    source_id,
    path,
    artifact_role,
    carrier_type,
    *,
    derived_from=None,
    transform=None,
    authenticity_status="verified",
    is_canonical=False,
    original_url=None,
    acquired_at=None,
    repository_visibility="public",
):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "artifact_id": artifact_id,
        "source_id": source_id,
        "artifact_role": artifact_role,
        "carrier_type": carrier_type,
        "local_path": path.resolve().relative_to(Path(root).resolve()).as_posix(),
        "original_url": original_url,
        "acquired_at": acquired_at,
        "page_count": _pdf_page_count(path) if path.suffix.lower() == ".pdf" else None,
        "byte_size": path.stat().st_size,
        "sha256": _sha256(path),
        "derived_from": derived_from,
        "transform": transform,
        "authenticity_status": authenticity_status,
        "verification_scope": "content_and_identity" if is_canonical else "integrity_and_lineage_only",
        "is_canonical": is_canonical,
        "repository_visibility": repository_visibility,
    }


def _derived_artifacts(root, source_id, parent_artifact_id, result_dir, artifact_prefix):
    """Register one MinerU result directory without treating derivatives as canonical."""
    result_dir = Path(result_dir)
    if not result_dir.is_dir():
        raise FileNotFoundError(result_dir)
    records = []
    image_index = 0
    for path in sorted(item for item in result_dir.rglob("*") if item.is_file()):
        name = path.name
        if path.parent.name == "images":
            image_index += 1
            role = "mineru_image"
            suffix = f"IMG-{image_index:03d}"
            carrier = "图像"
        elif name == "full.md":
            role, suffix, carrier = "mineru_markdown", "FULLMD", "OCR衍生"
        elif name == "layout.json":
            role, suffix, carrier = "mineru_layout", "LAYOUT", "计算结果"
        elif name.endswith("_content_list_v2.json"):
            role, suffix, carrier = "mineru_content_v2", "CONTENTV2", "计算结果"
        elif name.endswith("_content_list.json"):
            role, suffix, carrier = "mineru_content", "CONTENT", "计算结果"
        elif name.endswith("_model.json"):
            role, suffix, carrier = "mineru_model", "MODEL", "计算结果"
        elif name.endswith("_origin.pdf"):
            role, suffix, carrier = "mineru_origin_pdf", "ORIGIN", "OCR衍生"
        else:
            raise ValueError(f"unclassified MinerU artifact: {path}")
        records.append(
            _artifact_record(
                root,
                f"{artifact_prefix}-MINERU-{suffix}",
                source_id,
                path,
                role,
                carrier,
                derived_from=parent_artifact_id,
                transform="MinerU v4 pipeline extraction",
                is_canonical=False,
                repository_visibility="private_local" if role == "mineru_origin_pdf" else "public",
            )
        )
    return records


def build_source_registries(project_root, packages):
    """Build Source, Artifact, SourceRelation and verified split-manifest records."""
    root = Path(project_root).resolve()
    sources = []
    artifacts = []
    relations = []
    manifests = []
    master_fingerprints = {}
    next_original_page = {book_code: 1 for book_code in BOOK_ORDER}

    for book_code in BOOK_ORDER:
        config = BOOKS[book_code]
        source_id = f"SRC-MASTER-{book_code}"
        artifact_id = f"ART-MASTER-{book_code}-PDF"
        master_path = root / "Data" / "textbook" / config["master"]
        sources.append(
            {
                "source_id": source_id,
                "source_kind": "textbook_master",
                "title": config["name"],
                "creator_or_issuer": None,
                "publisher_or_channel": None,
                "edition": None,
                "isbn_or_document_number": None,
                "publication_date": None,
                "scope": config["name"],
                "source_level": "S1",
                "copyright_note": "项目内部教学研究使用；遵守原教材版权限制",
                "canonical_artifact_id": artifact_id,
                "metadata_status": "pending_enrichment",
            }
        )
        artifacts.append(
            _artifact_record(
                root,
                artifact_id,
                source_id,
                master_path,
                "master_pdf",
                "正式电子版",
                is_canonical=True,
                repository_visibility="private_local",
            )
        )
        master_fingerprints[book_code] = _pdf_page_fingerprints(master_path)

    for package in packages:
        source_id = package["source_id"]
        artifact_id = source_id.replace("SRC-PKG-", "ART-PKG-") + "-PDF"
        master_source_id = f"SRC-MASTER-{package['book_code']}"
        master_artifact_id = f"ART-MASTER-{package['book_code']}-PDF"
        split_path = root / package["local_path"]
        split_fingerprints = _pdf_page_fingerprints(split_path)
        expected_start = next_original_page[package["book_code"]]
        expected_end = expected_start + len(split_fingerprints) - 1
        master_sequence = master_fingerprints[package["book_code"]]
        if master_sequence[expected_start - 1 : expected_end] == split_fingerprints:
            start, end = expected_start, expected_end
        else:
            try:
                start, end = find_contiguous_range(master_sequence, split_fingerprints)
            except ValueError as exc:
                raise ValueError(f"{source_id} ({package['local_path']}): {exc}") from exc
            if start != expected_start:
                raise ValueError(
                    f"{source_id} breaks contiguous book coverage: expected p{expected_start}, found p{start}"
                )
        next_original_page[package["book_code"]] = end + 1
        sources.append(
            {
                **package,
                "creator_or_issuer": None,
                "publisher_or_channel": None,
                "edition": None,
                "isbn_or_document_number": None,
                "publication_date": None,
                "scope": package["book_name"],
                "source_level": "S1",
                "copyright_note": "规范主教材的已核验切分包，仅供项目内部研究",
                "canonical_artifact_id": artifact_id,
                "metadata_status": "derived_from_verified_master",
            }
        )
        artifacts.append(
            _artifact_record(
                root,
                artifact_id,
                source_id,
                split_path,
                "split_pdf",
                "切分衍生",
                derived_from=master_artifact_id,
                transform=f"contiguous page extraction p{start}-{end}",
                is_canonical=True,
                repository_visibility="private_local",
            )
        )
        result_dir = split_path.parent / "mineru_result" / split_path.stem
        artifacts.extend(
            _derived_artifacts(
                root,
                source_id,
                artifact_id,
                result_dir,
                artifact_id.removesuffix("-PDF"),
            )
        )
        relation_id = f"REL-{source_id.removeprefix('SRC-')}-EXCERPT"
        relations.append(
            {
                "relation_id": relation_id,
                "relation_type": "excerpt_of",
                "source_id_from": source_id,
                "source_id_to": master_source_id,
                "relation_status": "verified",
                "evidence_ids": [],
                "verifier": "bootstrap_knowledge_infrastructure.py",
                "verified_at": "2026-08-06",
            }
        )
        manifests.append(
            {
                "split_id": f"SPLIT-{package['book_code']}-{package['package_sequence']:03d}",
                "source_id": source_id,
                "master_source_id": master_source_id,
                "master_artifact_id": master_artifact_id,
                "split_artifact_id": artifact_id,
                "original_page_start": start,
                "original_page_end": end,
                "split_page_count": len(split_fingerprints),
                "master_page_count": len(master_fingerprints[package["book_code"]]),
                "page_count_check": end - start + 1 == len(split_fingerprints),
                "mapping_verification_status": "verified",
                "verification_method": "normalized_text_with_render_fallback_all_pages_and_sequence",
                "verified_at": "2026-08-06",
            }
        )

    for book_code, next_page in next_original_page.items():
        master_pages = len(master_fingerprints[book_code])
        if next_page != master_pages + 1:
            raise ValueError(
                f"{book_code} split coverage incomplete: covered through p{next_page - 1}, master has {master_pages}"
            )

    curriculum_records = (
        {
            "source_id": "SRC-CURR-2020",
            "title": "普通高中语文课程标准（2017年版2020年修订）",
            "path": root / "Data/reference/curriculum/普通高中语文课程标准（2017年版2020年修订）_教育部官方版.pdf",
            "artifact_id": "ART-CURR-2020-PDF",
            "carrier": "正式电子版",
            "document_number": "教材〔2020〕3号",
            "publication_date": "2020-06-03",
            "url": "https://www.moe.gov.cn/srcsite/A26/s8001/202006/t20200603_462199.html",
        },
        {
            "source_id": "SRC-CURR-2017",
            "title": "普通高中语文课程标准（2017年版）",
            "path": root / "Data/textbook/ZW18-310_普通高中语文课程标准（2017年版）96.pdf",
            "artifact_id": "ART-CURR-2017-PDF",
            "carrier": "纸本扫描件",
            "document_number": None,
            "publication_date": "2017",
            "url": None,
        },
    )
    for curriculum in curriculum_records:
        sources.append(
            {
                "source_id": curriculum["source_id"],
                "source_kind": "curriculum_standard",
                "title": curriculum["title"],
                "creator_or_issuer": "中华人民共和国教育部",
                "publisher_or_channel": "教育部政府门户网站" if curriculum["url"] else None,
                "edition": curriculum["title"],
                "isbn_or_document_number": curriculum["document_number"],
                "publication_date": curriculum["publication_date"],
                "scope": "普通高中语文课程",
                "source_level": "S1",
                "copyright_note": "规范文件，引用须回看官方或已核验载体",
                "canonical_artifact_id": curriculum["artifact_id"],
                "metadata_status": "verified",
            }
        )
        artifacts.append(
            _artifact_record(
                root,
                curriculum["artifact_id"],
                curriculum["source_id"],
                curriculum["path"],
                "curriculum_pdf",
                curriculum["carrier"],
                is_canonical=True,
                original_url=curriculum["url"],
                acquired_at="2026-08-05" if curriculum["url"] else None,
            )
        )

    curriculum_result = (
        root
        / "Data/textbook_extract/普通高中语文课程标准（2017年版2020年修订）/mineru_result"
        / "普通高中语文课程标准（2017年版2020年修订）_教育部官方版"
    )
    artifacts.extend(
        _derived_artifacts(
            root,
            "SRC-CURR-2020",
            "ART-CURR-2020-PDF",
            curriculum_result,
            "ART-CURR-2020",
        )
    )
    relations.extend(
        [
            {
                "relation_id": "REL-CURR-2020-REVISION-2017",
                "relation_type": "revision_of",
                "source_id_from": "SRC-CURR-2020",
                "source_id_to": "SRC-CURR-2017",
                "relation_status": "verified",
                "evidence_ids": [],
                "verifier": "Data/reference/curriculum/README.md",
                "verified_at": "2026-08-05",
            },
            {
                "relation_id": "REL-TB2-B2-EDITION",
                "relation_type": "edition_match",
                "source_id_from": "SRC-MASTER-TB2",
                "source_id_to": "SRC-MASTER-B2",
                "relation_status": "unknown",
                "evidence_ids": [],
                "verifier": None,
                "verified_at": None,
            },
        ]
    )
    return {
        "sources": sources,
        "artifacts": artifacts,
        "source_relations": relations,
        "split_manifest": manifests,
    }


def find_contiguous_range(master_fingerprints, split_fingerprints):
    """Return the unique one-based inclusive range of one fingerprint sequence."""
    width = len(split_fingerprints)
    if width == 0:
        raise ValueError("empty split fingerprint sequence")
    matches = [
        index
        for index in range(len(master_fingerprints) - width + 1)
        if master_fingerprints[index : index + width] == split_fingerprints
    ]
    if not matches:
        raise ValueError("split fingerprints do not occur in master")
    if len(matches) != 1:
        raise ValueError(f"ambiguous split fingerprint range: {len(matches)} matches")
    start = matches[0] + 1
    return start, start + width - 1


def write_jsonl(destination, records, force=False):
    """Atomically write one deterministic UTF-8 JSON object per line."""
    destination = Path(destination)
    if destination.exists() and not force:
        raise FileExistsError(f"refusing to replace existing registry: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    packages = discover_packages(root)
    deliverables = build_deliverables(packages)
    registries = build_source_registries(root, packages)
    meta = root / "work" / "knowledge" / "_meta"
    for name, records in registries.items():
        write_jsonl(meta / f"{name}.jsonl", records, force=args.force)
    write_jsonl(meta / "deliverables.jsonl", deliverables, force=args.force)
    print(
        json.dumps(
            {
                "packages": len(packages),
                "deliverables": len(deliverables),
                "sources": len(registries["sources"]),
                "artifacts": len(registries["artifacts"]),
                "split_mappings": len(registries["split_manifest"]),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
