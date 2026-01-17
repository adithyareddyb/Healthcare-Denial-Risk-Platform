import pandas as pd

def compute_business_impact(scored_path: str, output_path: str):
    df = pd.read_csv(scored_path)

    # If billed_amount is not present, you can merge it later from warehouse
    if "billed_amount" not in df.columns:
        raise ValueError("billed_amount column missing from scored data")

    df["expected_revenue_loss"] = df["denial_probability"] * df["billed_amount"]

    # Rank claims by impact
    df = df.sort_values("expected_revenue_loss", ascending=False)

    df.to_csv(output_path, index=False)
    print(f"Business impact file written to {output_path}")


if __name__ == "__main__":
    compute_business_impact(
        scored_path="data/processed/scored_claims.csv",
        output_path="data/processed/claim_risk_queue.csv",
    )
