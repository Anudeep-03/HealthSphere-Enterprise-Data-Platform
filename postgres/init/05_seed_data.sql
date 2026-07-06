-- 05_seed_data.sql
-- Baseline test data for initial verification and development.

-- Seed Patients
INSERT INTO patient_schema.patients (first_name, last_name, dob, gender, ssn)
VALUES
('John', 'Doe', '1985-05-15', 'Male', '123-45-6789'),
('Jane', 'Smith', '1992-11-20', 'Female', '987-65-4321'),
('Robert', 'Brown', '1970-01-10', 'Male', '111-22-3333'),
('Emily', 'Davis', '2000-08-25', 'Female', '444-55-6666');

-- Seed Contacts (using subqueries to link to patients)
INSERT INTO patient_schema.patient_contacts (patient_id, contact_type, contact_value, is_preferred)
SELECT id, 'Email', 'john.doe@example.com', true FROM patient_schema.patients WHERE ssn = '123-45-6789';

INSERT INTO patient_schema.patient_contacts (patient_id, contact_type, contact_value, is_preferred)
SELECT id, 'Mobile', '555-0101', false FROM patient_schema.patients WHERE ssn = '123-45-6789';

INSERT INTO patient_schema.patient_contacts (patient_id, contact_type, contact_value, is_preferred)
SELECT id, 'Email', 'jane.smith@example.com', true FROM patient_schema.patients WHERE ssn = '987-65-4321';

-- Seed Addresses
INSERT INTO patient_schema.patient_addresses (patient_id, address_type, street, city, state, zip)
SELECT id, 'Home', '123 Maple Ave', 'Springfield', 'IL', '62704' FROM patient_schema.patients WHERE ssn = '123-45-6789';

INSERT INTO patient_schema.patient_addresses (patient_id, address_type, street, city, state, zip)
SELECT id, 'Home', '456 Oak St', 'Metropolis', 'NY', '10001' FROM patient_schema.patients WHERE ssn = '987-65-4321';

-- Seed Appointments
INSERT INTO appointment_schema.appointments (patient_id, provider_id, clinic_id, appointment_time, status)
VALUES
((SELECT id FROM patient_schema.patients WHERE ssn = '123-45-6789'), gen_random_uuid(), gen_random_uuid(), NOW() + interval '1 day', 'Scheduled'),
((SELECT id FROM patient_schema.patients WHERE ssn = '987-65-4321'), gen_random_uuid(), gen_random_uuid(), NOW() + interval '2 days', 'Scheduled');

-- Seed Appointment History
INSERT INTO appointment_schema.appointment_status_history (appointment_id, old_status, new_status, changed_by)
SELECT id, NULL, 'Scheduled', gen_random_uuid() FROM appointment_schema.appointments LIMIT 2;

-- Seed Invoices
INSERT INTO billing_schema.invoices (patient_id, amount, due_date, status)
VALUES
((SELECT id FROM patient_schema.patients WHERE ssn = '123-45-6789'), 150.00, CURRENT_DATE + interval '30 days', 'Unpaid'),
((SELECT id FROM patient_schema.patients WHERE ssn = '987-65-4321'), 200.00, CURRENT_DATE + interval '30 days', 'Paid');

-- Seed Payments
INSERT INTO billing_schema.payments (invoice_id, amount, payment_method)
SELECT id, 200.00, 'Credit Card' FROM billing_schema.invoices WHERE status = 'Paid' LIMIT 1;

-- Seed Insurance Claims
INSERT INTO billing_schema.insurance_claims (invoice_id, insurer, status, amount_claimed)
SELECT id, 'HealthGuard Inc', 'Pending', 150.00 FROM billing_schema.invoices WHERE status = 'Unpaid' LIMIT 1;

-- Seed Audit Logs
INSERT INTO audit_schema.event_logs (user_id, action, resource, details)
VALUES
(gen_random_uuid(), 'SYSTEM_INIT', 'database', '{"version": "16.0", "env": "production", "step": "Step 3"}'),
(gen_random_uuid(), 'DATA_SEED', 'patient_schema', '{"records_inserted": 4, "status": "success"}');
