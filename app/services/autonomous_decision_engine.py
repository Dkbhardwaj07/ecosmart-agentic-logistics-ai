class AutonomousDecisionEngine:

    def evaluate(self, result):

        performance = result["overall_performance_index"]
        sustainability = result["sustainability_score"]
        confidence = result.get("optimization_confidence_score", 50)
        risk = result["risk_level"]

        autonomous_score = int(
            performance * 0.35 +
            sustainability * 0.30 +
            confidence * 0.25 +
            (100 if risk == "Low" else 60 if risk == "Medium" else 40) * 0.10
        )

        if autonomous_score >= 80:
            decision = "AUTO_EXECUTE"
            explanation = "AI approved fully autonomous shipment execution."

        elif autonomous_score >= 60:
            decision = "SEMI_AUTONOMOUS"
            explanation = "AI recommends execution with optional executive review."

        else:
            decision = "EXECUTIVE_REVIEW"
            explanation = "Executive intervention recommended."

        return {
            "autonomous_score": autonomous_score,
            "decision": decision,
            "explanation": explanation,
            "execution_probability": min(99, autonomous_score)
        }
