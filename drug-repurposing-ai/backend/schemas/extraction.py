"""Pydantic models for NLP extraction output."""

from typing import List, Optional
from pydantic import BaseModel


class ClinicalEntity(BaseModel):
    """A single extracted clinical entity."""
    text: str
    label: str  # DISEASE, CHEMICAL, GENE_OR_GENE_PRODUCT, SYMPTOM, etc.
    start: int
    end: int
    status: str = "confirmed"  # confirmed, negated, uncertain
    experiencer: str = "patient"  # patient, family
    temporality: str = "current"  # current, historical
    confidence: Optional[float] = None


class DiagnosisResult(BaseModel):
    """Identified diagnosis/condition from the report."""
    original_text: str
    normalized_name: Optional[str] = None
    canonical_id: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[float] = None
    status: str = "confirmed"  # confirmed, uncertain, negated


class ClinicalExtractionResult(BaseModel):
    """Complete NLP extraction result."""
    report_id: str
    entities: List[ClinicalEntity]
    diagnoses: List[DiagnosisResult]
    symptoms: List[ClinicalEntity]
    medications: List[ClinicalEntity]
    lab_tests: List[ClinicalEntity]
    biomarkers: List[ClinicalEntity]
    genes: List[ClinicalEntity]
    proteins: List[ClinicalEntity]
    clinical_findings: List[ClinicalEntity]
    primary_diagnosis: Optional[DiagnosisResult] = None


class ReportSummary(BaseModel):
    """Structured report summary for display."""
    report_id: str
    condition: Optional[str] = None
    condition_status: str = "confirmed"
    symptoms: List[str] = []
    clinical_findings: List[str] = []
    biomarkers: List[str] = []
    genes: List[str] = []
    proteins: List[str] = []
    current_medications: List[str] = []
