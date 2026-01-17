-- 1. Missing critical fields
SELECT 
    COUNT(*) AS total_claims,
    SUM(CASE WHEN payer_key IS NULL THEN 1 ELSE 0 END) AS missing_payer,
    SUM(CASE WHEN department_key IS NULL THEN 1 ELSE 0 END) AS missing_department,
    SUM(CASE WHEN cpt_key IS NULL THEN 1 ELSE 0 END) AS missing_cpt
FROM fact_claims;

-- 2. Invalid financial values
SELECT 
    COUNT(*) AS invalid_amounts
FROM fact_claims
WHERE billed_amount <= 0;

-- 3. Impossible dates (paid before submitted)
SELECT 
    COUNT(*) AS invalid_dates
FROM fact_claims
WHERE payment_date IS NOT NULL
  AND submission_date IS NOT NULL
  AND payment_date < submission_date;

-- 4. Denied claims with payment
SELECT 
    COUNT(*) AS denied_but_paid
FROM fact_claims
WHERE is_denied = TRUE AND paid_amount > 0;

-- 5. Duplicate Claim IDs (should be zero)
SELECT 
    COUNT(*) - COUNT(DISTINCT claim_id) AS duplicate_claims
FROM fact_claims;
