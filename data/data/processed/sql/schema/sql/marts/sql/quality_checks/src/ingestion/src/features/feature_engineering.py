import pandas as pd

def build_features(input_path: str, output_path: str):
    """
    Reads warehouse-style claims data and creates ML-ready features
    for denial risk prediction.
    """

    df = pd.read_csv(input_path, parse_dates=["service_date", "submission_date", "payment_date"])

    # Basic cleaning
    df = df.dropna(subset=["billed_amount", "claim_status"])

    # Target variable
    df["is_denied"] = (df["claim_status"] == "Denied").astype(int)

    # Date-based features
    df["days_to_submit"] = (df["submission_date"] - df["service_date"]).dt.days
    df["days_to_submit"] = df["days_to_submit"].fillna(df["days_to_submit"].median())

    # Financial features
    df["billed_amount_log"] = (df["billed_amount"] + 1).apply(lambda x: pd.np.log(x))

    # Categorical grouping
    df["cpt_group"] = df["cpt_code"].astype(str).str[:2]
    df["payer_group"] = df["payer"].str.lower().str.replace(" ", "_")

    # Aggregated risk signals
    payer_denial_rate = df.groupby("payer_group")["is_denied"].mean()
    dept_denial_rate = df.groupby("department")["is_denied"].mean()

    df["payer_denial_rate"] = df["payer_group"].map(payer_denial_rate)
    df["department_denial_rate"] = df["department"].map(dept_denial_rate)

    df["payer_denial_rate"] = df["payer_denial_rate"].fillna(df["payer_denial_rate"].mean())
    df["department_denial_rate"] = df["department_denial_rate"].fillna(df["department_denial_rate"].mean())

    features = df[
        [
            "billed_amount",
            "billed_amount_log",
            "days_to_submit",
            "payer_denial_rate",
            "department_denial_rate",
            "is_denied",
        ]
    ]

    features.to_csv(output_path, index=False)
    print(f"Feature set written to {output_path}")


if __name__ == "__main__":
    build_features(
        input_path="data/processed/fact_claims.csv",
        output_path="data/processed/model_features.csv",
    )
