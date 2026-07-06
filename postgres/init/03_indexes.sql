-- 03_indexes.sql
-- Performance optimizations for commonly queried columns and all Foreign Keys.

-- Patient Schema Indexes
CREATE INDEX idx_patient_contacts_patient_id ON patient_schema.patient_contacts(patient_id);
CREATE INDEX idx_patient_addresses_patient_id ON patient_schema.patient_addresses(patient_id);

-- Appointment Schema Indexes
CREATE INDEX idx_appointments_patient_id ON appointment_schema.appointments(patient_id);
CREATE INDEX idx_appointments_time ON appointment_schema.appointments(appointment_time);
CREATE INDEX idx_appointments_status ON appointment_schema.appointments(status);
CREATE INDEX idx_appt_status_hist_appt_id ON appointment_schema.appointment_status_history(appointment_id);

-- Billing Schema Indexes
CREATE INDEX idx_invoices_patient_id ON billing_schema.invoices(patient_id);
CREATE INDEX idx_invoices_status ON billing_schema.invoices(status);
CREATE INDEX idx_payments_invoice_id ON billing_schema.payments(invoice_id);
CREATE INDEX idx_claims_invoice_id ON billing_schema.insurance_claims(invoice_id);

-- Audit Schema Indexes
CREATE INDEX idx_event_logs_timestamp ON audit_schema.event_logs(timestamp);
CREATE INDEX idx_event_logs_user_id ON audit_schema.event_logs(user_id);
