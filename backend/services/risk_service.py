class RiskEngine:

    def calculate_risk(self, amount, anomaly_score):
        score = (0.6 * anomaly_score) + (0.4 * (amount / 100000))

        if score > 0.8:
            level = "HIGH"
        elif score > 0.5:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "risk_score": round(score * 100, 2),
            "risk_level": level
        }