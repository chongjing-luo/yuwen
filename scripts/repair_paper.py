#!/usr/bin/env python3
"""错版卷修复：对指定卷的全部不同 SHA 空白候选逐一 MinerU 验标题，选正确者。
全不匹配则删除 PAPER 目录并在 EXMAP 标 missing。"""
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

MAP = ROOT / "work/knowledge/exams/papers/EXMAP-V2_版本2文件试卷映射.jsonl"
WORK = ROOT / "Tmp/work/repair"
CN = {"XK1": "新课标一卷", "XK2": "新课标二卷", "XK3": "新课标三卷", "ZJ": "浙江卷",
      "XG1": "新高考一卷", "XG2": "新高考二卷", "JIA": "全国甲卷", "YI": "全国乙卷"}
TITLE_KEYS = {"XK1": ["新课标Ⅰ", "课标Ⅰ", "新课标一"], "XK2": ["新课标Ⅱ", "课标Ⅱ", "新课标二"],
              "ZJ": ["浙江"], "XG1": ["新高考Ⅰ", "新高考一"], "XG2": ["新高考Ⅱ", "新高考二"],
              "JIA": ["全国甲"], "YI": ["全国乙"], "XK3": ["新课标Ⅲ", "课标Ⅲ"]}


def sha_of(p):
    import hashlib
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return h.hexdigest()


def main(code, year):
    rows = [json.loads(l) for l in MAP.read_text(encoding="utf-8").splitlines() if l.strip()]
    cands = [r for r in rows if r.get("paper_code") == code and r.get("year") == year and r.get("kind") == "空白卷"]
    by_sha = {}
    for r in cands:
        s = r.get("sha256") or sha_of(ROOT / r["file"])
        by_sha.setdefault(s, r)
    paper_dir = ROOT / "work/knowledge/exams/papers" / f"PAPER-{code}-{year}_{CN[code]}"
    print(f"{code}-{year}: {len(cands)} 候选 / {len(by_sha)} 不同 SHA")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    staged = []
    for i, (s, r) in enumerate(sorted(by_sha.items(), key=lambda kv: -Path(kv[1]["file"]).stat().st_size)):
        dst = WORK / f"RP-{i}.pdf"
        shutil.copy2(ROOT / r["file"], dst)
        staged.append((dst, s, r))
    bid, _ = bm.submit_batch([str(d) for d, _, _ in staged], f"repair-{code}-{year}")
    if not bid:
        print("提交失败")
        return 1
    results = bm.poll_batch(bid)
    chosen = None
    for (dst, s, r) in staged:
        item = next((x for x in results if x.get("file_name", "").startswith(dst.stem)), None)
        if not item:
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
            head = (out / "full.md").read_text(encoding="utf-8")[:300]
            title = next((l.lstrip("# ").strip() for l in head.splitlines() if l.strip()), "")
            norm = str.maketrans({"Ⅰ": "I", "Ⅱ": "II", "Ⅲ": "III", "１": "1", "２": "2", "３": "3"})
            ok = year in title and any(k.translate(norm) in title.translate(norm) for k in TITLE_KEYS.get(code, []))
            print(f"  {'✅' if ok else '  '} {Path(r['file']).name[:40]} ← {title[:44]}")
            if ok and chosen is None:
                chosen = (r, out / "full.md", title)
        except Exception as e:
            print(f"  err {dst.stem}: {str(e)[:60]}")

    if chosen:
        r, fullmd, title = chosen
        shutil.rmtree(paper_dir, ignore_errors=True)
        raw = paper_dir / "raw"
        raw.mkdir(parents=True)
        dst = raw / f"PAPER-{code}-{year}_{CN[code]}.pdf"
        shutil.copy2(ROOT / r["file"], dst)
        mr = paper_dir / "mineru_result" / dst.stem
        mr.mkdir(parents=True)
        shutil.copy2(fullmd, mr / "full.md")
        (raw / "README.md").write_text(
            f"# PAPER-{code}-{year}（{CN[code]} {year}）\n\n"
            f"原件：`{r['file']}`（SHA256 `{(r.get('sha256') or sha_of(dst))[:16]}…`，渠道：{r.get('channel_province')}）\n"
            f"主件依据：repair_title_match（逐 SHA 验版命中）；证据：{r['evidence']}\n标题：{title[:50]}\n", encoding="utf-8")
        for x in rows:
            if x.get("paper_code") == code and x.get("year") == year and x.get("kind") == "空白卷":
                x["role"] = "primary" if x is r else "duplicate_channel"
                if x is r:
                    x["primary_basis"] = "repair_title_match"
        with open(MAP, "w", encoding="utf-8") as fh:
            for x in rows:
                fh.write(json.dumps(x, ensure_ascii=False) + "\n")
        print(f"✅ {code}-{year} 修复，主件：{Path(r['file']).name}")
        return 0
    else:
        shutil.rmtree(paper_dir, ignore_errors=True)
        for x in rows:
            if x.get("paper_code") == code and x.get("year") == year and x.get("kind") == "空白卷":
                x["role"] = "missing_no_valid_candidate"
        with open(MAP, "w", encoding="utf-8") as fh:
            for x in rows:
                fh.write(json.dumps(x, ensure_ascii=False) + "\n")
        print(f"❌ {code}-{year} 全部候选验版失败 → 判缺件")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
