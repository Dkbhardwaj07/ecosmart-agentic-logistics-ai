# 🌍 EcoSmart Agentic Logistics AI Platform
### Powered by Amazon Nova (AWS Bedrock) | Multi-Agent Autonomous Decision Intelligence

EcoSmart Agentic Logistics AI is an enterprise-grade autonomous logistics optimization platform built using Amazon Nova foundation models on AWS Bedrock.

The system uses a multi-agent AI architecture to optimize logistics routes by balancing operational cost, carbon emissions, sustainability impact, and execution risk.

Built for the Amazon Nova AI Hackathon 2026.

---

# 🚀 Key Features

### 🤖 Multi-Agent AI Architecture
Specialized agents collaborate autonomously:

• Route Optimization Agent  
• Sustainability Intelligence Agent  
• Carbon Impact Analysis Agent  
• Risk Assessment Agent  
• Simulation & Scenario Analysis Agent  
• Executive Advisory Agent (Powered by Amazon Nova)  
• Autonomous Decision Engine  

---

### 🌱 Sustainability Intelligence Engine
Analyzes:

• Carbon emissions  
• Sustainability score  
• Environmental efficiency  
• Carbon savings potential  

Provides eco-optimized logistics recommendations.

---

### 🧠 Amazon Nova Executive Advisory Layer
Uses Amazon Nova foundation model via AWS Bedrock to generate:

• Executive-level logistics advisory  
• Strategic sustainability recommendations  
• Risk-aware deployment decisions  
• Autonomous execution guidance  

---

### ⚡ Autonomous AI Decision Engine
Calculates:

• Performance Index  
• Autonomous Execution Score  
• Decision classification:

- Fully Autonomous Execution
- Semi-Autonomous Execution
- Executive Approval Required

---

### 📊 Interactive AI Dashboard
Streamlit-based dashboard provides:

• Real-time route optimization  
• Sustainability score visualization  
• Carbon savings analysis  
• Multi-agent decision flow visualization  
• Autonomous execution monitoring  
• Live AI agent status monitoring  

---

### 🗺️ Live Route Visualization
Displays:

• Source and destination mapping  
• Route visualization  
• Real-time logistics decision context  

---

# 🏗️ System Architecture

Frontend:
Streamlit Dashboard

Backend:
FastAPI Autonomous Multi-Agent System

AI Model:
Amazon Nova (AWS Bedrock)

Cloud Platform:
AWS + Streamlit Cloud

---

# 🧠 Amazon Nova Integration

Amazon Nova foundation model is used for:

• Executive AI advisory generation  
• Strategic logistics reasoning  
• Autonomous sustainability-aware decision support  

Service used:

AWS Bedrock Runtime  
Model: Nova 2 Lite  

---

# 📂 Project Structure

ecosmart-agentic-logistics-ai/
│
├── app/
│ ├── agents/
│ │ ├── route_agent.py
│ │ ├── sustainability_agent.py
│ │ ├── carbon_agent.py
│ │ ├── risk_agent.py
│ │ ├── simulation_agent.py
│ │ ├── performance_agent.py
│ │ └── orchestrator.py
│ │
│ ├── services/
│ │ ├── executive_ai_service.py
│ │ ├── autonomous_decision_engine.py
│ │ └── nova_ai_service.py
│ │
│ └── main.py
│
├── dashboard.py
├── requirements.txt
├── README.md
└── .streamlit/config.toml


---

# ⚙️ Installation

Clone repository:

git clone https://github.com/Dkbhardwaj07/ecosmart-agentic-logistics-ai

Install dependencies:
pip install -r requirements.txt


Run backend:
uvicorn app.main:app --reload

Run dashboard:
streamlit run dashboard.py

---

# 🧪 Example API Request

POST /optimize-route
{
"source": "Mumbai",
"destination": "Delhi",
"cargo_weight": 120,
"priority": "High"
}


Example Response:

{
"optimized_route": "Mumbai → Delhi",
"estimated_cost": 330,
"carbon_impact": 105.6,
"sustainability_score": 42,
"overall_performance_index": 60,
"optimization_confidence_score": 67
}


---

# 📊 AI Output Includes

• Optimized logistics route  
• Sustainability score  
• Carbon emission impact  
• Performance index  
• Alternative route simulation  
• Autonomous execution decision  
• Executive AI advisory  

---

# 🎥 Demo Video

(To be added)

---

# 🌍 Live Demo

(To be added after deployment)

---

# 🏆 Hackathon Submission Details

Hackathon:
Amazon Nova AI Hackathon 2026

Category:
Agentic AI

Core Requirement Met:
Uses Amazon Nova foundation model via AWS Bedrock.

---

# 🌟 Innovation Highlights

• Real-world enterprise logistics use case  
• Multi-agent autonomous AI architecture  
• Sustainability-aware optimization  
• Executive-level AI decision intelligence  
• Amazon Nova integration  

---

# 👨‍💻 Developer

Durgesh Bhardwaj  
Software Engineer  

GitHub:
https://github.com/Dkbhardwaj07

---

# 📜 License

MIT License

