#!/usr/bin/env python3
"""Create a basic paginated DOCX source-program artifact using only stdlib."""
from __future__ import annotations

import argparse
import html
import zipfile
from pathlib import Path


CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'''
RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''


def paragraph(text: str, page_break: bool = False) -> str:
    content = html.escape(text)
    break_xml = '<w:r><w:br w:type="page"/></w:r>' if page_break else ""
    return f'<w:p><w:pPr><w:spacing w:after="0" w:line="220"/></w:pPr>{break_xml}<w:r><w:rPr><w:rFonts w:ascii="Courier New" w:eastAsia="SimSun"/><w:sz w:val="14"/></w:rPr><w:t xml:space="preserve">{content}</w:t></w:r></w:p>'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_text", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pages = args.source_text.read_text(encoding="utf-8").split("\f")
    body = []
    for index, page in enumerate(pages):
        for line_index, line in enumerate(page.strip().splitlines()):
            body.append(paragraph(line, page_break=index > 0 and line_index == 0))
    document = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + "".join(body) + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1020" w:right="1020" w:bottom="1020" w:left="1020"/></w:sectPr></w:body></w:document>'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", CONTENT_TYPES)
        archive.writestr("_rels/.rels", RELS)
        archive.writestr("word/document.xml", document)


if __name__ == "__main__":
    main()
