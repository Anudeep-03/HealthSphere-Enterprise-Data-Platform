# Patient Service - HealthSphere Enterprise Data Platform

## Overview
The Patient Service is a microservice responsible for managing patient demographics, contact information, and addresses. It provides a set of RESTful CRUD APIs to maintain patient records in the HealthSphere database.

## Architecture
This service implements a **Layered Architecture** to ensure a clear separation of concerns:

`FastAPI (API Layer)` $\rightarrow$ `PatientService (Business Layer)` $\rightarrow$ `PatientRepository (Data Access Layer)` $\rightarrow$ `PostgreSQL`

- **API Layer**: Handles HTTP routing, input validation using Pydantic v2, and output serialization.
- **Service Layer**: Contains business logic, handles transaction boundaries, and manages the conversion between domain models and API schemas.
- **Repository Layer**: Abstracts all database interactions using SQLAlchemy 2.x ORM.
- **Database Layer**: Uses PostgreSQL with the `patient_schema`.

## Folder Organization
- `app/api/`: REST endpoint definitions and routing.
- `app/config/`: Environment variable management via Pydantic Settings.
- `app/database/`: Database engine configuration and SQLAlchemy session management.
- `app/models/`: SQLAlchemy ORM model definitions.
- `app/repositories/`: Data access objects (DAOs) implementing the Repository pattern.
- `app/services/`: Business logic orchestration.
- `app/schemas/`: Pydantic v2 models for request/response validation.
- `app/kafka/`: Placeholder for future asynchronous event publishing.
- `app/utils/`: Shared utilities for logging and custom exception handling.

## How to Run

### Prerequisites
- Docker and Docker Compose
- A running PostgreSQL instance (configured via the main project `docker-compose.yml`)

### Installation & Execution
1. Clone the project.
2. Navigate to the service directory:
   ```bash
   cd services/patient-service
   ```
3. Create a `.env` file based on `.env.example` (or use the provided `.env`).
4. Build and run using Docker:
   ```bash
   docker build -t patient-service .
   docker run -d --name patient-service --network healthsphere-network -p 8000:8000 patient-service
   ```

## How to Test
1. **Swagger UI**: Navigate to `http://localhost:8000/docs` to interact with the API.
2. **Health Check**: Verify service status via `GET /health`.
3. **CRUD Flow**: 
   - Create a patient using `POST /patients`.
   - Retrieve the patient using `GET /patients/{id}`.
   - Update demographics using `PUT /patients/{id}`.
   - Delete the patient using `DELETE /patients/{id}`.

## Tech Stack
- **Language**: Python 3.12
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.x (Async)
- **Validation**: Pydantic v2
- **Database**: PostgreSQL
- **Containerization**: Docker
