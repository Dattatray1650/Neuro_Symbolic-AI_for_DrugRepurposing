"""End-to-end pipeline test script."""
from nlp.entity_extraction import extract_entities, to_dict
from knowledge_graph.graph import get_graph, get_disease_stats, find_disease_node
from knowledge_graph.queries import generate_candidates, candidates_to_dict

# Test NLP
text = (
    "Patient: John Doe, 68M. Diagnosis: Alzheimer's disease (confirmed). "
    "Symptoms: Memory loss, cognitive decline, disorientation. "
    "Current medications: Donepezil 10mg daily. "
    "Biomarkers: Amyloid-beta elevated. APOE4 positive."
)

extraction = extract_entities(text)
d = to_dict(extraction)
print("=== NLP Results ===")
print("Primary disease:", d["primary_disease"], "(", d["disease_confidence"], ")")
print("Diseases:", [e["text"] for e in d["diseases"]])
print("Symptoms:", [e["text"] for e in d["symptoms"]])
print("Medications:", [e["text"] for e in d["medications"]])
print("Genes:", [e["text"] for e in d["genes"]])
print()

# Test KG
stats = get_disease_stats()
print("=== Knowledge Graph ===")
print("Nodes:", stats["total_nodes"], "Edges:", stats["total_edges"])
print("Diseases:", stats["diseases"], "Drugs:", stats["drugs"], "Genes:", stats["genes"])
print()

# Test Candidates
candidates = generate_candidates("Alzheimer's disease")
print("=== Top 5 Drug Candidates for Alzheimer ===")
for c in candidates[:5]:
    print(" #" + str(c.rank), c.drug_name, "score=" + str(c.candidate_score),
          "N=" + str(c.neural_score), "S=" + str(c.symbolic_score),
          "[" + c.evidence_classification + "]")
    for p in c.evidence_paths[:1]:
        print("   path:", " > ".join(str(x) for x in p.path))

print()
print("ALL TESTS PASSED")
