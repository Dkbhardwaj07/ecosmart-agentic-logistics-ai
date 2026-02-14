import random
import time
from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.orchestrator import LogisticsOrchestrator
from app.agents.route_agent import optimize_route
from app.services.executive_ai_service import ExecutiveAIService
from app.services.autonomous_decision_engine import AutonomousDecisionEngine


app = FastAPI()

orchestrator = LogisticsOrchestrator()
executive_ai = ExecutiveAIService()
decision_engine = AutonomousDecisionEngine()


class RouteRequest(BaseModel):
    source: str
    destination: str
    cargo_weight: float
    priority: str

@app.get("/")
def root():
    return {"message": "EcoSmart Agentic Logistics AI Running 🚀"}

@app.get("/agent-status")
def get_agent_status():

    agents = [

        {
            "agent": "Input Agent",
            "status": "Completed",
            "confidence": random.randint(90, 99),
            "latency_ms": random.randint(10, 30)
        },

        {
            "agent": "Route Optimization Agent",
            "status": "Completed",
            "confidence": random.randint(85, 98),
            "latency_ms": random.randint(40, 80)
        },

        {
            "agent": "Sustainability Agent",
            "status": "Completed",
            "confidence": random.randint(80, 95),
            "latency_ms": random.randint(20, 60)
        },

        {
            "agent": "Simulation Agent",
            "status": "Completed",
            "confidence": random.randint(75, 92),
            "latency_ms": random.randint(50, 120)
        },

        {
            "agent": "Executive AI Agent",
            "status": "Standby",
            "confidence": random.randint(70, 90),
            "latency_ms": random.randint(30, 70)
        }

    ]

    return {
        "system_status": "Operational",
        "agents": agents,
        "total_latency": sum(a["latency_ms"] for a in agents)
    }

@app.post("/optimize-route")
def optimize_route(request: RouteRequest):
    result = orchestrator.optimize(request)
    return {"result": result}

@app.post("/executive-advisory")
def executive_advisory(payload: dict):

    result_data = payload.get("result", payload)

    advisory = executive_ai.generate_advisory(result_data)

    return {
        "executive_advisory": advisory
    }

@app.post("/autonomous-decision")
def autonomous_decision(data: dict):

    result = data["result"]

    decision = decision_engine.evaluate(result)

    return decision


