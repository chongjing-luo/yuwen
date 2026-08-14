#!/usr/bin/env python3
"""Acquire the complete 360/Qiqiwenku preview as an isolated candidate snapshot.

The source is deliberately kept out of the main answer index.  The browser
context is required because the preview API rejects bare HTTP clients.
"""

from __future__ import annotations

import hashlib
import json
import base64
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
DOC_ID = "c3cbdc68ef52be938ea746f39e9a3f84"
SOURCE_URL = f"https://wenku.so.com/d/{DOC_ID}"
PARTNER_URL = "https://www.qiqiwenku.com/docx/64926719.html"
OUT = ROOT / "Data/reference/gaokao/external/2013_qiqiwenku_answer"
SOURCE_ID = "SRC-GK-2013-SC-QIQIWENKU-ANSWER"
ARTIFACT_ID = "ART-GK-2013-SC-QIQIWENKU-ANSWER"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now_cn() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def parse_jsonp(text: str) -> dict:
    match = re.match(r"^[^(]+\((.*)\)\s*;?\s*$", text, re.S)
    return json.loads(match.group(1) if match else text)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    acquired_at = now_cn()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox"],
        )
        page = browser.new_page()
        page.goto(SOURCE_URL, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(3_000)
        page_html = page.content().encode("utf-8")
        (OUT / "source.html").write_bytes(page_html)

        # The first ten CDN previews are embedded in the 360 page, while the
        # partner preview exposes the complete 29-page document through a
        # JSONP endpoint.  Use the partner's own browser context so its token
        # decryption function (EiePQRNA) is available without reimplementing
        # the obfuscated protocol.
        partner = browser.new_page()
        partner.goto(PARTNER_URL, wait_until="domcontentloaded", timeout=60_000)
        partner.wait_for_timeout(5_000)
        partner_html = partner.content().encode("utf-8")
        (OUT / "partner_source.html").write_bytes(partner_html)
        doc_key = partner.locator("#DocID").input_value()
        page_count = int(partner.locator("#page").input_value())
        request = partner.request
        pn_url = (
            f"https://view.qiqiwenku.com/home/Pn?id={doc_key}&ft=.docx&pn={page_count}&callback=x"
        )
        pn = parse_jsonp(request.get(pn_url, timeout=60_000).text())
        furl = pn.get("nextPageStr")
        if not furl:
            browser.close()
            raise RuntimeError("partner preview did not return a continuation token")
        trt = 0
        chunks: list[dict[str, object]] = []
        pages_seen = 0
        chunk_number = 0
        while furl and pages_seen < page_count:
            chunk_number += 1
            data = None
            for _attempt in range(8):
                api_url = (
                    "https://view.qiqiwenku.com/home/Indexqiqipdf?"
                    f"from=pc_{doc_key}&trt={trt}&furl={furl}&callback=x"
                )
                data = parse_jsonp(request.get(api_url, timeout=60_000).text())
                if data.get("sid"):
                    break
                # The service occasionally responds with `ing-send` while
                # preparing the next three-page chunk; retry the same token.
                time.sleep(1)
                trt = data.get("trt", trt)
            if not data or not data.get("sid"):
                browser.close()
                raise RuntimeError(f"partner preview chunk {chunk_number} unavailable")
            body = base64.b64decode(data["sid"])
            filename = f"preview_chunk_{chunk_number:02d}.pdf"
            (OUT / filename).write_bytes(body)
            chunk_pages = min(3, page_count - pages_seen)
            chunks.append(
                {
                    "chunk": chunk_number,
                    "page_start": pages_seen + 1,
                    "page_end": pages_seen + chunk_pages,
                    "filename": filename,
                    "byte_size": len(body),
                    "sha256": sha256_bytes(body),
                    "htkn": data.get("htkn"),
                }
            )
            pages_seen += chunk_pages
            if not data.get("next"):
                break
            furl = partner.evaluate("([token, secret]) => EiePQRNA(token, secret)", [data["next"], data["s"]])
            trt = data.get("trt", 0)
        partner.close()
        browser.close()
        if pages_seen != page_count:
            raise RuntimeError(f"partner preview returned {pages_seen}/{page_count} pages")
        browser.close()

    (OUT / "preview_chunks.json").write_text(
        json.dumps({"doc_id": doc_key, "page_count": page_count, "chunks": chunks}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    import subprocess

    subprocess.run(
        ["pdfunite", *[str(OUT / c["filename"]) for c in chunks], str(OUT / "full_preview.pdf")],
        check=True,
    )
    subprocess.run(["pdftotext", "-layout", str(OUT / "full_preview.pdf"), str(OUT / "full_preview.txt")], check=True)
    full_pdf = (OUT / "full_preview.pdf").read_bytes()
    page_urls_bytes = (OUT / "preview_chunks.json").read_bytes()
    manifest = {
        "schema_version": "gaokao-external-candidate-acquisition-0.1",
        "source_id": SOURCE_ID,
        "artifact_id": ARTIFACT_ID,
        "exam_id": "GK-SC-2013",
        "document_role": "answer",
        "candidate_status": "acquired_unverified",
        "source_level": "S3",
        "publisher_or_channel": "360文库转链/齐齐文库",
        "source_url": SOURCE_URL,
        "partner_url": PARTNER_URL,
        "doc_id": DOC_ID,
        "raw_id": "64926719",
        "upload_time": "2023-02-28",
        "page_count": page_count,
        "acquired_at": acquired_at,
        "source_html": "Data/reference/gaokao/external/2013_qiqiwenku_answer/source.html",
        "source_html_sha256": sha256_bytes(page_html),
        "partner_source_html": "Data/reference/gaokao/external/2013_qiqiwenku_answer/partner_source.html",
        "partner_source_html_sha256": sha256_bytes(partner_html),
        "preview_chunks": "Data/reference/gaokao/external/2013_qiqiwenku_answer/preview_chunks.json",
        "preview_chunks_sha256": sha256_bytes(page_urls_bytes),
        "chunks": chunks,
        "full_preview_pdf": "Data/reference/gaokao/external/2013_qiqiwenku_answer/full_preview.pdf",
        "full_preview_pdf_sha256": sha256_bytes(full_pdf),
        "full_preview_text": "Data/reference/gaokao/external/2013_qiqiwenku_answer/full_preview.txt",
        "authority_gate": "unverified_third_party_candidate",
        "scoring_gate": "not_available_as_official",
        "main_answer_index_mutated": False,
        "notes": [
            "第三方文库材料；上传者、转链方与命题机构无官方隶属证据。",
            "完整预览页仅作为可追溯候选快照，不据此生成官方答案或评分标准。",
            "页面图像可能包含水印；尚未完成逐题人工转录与独立二审。",
        ],
    }
    (OUT / "acquisition_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    registry_entry = {
        "source_id": SOURCE_ID,
        "artifact_id": ARTIFACT_ID,
        "source_kind": "gaokao_answer_candidate",
        "document_role": "answer",
        "source_level": "S3",
        "metadata_status": "acquired_unverified",
        "publisher_or_channel": "360文库转链/齐齐文库",
        "title": "2013年四川高考语文试题答案（齐齐文库第三方预览）",
        "scope": "四川省自主命题",
        "original_url": SOURCE_URL,
        "partner_url": PARTNER_URL,
        "artifact_path": "Data/reference/gaokao/external/2013_qiqiwenku_answer",
        "artifact_sha256": None,
        "page_count": page_count,
        "authenticity_status": "unverified_third_party_reprint",
        "status": "acquired_candidate_only",
        "is_canonical": False,
        "main_answer_index_mutated": False,
    }
    (OUT / "registry_entry.json").write_text(
        json.dumps(registry_entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"out": str(OUT), "pages": page_count, "chunks": len(chunks), "source_id": SOURCE_ID}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
