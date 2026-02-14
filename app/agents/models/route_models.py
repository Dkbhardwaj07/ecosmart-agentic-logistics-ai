from pydantic import BaseModel

class RouteRequest(BaseModel):
    source: str
    destination: str
    cargo_weight: float
    priority: str


class RouteResponse(BaseModel):
    optimized_route: str
    estimated_cost: float
    carbon_impact: float
    risk_level: str