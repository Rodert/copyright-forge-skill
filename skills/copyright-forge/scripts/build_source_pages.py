#!/usr/bin/env python3
"""Create immutable source-page text and print-ready HTML from a source selection."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from common import load_profile, write_json


def profile_value(profile: dict, field: str) -> str:
    entry = profile.get("software", {}).get(field, {})
    return str(entry.get("value", "")) if isinstance(entry, dict) else str(entry)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("selection", type=Path)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--lines-per-page", type=int, default=50)
    args = parser.parse_args()
    if args.lines_per_page < 50:
        raise SystemExit("Ordinary deposit output must use at least 50 lines per page")
    root, selection, profile = args.project.resolve(), json.loads(args.selection.read_text(encoding="utf-8")), load_profile(args.profile)
    all_lines = []
    for item in selection.get("files", []):
        path = root / item["path"]
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            all_lines.append((item["path"], number, line))
    pages = [all_lines[index:index + args.lines_per_page] for index in range(0, len(all_lines), args.lines_per_page)]
    included = list(range(len(pages))) if len(pages) < 60 else list(range(30)) + list(range(len(pages) - 30, len(pages)))
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    title = f"{profile_value(profile, 'full_name')} {profile_value(profile, 'version')}"
    text_pages, html_pages = [], []
    for display_number, page_index in enumerate(included, 1):
        rendered = []
        for path, line_number, line in pages[page_index]:
            rendered.append(f"{path}:{line_number:>5}  {line}")
        text_pages.append(f"{title}\n第 {display_number} 页\n" + "\n".join(rendered))
        html_pages.append("<section class='page'><header>" + html.escape(title) + f"<span>第 {display_number} 页</span></header><pre>" + html.escape("\n".join(rendered)) + "</pre></section>")
    (output / "source-material.txt").write_text("\n\n\f\n\n".join(text_pages) + "\n", encoding="utf-8")
    (output / "source-material.html").write_text("<!doctype html><meta charset='utf-8'><style>@page{size:A4;margin:18mm}body{font-family:monospace}.page{break-after:page}header{font-family:serif;border-bottom:1px solid #000;padding-bottom:4mm}header span{float:right}pre{font-size:8pt;line-height:1.35;white-space:pre-wrap}</style>" + "\n".join(html_pages), encoding="utf-8")
    write_json(output / "source-pages.json", {"lines_per_page": args.lines_per_page, "available_pages": len(pages), "included_original_pages": [number + 1 for number in included], "included_pages": len(included), "selection": "all" if len(pages) < 60 else "first_30_and_last_30", "header": title})


if __name__ == "__main__":
    main()
