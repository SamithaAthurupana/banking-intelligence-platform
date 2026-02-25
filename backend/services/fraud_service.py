import pandas as pd
import numpy as np

class FraudEngine:

    def __init__(self, threshold=50000):
        self.threshold = threshold

    def detect_fraud(self, transactions: list):
        df = pd.DataFrame(transactions)

        if df.empty:
            return []

        df["z_score"] = (df["amount"] - df["amount"].mean()) / df["amount"].std()

        df["is_fraud"] = (
            (df["amount"] > self.threshold) |
            (abs(df["z_score"]) > 3)
        )

        return df[df["is_fraud"]].to_dict(orient="records")