# src/ingestion/text_cleaner.py

import re
import unicodedata
from collections import Counter
from typing import List


def _normalize_unicode(text: str) -> str:
    """
    Normalize unicode characters (e.g., smart quotes, ligatures).
    """
    return unicodedata.normalize("NFKC", text)


def _fix_broken_lines(text: str) -> str:
    """
    Fix line breaks where sentences are broken mid-line,
    while preserving real paragraph breaks.
    """
    lines = text.splitlines()
    fixed_lines: List[str] = []

    buffer = ""

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if buffer:
                fixed_lines.append(buffer.strip())
                buffer = ""
            fixed_lines.append("")
            continue

        # If line ends with hyphen, join directly (word break)
        if stripped.endswith("-"):
            buffer += stripped[:-1]
        else:
            # If buffer exists, decide whether to merge
            if buffer:
                # Merge if previous line does not end sentence
                if not re.search(r"[.!?:]$", buffer):
                    buffer += " " + stripped
                else:
                    fixed_lines.append(buffer.strip())
                    buffer = stripped
            else:
                buffer = stripped

    if buffer:
        fixed_lines.append(buffer.strip())

    return "\n".join(fixed_lines)


def _remove_repeated_headers_footers(text: str, threshold: int = 3) -> str:
    """
    Remove repeated lines (headers/footers) that appear on many pages.
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    counts = Counter(lines)

    repeated = {line for line, cnt in counts.items() if cnt >= threshold}

    cleaned_lines = [line for line in text.splitlines() if line.strip() not in repeated]

    return "\n".join(cleaned_lines)


def clean_text(raw_text: str, preserve_case: bool = True) -> str:
    """
    Clean raw extracted text without destroying semantic structure.
    """

    if not raw_text or not raw_text.strip():
        return ""

    text = _normalize_unicode(raw_text)

    text = _fix_broken_lines(text)

    text = _remove_repeated_headers_footers(text)

    # Normalize excessive whitespace (but keep line breaks)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    if not preserve_case:
        text = text.lower()

    return text.strip()
