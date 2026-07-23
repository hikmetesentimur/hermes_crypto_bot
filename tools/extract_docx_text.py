#!/usr/bin/env python3
"""Extract paragraph and table text from a DOCX file into Markdown.

Usage:
    python3 tools/extract_docx_text.py input.docx output.md

Only Python's standard library is required.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": WORD_NS}


def node_text(node: ET.Element) -> str:
    parts: list[str] = []
    for child in node.iter():
        if child.tag == f"{{{WORD_NS}}}t" and child.text:
            parts.append(child.text)
        elif child.tag == f"{{{WORD_NS}}}tab":
            parts.append("\t")
        elif child.tag in {f"{{{WORD_NS}}}br", f"{{{WORD_NS}}}cr"}:
            parts.append("\n")
    return "".join(parts).strip()


def extract_blocks(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))

    body = root.find("w:body", NS)
    if body is None:
        raise ValueError("DOCX document body was not found")

    blocks: list[str] = []
    for child in body:
        if child.tag == f"{{{WORD_NS}}}p":
            text = node_text(child)
            if text:
                blocks.append(text)
        elif child.tag == f"{{{WORD_NS}}}tbl":
            rows: list[list[str]] = []
            for row in child.findall("w:tr", NS):
                cells = [node_text(cell).replace("\n", " ") for cell in row.findall("w:tc", NS)]
                if any(cells):
                    rows.append(cells)
            if rows:
                width = max(len(row) for row in rows)
                normalized = [row + [""] * (width - len(row)) for row in rows]
                blocks.append("| " + " | ".join(normalized[0]) + " |")
                blocks.append("| " + " | ".join(["---"] * width) + " |")
                blocks.extend("| " + " | ".join(row) + " |" for row in normalized[1:])
    return blocks


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: extract_docx_text.py INPUT.docx OUTPUT.md", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    blocks = extract_blocks(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "# Kripto Trading Bot Site Senaryosu — Ham Metin\n\n"
        "> Bu dosya, kullanıcı tarafından sağlanan Word belgesinin aranabilir metin kopyasıdır. "
        "Anlamı değiştirilmeden saklanır; düzenlenmiş gereksinimler ayrı belgelerde tutulur.\n\n"
        + "\n\n".join(blocks)
        + "\n",
        encoding="utf-8",
    )
    print(f"Extracted {len(blocks)} blocks to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
