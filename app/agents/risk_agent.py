class RiskAgent:

    def analyze(self, request):
        if request.priority.lower() == "high":
            return "Elevated"
        elif request.cargo_weight > 200:
            return "Medium"
        else:
            return "Low"
