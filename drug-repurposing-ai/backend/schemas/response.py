"""API response models."""

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response for file upload."""
    report_id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    message: str


class AnalysisStatusResponse(BaseModel):
    """Response for analysis status."""
    report_id: str
    status: str  # processing, completed, failed
    message: str
    steps: dict


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    status_code: int
