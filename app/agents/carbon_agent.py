class CarbonAgent:

    def calculate(self, request):
        carbon_factor = 0.8
        return round(request.cargo_weight * carbon_factor, 2)
