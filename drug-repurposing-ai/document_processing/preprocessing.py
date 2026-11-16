"""Document preprocessing — orchestrates PDF parsing, OCR, and text cleaning.

This is the main entry point for processing any uploaded document.
Routes to the correct extraction method based on file type and content.
"""

import logging
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List

from document_processing.pdf_parser import (
    extract_text_from_pdf,
    extract_page_as_image,
    PDFResult,
)
from document_processing.ocr import (
    extract_text_from_image,
    configure_tesseract,
    is_tesseract_available,
)

logger = logging.getLogger(__name__)


@dataclass
class DocumentResult:
    """Final result of document processing."""
    report_id: str
    raw_text: str
    cleaned_text: str
    num_pages: int
    has_text: bool
    has_images: bool
    extraction_method: str  # "pdf_text", "ocr", "direct_text", "pdf_text+ocr"
    confidence: Optional[float] = None
    warnings: List[str] = field(default_factory=list)


def process_document(file_path: str, report_id: str, tesseract_cmd: Optional[str] = None) -> DocumentResult:
    """Process an uploaded document and extract text.

    Automatically detects file type and routes to the appropriate
    extraction method:
    - .txt → direct text reading
    - .pdf → PyMuPDF text extraction (+ OCR for scanned pages)
    - .jpg/.jpeg/.png → OCR

    Args:
        file_path: Path to the uploaded file.
        report_id: Unique report identifier.
        tesseract_cmd: Optional path to Tesseract executable.

    Returns:
        DocumentResult with extracted and cleaned text.
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if tesseract_cmd:
        configure_tesseract(tesseract_cmd)

    if ext == ".txt":
        return _process_text_file(path, report_id)
    elif ext == ".pdf":
        return _process_pdf(path, report_id)
    elif ext in {".jpg", ".jpeg", ".png"}:
        return _process_image(path, report_id)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _process_text_file(path: Path, report_id: str) -> DocumentResult:
    """Process a plain text file."""
    raw_text = path.read_text(encoding="utf-8", errors="replace")
    cleaned = clean_text(raw_text)

    return DocumentResult(
        report_id=report_id,
        raw_text=raw_text,
        cleaned_text=cleaned,
        num_pages=1,
        has_text=bool(cleaned.strip()),
        has_images=False,
        extraction_method="direct_text",
        confidence=1.0,
    )


def _process_pdf(path: Path, report_id: str) -> DocumentResult:
    """Process a PDF file — extract text, OCR scanned pages."""
    pdf_result: PDFResult = extract_text_from_pdf(str(path))
    warnings = []

    # If there are scanned pages, try OCR on them
    ocr_texts = []
    method = "pdf_text"

    if pdf_result.scanned_pages:
        if is_tesseract_available():
            method = "pdf_text+ocr"
            for page_num in pdf_result.scanned_pages:
                try:
                    page_img = extract_page_as_image(str(path), page_num, dpi=300)
                    ocr_result = extract_text_from_image(page_img)
                    if ocr_result["text"]:
                        ocr_texts.append(f"[Page {page_num} - OCR]\n{ocr_result['text']}")
                except Exception as e:
                    warnings.append(f"OCR failed on page {page_num}: {str(e)}")
                    logger.warning(f"OCR failed on page {page_num}: {e}")
        else:
            warnings.append(
                f"Pages {pdf_result.scanned_pages} appear to be scanned images "
                "but Tesseract OCR is not available. Install Tesseract for better extraction."
            )

    # If no text was extracted at all, and there are images, try full OCR
    if not pdf_result.has_text and not ocr_texts:
        if is_tesseract_available():
            method = "ocr"
            for page_num in range(1, pdf_result.num_pages + 1):
                try:
                    page_img = extract_page_as_image(str(path), page_num, dpi=300)
                    ocr_result = extract_text_from_image(page_img)
                    if ocr_result["text"]:
                        ocr_texts.append(ocr_result["text"])
                except Exception as e:
                    warnings.append(f"OCR failed on page {page_num}: {str(e)}")

    # Combine all text
    text_parts = []
    if pdf_result.full_text:
        text_parts.append(pdf_result.full_text)
    text_parts.extend(ocr_texts)

    raw_text = "\n\n".join(text_parts)
    cleaned = clean_text(raw_text)

    if not cleaned.strip():
        warnings.append("No text could be extracted from the document.")

    return DocumentResult(
        report_id=report_id,
        raw_text=raw_text,
        cleaned_text=cleaned,
        num_pages=pdf_result.num_pages,
        has_text=bool(cleaned.strip()),
        has_images=pdf_result.has_images,
        extraction_method=method,
        warnings=warnings,
    )


def _process_image(path: Path, report_id: str) -> DocumentResult:
    """Process an image file using OCR."""
    warnings = []

    if not is_tesseract_available():
        return DocumentResult(
            report_id=report_id,
            raw_text="",
            cleaned_text="",
            num_pages=1,
            has_text=False,
            has_images=True,
            extraction_method="ocr",
            confidence=0.0,
            warnings=["Tesseract OCR is not installed. Cannot extract text from images."],
        )

    try:
        ocr_result = extract_text_from_image(str(path))
        raw_text = ocr_result["text"]
        cleaned = clean_text(raw_text)

        return DocumentResult(
            report_id=report_id,
            raw_text=raw_text,
            cleaned_text=cleaned,
            num_pages=1,
            has_text=bool(cleaned.strip()),
            has_images=True,
            extraction_method="ocr",
            confidence=ocr_result.get("confidence"),
            warnings=warnings,
        )
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return DocumentResult(
            report_id=report_id,
            raw_text="",
            cleaned_text="",
            num_pages=1,
            has_text=False,
            has_images=True,
            extraction_method="ocr",
            confidence=0.0,
            warnings=[f"OCR extraction failed: {str(e)}"],
        )


def clean_text(text: str) -> str:
    """Clean extracted text for downstream NLP processing.

    Steps:
    - Normalize Unicode characters
    - Fix common OCR artifacts
    - Normalize whitespace
    - Remove excessive blank lines
    - Strip leading/trailing whitespace per line

    Args:
        text: Raw extracted text.

    Returns:
        Cleaned text.
    """
    if not text:
        return ""

    # Normalize common Unicode issues
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u00a0", " ")  # Non-breaking space

    # Fix common OCR artifacts
    text = re.sub(r"[|]", "l", text)  # Pipe often misread for lowercase L
    text = re.sub(r"\b0(?=[a-z])", "O", text)  # Zero before lowercase often means O

    # Normalize whitespace within lines
    text = re.sub(r"[ \t]+", " ", text)

    # Clean up line endings
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\r", "\n", text)

    # Remove excessive blank lines (keep max 2)
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    # Strip each line
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)

    # Strip overall
    text = text.strip()

    return text
