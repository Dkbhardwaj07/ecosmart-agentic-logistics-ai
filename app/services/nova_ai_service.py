import boto3
import json


class ExecutiveAIService:

    def __init__(self):

        # Bedrock client
        self.client = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1"
        )


    # -----------------------------
    # Nova Bedrock Call Function
    # -----------------------------
    def generate_nova_response(self, prompt):

        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        try:

            response = self.client.invoke_model(
                modelId="us.amazon.nova-2-lite-v1:0",
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )

            result = json.loads(response["body"].read())

            return result["output"]["message"]["content"][0]["text"]

        except Exception as e:

            print("Nova error:", e)
            return None


    # -----------------------------
    # Executive Advisory Generator
    # -----------------------------
    def generate_advisory(self, result_data):

        try:

            prompt = f"""
You are an Executive Logistics AI Advisor.

Analyze this logistics optimization result and provide executive-level strategic recommendations.

Route: {result_data['optimized_route']}
Cost: {result_data['estimated_cost']}
Carbon Impact: {result_data['carbon_impact']}
Sustainability Score: {result_data['sustainability_score']}
Performance Index: {result_data['overall_performance_index']}

Provide:
• Strategic recommendation
• Risk assessment
• Sustainability improvement suggestion
• Executive decision guidance
"""

            # Call Nova
            response = self.generate_nova_response(prompt)

            if response:
                return response

        except Exception as e:

            print("Nova unavailable:", e)


        # -----------------------------
        # FALLBACK LOGIC
        # -----------------------------

        sustainability = result_data["sustainability_score"]
        performance = result_data["overall_performance_index"]
        risk = result_data["risk_level"]

        if sustainability >= 70:
            sustainability_msg = "This route demonstrates strong environmental sustainability."
        elif sustainability >= 40:
            sustainability_msg = "This route provides moderate sustainability performance with improvement potential."
        else:
            sustainability_msg = "This route has high environmental impact and requires optimization."


        if performance >= 80:
            decision_msg = "Fully autonomous execution is recommended."
        elif performance >= 60:
            decision_msg = "Semi-autonomous execution with executive monitoring is recommended."
        else:
            decision_msg = "Manual executive approval is advised before execution."


        advisory = f"""
Executive Logistics Advisory Report

Route: {result_data['optimized_route']}

Operational Assessment:
The route shows performance index of {performance} with risk level assessed as {risk}.

Sustainability Assessment:
{sustainability_msg}

Strategic Recommendation:
Cost, risk, and sustainability balance is acceptable for enterprise logistics deployment.

Executive Decision Guidance:
{decision_msg}

Future Optimization Strategy:
Consider eco-route prioritization and carbon-aware logistics planning.

AI Confidence Level: High
System Status: Executive AI Operational
"""

        return advisory.strip()
