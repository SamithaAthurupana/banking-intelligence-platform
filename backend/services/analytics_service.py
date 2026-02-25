import pandas as pd

class AnalyticsEngine:

    def generate_customer_analytics(self, transactions: list):

        if not transactions:
            return {"message": "No transactions found"}

        df = pd.DataFrame(transactions)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        total_spending = df["amount"].sum()
        average_transaction = df["amount"].mean()
        transaction_count = len(df)

        # Monthly aggregation
        df["month"] = df["timestamp"].dt.to_period("M")
        monthly_spending = (
            df.groupby("month")["amount"]
            .sum()
            .astype(float)
            .to_dict()
        )

        return {
            "total_spending": float(total_spending),
            "average_transaction": float(round(average_transaction, 2)),
            "transaction_count": transaction_count,
            "monthly_spending": {str(k): v for k, v in monthly_spending.items()}
        }