class ComparisonAgent:

    def generate_alternatives(self, request):

        # Express Route
        express_cost = request.cargo_weight * 3
        express_carbon = request.cargo_weight * 1.2

        # Eco Route
        eco_cost = request.cargo_weight * 2.6
        eco_carbon = request.cargo_weight * 0.6

        express_score = max(0, round(100 - (express_carbon * 0.5)))
        eco_score = max(0, round(100 - (eco_carbon * 0.5)))


        alternatives = [
            {
                "route": f"{request.source} → {request.destination} (Express)",
                "cost": round(express_cost, 2),
                "carbon": round(express_carbon, 2),
                "sustainability_score": round(express_score)
            },
            {
                "route": f"{request.source} → {request.destination} (Eco)",
                "cost": round(eco_cost, 2),
                "carbon": round(eco_carbon, 2),
                "sustainability_score": round(eco_score)
            }
        ]

        # Recommendation logic
        if eco_score > express_score:
            recommendation = "Eco Route Selected due to better sustainability-to-cost balance."
        else:
            recommendation = "Express Route Selected due to priority efficiency."

        return alternatives, recommendation
