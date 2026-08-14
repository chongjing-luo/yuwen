#!/usr/bin/env python3
"""Validate the independent 2011--2025 Gaokao reference batch."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data" / "reference" / "gaokao"


def main() -> int:
    manifest = json.loads((BASE / "manifest.json").read_text(encoding="utf-8"))
    rows = manifest.get("records", [])
    errors: list[str] = []
    if len(rows) != 30:
        errors.append(f"manifest records={len(rows)}; expected 30 (15 years × paper/answer)")
    if {r.get("year") for r in rows} != set(range(2011, 2026)):
        errors.append("year coverage is not exactly 2011--2025")
    acquired = [r for r in rows if r.get("status") == "acquired"]
    if len(acquired) != 20:
        errors.append(f"acquired records={len(acquired)}; expected 20 with currently available sources")
    for row in acquired:
        local_pdf = row.get("local_pdf")
        if not local_pdf:
            errors.append(f"{row.get('artifact_id')}: missing local_pdf")
            continue
        path = ROOT / local_pdf
        if not path.exists() or path.read_bytes()[:5] != b"%PDF-":
            errors.append(f"{row.get('artifact_id')}: invalid/missing PDF")
            continue
        info = subprocess.run(["/usr/bin/pdfinfo", str(path)], capture_output=True, text=True, check=True).stdout
        pages = next((int(line.split(":", 1)[1]) for line in info.splitlines() if line.startswith("Pages:")), 0)
        if pages != row.get("pdf_page_count") or not pages:
            errors.append(f"{row.get('artifact_id')}: page count mismatch")
        result_dir = ROOT / (row.get("mineru_result_dir") or "")
        if row.get("mineru_state") != "done" or not (result_dir / "full.md").exists():
            errors.append(f"{row.get('artifact_id')}: missing MinerU result")
        for json_path in result_dir.glob("*.json"):
            try:
                json.loads(json_path.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"{json_path}: invalid JSON ({exc})")
    if errors:
        print("FAILED")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"PASSED: {len(rows)} manifest records; {len(acquired)} acquired PDFs; all MinerU results and JSON valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
