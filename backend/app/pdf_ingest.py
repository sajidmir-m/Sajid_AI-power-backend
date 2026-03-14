from __future__ import annotations

import re
from typing import Iterable

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF. For a prototype, plain text extraction is sufficient.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    parts: list[str] = []
    for page in doc:
        parts.append(page.get_text("text"))
    doc.close()
    return "\n".join(parts)


_whitespace_re = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """
    Normalize whitespace and remove obvious extraction artifacts while keeping content intact.
    """
    text = text.replace("\u00ad", "")  # soft hyphen
    text = text.replace("\r", "\n")
    text = _whitespace_re.sub(" ", text)
    return text.strip()


def iter_words(text: str) -> Iterable[str]:
    for w in text.split(" "):
        w = w.strip()
        if w:
            yield w

