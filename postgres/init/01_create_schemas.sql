-- 01_create_schemas.sql
-- Initializes the logical boundaries for the healthcare data platform.
-- Each schema corresponds to a bounded context in the domain model.

CREATE SCHEMA IF NOT EXISTS patient_schema;
CREATE SCHEMA IF NOT EXISTS appointment_schema;
CREATE SCHEMA IF NOT EXISTS billing_schema;
CREATE SCHEMA IF NOT EXISTS audit_schema;

COMMENT ON SCHEMA patient_schema IS 'Patient demographics, contacts, and addresses';
COMMENT ON SCHEMA appointment_schema IS 'Scheduling, appointment tracking and status history';
COMMENT ON SCHEMA billing_schema IS 'Invoices, payments and insurance claims';
COMMENT ON SCHEMA audit_schema IS 'System-wide event logging for compliance and security';
