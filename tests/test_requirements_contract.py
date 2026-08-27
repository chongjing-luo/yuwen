"""CI环境契约：tests模块级导入闭包内的第三方依赖必须由requirements.txt声明。

问题来源：2026-08-25公开仓库CI selfcheck失败——测试模块顶层导入jsonschema但
requirements.txt未声明；本地系统Python恰好装有该包而全绿，CI全新环境在pytest
收集阶段即崩。本测试以requirements.txt文本为契约判定，不依赖当前环境的已装包，
防止同类"本地可用、CI缺失"的依赖漂移再次进入main。
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIREMENTS = ROOT / "requirements.txt"
TEST_GLOB = "tests/test_*.py"
LOCAL_PY_GLOBS = ("scripts/*.py", "scripts/checks/*.py", "tests/*.py", "*.py")

# requirements发行名到import名的归一化（大小写不敏感之外还需映射的仅有这些）。
DISTRIBUTION_TO_IMPORT = {
    "pyyaml": "yaml",
    "python-pptx": "pptx",
    "pillow": "pil",
    "beautifulsoup4": "bs4",
    "pymupdf": "fitz",
}


def _declared_import_names() -> set[str]:
    names: set[str] = set()
    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        entry = line.split("#", 1)[0].strip()
        if not entry:
            continue
        distribution = entry.split()[0].split("[")[0].split(">")[0].split("=")[0].split("<")[0].split("~")[0]
        distribution = distribution.rstrip("!")
        names.add(DISTRIBUTION_TO_IMPORT.get(distribution, distribution.replace("-", "_")))
    return names


def _module_scope_imports(path: Path) -> set[str]:
    """只看模块级import；函数内惰性import不进pytest收集失败面，不在此契约内。"""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    return names


def _local_module_names() -> tuple[set[str], dict[str, Path]]:
    """仓库内可导入对象：模块名与顶层目录名（如scripts命名空间包）。"""
    modules: dict[str, Path] = {}
    names: set[str] = set()
    for pattern in LOCAL_PY_GLOBS:
        for path in ROOT.glob(pattern):
            modules.setdefault(path.stem, path)
            names.add(path.parent.name)
            names.add(path.stem)
    return names, modules


def _tests_module_scope_third_party() -> set[str]:
    local_names, local_modules = _local_module_names()
    stdlib = set(sys.stdlib_module_names)
    third_party: set[str] = set()
    queue = sorted(ROOT.glob(TEST_GLOB))
    seen: set[Path] = set()
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        for name in _module_scope_imports(path):
            if name in local_names:
                if name in local_modules:
                    queue.append(local_modules[name])
            elif name not in stdlib:
                third_party.add(name)
    return third_party


def test_tests_module_scope_third_party_imports_are_declared() -> None:
    undeclared = _tests_module_scope_third_party() - _declared_import_names()
    assert not undeclared, (
        "以下第三方包被tests模块级导入闭包引用但requirements.txt未声明，"
        "CI全新环境将在pytest收集阶段失败：\n" + "\n".join(sorted(undeclared))
    )


def test_requirements_file_exists_and_nonempty() -> None:
    lines = [
        line.split("#", 1)[0].strip()
        for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines()
        if line.split("#", 1)[0].strip()
    ]
    assert lines, "requirements.txt不得为空"
