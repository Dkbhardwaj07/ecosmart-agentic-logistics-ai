class SustainabilityAgent:

    def evaluate(self, carbon_impact, cargo_weight):

        # Normalize carbon impact (assuming 0–200 realistic range)
        carbon_score = max(0, 100 - (carbon_impact * 0.5))

        # Weight impact adjustment
        weight_factor = min(cargo_weight / 500, 1) * 20

        score = max(0, round(carbon_score - weight_factor))

        if score > 75:
            recommendation = "Highly Sustainable Route 🌱"
            emission_category = "Low Emission"
        elif score > 40:
            recommendation = "Moderately Sustainable Route"
            emission_category = "Medium Emission"
        else:
            recommendation = "High Emission Route ⚠"
            emission_category = "High Emission"

        return {
            "sustainability_score": score,
            "eco_recommendation": recommendation,
            "emission_category": emission_category
        }
