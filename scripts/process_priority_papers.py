#!/usr/bin/env python3
"""优先批试卷 MinerU 整理（试卷配方，一次性工具）。

从 EXMAP 取 role=primary 且 kind=空白卷 且 2020+ 全国卷系主件，
按 PAPER-{code}-{year} 组织到 work/knowledge/exams/papers/，
提交 MinerU 并把 full.md 落到各卷 mineru_result/。断点续跑。
"""
import json
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import batch_mineru as bm

MAP = ROOT / "work/knowledge/exams/papers/EXMAP-V2_版本2文件试卷映射.jsonl"
DEST_BASE = ROOT / "work/knowledge/exams/papers"
PRIORITY_CODES = {"XG1", "XG2", "JIA", "YI"}
PRIORITY_FROM = 2020
CN_NAME = {"XG1": "新高考一卷", "XG2": "新高考二卷", "JIA": "全国甲卷", "YI": "全国乙卷"}


def main():
    rows = [json.loads(l) for l in MAP.read_text(encoding="utf-8").splitlines() if l.strip()]
    primaries = [
        r for r in rows
        if r.get("role") == "primary" and r.get("kind") == "空白卷"
        and r.get("paper_code") in PRIORITY_CODES and int(r["year"]) >= PRIORITY_FROM
    ]
    print(f"优先批主件 {len(primaries)} 份")
    staged = []
    for r in sorted(primaries, key=lambda x: (x["paper_code"], x["year"])):
        code, year = r["paper_code"], r["year"]
        paper_dir = DEST_BASE / f"PAPER-{code}-{year}_{CN_NAME[code]}"
        raw = paper_dir / "raw"
        raw.mkdir(parents=True, exist_ok=True)
        dst = raw / f"PAPER-{code}-{year}_{CN_NAME[code]}.pdf"
        if not dst.exists():
            shutil.copy2(ROOT / r["file"], dst)
        if not (raw / "README.md").exists():
            (raw / "README.md").write_text(
                f"# PAPER-{code}-{year}（{CN_NAME[code]} {year}）\n\n"
                f"原件：`{r['file']}`（SHA256 `{r['sha256'][:16]}…`，采集渠道：{r['channel_province']}）\n"
                f"主件依据：{r.get('primary_basis', 'single_channel')}；证据：{r['evidence']}\n", encoding="utf-8")
        if any(paper_dir.glob("mineru_result/*/full.md")):
            print(f"  [skip] {code}-{year} 已解析")
            continue
        staged.append((dst, paper_dir, code, year))
    print(f"待解析 {len(staged)} 份")

    for i in range(0, len(staged), bm.BATCH_SIZE):
        batch = staged[i:i + bm.BATCH_SIZE]
        bid, names = bm.submit_batch([str(d) for d, _, _, _ in batch], "gaokao-priority")
        if not bid:
            print("  ❌ 提交失败")
            continue
        print(f"  batch_id={bid}")
        results = bm.poll_batch(bid)
        ok = fail = 0
        for (dst, paper_dir, code, year) in batch:
            name = dst.stem
            item = next((x for x in results if x.get("file_name", "").startswith(name)), None)
            if not item:
                print(f"  ❌ {code}-{year} 无结果")
                fail += 1
                continue
            out_dir = paper_dir / "mineru_result" / name
            out_dir.mkdir(parents=True, exist_ok=True)
            if (out_dir / "full.md").exists():
                ok += 1
                continue
            try:
                zip_path = Path(tempfile.mkdtemp()) / "r.zip"
                subprocess.run([sys.executable, str(ROOT / "scripts/mineru_client.py"),
                                "download", "--url", item["full_zip_url"], "--out", str(zip_path)],
                               check=True, capture_output=True, timeout=300)
                with zipfile.ZipFile(zip_path) as zf:
                    for member in zf.namelist():
                        if member.endswith("full.md"):
                            shutil.copyfileobj(zf.open(member), open(out_dir / "full.md", "wb"))
                            break
                ok += 1
                print(f"  ✅ {code}-{year} full.md {(out_dir / 'full.md').stat().st_size}B")
            except Exception as e:
                fail += 1
                print(f"  ❌ {code}-{year}: {str(e)[:100]}")
        print(f"  批次完成 ok={ok} fail={fail}")
        time.sleep(3)
    done = sum(1 for _, pd, _, _ in staged if any(pd.glob("mineru_result/*/full.md")))
    print(f"完成 {done}/{len(staged)}")


if __name__ == "__main__":
    main()
