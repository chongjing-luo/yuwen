#!/usr/bin/env python3
"""Split PDFs into per-unit PDFs using MinerU content_list.json headings.

Only splits on '第X单元' (and supplementary sections like 古诗词诵读/后记).
Front matter before the first unit becomes '00_前言'.
"""
import json, re, os, glob
import fitz

UNIT = re.compile(r'^第[一二三四五六七八九十]+单元')
CN_NUM = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}

def cn_to_int(s):
    """Convert Chinese number (一..十, 十一..十九, 二十..二十九) to int."""
    if s == '十':
        return 10
    if s.startswith('十'):
        return 10 + CN_NUM[s[1]]
    if '十' in s:
        parts = s.split('十')
        return CN_NUM[parts[0]] * 10 + (CN_NUM[parts[1]] if parts[1] else 0)
    return CN_NUM.get(s, 0)


def find_unit_pages(cl_path, offset):
    """Find pages where unit headers appear. Returns list of (page_1based, unit_title)."""
    d = json.load(open(cl_path, encoding='utf-8'))
    results = []
    for it in d:
        if it.get('type') != 'text':
            continue
        t = (it.get('text') or '').strip()
        if not t:
            continue
        level = it.get('text_level', 99)
        pg = it.get('page_idx', 0) + offset + 1  # 1-based page number

        m = UNIT.match(t)
        if m and level <= 2:
            # Extract unit number
            unit_cn = m.group(0).replace('第', '').replace('单元', '')
            unit_num = cn_to_int(unit_cn)
            # Clean title: remove trailing whitespace/subtitles
            title = t.split('\n')[0].strip()
            # Keep just "第X单元" or include subtitle if present
            title_clean = re.sub(r'\s+', ' ', title)[:20]
            results.append((pg, unit_num, title_clean))

    return results


def find_extra_sections(cl_path, offset):
    """Find special sections for book2: 古诗词诵读, 后记."""
    d = json.load(open(cl_path, encoding='utf-8'))
    results = []
    for it in d:
        if it.get('type') != 'text':
            continue
        t = (it.get('text') or '').strip()
        if not t:
            continue
        level = it.get('text_level', 99)
        pg = it.get('page_idx', 0) + offset + 1
        if level <= 2 and t in ('古诗词诵读', '后记'):
            results.append((pg, t))
    return results


def sanitize(title):
    t = title.replace('\n', ' ').strip()
    t = re.sub(r'[\\/:*?"<>|（）()·\s]+', '_', t)
    return t[:30]


def split_book1():
    """Split book1 (教师教学用书, 347 pages) by unit."""
    orig = '/Users/luochongjing/Documents/Projects/Yuwen/Data/textbook/统编本高中语文必修下册 教师教学用书.pdf'

    # Book1 was split into two parts for MinerU:
    # Part A = pages 1-174 (offset 0), Part B = pages 175-347 (offset 174)
    cl1a = glob.glob('work/book1A_result/*_content_list.json')[0]
    cl1b = glob.glob('work/book1B_result/*_content_list.json')[0]

    units_a = find_unit_pages(cl1a, 0)
    units_b = find_unit_pages(cl1b, 174)

    all_units = units_a + units_b
    print(f"\n===== BOOK1 (教师教学用书, 347页) =====")
    print(f"Found {len(all_units)} raw unit markers:")
    for pg, num, title in all_units:
        print(f"  第{num}单元 -> p{pg}: {title}")

    # Sort by page, then filter: keep only markers where unit numbers are
    # monotonically increasing starting from 1. This removes TOC/intro false positives
    # (e.g. "第三单元" mentioned on p16 before real 第一单元 on p19).
    all_units.sort(key=lambda x: x[0])
    unique = []
    expected = 1
    for pg, num, title in all_units:
        if num == expected:
            unique.append((pg, num, title))
            expected += 1
        else:
            print(f"  [SKIP] 第{num}单元 p{pg} (expected 第{expected}单元, likely TOC/intro reference)")

    # Build ranges
    doc = fitz.open(orig)
    total = doc.page_count
    ranges = []

    # Front matter (before first unit)
    if unique and unique[0][0] > 1:
        ranges.append((1, unique[0][0] - 1, '前言', 0))
    elif not unique:
        ranges.append((1, total, '全文', 0))

    for i, (pg, num, title) in enumerate(unique):
        end = unique[i + 1][0] - 1 if i + 1 < len(unique) else total
        ranges.append((pg, end, title, num))

    out_dir = '/Users/luochongjing/Documents/Projects/Yuwen/output/book1_教师用书_单元'
    os.makedirs(out_dir, exist_ok=True)
    # Clean old files
    for f in glob.glob(out_dir + '/*.pdf'):
        os.remove(f)

    print(f"\nSplitting into {len(ranges)} files:")
    for i, (a, b, t, num) in enumerate(ranges):
        prefix = '00' if num == 0 else f"{num:02d}"
        name = f"{prefix}_{sanitize(t)}.pdf"
        d = fitz.open()
        d.insert_pdf(doc, from_page=a - 1, to_page=b - 1)
        d.save(os.path.join(out_dir, name))
        d.close()
        print(f"  {name}  (p{a}-{b}, {b-a+1} pages)")
    doc.close()
    return out_dir


def split_book2():
    """Split book2 (课本, 123 pages) by unit."""
    orig = '/Users/luochongjing/Documents/Projects/Yuwen/Data/textbook/高中语文选择性必修下册(OCR).pdf'

    cl2 = glob.glob('work/book2_result/*_content_list.json')[0]
    units = find_unit_pages(cl2, 0)
    extras = find_extra_sections(cl2, 0)

    print(f"\n===== BOOK2 (课本, 123页) =====")
    print(f"Found {len(units)} unit markers:")
    for pg, num, title in units:
        print(f"  第{num}单元 -> p{pg}: {title}")
    print(f"Found {len(extras)} extra sections:")
    for pg, title in extras:
        print(f"  {title} -> p{pg}")

    # Combine: units get numbered, extras get sequential after
    # Build combined list sorted by page
    combined = []
    for pg, num, title in units:
        combined.append((pg, num, title))
    for pg, title in extras:
        # Assign a high number for sorting
        combined.append((pg, 100 + len([c for c in combined if c[1] >= 100]), title))
    combined.sort(key=lambda x: x[0])

    doc = fitz.open(orig)
    total = doc.page_count
    ranges = []

    # Front matter
    if combined and combined[0][0] > 1:
        ranges.append((1, combined[0][0] - 1, '前言', 0))

    for i, (pg, num, title) in enumerate(combined):
        end = combined[i + 1][0] - 1 if i + 1 < len(combined) else total
        ranges.append((pg, end, title, num))

    out_dir = '/Users/luochongjing/Documents/Projects/Yuwen/output/book2_课本_单元'
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(out_dir + '/*.pdf'):
        os.remove(f)

    print(f"\nSplitting into {len(ranges)} files:")
    for i, (a, b, t, num) in enumerate(ranges):
        prefix = '00' if num == 0 else f"{num:02d}"
        name = f"{prefix}_{sanitize(t)}.pdf"
        d = fitz.open()
        d.insert_pdf(doc, from_page=a - 1, to_page=b - 1)
        d.save(os.path.join(out_dir, name))
        d.close()
        print(f"  {name}  (p{a}-{b}, {b-a+1} pages)")
    doc.close()
    return out_dir


if __name__ == '__main__':
    os.chdir('/Users/luochongjing/Documents/Projects/Yuwen')
    d1 = split_book1()
    d2 = split_book2()
    print(f"\nDone! Output directories:")
    print(f"  {d1}")
    print(f"  {d2}")
