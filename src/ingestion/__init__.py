# src/ingestion/__init__.py

from typing import Dict

from src.ingestion.pdf_extractor import extract_text_from_pdf
from src.ingestion.ocr_fallback import extract_text_with_ocr
from src.ingestion.text_cleaner import clean_text


def ingest_resume(pdf_path: str) -> Dict:
    """
    Orchestrates resume ingestion:
    PDF extraction → OCR fallback (if needed) → text cleaning
    """

    extraction = extract_text_from_pdf(pdf_path)

    if extraction["status"] == "FAILED":
        return {
            "status": "FAILED",
            "source": "pdf",
            "raw_text": "",
            "cleaned_text": "",
            "meta": extraction,
            "error": extraction.get("error"),
        }

    # Decide OCR fallback
    if extraction["status"] == "EMPTY":
        ocr = extract_text_with_ocr(pdf_path)

        if ocr["status"] != "OK":
            return {
                "status": "FAILED",
                "source": "ocr",
                "raw_text": "",
                "cleaned_text": "",
                "meta": ocr,
                "error": ocr.get("error"),
            }

        raw_text = ocr["ocr_text"]
        source = "ocr"
        meta = ocr

    else:
        raw_text = extraction["raw_text"]
        source = "pdf"
        meta = extraction

    cleaned_text = clean_text(raw_text, preserve_case=True)

    if not cleaned_text:
        return {
            "status": "FAILED",
            "source": source,
            "raw_text": raw_text,
            "cleaned_text": "",
            "meta": meta,
            "error": "Cleaned text is empty",
        }

    return {
        "status": "SUCCESS",
        "source": source,
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "meta": meta,
        "error": None,
    }
