#!/usr/bin/env python3
"""L0-A 专项：MinerU origin.pdf 重序列化副本去重（docs/architecture/L0统一治理专项方案.md 方案 A）。

配对 `Data/2008-2024·（四川）语文高考真题/` 顶层源 PDF 与
`mineru_result/<卷名>/<uuid>_origin.pdf`，做内容级等价校验（逐页）：
  - 页数一致；
  - mediabox 尺寸差 < 0.5pt（容差吸收重序列化浮点噪声，如 521.65 vs 521.65002）；
  - 有文本层：规范化文本（去全部空白）哈希一致；
  - 无文本层（扫描页）：页内全部嵌入图像的解码字节哈希一致——扫描页的图像即内容。
图像不可解码的页记 unverifiable，保守保留。

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
DIM_TOLERANCE_PT = 0.5


def norm_text_hash(page) -> tuple[str, bool]:
    """返回 (规范化文本哈希, 是否有文本层)。"""
    text = (page.extract_text() or "").strip()
    packed = "".join(text.split())
    return hashlib.sha256(packed.encode("utf-8")).hexdigest(), bool(packed)


def page_image_hashes(page) -> list[str] | None:
    """页内全部嵌入图像的解码字节哈希；不可解码返回 None（保守不判等）。"""
    try:
        return sorted(hashlib.sha256(im.data).hexdigest() for im in page.images)
    except Exception:
        return None


def dims(page) -> tuple[float, float]:
    box = page.mediabox
    return float(box.width), float(box.height)


def page_verdict(ps, po) -> str:
    """单页判定：ok / mismatch / unverifiable。"""
    ws, hs_ = dims(ps)
    wo, ho = dims(po)
    if abs(ws - wo) >= DIM_TOLERANCE_PT or abs(hs_ - ho) >= DIM_TOLERANCE_PT:
        return "mismatch"
    ts, has_s = norm_text_hash(ps)
    to, has_o = norm_text_hash(po)
    if has_s or has_o:
        return "ok" if ts == to else "mismatch"
    imgs_s, imgs_o = page_image_hashes(ps), page_image_hashes(po)
    if imgs_s is None or imgs_o is None:
        return "unverifiable"
    return "ok" if imgs_s == imgs_o else "mismatch"


def compare_papers(src_path: Path, org_path: Path) -> dict:
    src, org = PdfReader(src_path), PdfReader(org_path)
    detail = {
        "source": str(src_path.relative_to(ROOT)),
        "origin": str(org_path.relative_to(ROOT)),
        "origin_bytes": org_path.stat().st_size,
        "src_pages": len(src.pages),
        "org_pages": len(org.pages),
        "max_dim_diff_pt": 0.0,
        "scan_pages": 0,
    }
    if len(src.pages) != len(org.pages):
        detail.update(verdict="mismatch", reason=f"页数不一致 {len(src.pages)} vs {len(org.pages)}")
        return detail
    counts = {"ok": 0, "mismatch": 0, "unverifiable": 0}
    for ps, po in zip(src.pages, org.pages):
        verdict = page_verdict(ps, po)
        counts[verdict] += 1
        ws, hs_ = dims(ps)
        wo, ho = dims(po)
        detail["max_dim_diff_pt"] = max(detail["max_dim_diff_pt"], abs(ws - wo), abs(hs_ - ho))
        if not (norm_text_hash(ps)[1] or norm_text_hash(po)[1]):
            detail["scan_pages"] += 1
    detail.update(pages=counts)
    if counts["mismatch"]:
        detail.update(verdict="mismatch", reason=f"{counts['mismatch']} 页内容不一致")
    elif counts["unverifiable"]:
        detail.update(verdict="unverifiable", reason=f"{counts['unverifiable']} 页图像不可解码，保守保留")
    else:
        detail.update(verdict="equivalent", reason="逐页文本/图像流哈希一致")
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
    args = parser.parse_args()

    results, deleted_bytes = [], 0
    for src, org in build_pairs():
        detail = compare_papers(src, org)
        if args.apply and detail["verdict"] == "equivalent":
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
        "pairs": len(results),
        "verdicts": {v: sum(1 for r in results if r["verdict"] == v) for v in {r["verdict"] for r in results}},
        "unpaired_origins": unpaired_orgs,
        "deletable_bytes": sum(r["origin_bytes"] for r in results if r["verdict"] == "equivalent"),
        "deleted_bytes": deleted_bytes,
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for v, n in report["verdicts"].items():
        print(f"{v}: {n}")
    if unpaired_orgs:
        print(f"无源配对的 origin: {len(unpaired_orgs)}")
    print(f"{'已删除' if args.apply else '可删除'}字节: {report['deletable_bytes'] / 1048576:.0f}M")
    print(f"报告 → {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
