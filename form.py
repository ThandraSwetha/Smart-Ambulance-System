import streamlit as st
import time
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="QuickDoc Hospital Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "alerts" not in st.session_state:
    st.session_state.alerts = []
if "animate" not in st.session_state:
    st.session_state.animate = True

# ---------------- CSS & ANIMATIONS ----------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main, .block-container, section.main {
    background-color: #f6f8fb !important;
    color: #111111 !important;
    min-height: 100vh;
}
body {
    background: linear-gradient(180deg, #ffffff 0%, #f3f6fb 55%, #eef3f9 100%) !important;
    color: #111111 !important;
}
.block-container {
    padding: 2rem 2rem 3rem !important;
}
.card {
    background: rgba(255,255,255,0.96);
    color: #111111;
    padding: 28px;
    border-radius: 24px;
    border: 1px solid rgba(15, 23, 42, 0.06);
    box-shadow: 0 24px 70px rgba(14, 30, 60, 0.12);
    animation: floatIn 0.85s ease-out;
}
.alert {
    background: #f8d5ff;
    color: #111111;
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 16px;
    border: 1px solid rgba(248, 213, 255, 0.35);
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.7), 0 10px 30px rgba(248, 213, 255, 0.24);
    animation: pulse 2s ease-in-out infinite;
}
.success {
    background: rgba(255,255,255,0.96);
    color: #111111;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(34, 197, 94, 0.18);
    box-shadow: 0 14px 35px rgba(34, 197, 94, 0.12);
}
.stButton > button, .stDownloadButton > button {
    background: #e6e8fa !important;
    color: #111111 !important;
    border: 1px solid rgba(230, 232, 250, 0.5) !important;
    border-radius: 16px !important;
    padding: 0.95rem 1.6rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    box-shadow: 0 20px 60px rgba(230, 232, 250, 0.3) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
    animation: buttonGlow 3s ease-in-out infinite alternate;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #d4d6f0 !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 24px 70px rgba(230, 232, 250, 0.4) !important;
}
.stTitle, .stHeader, .css-1v0mbdj, h1, h2, h3, h4, h5, h6 {
    color: #111111 !important;
    animation: popIn 0.85s ease-out;
    text-align: center !important;
}
.stCaption, small, .stMarkdown small {
    text-align: center !important;
}
.stMarkdown h2, .stMarkdown h3 {
    color: #111111 !important;
}
.stSubheader {
    color: #111111 !important;
}
@keyframes pulse {
    0% { box-shadow: inset 0 0 0 1px rgba(248, 213, 255, 0.35), 0 10px 30px rgba(248, 213, 255, 0.24); }
    50% { box-shadow: inset 0 0 0 1px rgba(248, 213, 255, 0.45), 0 14px 40px rgba(248, 213, 255, 0.30); }
    100% { box-shadow: inset 0 0 0 1px rgba(248, 213, 255, 0.35), 0 10px 30px rgba(248, 213, 255, 0.24); }
}
@keyframes floatIn {
    from { opacity: 0; transform: translateY(20px) scale(0.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes popIn {
    from { opacity: 0; transform: translateY(14px) scale(0.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes buttonGlow {
    from { box-shadow: 0 18px 45px rgba(230, 232, 250, 0.2); }
    to { box-shadow: 0 26px 72px rgba(230, 232, 250, 0.3); }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div style="text-align:center; margin-bottom: 0.8rem;">
    <h1 style="margin:0; font-size:2.5rem; color:#111111;">🏥 QuickDoc – Hospital Emergency Dashboard</h1>
    <p style="margin:0.65rem 0 0; color:#4b5563; font-size:1rem;">Live incoming ambulance & patient pre-admission system</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# ---------------- SIMULATED INCOMING DATA ----------------
def generate_emergency():
    return {
        "patient": random.choice(["Ramesh", "Sita", "Arjun", "Meena"]),
        "blood": random.choice(["A+", "B+", "O+", "AB+", "O-"]),
        "emergency": random.choice([
            "Accident / Trauma",
            "Cardiac Emergency",
            "Maternity"
        ]),
        "ambulance": f"AMB-{random.randint(100,999)}",
        "eta": random.randint(3, 10)
    }

# ---------------- CONTROL PANEL ----------------
col1, col2 = st.columns([3,1])
with col2:
    if st.button("🚨 Simulate New Emergency"):
        st.session_state.alerts.insert(0, generate_emergency())

# ---------------- ALERTS ----------------
colA, colB = st.columns([2,3])

with colA:
    st.subheader("🚑 Incoming Ambulances")

    if not st.session_state.alerts:
        st.info("No incoming emergencies")
    else:
        for alert in st.session_state.alerts:
            st.markdown(f"""
            <div class="alert">
                <b>🚨 Emergency:</b> {alert['emergency']}<br>
                <b>🚑 Ambulance:</b> {alert['ambulance']}<br>
                <b>⏳ ETA:</b> {alert['eta']} minutes
            </div>
            """, unsafe_allow_html=True)

with colB:
    st.subheader("🧾 Patient Pre-Admission Details")

    if st.session_state.alerts:
        p = st.session_state.alerts[0]
        st.markdown(f"""
        <div class="card">
            <h3>🧑 Patient: {p['patient']}</h3>
            <p><b>Emergency:</b> {p['emergency']}</p>
            <p><b>Blood Group:</b> {p['blood']}</p>
            <p><b>Ambulance ID:</b> {p['ambulance']}</p>
            <p><b>ETA:</b> {p['eta']} minutes</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✅ Prepare Emergency Ward"):
            st.success("Emergency ward & doctors notified!")
    else:
        st.info("Waiting for ambulance data")

# ---------------- FOOTER ----------------
st.divider()
st.caption("QuickDoc Hospital System | Smart Emergency Healthcare 🚑")