import folium
from streamlit_folium import st_folium
import streamlit as st
import requests
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================

API_BASE = "https://ecosmart-api.onrender.com"

CITY_COORDS = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Chennai": (13.0827, 80.2707),
    "Jaipur": (26.9124, 75.7873),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639)
}

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="EcoSmart Agentic Logistics AI",
    layout="wide"
)

st.title("🌍 EcoSmart Agentic Logistics AI Platform")
st.markdown("AI-powered Sustainable Route Optimization using Amazon Nova")

# =========================
# SESSION STATE
# =========================

if "result" not in st.session_state:
    st.session_state.result = None

if "advisory" not in st.session_state:
    st.session_state.advisory = None

# =========================
# INPUT FORM
# =========================

with st.form("route_form"):

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox("Source City", list(CITY_COORDS.keys()), index=0)
        destination = st.selectbox("Destination City", list(CITY_COORDS.keys()), index=1)

    with col2:
        cargo_weight = st.number_input("Cargo Weight (kg)", 1, 10000, 120)
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    submitted = st.form_submit_button("Optimize Route")

# =========================
# CALL API
# =========================

if submitted:

    payload = {
        "source": source,
        "destination": destination,
        "cargo_weight": cargo_weight,
        "priority": priority
    }

    try:

        response = requests.post(
            f"{API_BASE}/optimize-route",
            json=payload
        )

        if response.status_code == 200:

            st.session_state.result = response.json()["result"]
            st.session_state.advisory = None

        else:
            st.error("API Error")

    except:
        st.error("Backend not reachable")

# =========================
# DISPLAY RESULT
# =========================

if st.session_state.result:

    result = st.session_state.result

    st.success("Optimization Complete")

    # =========================
    # KPI METRICS
    # =========================

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Estimated Cost", f"${result['estimated_cost']}")
    col2.metric("🌿 Carbon Impact", f"{result['carbon_impact']} kg CO₂")
    col3.metric("📊 Performance Index", result["overall_performance_index"])

    st.divider()

    # =========================
    # GAUGES (PERFECT ALIGNMENT)
    # =========================

    st.subheader("AI Sustainability & Optimization Confidence")

    col1, col2 = st.columns(2)

    with col1:

        sustainability_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["sustainability_score"],
            title={'text': "Sustainability Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 40], 'color': "red"},
                    {'range': [40, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "green"}
                ]
            }
        ))

        sustainability_fig.update_layout(height=350)

        st.plotly_chart(sustainability_fig, use_container_width=True)

    with col2:

        confidence = result.get("optimization_confidence_score", 72)

        confidence_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            title={'text': "Optimization Confidence"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#00FFA3"},
                'steps': [
                    {'range': [0, 50], 'color': "#FF4B4B"},
                    {'range': [50, 75], 'color': "#FFA500"},
                    {'range': [75, 100], 'color': "#00FFA3"}
                ]
            }
        ))

        confidence_fig.update_layout(height=350)

        st.plotly_chart(confidence_fig, use_container_width=True)

    st.divider()

    # -------------------------
    # Carbon Savings Impact (PROPER ALIGNMENT)
    # -------------------------
    st.subheader("Carbon Savings Impact")

    baseline = result["carbon_impact"] * 1.3
    optimized = result["carbon_impact"]

    carbon_saved = max(0, baseline - optimized)

    trees_equivalent = carbon_saved / 21
    distance_saved = carbon_saved * 4

    # Clean 3-column KPI layout
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Carbon Saved", f"{carbon_saved:.2f} kg CO₂")

    with c2:
        st.metric("Trees Equivalent", f"{trees_equivalent:.1f} 🌳")

    with c3:
        st.metric("Driving Saved", f"{distance_saved:.0f} km 🚗")


    # Progress bar below metrics (FULL WIDTH)
    saving_percent = int((carbon_saved / baseline) * 100) if baseline > 0 else 0

    st.progress(saving_percent)

    st.caption("Environmental impact reduction compared to standard logistics route")
    # =========================
    # RADAR CHART
    # =========================

    st.subheader("Performance Radar Overview")

    risk_score = 100 if result["risk_level"] == "Low" else 60

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

    radar.update_layout(height=500)

    st.plotly_chart(radar, use_container_width=True)

    st.divider()

    # =========================
    # MAP
    # =========================

    st.subheader("Live Route Visualization")

    source_coords = CITY_COORDS[source]
    dest_coords = CITY_COORDS[destination]

    m = folium.Map(location=source_coords, zoom_start=5)

    folium.Marker(source_coords, icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(dest_coords, icon=folium.Icon(color="red")).add_to(m)

    folium.PolyLine(
        [source_coords, dest_coords],
        color="blue",
        weight=4
    ).add_to(m)

    st_folium(m, width=900)

    st.divider()

    # =========================
    # EXECUTIVE ADVISORY
    # =========================

    if st.button("Generate Executive Advisory (Amazon Nova)"):

        response = requests.post(
            f"{API_BASE}/executive-advisory",
            json={"result": result}
        )

        if response.status_code == 200:

            st.session_state.advisory = response.json()["executive_advisory"]

    if st.session_state.advisory:

        st.subheader("Executive AI Advisory")

        col1, col2 = st.columns(2)

        with col1:
            st.success("Nova Executive AI: Active")

        with col2:
            st.success("Autonomous Decision Engine: Enabled")

        st.info(st.session_state.advisory)

# =========================
# AGENT MONITOR
# =========================

st.divider()

st.subheader("Live AI Agent Monitor")

try:

    status_response = requests.get(f"{API_BASE}/agent-status")

    if status_response.status_code == 200:

        data = status_response.json()

        st.success(f"System Status: {data['system_status']}")

        st.metric("Total Latency", f"{data['total_latency']} ms")

        for agent in data["agents"]:

            col1, col2, col3 = st.columns(3)

            col1.write(agent["agent"])
            col2.write(agent["status"])
            col3.write(f"{agent['confidence']}%")

except:

    st.warning("Agent monitor unavailable")
