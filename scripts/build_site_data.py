#!/usr/bin/env python3
"""Build the dependency-free site/data.js file from JSON sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "site" / "data.js"


def load(name: str):
    path = ROOT / "data" / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def render() -> str:
    payload = {
        "chapters": load("chapters.json"),
        "images": load("image-manifest.json"),
        "corrections": load("corrections.json"),
    }
    return "window.JIESHIWEI_DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != content:
            raise SystemExit("site/data.js is stale; run scripts/build_site_data.py")
        print("site/data.js is current")
        return
    TARGET.write_text(content, encoding="utf-8")
    print("wrote site/data.js")


if __name__ == "__main__":
    main()
