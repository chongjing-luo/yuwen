#!/usr/bin/env python3
"""Download and validate a 2011--2025 Sichuan-relevant Gaokao Chinese corpus.

The EOL pages are treated as third-party archival reproductions (S3), never as
Ministry/examination-authority originals.  Each acquired item keeps:

* the source HTML snapshot;
* a paper/answer PDF rendered from the article's ``TRS_Editor`` content;
* a JSON artifact record with URL, SHA-256, page count and validation checks.

Some early EOL pages contain image-only papers.  The script resolves those
images, including the 2012--2017 legacy image naming conventions, and renders
only the paper body.  Missing/expired source material is recorded as
``blocked`` rather than being silently replaced by an unrelated answer bank.

Usage:
    python scripts/download_gaokao_references.py
    python scripts/download_gaokao_references.py --years 2023 2024 2025
    python scripts/download_gaokao_references.py --no-pdf
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data" / "reference" / "gaokao"
HTML_DIR = BASE / "html"
PDF_DIR = BASE / "pdf"
REG_DIR = BASE / "registry"
USER_AGENT = "YuwenResearch/1.0 (educational research; contact via project README)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})


# Main corpus = 15 complete examination years.  Sichuan's paper is an actual
# provincial paper through 2015 and the indicated national paper afterwards.
RECORDS: list[dict[str, Any]] = [
    {"year": 2011, "paper_code": "SC", "paper_title": "2011四川卷", "sichuan_relation": "四川省自主命题", "question_url": "https://gaokao.eol.cn/huodong/2011gkst/201105/t20110531_624490.shtml", "answer_url": "http://gaokao.eol.cn/2011gkst_11308/20110531/t20110531_624538.shtml", "image_pattern": None},
    {"year": 2012, "paper_code": "SC", "paper_title": "2012四川卷", "sichuan_relation": "四川省自主命题", "question_url": "https://gaokao.eol.cn/huodong/2012gkst/201206/t20120612_790209.shtml", "answer_url": "http://gaokao.eol.cn/2012gkst_9309/20120609/t20120609_788676.shtml", "image_pattern": "https://img.eol.cn/html/g/2012gkst/sc/yw{n}.jpg"},
    {"year": 2013, "paper_code": "SC", "paper_title": "2013四川卷", "sichuan_relation": "四川省自主命题", "question_url": "https://gaokao.eol.cn/shiti/zhenti/201306/t20130609_959730.shtml", "answer_url": "http://gaokao.eol.cn/lnzt_2898/20130609/t20130609_959940.shtml", "image_pattern": "https://img.eol.cn/html/g/2013gkst/sc/yw{n}.jpg"},
    {"year": 2014, "paper_code": "SC", "paper_title": "2014四川卷", "sichuan_relation": "四川省自主命题", "question_url": "https://gaokao.eol.cn/shiti/zhenti/201406/t20140609_1129123.shtml", "answer_url": "http://gaokao.eol.cn/lnzt_2898/20140609/t20140609_1129238.shtml", "image_pattern": "https://img.eol.cn/html/g/2014gkst/sc/yw{n}.jpg"},
    {"year": 2015, "paper_code": "SC", "paper_title": "2015四川卷", "sichuan_relation": "四川省自主命题", "question_url": "https://gaokao.eol.cn/shiti/zhenti/201506/t20150608_1269666.shtml", "answer_url": "https://gaokao.eol.cn/shiti/zhenti/201506/t20150609_1270901.shtml", "image_pattern": "https://img.eol.cn/html/g/2015gkst/sc/yww{n}.jpg"},
    {"year": 2016, "paper_code": "NC3", "paper_title": "2016全国卷Ⅲ", "sichuan_relation": "四川适用全国卷Ⅲ", "question_url": "https://gaokao.eol.cn/shiti/zhenti/201606/t20160609_1410914.shtml", "answer_url": "https://gaokao.eol.cn/shiti/zhenti/201606/t20160609_1410915.shtml", "image_pattern": "https://img.eol.cn/images/ed/gaokao/2016shiti/qgj3/yw{n}.jpg"},
    {"year": 2017, "paper_code": "NC3", "paper_title": "2017全国卷Ⅲ", "sichuan_relation": "四川适用全国卷Ⅲ", "question_url": "https://gaokao.eol.cn/gui_zhou/dongtai/201706/t20170607_1523486.shtml", "answer_url": "https://gaokao.eol.cn/he_bei/dongtai/201706/t20170608_1524427.shtml", "image_pattern": "https://img.eol.cn/images/ed/gaokao/2017shiti/qgj3/j3yw{n}.jpg"},
    {"year": 2018, "paper_code": "NC3", "paper_title": "2018全国卷Ⅲ", "sichuan_relation": "四川适用全国卷Ⅲ", "question_url": "https://gaokao.eol.cn/shiti/zhenti/201806/t20180608_1607248.shtml", "answer_url": None, "image_pattern": None},
    {"year": 2019, "paper_code": "NC3", "paper_title": "2019全国卷Ⅲ", "sichuan_relation": "四川适用全国卷Ⅲ", "question_url": "https://gaokao.eol.cn/shiti/zhenti/201906/t20190609_1662996.shtml", "answer_url": None, "image_pattern": None},
    {"year": 2020, "paper_code": "NC3", "paper_title": "2020全国卷Ⅲ", "sichuan_relation": "四川适用全国卷Ⅲ", "question_url": "https://gaokao.eol.cn/shiti/zhenti/202007/t20200709_1737454.shtml", "answer_url": None, "image_pattern": None},
    {"year": 2021, "paper_code": "NCA", "paper_title": "2021全国甲卷", "sichuan_relation": "四川适用全国甲卷", "question_url": "https://gaokao.eol.cn/shiti/zhenti/202107/t20210730_2141800.shtml", "answer_url": None, "image_pattern": None},
    {"year": 2022, "paper_code": "NCA", "paper_title": "2022全国甲卷", "sichuan_relation": "四川适用全国甲卷", "question_url": "https://gaokao.eol.cn/shiti/zhenti/202206/t20220609_2230737.shtml", "answer_url": None, "image_pattern": None},
    {"year": 2023, "paper_code": "NCA", "paper_title": "2023全国甲卷", "sichuan_relation": "四川适用全国甲卷", "question_url": "https://gaokao.eol.cn/shiti/yw/202306/t20230612_2436312.shtml", "answer_url": "https://gaokao.eol.cn/shiti/yw/202306/t20230613_2439481.shtml", "image_pattern": None},
    {"year": 2024, "paper_code": "NCA", "paper_title": "2024全国甲卷", "sichuan_relation": "四川适用全国甲卷", "question_url": "https://gaokao.eol.cn/shiti/yw/202406/t20240613_2616374.shtml", "answer_url": "https://gaokao.eol.cn/shiti/yw/202406/t20240612_2616080_9.shtml", "image_pattern": None},
    {"year": 2025, "paper_code": "NC2", "paper_title": "2025全国二卷", "sichuan_relation": "四川适用全国二卷", "question_url": "https://gaokao.eol.cn/shiti/yw/202506/t20250612_2674255.shtml", "answer_url": "https://gaokao.eol.cn/shiti/yw/202506/t20250612_2674255_10.shtml", "image_pattern": None},
]


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.part")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def get(url: str) -> requests.Response:
    response = SESSION.get(url, timeout=45, allow_redirects=True)
    response.raise_for_status()
    return response


def fetch_html(url: str, path: Path) -> tuple[str, str]:
    response = get(url)
    atomic_write(path, response.content)
    return response.url, response.content.decode("utf-8", "replace")


def _paper_images(article: BeautifulSoup, base_url: str) -> list[str]:
    urls: list[str] = []
    for img in article.find_all("img"):
        src = img.get("src") or img.get("oldsrc") or img.get("data-original")
        if not src:
            continue
        absolute = urljoin(base_url, src)
        # Keep images belonging to the article; the article container excludes ads.
        if absolute not in urls:
            urls.append(absolute)
    return urls


def _legacy_images(pattern: str) -> list[str]:
    urls = []
    for n in range(1, 40):
        url = pattern.format(n=n)
        try:
            response = get(url)
        except requests.RequestException:
            break
        if not response.headers.get("content-type", "").lower().startswith("image/"):
            break
        urls.append(url)
    return urls


def _rewrite_images(html: str) -> str:
    # Old EOL image URLs are still served over HTTP but are safe to upgrade;
    # Chrome otherwise blocks them when the temporary wrapper is loaded locally.
    return re.sub(r'(?P<q>["\'])http://(?P<url>[^"\']+)(?P=q)', r"\g<q>https://\g<url>\g<q>", html)


def _embed_images(body: str, image_urls: list[str]) -> str:
    """Embed article images so Chrome cannot print before remote assets load."""
    for url in image_urls:
        # The 2018 article includes many third-party inline illustrations from
        # pstatp.com.  They are not the EOL paper carrier and can be slow or
        # expired; retain their original URL for provenance but do not make a
        # batch run wait on them.
        if "pstatp.com" in url:
            continue
        try:
            response = SESSION.get(url, timeout=15, allow_redirects=True)
            response.raise_for_status()
            mime = response.headers.get("content-type", "image/jpeg").split(";", 1)[0]
            if not mime.startswith("image/"):
                continue
            data_uri = f"data:{mime};base64,{base64.b64encode(response.content).decode('ascii')}"
            names = {url, url.replace("https://", "http://")}
            for name in names:
                body = body.replace(name, data_uri)
            # Relative legacy article paths (e.g. ``./W020...jpg``) need a
            # targeted replacement.  Replacing the bare basename globally
            # would corrupt the already embedded URL path.
            basename = url.rsplit("/", 1)[-1]
            for quoted in (f'"./{basename}"', f"'./{basename}'", f'"{basename}"', f"'{basename}'"):
                body = body.replace(quoted, quoted[0] + data_uri + quoted[-1])
        except requests.RequestException:
            # The URL remains in the wrapper and is retained in metadata; a
            # transient CDN failure must not erase provenance.
            continue
    return body


def make_wrapper(article_html: str, image_urls: list[str]) -> str:
    body = _rewrite_images(article_html)
    # If an image is externally linked but absent from the HTML (legacy mode),
    # append it in source order.  The image URLs are preserved in metadata.
    if image_urls:
        existing = set(re.findall(r"(?:src|oldsrc|data-original)=[\"']([^\"']+)", body))
        missing = [u for u in image_urls if u not in existing and u.rsplit("/", 1)[-1] not in body]
        if missing:
            body += "\n" + "\n".join(f'<p class="paper-image"><img src="{u}" /></p>' for u in missing)
    body = _embed_images(body, image_urls)
    return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page { size: A4; margin: 12mm 14mm; }
body { font-family: "Noto Serif CJK SC", "SimSun", serif; font-size: 12pt; line-height: 1.65; color: #111; }
table { border-collapse: collapse; max-width: 100%; } td, th { border: 1px solid #777; padding: 3px; }
img { max-width: 100%; height: auto; display: block; margin: 3mm auto; }
.paper-image { page-break-inside: avoid; text-align: center; }
a { color: #111; text-decoration: none; }
</style></head><body><main class="paper">""" + body + "</main></body></html>"


def render_pdf(html: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="yuwen-gaokao-") as td:
        html_path = Path(td) / "paper.html"
        html_path.write_text(html, encoding="utf-8")
        url = html_path.as_uri()
        tmp = output.with_name(f".{output.name}.part")
        command = [
            "/usr/bin/google-chrome", "--headless", "--no-sandbox", "--disable-gpu",
            "--allow-file-access-from-files", "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=3000",
            f"--print-to-pdf={tmp}", url,
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=180)
        if result.returncode != 0 or not tmp.exists():
            raise RuntimeError(f"Chrome PDF failed: {result.stderr[-500:]}")
        os.replace(tmp, output)


def pdf_checks(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "magic_pdf": path.read_bytes()[:5] == b"%PDF-",
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }
    info = subprocess.run(["/usr/bin/pdfinfo", str(path)], capture_output=True, text=True, check=True)
    match = re.search(r"^Pages:\s+(\d+)", info.stdout, re.MULTILINE)
    result["page_count"] = int(match.group(1)) if match else None
    text_result = subprocess.run(["/usr/bin/pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, check=True)
    extracted = text_result.stdout.strip()
    result["text_chars"] = len(extracted)
    result["text_extractable"] = bool(extracted)
    result["validation_status"] = "verified" if result["magic_pdf"] and result["page_count"] and result["byte_size"] > 1000 else "rejected"
    return result


def fetch_article(record: dict[str, Any], role: str, url: str, html_path: Path) -> dict[str, Any]:
    if not url:
        return {"status": "not_available", "url": None}
    try:
        final_url, raw = fetch_html(url, html_path)
    except Exception as exc:
        return {"status": "blocked", "url": url, "error": str(exc)[:300]}
    soup = BeautifulSoup(raw, "html.parser")
    article = soup.select_one(".TRS_Editor")
    if article is None:
        # Legacy 2011 pages use a different layout.  Do not mistake the whole
        # page's navigation for an exam paper.
        if role == "question" and record.get("year") == 2011:
            return {"status": "blocked", "url": final_url, "error": "article body has expired 20x20 placeholder; no recoverable paper image"}
        article = soup.body or soup
    image_urls = _legacy_images(record["image_pattern"]) if role == "question" and record.get("image_pattern") else _paper_images(article, final_url)
    if role == "question" and record.get("year") == 2011:
        paper_images = [u for u in image_urls if "1307427016" in u]
        if not paper_images:
            return {"status": "blocked", "url": final_url, "error": "source page has no recoverable question image"}
    return {"status": "acquired", "url": final_url, "html": raw, "article_html": str(article), "image_urls": image_urls}


def process_record(record: dict[str, Any], make_pdfs: bool = True) -> list[dict[str, Any]]:
    year = record["year"]
    year_dir = HTML_DIR / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)
    out: list[dict[str, Any]] = []
    for role, url in (("question", record["question_url"]), ("answer", record.get("answer_url"))):
        stem = f"{year}_{record['paper_code']}_{role}"
        html_path = year_dir / f"{role}.html"
        fetched = fetch_article(record, role, url, html_path)
        base = {
            "artifact_id": f"ART-GK-{year}-{record['paper_code']}-{role.upper()}",
            "source_id": f"SRC-GK-{year}-{record['paper_code']}-{role.upper()}",
            "year": year,
            "paper_code": record["paper_code"],
            "paper_title": record["paper_title"],
            "document_role": role,
            "sichuan_relation": record["sichuan_relation"],
            "source_level": "S3",
            "carrier_type": "网页快照/网页渲染PDF",
            "original_url": url,
            "acquired_at": now(),
            "local_html": str(html_path.relative_to(ROOT)) if html_path.exists() else None,
            "html_sha256": sha256(html_path) if html_path.exists() else None,
            "html_byte_size": html_path.stat().st_size if html_path.exists() else None,
            "status": fetched.get("status"),
            "transform": "EOL HTML snapshot; article body rendered by headless Chrome" if fetched.get("status") == "acquired" else None,
            "authenticity_status": "unverified",
        }
        if fetched.get("status") != "acquired":
            base["error"] = fetched.get("error")
            out.append(base)
            print(f"{year} {role}: {fetched.get('status')} — {fetched.get('error', '')}")
            continue
        if make_pdfs:
            pdf_path = PDF_DIR / str(year) / f"{stem}.pdf"
            try:
                render_pdf(make_wrapper(fetched["article_html"], fetched["image_urls"]), pdf_path)
                checks = pdf_checks(pdf_path)
                base.update({
                    "local_pdf": str(pdf_path.relative_to(ROOT)),
                    "pdf": checks,
                    "pdf_page_count": checks.get("page_count"),
                    "sha256": checks.get("sha256"),
                    "byte_size": checks.get("byte_size"),
                })
                print(f"{year} {role}: {checks['validation_status']} p{checks.get('page_count')} {checks.get('byte_size')}B")
            except Exception as exc:
                base.update({"status": "pdf_failed", "error": str(exc)[:300]})
                print(f"{year} {role}: pdf_failed — {exc}")
        base["image_urls"] = fetched["image_urls"]
        out.append(base)
    return out


def write_registries(records: list[dict[str, Any]]) -> None:
    REG_DIR.mkdir(parents=True, exist_ok=True)
    source_rows, artifact_rows, relation_rows = [], [], []
    for row in records:
        source_rows.append({
            "source_id": row["source_id"], "title": f"{row['paper_title']}语文{row['document_role']}",
            "source_kind": "gaokao_paper" if row["document_role"] == "question" else "gaokao_answer",
            "source_level": row["source_level"], "publisher_or_channel": "中国教育在线（第三方转载）",
            "scope": row["sichuan_relation"], "document_role": row["document_role"],
            "canonical_artifact_id": row["artifact_id"], "metadata_status": "acquired" if row["status"] == "acquired" else "blocked",
            "copyright_note": "仅作内部研究；原始内容版权归发布方/命题机构所有",
        })
        artifact_rows.append({
            "artifact_id": row["artifact_id"], "source_id": row["source_id"], "artifact_role": row["document_role"],
            "carrier_type": row["carrier_type"], "local_path": row.get("local_pdf") or row.get("local_html"),
            "original_url": row.get("original_url"), "acquired_at": row.get("acquired_at"),
            "html_sha256": row.get("html_sha256"), "html_byte_size": row.get("html_byte_size"),
            "page_count": row.get("pdf_page_count"), "byte_size": row.get("byte_size"), "sha256": row.get("sha256"),
            "derived_from": row.get("local_html"), "transform": row.get("transform"),
            "authenticity_status": row.get("authenticity_status"), "is_canonical": False,
            "status": row["status"], "error": row.get("error"), "image_urls": row.get("image_urls", []),
        })
        if row["document_role"] == "answer":
            relation_rows.append({"relation_id": f"REL-GK-{row['year']}-{row['paper_code']}-ANSWER", "relation_type": "answer_of", "source_id_from": row["source_id"], "source_id_to": f"SRC-GK-{row['year']}-{row['paper_code']}-QUESTION", "relation_status": "verified" if row["status"] == "acquired" else "unknown"})
    for name, rows in (("sources.jsonl", source_rows), ("artifacts.jsonl", artifact_rows), ("source_relations.jsonl", relation_rows)):
        path = REG_DIR / name
        atomic_write(path, ("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n").encode("utf-8"))


def merge_manifest_rows(new_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge a partial rerun without dropping previously acquired years."""
    existing_path = BASE / "manifest.json"
    existing: dict[tuple[int, str], dict[str, Any]] = {}
    if existing_path.exists():
        try:
            old = json.loads(existing_path.read_text(encoding="utf-8"))
            for row in old.get("records", []):
                existing[(row.get("year"), row.get("document_role"))] = row
        except (OSError, ValueError, TypeError):
            existing = {}
    for row in new_rows:
        key = (row.get("year"), row.get("document_role"))
        prior = existing.get(key, {})
        # Preserve MinerU lineage when a download-only rerun refreshes HTML.
        merged = dict(prior)
        merged.update(row)
        for field in ("local_pdf", "pdf", "pdf_page_count", "sha256", "byte_size", "image_urls"):
            if not row.get(field) and prior.get(field):
                merged[field] = prior[field]
        for field in ("mineru_state", "mineru_result_dir", "mineru_error", "mineru_processed_at"):
            if field not in row and field in prior:
                merged[field] = prior[field]
        existing[key] = merged
    return sorted(existing.values(), key=lambda r: (r.get("year", 0), r.get("document_role", "")))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", type=int, nargs="*", default=None, help="default: 2011--2025")
    parser.add_argument("--no-pdf", action="store_true", help="only save HTML snapshots and metadata")
    args = parser.parse_args()
    selected = set(args.years) if args.years else {r["year"] for r in RECORDS}
    all_rows: list[dict[str, Any]] = []
    for record in RECORDS:
        if record["year"] not in selected:
            continue
        all_rows.extend(process_record(record, make_pdfs=not args.no_pdf))
    merged_rows = merge_manifest_rows(all_rows)
    write_registries(merged_rows)
    manifest = {
        "generated_at": now(), "coverage": "2011--2025", "selected_years": sorted(selected),
        "source_policy": "EOL is S3 third-party reproduction; not an official examination-authority original",
        "records": merged_rows,
    }
    atomic_write(BASE / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8"))
    acquired = sum(1 for r in merged_rows if r["status"] == "acquired")
    print(f"完成：本次 {len(all_rows)} 条；清单累计 {acquired}/{len(merged_rows)} 文档取得；登记 {BASE / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
