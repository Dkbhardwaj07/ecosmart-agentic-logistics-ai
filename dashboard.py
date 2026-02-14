import folium
from streamlit_folium import st_folium
import streamlit as st
import requests
import plotly.graph_objects as go

# ✅ YOUR LIVE BACKEND
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

# PAGE CONFIG
st.set_page_config(
    page_title="EcoSmart Agentic Logistics AI",
    layout="wide"
)

st.title("🌍 EcoSmart Agentic Logistics AI Platform")
st.markdown("AI-powered Sustainable Route Optimization using Amazon Nova")

# SESSION STATE
if "result" not in st.session_state:
    st.session_state.result = None

if "advisory" not in st.session_state:
    st.session_state.advisory = None


# AGENT FLOW UI
def show_agent_flow(result):

    st.subheader("AI Multi-Agent Decision Flow")

    agents = [
        ("Input Agent", "Receives logistics request"),
        ("Route Optimization", result["optimized_route"]),
        ("Sustainability", f"Score: {result['sustainability_score']}"),
        ("Risk Analysis", result["risk_level"]),
        ("Simulation", "Scenario Tested"),
        ("Executive AI", "Strategic Advisory"),
        ("Final Decision", f"Index: {result['overall_performance_index']}")
    ]

    rows = [agents[i:i+3] for i in range(0, len(agents), 3)]

    for row in rows:

        cols = st.columns(len(row))

        for col, agent in zip(cols, row):

            with col:
                st.success(agent[0])
                st.write(agent[1])


# INPUT FORM
with st.form("route_form"):

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("Source", "Mumbai")
        destination = st.text_input("Destination", "Delhi")

    with col2:
        cargo_weight = st.number_input("Cargo Weight", value=120)
        priority = st.selectbox("Priority", ["Low","Medium","High"])

    submit = st.form_submit_button("Optimize Route")


# CALL API
if submit:

    payload = {
        "source": source,
        "destination": destination,
        "cargo_weight": cargo_weight,
        "priority": priority
    }

    try:

        res = requests.post(
            f"{API_BASE}/optimize-route",
            json=payload,
            timeout=60
        )

        if res.status_code == 200:

            st.session_state.result = res.json()["result"]

    except:
        st.error("Backend not reachable")


# DISPLAY RESULT
if st.session_state.result:

    result = st.session_state.result

    st.success("Optimization Complete")

    col1,col2,col3 = st.columns(3)

    col1.metric("💰 Estimated Cost", f"${result['estimated_cost']}", "Optimized")
    col2.metric("🌿 Carbon Impact", f"{result['carbon_impact']} kg CO₂", "Reduced")
    col3.metric("📊 Performance Index", result["overall_performance_index"], "AI Optimized")



    # Sustainability Gauge
    st.subheader("AI Sustainability & Optimization Confidence")

    col1, col2 = st.columns(2)

    with col1:
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
                    {'range': [75, 100], 'color': "#00FFA3"},
                ],
            }
        ))

    st.plotly_chart(confidence_fig, use_container_width=True)



    # Confidence Gauge
    st.subheader("AI Confidence")

    confidence = result.get("optimization_confidence_score",75)

    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        gauge={'axis':{'range':[0,100]}}
    ))

    st.plotly_chart(fig2,use_container_width=True)


    # Radar Chart
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
            showlegend=False,
            height=500
        )

    st.plotly_chart(radar, use_container_width=True)



    # Agent Flow
    show_agent_flow(result)


    # Advisory button
    if st.button("Generate Executive Advisory"):

        try:

            res = requests.post(
                f"{API_BASE}/executive-advisory",
                json={"result":result}
            )

            if res.status_code==200:

                st.session_state.advisory=res.json()["executive_advisory"]

        except:
            st.error("Nova unavailable")


    # Autonomous Decision
    try:

        res=requests.post(
            f"{API_BASE}/autonomous-decision",
            json={"result":result}
        )

        if res.status_code==200:

            data=res.json()

            st.subheader("Autonomous Engine")

            st.metric("Score",data["autonomous_score"])

            st.info(data["explanation"])

    except:
        pass


    # MAP
    st.subheader("Route Map")

    src=CITY_COORDS.get(source)
    dst=CITY_COORDS.get(destination)

    if src and dst:

        m=folium.Map(location=src,zoom_start=5)

        folium.Marker(src).add_to(m)
        folium.Marker(dst).add_to(m)

        folium.PolyLine([src,dst]).add_to(m)

        st_folium(m,width=800)


# AGENT STATUS
st.subheader("Agent Monitor")

try:

    res=requests.get(f"{API_BASE}/agent-status")

    if res.status_code==200:

        data=res.json()

        st.success(data["system_status"])

        for agent in data["agents"]:

            col1,col2,col3=st.columns(3)

            col1.write(agent["agent"])
            col2.write(agent["status"])
            col3.write(agent["confidence"])

except:
    st.warning("Monitor offline")


# ADVISORY DISPLAY
if st.session_state.advisory:

    st.subheader("Executive AI Advisory")

    col1,col2=st.columns(2)

    col1.success("Nova Active")
    col2.success("Autonomous Engine Active")

    st.info(st.session_state.advisory)
