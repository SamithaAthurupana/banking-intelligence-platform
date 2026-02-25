import pandas as pd
import numpy as np
from datetime import timedelta

class FraudEngine:

    def __init__(self, high_amount_threshold=50000):
        self.high_amount_threshold = high_amount_threshold

    def analyze(self, new_txn: dict, history: list):
        df = pd.DataFrame(history)

        if df.empty:
            return {"fraud": False, "anomaly_score": 0}

        # Include new transaction temporarily
        df = pd.concat([df, pd.DataFrame([new_txn])], ignore_index=True)

        # Z-score anomaly detection
        mean = df["amount"].mean()
        std = df["amount"].std() or 1
        z_score = (new_txn["amount"] - mean) / std

        # Rapid transaction detection (within 1 min)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        recent = df[
            df["timestamp"] > (pd.to_datetime(new_txn["timestamp"]) - timedelta(minutes=1))
        ]

        rapid_count = len(recent)

        fraud_flag = (
            new_txn["amount"] > self.high_amount_threshold or
            abs(z_score) > 3 or
            rapid_count > 3
        )

        anomaly_score = min(abs(z_score) / 5, 1)

        return {
            "fraud": fraud_flag,
            "anomaly_score": anomaly_score
        }