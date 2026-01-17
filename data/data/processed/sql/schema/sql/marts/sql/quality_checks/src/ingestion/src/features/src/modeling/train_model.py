import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

def train_models(feature_path: str, output_path: str):
    df = pd.read_csv(feature_path)

    X = df.drop(columns=["is_denied"])
    y = df["is_denied"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Baseline model
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    lr_preds = lr.predict_proba(X_test)[:, 1]

    print("Logistic Regression AUC:", roc_auc_score(y_test, lr_preds))
    print(classification_report(y_test, lr_preds > 0.5))

    # Stronger model
    rf = RandomForestClassifier(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict_proba(X_test)[:, 1]

    print("Random Forest AUC:", roc_auc_score(y_test, rf_preds))
    print(classification_report(y_test, rf_preds > 0.5))

    # Save predictions for BI
    results = X_test.copy()
    results["is_denied_actual"] = y_test.values
    results["denial_probability"] = rf_preds

    results.to_csv(output_path, index=False)
    print(f"Scored claims written to {output_path}")


if __name__ == "__main__":
    train_models(
        feature_path="data/processed/model_features.csv",
        output_path="data/processed/scored_claims.csv",
    )
