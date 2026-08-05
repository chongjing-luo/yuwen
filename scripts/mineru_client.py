#!/usr/bin/env python3
"""MinerU v4 precise API client (batch upload flow).

Subcommands:
  submit   --file PATH [--name N] [--page-ranges "1-174,175-347"]  -> prints batch_id
  poll     --batch-id ID   -> blocks until done, prints final json
  download --url URL --out PATH
"""
import os, sys, json, time, argparse, urllib.request, urllib.error

BASE = "https://mineru.net"

def _load_token():
    """Token lookup order: env var MINERU_TOKEN > ~/.workbuddy/mineru_token"""
    tok = os.environ.get("MINERU_TOKEN", "")
    if tok:
        return tok.strip()
    p = os.path.expanduser("~/.workbuddy/mineru_token")
    try:
        with open(p) as f:
            return f.read().strip()
    except Exception:
        return ""

TOKEN = _load_token()


def _req(method, path, body=None, headers=None, raw=False, timeout=120):
    url = BASE + path
    data = None
    h = {"Authorization": f"Bearer {TOKEN}"}
    if headers:
        h.update(headers)
    if body is not None:
        if isinstance(body, (dict, list)):
            data = json.dumps(body).encode("utf-8")
            h.setdefault("Content-Type", "application/json")
        else:
            data = body
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = r.read().decode("utf-8", "replace")
            if raw:
                return r.status, r.headers, resp
            try:
                return r.status, r.headers, json.loads(resp)
            except Exception:
                return r.status, r.headers, resp
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode("utf-8", "replace")


def submit(files, extra=None):
    """files: list of {"path":, "name":, "page_ranges": optional}"""
    body = {"files": [{"name": f["name"]} for f in files]}
    if extra:
        body.update(extra)
    for f, src in zip(body["files"], files):
        if src.get("page_ranges"):
            f["page_ranges"] = src["page_ranges"]
    print("[submit] body:", json.dumps(body, ensure_ascii=False)[:400])
    st, hd, js = _req("POST", "/api/v4/file-urls/batch", body)
    print("[submit] status:", st)
    if not isinstance(js, dict):
        print("UNEXPECTED:", js[:1000]); return None, []
    data = js.get("data", js)
    batch_id = data.get("batch_id")
    file_urls = data.get("file_urls") or []
    print("BATCH_ID=", batch_id)
    if file_urls:
        print("UPLOAD_URL=" + file_urls[0])
    # upload each (file_urls are strings) using curl for reliable large-file transfer
    import subprocess
    paths = [f["path"] for f in files]
    for up, fp in zip(file_urls, paths):
        print(f"PUT upload (curl) -> {up[:70]}...")
        r = subprocess.run(["curl", "-sS", "-X", "PUT", "--upload-file", fp, up],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  curl ERROR: {r.stderr[:300]}")
        else:
            print(f"  curl done (rc=0) msg={r.stdout[:200]}")
    return batch_id, js


def poll(batch_id, interval=12, timeout=3600):
    print(f"[poll] batch {batch_id}")
    waited = 0
    last = None
    while waited < timeout:
        st, hd, js = _req("GET", f"/api/v4/extract-results/batch/{batch_id}")
        if not isinstance(js, dict):
            print("non-json:", str(js)[:500]); time.sleep(interval); waited += interval; continue
        data = js.get("data", js)
        # 字段名是 extract_result（skill 已验证），兼容 results/extract_results
        results = (data.get("extract_result")
                   or data.get("results")
                   or data.get("extract_results") or [])
        if isinstance(results, list):
            states = [(r.get("state") or r.get("status")) for r in results]
            print(f"  t={waited}s states={states}")
            if states and all(s in ("done", "failed") for s in states):
                return js
        else:
            print(f"  t={waited}s data={str(data)[:200]}")
        last = js
        time.sleep(interval); waited += interval
    return last


def download(url, out):
    print(f"[download] -> {out}")
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=300) as r:
        data = r.read()
    with open(out, "wb") as f:
        f.write(data)
    print(f"  saved {len(data)} bytes")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("submit")
    s.add_argument("--file", action="append", nargs=2, metavar=("PATH", "NAME"), help="repeatable")
    s.add_argument("--page-ranges", default=None)
    s2 = sub.add_parser("poll")
    s2.add_argument("--batch-id", required=True)
    s3 = sub.add_parser("download")
    s3.add_argument("--url", required=True)
    s3.add_argument("--out", required=True)
    args = ap.parse_args()

    if args.cmd == "submit":
        files = [{"path": p, "name": n} for p, n in args.file]
        if args.page_ranges:
            # apply same page_ranges to first file only (used for single big file split)
            files[0]["page_ranges"] = args.page_ranges.split(",")
        bid, _ = submit(files, extra={"language": "ch", "enable_formula": True,
                                      "enable_table": True, "model_version": "pipeline"})
        print("BATCH_ID=" + str(bid))
    elif args.cmd == "poll":
        js = poll(args.batch_id)
        print("FINAL_JSON=" + json.dumps(js, ensure_ascii=False)[:4000])
    elif args.cmd == "download":
        download(args.url, args.out)
