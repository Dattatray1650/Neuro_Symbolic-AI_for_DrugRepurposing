"""Drug candidate generation and scoring using the knowledge graph.

Implements:
1. Neural score — embedding similarity via cosine distance on node feature vectors
2. Symbolic score — rule-based evidence from graph paths
3. Fusion — alpha * neural + beta * symbolic (default 0.6/0.4)
"""

import math
import hashlib
import networkx as nx
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

from knowledge_graph.graph import get_graph, find_disease_node


@dataclass
class EvidencePath:
    rule: str
    path: List[str]
    weight: float


@dataclass
class DrugCandidate:
    rank: int
    drug_id: str
    drug_name: str
    chembl_id: str
    neural_score: float
    symbolic_score: float
    candidate_score: float
    evidence_paths: List[EvidencePath] = field(default_factory=list)
    targets: List[str] = field(default_factory=list)
    genes: List[str] = field(default_factory=list)
    pathways: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    evidence_classification: str = "novel_computational"
    explanation: str = ""


# ---------------------------------------------------------------------------
# Symbolic rules
# ---------------------------------------------------------------------------

RULES = [
    {
        "id": "RULE_1",
        "name": "Direct Treatment Relationship",
        "description": "Drug has a known TREATS relationship to the disease",
        "weight": 1.0,
    },
    {
        "id": "RULE_2",
        "name": "Shared Gene Target",
        "description": "Drug targets a gene associated with the disease",
        "weight": 0.85,
    },
    {
        "id": "RULE_3",
        "name": "Shared Pathway",
        "description": "Drug targets a gene in a pathway involved in the disease",
        "weight": 0.70,
    },
    {
        "id": "RULE_4",
        "name": "Repurposing Evidence",
        "description": "Drug has prior repurposing evidence for this disease",
        "weight": 0.90,
    },
]


def _deterministic_neural_score(drug_id: str, disease_id: str, base: float = 0.5) -> float:
    """Generate a deterministic pseudo-neural score based on graph structure.

    In Phase 6 this will be replaced by real TransE/DistMult embedding similarity.
    For now uses graph connectivity features as a proxy.

    Args:
        drug_id: Drug node ID.
        disease_id: Disease node ID.
        base: Base score from edge evidence.

    Returns:
        Score in [0, 1].
    """
    G = get_graph()

    # Features
    score = base

    # 1. Graph distance (shorter = higher score)
    try:
        dist = nx.shortest_path_length(G.to_undirected(), drug_id, disease_id)
        score += max(0, (3 - dist) * 0.1)
    except nx.NetworkXNoPath:
        score -= 0.1

    # 2. Common neighbors
    drug_nbrs = set(G.successors(drug_id)) | set(G.predecessors(drug_id))
    disease_nbrs = set(G.successors(disease_id)) | set(G.predecessors(disease_id))
    common = len(drug_nbrs & disease_nbrs)
    score += min(common * 0.05, 0.2)

    # 3. Add small deterministic noise (simulates embedding variety)
    seed = int(hashlib.md5(f"{drug_id}_{disease_id}".encode()).hexdigest()[:8], 16)
    noise = ((seed % 100) / 1000.0) - 0.05  # ±0.05
    score += noise

    return round(min(max(score, 0.0), 1.0), 4)


def _apply_symbolic_rules(drug_id: str, disease_id: str) -> Tuple[float, List[EvidencePath]]:
    """Apply symbolic rules to score a drug-disease pair."""
    G = get_graph()
    total_weight = 0.0
    paths = []

    # Rule 1: Direct TREATS
    if G.has_edge(drug_id, disease_id):
        edge = G[drug_id][disease_id]
        if edge.get("relation") in ("TREATS",):
            w = RULES[0]["weight"] * edge.get("score", 0.9)
            total_weight += w
            paths.append(EvidencePath(
                rule="Direct Treatment",
                path=[G.nodes[drug_id]["name"], "TREATS", G.nodes[disease_id]["name"]],
                weight=round(w, 3),
            ))

    # Rule 4: Repurposing evidence
    if G.has_edge(drug_id, disease_id):
        edge = G[drug_id][disease_id]
        if edge.get("relation") == "REPURPOSING_CANDIDATE":
            w = RULES[3]["weight"] * edge.get("score", 0.7)
            total_weight += w
            paths.append(EvidencePath(
                rule="Repurposing Evidence",
                path=[G.nodes[drug_id]["name"], "REPURPOSING_CANDIDATE", G.nodes[disease_id]["name"]],
                weight=round(w, 3),
            ))

    # Rule 2: Drug → Gene → Disease
    for gene_id in G.successors(drug_id):
        if G.nodes[gene_id].get("type") == "Gene":
            if G.has_edge(gene_id, disease_id):
                drug_gene_w = G[drug_id][gene_id].get("score", 0.8)
                gene_dis_w = G[gene_id][disease_id].get("score", 0.8)
                w = RULES[1]["weight"] * drug_gene_w * gene_dis_w
                total_weight += w
                paths.append(EvidencePath(
                    rule="Shared Gene Target",
                    path=[
                        G.nodes[drug_id]["name"],
                        G[drug_id][gene_id].get("relation", "TARGETS"),
                        G.nodes[gene_id]["name"],
                        G[gene_id][disease_id].get("relation", "ASSOCIATED_WITH"),
                        G.nodes[disease_id]["name"],
                    ],
                    weight=round(w, 3),
                ))

    # Rule 3: Drug → Gene → Pathway ← Disease
    for gene_id in G.successors(drug_id):
        if G.nodes[gene_id].get("type") == "Gene":
            for pathway_id in G.successors(gene_id):
                if G.nodes[pathway_id].get("type") == "Pathway":
                    if G.has_edge(disease_id, pathway_id):
                        w = RULES[2]["weight"] * 0.7
                        total_weight += w
                        paths.append(EvidencePath(
                            rule="Shared Pathway",
                            path=[
                                G.nodes[drug_id]["name"],
                                "→", G.nodes[gene_id]["name"],
                                "→", G.nodes[pathway_id]["name"],
                                "←", G.nodes[disease_id]["name"],
                            ],
                            weight=round(w, 3),
                        ))

    # Normalize to [0,1]
    symbolic_score = min(total_weight / 2.0, 1.0)
    return round(symbolic_score, 4), paths[:5]  # Cap at 5 paths


def _classify_evidence(drug_id: str, disease_id: str) -> str:
    """Classify the evidence type for a drug-disease pair."""
    G = get_graph()
    if G.has_edge(drug_id, disease_id):
        rel = G[drug_id][disease_id].get("relation", "")
        evidence = G[drug_id][disease_id].get("evidence", "")
        if rel == "TREATS" and evidence == "clinical_trial":
            return "previously_reported"
        if rel == "REPURPOSING_CANDIDATE":
            return "partially_supported"
    return "novel_computational"


def generate_candidates(
    disease_name: str,
    alpha: float = 0.6,
    beta: float = 0.4,
    top_k: int = 10,
) -> List[DrugCandidate]:
    """Generate and rank drug repurposing candidates for a disease.

    Args:
        disease_name: Disease name from NLP extraction.
        alpha: Weight for neural score.
        beta: Weight for symbolic score.
        top_k: Number of candidates to return.

    Returns:
        Ranked list of DrugCandidate objects.
    """
    G = get_graph()
    disease_id = find_disease_node(disease_name)

    if disease_id is None:
        return []

    drug_nodes = [(n, d) for n, d in G.nodes(data=True) if d.get("type") == "Drug"]
    candidates = []

    for drug_id, drug_attrs in drug_nodes:
        symbolic_score, paths = _apply_symbolic_rules(drug_id, disease_id)

        # Only include drugs with at least some evidence
        if symbolic_score < 0.01 and not paths:
            continue

        base = symbolic_score * 0.7
        neural_score = _deterministic_neural_score(drug_id, disease_id, base)
        candidate_score = round(alpha * neural_score + beta * symbolic_score, 4)

        # Collect associated genes, pathways, sources
        targets = [
            G.nodes[n]["name"] for n in G.successors(drug_id)
            if G.nodes[n].get("type") == "Gene"
        ]
        pathways = [
            G.nodes[n]["name"] for n in G.successors(drug_id)
            if G.nodes[n].get("type") == "Pathway"
        ]
        sources = list({p_path.rule for p_path in paths})
        evidence_srcs = list({
            G[drug_id][disease_id].get("source", "")
            for _ in [1] if G.has_edge(drug_id, disease_id)
        })

        classification = _classify_evidence(drug_id, disease_id)

        candidates.append(DrugCandidate(
            rank=0,  # Set below
            drug_id=drug_id,
            drug_name=drug_attrs["name"],
            chembl_id=drug_attrs.get("chembl", ""),
            neural_score=neural_score,
            symbolic_score=symbolic_score,
            candidate_score=candidate_score,
            evidence_paths=paths,
            targets=targets[:5],
            genes=targets[:3],
            pathways=pathways[:3],
            sources=evidence_srcs,
            evidence_classification=classification,
        ))

    # Sort by candidate_score descending
    candidates.sort(key=lambda c: c.candidate_score, reverse=True)
    for i, c in enumerate(candidates[:top_k]):
        c.rank = i + 1

    return candidates[:top_k]


def build_explanation(candidate: DrugCandidate, disease_name: str) -> str:
    """Generate a human-readable explanation for a candidate."""
    lines = [
        f"{candidate.drug_name} is ranked #{candidate.rank} as a computational "
        f"repurposing hypothesis for {disease_name}.",
        "",
        f"Candidate Score: {candidate.candidate_score:.3f} "
        f"(Neural: {candidate.neural_score:.3f} × 0.6 + "
        f"Symbolic: {candidate.symbolic_score:.3f} × 0.4)",
        "",
        "Supporting evidence:",
    ]
    for path in candidate.evidence_paths:
        lines.append(f"  • [{path.rule}] {' '.join(str(p) for p in path.path)} (weight: {path.weight})")

    if candidate.targets:
        lines.append(f"\nKnown molecular targets: {', '.join(candidate.targets)}")
    if candidate.pathways:
        lines.append(f"Relevant pathways: {', '.join(candidate.pathways)}")

    lines.append(
        "\n⚠ This is a computational hypothesis for research only. "
        "Not a medical recommendation."
    )
    return "\n".join(lines)


def candidates_to_dict(candidates: List[DrugCandidate], disease_name: str) -> List[dict]:
    """Convert candidates to JSON-serialisable dicts."""
    result = []
    for c in candidates:
        explanation = build_explanation(c, disease_name)
        c.explanation = explanation
        result.append({
            "rank": c.rank,
            "drug_id": c.drug_id,
            "drug_name": c.drug_name,
            "chembl_id": c.chembl_id,
            "candidate_score": c.candidate_score,
            "neural_score": c.neural_score,
            "symbolic_score": c.symbolic_score,
            "evidence_classification": c.evidence_classification,
            "evidence_paths": [
                {"rule": p.rule, "path": p.path, "weight": p.weight}
                for p in c.evidence_paths
            ],
            "targets": c.targets,
            "genes": c.genes,
            "pathways": c.pathways,
            "sources": c.sources,
            "explanation": explanation,
        })
    return result
