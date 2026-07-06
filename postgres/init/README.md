# HealthSphere Database Initialization

## Overview
This directory contains the SQL initialization scripts for the HealthSphere Enterprise Data Platform. These scripts are designed to be executed automatically by the PostgreSQL Docker image on its first startup.

## Initialization Process
PostgreSQL official images are configured to execute any `.sql`, `.sql.gz`, or `.sh` scripts located in the `/docker-entrypoint-initdb.d` directory inside the container. 
- Scripts are executed in **lexicographical (alphabetical) order**.
- This process only happens if the data directory (`/var/lib/postgresql/data`) is empty.

## Schema Architecture
The database uses a domain-driven schema approach to isolate business contexts:
1. **`patient_schema`**: Core patient identity and contact management.
2. **`appointment_schema`**: Clinical scheduling and status tracking.
3. **`billing_schema`**: Financial records, invoicing, and insurance.
4. **`audit_schema`**: Immutable system logs for compliance.

## Key Design Decisions

### UUIDs vs. SERIAL
We use **UUID v4** (`gen_random_uuid()`) for all primary keys because:
- **Distributed Systems**: Prevents ID collisions when merging data from different sources.
- **Security**: Obfuscates the number of records and prevents predictable ID attacks (ID scraping).
- **Lakehouse Integration**: Provides a consistent global identifier across the Bronze $\rightarrow$ Silver $\rightarrow$ Gold pipeline.

### Indexing Strategy
- **B-tree Indexes**: Applied to all Foreign Keys to ensure join performance.
- **Search Optimization**: Indexes are placed on high-cardinality filter columns such as `appointment_time`, `ssn`, and `status`.
- **JSONB**: The audit log uses `JSONB` for flexible, semi-structured event details.

### Downstream Data Flow (The Medallion Pipeline)
This OLTP database is the source for the platform's data lakehouse:
1. **Capture**: Change Data Capture (CDC) via Debezium monitors the PostgreSQL WAL (`wal_level = logical`).
2. **Transport**: Every change is streamed as an event to **Kafka**.
3. **Bronze**: Kafka Connect sinks raw events into MinIO as Parquet files.
4. **Silver**: Spark jobs clean, deduplicate, and cast types.
5. **Gold**: dbt/Spark aggregate data for analytics dashboards.

## Development Commands

### 1. Rebuild the Database
To force a re-run of the initialization scripts (e.g., after modifying SQL files):
```bash
docker compose down -v
docker compose up -d postgres
```

### 2. Verify Schemas and Tables
Connect to the database:
```bash
docker exec -it healthsphere-postgres psql -U postgres -d healthsphere_db
```
*(Replace `postgres` and `healthsphere_db` with your `.env` values)*

List schemas:
```sql
\dn
```
List tables in a specific schema:
```sql
\dt patient_schema.*
```

### 3. Verify Seed Data
Check if sample patients were loaded:
```sql
SELECT * FROM patient_schema.patients;
```
