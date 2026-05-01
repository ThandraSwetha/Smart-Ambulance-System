import streamlit as st
import time
import random
import folium
from streamlit_folium import st_folium

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="QuickDoc Emergency Tracker",
    page_icon="🚑",
    layout="wide"
)

# ---------------- PROFESSIONAL WHITE UI ----------------
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: white;
}

/* HEADER */
.main-title {
    font-size: 34px;
    font-weight: 700;
    color: #374151;
    text-align: center;
}

/* SUBTITLE */
.subtitle {
    text-align:center;
    color:#6b7280;
    margin-bottom:20px;
}

/* CARD DESIGN */
.card {
    background: white;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* RED ROUNDED BUTTON */
.stButton>button {
    background: #ef4444 !important;
    color: white !important;
    border-radius: 999px !important;
    padding: 12px 28px !important;
    border: none !important;
    font-weight: 600 !important;
}

.stButton>button:hover {
    background: #dc2626 !important;
}

/* BIG EMERGENCY BUTTON */
.big-btn button {
    height: 60px;
    font-size: 18px;
    width: 100%;
}

/* TABS STYLE */
button[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "started" not in st.session_state:
    st.session_state.started = False

if "route_index" not in st.session_state:
    st.session_state.route_index = 0

if "patient" not in st.session_state:
    st.session_state.patient = {}

# ---------------- LOCATIONS ----------------
AMBULANCE_BASE = (17.4948, 78.3996)
PATIENT_HOME = (17.4850, 78.3850)
HOSPITAL = (17.4530, 78.3910)

# ---------------- ROUTE FUNCTION ----------------
def interpolate(start, end, steps=25):
    lat1, lon1 = start
    lat2, lon2 = end
    return [
        (lat1 + (lat2-lat1)*i/steps, lon1 + (lon2-lon1)*i/steps)
        for i in range(steps+1)
    ]

to_patient = interpolate(AMBULANCE_BASE, PATIENT_HOME)
to_hospital = interpolate(PATIENT_HOME, HOSPITAL)
FULL_ROUTE = to_patient + to_hospital

# ---------------- HEADER ----------------
st.markdown(
    "<div class='main-title'>🚑 ONE-TAP EMERGENCY AMBULANCE DISPATCH SYSTEM & LIVE TRACKING</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Automated Emergency Response Dashboard</div>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- TABS ----------------
t1, t2, t3, t4 = st.tabs([
    "🚨 Emergency",
    "🚑 Ambulance Status",
    "🗺 Live Tracking",
    "🏥 Patient & Hospital"
])

# ================= EMERGENCY TAB =================
with t1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Trigger Emergency")

    col1, col2 = st.columns(2)

    with col1:
        st.radio("Emergency Type", [
            "Accident",
            "Trauma",
            "Cardiac Emergency",
            "Maternity"
        ])

    with col2:
        st.selectbox("Severity Level", ["Low", "Medium", "High"])

    st.markdown("<div class='big-btn'>", unsafe_allow_html=True)

    if st.button("🚨 ONE-TAP EMERGENCY"):
        st.session_state.started = True
        st.session_state.route_index = 0
        st.success("Emergency Activated 🚑 Ambulance Dispatched")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= AMBULANCE STATUS =================
with t2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Ambulance Dispatch Status")

    if st.session_state.started:
        st.success("Nearest Ambulance Assigned")
        st.markdown(f"### Ambulance ID: AMB-{random.randint(100,999)}")
        st.progress(70)
    else:
        st.info("No active emergency")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= LIVE MAP =================
with t3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Live Ambulance Route Tracking")

    if st.session_state.started:

        start_btn = st.button("▶ Start Ambulance Movement")
        placeholder = st.empty()

        if start_btn:
            for i in range(len(FULL_ROUTE)):
                st.session_state.route_index = i
                current = FULL_ROUTE[i]

                with placeholder.container():
                    m = folium.Map(location=current, zoom_start=14)

                    folium.Marker(
                        AMBULANCE_BASE,
                        tooltip="Ambulance Base",
                        icon=folium.Icon(color="blue")
                    ).add_to(m)

                    folium.Marker(
                        PATIENT_HOME,
                        tooltip="Patient Home",
                        icon=folium.Icon(color="red")
                    ).add_to(m)

                    folium.Marker(
                        HOSPITAL,
                        tooltip="Hospital",
                        icon=folium.Icon(color="green")
                    ).add_to(m)

                    folium.PolyLine(
                        FULL_ROUTE[:i+1],
                        color="blue",
                        weight=5
                    ).add_to(m)

                    folium.Marker(
                        current,
                        tooltip="🚑 Ambulance",
                        icon=folium.Icon(color="orange")
                    ).add_to(m)

                    st_folium(m, width=900, height=500)

                    if i < len(to_patient):
                        st.info("🚑 Ambulance going to patient home...")
                    elif i == len(to_patient):
                        st.success("✅ Patient picked up!")
                    else:
                        st.warning("🏥 Transporting patient to hospital...")

                time.sleep(0.3)

    else:
        st.info("Activate emergency first")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PATIENT FORM =================
with t4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Hospital Pre-Admission Form")

    if st.session_state.started:

        with st.form("patient_form"):
            st.session_state.patient["Name"] = st.text_input("Patient Name")
            st.session_state.patient["Phone"] = st.text_input("Phone Number")
            st.session_state.patient["Address"] = st.text_area("Address")
            st.session_state.patient["Blood Group"] = st.selectbox(
                "Blood Group",
                ["A+","A-","B+","B-","O+","O-","AB+","AB-","Unknown"]
            )

            submit = st.form_submit_button("Send to Hospital")

        if submit:
            st.success("Patient details sent to hospital ✅")
            st.write("### Patient Summary")
            for k, v in st.session_state.patient.items():
                st.write(f"**{k}:** {v}")

    else:
        st.info("Waiting for emergency activation")

    st.markdown("</div>", unsafe_allow_html=True)