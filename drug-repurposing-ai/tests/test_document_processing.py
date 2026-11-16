"""Tests for document processing module."""

import pytest
from pathlib import Path
from document_processing.preprocessing import clean_text, process_document

# --- clean_text tests ---

def test_clean_text_normalizes_whitespace():
    raw = "Patient    has   multiple   spaces"
    result = clean_text(raw)
    assert "  " not in result
    assert "Patient has multiple spaces" == result


def test_clean_text_handles_unicode():
    raw = "\u201cDiagnosis\u201d: Alzheimer\u2019s disease"
    result = clean_text(raw)
    assert '"' in result
    assert "'" in result


def test_clean_text_removes_excessive_blank_lines():
    raw = "Line 1\n\n\n\n\n\n\nLine 2"
    result = clean_text(raw)
    assert result.count("\n") <= 3


def test_clean_text_empty_input():
    assert clean_text("") == ""
    assert clean_text(None) == ""


def test_clean_text_strips_lines():
    raw = "  Line 1  \n  Line 2  "
    result = clean_text(raw)
    assert result == "Line 1\nLine 2"


# --- process_document tests ---

def test_process_text_file(tmp_path):
    """Test processing a plain text file."""
    txt_file = tmp_path / "report.txt"
    txt_file.write_text(
        "Patient Name: John Doe\n"
        "Diagnosis: Alzheimer's disease\n"
        "Symptoms: Memory loss, cognitive decline\n"
        "Current Medications: Donepezil 10mg\n",
        encoding="utf-8",
    )

    result = process_document(str(txt_file), report_id="test-001")
    assert result.report_id == "test-001"
    assert result.has_text is True
    assert result.extraction_method == "direct_text"
    assert "Alzheimer" in result.cleaned_text
    assert "Donepezil" in result.cleaned_text
    assert result.num_pages == 1
    assert result.confidence == 1.0


def test_process_text_file_empty(tmp_path):
    """Test processing an empty text file."""
    txt_file = tmp_path / "empty.txt"
    txt_file.write_text("", encoding="utf-8")

    result = process_document(str(txt_file), report_id="test-002")
    assert result.has_text is False
    assert result.cleaned_text == ""


def test_process_unsupported_extension(tmp_path):
    """Test that unsupported file types raise ValueError."""
    bad_file = tmp_path / "report.docx"
    bad_file.write_text("hello")

    with pytest.raises(ValueError, match="Unsupported file type"):
        process_document(str(bad_file), report_id="test-003")


def test_process_missing_file():
    """Test that missing files raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        process_document("nonexistent.txt", report_id="test-004")


# --- PDF extraction tests ---

def test_pdf_parser_import():
    """Verify PyMuPDF is importable."""
    import fitz
    assert hasattr(fitz, "open")


def test_create_and_parse_pdf(tmp_path):
    """Create a simple PDF with text and verify extraction."""
    import fitz

    # Create a test PDF
    doc = fitz.open()
    page = doc.new_page()
    text_point = fitz.Point(72, 100)
    page.insert_text(text_point, "Patient diagnosed with Type 2 Diabetes Mellitus.", fontsize=12)
    page.insert_text(fitz.Point(72, 130), "HbA1c: 8.5%", fontsize=12)
    page.insert_text(fitz.Point(72, 160), "Current medication: Metformin 500mg", fontsize=12)

    pdf_path = tmp_path / "test_report.pdf"
    doc.save(str(pdf_path))
    doc.close()

    # Process it
    result = process_document(str(pdf_path), report_id="test-pdf-001")
    assert result.has_text is True
    assert result.extraction_method == "pdf_text"
    assert "Diabetes" in result.cleaned_text
    assert "Metformin" in result.cleaned_text
    assert result.num_pages == 1


def test_pdf_multi_page(tmp_path):
    """Test extraction from a multi-page PDF."""
    import fitz

    doc = fitz.open()
    for i in range(3):
        page = doc.new_page()
        page.insert_text(fitz.Point(72, 100), f"Page {i+1} content: medical findings", fontsize=12)

    pdf_path = tmp_path / "multi_page.pdf"
    doc.save(str(pdf_path))
    doc.close()

    result = process_document(str(pdf_path), report_id="test-pdf-002")
    assert result.num_pages == 3
    assert "Page 1" in result.cleaned_text
    assert "Page 3" in result.cleaned_text
