"""Live API end-to-end test."""
import requests, json, time

BASE = "http://127.0.0.1:8000"
time.sleep(2)

# Step 1: Health
r = requests.get(f"{BASE}/health")
assert r.status_code == 200, r.text
print("PASS health:", r.json()["status"])

# Step 2: Upload
report_text = (
    "MEDICAL REPORT\n"
    "Patient: Jane Smith, 72F\n"
    "Chief Complaint: Progressive memory loss and cognitive decline for 3 years\n"
    "Diagnosis: Alzheimer's disease (confirmed)\n"
    "Symptoms: Memory loss, cognitive decline, disorientation, confusion\n"
    "Clinical Findings: Amyloid-beta elevated. Tau protein elevated. APOE4 positive.\n"
    "Current Medications: Donepezil 10mg, Memantine 20mg\n"
    "HbA1c: 5.7%\n"
)
r = requests.post(
    f"{BASE}/api/upload/",
    files={"file": ("alzheimer_report.txt", report_text.encode(), "text/plain")}
)
assert r.status_code == 200, r.text
rid = r.json()["report_id"]
print("PASS upload, report_id:", rid[:8] + "...")

# Step 3: Trigger analysis
r = requests.post(f"{BASE}/api/analysis/{rid}")
assert r.status_code == 200, r.text
data = r.json()
print("PASS analysis, disease:", data["disease_identified"], "candidates:", data["candidates_found"])

# Step 4: Get summary
r = requests.get(f"{BASE}/api/analysis/{rid}/summary")
assert r.status_code == 200, r.text
s = r.json()
print("PASS summary, entities:", s["total_entities"],
      "symptoms:", len(s["symptoms"]), "meds:", len(s["medications"]))

# Step 5: Get results
r = requests.get(f"{BASE}/api/results/{rid}")
assert r.status_code == 200, r.text
results = r.json()
print("PASS results, top candidate:", results["candidates"][0]["drug_name"],
      "score:", results["candidates"][0]["candidate_score"])
print("     evidence paths:", len(results["candidates"][0]["evidence_paths"]))

# Step 6: Get graph
r = requests.get(f"{BASE}/api/results/{rid}/graph")
assert r.status_code == 200, r.text
g = r.json()
print("PASS graph, nodes:", len(g["nodes"]), "edges:", len(g["edges"]))

print("\nALL API TESTS PASSED")
