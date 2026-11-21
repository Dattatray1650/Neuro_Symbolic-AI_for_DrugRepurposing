"""Medical report upload and document processing endpoint."""

import uuid
import logging
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.config import (
    UPLOAD_DIR,
    MAX_UPLOAD_SIZE_BYTES,
    ALLOWED_EXTENSIONS,
    TESSERACT_CMD,
)

from backend.schemas.response import UploadResponse


router = APIRouter()

logger = logging.getLogger(__name__)

# Temporary in-memory storage.
# Reports are lost when the backend process restarts.
report_store: dict = {}


@router.post("/", response_model=UploadResponse)
async def upload_report(file: UploadFile = File(...)):
    """Upload and process a medical report."""

    # Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    ext = Path(file.filename).suffix.lower()

    # Validate extension
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{ext}'. "
                f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            ),
        )

    # Read file
    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Validate file size
    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"File too large. Maximum size: "
                f"{MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)}MB"
            ),
        )

    # Generate unique report ID
    report_id = str(uuid.uuid4())

    # Save uploaded file
    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        save_path = UPLOAD_DIR / f"{report_id}{ext}"
        save_path.write_bytes(content)

    except Exception as e:
        logger.exception("File saving failed")

        raise HTTPException(
            status_code=500,
            detail=f"Could not save uploaded file: {str(e)}"
        )

    # Process document
    from document_processing.preprocessing import process_document

    try:
        doc_result = process_document(
            file_path=str(save_path),
            report_id=report_id,
            tesseract_cmd=TESSERACT_CMD,
        )

        # Store processed report
        report_store[report_id] = {
            "report_id": report_id,
            "filename": file.filename,
            "file_type": ext,
            "file_size": len(content),
            "document_result": doc_result,
            "analysis": None,
        }

        logger.info("UPLOAD SUCCESS")
        logger.info("REPORT ID: %s", report_id)
        logger.info("REPORT STORE KEYS: %s", list(report_store.keys()))
        logger.info("EXTRACTION METHOD: %s", doc_result.extraction_method)
        logger.info("TEXT AVAILABLE: %s", doc_result.has_text)

        return UploadResponse(
            report_id=report_id,
            filename=file.filename,
            file_type=ext,
            file_size=len(content),
            status="processed",
            message=(
                "File uploaded and processed successfully. "
                f"Extraction method: {doc_result.extraction_method}. "
                f"Text extracted: {'Yes' if doc_result.has_text else 'No'}. "
                f"Pages: {doc_result.num_pages}."
                + (
                    f" Warnings: {'; '.join(doc_result.warnings)}"
                    if doc_result.warnings else ""
                )
            ),
        )

    except Exception as e:

        logger.exception("DOCUMENT PROCESSING FAILED")

        # Store upload information for debugging
        report_store[report_id] = {
            "report_id": report_id,
            "filename": file.filename,
            "file_type": ext,
            "file_size": len(content),
            "document_result": None,
            "analysis": None,
            "error": str(e),
        }

        logger.info("REPORT STORED WITH PROCESSING ERROR: %s", report_id)

        return UploadResponse(
            report_id=report_id,
            filename=file.filename,
            file_type=ext,
            file_size=len(content),
            status="uploaded",
            message=(
                "File uploaded, but document processing failed: "
                f"{str(e)}"
            ),
        )


@router.get("/{report_id}/text")
async def get_extracted_text(report_id: str):
    """Get extracted text from a processed report."""

    if report_id not in report_store:
        raise HTTPException(
            status_code=404,
            detail="Report not found. Please upload the file again."
        )

    data = report_store[report_id]
    doc_result = data.get("document_result")

    if doc_result is None:
        raise HTTPException(
            status_code=422,
            detail=data.get(
                "error",
                "Document has not been processed successfully."
            )
        )

    return {
        "report_id": report_id,
        "extraction_method": doc_result.extraction_method,
        "num_pages": doc_result.num_pages,
        "has_text": doc_result.has_text,
        "confidence": doc_result.confidence,
        "cleaned_text": doc_result.cleaned_text[:2000],
        "full_text_length": len(doc_result.cleaned_text),
        "warnings": doc_result.warnings,
    }