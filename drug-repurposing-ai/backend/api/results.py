"""Results retrieval endpoints."""

from fastapi import APIRouter, HTTPException
from backend.api.upload import report_store
from knowledge_graph.graph import get_disease_stats

router = APIRouter()

DISCLAIMER = (
    "This system generates computational drug-repurposing hypotheses "
    "for research purposes only. It does not provide medical advice, "
    "diagnosis, or treatment recommendations. Candidate drugs require "
    "independent experimental, clinical, and regulatory validation."
)


@router.get("/{report_id}")
async def get_results(report_id: str):
    """Get ranked drug-repurposing candidates for a report."""
    if report_id not in report_store:
        raise HTTPException(status_code=404, detail="Report not found.")

    analysis = report_store[report_id].get("analysis")
    if not analysis:
        raise HTTPException(
            status_code=422,
            detail="Analysis not run yet. POST to /api/analysis/{report_id} first."
        )

    return {
        "report_id": report_id,
        "disease": analysis["disease_name"],
        "disease_confidence": analysis["disease_confidence"],
        "candidates": analysis["candidates"],
        "total_candidates": len(analysis["candidates"]),
        "fusion_weights": {"alpha_neural": 0.6, "beta_symbolic": 0.4},
        "data_note": "DEMO DATA — research prototype only",
        "disclaimer": DISCLAIMER,
    }


@router.get("/{report_id}/candidate/{drug_id}")
async def get_candidate_detail(report_id: str, drug_id: str):
    """Get detailed explanation for a specific drug candidate."""
    if report_id not in report_store:
        raise HTTPException(status_code=404, detail="Report not found.")

    analysis = report_store[report_id].get("analysis")
    if not analysis:
        raise HTTPException(status_code=422, detail="Run analysis first.")

    candidates = analysis["candidates"]
    candidate = next((c for c in candidates if c["drug_id"] == drug_id), None)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate {drug_id} not found.")

    return {**candidate, "disclaimer": DISCLAIMER}


@router.get("/{report_id}/graph")
async def get_graph_data(report_id: str):
    """Get knowledge graph subgraph for visualization."""
    if report_id not in report_store:
        raise HTTPException(status_code=404, detail="Report not found.")

    analysis = report_store[report_id].get("analysis")
    if not analysis:
        raise HTTPException(status_code=422, detail="Run analysis first.")

    from knowledge_graph.graph import get_graph, find_disease_node
    import networkx as nx

    G = get_graph()
    disease_id = find_disease_node(analysis["disease_name"])

    if not disease_id:
        return {"nodes": [], "edges": [], "note": "Disease not found in graph"}

    # Get ego graph (2-hop around disease)
    ego = nx.ego_graph(G.to_undirected(), disease_id, radius=2)

    nodes = []
    for node_id in ego.nodes:
        attrs = G.nodes[node_id]
        nodes.append({
            "id": node_id,
            "label": attrs.get("name", node_id),
            "type": attrs.get("type", "Unknown"),
        })

    edges = []
    for src, dst in ego.edges:
        if G.has_edge(src, dst):
            e = G[src][dst]
            edges.append({
                "source": src,
                "target": dst,
                "relation": e.get("relation", ""),
                "score": e.get("score", 0),
            })

    return {
        "nodes": nodes[:60],  # Cap for visualization
        "edges": edges[:100],
        "data_note": "DEMO DATA",
        "stats": get_disease_stats(),
    }
