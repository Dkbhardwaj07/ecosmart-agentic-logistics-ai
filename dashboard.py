import folium
from streamlit_folium import st_folium
import streamlit as st
import requests
import plotly.graph_objects as go

CITY_COORDS = {

    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Chennai": (13.0827, 80.2707),
    "Jaipur": (26.9124, 75.7873),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639)

}

# -------------------------
# Page Config (MUST BE FIRST)
# -------------------------
st.set_page_config(
    page_title="EcoSmart Agentic Logistics AI",
    layout="wide"
)

st.title("🌍 EcoSmart Agentic Logistics AI Platform")
st.markdown("AI-powered Sustainable Route Optimization & Executive Advisory")


# -------------------------
# Session State Init
# -------------------------
if "result" not in st.session_state:
    st.session_state.result = None

if "advisory" not in st.session_state:
    st.session_state.advisory = None


# -------------------------
# Multi-Agent Flow UI
# -------------------------
def show_agent_flow(result):

    st.subheader("AI Multi-Agent Decision Flow")

    agents = [
        ("Input Agent", "Receives logistics request"),
        ("Route Optimization", f"Route: {result['optimized_route']}"),
        ("Sustainability", f"Score: {result['sustainability_score']}"),
        ("Risk Analysis", f"Risk: {result['risk_level']}"),
        ("Simulation", "Scenario tested"),
        ("Executive AI", "Strategic advisory"),
        ("Final Decision", f"Index: {result['overall_performance_index']}")
    ]

    rows = [agents[i:i+3] for i in range(0, len(agents), 3)]

    for row in rows:

        cols = st.columns(len(row))

        for col, (name, desc) in zip(cols, row):

            with col:

                st.markdown(f"""
                <div style="
                    padding:20px;
                    border-radius:12px;
                    background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
                    border:1px solid #00FFA3;
                    text-align:center;
                    font-size:14px;
                    min-height:100px;
                ">
                
                <b>{name}</b><br>
                <span style="color:#00FFA3">{desc}</span>
                
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='text-align:center;font-size:24px'>⬇</div>", unsafe_allow_html=True)


# -------------------------
# Input Form
# -------------------------
with st.form("route_form"):

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("Source City", "Mumbai")
        destination = st.text_input("Destination City", "Delhi")

    with col2:
        cargo_weight = st.number_input("Cargo Weight (kg)", min_value=1, value=120)
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    submitted = st.form_submit_button("Optimize Route")


# -------------------------
# API CALL
# -------------------------
if submitted:

    payload = {
        "source": source,
        "destination": destination,
        "cargo_weight": cargo_weight,
        "priority": priority
    }

    response = requests.post(
        "http://127.0.0.1:8000/optimize-route",
        json=payload
    )

    if response.status_code == 200:

        st.session_state.result = response.json()["result"]
        st.session_state.advisory = None

    else:
        st.error("API Error")


# -------------------------
# DISPLAY RESULT
# -------------------------
if st.session_state.result:

    result = st.session_state.result

    st.success("Optimization Complete")


    # -------------------------
    # KPI METRICS
    # -------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Estimated Cost", f"${result['estimated_cost']}")
    col2.metric("🌿 Carbon Impact", f"{result['carbon_impact']} kg CO₂")
    col3.metric("📊 Performance Index", result["overall_performance_index"])


    # -------------------------
    # Sustainability Gauge
    # -------------------------
    st.subheader("Sustainability Score")

    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["sustainability_score"],
        title={'text': "Sustainability Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "green"},
            ],
        }
    ))

    st.plotly_chart(gauge_fig, use_container_width=True)


    # -------------------------
    # Confidence Meter
    # -------------------------
    st.subheader("AI Optimization Confidence")

    confidence = result.get("optimization_confidence_score", 0)

    confidence_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        title={'text': "Confidence Level"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#00FFA3"},
            'steps': [
                {'range': [0, 50], 'color': "#FF4B4B"},
                {'range': [50, 75], 'color': "#FFA500"},
                {'range': [75, 100], 'color': "#00FFA3"},
            ],
        }
    ))

    st.plotly_chart(confidence_fig, use_container_width=True)


    # -------------------------
    # Carbon Savings
    # -------------------------
    st.subheader("Carbon Savings Impact")

    baseline = result["carbon_impact"] * 1.3
    optimized = result["carbon_impact"]

    saved = max(0, baseline - optimized)

    trees = saved / 21
    km = saved * 4

    col1, col2, col3 = st.columns(3)

    col1.metric("Carbon Saved", f"{saved:.2f} kg CO₂")
    col2.metric("Trees Equivalent", f"{trees:.1f} 🌳")
    col3.metric("Driving Saved", f"{km:.0f} km 🚗")

    percent = int((saved / baseline) * 100) if baseline > 0 else 0
    st.progress(percent)


    # -------------------------
    # Radar Chart
    # -------------------------
    st.subheader("Performance Radar Overview")

    risk_score = 100 if result["risk_level"] == "Low" else 60 if result["risk_level"] == "Medium" else 40
    carbon_eff = max(0, 100 - result["carbon_impact"] / 3)

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=[
            result["overall_performance_index"],
            result["sustainability_score"],
            carbon_eff,
            risk_score
        ],
        theta=[
            "Performance",
            "Sustainability",
            "Carbon Efficiency",
            "Risk Stability"
        ],
        fill='toself'
    ))

    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False
    )

    st.plotly_chart(radar, use_container_width=True)


    # -------------------------
    # Agent Flow
    # -------------------------
    show_agent_flow(result)


    # -------------------------
    # Autonomous Decision Mode
    # -------------------------
    st.subheader("Autonomous AI Decision Mode")

    performance = result["overall_performance_index"]
    sustainability = result["sustainability_score"]
    confidence = result.get("optimization_confidence_score", 50)

    autonomous_score = int(
        performance * 0.4 +
        sustainability * 0.3 +
        confidence * 0.3
    )

    st.metric("Autonomous Decision Score", autonomous_score)

    if autonomous_score >= 80:
        decision = "Fully Autonomous Execution Approved"
        color = "#00FFA3"

    elif autonomous_score >= 60:
        decision = "Semi-Autonomous Execution Recommended"
        color = "#FFA500"

    else:
        decision = "Manual Executive Approval Required"
        color = "#FF4B4B"

    st.markdown(f"""
    <div style="
        padding:20px;
        border-radius:10px;
        border:2px solid {color};
        text-align:center;
        font-size:18px;">
        🤖 <b>{decision}</b>
    </div>
    """, unsafe_allow_html=True)


    # -------------------------
    # Alternative Routes
    # -------------------------
    st.subheader("Alternative Routes")
    st.table(result["alternative_routes"])


    # -------------------------
    # Simulation Analysis
    # -------------------------
    st.subheader("Simulation Analysis")
    st.table(result["simulation_analysis"])


    # -------------------------
    # Decision Explanation
    # -------------------------
    st.subheader("Decision Explanation")
    st.write(result["decision_explanation"])


    # -------------------------
    # Executive Advisory Button
    # -------------------------
    if st.button("Generate Executive Advisory (Nova)"):

        response = requests.post(
            "http://127.0.0.1:8000/executive-advisory",
            json={"result": result}
        )

        if response.status_code == 200:

            st.session_state.advisory = response.json()["executive_advisory"]

        else:

            st.session_state.advisory = "Nova advisory unavailable"

    # -------------------------
    # Autonomous AI Decision Engine
    # -------------------------
    st.subheader("Autonomous AI Execution Engine")

    decision_response = requests.post(
        "http://127.0.0.1:8000/autonomous-decision",
        json={"result": result}
    )

    if decision_response.status_code == 200:

        decision_data = decision_response.json()

        st.metric("Autonomous Score", decision_data["autonomous_score"])

        if decision_data["decision"] == "AUTO_EXECUTE":
            st.success("FULLY AUTONOMOUS EXECUTION APPROVED")

        elif decision_data["decision"] == "SEMI_AUTONOMOUS":
            st.warning("SEMI-AUTONOMOUS EXECUTION")

        else:
            st.error("EXECUTIVE APPROVAL REQUIRED")

        st.info(decision_data["explanation"])

    # -------------------------
    # Live Route Map
    # -------------------------
    st.subheader("Live Route Visualization")

    source_coords = CITY_COORDS.get(source)
    dest_coords = CITY_COORDS.get(destination)

    if source_coords and dest_coords:

        m = folium.Map(location=source_coords, zoom_start=5)

        folium.Marker(
            source_coords,
            tooltip="Source",
            icon=folium.Icon(color="green")
        ).add_to(m)

        folium.Marker(
            dest_coords,
            tooltip="Destination",
            icon=folium.Icon(color="red")
        ).add_to(m)

        folium.PolyLine(
            [source_coords, dest_coords],
            color="blue",
            weight=4
        ).add_to(m)

        st_folium(m, width=800)


# -------------------------
# Live Agent Monitor
# -------------------------
st.subheader("Live AI Agent Monitor")

status_response = requests.get("http://127.0.0.1:8000/agent-status")

if status_response.status_code == 200:

    status_data = status_response.json()

    st.success(f"System Status: {status_data['system_status']}")

    st.metric("Total Pipeline Latency", f"{status_data['total_latency']} ms")

    for agent in status_data["agents"]:

        col1, col2, col3 = st.columns(3)

        col1.write(f"Agent: {agent['agent']}")
        col2.write(f"Status: {agent['status']}")
        col3.write(f"Confidence: {agent['confidence']}%")


# -------------------------
# Advisory Display
# -------------------------
if st.session_state.advisory:

    st.subheader("Executive AI Advisory (Powered by Amazon Nova Bedrock)")

    # Nova Status Badges (ADD HERE)
    col1, col2 = st.columns(2)

    with col1:
        st.success("Nova Executive AI: Active")

    with col2:
        st.success("Autonomous Decision Engine: Enabled")

    # Advisory Output
    st.info(st.session_state.advisory)

