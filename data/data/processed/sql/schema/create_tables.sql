CREATE TABLE dim_payer (
    payer_key SERIAL PRIMARY KEY,
    payer_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE dim_department (
    department_key SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE dim_cpt (
    cpt_key SERIAL PRIMARY KEY,
    cpt_code VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE fact_claims (
    claim_id VARCHAR(50) PRIMARY KEY,
    service_date DATE,
    submission_date DATE,
    payment_date DATE,
    payer_key INT REFERENCES dim_payer(payer_key),
    department_key INT REFERENCES dim_department(department_key),
    cpt_key INT REFERENCES dim_cpt(cpt_key),
    billed_amount NUMERIC(12,2),
    paid_amount NUMERIC(12,2),
    claim_status VARCHAR(20),
    is_denied BOOLEAN,
    days_to_payment INT
);
