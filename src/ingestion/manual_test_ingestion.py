# src/ingestion/manual_test_ingestion.py

from src.ingestion.pdf_extractor import extract_text_from_pdf
from src.ingestion.ocr_fallback import extract_text_with_ocr

# res = extract_text_from_pdf("data/raw/scanned_resume.pdf")
# print(f"Digital Resume: {res['status']}, {res['char_count']} chars")

# if res["status"] == "EMPTY":
#     ocr = extract_text_with_ocr("data/raw/scanned_resume.pdf")
#     print(f"Scanned Resume: {ocr['status']}, {ocr['char_count']} chars")


from src.ingestion import ingest_resume

# result = ingest_resume("data/raw/scanned_resume.pdf")
result = ingest_resume("data/raw/outline_resume.pdf")

print(result["status"])
print(result["source"])
print(len(result["cleaned_text"]))
print(result["error"])

print("*" * 5 + " META " + "*" * 5)
print(result["meta"])

print("*" * 5 + " CLEANED TEXT " + "*" * 5)
print(result["cleaned_text"])
