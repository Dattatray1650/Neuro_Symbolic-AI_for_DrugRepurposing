"""PDF text extraction using PyMuPDF (fitz).

Extracts text from machine-readable PDFs page-by-page.
Detects whether pages contain extractable text or are scanned images.
Handles basic table extraction where available.
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class PageResult:
    """Extraction result for a single PDF page."""
    page_number: int
    text: str
    has_text: bool
    has_images: bool
    image_count: int = 0
    tables: List[List[List[str]]] = field(default_factory=list)


@dataclass
class PDFResult:
    """Complete PDF extraction result."""
    pages: List[PageResult]
    full_text: str
    num_pages: int
    has_text: bool
    has_images: bool
    extraction_method: str = "pdf_text"
    scanned_pages: List[int] = field(default_factory=list)


def extract_text_from_pdf(file_path: str) -> PDFResult:
    """Extract text from a PDF file using PyMuPDF.

    For each page, determines whether it contains extractable text
    or is a scanned image requiring OCR.

    Args:
        file_path: Path to the PDF file.

    Returns:
        PDFResult with extracted text and metadata.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    doc = fitz.open(str(path))
    pages = []
    scanned_pages = []
    all_text_parts = []
    has_any_text = False
    has_any_images = False

    try:
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Extract text
            text = page.get_text("text").strip()

            # Count images on the page
            image_list = page.get_images(full=True)
            image_count = len(image_list)

            # Determine if page has meaningful text
            # A page with very little text but images is likely scanned
            has_text = len(text) > 20  # More than trivial text
            has_images = image_count > 0

            if has_text:
                has_any_text = True
            if has_images:
                has_any_images = True

            # If page has images but no meaningful text, mark as scanned
            if has_images and not has_text:
                scanned_pages.append(page_num + 1)

            # Try to extract tables (PyMuPDF >= 1.23)
            tables = []
            try:
                found_tables = page.find_tables()
                for table in found_tables:
                    table_data = table.extract()
                    if table_data:
                        tables.append(table_data)
            except (AttributeError, Exception):
                # find_tables() not available in older versions
                pass

            page_result = PageResult(
                page_number=page_num + 1,
                text=text,
                has_text=has_text,
                has_images=has_images,
                image_count=image_count,
                tables=tables,
            )
            pages.append(page_result)

            if text:
                all_text_parts.append(text)

    finally:
        doc.close()

    full_text = "\n\n".join(all_text_parts)

    return PDFResult(
        pages=pages,
        full_text=full_text,
        num_pages=len(pages),
        has_text=has_any_text,
        has_images=has_any_images,
        extraction_method="pdf_text",
        scanned_pages=scanned_pages,
    )


def extract_page_as_image(file_path: str, page_number: int, dpi: int = 300) -> bytes:
    """Render a PDF page as a PNG image for OCR processing.

    Args:
        file_path: Path to the PDF file.
        page_number: 1-indexed page number to render.
        dpi: Resolution for rendering (default 300 for good OCR quality).

    Returns:
        PNG image bytes.
    """
    doc = fitz.open(str(file_path))
    try:
        page = doc[page_number - 1]
        # Scale factor: 72 DPI is the PDF default
        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)
        pixmap = page.get_pixmap(matrix=matrix)
        return pixmap.tobytes("png")
    finally:
        doc.close()


def get_pdf_metadata(file_path: str) -> dict:
    """Extract metadata from a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Dictionary with PDF metadata.
    """
    doc = fitz.open(str(file_path))
    try:
        metadata = doc.metadata or {}
        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "page_count": len(doc),
            "encrypted": doc.is_encrypted,
        }
    finally:
        doc.close()
