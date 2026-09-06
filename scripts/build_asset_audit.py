#!/usr/bin/env python3
"""Generate a readable asset coverage report from the project manifest."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    chapters = json.loads((ROOT / "data/chapters.json").read_text(encoding="utf-8"))["chapters"]
    manifest = json.loads((ROOT / "data/image-manifest.json").read_text(encoding="utf-8"))["images"]
    by_chapter: dict[int, set[int]] = defaultdict(set)
    for item in manifest:
        if item.get("chapter") is not None and item.get("page") is not None and item.get("review_status") != "superseded":
            by_chapter[item["chapter"]].add(item["page"])

    lines = [
        "# 图片资产审计",
        "",
        "本报告由 `scripts/build_asset_audit.py` 生成。‘已对应’只表示章页身份可靠恢复，不代表图片中文字已经最终审核。",
        "",
        "| 章 | 章节 | 计划页 | 已对应页 | 缺失或未对应页 |",
        "|---:|---|---:|---|---|",
    ]
    for chapter in chapters:
        pages = by_chapter.get(chapter["number"], set())
        missing = [str(i) for i in range(1, chapter["pages"] + 1) if i not in pages]
        lines.append(
            f"| {chapter['number']} | {chapter['title']} | {chapter['pages']} | "
            f"{', '.join(map(str, sorted(pages))) or '—'} | {', '.join(missing) or '—'} |"
        )
    unmapped = sum(1 for item in manifest if item.get("review_status") == "needs_mapping")
    reference = sum(1 for item in manifest if item.get("asset_role") == "visual_reference")
    lines += ["", f"- 待人工对应候选图：{unmapped}张。", f"- 视觉参考图：{reference}张。", ""]
    (ROOT / "docs/asset-audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote docs/asset-audit.md")


if __name__ == "__main__":
    main()
