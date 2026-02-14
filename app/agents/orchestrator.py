from .route_agent import RouteAgent
from .cost_agent import CostAgent
from .carbon_agent import CarbonAgent
from .risk_agent import RiskAgent
from .sustainability_agent import SustainabilityAgent
from .explanation_agent import ExplanationAgent
from app.services.ai_service import NovaAIService
from .comparison_agent import ComparisonAgent
from .simulation_agent import SimulationAgent
from .performance_agent import PerformanceAgent




class LogisticsOrchestrator:

    def __init__(self):
        self.route_agent = RouteAgent()
        self.cost_agent = CostAgent()
        self.carbon_agent = CarbonAgent()
        self.risk_agent = RiskAgent()
        self.sustainability_agent = SustainabilityAgent()
        self.explanation_agent = ExplanationAgent()
        self.ai_service = NovaAIService()
        self.comparison_agent = ComparisonAgent()
        self.simulation_agent = SimulationAgent()
        self.performance_agent = PerformanceAgent()



    def optimize(self, request):

        # Step 1: Base Calculations
        route = self.route_agent.get_route(request)
        cost = self.cost_agent.calculate(request)
        carbon = self.carbon_agent.calculate(request)
        risk = self.risk_agent.analyze(request)

        # Step 2: Agent Collaboration Logic

        # If high priority, increase cost slightly (fast delivery route)
        if request.priority.lower() == "high":
            cost *= 1.1

        # If heavy cargo, carbon impact increases
        if request.cargo_weight > 200:
            carbon *= 1.2

        # If risk elevated, sustainability penalty
        if risk == "Elevated":
            carbon *= 1.1

        sustainability = self.sustainability_agent.evaluate(
            carbon, request.cargo_weight
        )

        explanation = self.explanation_agent.generate(
            route, cost, carbon, risk, sustainability["sustainability_score"]
        )

        ai_reasoning = self.ai_service.generate_reasoning({
                "route": route,
                "cost": round(cost,2),
                "carbon": round(carbon,2),
                "risk": risk,
                "score": sustainability["sustainability_score"]
            })

        alternatives, recommendation = self.comparison_agent.generate_alternatives(request)
        simulations = self.simulation_agent.simulate(request)
        performance_index = self.performance_agent.calculate(
            cost,
            carbon,
            sustainability["sustainability_score"],
            risk
        )


        # Optimization Confidence Score
        confidence_score = 100 - abs(sustainability["sustainability_score"] - 75)

        return {
            "optimized_route": route,
            "estimated_cost": round(cost, 2),
            "carbon_impact": round(carbon, 2),
            "risk_level": risk,
            **sustainability,
            "optimization_confidence_score": max(50, round(confidence_score)),
            "decision_explanation": explanation,
            "ai_reasoning": ai_reasoning if ai_reasoning else "AI reasoning temporarily unavailable",
            "alternative_routes": alternatives,
            "recommended_strategy": recommendation,
            "simulation_analysis": simulations,
            "overall_performance_index": performance_index

        }
