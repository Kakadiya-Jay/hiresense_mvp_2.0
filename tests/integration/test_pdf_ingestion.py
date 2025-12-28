# tests/ingestion/test_pdf_ingestion.py

import os
import pytest

from src.ingestion.pdf_extractor import extract_text_from_pdf
from src.ingestion.ocr_fallback import extract_text_with_ocr


ASSETS_DIR = "tests/assets"


def test_digital_pdf_extraction_ok():
    """
    Digital PDF should be extracted via PyMuPDF without OCR.
    """
    pdf_path = os.path.join(ASSETS_DIR, "digital_resume.pdf")
    result = extract_text_from_pdf(pdf_path)

    assert result["status"] == "OK"
    assert result["char_count"] > 200
    assert result["num_pages"] > 0
    assert result["block_count"] > 0
    assert isinstance(result["raw_text"], str)


def test_scanned_pdf_triggers_empty():
    """
    Scanned PDF should return EMPTY from PDF extractor.
    """
    pdf_path = os.path.join(ASSETS_DIR, "scanned_resume.pdf")
    result = extract_text_from_pdf(pdf_path)

    assert result["status"] == "EMPTY"
    assert result["char_count"] < 200


def test_scanned_pdf_ocr_fallback_success():
    """
    OCR should successfully extract text from scanned PDF.
    """
    pdf_path = os.path.join(ASSETS_DIR, "scanned_resume.pdf")
    ocr_result = extract_text_with_ocr(pdf_path)

    assert ocr_result["status"] == "OK"
    assert ocr_result["char_count"] > 100
    assert isinstance(ocr_result["ocr_text"], str)


def test_broken_pdf_fails_cleanly():
    """
    Invalid PDF should fail loudly and predictably.
    """
    pdf_path = os.path.join(ASSETS_DIR, "broken.pdf")
    result = extract_text_from_pdf(pdf_path)

    assert result["status"] == "FAILED"
    assert result["error"] is not None
