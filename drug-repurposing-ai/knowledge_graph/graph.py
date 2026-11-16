"""Biomedical Knowledge Graph using NetworkX.

Built from curated real drug-disease-gene-pathway relationships
sourced from ChEMBL, DisGeNET, Open Targets, STRING (public data).

Labeled clearly as DEMO DATA for research purposes.
"""

import networkx as nx
from typing import List, Dict, Optional


# ---------------------------------------------------------------------------
# Real biomedical relationships (curated demo subset)
# Source: ChEMBL, Open Targets, DisGeNET (CC BY 4.0 / CC0)
# ---------------------------------------------------------------------------

DEMO_NODES = [
    # Diseases
    {"id": "D:alzheimer", "type": "Disease", "name": "Alzheimer's Disease", "umls": "C0002395"},
    {"id": "D:parkinson", "type": "Disease", "name": "Parkinson's Disease", "umls": "C0030567"},
    {"id": "D:diabetes2", "type": "Disease", "name": "Type 2 Diabetes Mellitus", "umls": "C0011860"},
    {"id": "D:breast_cancer", "type": "Disease", "name": "Breast Cancer", "umls": "C0006142"},
    {"id": "D:rheumatoid", "type": "Disease", "name": "Rheumatoid Arthritis", "umls": "C0003873"},
    {"id": "D:heart_failure", "type": "Disease", "name": "Heart Failure", "umls": "C0018801"},
    {"id": "D:depression", "type": "Disease", "name": "Major Depressive Disorder", "umls": "C1269683"},
    {"id": "D:multiple_sclerosis","type": "Disease", "name": "Multiple Sclerosis", "umls": "C0026769"},
    {"id": "D:lung_cancer", "type": "Disease", "name": "Lung Cancer", "umls": "C0242379"},
    {"id": "D:hypertension", "type": "Disease", "name": "Hypertension", "umls": "C0020538"},

    # Drugs (ChEMBL IDs)
    {"id": "DR:donepezil",    "type": "Drug", "name": "Donepezil",    "chembl": "CHEMBL502"},
    {"id": "DR:memantine",    "type": "Drug", "name": "Memantine",    "chembl": "CHEMBL807"},
    {"id": "DR:rivastigmine", "type": "Drug", "name": "Rivastigmine", "chembl": "CHEMBL564"},
    {"id": "DR:metformin",    "type": "Drug", "name": "Metformin",    "chembl": "CHEMBL1431"},
    {"id": "DR:sitagliptin",  "type": "Drug", "name": "Sitagliptin",  "chembl": "CHEMBL1422"},
    {"id": "DR:empagliflozin","type": "Drug", "name": "Empagliflozin","chembl": "CHEMBL2219475"},
    {"id": "DR:levodopa",     "type": "Drug", "name": "Levodopa",     "chembl": "CHEMBL1009"},
    {"id": "DR:rasagiline",   "type": "Drug", "name": "Rasagiline",   "chembl": "CHEMBL1232"},
    {"id": "DR:trastuzumab",  "type": "Drug", "name": "Trastuzumab",  "chembl": "CHEMBL1201585"},
    {"id": "DR:tamoxifen",    "type": "Drug", "name": "Tamoxifen",    "chembl": "CHEMBL83"},
    {"id": "DR:methotrexate", "type": "Drug", "name": "Methotrexate", "chembl": "CHEMBL426"},
    {"id": "DR:adalimumab",   "type": "Drug", "name": "Adalimumab",   "chembl": "CHEMBL1201580"},
    {"id": "DR:lisinopril",   "type": "Drug", "name": "Lisinopril",   "chembl": "CHEMBL1032"},
    {"id": "DR:carvedilol",   "type": "Drug", "name": "Carvedilol",   "chembl": "CHEMBL1016"},
    {"id": "DR:sertraline",   "type": "Drug", "name": "Sertraline",   "chembl": "CHEMBL1046"},
    {"id": "DR:fluoxetine",   "type": "Drug", "name": "Fluoxetine",   "chembl": "CHEMBL41"},
    {"id": "DR:interferon",   "type": "Drug", "name": "Interferon Beta","chembl": "CHEMBL1201572"},
    {"id": "DR:erlotinib",    "type": "Drug", "name": "Erlotinib",    "chembl": "CHEMBL553"},
    {"id": "DR:liraglutide",  "type": "Drug", "name": "Liraglutide",  "chembl": "CHEMBL2103841"},
    {"id": "DR:semaglutide",  "type": "Drug", "name": "Semaglutide",  "chembl": "CHEMBL3660065"},

    # Genes / Proteins
    {"id": "G:ACHE",  "type": "Gene", "name": "ACHE",  "entrez": "43"},
    {"id": "G:BCHE",  "type": "Gene", "name": "BCHE",  "entrez": "590"},
    {"id": "G:NMDAR", "type": "Gene", "name": "GRIN1", "entrez": "2902"},
    {"id": "G:APOE",  "type": "Gene", "name": "APOE",  "entrez": "348"},
    {"id": "G:APP",   "type": "Gene", "name": "APP",   "entrez": "351"},
    {"id": "G:MAOB",  "type": "Gene", "name": "MAOB",  "entrez": "4129"},
    {"id": "G:SNCA",  "type": "Gene", "name": "SNCA",  "entrez": "6622"},
    {"id": "G:LRRK2", "type": "Gene", "name": "LRRK2", "entrez": "120892"},
    {"id": "G:HER2",  "type": "Gene", "name": "ERBB2", "entrez": "2064"},
    {"id": "G:ESR1",  "type": "Gene", "name": "ESR1",  "entrez": "2099"},
    {"id": "G:TNF",   "type": "Gene", "name": "TNF",   "entrez": "7124"},
    {"id": "G:ACE",   "type": "Gene", "name": "ACE",   "entrez": "1636"},
    {"id": "G:ADRB",  "type": "Gene", "name": "ADRB1", "entrez": "153"},
    {"id": "G:SERT",  "type": "Gene", "name": "SLC6A4","entrez": "6532"},
    {"id": "G:EGFR",  "type": "Gene", "name": "EGFR",  "entrez": "1956"},
    {"id": "G:GLP1R", "type": "Gene", "name": "GLP1R", "entrez": "2740"},
    {"id": "G:AMPK",  "type": "Gene", "name": "PRKAA1","entrez": "5562"},
    {"id": "G:INSR",  "type": "Gene", "name": "INSR",  "entrez": "3643"},

    # Pathways
    {"id": "P:cholinergic",    "type": "Pathway", "name": "Cholinergic Signaling"},
    {"id": "P:glutamate",      "type": "Pathway", "name": "Glutamate Signaling"},
    {"id": "P:dopamine",       "type": "Pathway", "name": "Dopamine Metabolism"},
    {"id": "P:ampk",           "type": "Pathway", "name": "AMPK Signaling"},
    {"id": "P:tnf",            "type": "Pathway", "name": "TNF Signaling"},
    {"id": "P:pi3k",           "type": "Pathway", "name": "PI3K-Akt Signaling"},
    {"id": "P:ras_mapk",       "type": "Pathway", "name": "RAS-MAPK Signaling"},
    {"id": "P:renin",          "type": "Pathway", "name": "Renin-Angiotensin System"},
    {"id": "P:serotonin",      "type": "Pathway", "name": "Serotonin Signaling"},
    {"id": "P:glp1",           "type": "Pathway", "name": "GLP-1 Receptor Signaling"},
    {"id": "P:neuroinflam",    "type": "Pathway", "name": "Neuroinflammation"},
]

DEMO_EDGES = [
    # Alzheimer ← drugs
    ("DR:donepezil",    "D:alzheimer", "TREATS",         {"score": 0.98, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:memantine",    "D:alzheimer", "TREATS",         {"score": 0.95, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:rivastigmine", "D:alzheimer", "TREATS",         {"score": 0.93, "source": "ChEMBL", "evidence": "clinical_trial"}),
    # Alzheimer ← genes
    ("G:APOE",  "D:alzheimer", "ASSOCIATED_WITH",        {"score": 0.95, "source": "DisGeNET"}),
    ("G:APP",   "D:alzheimer", "ASSOCIATED_WITH",        {"score": 0.90, "source": "DisGeNET"}),
    ("G:ACHE",  "D:alzheimer", "ASSOCIATED_WITH",        {"score": 0.80, "source": "DisGeNET"}),
    # Alzheimer → pathways
    ("D:alzheimer","P:cholinergic", "INVOLVES",          {"score": 0.9,  "source": "Reactome"}),
    ("D:alzheimer","P:glutamate",   "INVOLVES",          {"score": 0.85, "source": "Reactome"}),
    ("D:alzheimer","P:neuroinflam", "INVOLVES",          {"score": 0.88, "source": "Reactome"}),
    # Drug targets
    ("DR:donepezil", "G:ACHE",  "INHIBITS",             {"score": 0.99, "source": "ChEMBL"}),
    ("DR:memantine", "G:NMDAR", "INHIBITS",             {"score": 0.97, "source": "ChEMBL"}),
    ("DR:rivastigmine","G:BCHE","INHIBITS",             {"score": 0.96, "source": "ChEMBL"}),

    # Repurposing candidates for Alzheimer
    ("DR:metformin",   "D:alzheimer", "REPURPOSING_CANDIDATE", {"score": 0.70, "source": "Open Targets", "evidence": "observational"}),
    ("DR:liraglutide", "D:alzheimer", "REPURPOSING_CANDIDATE", {"score": 0.65, "source": "Open Targets", "evidence": "preclinical"}),
    ("DR:semaglutide", "D:alzheimer", "REPURPOSING_CANDIDATE", {"score": 0.68, "source": "Open Targets", "evidence": "preclinical"}),
    ("DR:rasagiline",  "D:alzheimer", "REPURPOSING_CANDIDATE", {"score": 0.60, "source": "PubMed", "evidence": "observational"}),

    # Parkinson ← drugs
    ("DR:levodopa",   "D:parkinson", "TREATS",          {"score": 0.99, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:rasagiline", "D:parkinson", "TREATS",          {"score": 0.92, "source": "ChEMBL", "evidence": "clinical_trial"}),
    # Parkinson ← genes
    ("G:SNCA",  "D:parkinson", "ASSOCIATED_WITH",       {"score": 0.95, "source": "DisGeNET"}),
    ("G:LRRK2", "D:parkinson", "ASSOCIATED_WITH",       {"score": 0.90, "source": "DisGeNET"}),
    ("G:MAOB",  "D:parkinson", "ASSOCIATED_WITH",       {"score": 0.80, "source": "DisGeNET"}),
    # Parkinson → pathways
    ("D:parkinson","P:dopamine",    "INVOLVES",         {"score": 0.98, "source": "Reactome"}),
    ("D:parkinson","P:neuroinflam", "INVOLVES",         {"score": 0.82, "source": "Reactome"}),
    # Repurposing for Parkinson
    ("DR:sertraline",  "D:parkinson","REPURPOSING_CANDIDATE", {"score": 0.55, "source": "PubMed", "evidence": "observational"}),

    # Diabetes ← drugs
    ("DR:metformin",    "D:diabetes2", "TREATS",        {"score": 0.99, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:sitagliptin",  "D:diabetes2", "TREATS",        {"score": 0.95, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:empagliflozin","D:diabetes2", "TREATS",        {"score": 0.96, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:liraglutide",  "D:diabetes2", "TREATS",        {"score": 0.94, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:semaglutide",  "D:diabetes2", "TREATS",        {"score": 0.95, "source": "ChEMBL", "evidence": "clinical_trial"}),
    # Diabetes ← genes
    ("G:INSR",  "D:diabetes2", "ASSOCIATED_WITH",       {"score": 0.90, "source": "DisGeNET"}),
    ("G:AMPK",  "D:diabetes2", "ASSOCIATED_WITH",       {"score": 0.85, "source": "DisGeNET"}),
    ("G:GLP1R", "D:diabetes2", "ASSOCIATED_WITH",       {"score": 0.88, "source": "DisGeNET"}),
    # Repurposing for Diabetes
    ("DR:empagliflozin","D:heart_failure","REPURPOSING_CANDIDATE",{"score":0.88,"source":"Open Targets","evidence":"clinical_trial"}),

    # Breast Cancer
    ("DR:trastuzumab","D:breast_cancer","TREATS",       {"score": 0.98, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:tamoxifen",  "D:breast_cancer","TREATS",       {"score": 0.97, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("G:HER2", "D:breast_cancer","ASSOCIATED_WITH",     {"score": 0.95, "source": "DisGeNET"}),
    ("G:ESR1", "D:breast_cancer","ASSOCIATED_WITH",     {"score": 0.90, "source": "DisGeNET"}),
    ("DR:trastuzumab","G:HER2","TARGETS",               {"score": 0.99, "source": "ChEMBL"}),

    # Rheumatoid Arthritis
    ("DR:methotrexate","D:rheumatoid","TREATS",         {"score": 0.98, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:adalimumab",  "D:rheumatoid","TREATS",         {"score": 0.97, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("G:TNF",  "D:rheumatoid","ASSOCIATED_WITH",        {"score": 0.95, "source": "DisGeNET"}),
    ("DR:adalimumab","G:TNF","INHIBITS",                {"score": 0.99, "source": "ChEMBL"}),
    ("D:rheumatoid","P:tnf","INVOLVES",                 {"score": 0.95, "source": "Reactome"}),

    # Heart Failure
    ("DR:lisinopril", "D:heart_failure","TREATS",       {"score": 0.97, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:carvedilol", "D:heart_failure","TREATS",       {"score": 0.95, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("G:ACE",  "D:heart_failure","ASSOCIATED_WITH",     {"score": 0.88, "source": "DisGeNET"}),
    ("G:ADRB", "D:heart_failure","ASSOCIATED_WITH",     {"score": 0.85, "source": "DisGeNET"}),
    ("D:heart_failure","P:renin","INVOLVES",            {"score": 0.90, "source": "Reactome"}),

    # Depression
    ("DR:sertraline", "D:depression","TREATS",          {"score": 0.97, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("DR:fluoxetine", "D:depression","TREATS",          {"score": 0.96, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("G:SERT", "D:depression","ASSOCIATED_WITH",        {"score": 0.88, "source": "DisGeNET"}),
    ("DR:sertraline","G:SERT","INHIBITS",               {"score": 0.99, "source": "ChEMBL"}),

    # Multiple Sclerosis
    ("DR:interferon","D:multiple_sclerosis","TREATS",   {"score": 0.95, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("D:multiple_sclerosis","P:neuroinflam","INVOLVES", {"score": 0.92, "source": "Reactome"}),

    # Lung Cancer
    ("DR:erlotinib","D:lung_cancer","TREATS",           {"score": 0.95, "source": "ChEMBL", "evidence": "clinical_trial"}),
    ("G:EGFR","D:lung_cancer","ASSOCIATED_WITH",        {"score": 0.95, "source": "DisGeNET"}),
    ("DR:erlotinib","G:EGFR","INHIBITS",                {"score": 0.99, "source": "ChEMBL"}),
    ("D:lung_cancer","P:ras_mapk","INVOLVES",           {"score": 0.90, "source": "Reactome"}),

    # Protein-Protein (STRING high-confidence links)
    ("G:ACHE", "G:BCHE",  "INTERACTS",                 {"score": 0.80, "source": "STRING"}),
    ("G:SNCA", "G:LRRK2", "INTERACTS",                 {"score": 0.75, "source": "STRING"}),
    ("G:TNF",  "G:INSR",  "INTERACTS",                 {"score": 0.72, "source": "STRING"}),
    ("G:EGFR", "G:HER2",  "INTERACTS",                 {"score": 0.90, "source": "STRING"}),
    ("G:AMPK", "G:INSR",  "INTERACTS",                 {"score": 0.78, "source": "STRING"}),
    ("G:APOE", "G:APP",   "INTERACTS",                 {"score": 0.82, "source": "STRING"}),

    # Gene-Pathway memberships
    ("G:ACHE",  "P:cholinergic", "IN_PATHWAY",         {"score": 0.95, "source": "Reactome"}),
    ("G:NMDAR", "P:glutamate",   "IN_PATHWAY",         {"score": 0.95, "source": "Reactome"}),
    ("G:SNCA",  "P:dopamine",    "IN_PATHWAY",         {"score": 0.90, "source": "Reactome"}),
    ("G:MAOB",  "P:dopamine",    "IN_PATHWAY",         {"score": 0.88, "source": "Reactome"}),
    ("G:AMPK",  "P:ampk",        "IN_PATHWAY",         {"score": 0.98, "source": "Reactome"}),
    ("G:TNF",   "P:tnf",         "IN_PATHWAY",         {"score": 0.98, "source": "Reactome"}),
    ("G:EGFR",  "P:ras_mapk",    "IN_PATHWAY",         {"score": 0.95, "source": "Reactome"}),
    ("G:ACE",   "P:renin",       "IN_PATHWAY",         {"score": 0.98, "source": "Reactome"}),
    ("G:SERT",  "P:serotonin",   "IN_PATHWAY",         {"score": 0.98, "source": "Reactome"}),
    ("G:GLP1R", "P:glp1",        "IN_PATHWAY",         {"score": 0.98, "source": "Reactome"}),
    ("G:INSR",  "P:ampk",        "IN_PATHWAY",         {"score": 0.85, "source": "Reactome"}),
]


def build_knowledge_graph() -> nx.DiGraph:
    """Build the biomedical knowledge graph from demo data."""
    G = nx.DiGraph()

    for node in DEMO_NODES:
        G.add_node(node["id"], **node)

    for src, dst, rel, attrs in DEMO_EDGES:
        G.add_edge(src, dst, relation=rel, **attrs)

    return G


# Singleton graph instance
_graph: Optional[nx.DiGraph] = None


def get_graph() -> nx.DiGraph:
    """Get the global knowledge graph (builds on first call)."""
    global _graph
    if _graph is None:
        _graph = build_knowledge_graph()
    return _graph


def find_disease_node(disease_name: str) -> Optional[str]:
    """Find a disease node ID matching the given name (fuzzy)."""
    G = get_graph()
    name_lower = disease_name.lower()

    # Direct match
    for node_id, attrs in G.nodes(data=True):
        if attrs.get("type") == "Disease":
            if name_lower in attrs.get("name", "").lower():
                return node_id
            if name_lower in node_id.lower():
                return node_id

    # Keyword match
    keywords = {
        "alzheimer": "D:alzheimer",
        "parkinson": "D:parkinson",
        "diabetes": "D:diabetes2",
        "breast cancer": "D:breast_cancer",
        "rheumatoid": "D:rheumatoid",
        "heart failure": "D:heart_failure",
        "depression": "D:depression",
        "multiple sclerosis": "D:multiple_sclerosis",
        "lung cancer": "D:lung_cancer",
        "hypertension": "D:hypertension",
    }
    for kw, node_id in keywords.items():
        if kw in name_lower:
            return node_id

    return None


def get_disease_stats() -> dict:
    G = get_graph()
    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "diseases": len([n for n, d in G.nodes(data=True) if d.get("type") == "Disease"]),
        "drugs": len([n for n, d in G.nodes(data=True) if d.get("type") == "Drug"]),
        "genes": len([n for n, d in G.nodes(data=True) if d.get("type") == "Gene"]),
        "pathways": len([n for n, d in G.nodes(data=True) if d.get("type") == "Pathway"]),
        "data_note": "DEMO DATA — curated subset from ChEMBL, DisGeNET, Open Targets, STRING",
    }
