#!/usr/bin/env python3
"""Render source-material.txt into a paginated PDF without touching project code."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_text", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise SystemExit("PDF rendering requires reportlab. Install it in the Agent runtime before rendering.") from exc
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    pages = args.source_text.read_text(encoding="utf-8").split("\f")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    document = canvas.Canvas(str(args.output), pagesize=A4)
    width, height = A4
    for page in pages:
        y = height - 42
        for line in page.strip().splitlines():
            document.setFont("STSong-Light" if any(ord(char) > 127 for char in line) else "Courier", 7)
            document.drawString(42, y, line[:150])
            y -= 10
        document.showPage()
    document.save()


if __name__ == "__main__":
    main()
