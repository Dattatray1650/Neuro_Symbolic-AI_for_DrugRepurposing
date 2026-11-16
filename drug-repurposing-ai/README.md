# Neuro-Symbolic AI for Explainable Drug Repurposing from Medical Reports

## Overview

An AI research prototype where a user uploads a medical report, and the system:
1. Extracts clinical information (diagnoses, symptoms, medications, genes, biomarkers)
2. Identifies and normalizes the documented disease/condition
3. Connects to a biomedical knowledge graph built from real public data
4. Uses neural AI + symbolic reasoning (neuro-symbolic fusion) to identify drug repurposing candidates
5. Ranks and explains every candidate with traceable evidence paths

> **⚠️ IMPORTANT DISCLAIMER**
> This system generates computational drug-repurposing hypotheses for research purposes only.
> It does not provide medical advice, diagnosis, or treatment recommendations.
> Candidate drugs require independent experimental, clinical, and regulatory validation.

## Tech Stack

- **Backend**: Python, FastAPI
- **NLP**: scispaCy, medspaCy
- **Document Processing**: PyMuPDF, Tesseract OCR, OpenCV
- **Knowledge Graph**: NetworkX (MVP), Neo4j (advanced)
- **ML**: scikit-learn, XGBoost, PyTorch, PyTorch Geometric
- **Frontend**: React, Tailwind CSS, Plotly, react-force-graph

## Quick Start

### Backend
```bash
cd drug-repurposing-ai
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### API Docs
Once running, visit: http://localhost:8000/docs

## Project Structure

```
drug-repurposing-ai/
├── backend/          # FastAPI application
├── document_processing/  # PDF/OCR text extraction
├── nlp/              # Clinical NLP & entity extraction
├── data/             # Raw and processed datasets
├── knowledge_graph/  # Biomedical knowledge graph
├── ml/               # Machine learning models
├── symbolic/         # Symbolic reasoning rules
├── fusion/           # Neuro-symbolic score fusion
├── explanation/      # Explainability generation
├── validation/       # Evidence classification
├── frontend/         # React dashboard
├── tests/            # Test suites
├── notebooks/        # Jupyter exploration
└── scripts/          # Data download & build scripts
```

## Development Phases

1. ✅ Project Scaffolding & Environment
2. Medical Report Processing
3. Clinical NLP & Entity Extraction
4. Biomedical Data Pipeline & Knowledge Graph
5. Candidate Generation & Baseline ML
6. Neural Model (Graph Embeddings)
7. Symbolic Reasoning
8. Fusion, Ranking & Explanation
9. Frontend Dashboard

## License

Academic research project.
