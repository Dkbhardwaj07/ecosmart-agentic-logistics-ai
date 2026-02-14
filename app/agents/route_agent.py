class RouteAgent:

    def get_route(self, request):
        return f"{request.source} → {request.destination}"


def optimize_route(request):
    return {
        "optimized_route": f"{request.source} → {request.destination}",
        "estimated_cost": request.cargo_weight * 2.5,
        "priority_level": request.priority,
        "carbon_impact": request.cargo_weight * 0.8
    }
