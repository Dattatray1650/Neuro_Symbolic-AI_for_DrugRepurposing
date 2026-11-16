"""API route aggregation."""

from fastapi import APIRouter

from backend.api.upload import router as upload_router
from backend.api.analysis import router as analysis_router
from backend.api.results import router as results_router

api_router = APIRouter()

api_router.include_router(upload_router, prefix="/upload", tags=["Upload"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(results_router, prefix="/results", tags=["Results"])
