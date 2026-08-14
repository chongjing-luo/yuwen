#!/usr/bin/env python3
"""Merge the eight validated 《氓》 modules without losing speaker notes."""

from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "work" / "备课" / "选择性必修下册" / "氓" / "_v62_stage"
OUTPUT_DIR = STAGE / "full" / "pptx"
OUTPUT = OUTPUT_DIR / "04_氓_V64完整课堂课件_48页逐字稿.pptx"
MANIFEST = OUTPUT_DIR / "full_v64_pptx_manifest.json"

MODULES = [
    (
        "opening",
        STAGE / "opening" / "pptx" / "04_氓_V62导入课堂课件.pptx",
        ["O01", "O02", "O03", "O04", "O05", "O06", "O07", "O08", "O09"],
    ),
    (
        "chapter_1",
        STAGE / "chapter_1" / "pptx" / "04_氓_V62第一章课堂课件.pptx",
        ["C101", "C102", "C103", "C104", "C105"],
    ),
    (
        "chapter_2",
        STAGE / "chapter_2" / "pptx" / "04_氓_V62第二章课堂课件.pptx",
        ["C201", "C202", "C204", "C206"],
    ),
    (
        "chapter_3",
        STAGE / "chapter_3" / "pptx" / "04_氓_V63第三章课堂课件.pptx",
        ["C301", "C302", "C303", "C305", "C306"],
    ),
    (
        "chapter_4",
        STAGE / "chapter_4" / "pptx" / "04_氓_V63第四章课堂课件.pptx",
        ["C401", "C402", "C403", "C404", "C405", "C406"],
    ),
    (
        "chapter_5",
        STAGE / "chapter_5" / "pptx" / "04_氓_V63第五章课堂课件.pptx",
        ["C501", "C502", "C503", "C504", "C505"],
    ),
    (
        "chapter_6",
        STAGE / "chapter_6" / "pptx" / "04_氓_V63第六章课堂课件.pptx",
        ["C601", "C602", "C603", "C604", "C605", "C606"],
    ),
    (
        "synthesis",
        STAGE / "synthesis" / "pptx" / "04_氓_V64全文综合课堂课件.pptx",
        ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08"],
    ),
]

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
SLIDE_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
NOTES_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"
SLIDE_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
NOTES_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def numbered_parts(names: list[str], pattern: str) -> list[str]:
    compiled = re.compile(pattern)
    matches = [name for name in names if compiled.fullmatch(name)]
    return sorted(matches, key=lambda name: int(re.search(r"\d+", Path(name).stem).group()))


def xml_bytes(root: etree._Element) -> bytes:
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def assert_module_shape(module: str, path: Path, page_ids: list[str]) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        slides = numbered_parts(names, r"ppt/slides/slide\d+\.xml")
        notes = numbered_parts(names, r"ppt/notesSlides/notesSlide\d+\.xml")
        if len(slides) != len(page_ids) or len(notes) != len(page_ids):
            raise ValueError(
                f"{module}: expected {len(page_ids)} slides/notes, got {len(slides)}/{len(notes)}"
            )
        binary_parts = [
            name
            for name in names
            if name.startswith(("ppt/media/", "ppt/charts/", "ppt/embeddings/"))
            and not name.endswith("/")
        ]
        if binary_parts:
            raise ValueError(f"{module}: unsupported binary dependencies: {binary_parts}")
        for page_id, note_name in zip(page_ids, notes):
            note_xml = archive.read(note_name).decode("utf-8")
            if page_id not in note_xml or "教师逐字稿" not in note_xml:
                raise ValueError(f"{module}: {note_name} is not bound to {page_id}")


def rewrite_slide_rels(raw: bytes, slide_number: int) -> bytes:
    root = etree.fromstring(raw)
    notes_targets = [
        rel
        for rel in root.findall(f"{{{PKG_REL_NS}}}Relationship")
        if rel.get("Type") == NOTES_REL_TYPE
    ]
    if len(notes_targets) != 1:
        raise ValueError(f"slide {slide_number}: expected one notes relationship")
    notes_targets[0].set("Target", f"../notesSlides/notesSlide{slide_number}.xml")
    return xml_bytes(root)


def rewrite_notes_rels(raw: bytes, slide_number: int) -> bytes:
    root = etree.fromstring(raw)
    slide_targets = [
        rel
        for rel in root.findall(f"{{{PKG_REL_NS}}}Relationship")
        if rel.get("Type") == SLIDE_REL_TYPE
    ]
    if len(slide_targets) != 1:
        raise ValueError(f"notes {slide_number}: expected one slide relationship")
    slide_targets[0].set("Target", f"../slides/slide{slide_number}.xml")
    return xml_bytes(root)


def rewrite_presentation(raw: bytes, page_count: int) -> bytes:
    root = etree.fromstring(raw)
    slide_list = root.find(f"{{{P_NS}}}sldIdLst")
    if slide_list is None:
        raise ValueError("presentation.xml has no slide list")
    slide_list.clear()
    for index in range(1, page_count + 1):
        slide_id = etree.SubElement(slide_list, f"{{{P_NS}}}sldId")
        slide_id.set("id", str(255 + index))
        slide_id.set(f"{{{R_NS}}}id", f"rId{99 + index}")
    return xml_bytes(root)


def rewrite_presentation_rels(raw: bytes, page_count: int) -> bytes:
    root = etree.fromstring(raw)
    for rel in list(root.findall(f"{{{PKG_REL_NS}}}Relationship")):
        if rel.get("Type") == SLIDE_REL_TYPE:
            root.remove(rel)
    for index in range(1, page_count + 1):
        rel = etree.SubElement(root, f"{{{PKG_REL_NS}}}Relationship")
        rel.set("Id", f"rId{99 + index}")
        rel.set("Type", SLIDE_REL_TYPE)
        rel.set("Target", f"slides/slide{index}.xml")
    return xml_bytes(root)


def rewrite_content_types(raw: bytes, page_count: int) -> bytes:
    root = etree.fromstring(raw)
    for override in list(root.findall(f"{{{CT_NS}}}Override")):
        part_name = override.get("PartName", "")
        if re.fullmatch(r"/ppt/(?:slides/slide|notesSlides/notesSlide)\d+\.xml", part_name):
            root.remove(override)
    for index in range(1, page_count + 1):
        slide_override = etree.SubElement(root, f"{{{CT_NS}}}Override")
        slide_override.set("PartName", f"/ppt/slides/slide{index}.xml")
        slide_override.set("ContentType", SLIDE_CONTENT_TYPE)
        notes_override = etree.SubElement(root, f"{{{CT_NS}}}Override")
        notes_override.set("PartName", f"/ppt/notesSlides/notesSlide{index}.xml")
        notes_override.set("ContentType", NOTES_CONTENT_TYPE)
    return xml_bytes(root)


def rewrite_app_properties(raw: bytes, page_count: int) -> bytes:
    root = etree.fromstring(raw)
    for element in root.iter():
        local_name = etree.QName(element).localname
        if local_name in {"Slides", "Notes"}:
            element.text = str(page_count)
    return xml_bytes(root)


def merge() -> dict:
    for module, path, page_ids in MODULES:
        assert_module_shape(module, path, page_ids)

    page_ids = [page_id for _, _, ids in MODULES for page_id in ids]
    if len(page_ids) != 48 or len(set(page_ids)) != 48:
        raise ValueError(f"expected 48 unique page IDs, got {len(page_ids)}/{len(set(page_ids))}")

    base_path = MODULES[0][1]
    with zipfile.ZipFile(base_path) as base_archive:
        base_files = {
            name: base_archive.read(name)
            for name in base_archive.namelist()
            if not name.endswith("/")
        }

    for name in list(base_files):
        if re.fullmatch(
            r"ppt/(?:slides/slide\d+\.xml|slides/_rels/slide\d+\.xml\.rels|"
            r"notesSlides/notesSlide\d+\.xml|notesSlides/_rels/notesSlide\d+\.xml\.rels)",
            name,
        ):
            del base_files[name]

    full_index = 0
    page_manifest = []
    for module, module_path, expected_ids in MODULES:
        with zipfile.ZipFile(module_path) as archive:
            names = archive.namelist()
            slides = numbered_parts(names, r"ppt/slides/slide\d+\.xml")
            slide_rels = numbered_parts(names, r"ppt/slides/_rels/slide\d+\.xml\.rels")
            notes = numbered_parts(names, r"ppt/notesSlides/notesSlide\d+\.xml")
            notes_rels = numbered_parts(names, r"ppt/notesSlides/_rels/notesSlide\d+\.xml\.rels")
            if not (len(slides) == len(slide_rels) == len(notes) == len(notes_rels) == len(expected_ids)):
                raise ValueError(f"{module}: incomplete slide relationship parts")
            for local_index, page_id in enumerate(expected_ids):
                full_index += 1
                base_files[f"ppt/slides/slide{full_index}.xml"] = archive.read(slides[local_index])
                base_files[f"ppt/slides/_rels/slide{full_index}.xml.rels"] = rewrite_slide_rels(
                    archive.read(slide_rels[local_index]), full_index
                )
                base_files[f"ppt/notesSlides/notesSlide{full_index}.xml"] = archive.read(notes[local_index])
                base_files[f"ppt/notesSlides/_rels/notesSlide{full_index}.xml.rels"] = rewrite_notes_rels(
                    archive.read(notes_rels[local_index]), full_index
                )
                page_manifest.append(
                    {
                        "slide": full_index,
                        "page_id": page_id,
                        "module": module,
                        "module_slide": local_index + 1,
                    }
                )

    page_count = len(page_manifest)
    base_files["ppt/presentation.xml"] = rewrite_presentation(
        base_files["ppt/presentation.xml"], page_count
    )
    base_files["ppt/_rels/presentation.xml.rels"] = rewrite_presentation_rels(
        base_files["ppt/_rels/presentation.xml.rels"], page_count
    )
    base_files["[Content_Types].xml"] = rewrite_content_types(
        base_files["[Content_Types].xml"], page_count
    )
    if "docProps/app.xml" in base_files:
        base_files["docProps/app.xml"] = rewrite_app_properties(
            base_files["docProps/app.xml"], page_count
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_suffix(".tmp.pptx")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as output_archive:
        for name, data in base_files.items():
            output_archive.writestr(name, data)
    os.replace(temporary, OUTPUT)

    result = {
        "schema_version": "1.0",
        "lesson": "《氓》",
        "version": "6.4-full-48-page-local-audit-candidate",
        "status": "implementation_candidate_not_classroom_observed",
        "artifact": OUTPUT.relative_to(ROOT).as_posix(),
        "sha256": sha256(OUTPUT),
        "slide_count": page_count,
        "notes_count": page_count,
        "sources": [
            {
                "module": module,
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "slides": len(ids),
            }
            for module, path, ids in MODULES
        ],
        "pages": page_manifest,
        "illustration_policy": "no_character_illustration_until_page_functions_pass_two independent reviews",
    }
    MANIFEST.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    result = merge()
    print(
        f"MENG_V64_FULL_PPTX_OK slides={result['slide_count']} "
        f"notes={result['notes_count']} output={OUTPUT}"
    )


if __name__ == "__main__":
    main()
