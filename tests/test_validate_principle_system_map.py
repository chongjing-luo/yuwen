from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "checks" / "validate_principle_system_map.py"
SYSTEM_MAP = ROOT / "work" / "methodology" / "lesson-preparation" / "原则体系.md"
CANONICAL = ROOT / "work" / "methodology" / "lesson-preparation" / "备课基本原则.md"
REGISTRY = ROOT / "work" / "principles" / "registry.yaml"


def run_checker(system_map: Path):
    return subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            "--map",
            str(system_map),
            "--canonical",
            str(CANONICAL),
            "--registry",
            str(REGISTRY),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_current_principle_system_partitions_all_47_principles_once():
    result = run_checker(SYSTEM_MAP)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "47/47" in result.stdout


def test_duplicate_primary_assignment_reports_both_duplicate_and_missing(tmp_path):
    broken = SYSTEM_MAP.read_text(encoding="utf-8").replace(
        "条款：P-02 原文主线", "条款：P-01 原文主线", 1
    )
    broken_path = tmp_path / "broken_principle_system.md"
    broken_path.write_text(broken, encoding="utf-8")

    result = run_checker(broken_path)
    assert result.returncode != 0
    assert "重复主归属: P-01" in result.stdout
    assert "缺少主归属: P-02" in result.stdout


def test_each_domain_requires_explicit_valid_mechanism_nodes(tmp_path):
    broken = SYSTEM_MAP.read_text(encoding="utf-8").replace(
        "机制节点：K1 教什么界定", "机制节点缺失：K1 教什么界定", 1
    )
    broken_path = tmp_path / "broken_mechanism_map.md"
    broken_path.write_text(broken, encoding="utf-8")

    result = run_checker(broken_path)
    assert result.returncode != 0
    assert "域一缺少机制节点" in result.stdout


def test_each_domain_requires_the_complete_registry_node_union(tmp_path):
    broken = SYSTEM_MAP.read_text(encoding="utf-8").replace(
        "K1 教什么界定｜K2 情境锚定｜K5 负荷预算｜U2 证据锚定｜J1 自主感｜J4 文学愉悦",
        "K1 教什么界定｜K2 情境锚定｜K5 负荷预算｜U2 证据锚定｜J1 自主感",
        1,
    )
    broken_path = tmp_path / "missing_domain_node.md"
    broken_path.write_text(broken, encoding="utf-8")

    result = run_checker(broken_path)
    assert result.returncode != 0
    assert "域一机制节点遗漏" in result.stdout
    assert "J4" in result.stdout


def test_each_domain_rejects_nodes_not_bound_to_its_principles(tmp_path):
    broken = SYSTEM_MAP.read_text(encoding="utf-8").replace(
        "K1 教什么界定｜K2 情境锚定｜K5 负荷预算｜U2 证据锚定｜J1 自主感｜J4 文学愉悦",
        "K1 教什么界定｜K2 情境锚定｜K5 负荷预算｜U1 生成先于告知｜U2 证据锚定｜J1 自主感｜J4 文学愉悦",
        1,
    )
    broken_path = tmp_path / "extra_domain_node.md"
    broken_path.write_text(broken, encoding="utf-8")

    result = run_checker(broken_path)
    assert result.returncode != 0
    assert "域一机制节点越界" in result.stdout
    assert "U1" in result.stdout


def test_global_selfcheck_runs_the_principle_system_map_gate(tmp_path: Path):
    report_path = tmp_path / "selfcheck.md"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_selfcheck.py",
            "--skip-tests",
            "--report-path",
            str(report_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert "原则体系映射" in result.stdout
    report = report_path.read_text(encoding="utf-8")
    assert "⏭️ 全量测试（pytest）" in report
    assert "✅ 全量测试（pytest）" not in report
    assert result.returncode != 0
    assert "部分检查未执行" in result.stdout
