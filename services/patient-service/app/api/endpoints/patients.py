from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.patient_service import PatientService
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.utils.exceptions import PatientNotFoundException, DatabaseOperationError, ValidationErrorException
from uuid import UUID
from typing import List

router = APIRouter()

def get_patient_service(db: AsyncSession = Depends(get_db)) -> PatientService:
    return PatientService(db)

@router.post("/", response_model=PatientRead, status_code=201)
async def create_patient(patient: PatientCreate, service: PatientService = Depends(get_patient_service)):
    try:
        return await service.create_patient(patient)
    except ValidationErrorException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except DatabaseOperationError as e:
        raise HTTPException(status_code=500, detail=e.message)

@router.get("/", response_model=List[PatientRead])
async def get_patients(service: PatientService = Depends(get_patient_service)):
    return await service.list_patients()

@router.get("/{patient_id}", response_model=PatientRead)
async def get_patient(patient_id: UUID, service: PatientService = Depends(get_patient_service)):
    try:
        return await service.get_patient(patient_id)
    except PatientNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

@router.put("/{patient_id}", response_model=PatientRead)
async def update_patient(patient_id: UUID, patient: PatientUpdate, service: PatientService = Depends(get_patient_service)):
    try:
        return await service.update_patient(patient_id, patient)
    except PatientNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseOperationError as e:
        raise HTTPException(status_code=500, detail=e.message)

@router.delete("/{patient_id}", status_code=204)
async def delete_patient(patient_id: UUID, service: PatientService = Depends(get_patient_service)):
    try:
        await service.delete_patient(patient_id)
        return None
    except PatientNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DatabaseOperationError as e:
        raise HTTPException(status_code=500, detail=e.message)
