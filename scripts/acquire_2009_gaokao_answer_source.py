#!/usr/bin/env python3
"""Acquire independent 2009 Sichuan Chinese exam answer-page snapshots.

This is an acquisition-only step.  It deliberately does not infer or import
answer candidates; the embedded PDF/HTML still needs a separate candidate
review before any question-level rows are generated.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Data/reference/gaokao/external/2009_gaokao_answer"
PAGE_URL = "https://www.gaokao.com/e/20090611/4b8bcafdad195.shtml"
SCDFZ_URL = "https://www.scdfz.org.cn/scyx/scgkt/2000nyh/yw/content_19900"
SCDFZ_PDF_URL = "https://www.scdfz.org.cn/Upload/main/ContentManage/Article/File/201906061738078672.pdf"
UA = "Mozilla/5.0 (compatible; yuwen-research/1.0)"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    response = session.get(PAGE_URL, timeout=30)
    response.raise_for_status()
    html_path = OUT / "source.html"
    html_path.write_bytes(response.content)
    scdfz = session.get(SCDFZ_URL, timeout=30, verify=False)
    scdfz.raise_for_status()
    scdfz_html_path = OUT / "scdfz_source.html"
    scdfz_html_path.write_bytes(scdfz.content)
    scdfz_pdf = session.get(SCDFZ_PDF_URL, timeout=30, verify=False)
    scdfz_pdf.raise_for_status()
    scdfz_pdf_path = OUT / "scdfz_answer.pdf"
    scdfz_pdf_path.write_bytes(scdfz_pdf.content)

    now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    metadata = {
        "schema_version": "exam-answer-source-acquisition-0.1",
        "acquired_at": now,
        "exam_id": "GK-SC-2009",
        "source_url": PAGE_URL,
        "source_title": "2009年高考四川语文试题（含详细答案解析）",
        "publisher_or_channel": "高考网转载（第三方）",
        "source_status": "acquired_unverified_candidate",
        "source_html": {"path": str(html_path.relative_to(ROOT)), "sha256": sha(html_path), "byte_size": html_path.stat().st_size},
        "independent_source": {
            "page_url": SCDFZ_URL,
            "page_path": str(scdfz_html_path.relative_to(ROOT)),
            "page_sha256": sha(scdfz_html_path),
            "page_byte_size": scdfz_html_path.stat().st_size,
            "pdf_url": SCDFZ_PDF_URL,
            "pdf_path": str(scdfz_pdf_path.relative_to(ROOT)),
            "pdf_sha256": sha(scdfz_pdf_path),
            "pdf_byte_size": scdfz_pdf_path.stat().st_size,
            "publisher_or_channel": "四川省地方志工作办公室网站转载（页面注明来源）",
        },
        "candidate_import_status": "not_started_visual_review_required",
        "policy": "仅作第三方候选来源快照；不得据此标记官方答案或评分标准。",
    }
    (OUT / "acquisition_manifest.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "acquired", "output": str(OUT.relative_to(ROOT)), "source_sha256": metadata["source_html"]["sha256"], "independent_pdf_sha256": metadata["independent_source"]["pdf_sha256"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
