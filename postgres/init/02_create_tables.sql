-- 02_create_tables.sql
-- Defines core entities and their relationships.
-- All primary keys use UUIDs for distributed scalability and security.

-- Utility for automatic updated_at timestamps
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ===========================================================================
-- PATIENT SCHEMA
-- ===========================================================================

CREATE TABLE patient_schema.patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(20),
    ssn VARCHAR(11) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patient_schema.patient_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patient_schema.patients(id) ON DELETE CASCADE,
    contact_type VARCHAR(20) NOT NULL, -- e.g., 'Mobile', 'Email', 'Work'
    contact_value TEXT NOT NULL,
    is_preferred BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patient_schema.patient_addresses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patient_schema.patients(id) ON DELETE CASCADE,
    address_type VARCHAR(20) NOT NULL, -- e.g., 'Home', 'Mailing'
    street TEXT NOT NULL,
    city TEXT NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip VARCHAR(10) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================================================
-- APPOINTMENT SCHEMA
-- ===========================================================================

CREATE TABLE appointment_schema.appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patient_schema.patients(id),
    provider_id UUID NOT NULL,
    clinic_id UUID NOT NULL,
    appointment_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) NOT NULL, -- e.g., 'Scheduled', 'Completed', 'Cancelled'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointment_schema.appointment_status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL REFERENCES appointment_schema.appointments(id) ON DELETE CASCADE,
    old_status VARCHAR(20),
    new_status VARCHAR(20) NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    changed_by UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================================================
-- BILLING SCHEMA
-- ===========================================================================

CREATE TABLE billing_schema.invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patient_schema.patients(id),
    amount NUMERIC(12, 2) NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL, -- e.g., 'Unpaid', 'Partial', 'Paid'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE billing_schema.payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES billing_schema.invoices(id),
    amount NUMERIC(12, 2) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    payment_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE billing_schema.insurance_claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES billing_schema.invoices(id),
    claim_id_external VARCHAR(50) UNIQUE,
    insurer TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    amount_claimed NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================================================
-- AUDIT SCHEMA
-- ===========================================================================

CREATE TABLE audit_schema.event_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id UUID,
    action VARCHAR(50) NOT NULL,
    resource VARCHAR(100),
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Apply updated_at triggers
CREATE TRIGGER tr_patients_upd BEFORE UPDATE ON patient_schema.patients FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER tr_contacts_upd BEFORE UPDATE ON patient_schema.patient_contacts FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER tr_addresses_upd BEFORE UPDATE ON patient_schema.patient_addresses FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER tr_appts_upd BEFORE UPDATE ON appointment_schema.appointments FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER tr_appts_hist_upd BEFORE UPDATE ON appointment_schema.appointment_status_history FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER tr_inv_upd BEFORE UPDATE ON billing_schema.invoices FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER tr_pay_upd BEFORE UPDATE ON billing_schema.payments FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER tr_claims_upd BEFORE UPDATE ON billing_schema.insurance_claims FOR EACH ROW EXECUTE FUNCTION update_timestamp();
CREATE TRIGGER tr_logs_upd BEFORE UPDATE ON audit_schema.event_logs FOR EACH ROW EXECUTE FUNCTION update_timestamp();
