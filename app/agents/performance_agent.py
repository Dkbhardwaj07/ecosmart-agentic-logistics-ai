class PerformanceAgent:

    def calculate(self, cost, carbon, sustainability_score, risk):

        # Normalize cost (assume 0–1000 range realistic)
        cost_score = max(0, 100 - (cost / 10))

        # Normalize carbon (assume 0–300 range realistic)
        carbon_score = max(0, 100 - (carbon * 0.3))

        # Risk penalty
        if risk == "Elevated":
            risk_penalty = 20
        elif risk == "Medium":
            risk_penalty = 10
        else:
            risk_penalty = 0

        # Combine weighted score
        overall_score = (
            (sustainability_score * 0.4) +
            (cost_score * 0.2) +
            (carbon_score * 0.2) +
            (100 - risk_penalty) * 0.2
        )

        return round(max(0, overall_score))
