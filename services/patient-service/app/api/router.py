from fastapi import APIRouter
from app.api.endpoints import patients

api_router = APIRouter()
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])
