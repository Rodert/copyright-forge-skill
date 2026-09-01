#!/usr/bin/env python3
"""Render a portable, user-facing HTML quality report from reviewer JSON."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def items(title: str, findings: list[dict]) -> str:
    rows = "".join(f"<li><strong>{html.escape(str(item.get('code', 'CHECK')))}</strong> {html.escape(str(item.get('message', '')))} {html.escape(str(item.get('path', '')))}</li>" for item in findings)
    return f"<section><h2>{title}</h2><ul>{rows or '<li>无</li>'}</ul></section>"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    review = json.loads(args.review.read_text(encoding="utf-8"))
    gate_rows = "".join(f"<tr><td>{html.escape(gate['id'])}</td><td>{html.escape(gate['name'])}</td><td>{html.escape(gate['status'])}</td></tr>" for gate in review.get("gates", []))
    page = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Copyright Forge Quality Report</title><style>body{{max-width:900px;margin:48px auto;padding:0 24px;font:16px/1.6 system-ui;color:#17241f}}header{{border-bottom:2px solid #2f6756}}.score{{font-size:48px;color:#2f6756;font-weight:700}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #c4d0c8;text-align:left}}li{{margin:.5em 0}}strong{{color:#a54a2a}}</style><header><p>Copyright Forge</p><h1>材料质量报告</h1><p class="score">{review.get('quality_score', 0)} / 100</p><p>{html.escape(str(review.get('quality_label', review.get('status', ''))))}</p></header><section><h2>八道质量门</h2><table><thead><tr><th>ID</th><th>检查项</th><th>状态</th></tr></thead><tbody>{gate_rows}</tbody></table></section>{items('阻断问题', review.get('blockers', []))}{items('需要注意', review.get('warnings', []))}</html>'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
