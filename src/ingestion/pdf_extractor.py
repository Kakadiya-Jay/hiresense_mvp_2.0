# src/ingestion/pdf_extractor.py

from typing import Dict
import fitz  # PyMuPDF


MIN_TEXT_LENGTH = 200  # chars; below this → treat as empty
MIN_BLOCK_CHARS = 5  # ignore tiny blocks


def extract_text_from_pdf(pdf_path: str) -> Dict:
    """
    Extract text from a digital PDF using layout-aware blocks.
    OCR is NOT performed here.
    """

    raw_text_parts = []
    block_count = 0
    num_pages = 0

    try:
        doc = fitz.open(pdf_path)
        num_pages = len(doc)

        for page in doc:
            blocks = page.get_text("blocks")

            # Each block: (x0, y0, x1, y1, text, block_no, block_type)
            # Sort by vertical position, then horizontal
            blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

            for block in blocks:
                text = block[4].strip()

                if not text:
                    continue
                if len(text) < MIN_BLOCK_CHARS:
                    continue

                raw_text_parts.append(text)
                block_count += 1

        raw_text = "\n".join(raw_text_parts)
        char_count = len(raw_text)

        if char_count < MIN_TEXT_LENGTH:
            return {
                "raw_text": raw_text,
                "num_pages": num_pages,
                "block_count": block_count,
                "char_count": char_count,
                "status": "EMPTY",
                "error": None,
            }

        return {
            "raw_text": raw_text,
            "num_pages": num_pages,
            "block_count": block_count,
            "char_count": char_count,
            "status": "OK",
            "error": None,
        }

    except Exception as e:
        return {
            "raw_text": "",
            "num_pages": num_pages,
            "block_count": block_count,
            "char_count": 0,
            "status": "FAILED",
            "error": str(e),
        }
