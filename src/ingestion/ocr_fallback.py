# src/ingestion/ocr_fallback.py

from typing import Dict
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_with_ocr(pdf_path: str) -> Dict:
    """
    Perform OCR on scanned PDFs using Tesseract.
    """

    ocr_text_parts = []

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")

            image = Image.open(io.BytesIO(img_bytes))
            text = pytesseract.image_to_string(image)

            if text.strip():
                ocr_text_parts.append(text)

        ocr_text = "\n".join(ocr_text_parts)
        char_count = len(ocr_text)

        if char_count == 0:
            return {
                "ocr_text": "",
                "char_count": 0,
                "status": "FAILED",
                "error": "OCR produced no text",
            }

        return {
            "ocr_text": ocr_text,
            "char_count": char_count,
            "status": "OK",
            "error": None,
        }

    except Exception as e:
        return {"ocr_text": "", "char_count": 0, "status": "FAILED", "error": str(e)}
