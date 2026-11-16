"""Pydantic models for medical report data."""

from typing import Optional
from pydantic import BaseModel


class DocumentResult(BaseModel):
    """Result of document processing (PDF/OCR extraction)."""
    report_id: str
    raw_text: str
    cleaned_text: str
    num_pages: int
    has_text: bool
    has_images: bool
    extraction_method: str  # "pdf_text", "ocr", "direct_text"
    confidence: Optional[float] = None


class ReportMetadata(BaseModel):
    """Metadata about an uploaded report."""
    report_id: str
    filename: str
    file_type: str
    file_size: int
    status: str
