class ExplanationAgent:

    def generate(self, route, cost, carbon, risk, sustainability_score):

        explanation = (
            f"The selected route {route} balances operational cost ({cost}) "
            f"and environmental impact ({round(carbon, 2)} kg CO₂). "
            f"Risk level is assessed as {risk}. "
            f"The sustainability score of {sustainability_score} "
            f"indicates overall environmental efficiency."
        )

        return explanation
