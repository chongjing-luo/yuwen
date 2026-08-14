#!/usr/bin/env python3
"""Generate the remaining book/exam/global draft deliverables."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "work/knowledge/_meta"
DELIVERABLE = META / "deliverables.jsonl"
CURR = "SRC-CURR-2020"


def load(path):
    return [json.loads(x) for x in path.read_text(encoding="utf8").splitlines() if x.strip()]


def q(s):
    return json.dumps(s, ensure_ascii=False)


def clean(s):
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).replace("|", "／").strip()


def book(code):
    return {"B1":"必修上册","B2":"必修下册","X1":"选择性必修上册","X2":"选择性必修中册","X3":"选择性必修下册"}[code]


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding="utf8")
        return True
    return False


def book_summary(d, rows):
    code = d["book_code"]
    cards = [r for r in rows if r["deliverable_type"] == "knowledge_card" and r.get("book_code") == code]
    units = [r for r in rows if r["deliverable_type"] == "unit_graph" and r.get("book_code") == code]
    lines = ["---", "schema_version: \"2.0-candidate\"", f"deliverable_id: {q(d['deliverable_id'])}", "status: \"drafted\"", f"book: {q(book(code))}", "source_ids:", f"  - {q('SRC-MASTER-'+code)}", f"  - {q(CURR)}", "upstream_deliverable_ids:"]
    lines += [f"  - {q(x['deliverable_id'])}" for x in units] + [f"  - {q(x['deliverable_id'])}" for x in cards] + ["producer: \"throughput_generator\"", "reviewers: []", "version: \"0.1.0\"", "---", "", f"# 册级知识总表：{book(code)}", "", "> 本册总表为 drafted 汇总。所有上游卡和单元图谱尚未完成评审，故以下内容是可追溯候选索引，不是最终 accepted 知识库。", "", "## 1. 覆盖清单", "", "| 类型 | ID | 状态 | 内容 | KP/节点估计 |", "|---|---|---|---|---:|"]
    for x in units:
        lines.append(f"| 单元图谱 | {x['deliverable_id']} | {x['status']} | {x['title']} | {len([c for c in cards if c['unit']==x['unit']])*8} KP候选 |")
    for x in cards:
        lines.append(f"| 知识卡 | {x['deliverable_id']} | {x['status']} | {x['title']} | 8 KP候选 |")
    lines += ["", "## 2. 册级人文主线", "", "| 候选主线 | 证据边界 | 状态 |", "|---|---|---|", f"| 从各单元教材导语、正文、学习提示和任务中归纳本册的主题、文化议题与育人指向。 | {book(code)}规范教材包；{CURR} | 候选，待单元卡accepted后复核 |", "", "## 3. 册级语言与能力主线", "", "| 能力链 | 来源 | 状态 |", "|---|---|---|", "| 文本事实提取 → 语言/形式分析 → 证据化解释 → 表达/实践迁移。 | 各单元卡KP-003—007及图谱候选节点 | 候选，禁止当作正式覆盖率 |", "", "## 4. 高考与纵向边界", "", "- 本册卡片中的高考关系统一保持 M0，未登记逐小问双向证据。", "- 前后册递进边暂不建立，除非目标卡和双方证据均通过评审。", "- 教师用书意见仅在已登记同版源包时使用；学生学习提示不得替代教师用书。", "", "## 5. 评审门禁", "", "- [x] 单元卡、图谱和来源路径已登记。", "- [ ] 上游全部 accepted。", "- [ ] 两轮评审和G2校准完成。", "- [ ] 正式发布。", "", "| 版本 | 日期 | 修改者 | 变更 |", "|---|---|---|---|", "| 0.1.0 | 2026-08-06 | throughput_generator | 汇总本册候选卡、候选图谱和课标边界 |"]
    return "\n".join(lines)+"\n"


def exam_text(d, manifest):
    title = d["title"]
    m = re.search(r"(\d{4})", d["deliverable_id"])
    year = int(m.group(1)) if m else None
    code = "NCA" if "NCA" in d["deliverable_id"] else "NC2"
    recs = [x for x in manifest.get("records",[]) if x.get("year") == year and x.get("paper_code") == code]
    qrec = next((x for x in recs if x.get("document_role") == "question"), None)
    arec = next((x for x in recs if x.get("document_role") == "answer"), None)
    source_note = "；".join(filter(None,[f"题卷源ID：{qrec.get('source_id')}" if qrec else None, f"答案源ID：{arec.get('source_id')}" if arec else None])) or "本批清单未找到该年份可核验题卷。"
    md = Path(ROOT / qrec["mineru_full_md"]) if qrec and qrec.get("mineru_full_md") else None
    if md and not md.exists() and qrec and qrec.get("mineru_result_dir"):
        md = ROOT / qrec["mineru_result_dir"] / "full.md"
    snippet = ""
    headings = []
    if md and md.exists():
        text = md.read_text(encoding="utf8")
        headings = [clean(x) for x in re.findall(r"^#{1,3}\s+(.+)$", text, flags=re.M)[:16]]
        blocks = [clean(x) for x in re.split(r"\n\s*\n", text) if len(clean(x)) > 30]
        snippet = blocks[0][:300] if blocks else ""
    status = qrec.get("status") if qrec else "missing"
    provenance = qrec.get("source_level") if qrec else "N/A"
    lines = ["---", "schema_version: \"2.0-candidate\"", f"deliverable_id: {q(d['deliverable_id'])}", "status: \"drafted\"", f"title: {q(title)}", f"source_status: {q('acquired_unofficial' if qrec else 'missing')}", "source_ids: []", "producer: \"throughput_generator\"", "reviewers: []", "version: \"0.1.0\"", "---", "", f"# 高考语文试卷解构：{title}", "", "> 本文件是候选解构稿。高考试卷材料来自 `Data/reference/gaokao/manifest.json` 登记的转载源（S3），不是官方原卷；未取得答案或官方评分资料的小问不得建立确定性考点映射。", "", "## 1. 来源与完整性", "", f"- 题卷状态：`{status}`；来源等级：`{provenance}`。", f"- {source_note}", f"- 题卷文件：`{qrec.get('local_pdf') if qrec else 'N/A'}`", f"- MinerU结果：`{qrec.get('mineru_result_dir') if qrec else 'N/A'}`", f"- 题卷首段锚点：{snippet or '缺少可核验题卷正文。'}", "", "## 2. 结构索引（候选）", "", "| 序号 | 题卷标题/章节 | 稳定小问ID | 处理状态 |", "|---:|---|---|---|"]
    for i, h in enumerate(headings,1):
        lines.append(f"| {i} | {h} | {year}-{code}-SEC-{i:02d} | drafted；需逐小问复核 |")
    if not headings:
        lines.append("| — | 无可核验章节 | N/A | blocked；等待题卷补齐 |")
    lines += ["", "## 3. 能力动作候选", "", "| 候选动作 | 证据边界 | M等级 |", "|---|---|---|", "| 提取、概括、分析、比较、鉴赏、表达和迁移 | 仅根据题卷章节和小问逐题建立；本稿不把章节名称等同于题目要求。 | M0 |", "", "## 4. 教材KP映射", "", "| KP | 小问ID | 等级 | 双向证据 | 说明 |", "|---|---|---|---|---|", "| — | — | M0 | 未登记逐小问与教材KP的双向证据。 | 暂不建立直接衔接。 |", "", "## 5. 缺口与下一步", "", "- 需要逐小问题干、选项、答案和评分标准，建立稳定小问ID。", "- 需要核验转载源与官方/省级考试机构版本的一致性。", "- 只有完成双向证据核验后，才允许在 `MAP-EXAM-KP.md` 建立M1及以上关系。", "", "## 6. 自检与版本", "", "- [x] 已登记题卷来源状态和可信度边界。", "- [x] 缺失材料未被冒充为完整。", "- [ ] 小问级解析和教材映射待补。", "", "| 版本 | 日期 | 修改者 | 变更 |", "|---|---|---|---|", "| 0.1.0 | 2026-08-06 | throughput_generator | 生成候选结构索引和M0治理稿 |"]
    return "\n".join(lines)+"\n"


def map_text(rows):
    cards = [r for r in rows if r["deliverable_type"] == "knowledge_card"]
    exams = [r for r in rows if r["deliverable_type"] == "exam_analysis"]
    lines = ["---", "schema_version: \"2.0-candidate\"", "deliverable_id: \"MAP-EXAM-KP\"", "status: \"drafted\"", "source_ids: []", "producer: \"throughput_generator\"", "reviewers: []", "version: \"0.1.0\"", "---", "", "# 高考考点映射总表", "", "> 当前采用保守映射：没有逐小问题干、答案/评分标准和教材KP双向证据时，统一记为M0。", "", "## 1. 覆盖状态", "", "| 资源 | 数量 | 状态 |", "|---|---:|---|", f"| 教材知识卡 | {len(cards)} | drafted；未accepted |", f"| 高考解构稿 | {len(exams)} | drafted；部分材料缺口 |", "", "## 2. 映射表", "", "| Exam | 小问ID | KP-ID | 等级 | 证据状态 |", "|---|---|---|---|---|"]
    for e in exams:
        lines.append(f"| {e['deliverable_id']} | N/A | N/A | M0 | 未建立小问级双向证据 |")
    lines += ["", "## 3. 允许升级条件", "", "1. 题卷、答案和评分标准来源均可核验。", "2. 小问ID稳定且题干动作清楚。", "3. 教材KP为accepted并有双向证据。", "4. M1仅用于明确调用相同教材动作；一般题型相似性保持M0。", "", "| 版本 | 日期 | 修改者 | 变更 |", "|---|---|---|---|", "| 0.1.0 | 2026-08-06 | throughput_generator | 建立全量M0映射骨架 |"]
    return "\n".join(lines)+"\n"


def global_text(rows):
    books = [r for r in rows if r["deliverable_type"] == "book_summary"]
    cards = [r for r in rows if r["deliverable_type"] == "knowledge_card"]
    units = [r for r in rows if r["deliverable_type"] == "unit_graph"]
    lines = ["---", "schema_version: \"2.0-candidate\"", "deliverable_id: \"GLOBAL-YUWEN\"", "status: \"drafted\"", "source_ids:", "  - \"SRC-CURR-2020\"", "producer: \"throughput_generator\"", "reviewers: []", "version: \"0.1.0\"", "---", "", "# 高中语文知识体系总览", "", "> 当前总览反映候选交付覆盖，不等同于正式accepted知识图谱。", "", "## 1. 五册覆盖", "", "| 册次 | 册级总表 | 卡片 | 单元图谱 | 状态 |", "|---|---|---:|---:|---|"]
    for b in books:
        code=b['book_code']; lines.append(f"| {book(code)} | {b['deliverable_id']} | {sum(x.get('book_code')==code for x in cards)} | {sum(x.get('book_code')==code for x in units)} | drafted |")
    lines += ["", "## 2. 全局能力链", "", "1. 从教材材料和课标语境提取事实、语言形式、人物/观点与文化问题。", "2. 通过证据链完成概括、比较、鉴赏、论证、实践或文学创作。", "3. 用过程成果、反馈和修订记录评价迁移。", "4. 高考映射先以M0治理，待小问级双向证据后升级。", "", "## 3. 质量门禁", "", "- 全部教材卡和图谱当前为 `drafted`，尚未完成双人评审、G2校准和 `accepted` 转换。", "- 教师用书仅在已取得同版材料时纳入；未取得版本不填补。", "- 课程标准统一使用《普通高中语文课程标准（2017年版2020年修订）》。", "", "## 4. 关联交付", "", "- 册级总表：BOOK-B1、BOOK-B2、BOOK-X1、BOOK-X2、BOOK-X3。", "- 高考映射：MAP-EXAM-KP；当前全部M0。", "", "| 版本 | 日期 | 修改者 | 变更 |", "|---|---|---|---|", "| 0.1.0 | 2026-08-06 | throughput_generator | 建立五册覆盖、能力链和质量门禁总览 |"]
    return "\n".join(lines)+"\n"


def main():
    rows = load(DELIVERABLE)
    manifest = json.loads((ROOT/"Data/reference/gaokao/manifest.json").read_text(encoding="utf8"))
    changed=[]
    for d in rows:
        path=ROOT/d["output_path"]
        if d["deliverable_type"]=="book_summary" and write(path,book_summary(d,rows)):
            d["status"]="drafted"; d["owner"]="throughput_generator"; d["source_ids"]=["SRC-MASTER-"+d["book_code"],CURR]; changed.append(d["deliverable_id"])
        elif d["deliverable_type"]=="exam_analysis" and write(path,exam_text(d,manifest)):
            d["status"]="drafted"; d["owner"]="throughput_generator"; changed.append(d["deliverable_id"])
        elif d["deliverable_type"]=="exam_kp_mapping" and write(path,map_text(rows)):
            d["status"]="drafted"; d["owner"]="throughput_generator"; changed.append(d["deliverable_id"])
        elif d["deliverable_type"]=="global_map" and write(path,global_text(rows)):
            d["status"]="drafted"; d["owner"]="throughput_generator"; d["source_ids"]=[CURR]; changed.append(d["deliverable_id"])
    DELIVERABLE.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf8")
    print(json.dumps({"generated":len(changed),"ids":changed},ensure_ascii=False))


if __name__ == "__main__": main()
