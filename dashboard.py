import folium
from streamlit_folium import st_folium
import streamlit as st
import requests
import plotly.graph_objects as go

# ✅ LIVE BACKEND API (Render)
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

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="EcoSmart Agentic Logistics AI",
    layout="wide"
)

st.title("🌍 EcoSmart Agentic Logistics AI Platform")
st.markdown("AI-powered Sustainable Route Optimization & Executive Advisory")

# -------------------------
# Session State
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
# CALL BACKEND API
# -------------------------
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
            json=payload,
            timeout=60
        )

        if response.status_code == 200:

            st.session_state.result = response.json()["result"]
            st.session_state.advisory = None

        else:
            st.error("API Error")

    except:
        st.error("Backend connection failed. Please wait or retry.")


# -------------------------
# DISPLAY RESULT
# -------------------------
if st.session_state.result:

    result = st.session_state.result

    st.success("Optimization Complete")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Estimated Cost", f"${result['estimated_cost']}")
    col2.metric("🌿 Carbon Impact", f"{result['carbon_impact']} kg CO₂")
    col3.metric("📊 Performance Index", result["overall_performance_index"])


    # Sustainability Gauge
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["sustainability_score"],
        title={'text': "Sustainability Score"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    st.plotly_chart(gauge_fig, use_container_width=True)


    # Agent Flow
    show_agent_flow(result)


    # Executive Advisory Button
    if st.button("Generate Executive Advisory (Nova)"):

        try:

            response = requests.post(
                f"{API_BASE}/executive-advisory",
                json={"result": result},
                timeout=60
            )

            if response.status_code == 200:
                st.session_state.advisory = response.json()["executive_advisory"]

        except:
            st.error("Executive AI temporarily unavailable")


    # Autonomous Decision
    try:

        decision_response = requests.post(
            f"{API_BASE}/autonomous-decision",
            json={"result": result}
        )

        if decision_response.status_code == 200:

            decision_data = decision_response.json()

            st.subheader("Autonomous Decision Engine")

            st.metric("Autonomous Score", decision_data["autonomous_score"])
            st.info(decision_data["explanation"])

    except:
        pass


    # Route Map
    st.subheader("Live Route Map")

    source_coords = CITY_COORDS.get(source)
    dest_coords = CITY_COORDS.get(destination)

    if source_coords and dest_coords:

        m = folium.Map(location=source_coords, zoom_start=5)

        folium.Marker(source_coords).add_to(m)
        folium.Marker(dest_coords).add_to(m)

        folium.PolyLine(
            [source_coords, dest_coords],
            color="blue"
        ).add_to(m)

        st_folium(m, width=800)


# -------------------------
# Agent Monitor
# -------------------------
st.subheader("Live Agent Monitor")

try:

    status_response = requests.get(f"{API_BASE}/agent-status")

    if status_response.status_code == 200:

        status_data = status_response.json()

        st.success(status_data["system_status"])

        for agent in status_data["agents"]:

            col1, col2, col3 = st.columns(3)

            col1.write(agent["agent"])
            col2.write(agent["status"])
            col3.write(f"{agent['confidence']}%")

except:
    st.warning("Agent monitor unavailable")


# -------------------------
# Advisory Display
# -------------------------
if st.session_state.advisory:

    st.subheader("Executive AI Advisory")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Nova Executive AI: Active")

    with col2:
        st.success("Autonomous Decision Engine: Enabled")

    st.info(st.session_state.advisory)
