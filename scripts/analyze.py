#!/usr/bin/env python3
"""Analyze a MinerU content_list.json to find section/lesson boundaries.

Usage: analyze.py <content_list.json> [page_offset]
  page_offset: add to MinerU's 1-based page to map to original PDF page
                (0 for whole-file; 174 for book1 partB).
Prints: type distribution + candidate heading items (short text with page).
"""
import json, sys, re
from collections import Counter

path = sys.argv[1]
offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0
data = json.load(open(path, encoding="utf-8"))
items = data if isinstance(data, list) else data.get("content_list", data.get("data", []))

print("total items:", len(items))
c = Counter(it.get("type") for it in items)
print("types:", dict(c))

def text_of(it):
    t = it.get("text")
    if t is None:
        t = it.get("title")
    if isinstance(t, list):
        t = " ".join(str(x) for x in t)
    return t or ""

# candidate headings: short text, or explicit heading/title type
print("\n--- candidate headings (short text / heading types) ---")
for it in items:
    t = it.get("type")
    txt = text_of(it).strip()
    pg = it.get("page")
    if not txt or pg is None:
        continue
    is_heading_type = t in ("heading", "title", "h1", "h2", "h3")
    short = len(txt) <= 50
    if is_heading_type or (short and re.search(r"[一-鿿]", txt)):
        print(f"  p{pg+offset} [{t}] {txt[:50]}")
