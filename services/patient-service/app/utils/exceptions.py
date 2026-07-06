from fastapi import HTTPException, status

class PatientServiceException(Exception):
    """Base exception for Patient Service."""
    pass

class PatientNotFoundException(PatientServiceException):
    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        self.message = f"Patient with ID {patient_id} not found"
        super().__init__(self.message)

class DatabaseOperationError(PatientServiceException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ValidationErrorException(PatientServiceException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
