-- Load dimension tables
INSERT INTO dim_payer (payer_name)
SELECT DISTINCT Payer
FROM raw_claims
WHERE Payer IS NOT NULL
ON CONFLICT (payer_name) DO NOTHING;

INSERT INTO dim_department (department_name)
SELECT DISTINCT Department
FROM raw_claims
WHERE Department IS NOT NULL
ON CONFLICT (department_name) DO NOTHING;

INSERT INTO dim_cpt (cpt_code)
SELECT DISTINCT CPTCode
FROM raw_claims
WHERE CPTCode IS NOT NULL
ON CONFLICT (cpt_code) DO NOTHING;

-- Load fact table
INSERT INTO fact_claims (
    claim_id,
    service_date,
    submission_date,
    payment_date,
    payer_key,
    department_key,
    cpt_key,
    billed_amount,
    paid_amount,
    claim_status,
    is_denied,
    days_to_payment
)
SELECT
    r.ClaimID,
    r.ServiceDate::DATE,
    r.SubmissionDate::DATE,
    r.PaymentDate::DATE,
    p.payer_key,
    d.department_key,
    c.cpt_key,
    r.BilledAmount,
    r.PaidAmount,
    r.ClaimStatus,
    CASE WHEN r.ClaimStatus = 'Denied' THEN TRUE ELSE FALSE END AS is_denied,
    CASE 
        WHEN r.PaymentDate IS NOT NULL AND r.SubmissionDate IS NOT NULL 
        THEN (r.PaymentDate::DATE - r.SubmissionDate::DATE)
        ELSE NULL 
    END AS days_to_payment
FROM raw_claims r
LEFT JOIN dim_payer p ON r.Payer = p.payer_name
LEFT JOIN dim_department d ON r.Department = d.department_name
LEFT JOIN dim_cpt c ON r.CPTCode = c.cpt_code;
