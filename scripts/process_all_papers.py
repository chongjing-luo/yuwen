#!/usr/bin/env python3
"""全量试卷批处理（organize 配方）：所有主件空白卷 → PAPER 目录 → MinerU → full.md。

断点续跑（已有 full.md 跳过）；分批提交限流。契约③④由 extract_exam_questions.py
在批后统一执行。
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

MAP = ROOT / "work/knowledge/高考真题整理/EXMAP-V2_版本2文件试卷映射.jsonl"
DEST_BASE = ROOT / "work/knowledge/高考真题整理"

CN_NAME = {
    "DG1": "大纲全国一卷", "DG2": "大纲全国二卷", "DGB": "大纲版2012",
    "XKB": "新课标卷未分版", "XK1": "新课标一卷", "XK2": "新课标二卷", "XK3": "新课标三卷",
    "XG1": "新高考一卷", "XG2": "新高考二卷", "JIA": "全国甲卷", "YI": "全国乙卷",
    "SCZ": "四川自主卷", "BJ": "北京卷", "SH": "上海卷", "TJ": "天津卷", "JS": "江苏卷",
    "ZJ": "浙江卷", "SD": "山东卷", "GD": "广东卷", "HUB": "湖北卷", "HUN": "湖南卷",
    "FJ": "福建卷", "AH": "安徽卷", "JX": "江西卷", "LN": "辽宁卷", "CQ": "重庆卷",
}


def main():
    rows = [json.loads(l) for l in MAP.read_text(encoding="utf-8").splitlines() if l.strip()]
    primaries = [
        r for r in rows
        if r.get("role") == "primary" and r.get("kind") == "空白卷"
        and r.get("paper_code") in CN_NAME and r.get("year") and r["year"].isdigit()
    ]
    print(f"主件空白卷共 {len(primaries)} 份")
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
            import hashlib
            if not r.get("sha256"):
                h = hashlib.sha256()
                with open(dst, "rb") as fh:
                    for chunk in iter(lambda: fh.read(1 << 20), b""):
                        h.update(chunk)
                r["sha256"] = h.hexdigest()
            (raw / "README.md").write_text(
                f"# PAPER-{code}-{year}（{CN_NAME[code]} {year}）\n\n"
                f"原件：`{r['file']}`（SHA256 `{r['sha256'][:16]}…`，采集渠道：{r.get('channel_province', '?')}）\n"
                f"主件依据：{r.get('primary_basis', 'single_channel')}；证据：{r['evidence']}\n", encoding="utf-8")
        if any(paper_dir.glob("mineru_result/*/full.md")):
            continue
        staged.append((dst, paper_dir, code, year))
    print(f"待解析 {len(staged)} 份")

    total_ok = total_fail = 0
    for i in range(0, len(staged), bm.BATCH_SIZE):
        batch = staged[i:i + bm.BATCH_SIZE]
        print(f"--- 批 {i // bm.BATCH_SIZE + 1}/{(len(staged) + bm.BATCH_SIZE - 1) // bm.BATCH_SIZE}（{len(batch)} 份）---", flush=True)
        bid, _ = bm.submit_batch([str(d) for d, _, _, _ in batch], "gaokao-all")
        if not bid:
            print("  ❌ 提交失败，跳过本批")
            total_fail += len(batch)
            continue
        results = bm.poll_batch(bid)
        for (dst, paper_dir, code, year) in batch:
            name = dst.stem
            item = next((x for x in results if x.get("file_name", "").startswith(name)), None)
            if not item:
                print(f"  ❌ {code}-{year} 无结果", flush=True)
                total_fail += 1
                continue
            out_dir = paper_dir / "mineru_result" / name
            out_dir.mkdir(parents=True, exist_ok=True)
            if (out_dir / "full.md").exists():
                total_ok += 1
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
                total_ok += 1
                print(f"  ✅ {code}-{year}", flush=True)
            except Exception as e:
                total_fail += 1
                print(f"  ❌ {code}-{year}: {str(e)[:80]}", flush=True)
        time.sleep(3)
    print(f"完成 ok={total_ok} fail={total_fail} / 待解析 {len(staged)}")


if __name__ == "__main__":
    main()
