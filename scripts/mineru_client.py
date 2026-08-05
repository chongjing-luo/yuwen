#!/usr/bin/env python3
"""MinerU v4 precise API client (batch upload flow).

Subcommands:
  submit   --file PATH [--name N] [--page-ranges "1-174,175-347"]  -> prints batch_id
  poll     --batch-id ID   -> blocks until done, prints final json
  download --url URL --out PATH
"""
import argparse
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from urllib.parse import urlsplit

BASE = "https://mineru.net"
PROXY_ENV_KEYS = (
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
    "http_proxy", "https_proxy", "all_proxy",
)


def _validate_https_url(url):
    """Reject malformed and downgrade-prone transfer URLs."""
    parsed = urlsplit(url)
    if parsed.scheme.lower() != "https" or not parsed.hostname:
        raise ValueError("MinerU transfers require a valid HTTPS URL")
    return parsed


def _redact_url(url):
    """Return only the origin so signed paths and query strings never reach logs."""
    parsed = urlsplit(url)
    if not parsed.hostname:
        return "<redacted-url>"
    return f"{parsed.scheme.lower()}://{parsed.hostname.lower()}/<redacted>"


def _redact_error(message, url):
    safe = (message or "").replace(url, _redact_url(url))
    return re.sub(r"https://[^\s]+", lambda match: _redact_url(match.group(0)), safe)[:300]


def _transfer_env(url):
    """Bypass the broken local proxy only for the MinerU OpenXLab CDN."""
    parsed = _validate_https_url(url)
    env = os.environ.copy()
    host = parsed.hostname.lower()
    if host == "cdn-mineru.openxlab.org.cn" or host.endswith(".openxlab.org.cn"):
        for key in PROXY_ENV_KEYS:
            env.pop(key, None)
        env["NO_PROXY"] = host
        env["no_proxy"] = host
    return env


def _curl_transfer(url, *, output=None, upload=None):
    """Run a retrying HTTPS-only curl transfer."""
    if (output is None) == (upload is None):
        raise ValueError("Specify exactly one of output or upload")
    _validate_https_url(url)
    command = [
        "/usr/bin/curl",
        "--fail", "--location",
        "--retry", "4", "--retry-all-errors", "--retry-delay", "1",
        "--connect-timeout", "30", "--max-time", "600",
        "--silent", "--show-error",
        "--proto", "=https", "--proto-redir", "=https", "--tlsv1.2",
    ]
    if output is not None:
        command.extend(["-o", output])
    else:
        command.extend(["--upload-file", upload])
    command.append(url)
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=_transfer_env(url),
    )


def _validate_download(path, destination):
    """Validate MinerU ZIP responses before replacing a previous good file."""
    if not destination.lower().endswith(".zip"):
        return
    try:
        with zipfile.ZipFile(path) as archive:
            if not archive.namelist():
                raise RuntimeError("download failed: ZIP archive is empty")
            bad_member = archive.testzip()
    except zipfile.BadZipFile as exc:
        raise RuntimeError("download failed: invalid ZIP archive") from exc
    if bad_member is not None:
        raise RuntimeError("download failed: ZIP archive failed CRC validation")


def _load_token():
    """Token lookup: environment > project .env > ~/.workbuddy/mineru_token."""
    tok = os.environ.get("MINERU_TOKEN", "")
    if tok:
        return tok.strip()
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    try:
        with open(env_path) as f:
            for line in f:
                key, sep, value = line.strip().partition("=")
                if sep and key.strip() == "MINERU_TOKEN":
                    return value.strip().strip('"').strip("'")
    except Exception:
        pass
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
        print(f"UPLOAD_URLS={len(file_urls)} (redacted)")
    # Upload each file through the same HTTPS-only, retrying transfer policy.
    paths = [f["path"] for f in files]
    if len(file_urls) != len(paths):
        raise RuntimeError(
            f"MinerU returned {len(file_urls)} upload URLs for {len(paths)} files"
        )
    for index, (up, fp) in enumerate(zip(file_urls, paths), start=1):
        print(f"PUT upload {index}/{len(paths)} (curl) -> {_redact_url(up)}")
        r = _curl_transfer(up, upload=fp)
        if r.returncode != 0:
            raise RuntimeError(
                f"upload failed (rc={r.returncode}): {_redact_error(r.stderr, up)}"
            )
        print("  curl done (rc=0)")
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
    _validate_https_url(url)
    destination = os.path.abspath(out)
    destination_dir = os.path.dirname(destination)
    os.makedirs(destination_dir, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{os.path.basename(destination)}.",
        suffix=".part",
        dir=destination_dir,
    )
    os.close(fd)
    try:
        curl_result = _curl_transfer(url, output=temporary)
        result = curl_result
        if result.returncode != 0:
            print(f"  curl failed (rc={result.returncode}); retrying with wget")
            result = subprocess.run([
                "/usr/bin/wget",
                "--https-only", "--tries=5", "--timeout=60", "--retry-connrefused",
                "--quiet", "-O", temporary, url,
            ], capture_output=True, text=True, env=_transfer_env(url))
        if result.returncode != 0:
            curl_error = _redact_error(curl_result.stderr, url)
            wget_error = _redact_error(result.stderr, url)
            raise RuntimeError(
                f"download failed (curl rc={curl_result.returncode}; "
                f"wget rc={result.returncode}): {curl_error or wget_error}"
            )
        size = os.path.getsize(temporary)
        if size == 0:
            raise RuntimeError("download failed: received an empty file")
        _validate_download(temporary, destination)
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(f"  saved {size} bytes")


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
