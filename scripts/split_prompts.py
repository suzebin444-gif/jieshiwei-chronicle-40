#!/usr/bin/env python3
"""Split chapter blocks from prompts/MASTER-PROMPT.md into chapter files."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "prompts" / "MASTER-PROMPT.md"
OUT = ROOT / "prompts" / "chapters"


def main() -> None:
    text = MASTER.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(?ms)^### 第(?P<number>\d+)章《(?P<title>[^》]+)》｜(?P<period>[^｜]+)｜(?P<pages>\d+)页\s*\n"
        r"(?P<body>.*?)(?=^### 第\d+章|^## 五、|\Z)"
    )
    blocks = list(pattern.finditer(text))
    if not blocks:
        raise SystemExit("No chapter blocks found in MASTER-PROMPT.md")

    OUT.mkdir(parents=True, exist_ok=True)
    for match in blocks:
        number = int(match.group("number"))
        title = match.group("title")
        period = match.group("period")
        pages = match.group("pages")
        body = match.group("body").strip()
        content = (
            f"# 第{number}章《{title}》\n\n"
            f"- 年代：{period}\n"
            f"- 计划页数：{pages}\n"
            f"- 状态：章节提示词已整理，逐页生成时需叠加全局母提示词\n\n"
            f"{body}\n"
        )
        (OUT / f"ch-{number:02d}.md").write_text(content, encoding="utf-8")

    print(f"wrote {len(blocks)} chapter prompt files")


if __name__ == "__main__":
    main()
