#!/usr/bin/env python3
"""Split a PDF into per-lesson PDFs using MinerU content_list.json headings.

Detection:
  book1 (teacher book): a page is a section start if it holds
      - a unit header  '第X单元'   OR
      - a numbered lesson 'N标题' (N in 1..16, no period before CJK)
  book2 (student book): a page is a section start if it holds
      - a unit header '第X单元'  OR
      - a section label 单元研习任务 / 古诗词诵读 / 后记  OR
      - a short top-of-page title (lesson name, no digits, no paren)

Front matter (cover/编写说明/目录) before --start-page is skipped and emitted
as a '00_前言' file.
"""
import json, re, os, argparse
import fitz

UNIT = re.compile(r'^第[一二三四五六七八九十]+单元')
LESSON = re.compile(r'^\s*(\d{1,2})\s*[\u4e00-\u9fff]')
STANDALONE_NUM = re.compile(r'^\s*\*?\d{1,2}\*?\s*$')
SECT_B2 = ['单元研习任务', '古诗词诵读', '后记']
EXCLUDE = re.compile(
    r'(^语文$)|(^普通高中教科书$)|(^选择性必修$)|(^下册$)|(^教师教学用书$)'
    r'|(编写说明)|(目\s*录)|(图书在版编目)|(CIP)|(关于教师教学用书)'
    r'|(学习提示)|(单元目标)|(编写意图)|(教学指导)|(课文解说)'
    r'|(关于单元学习任务)|(单元教学设计举例)|(资料链接)|(总主编)|(本册主编)'
    r'|(^\s*[（(])|(^[一二三四五六七八九十]+[、.．])'
    r'|(第[一二三四五六七八九十]+[幕折章回场])'
    r'|(语言的锤炼)|(说真话，?抒真情)|(文章修改)'
)


def page_headings(cl_path, offset):
    d = json.load(open(cl_path, encoding='utf-8'))
    pages = {}
    for it in d:
        if it.get('type') != 'text':
            continue
        t = (it.get('text') or '').strip()
        if not t:
            continue
        pg = it.get('page_idx', 0) + offset + 1  # convert to 1-based page for insert_pdf
        pages.setdefault(pg, []).append((it.get('text_level') or 9, t, it['bbox'][1]))
    return pages


def is_lesson(t):
    m = LESSON.match(t)
    if not m:
        return False
    if int(m.group(1)) > 16:
        return False
    if t[m.end() - 1] in '年月日世纪代':
        return False
    return True


def is_title(t):
    if len(t) < 2 or len(t) > 20:
        return False
    if not re.search(r'[\u4e00-\u9fff]', t):
        return False
    if re.search(r'[0-9]', t):
        return False
    if t[0] in '（([':
        return False
    if re.match(r'^[一二三四五六七八九十]+[、.．]', t):
        return False
    if t[-1] in '。！？，：；' or t[-1] in '"\'':
        return False
    return True


def detect(cl_offsets, is_book2, start_page):
    pages = {}
    for cl, off in cl_offsets:
        ph = page_headings(cl, off)
        for pg, items in ph.items():
            pages.setdefault(pg, []).extend(items)
    splits = []
    seen = set()

    def strong(t):
        if EXCLUDE.search(t):
            return False
        if UNIT.match(t):
            return True
        if is_book2 and any(s in t for s in SECT_B2):
            return True
        if not is_book2 and is_lesson(t):
            return True
        return False

    for pg in sorted(pages):
        if pg < start_page:
            continue
        items = pages[pg]
        hit = None
        # 1) unit header / book2 section label / numbered lesson
        for lvl, t, top in items:
            if strong(t):
                hit = t
                break
        # 2) book1: standalone number block -> merge number + nearby title
        if not hit and not is_book2:
            num = None
            for lvl, t, top in items:
                if EXCLUDE.search(t):
                    continue
                if STANDALONE_NUM.match(t):
                    num = (lvl, t, top)
                    break
            if num:
                cand = [(lvl, x) for (lvl, x, top) in items
                        if x != num[1] and lvl <= 2 and not STANDALONE_NUM.match(x)
                        and not EXCLUDE.search(x) and is_title(x)]
                if cand:
                    cand.sort(key=lambda c: -len(c[1]))
                    hit = num[1].strip().replace('*', '') + cand[0][1].strip()
        # 3) book1: '课文解说' header page -> first lesson of that unit follows it
        if not hit and not is_book2:
            ks_top = None
            for lvl, t, top in items:
                if lvl == 2 and t.strip() == '课文解说':
                    ks_top = top
                    break
            if ks_top is not None:
                after = [(top, x) for (lvl, x, top) in items
                         if top > ks_top and x.strip() != '课文解说'
                         and not EXCLUDE.search(x) and is_title(x)]
                if after:
                    after.sort(key=lambda c: c[0])
                    hit = after[0][1].strip()
        # 4) book2 lesson titles: L1 always; L2 if title-like; special LNone
        if not hit and is_book2:
            for lvl, t, top in items:
                if EXCLUDE.search(t):
                    continue
                if lvl == 1:
                    hit = t
                    break
            if not hit:
                for lvl, t, top in sorted(items, key=lambda x: x[2]):
                    if EXCLUDE.search(t):
                        continue
                    if lvl == 2 and is_title(t):
                        hit = t
                        break
            if not hit:
                for lvl, t, top in sorted(items, key=lambda x: x[2]):
                    if EXCLUDE.search(t):
                        continue
                    if lvl == 9 and (t.startswith('离骚') or t.startswith('蜀相')):
                        hit = t.strip()
                        break
        if hit and pg not in seen:
            seen.add(pg)
            splits.append((pg, hit))
    return splits


def sanitize(title):
    t = title.replace('\n', ' ').strip()
    t = re.sub(r'[\\/:*?"<>|（）()·\s]+', '_', t)
    return t[:18]


def run(cl_offsets, is_book2, start_page, orig_pdf, out_dir, write):
    sections = detect(cl_offsets, is_book2, start_page)
    doc = fitz.open(orig_pdf)
    total = doc.page_count
    # build ranges (1-based pages)
    ranges = []
    if sections and sections[0][0] > 1:
        ranges.append((1, sections[0][0] - 1, '前言'))
    for i, (pg, t) in enumerate(sections):
        end = sections[i + 1][0] - 1 if i + 1 < len(sections) else total
        ranges.append((pg, end, t))
    print(f"\n===== {'BOOK1' if not is_book2 else 'BOOK2'} : {len(ranges)} files =====")
    for i, (a, b, t) in enumerate(ranges):
        print(f"  {i:02d}. p{a}-{b}  '{t}'")
    if not write:
        return
    os.makedirs(out_dir, exist_ok=True)
    for i, (a, b, t) in enumerate(ranges):
        name = f"{i:02d}_{sanitize(t)}.pdf"
        d = fitz.open()
        d.insert_pdf(doc, from_page=a - 1, to_page=b - 1)
        d.save(os.path.join(out_dir, name))
        print("  saved", name)
    doc.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cl1a'); ap.add_argument('--off1a', type=int, default=0)
    ap.add_argument('--cl1b'); ap.add_argument('--off1b', type=int, default=174)
    ap.add_argument('--cl2'); ap.add_argument('--off2', type=int, default=0)
    ap.add_argument('--orig1'); ap.add_argument('--orig2')
    ap.add_argument('--out', default='output')
    ap.add_argument('--start1', type=int, default=18)
    ap.add_argument('--start2', type=int, default=6)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    if args.cl1a:
        run([(args.cl1a, args.off1a), (args.cl1b, args.off1b)], False, args.start1,
            args.orig1, os.path.join(args.out, 'book1_教师用书'), args.write)
    if args.cl2:
        run([(args.cl2, args.off2)], True, args.start2,
            args.orig2, os.path.join(args.out, 'book2_课本'), args.write)


if __name__ == '__main__':
    main()
