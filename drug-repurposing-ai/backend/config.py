"""Application configuration loaded from environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR", "data/uploads")
MODEL_DIR = BASE_DIR / os.getenv("MODEL_DIR", "models")

# App settings
APP_NAME = os.getenv("APP_NAME", "Drug Repurposing AI")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Upload
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".txt"}

# Tesseract
TESSERACT_CMD = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")

# Knowledge Graph
KG_PATH = BASE_DIR / os.getenv("KG_PATH", "data/processed/knowledge_graph.gpickle")

# Fusion Weights
ALPHA = float(os.getenv("ALPHA", "0.6"))
BETA = float(os.getenv("BETA", "0.4"))

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "metadata").mkdir(parents=True, exist_ok=True)
