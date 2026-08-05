#!/usr/bin/env python3
"""批量跑 MinerU：遍历 Data/textbook_extract/{册}/ 下所有 split PDF，
分批提交 → 轮询 → 下载解压 → 整理到 {册}/mineru_result/{文件名}/"""

import os, sys, json, time, glob, zipfile, subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'scripts'))
import mineru_client as mc

# 支持环境变量覆盖；默认指向 <项目根>/Data/textbook_extract
BASE = os.environ.get('YUWEN_DATA_DIR', os.path.join(PROJECT_ROOT, 'Data', 'textbook_extract'))
BATCH_SIZE = 20          # 每批提交的文件数
POLL_INTERVAL = 20       # 轮询间隔秒

def get_pdf_files(book_dir):
    """返回该册所有切分 PDF（按文件名排序）"""
    return sorted(glob.glob(os.path.join(book_dir, '*.pdf')))

def submit_batch(files, book_name):
    """提交一批文件，返回 (batch_id, file_names)"""
    names = [os.path.basename(f) for f in files]
    flist = [{"path": f, "name": n} for f, n in zip(files, names)]
    bid, js = mc.submit(flist, extra={"language": "ch", "enable_formula": True,
                                      "enable_table": True, "model_version": "pipeline"})
    return bid, names

def poll_batch(bid, timeout=5400):
    """轮询直到全部 done/failed，返回结果列表 [{file_name, state, full_zip_url}]"""
    waited = 0
    while waited < timeout:
        st, hd, js = mc._req("GET", f"/api/v4/extract-results/batch/{bid}")
        if isinstance(js, dict):
            data = js.get("data", js)
            results = (data.get("extract_result") or data.get("results") or [])
            if results:
                states = [r.get("state") for r in results]
                done = all(s in ("done", "failed") for s in states)
                if done:
                    return results
        time.sleep(POLL_INTERVAL)
        waited += POLL_INTERVAL
        if waited % 120 == 0:
            print(f"  [poll {bid[:8]}] 已等待 {waited}s")
    raise TimeoutError(f"batch {bid} 轮询超时")

def download_and_extract(book_dir, results, book_name):
    """下载每个结果的 zip 并解压到 {册}/mineru_result/{原始文件名去.pdf}/"""
    out_root = os.path.join(book_dir, 'mineru_result')
    os.makedirs(out_root, exist_ok=True)
    # zip 缓存到 /tmp（系统自动清理），避免在项目目录内删除文件触发安全拦截
    cache_dir = '/tmp/mineru_zips'
    os.makedirs(cache_dir, exist_ok=True)
    ok, fail = 0, 0
    for r in results:
        fname = r.get("file_name", "")
        state = r.get("state")
        url = r.get("full_zip_url", "")
        if state != "done" or not url:
            print(f"  ❌ {fname}: state={state} err={r.get('err_msg','')[:100]}")
            fail += 1
            continue
        # 输出目录 = 文件名去掉.pdf
        out_dir = os.path.join(out_root, fname[:-4] if fname.endswith('.pdf') else fname)
        os.makedirs(out_dir, exist_ok=True)
        if os.path.exists(os.path.join(out_dir, 'full.md')):
            print(f"  ⏭ {fname}: 已存在，跳过")
            ok += 1
            continue
        zip_path = os.path.join(cache_dir, f"{book_name}_{fname}.zip")
        try:
            mc.download(url, zip_path)
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(out_dir)
            print(f"  ✅ {fname} -> {os.path.relpath(out_dir, BASE)}")
            ok += 1
        except Exception as e:
            print(f"  ❌ {fname} 下载失败: {str(e)[:150]}")
            fail += 1
    return ok, fail

def process_book(book_name, skip_existing=True):
    book_dir = os.path.join(BASE, book_name)
    pdfs = get_pdf_files(book_dir)
    print(f"\n===== {book_name}: {len(pdfs)} 个文件 =====")
    if not pdfs:
        print("  (无 PDF 文件，跳过)")
        return

    # 跳过已解析的（mineru_result 下已有 full.md 的文件）
    if skip_existing:
        pending = []
        for f in pdfs:
            base_name = os.path.basename(f)[:-4]
            md = os.path.join(book_dir, 'mineru_result', base_name, 'full.md')
            if not os.path.exists(md):
                pending.append(f)
        print(f"  待解析 {len(pending)} 个（已解析 {len(pdfs)-len(pending)} 个）")
        pdfs = pending
        if not pdfs:
            print("  全部已完成")
            return

    # 分批提交
    for i in range(0, len(pdfs), BATCH_SIZE):
        batch = pdfs[i:i+BATCH_SIZE]
        print(f"\n  --- 提交批次 {i//BATCH_SIZE+1} ({len(batch)} 个文件) ---")
        bid, names = submit_batch(batch, book_name)
        if not bid:
            print("  ❌ 提交失败，跳过本批")
            continue
        print(f"  batch_id={bid}")
        results = poll_batch(bid)
        ok, fail = download_and_extract(book_dir, results, book_name)
        print(f"  批次完成: 成功 {ok}, 失败 {fail}")
        # 每批间隔，避免限流
        time.sleep(3)

if __name__ == '__main__':
    books = ['必修上册', '必修下册', '选择性必修上册', '选择性必修中册', '选择性必修下册', '必修下册教师用书']
    # 支持命令行指定某册: python batch_mineru.py 选择性必修下册
    if len(sys.argv) > 1:
        books = [sys.argv[1]]
    for b in books:
        try:
            process_book(b)
        except Exception as e:
            print(f"  ⚠️ {b} 处理异常: {str(e)[:200]}")
    print("\n✅ 全部批次处理完毕")
