#!/usr/bin/env python3
"""Repair only reviewed, derived exam boundaries.

The source PDFs and MinerU ``full.md`` files are deliberately excluded.  This
script trims two known next-section contaminations identified by an
independent PDF review, updates the derived segment provenance/hash fields,
and creates a clean material derivative for 2024 MAT-02.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract"
KP = ROOT / "work/knowledge/高考分析"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_markdown(text: str) -> tuple[str, str, str]:
    # Locate the stable link block rather than splitting every ``---``.  This
    # also repairs an earlier malformed derived header if the script was
    # interrupted after adding a new frontmatter key.
    link_start = text.find("\n\n- 清洗整卷：")
    if link_start < 0:
        raise ValueError("unexpected markdown link block")
    raw_header = text[:link_start]
    link_and_body = text[link_start + 2:]
    separator = link_and_body.find("\n---\n\n")
    if separator < 0:
        raise ValueError("missing link/body separator")
    links = link_and_body[:separator]
    body = link_and_body[separator + len("\n---\n\n"):]
    entries: dict[str, object] = {}
    for line in raw_header.splitlines():
        if not line or line.strip() == "---" or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        try:
            entries[key.strip()] = json.loads(raw.strip())
        except json.JSONDecodeError:
            entries[key.strip()] = raw.strip().strip('"')
    canonical = "---\n" + "\n".join(
        f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in entries.items()
    ) + "\n---\n"
    return canonical, links, body


def replace_frontmatter(header: str, key: str, value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False)
    pattern = rf"(?m)^{re.escape(key)}: .*?$"
    if not re.search(pattern, header):
        # Insert newly derived metadata *inside* the frontmatter.  ``header``
        # is canonical and already ends in a closing ``---``; appending after
        # that delimiter creates a second, non-frontmatter metadata block.
        close_idx = header.rfind("\n---")
        if close_idx >= 0:
            header = header[:close_idx] + f"\n{key}: {encoded}" + header[close_idx:]
        else:
            header = header.rstrip("\n") + f"\n{key}: {encoded}\n"
    else:
        header = re.sub(pattern, f"{key}: {encoded}", header)
    return header


def read_frontmatter(text: str) -> dict[str, object]:
    header = text.split("\n---\n", 1)[0]
    data: dict[str, object] = {}
    for line in header.splitlines()[1:]:
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        try:
            data[key] = json.loads(raw.strip())
        except json.JSONDecodeError:
            data[key] = raw.strip().strip('"')
    return data


def rewrite_segment(path: Path, sentinel: str, *, page_end: int,
                    page_index_end: int, raw_line_end: int,
                    exclude_page_prefix: str, note: str) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    header, links, body = split_markdown(text)
    marker = f"\n{sentinel}"
    fm = read_frontmatter(text)
    if marker in body:
        cleaned_body = body.split(marker, 1)[0].rstrip() + "\n"
    elif fm.get("boundary_status") == "boundary_reviewed_trimmed":
        # Idempotent rerun after a previous successful repair.
        cleaned_body = body.rstrip() + "\n"
    else:
        raise ValueError(f"{path}: boundary sentinel not found: {sentinel}")
    block_ids = [x for x in fm.get("source_block_ids", []) if not str(x).startswith(exclude_page_prefix)]
    bbox = {k: v for k, v in (fm.get("source_bbox_json", {}) or {}).items()
            if not str(k).startswith(exclude_page_prefix)}
    header = replace_frontmatter(header, "source_pdf_page_end", page_end)
    header = replace_frontmatter(header, "source_pdf_page_index_end", page_index_end)
    header = replace_frontmatter(header, "printed_page_no_end", page_end)
    header = replace_frontmatter(header, "source_block_ids", block_ids)
    header = replace_frontmatter(header, "source_bbox_json", bbox)
    header = replace_frontmatter(header, "segment_clean_sha256", sha256_text(cleaned_body.strip()))
    header = replace_frontmatter(header, "boundary_status", "boundary_reviewed_trimmed")
    header = replace_frontmatter(header, "boundary_note", note)
    header = replace_frontmatter(header, "raw_line_end", raw_line_end)
    # ``header`` is already canonical frontmatter including its closing
    # ``---`` line.  Add one blank line before the link block; do not append a
    # second frontmatter delimiter (the earlier implementation did so).
    path.write_text(header + "\n" + links + "\n---\n\n" + cleaned_body, encoding="utf-8")
    return {"path": str(path.relative_to(ROOT)), "clean_sha256": sha256_text(cleaned_body.strip()),
            "source_block_count": len(block_ids), "page_end": page_end}


def create_clean_material(original: Path, output: Path, sentinel: str, *, page_end: int,
                          note: str) -> dict[str, object]:
    text = original.read_text(encoding="utf-8")
    header, links, body = split_markdown(text)
    marker = f"\n{sentinel}"
    fm = read_frontmatter(text)
    if marker in body:
        cleaned_body = body.split(marker, 1)[0].rstrip() + "\n"
    elif fm.get("boundary_status") == "boundary_reviewed_trimmed":
        cleaned_body = body.rstrip() + "\n"
    else:
        raise ValueError(f"{original}: material sentinel not found")
    header = replace_frontmatter(header, "schema_version", "exam-material-clean-0.1")
    header = replace_frontmatter(header, "source_material_path", str(original.relative_to(ROOT)))
    header = replace_frontmatter(header, "source_pdf_page_end", page_end)
    header = replace_frontmatter(header, "material_clean_sha256", sha256_text(cleaned_body.strip()))
    header = replace_frontmatter(header, "raw_material_sha256", fm.get("material_clean_sha256", ""))
    header = replace_frontmatter(header, "cleaning_status", "boundary_reviewed_trimmed")
    header = replace_frontmatter(header, "boundary_status", "boundary_reviewed_trimmed")
    header = replace_frontmatter(header, "boundary_note", note)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(header + "\n" + links + "\n---\n\n" + cleaned_body, encoding="utf-8")
    return {"path": str(output.relative_to(ROOT)), "clean_sha256": sha256_text(cleaned_body.strip()),
            "page_end": page_end}


def update_vertical_nodes(exam_id: str, *, segment_id: str, segment_path: str,
                          clean_sha256: str, material_clean_path: str | None = None,
                          page_end: int | None = None, page_index_end: int | None = None,
                          boundary_note: str | None = None) -> int:
    path = KP / f"{exam_id}-response_nodes_vertical_slice.jsonl"
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    changed = 0
    for row in rows:
        if row.get("source_question_segment") != segment_id:
            continue
        row["segment_clean_sha256"] = clean_sha256
        if material_clean_path:
            row["source_material_clean"] = material_clean_path
        if page_end is not None:
            row["source_pdf_page_index_end"] = page_index_end
            row["boundary_status"] = "boundary_reviewed_trimmed"
            row["boundary_note"] = boundary_note
        actions = row.setdefault("prompt_cleaning_actions", [])
        if boundary_note and boundary_note not in actions:
            actions.append(boundary_note)
        changed += 1
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    results: list[dict[str, object]] = []
    seg_2016 = EXTRACT / "GK-NC3-2016/segments/question/Q006.md"
    note_2016 = "独立 PDF 复核：Q006 正文止于印刷第11页；第12页‘五、语言文字运用’为下一节标题。"
    r2016 = rewrite_segment(seg_2016, "## 五、语言文字运用（20分）", page_end=11,
                            page_index_end=10, raw_line_end=247,
                            exclude_page_prefix="P12-", note=note_2016)
    results.append(r2016)

    seg_2024 = EXTRACT / "GK-NCA-2024/segments/question/Q006.md"
    note_2024 = "独立 PDF 复核：Q006 正文止于印刷第5页首行；第5页后的‘（三）文学类文本’不属于 Q006。"
    r2024 = rewrite_segment(seg_2024, "## （三）文学类文本同读（本题共3小题，15分）", page_end=5,
                            page_index_end=4, raw_line_end=70,
                            exclude_page_prefix="P6-", note=note_2024)
    results.append(r2024)

    original_mat = EXTRACT / "GK-NCA-2024/materials/MAT-2024-SC-02.md"
    clean_mat = EXTRACT / "GK-NCA-2024/materials_clean/MAT-2024-SC-02-clean.md"
    mat_note = "独立 PDF 复核：古建筑材料止于 Q006 末句；文学类文本另归 Q007—Q009，不并入 MAT-02。"
    rmat = create_clean_material(original_mat, clean_mat,
                                 "## （三）文学类文本同读（本题共3小题，15分）",
                                 page_end=5, note=mat_note)
    results.append(rmat)

    n2016 = update_vertical_nodes(
        "GK-NC3-2016", segment_id="Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q006.md",
        segment_path=str(seg_2016.relative_to(ROOT)), clean_sha256=str(r2016["clean_sha256"]),
        material_clean_path="Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/materials_clean/MAT-2016-SC-05-clean.md",
        page_end=11, page_index_end=10, boundary_note=note_2016)
    n2024 = update_vertical_nodes(
        "GK-NCA-2024", segment_id="Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q006.md",
        segment_path=str(seg_2024.relative_to(ROOT)), clean_sha256=str(r2024["clean_sha256"]),
        material_clean_path="Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/materials_clean/MAT-2024-SC-02-clean.md",
        page_end=5, page_index_end=4, boundary_note=note_2024)
    # Q4/Q5 share the same reviewed clean material derivative even though
    # their own question boundaries are already correct.
    path_2024 = KP / "GK-NCA-2024-response_nodes_vertical_slice.jsonl"
    rows = [json.loads(x) for x in path_2024.read_text(encoding="utf-8").splitlines() if x.strip()]
    for row in rows:
        if row.get("question_id") in {4, 5}:
            row["source_material_clean"] = "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/materials_clean/MAT-2024-SC-02-clean.md"
    path_2024.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    results.append({"updated_nodes_2016_q006": n2016, "updated_nodes_2024_q006": n2024})
    print(json.dumps({"status": "repaired_derived_boundaries", "results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
