class SimulationAgent:

    def simulate(self, request):

        # Scenario 1: Reduce cargo by 10%
        reduced_weight = request.cargo_weight * 0.9
        reduced_carbon = reduced_weight * 0.8
        reduced_cost = reduced_weight * 2.5

        scenario_1 = {
            "scenario": "Reduce cargo weight by 10%",
            "estimated_cost": round(reduced_cost, 2),
            "carbon_impact": round(reduced_carbon, 2),
            "sustainability_score": max(0, round(100 - (reduced_carbon * 0.5)))
        }

        # Scenario 2: Change priority to Low
        low_priority_cost = request.cargo_weight * 2.3
        low_priority_carbon = request.cargo_weight * 0.7

        scenario_2 = {
            "scenario": "Switch to Low Priority Delivery",
            "estimated_cost": round(low_priority_cost, 2),
            "carbon_impact": round(low_priority_carbon, 2),
            "sustainability_score": max(0, round(100 - (low_priority_carbon * 0.5)))
        }

        return [scenario_1, scenario_2]
