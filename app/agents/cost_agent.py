class CostAgent:

    def calculate(self, request):
        base_rate = 2.5
        return round(request.cargo_weight * base_rate, 2)
