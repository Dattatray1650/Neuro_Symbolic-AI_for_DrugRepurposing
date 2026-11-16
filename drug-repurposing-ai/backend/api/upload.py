"""Medical report upload and document processing endpoint."""

import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.config import UPLOAD_DIR, MAX_UPLOAD_SIZE_BYTES, ALLOWED_EXTENSIONS, TESSERACT_CMD
from backend.schemas.response import UploadResponse

router = APIRouter()

# In-memory storage for report data (will be replaced by DB in production)
report_store: dict = {}


@router.post("/", response_model=UploadResponse)
async def upload_report(file: UploadFile = File(...)):
    """Upload a medical report (PDF, JPG, JPEG, PNG, or TXT).

    Processes the document immediately after upload:
    - PDF: extracts text via PyMuPDF, OCR for scanned pages
    - Images: runs OCR pipeline
    - TXT: reads directly
    """
    # Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # Read file content
    content = await file.read()

    # Validate file size
    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_UPLOAD_SIZE_BYTES // (1024*1024)}MB",
        )

    # Generate unique report ID
    report_id = str(uuid.uuid4())

    # Save file
    save_path = UPLOAD_DIR / f"{report_id}{ext}"
    save_path.write_bytes(content)

    # Process the document
    from document_processing.preprocessing import process_document

    try:
        doc_result = process_document(
            file_path=str(save_path),
            report_id=report_id,
            tesseract_cmd=TESSERACT_CMD,
        )

        # Store the result for later retrieval
        report_store[report_id] = {
            "report_id": report_id,
            "filename": file.filename,
            "file_type": ext,
            "file_size": len(content),
            "document_result": doc_result,
        }

        return UploadResponse(
            report_id=report_id,
            filename=file.filename,
            file_type=ext,
            file_size=len(content),
            status="processed",
            message=(
                f"File uploaded and processed successfully. "
                f"Extraction method: {doc_result.extraction_method}. "
                f"Text extracted: {'Yes' if doc_result.has_text else 'No'}. "
                f"Pages: {doc_result.num_pages}."
                + (f" Warnings: {'; '.join(doc_result.warnings)}" if doc_result.warnings else "")
            ),
        )
    except Exception as e:
        # If processing fails, still store the upload but mark as unprocessed
        report_store[report_id] = {
            "report_id": report_id,
            "filename": file.filename,
            "file_type": ext,
            "file_size": len(content),
            "document_result": None,
            "error": str(e),
        }

        return UploadResponse(
            report_id=report_id,
            filename=file.filename,
            file_type=ext,
            file_size=len(content),
            status="uploaded",
            message=f"File uploaded but processing encountered an issue: {str(e)}",
        )


@router.get("/{report_id}/text")
async def get_extracted_text(report_id: str):
    """Get the extracted text from a processed report."""
    if report_id not in report_store:
        raise HTTPException(status_code=404, detail="Report not found")

    data = report_store[report_id]
    doc_result = data.get("document_result")

    if doc_result is None:
        raise HTTPException(status_code=422, detail="Document has not been processed yet")

    return {
        "report_id": report_id,
        "extraction_method": doc_result.extraction_method,
        "num_pages": doc_result.num_pages,
        "has_text": doc_result.has_text,
        "confidence": doc_result.confidence,
        "cleaned_text": doc_result.cleaned_text[:2000],  # Preview first 2000 chars
        "full_text_length": len(doc_result.cleaned_text),
        "warnings": doc_result.warnings,
    }
