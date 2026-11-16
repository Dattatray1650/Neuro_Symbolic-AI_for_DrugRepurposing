"""Pydantic models for drug repurposing candidates."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ReasoningPath(BaseModel):
    """A single reasoning path through the knowledge graph."""
    rule: str
    path: List[str]  # ["Drug A", "TARGETS", "Protein P1", "ASSOCIATED_WITH", "Disease X"]
    entities: Dict[str, Optional[str]]  # {"protein": "P1", "gene": null, "pathway": null}
    weight: float
    source_confidence: Optional[float] = None


class CandidateDrug(BaseModel):
    """A single drug repurposing candidate."""
    rank: int
    drug_name: str
    drug_id: str
    candidate_score: float
    neural_score: float
    symbolic_score: float
    evidence_paths: List[ReasoningPath] = []
    rules_fired: List[str] = []
    evidence_classification: str = "novel_computational"  # previously_reported, partially_supported, novel_computational, insufficient_evidence
    explanation: Optional[str] = None
    targets: List[str] = []
    genes: List[str] = []
    pathways: List[str] = []
    sources: List[str] = []


class RankingResult(BaseModel):
    """Complete ranking result for a report."""
    report_id: str
    disease_name: str
    disease_id: str
    candidates: List[CandidateDrug]
    total_candidates: int
    alpha: float
    beta: float
    disclaimer: str = (
        "This system generates computational drug-repurposing hypotheses "
        "for research purposes only. It does not provide medical advice, "
        "diagnosis, or treatment recommendations. Candidate drugs require "
        "independent experimental, clinical, and regulatory validation."
    )
