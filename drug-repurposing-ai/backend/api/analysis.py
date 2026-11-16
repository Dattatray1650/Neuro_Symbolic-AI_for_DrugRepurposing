"""Analysis API — runs the full NLP + KG + scoring pipeline."""

from fastapi import APIRouter, HTTPException
from backend.api.upload import report_store
from backend.config import TESSERACT_CMD, ALPHA, BETA

router = APIRouter()


@router.post("/{report_id}")
async def trigger_analysis(report_id: str):
    """Run the complete analysis pipeline on an uploaded report."""
    if report_id not in report_store:
        raise HTTPException(status_code=404, detail="Report not found. Upload the file first.")

    data = report_store[report_id]
    doc_result = data.get("document_result")

    if doc_result is None:
        raise HTTPException(status_code=422, detail="Document processing failed.")

    # Step 1: NLP extraction
    from nlp.entity_extraction import extract_entities, to_dict
    extraction = extract_entities(doc_result.cleaned_text)
    entity_dict = to_dict(extraction)

    # Step 2: Knowledge graph candidate generation
    from knowledge_graph.queries import generate_candidates, candidates_to_dict
    from knowledge_graph.graph import get_disease_stats

    disease_name = extraction.primary_disease or ""
    candidates = generate_candidates(disease_name, alpha=ALPHA, beta=BETA)
    candidates_data = candidates_to_dict(candidates, disease_name)

    # Cache results
    report_store[report_id]["analysis"] = {
        "entity_extraction": entity_dict,
        "candidates": candidates_data,
        "disease_name": disease_name,
        "disease_confidence": extraction.disease_confidence,
    }

    return {
        "report_id": report_id,
        "status": "completed",
        "disease_identified": disease_name,
        "disease_confidence": extraction.disease_confidence,
        "total_entities": entity_dict["total_entities"],
        "candidates_found": len(candidates_data),
        "disclaimer": (
            "This system generates computational drug-repurposing hypotheses "
            "for research purposes only. Not medical advice."
        ),
    }


@router.get("/{report_id}/summary")
async def get_report_summary(report_id: str):
    """Get structured NLP summary of an analyzed report."""
    if report_id not in report_store:
        raise HTTPException(status_code=404, detail="Report not found.")

    analysis = report_store[report_id].get("analysis")
    if not analysis:
        raise HTTPException(status_code=422, detail="Run POST /analysis/{report_id} first.")

    return {
        "report_id": report_id,
        "status": "completed",
        **analysis["entity_extraction"],
    }
