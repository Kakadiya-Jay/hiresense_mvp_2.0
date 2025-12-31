# src/ingestion/pdf_extractor.py

from typing import Dict
import fitz  # PyMuPDF


MIN_TEXT_LENGTH = 200  # chars; below this → treat as empty


def extract_text_from_pdf(pdf_path: str) -> Dict:
    """
    Extract text from a digital PDF using PyMuPDF's built-in
    reading-order heuristics.
    OCR is NOT performed here.
    """

    raw_text_parts = []
    num_pages = 0

    try:
        doc = fitz.open(pdf_path)
        num_pages = len(doc)

        for page in doc:
            # Use PyMuPDF's internal layout + reading-order logic
            page_text = page.get_text()

            if page_text and page_text.strip():
                raw_text_parts.append(page_text.strip())
                raw_text_parts.append("")  # page boundary

        raw_text = "\n".join(raw_text_parts).strip()
        char_count = len(raw_text)

        if char_count < MIN_TEXT_LENGTH:
            return {
                "raw_text": raw_text,
                "num_pages": num_pages,
                "block_count": 0,
                "char_count": char_count,
                "status": "EMPTY",
                "error": None,
            }

        return {
            "raw_text": raw_text,
            "num_pages": num_pages,
            "block_count": 0,  # not applicable with get_text()
            "char_count": char_count,
            "status": "OK",
            "error": None,
        }

    except Exception as e:
        return {
            "raw_text": "",
            "num_pages": num_pages,
            "block_count": 0,
            "char_count": 0,
            "status": "FAILED",
            "error": str(e),
        }
