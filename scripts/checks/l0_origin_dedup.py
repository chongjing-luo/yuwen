#!/usr/bin/env python3
"""L0-A 专项：MinerU origin.pdf 重序列化副本去重（docs/architecture/L0统一治理专项方案.md 方案 A）。

配对 `Data/2008-2024·（四川）语文高考真题/` 顶层源 PDF 与
`mineru_result/<卷名>/<uuid>_origin.pdf`，做内容级等价校验：
  - 页数一致；
  - 逐页 mediabox 尺寸一致；
  - 逐页文本（去除全部空白后）哈希一致。
双方文本层均为空的页（扫描件）降级为 dims_fallback，默认不删（--allow-scan 才删）。

用法：
  python3 scripts/checks/l0_origin_dedup.py            # 干跑，仅出报告
  python3 scripts/checks/l0_origin_dedup.py --apply    # 删除「equivalent」对的 origin.pdf（git 跟踪，历史可恢复）
报告写入 work/evaluation/reports/l0_origin_dedup.json。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OLD_EXAM_DIR = ROOT / "Data" / "2008-2024·（四川）语文高考真题"
REPORT_PATH = ROOT / "work" / "evaluation" / "reports" / "l0_origin_dedup.json"


def norm_text_hash(page) -> tuple[str, bool]:
    """返回 (规范化文本哈希, 是否有文本层)。"""
    text = (page.extract_text() or "").strip()
    packed = "".join(text.split())
    return hashlib.sha256(packed.encode("utf-8")).hexdigest(), bool(packed)


def compare_papers(src_path: Path, org_path: Path) -> dict:
    src, org = PdfReader(src_path), PdfReader(org_path)
    detail = {
        "source": str(src_path.relative_to(ROOT)),
        "origin": str(org_path.relative_to(ROOT)),
        "origin_bytes": org_path.stat().st_size,
        "src_pages": len(src.pages),
        "org_pages": len(org.pages),
    }
    if len(src.pages) != len(org.pages):
        detail.update(verdict="mismatch", reason=f"页数不一致 {len(src.pages)} vs {len(org.pages)}")
        return detail
    text_mismatch = dim_mismatch = 0
    scan_pages = 0
    for i, (ps, po) in enumerate(zip(src.pages, org.pages)):
        hs, has_s = norm_text_hash(ps)
        ho, has_o = norm_text_hash(po)
        if not has_s and not has_o:
            scan_pages += 1
        elif hs != ho:
            text_mismatch += 1
        ds = (round(float(ps.mediabox.width), 1), round(float(ps.mediabox.height), 1))
        do = (round(float(po.mediabox.width), 1), round(float(po.mediabox.height), 1))
        if ds != do:
            dim_mismatch += 1
    detail.update(scan_pages=scan_pages, text_mismatch=text_mismatch, dim_mismatch=dim_mismatch)
    if text_mismatch or dim_mismatch:
        detail.update(verdict="mismatch", reason=f"文本差异页 {text_mismatch}，尺寸差异页 {dim_mismatch}")
    elif scan_pages and scan_pages == len(src.pages):
        detail.update(verdict="dims_fallback", reason="全卷无文本层（扫描件），仅页数+尺寸可证")
    elif scan_pages:
        detail.update(verdict="partial_scan", reason=f"{scan_pages} 页无文本层（混合卷），其余页等价")
    else:
        detail.update(verdict="equivalent", reason="页数+尺寸+逐页文本全部一致")
    return detail


def build_pairs() -> list[tuple[Path, Path]]:
    pairs = []
    for org in sorted((OLD_EXAM_DIR / "mineru_result").glob("*/*_origin.pdf")):
        src = OLD_EXAM_DIR / f"{org.parent.name}.pdf"
        if src.exists():
            pairs.append((src, org))
    return pairs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="删除 equivalent 对的 origin.pdf")
    parser.add_argument("--allow-scan", action="store_true", help="扫描件降级判定也允许删除（默认保守保留）")
    args = parser.parse_args()

    deletable_verdicts = {"equivalent"} | ({"dims_fallback"} if args.allow_scan else set())
    results, deleted_bytes = [], 0
    for src, org in build_pairs():
        detail = compare_papers(src, org)
        if args.apply and detail["verdict"] in deletable_verdicts:
            deleted_bytes += detail["origin_bytes"]
            detail["deleted"] = True
            org.unlink()
        results.append(detail)

    unpaired_orgs = [
        str(p.relative_to(ROOT))
        for p in (OLD_EXAM_DIR / "mineru_result").glob("*/*_origin.pdf")
        if not (OLD_EXAM_DIR / f"{p.parent.name}.pdf").exists()
    ]
    report = {
        "plan": "L0-A (docs/architecture/L0统一治理专项方案.md)",
        "applied": args.apply,
        "allow_scan": args.allow_scan,
        "pairs": len(results),
        "verdicts": {v: sum(1 for r in results if r["verdict"] == v) for v in {r["verdict"] for r in results}},
        "unpaired_origins": unpaired_orgs,
        "deleted_bytes": deleted_bytes,
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for v, n in report["verdicts"].items():
        print(f"{v}: {n}")
    if unpaired_orgs:
        print(f"无源配对的 origin: {len(unpaired_orgs)}")
    print(f"{'已删除' if args.apply else '可删除'}字节: {deleted_bytes / 1048576:.0f}M")
    print(f"报告 → {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
