#!/usr/bin/env python3
"""CI失败注解输出器：把自检报告中的❌段落转成GitHub Actions ``::error::`` 注解。

GitHub Actions日志下载需认证，公开仓库只能匿名读到注解；本工具让CI失败原因
（哪个环节、具体错误行）直接出现在check-run注解里，无需登录即可诊断。

用法：python3 scripts/checks/emit_selfcheck_failure_annotations.py REPORT_PATH
退出码恒为0（诊断输出不改变门禁结果）。
"""
from __future__ import annotations

import sys
from pathlib import Path

MAX_ANNOTATION_CHARS = 650


def main() -> int:
    if len(sys.argv) != 2:
        return 0
    report = Path(sys.argv[1])
    if not report.is_file():
        return 0
    for section in report.read_text(encoding="utf-8").split("### ")[1:]:
        if not section.startswith("❌"):
            continue
        detail = "%0A".join(section.strip().splitlines())
        print(f"::error::{detail[:MAX_ANNOTATION_CHARS]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
