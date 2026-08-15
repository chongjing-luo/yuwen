#!/usr/bin/env python3
"""转型年（2011/2012 缝隙）身份核验：MinerU 解析后读标题定卷。

对 EXMAP 中 evidence=unresolved_queue 的文件，按（省,年）去重取空白卷一件，
提交 MinerU，读 full.md 首部标题映射卷代码，回写 EXMAP（ocr_title_verified）。
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import batch_mineru as bm

MAP = ROOT / "work/knowledge/高考真题整理/EXMAP-V2_版本2文件试卷映射.jsonl"
WORK = ROOT / "Tmp/work/transition-verify"

TITLE_RULES = [
    ("DG1", ["大纲Ⅰ", "大纲一", "全国Ⅰ", "全国一", "全国卷（Ⅰ）"]),
    ("DG2", ["大纲Ⅱ", "大纲二", "全国Ⅱ", "全国二"]),
    ("XK1", ["新课标Ⅰ", "课标Ⅰ", "新课标一"]),
    ("XK2", ["新课标Ⅱ", "课标Ⅱ", "新课标二", "课标全国Ⅱ"]),
    ("XK3", ["新课标Ⅲ", "课标Ⅲ"]),
    ("XG1", ["新高考Ⅰ", "新高考一"]),
    ("XG2", ["新高考Ⅱ", "新高考二"]),
    ("JIA", ["全国甲"]),
    ("YI", ["全国乙"]),
]
AUTON_TITLES = {
    "北京": "BJ", "上海": "SH", "天津": "TJ", "江苏": "JS", "浙江": "ZJ",
    "山东": "SD", "广东": "GD", "湖北": "HUB", "湖南": "HUN", "福建": "FJ",
    "安徽": "AH", "江西": "JX", "辽宁": "LN", "重庆": "CQ", "四川": "SCZ",
}


def title_code(title: str, year: str, channel: str):
    for code, keys in TITLE_RULES:
        if any(k in title for k in keys):
            return code
    if "新课标" in title:
        return "XK?"  # 未标卷号
    for prov, code in AUTON_TITLES.items():
        if prov in title:
            return code
    return None


def main():
    rows = [json.loads(l) for l in MAP.read_text(encoding="utf-8").splitlines() if l.strip()]
    pending = [r for r in rows if r.get("evidence") == "unresolved_queue" and r.get("kind") == "空白卷"]
    by_key = {}
    for r in pending:
        by_key.setdefault((r["channel_province"], r["year"]), r)
    print(f"转型年空白卷 {len(pending)} 件 →（省,年）{len(by_key)} 组待核验")

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    staged = []
    for (prov, year), r in sorted(by_key.items()):
        dst = WORK / f"TV-{prov}-{year}.pdf"
        shutil.copy2(ROOT / r["file"], dst)
        staged.append((dst, prov, year, r))
    bid, _ = bm.submit_batch([str(d) for d, _, _, _ in staged], "transition-verify")
    if not bid:
        print("❌ 提交失败")
        return 1
    print("batch_id", bid)
    results = bm.poll_batch(bid)

    verdicts = {}
    for (dst, prov, year, r) in staged:
        item = next((x for x in results if x.get("file_name", "").startswith(dst.stem)), None)
        if not item:
            verdicts[(prov, year)] = (None, "no_result")
            continue
        out = WORK / dst.stem
        out.mkdir(exist_ok=True)
        try:
            zip_path = Path(tempfile.mkdtemp()) / "r.zip"
            subprocess.run([sys.executable, str(ROOT / "scripts/mineru_client.py"),
                            "download", "--url", item["full_zip_url"], "--out", str(zip_path)],
                           check=True, capture_output=True, timeout=300)
            with zipfile.ZipFile(zip_path) as zf:
                for m in zf.namelist():
                    if m.endswith("full.md"):
                        shutil.copyfileobj(zf.open(m), open(out / "full.md", "wb"))
                        break
            text = (out / "full.md").read_text(encoding="utf-8")[:300]
            title = next((l.lstrip("# ").strip() for l in text.splitlines() if l.strip()), "")
            code = title_code(title, year, prov)
            verdicts[(prov, year)] = (code, title[:50])
            print(f"  {prov}-{year}: {code} ← {title[:40]}")
        except Exception as e:
            verdicts[(prov, year)] = (None, f"err:{str(e)[:50]}")

    # 回写 EXMAP（同省年全部件：空白+解析）
    for r in rows:
        if r.get("evidence") in ("unresolved_queue",) and r.get("year"):
            v = verdicts.get((r["channel_province"], r["year"]))
            if v and v[0]:
                r["paper_code"] = v[0]
                r["evidence"] = "ocr_title_verified"
                r.pop("needs_verification", None)
                r["verify_note"] = f"标题：{v[1]}"
    with open(MAP, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    resolved = sum(1 for v in verdicts.values() if v[0])
    print(f"核验完成：{resolved}/{len(verdicts)} 组定身份")
    for (prov, year), v in sorted(verdicts.items()):
        if not v[0]:
            print(f"  仍未知: {prov}-{year} ({v[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
