#!/usr/bin/env python3
"""Validate chapter metadata, prompts, image manifest and referenced files."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    chapters_doc = load_json(ROOT / "data" / "chapters.json")
    chapters = chapters_doc["chapters"]

    numbers = [c["number"] for c in chapters]
    if numbers != list(range(1, 41)):
        errors.append("chapters must be numbered consecutively from 1 to 40")

    total_pages = sum(c["pages"] for c in chapters)
    if total_pages != chapters_doc["planned_pages"] or total_pages != 434:
        errors.append(f"planned page count mismatch: {total_pages}")

    for chapter in chapters:
        prompt = ROOT / "prompts" / "chapters" / f"ch-{chapter['number']:02d}.md"
        if not prompt.exists():
            errors.append(f"missing prompt: {prompt.relative_to(ROOT)}")

    manifest_path = ROOT / "data" / "image-manifest.json"
    if manifest_path.exists():
        images = load_json(manifest_path).get("images", [])
        ids = [item["id"] for item in images]
        duplicates = [key for key, count in Counter(ids).items() if count > 1]
        if duplicates:
            errors.append(f"duplicate image ids: {duplicates}")
        for item in images:
            file_path = ROOT / item["file"]
            if not file_path.exists():
                errors.append(f"missing image file: {item['file']}")
            chapter = item.get("chapter")
            page = item.get("page")
            if chapter is not None and not 1 <= chapter <= 40:
                errors.append(f"invalid chapter for {item['id']}: {chapter}")
            if chapter is not None and page is not None:
                max_pages = chapters[chapter - 1]["pages"]
                if not 1 <= page <= max_pages:
                    errors.append(f"invalid page for {item['id']}: ch{chapter} p{page}")
            if item.get("review_status") == "approved" and (chapter is None or page is None):
                errors.append(f"approved image lacks chapter/page: {item['id']}")
            if item.get("review_status") == "needs_mapping":
                warnings.append(f"unmapped candidate: {item['id']}")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"VALIDATION PASSED: 40 chapters, {total_pages} planned pages")
    if warnings:
        print(f"WARNINGS: {len(warnings)} candidate images still need mapping")
    return 0


if __name__ == "__main__":
    sys.exit(main())
