import boto3
import json

class NovaAIService:

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1"
        )

    def generate_reasoning(self, context_data):

        prompt = f"""
        You are a logistics sustainability AI.

        Given the following system decision:

        Route: {context_data['route']}
        Cost: {context_data['cost']}
        Carbon Impact: {context_data['carbon']}
        Risk Level: {context_data['risk']}
        Sustainability Score: {context_data['score']}

        Provide a short professional explanation of why this decision was made,
        including environmental and operational trade-offs.
        """

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

        except Exception:
            return None
