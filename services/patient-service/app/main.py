from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.router import api_router
from app.config.config import settings
from app.utils.logging import setup_logging, logger
from app.utils.exceptions import PatientServiceException
from pydantic import ValidationError
from app.kafka.producer import kafka_producer

# Initialize logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Kafka Producer
    try:
        await kafka_producer.start()
    except Exception as e:
        logger.error(f"Critical startup failure: Kafka Producer could not start: {e}")
        # We allow the app to start even if Kafka is down (graceful degradation)

    yield

    # Shutdown: Close Kafka Producer
    await kafka_producer.stop()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Global Exception Handlers
@app.exception_handler(PatientServiceException)
async def patient_service_exception_handler(request: Request, exc: PatientServiceException):
    logger.error(f"Service Error: {exc.message} | Path: {request.url.path}")
    # Map custom exceptions to HTTP statuses
    from app.utils.exceptions import PatientNotFoundException
    if isinstance(exc, PatientNotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.message})
    return JSONResponse(status_code=500, content={"detail": "An internal service error occurred"})

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning(f"Validation Error | Path: {request.url.path} | Errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled Exception | Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred on the server"}
    )

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Request completed: {request.method} {request.url.path} | Status: {response.status_code}")
    return response

# Health Check
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}

# Include API Router
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
