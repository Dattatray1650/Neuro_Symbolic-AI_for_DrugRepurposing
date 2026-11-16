"""Clinical extraction orchestrator — combines document processing + NLP."""

from document_processing.preprocessing import process_document, DocumentResult
from nlp.entity_extraction import extract_entities, to_dict, ClinicalExtraction
from typing import Optional


def run_pipeline(file_path: str, report_id: str, tesseract_cmd: Optional[str] = None) -> dict:
    """Full pipeline: document → text → entities.

    Args:
        file_path: Path to uploaded file.
        report_id: Unique report ID.
        tesseract_cmd: Path to Tesseract executable.

    Returns:
        Dict with document info + extracted entities.
    """
    # Step 1: Extract text
    doc: DocumentResult = process_document(file_path, report_id, tesseract_cmd)

    # Step 2: Extract clinical entities
    extraction: ClinicalExtraction = extract_entities(doc.cleaned_text)
    entity_dict = to_dict(extraction)

    return {
        "report_id": report_id,
        "document": {
            "extraction_method": doc.extraction_method,
            "num_pages": doc.num_pages,
            "has_text": doc.has_text,
            "text_length": len(doc.cleaned_text),
            "warnings": doc.warnings,
        },
        "clinical_extraction": entity_dict,
        "cleaned_text_preview": doc.cleaned_text[:500],
    }
