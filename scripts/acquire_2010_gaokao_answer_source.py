#!/usr/bin/env python3
"""Acquire and normalize the 2010 Sichuan answer attachment.

This is a third-party gaokao.com attachment.  The script preserves the HTML,
RAR and extracted DOC, and writes only a derived UTF-8 text copy.  It never
touches the exam PDFs, MinerU output or the main answer index.
"""
from __future__ import annotations

import hashlib
import subprocess
import tempfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Data/reference/gaokao/external/2010_gaokao_answer"
HTML_URL = "https://www.gaokao.com/e/20100513/4beba0aa4a96d.shtml"
RAR_URL = "https://files.eduuu.com/ohr/2010/06/12/145336_4c132ef00dce2.rar"


def fetch(url: str) -> bytes:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    response.raise_for_status()
    return response.content


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    html = OUT / "source.html"
    rar = OUT / "answer_bundle.rar"
    html.write_bytes(fetch(HTML_URL))
    rar.write_bytes(fetch(RAR_URL))
    with tempfile.TemporaryDirectory(prefix="yuwen_2010_answer_") as tmp:
        extracted = Path(tmp) / "extracted"
        extracted.mkdir()
        subprocess.run(["unrar", "x", "-o+", str(rar), str(extracted)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        docs = sorted(extracted.glob("*.doc"))
        if len(docs) != 1:
            raise RuntimeError(f"expected one DOC, found {len(docs)}")
        doc = OUT / docs[0].name
        doc.write_bytes(docs[0].read_bytes())
        with tempfile.TemporaryDirectory(prefix="yuwen_2010_answer_txt_") as txt_tmp:
            subprocess.run([
                "libreoffice", "--headless", "--convert-to", "txt",
                "--outdir", txt_tmp, str(doc),
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            converted = Path(txt_tmp) / f"{doc.stem}.txt"
            if not converted.exists():
                raise RuntimeError(f"conversion output missing: {converted}")
            (OUT / "answer_source.txt").write_text(
                converted.read_text(encoding="utf-8-sig"), encoding="utf-8"
            )
    print({
        "html": str(html.relative_to(ROOT)),
        "rar": str(rar.relative_to(ROOT)),
        "doc": str(doc.relative_to(ROOT)),
        "text": str((OUT / "answer_source.txt").relative_to(ROOT)),
        "sha256": {p.name: sha(p) for p in (html, rar, doc, OUT / "answer_source.txt")},
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
