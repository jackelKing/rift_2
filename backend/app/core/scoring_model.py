import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def compute_anomaly_scores(feature_df):

    # Remove account_id before ML
    X = feature_df.drop(columns=["account_id"])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    model.fit(X_scaled)

    # Higher anomaly → more negative → invert
    raw_scores = -model.score_samples(X_scaled)

    # Normalize to 0–100
    min_score = raw_scores.min()
    max_score = raw_scores.max()

    normalized = 100 * (raw_scores - min_score) / (max_score - min_score + 1e-8)

    result = pd.DataFrame({
        "account_id": feature_df["account_id"],
        "ml_score": normalized
    })

    return result
