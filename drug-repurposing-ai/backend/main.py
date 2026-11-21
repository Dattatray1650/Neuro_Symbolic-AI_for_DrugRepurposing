"""FastAPI application entry point for Drug Repurposing AI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import APP_NAME, DEBUG
from backend.api.router import api_router

app = FastAPI(
    title=APP_NAME,
    description=(
        "Neuro-Symbolic AI for Explainable Drug Repurposing from Medical Reports. "
        "This system generates computational drug-repurposing hypotheses for research "
        "purposes only. It does not provide medical advice, diagnosis, or treatment "
        "recommendations."
    ),
    version="0.1.0",
    debug=DEBUG,
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://localhost:8001",
    "http://localhost:5173",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_router, prefix="/api")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": APP_NAME}


if __name__ == "__main__":
    import uvicorn
    from backend.config import HOST, PORT
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
