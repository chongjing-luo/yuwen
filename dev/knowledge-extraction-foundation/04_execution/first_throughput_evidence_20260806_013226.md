# First-Throughput Evidence

- Active task: `knowledge-extraction-foundation`
- Architecture source: `work/语文备课系统_知识点提取研究计划.md` §3–§8
- User sample or fixture identity: real project record `SRC-PKG-B1-001`（必修上册《沁园春·长沙》切分包）及现有样卡对应交付 `CARD-B1-U01-01`
- Sample classification: real
- Exact bootstrap command: `python scripts/bootstrap_knowledge_infrastructure.py`
- Bootstrap exit code: `0`
- Bootstrap output: `{"packages": 144, "deliverables": 120, "sources": 152, "artifacts": 1266, "split_mappings": 144}`
- Exact validation command: `python scripts/validate_knowledge_base.py --report work/knowledge/_meta/validation_reports/first_throughput_validation_20260806_013226.json`
- Validation exit code: `0`
- Result: passed
- Output path: `work/knowledge/_meta/validation_reports/first_throughput_validation_20260806_013226.json`
- Validation run: `VAL-20260806-013236+0800`，6个检查域全部passed，0错误
- Full regression command: `python -m unittest discover -s tests -v && python -m py_compile scripts/bootstrap_knowledge_infrastructure.py scripts/validate_knowledge_base.py scripts/mineru_client.py scripts/batch_mineru.py && git diff --check`
- Full regression result: 21 tests passed；编译与diff检查通过
- Environment: Python 3.10.17；Poppler `pdftotext` 22.02.0；Linux；Asia/Shanghai
- Source snapshot: parent revision `4f053ced56c715c8e8cd8a9c7412080da8e760bc` plus the atomic foundation commit containing this evidence
- Randomness/nondeterminism: none；排序、ID、JSON键和哈希均确定性生成

## Changed files

- `scripts/bootstrap_knowledge_infrastructure.py`
- `scripts/validate_knowledge_base.py`
- `tests/test_knowledge_infrastructure.py`
- `tests/test_validate_knowledge_base.py`
- `work/knowledge/_meta/` registries, candidate contracts, rubrics and reports
- `work/knowledge/_templates/` execution/review templates
- `work/knowledge/README.md` and reference-entry README files
- this task index, implementation spec and evidence

## Exercised seams and data contracts

1. local master/split PDFs → normalized package record;
2. per-page normalized text fingerprint, with render fallback for empty pages → one-based contiguous split mapping;
3. Source → canonical Artifact → derived MinerU Artifacts;
4. package Source → knowledge-card deliverable → unit/book/global dependency graph;
5. JSONL registries + taxonomy + rubrics + schemas + templates → machine validation report;
6. real `SRC-PKG-B1-001` → planned/imported `CARD-B1-U01-01` record, retaining legacy path and `draft_existing` boundary.

## Core validation results

- 144 packages = 113 student + 31 teacher;
- 152 Sources each have exactly one verified canonical Artifact;
- 1266 Artifacts passed path, size, SHA-256 and JSON syntax checks where applicable;
- 144 split mappings passed all-page fingerprint, ordered continuity and page-count checks;
- 120 deliverables = 81 cards + 28 unit graphs + 5 book summaries + 4 exams + 1 mapping + 1 global map;
- six rubrics each total 100 points;
- accepted deliverables remain `0`, as required before calibration.

## Mock, placeholder, or pseudo-transform boundaries

- No mock records were used on the first-throughput path.
- Missing external reference families are represented by directory/readme boundaries and `source_status=missing_official_artifacts` on planned exam deliverables; no fake Source or Artifact was created.
- Content extraction and semantic scoring are intentionally not implemented in the foundation.

## Simplification-debt references

- See `implementation_spec_20260806_010616.md` §Simplification debt.
- Structural validation does not replace human review of literary interpretation or visual verification of direct quotations.

## Limitations and next breadth tasks

- Collect and register official high-school assessment framework, junior-high evidence, Sichuan policy, and 2023–2026 paper/answer/scoring artifacts.
- Resolve `REL-TB2-B2-EDITION` from `unknown` only after edition evidence exists.
- Assign owners through task packets; agents must not edit shared ledgers concurrently.
- Rework 3 existing cards and 1 graph, then complete the 10-card + 5-graph calibration before freezing contracts.

- Approval: approved
- Approval basis: user directive on 2026-08-06 to build the foundation for execution by other agents, recorded in `PROJECT_INDEX.md`
- User skip decision: no
- Skip reason: n/a
- Skip decision timestamp: n/a
