#!/usr/bin/env python3
"""Import formal pages and a deduplicated candidate catalog as compact WebP files."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def convert(source: Path, target: Path, width: int, quality: int) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp.webp")
    subprocess.run(
        ["convert", f"{source}[0]", "-auto-orient", "-strip", "-resize", f"{width}x{width}>", "-quality", str(quality), str(temporary)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if temporary.stat().st_size == 0:
        raise RuntimeError(f"conversion produced an empty file: {source}")
    temporary.replace(target)


def dimensions(path: Path) -> tuple[int, int]:
    result = subprocess.run(["identify", "-format", "%w %h", str(path)], check=True, text=True, capture_output=True)
    width, height = result.stdout.split()
    return int(width), int(height)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formal-root", type=Path, required=True)
    parser.add_argument("--catalog-root", type=Path, action="append", default=[])
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--quality", type=int, default=76)
    args = parser.parse_args()

    manifest: list[dict] = []
    formal_map = json.loads((ROOT / "data" / "formal-image-map.json").read_text(encoding="utf-8"))["images"]
    formal_hashes: set[str] = set()

    for item in formal_map:
        source = args.formal_root / item["source"]
        if not source.exists():
            raise SystemExit(f"missing formal source: {source}")
        source_hash = digest(source)
        formal_hashes.add(source_hash)
        target_rel = Path("assets/pages") / f"ch-{item['chapter']:02d}" / f"ch-{item['chapter']:02d}_p-{item['page']:03d}_v-{item['version']:02d}.webp"
        target = ROOT / target_rel
        convert(source, target, args.width, args.quality)
        width, height = dimensions(target)
        manifest.append({
            "id": f"ch{item['chapter']:02d}-p{item['page']:03d}-v{item['version']:02d}",
            "title": f"第{item['chapter']}章 第{item['page']}页",
            "file": target_rel.as_posix(),
            "chapter": item["chapter"], "page": item["page"], "version": item["version"],
            "source_filename": item["source"], "source_sha256": source_hash,
            "width": width, "height": height,
            "review_status": "needs_review", "asset_role": "formal_page_candidate",
            "note": "章页身份已恢复；图片内中文与画面仍需最终人工逐字复核"
        })

    candidates: list[tuple[str, Path]] = []
    seen: set[str] = set(formal_hashes)
    for raw_root in args.catalog_root:
        for source in sorted(raw_root.iterdir(), key=lambda p: p.name):
            if not source.is_file() or ".openai-download-" in source.name:
                continue
            try:
                source_hash = digest(source)
                dimensions(source)
            except (OSError, subprocess.CalledProcessError):
                continue
            if source_hash in seen:
                continue
            seen.add(source_hash)
            candidates.append((source_hash, source))

    for index, (source_hash, source) in enumerate(candidates, start=1):
        asset_id = f"asset-{index:04d}"
        target_rel = Path("assets/catalog") / f"{asset_id}.webp"
        target = ROOT / target_rel
        convert(source, target, args.width, args.quality)
        width, height = dimensions(target)
        manifest.append({
            "id": asset_id, "title": source.stem, "file": target_rel.as_posix(),
            "chapter": None, "page": None, "version": 1,
            "source_filename": source.name, "source_sha256": source_hash,
            "width": width, "height": height,
            "review_status": "needs_mapping", "asset_role": "recovered_candidate",
            "note": "已找回且去重；需人工确认章页、版本和文字后再提升为正式页"
        })

    reference = ROOT / "assets/references/ref-five-color-lions-01.jpg"
    if reference.exists():
        width, height = dimensions(reference)
        manifest.append({
            "id": "ref-five-color-lions-01", "title": "碣石五色狮用户原型照片",
            "file": "assets/references/ref-five-color-lions-01.jpg", "chapter": None, "page": None, "version": 1,
            "source_filename": "8c0875fb15374b7dba6043ceeeb5965a.jpg", "source_sha256": digest(reference),
            "width": width, "height": height, "review_status": "reference_only", "asset_role": "visual_reference",
            "note": "用户提供；五色狮正式页面必须以此造型为原型，不作为漫画正文页"
        })

    document = {
        "schema_version": 1,
        "summary": {"formal_page_candidates": len(formal_map), "unmapped_candidates": len(candidates), "references": 1 if reference.exists() else 0, "total": len(manifest)},
        "images": manifest,
    }
    (ROOT / "data" / "image-manifest.json").write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"imported {len(formal_map)} formal page candidates and {len(candidates)} unmapped candidates")


if __name__ == "__main__":
    main()
