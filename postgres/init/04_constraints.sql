-- 04_constraints.sql
-- Specialized data integrity constraints and business rules.

-- Ensure invoice amount is always positive or zero
ALTER TABLE billing_schema.invoices ADD CONSTRAINT check_positive_invoice_amount CHECK (amount >= 0);

-- Ensure payment amount is strictly positive
ALTER TABLE billing_schema.payments ADD CONSTRAINT check_positive_payment_amount CHECK (amount > 0);

-- Ensure insurance claims have a non-negative claimed amount
ALTER TABLE billing_schema.insurance_claims ADD CONSTRAINT check_positive_claim_amount CHECK (amount_claimed >= 0);
