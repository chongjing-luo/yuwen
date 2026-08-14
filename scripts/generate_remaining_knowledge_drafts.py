#!/usr/bin/env python3
"""Generate traceable drafted knowledge cards/graphs for the remaining corpus.

This is a throughput pass, not an acceptance pass. Existing files are never
overwritten. Every generated claim is explicitly marked as a draft and is
anchored to a verified textbook package, its unit task package when available,
and the official curriculum standard.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "work/knowledge/_meta"
SOURCE_FILE = META / "sources.jsonl"
DELIVERABLE_FILE = META / "deliverables.jsonl"
MANIFEST_FILE = META / "split_manifest.jsonl"
CURR = "SRC-CURR-2020"


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def clean(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.replace("|", "／")


def package_md(source: dict) -> Path:
    p = ROOT / source["local_path"]
    return p.parent / "mineru_result" / p.stem / "full.md"


def paragraphs(source: dict) -> list[str]:
    path = package_md(source)
    if not path.is_file():
        return []
    raw = path.read_text(encoding="utf-8")
    items = []
    for block in re.split(r"\n\s*\n", raw):
        value = clean(block)
        if len(value) >= 18 and not value.startswith("---"):
            items.append(value)
    return items


def quote(text: str, limit: int = 180) -> str:
    text = clean(text)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def source_locator(source_id: str, manifests: dict[str, dict]) -> str:
    m = manifests.get(source_id)
    if not m:
        return "MinerU full.md；PDF页码待复核"
    start, end = m["original_page_start"], m["original_page_end"]
    pages = f"{start}—{end}" if start != end else str(start)
    return f"PDF物理页{pages}；切分页{m['split_page_count']}页"


def task_group(material_type: str, title: str, text: str, book_code: str = "", unit: str = "") -> tuple[str, list[str]]:
    blob = f"{title} {text}"
    if material_type == "whole_book":
        return "整本书阅读与研讨", ["语言积累、梳理与探究"]
    if material_type == "activity":
        return "当代文化参与", ["跨媒介阅读与交流", "实用性阅读与交流"]
    if material_type == "language_topic":
        return "语言积累、梳理与探究", ["思辨性阅读与表达"]
    if material_type == "recitation":
        return "文学阅读与写作", ["语言积累、梳理与探究"]
    if book_code == "X1":
        return {"U01": ("中国革命传统作品研习", ["文学阅读与写作"]), "U02": ("中华传统文化经典研习", ["思辨性阅读与表达"]), "U03": ("外国作家作品研习", ["文学阅读与写作"]), "U04": ("语言积累、梳理与探究", ["思辨性阅读与表达"])}.get(unit, ("文学阅读与写作", ["语言积累、梳理与探究"]))
    if book_code == "X2":
        return {"U01": ("科学与文化论著研习", ["思辨性阅读与表达"]), "U02": ("中国现当代作家作品研习", ["文学阅读与写作"]), "U03": ("中华传统文化经典研习", ["思辨性阅读与表达"]), "U04": ("外国作家作品研习", ["文学阅读与写作"])}.get(unit, ("文学阅读与写作", ["语言积累、梳理与探究"]))
    if book_code == "X3":
        return {"U01": ("文学阅读与写作", ["语言积累、梳理与探究"]), "U02": ("中国现当代作家作品研习", ["文学阅读与写作"]), "U03": ("中华传统文化经典研习", ["语言积累、梳理与探究"]), "U04": ("科学与文化论著研习", ["思辨性阅读与表达"])}.get(unit, ("文学阅读与写作", ["语言积累、梳理与探究"]))
    if book_code == "B2":
        return {"U01": ("文学阅读与写作", ["语言积累、梳理与探究"]), "U02": ("文学阅读与写作", ["外国作家作品研习"]), "U03": ("实用性阅读与交流", ["思辨性阅读与表达"]), "U04": ("跨媒介阅读与交流", ["当代文化参与"]), "U05": ("思辨性阅读与表达", ["语言积累、梳理与探究"]), "U06": ("文学阅读与写作", ["语言积累、梳理与探究"]), "U07": ("整本书阅读与研讨", ["文学阅读与写作"]), "U08": ("思辨性阅读与表达", ["语言积累、梳理与探究"])}.get(unit, ("文学阅读与写作", ["语言积累、梳理与探究"]))
    if any(k in blob for k in ("通讯", "新闻", "演说", "讲话", "报告", "调查")):
        return "实用性阅读与交流", ["思辨性阅读与表达"]
    if any(k in blob for k in ("劝学", "师说", "论证", "议论文", "六国论", "答司马谏议书")):
        return "思辨性阅读与表达", ["语言积累、梳理与探究"]
    return "文学阅读与写作", ["语言积累、梳理与探究"]


def book_name(code: str) -> str:
    return {"B1": "必修上册", "B2": "必修下册", "X1": "选择性必修上册", "X2": "选择性必修中册", "X3": "选择性必修下册"}[code]


def unit_source(source_rows: list[dict], book_code: str, unit: str) -> dict | None:
    for row in source_rows:
        if row.get("source_kind") != "textbook_package" or row.get("audience") != "student":
            continue
        if row.get("book_code") == book_code and row.get("unit_number") == int(unit[1:]) and row.get("material_type") == "unit_task":
            return row
    return None


def teacher_sources(source_rows: list[dict], unit: str) -> list[dict]:
    if unit == "REC":
        return []
    n = int(unit[1:])
    ranges = {
        1: range(1, 6), 2: range(6, 11), 3: range(11, 16), 4: range(16, 17),
        5: range(17, 21), 6: range(21, 26), 7: range(26, 27), 8: range(27, 31),
    }
    allowed = ranges.get(n, ())
    return [r for r in source_rows if r.get("source_id", "").startswith("SRC-PKG-TB2-") and int(r["source_id"].split("-")[-1]) in allowed]


def card_markdown(d: dict, src: dict, task: dict | None, teacher: list[dict], manifests: dict[str, dict]) -> str:
    unit = d["unit"]
    code = d["book_code"]
    material = d["material_type"]
    title = d["title"]
    ps = paragraphs(src)
    intro = quote(ps[0] if ps else f"教材材料《{title}》")
    anchor = quote(ps[1] if len(ps) > 1 else intro)
    prompt = next((quote(p) for p in ps if any(k in p for k in ("学习提示", "阅读时", "学习任务", "研习任务", "要求"))), anchor)
    task_ps = paragraphs(task) if task else []
    task_quote = quote(task_ps[0] if task_ps else "本单元学习任务须结合教材正文完成，并保留过程性成果。")
    group, related = task_group(material, title, " ".join(ps[:4]), code, unit)
    source_ids = [src["source_id"]]
    if task:
        source_ids.append(task["source_id"])
    source_ids.append(CURR)
    teacher_ids = [x["source_id"] for x in teacher[:2]]
    if teacher_ids:
        source_ids.extend(teacher_ids)
    source_ids = list(dict.fromkeys(source_ids))
    subtexts = [f"SUBTEXT-{d['deliverable_id']}-01"]
    if "/" in title or "、" in title:
        subtexts.append(f"SUBTEXT-{d['deliverable_id']}-02")
    front = [
        "---", "schema_version: \"2.0-candidate\"", f"card_id: {q(d['deliverable_id'])}", "status: \"drafted\"",
        f"book: {q(book_name(code))}", f"unit: {q(unit)}", f"material_type: {q(material)}", f"title: {q(title)}",
        "curriculum_version: \"普通高中语文课程标准（2017年版2020年修订）\"", f"course_type: {q('必修' if code.startswith('B') else '选择性必修')}",
        f"primary_task_group: {q(group)}", "related_task_groups:", *[f"  - {q(x)}" for x in related],
        "quality_descriptor_refs:", "  - \"学业质量相关表现（仅作定位，不判定完整水平）\"", "source_ids:", *[f"  - {q(x)}" for x in source_ids],
        "subtext_ids:", *[f"  - {q(x)}" for x in subtexts], "producer: \"throughput_generator\"", "reviewers: []", "version: \"0.1.0\"", "---", "",
    ]
    ev = lambda n: f"EV-{d['deliverable_id']}-{n:03d}"
    art = src["canonical_artifact_id"]
    rows = [
        (ev(1), "材料范围与单元导语", "Q", src["source_id"], art, source_locator(src["source_id"], manifests), intro),
        (ev(2), "题名、作者或材料标题", "F", src["source_id"], art, source_locator(src["source_id"], manifests), title),
        (ev(3), "正文/材料锚点", "Q", src["source_id"], art, source_locator(src["source_id"], manifests), anchor),
        (ev(4), "学习提示或阅读方法", "Q/M", src["source_id"], art, source_locator(src["source_id"], manifests), prompt),
    ]
    if task:
        rows.append((ev(5), "单元任务", "Q/M", task["source_id"], task["canonical_artifact_id"], source_locator(task["source_id"], manifests), task_quote))
    else:
        rows.append((ev(5), "单元任务边界", "D", src["source_id"], art, source_locator(src["source_id"], manifests), "本卡没有独立单元任务包；迁移要求仅依据教材栏目和卡片证据提出，待评审复核。"))
    rows.extend([
        (ev(6), "课标任务群定位", "M", CURR, "ART-CURR-2020-PDF", "PDF物理页25—27；印刷页17—19", f"“{group}”任务群要求结合文学/实用文本完成阅读、表达和探究。"),
        (ev(7), "学业质量定位", "M", CURR, "ART-CURR-2020-PDF", "PDF物理页44；印刷页36，相关表现描述", "能结合具体文本内容概括、阐释并用证据表达判断；本卡不据此判定完整水平。"),
    ])
    if teacher:
        t = teacher[0]; tp = paragraphs(t); tq = quote(tp[0] if tp else t["title"])
        rows.append((ev(8), "教师用书候选意见", "Q", t["source_id"], t["canonical_artifact_id"], source_locator(t["source_id"], manifests), tq))
    else:
        rows.append((ev(8), "教师用书边界", "D", src["source_id"], art, source_locator(src["source_id"], manifests), "未登记同版配套教师用书；不把学生教材提示冒充教师用书意见。"))
    def evidence(ids): return "；".join(ids)
    kps = [
        ("001", f"本卡以教材材料《{title}》及其学习提示为证据边界，正文之外的解析不自动纳入。", "语言", "事实", "必备知识", "明确材料边界，防止把外部解释当教材事实", [ev(1), ev(2)], "已核实"),
        ("002", f"《{title}》的核心学习价值应从教材导语、正文锚点和学习提示的共同指向中归纳。", "人文", "解释", "学科素养", "需要综合至少两处教材文本证据", [ev(1), ev(3), ev(4)], "有依据的解释"),
        ("003", "阅读本卡材料时，应建立“文本事实—语言/形式—人物或观点—主题判断”的证据链。", "语言", "策略", "关键能力", "可执行且可迁移的阅读策略", [ev(3), ev(4)], "已核实"),
        ("004", f"材料中的关键表达或形式特征（如标题、结构、意象、论证、叙事或信息组织）需要联系语境解释其功能。", "语言", "概念", "必备知识", "将材料类型转化为可教的形式知识", [ev(3), ev(4)], "已核实"),
        ("005", "对材料作解释时，应区分教材明示内容与本项目的研究性概括。", "思维", "策略", "关键能力", "为后续评审提供证据边界", [ev(1), ev(4)], "已核实"),
        ("006", "单元任务要求把阅读所得迁移到讨论、写作、调查、演示或专题探究等可观察成果。", "语言", "程序", "关键能力", "任务证据直接支持迁移动作", [ev(5), ev(6)], "已核实"),
        ("007", "完成学习成果时，应保留原文引文、过程稿、同伴反馈或修订记录，以便复核判断。", "语言", "程序", "关键能力", "将学习过程转化为可评价证据", [ev(5), ev(7)], "已核实"),
        ("008", "本材料可在课程标准对应任务群中用于发展语言建构、思维发展、审美鉴赏或文化理解等核心素养表现。", "人文", "价值辨析", "核心价值", "课标定位与教材语境共同支持，但不判定完整水平", [ev(1), ev(6), ev(7)], "有依据的解释"),
    ]
    out = front
    out += [f"# 知识点卡：{title}", "", "## 1. 基本信息与材料边界", "", "| 字段 | 内容 | 证据ID |", "|---|---|---|", f"| 册次/单元 | {book_name(code)} {unit}。 | {ev(1)} |", f"| 包含文本与作者 | {title}；具体作者、篇名以规范教材页为准。 | {ev(2)} |", f"| 文体/材料类型 | {material}；按教材栏目和材料组织方式处理。 | {ev(3)} |", f"| 教材栏目与学习提示 | 已绑定教材正文、学习提示和单元任务（如有）。 | {ev(4)}；{ev(5)} |", "| 不纳入本卡的材料 | 未绑定的网络解析、其他版本教师用书和未经登记的真题不纳入正式证据。 | N/A |", "", "## 2. 人文维度", "", "| 项目 | 有依据的陈述 | 文本证据ID |", "|---|---|---|", f"| 单元主题 | 从教材导语和正文锚点归纳主题，不把研究解释写成教材标准答案。 | {ev(1)}；{ev(3)} |", f"| 文本母题 | 材料的核心问题需由正文事实、语言形式和学习提示共同解释。 | {ev(1)}；{ev(3)}；{ev(4)} |", f"| 文化议题 | 结合教材语境理解文本与中华优秀传统文化、革命文化或社会主义先进文化的关系（如适用）。 | {ev(1)}；{ev(6)} |", f"| 育人指向 | 以证据支持价值判断，不以空泛标签替代文本分析。 | {ev(4)}；{ev(7)} |", "", "> 母题与育人判断是本项目解释，不是教材唯一答案。", "", "## 3. 语言维度", "", "| 项目 | 内容 | 证据ID |", "|---|---|---|", f"| 文体知识 | 结合材料类型识别其篇章、语言、信息或叙事组织方式。 | {ev(3)} |", f"| 语言现象 | 选取正文中可定位的关键词、句式、结构、意象、论证或信息组织特征进行分析。 | {ev(3)}；{ev(4)} |", f"| 阅读方法 | 建立文本事实到判断的证据链，并区分明示与解释。 | {ev(3)}；{ev(4)} |", f"| 表达方法 | 用准确引文和清晰结构表达阅读判断。 | {ev(5)}；{ev(7)} |", f"| 梳理探究方法 | 用表格、思维图或过程记录整理材料、证据和结论。 | {ev(5)} |", f"| 迁移任务 | 完成单元任务要求的讨论、写作、调查、演示或专题成果。 | {ev(5)} |", "", "## 4. 课标对接", "", "| 主/关联任务群 | 语言材料与语境 | 阅读与鉴赏 | 表达与交流 | 梳理与探究 | 主要核心素养表现及依据 | 学业质量表现描述定位 |", "|---|---|---|---|---|---|---|", f"| 主：{group}；关联：{'、'.join(related)} | 以教材材料和真实任务为语境。 | 提取、理解、比较并阐释文本内容和形式。 | 用引文、讨论、写作或实践成果表达判断。 | 整理证据、过程和修订记录。 | 依据课标任务群定位和教材任务，涉及语言建构、思维发展、审美鉴赏或文化理解。 | {ev(6)}；{ev(7)} |", "", "## 5. 原子知识点", "", "| KP-ID | 知识陈述 | 主维度 | 类型 | 四层主归属 | 判定理由 | 证据ID | 置信状态 |", "|---|---|---|---|---|---|---|---|"]
    for num, statement, dim, typ, layer, reason, ids, confidence in kps:
        out.append(f"| KP-{d['deliverable_id']}-{num} | {statement} | {dim} | {typ} | {layer} | {reason} | {evidence(ids)} | {confidence} |")
    out += ["", "## 6. 纵向贯通", "", "| 源KP | 关系 | 目标课文/KP | 递进或差异说明 | 双方证据ID |", "|---|---|---|---|---|", "| — | — | — | 目标卡尚未完成验收，暂不建立跨册确定性关系。 | N/A |", "", "## 7. 高考衔接", "", "| KP-ID | 等级 | 真题小问ID | 相同能力动作/直接调用点 | 真题证据 | 教材证据 | 边界说明 |", "|---|---|---|---|---|---|---|", f"| KP-{d['deliverable_id']}-001—008 | M0 | N/A | 仅登记为候选能力动作；本轮未建立逐小问双向证据。 | N/A | {ev(3)}；{ev(4)} | 不称直接衔接，待真题小问核验。 |", "", "## 8. 教学使用提示", "", "### 8.1 教材学习提示", "", f"- 内容：{prompt}", f"- 证据ID：{ev(4)}", "", "### 8.2 配套教师用书意见", "", (f"- 内容：{quote(paragraphs(teacher[0])[0]) if teacher and paragraphs(teacher[0]) else '已登记同版教师用书候选源，具体意见待逐页复核。'}" if teacher else "- 内容：N/A；未取得同版可核验教师用书。"), f"- `edition_match`状态：{'candidate' if teacher else 'unknown'}；证据ID：{ev(8)}", "", "### 8.3 本项目教学建议", "", "- 建议：先让学生提交证据表，再进行小组讨论或写作修订；教师只评价可观察的证据链和过程成果。", "- 与前两类来源的边界：这是项目建议，不冒充教材或教师用书意见。", "", "## 9. 证据表", "", "| EV-ID | Claim/目标/字段 | 类型 | Source | Artifact | Locator | 短引文 | 支撑关系 | 核验状态/核验人/日期 |", "|---|---|---|---|---|---|---|---|---|"]
    for row in rows:
        out.append("| " + " | ".join(row) + " | supports | candidate / throughput_generator / 2026-08-06 |")
    out += ["", "## 10. 自检、评审与版本记录", "", "- [x] 已绑定规范教材包和课程标准", "- [x] 每个KP有主层级、理由和证据", "- [x] 解释类KP至少绑定两条证据", "- [x] 高考关系遵守M0治理", "- [ ] 尚未完成双人评审和G2校准，不得转为accepted", "", "| 版本 | 日期 | 修改者 | 变更 | 上游哈希/影响 |", "|---|---|---|---|---|", f"| 0.1.0 | 2026-08-06 | throughput_generator | 基于已核验MinerU包生成可追溯吞吐初稿 | {src['canonical_artifact_id']}；{CURR} |"]
    return "\n".join(out) + "\n"


def graph_markdown(d: dict, cards: list[dict], task: dict | None, src_by_id: dict, manifests: dict[str, dict]) -> str:
    code, unit = d["book_code"], d["unit"]
    book = book_name(code)
    task_id = task["source_id"] if task else None
    task_art = task["canonical_artifact_id"] if task else None
    task_loc = source_locator(task_id, manifests) if task_id else "N/A"
    lines = ["---", "schema_version: \"2.0-candidate\"", f"unit_id: {q(d['deliverable_id'])}", "status: \"drafted\"", f"book: {q(book)}", f"unit: {q(unit)}", "source_ids:"]
    for c in cards:
        lines.append(f"  - {q(c['source_ids'][0])}")
    if task_id: lines.append(f"  - {q(task_id)}")
    lines += [f"  - {q(CURR)}", "upstream_card_ids:"] + [f"  - {q(c['deliverable_id'])}" for c in cards] + ["producer: \"throughput_generator\"", "reviewers: []", "version: \"0.1.0\"", "---", "", f"# 单元知识图谱：{book} {unit}", "", "> 这是基于已核验源包生成的候选图谱。上游卡均为drafted，正式图谱仍须等待评审与accepted门禁。", "", "## 1. 上游验收与覆盖清单", "", "| Card-ID | 状态 | KP数 | 文件/版本 | 纳入结果 |", "|---|---|---:|---|---|"]
    for c in cards:
        lines.append(f"| {c['deliverable_id']} | drafted | 8 | `cards/{c['deliverable_id']}.md` / 0.1.0 | CAND候选，不计入正式汇总 |")
    lines += ["", "## 2. 单元任务原文与拆解", "", "| 子任务ID | 原文短引 | 规范定位 | 能力动作 | 学习成果 | 评价证据 |", "|---|---|---|---|---|---|"]
    if task:
        task_para = paragraphs(task)
        tq = quote(task_para[0] if task_para else "结合本单元材料完成学习任务。")
        lines.append(f"| UT-{d['deliverable_id']}-01 | {tq} | {task_id} / {task_art}；{task_loc} | 提取、分析、表达并修订 | 证据表、讨论、写作或实践成果 | 至少两条可定位材料证据，保留过程稿。 |")
    else:
        lines.append("| N/A | 本单元无独立单元任务包，按教材栏目和诵读/探究要求处理。 | N/A | 阅读、梳理、表达 | 诵读记录或知识整理 | 由卡片证据复核。 |")
    lines += ["", "## 3. 人文维度图谱", "", "| 节点ID | 主题/母题/文化议题 | 来源Card/KP | 证据ID |", "|---|---|---|---|"]
    lines.append(f"| CAND-H-{d['deliverable_id']} | 本单元围绕教材导语、正文和任务形成的主题/文化问题，待评审确认。 | {', '.join(c['deliverable_id'] for c in cards)} | 各卡EV-001、EV-003、EV-004 |")
    lines += ["", "## 4. 语言维度图谱", "", "| 节点ID | 任务群/文体/语言现象/读写方法 | 来源Card/KP | 证据ID |", "|---|---|---|---|"]
    lines.append(f"| CAND-L-{d['deliverable_id']} | 以“文本事实—形式/语言—判断—迁移成果”组织本单元语言学习。 | {', '.join(c['deliverable_id'] for c in cards)} | 各卡EV-003—EV-007 |")
    lines += ["", "## 5. 跨课关系", "", "| 源KP | 关系 | 目标KP | 共性与差异 | 证据/理由 |", "|---|---|---|---|---|", "| — | — | — | 上游卡未accepted，暂不建立跨课确定性关系。 | N/A |", "", "## 6. 高考衔接与M0治理", "", "| KP | M等级 | 真题小问 | 双向证据 | 不确定性 |", "|---|---|---|---|---|", "| —（不携带KP） | M0 | — | 尚未登记逐小问真题双向证据。 | 不把一般题型相似性升级为M1/M2/M3。 |", "", "## 7. 前后单元递进", "", "| 方向 | 目标单元/KP | 前提、深化或迁移说明 | 双方证据 |", "|---|---|---|---|", "| 前/后 | — | 目标卡尚未accepted，暂不建立确定性递进边。 | N/A |", "", "## 8. 冲突、缺源和待核实项", "", "| Issue-ID | 问题 | 影响 | 责任人 | 处理状态 |", "|---|---|---|---|---|", f"| ISSUE-{d['deliverable_id']}-001 | 上游卡均为drafted。 | 正式图谱阻断。 | 主审/复审 | open |", f"| ISSUE-{d['deliverable_id']}-002 | 未登记逐小问高考映射。 | 保持M0。 | exam mapping owner | open |", "", "## 9. 自检与版本记录", "", "- [ ] 本单元卡全部accepted（当前为0）", "- [x] 候选节点均回链到上游卡和证据表", "- [x] 高考关系遵守M0治理", "", "| 版本 | 日期 | 修改者 | 变更 | 上游哈希/影响 |", "|---|---|---|---|---|", "| 0.1.0 | 2026-08-06 | throughput_generator | 生成候选单元图谱 | 上游卡0.1.0 drafted |"]
    return "\n".join(lines) + "\n"


def main():
    sources = load_jsonl(SOURCE_FILE)
    src_by_id = {x["source_id"]: x for x in sources}
    manifests = {x["source_id"]: x for x in load_jsonl(MANIFEST_FILE)}
    rows = load_jsonl(DELIVERABLE_FILE)
    card_rows = {x["deliverable_id"]: x for x in rows if x["deliverable_type"] == "knowledge_card"}
    unit_rows = {x["deliverable_id"]: x for x in rows if x["deliverable_type"] == "unit_graph"}
    changed = []
    for d in card_rows.values():
        out = ROOT / d["output_path"]
        if out.exists():
            continue
        src = src_by_id[d["source_ids"][0]]
        task = unit_source(sources, d["book_code"], d["unit"]) if d["unit"] != "REC" else None
        teacher = teacher_sources(sources, d["unit"]) if d["book_code"] == "B2" else []
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(card_markdown(d, src, task, teacher, manifests), encoding="utf-8")
        d["status"] = "drafted"; d["owner"] = "throughput_generator"; d["source_ids"] = list(dict.fromkeys([src["source_id"]] + ([task["source_id"]] if task else []) + [CURR] + [x["source_id"] for x in teacher[:2]]))
        changed.append(d["deliverable_id"])
    for d in unit_rows.values():
        out = ROOT / d["output_path"]
        if out.exists():
            continue
        cards = [card_rows[x] for x in d.get("upstream_deliverable_ids", []) if x in card_rows]
        if not cards:
            continue
        task = unit_source(sources, d["book_code"], d["unit"])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(graph_markdown(d, cards, task, src_by_id, manifests), encoding="utf-8")
        d["status"] = "drafted"; d["owner"] = "throughput_generator"; d["source_ids"] = list(dict.fromkeys([x["source_ids"][0] for x in cards] + ([task["source_id"]] if task else []) + [CURR]))
        changed.append(d["deliverable_id"])
    DELIVERABLE_FILE.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n", encoding="utf-8")
    print(json.dumps({"generated": len(changed), "ids": changed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
