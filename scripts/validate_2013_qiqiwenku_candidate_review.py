#!/usr/bin/env python3
"""Validate the isolated 2013 Qiqiwenku contamination review."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/reference/gaokao/external/2013_qiqiwenku_answer"
MAIN = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/answer_index.jsonl"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_qiqiwenku_candidate_review_20260809.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((BASE / "acquisition_manifest.json").read_text(encoding="utf-8"))
    review_rows = [json.loads(x) for x in (BASE / "candidate_review.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    review = review_rows[0] if len(review_rows) == 1 else {}
    pdfinfo = subprocess.run(["pdfinfo", str(BASE / "full_preview.pdf")], capture_output=True, text=True, check=True).stdout
    pages = next((int(line.split(":", 1)[1].strip()) for line in pdfinfo.splitlines() if line.startswith("Pages:")), None)
    if manifest.get("page_count") != 29 or pages != 29:
        errors.append(f"page count mismatch: manifest={manifest.get('page_count')} pdf={pages}")
    if manifest.get("full_preview_pdf_sha256") != sha256(BASE / "full_preview.pdf"):
        errors.append("full preview PDF hash mismatch")
    for marker in ("jiangsu_answer_heading", "jiangsu_supplement_heading", "questions_beyond_sichuan_scope"):
        if not review.get("markers", {}).get(marker):
            errors.append(f"missing contamination marker: {marker}")
    if review.get("candidate_status") != "blocked_contaminated":
        errors.append("candidate status escaped blocked_contaminated")
    if review.get("scoring_status") != "not_available_as_official":
        errors.append("scoring status escaped conservative boundary")
    if review.get("mapping_level") != "M0" or review.get("kp_id") != "N/A":
        errors.append("mapping gate changed")
    if review.get("decision", "").find("main answer_index") < 0:
        errors.append("review does not explicitly protect main answer index")
    if sha256(MAIN) != "489ba22579be29b0426db2ece4732bc83bc850a903ca8d513c192a510a74289a":
        errors.append("2013 main answer index hash changed")
    registry = (ROOT / "Data/reference/gaokao/registry/sources.jsonl").read_text(encoding="utf-8")
    artifacts = (ROOT / "Data/reference/gaokao/registry/artifacts.jsonl").read_text(encoding="utf-8")
    relations = (ROOT / "Data/reference/gaokao/registry/source_relations.jsonl").read_text(encoding="utf-8")
    for needle, content in [
        ("SRC-GK-2013-SC-QIQIWENKU-ANSWER", registry),
        ("ART-GK-2013-SC-QIQIWENKU-ANSWER", artifacts),
        ("REL-GK-2013-SC-QIQIWENKU-ANSWER", relations),
    ]:
        if needle not in content:
            errors.append(f"registry entry missing: {needle}")
    result = "passed" if not errors else "failed"
    receipt = {
        "schema_version": "exam-qiqiwenku-candidate-review-validation-0.1",
        "result": result,
        "page_count": pages,
        "review_rows": len(review_rows),
        "main_answer_index_sha256": sha256(MAIN),
        "errors": errors,
        "checks": {
            "complete_preview": not errors or (manifest.get("page_count") == 29 and pages == 29),
            "contamination_markers": all(review.get("markers", {}).get(m) for m in ("jiangsu_answer_heading", "jiangsu_supplement_heading", "questions_beyond_sichuan_scope")),
            "blocked_boundary": review.get("candidate_status") == "blocked_contaminated",
            "main_index_unchanged": sha256(MAIN) == "489ba22579be29b0426db2ece4732bc83bc850a903ca8d513c192a510a74289a",
            "registry_traceability": all(n in c for n, c in [("SRC-GK-2013-SC-QIQIWENKU-ANSWER", registry), ("ART-GK-2013-SC-QIQIWENKU-ANSWER", artifacts), ("REL-GK-2013-SC-QIQIWENKU-ANSWER", relations)]),
        },
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
