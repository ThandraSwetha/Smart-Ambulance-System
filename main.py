# import streamlit as st
# import time
# import random
# import folium
# from streamlit_folium import st_folium

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="QuickDoc Emergency Tracker",
#     page_icon="🚑",
#     layout="wide"
# )

# # ---------------- SESSION STATE ----------------
# if "route_index" not in st.session_state:
#     st.session_state.route_index = 0
# if "started" not in st.session_state:
#     st.session_state.started = False
# if "emergency" not in st.session_state:
#     st.session_state.emergency = None
# if "animation_frame" not in st.session_state:
#     st.session_state.animation_frame = 0
# if "auto_play" not in st.session_state:
#     st.session_state.auto_play = True

# # ---------------- ROUTES ----------------
# ROUTES = {
#     "Accident / Trauma": ["Lingampally", "Chandanagar", "Miyapur", "Kukatpally", "City Trauma Hospital"],
#     "Cardiac Emergency": ["Lingampally", "BHEL", "KPHB", "Heart Care Hospital"],
#     "Maternity": ["Lingampally", "Chandanagar", "Maternity Care Hospital"]
# }

# # ---------------- LOCATIONS ----------------
# LOCATIONS = {
#     "Home": [17.4448, 78.3719],
#     "Patient": [17.4495, 78.3751],
#     "Hospital": [17.4200, 78.4500]
# }

# # ---------------- CSS STYLING ----------------
# st.markdown("""
# <style>
# .stApp { background: white; color: black; }

# .glass {
#     background: rgba(255,255,255,0.4);
#     backdrop-filter: blur(8px);
#     -webkit-backdrop-filter: blur(8px);
#     padding: 20px;
#     border-radius: 18px;
#     margin-bottom: 20px;
#     border: 1px solid rgba(255,255,255,0.3);
# }

# div[role="radiogroup"] label { color: black !important; }
# div[role="radiogroup"] p { color: black !important; }

# .stButton > button {
#     background-color: white !important;
#     color: black !important;
#     border: 2px solid red !important;
#     border-radius: 12px !important;
#     padding: 12px 20px !important;
#     font-weight: bold !important;
# }
# .stButton > button:hover { background-color: #f5f5f5 !important; }

# .stTabs [data-baseweb="tab"] {
#     background: #ef4444;
#     color: white;
#     border-radius: 999px;
#     padding: 10px 25px;
# }
# .stTabs [aria-selected="true"] {
#     background: #dc2626 !important;
#     color: white !important;
# }

# /* Map Full Width */
# iframe { width: 100% !important; max-width: none !important; }
# [data-testid="stIFrame"] { width: 100% !important; }

# # /* Patient Form White Background */
# # form { background-color: white ; padding: 20px; border-radius: 12px; }
# # .stTextInput > div > input, 
# # .stTextArea > div > textarea, 
# # .stSelectbox > div > div > div {
# #     background-color: white ; border-radius: 8px;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- HEADER ----------------
# st.markdown("<h1 style='text-align:center;'>🚑 ONE-TAP EMERGENCY & LIVE AMBULANCE TRACKING</h1>", unsafe_allow_html=True)
# st.divider()

# # ---------------- TABS ----------------
# t1, t2, t3, t4 = st.tabs([
#     "🆘 Emergency",
#     "🚑 Ambulance",
#     "🗺 Live Route",
#     "🏥 Patient & Hospital"
# ])

# # ================= EMERGENCY =================
# with t1:
#     st.markdown("<div class='glass'>", unsafe_allow_html=True)
#     st.subheader("🆘 Trigger Emergency")

#     emergency_type = st.radio("Select Emergency Type", list(ROUTES.keys()), horizontal=True)

#     if st.button("🚨 ONE-TAP EMERGENCY", use_container_width=True):
#         st.session_state.started = True
#         st.session_state.route_index = 0
#         st.session_state.animation_frame = 0
#         st.session_state.auto_play = True
#         st.session_state.emergency = emergency_type
#         st.success("Emergency Activated 🚨 Ambulance Dispatched")

#     st.markdown("</div>", unsafe_allow_html=True)

# # ================= AMBULANCE =================
# with t2:
#     st.markdown("<div class='glass'>", unsafe_allow_html=True)
#     st.subheader("🚑 Ambulance Dispatch Status")

#     if st.session_state.started:
#         st.success("Nearest Ambulance Assigned")
#         st.markdown(f"### 🚑 Ambulance ID: AMB-{random.randint(100,999)}")
#         st.progress(70)
#     else:
#         st.info("No active emergency")

#     st.markdown("</div>", unsafe_allow_html=True)

# # ================= LIVE ROUTE =================
# def interpolate_route(start, end, steps=25):
#     """Create smooth interpolated waypoints between two locations"""
#     lat_diff = end[0] - start[0]
#     lon_diff = end[1] - start[1]
#     return [[start[0] + lat_diff * i / steps, start[1] + lon_diff * i / steps] 
#             for i in range(steps + 1)]

# # Build complete route with interpolation
# full_route = (
#     interpolate_route(LOCATIONS["Home"], LOCATIONS["Patient"], steps=20) +
#     interpolate_route(LOCATIONS["Patient"], LOCATIONS["Hospital"], steps=25)[1:]
# )

# with t3:
#     if st.session_state.started:
#         st.markdown("<div style='display:flex; align-items:center; justify-content:space-between; gap:20px;'>"
#                     "<div><h3 style='margin:0;'>🗺 Live Ambulance Tracking</h3></div>"
#                     "</div>", unsafe_allow_html=True)
        
#         frame = st.session_state.animation_frame
#         if frame < 0:
#             frame = 0
#         elif frame >= len(full_route):
#             frame = len(full_route) - 1

#         current_pos = full_route[frame]
#         journey_pct = int((frame / (len(full_route) - 1)) * 100)
#         stage = "En route to patient" if frame < 20 else "Heading to hospital"
#         next_stop = "Patient" if frame < 20 else "Hospital"

#         summary_col1, summary_col2, summary_col3 = st.columns([2, 1, 1])
#         with summary_col1:
#             st.markdown(f"**Stage:** {stage}  ")
#             st.markdown(f"**Next stop:** {next_stop}  ")
#         with summary_col2:
#             st.metric("Progress", f"{journey_pct}%")
#         with summary_col3:
#             st.metric("Status", "In Transit" if journey_pct < 100 else "Arrived")

#         st.progress(journey_pct / 100)
#         st.markdown("---")

#         # Control buttons
#         control_col1, control_col2 = st.columns([1,1])
#         with control_col1:
#             if frame == len(full_route) - 1:
#                 play_label = "🔁 Replay"
#             else:
#                 play_label = "⏸ Pause" if st.session_state.auto_play else "▶ Play"

#             if st.button(play_label, use_container_width=True):
#                 if frame == len(full_route) - 1:
#                     st.session_state.animation_frame = 0
#                     st.session_state.auto_play = True
#                 else:
#                     st.session_state.auto_play = not st.session_state.auto_play
#         with control_col2:
#             frame = st.slider("Position", 0, len(full_route)-1, frame, key="ambulance_slider")
#             st.session_state.animation_frame = frame
#             if frame < len(full_route) - 1:
#                 st.session_state.auto_play = False

#         # Build map
#         m = folium.Map(
#             location=current_pos,
#             zoom_start=15,
#             tiles='CartoDB dark_matter',
#             attr='CartoDB'
#         )

#         # Future route (dashed grey)
#         folium.PolyLine(
#             full_route[frame:],
#             color="#9CA3AF",
#             weight=4,
#             opacity=0.45,
#             dash_array="8,6"
#         ).add_to(m)

#         # Traveled route (moving red)
#         if frame > 0:
#             folium.PolyLine(
#                 full_route[:frame+1],
#                 color="#F87171",
#                 weight=6,
#                 opacity=0.95
#             ).add_to(m)

#         folium.Marker(
#             LOCATIONS["Home"],
#             popup="<b>🏠 Ambulance Base</b>",
#             tooltip="Ambulance Base",
#             icon=folium.Icon(color="blue", icon="building", prefix="fa")
#         ).add_to(m)

#         folium.Marker(
#             LOCATIONS["Patient"],
#             popup="<b>🏥 Patient Location</b>",
#             tooltip="Patient Location",
#             icon=folium.Icon(color="red", icon="heart", prefix="fa")
#         ).add_to(m)

#         folium.Marker(
#             LOCATIONS["Hospital"],
#             popup="<b>🏗️ Hospital</b>",
#             tooltip="Hospital",
#             icon=folium.Icon(color="green", icon="hospital", prefix="fa")
#         ).add_to(m)

#         folium.CircleMarker(
#             location=current_pos,
#             radius=18,
#             popup=f"<b>🚑 Ambulance</b><br>{journey_pct}% Complete",
#             tooltip="Ambulance",
#             color="#F97316",
#             fill=True,
#             fillColor="#FB923C",
#             fillOpacity=0.95,
#             weight=3
#         ).add_to(m)

#         folium.Marker(
#             current_pos,
#             popup=f"<b>🚑 Ambulance</b><br>{journey_pct}% Complete",
#             icon=folium.Icon(color="orange", icon="ambulance", prefix="fa", icon_color="white")
#         ).add_to(m)

#         st_folium(m, width=1080, height=620, key="ambulance_tracker_interactive")

#         if st.session_state.auto_play and frame < len(full_route) - 1:
#             time.sleep(0.12)
#             st.session_state.animation_frame += 1
#             st.experimental_rerun()
#     else:
#         st.info("🔔 Activate emergency to start tracking")

# # ================= PATIENT INFO =================

#   # ================= PATIENT INFO =================
# with t4:
#     st.markdown("""
#     <style>
#     /* Form container */
#     div[data-testid="stForm"] {
#         background-color: white !important;
#         padding: 20px !important;
#         border-radius: 12px !important;
#         border: 1px solid #ddd !important;
#     }

#     /* Inputs */
#     div[data-testid="stForm"] input,
#     div[data-testid="stForm"] textarea {
#         background-color: white !important;
#         color: black !important;
#         border-radius: 8px !important;
#         border: 1px solid #ccc !important;
#     }

#     /* 🔥 DROPDOWN FULL FIX */
#     div[data-testid="stForm"] div[data-baseweb="select"] {
#         background-color: white !important;
#         color: black !important;
#     }

#     div[data-testid="stForm"] div[data-baseweb="select"] * {
#         background-color: white !important;
#         color: black !important;
#     }

#     /* Labels */
#     div[data-testid="stForm"] label {
#         color: black !important;
#         font-weight: 500;
#     }

#     /* Button */
#     div[data-testid="stForm"] button {
#         background-color: white !important;
#         color: black !important;
#         border: 2px solid #ccc !important;
#         border-radius: 8px !important;
#         font-weight: bold !important;
#     }

#     div[data-testid="stForm"] button:hover {
#         background-color: #f5f5f5 !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     st.markdown("<div class='glass'>", unsafe_allow_html=True)
#     st.subheader("🏥 Hospital Pre-Admission Form")

#     if st.session_state.started:
#         with st.form("details"):
#             name = st.text_input("Patient Name")
#             phone = st.text_input("Phone Number")
#             address = st.text_area("Address")
#             blood = st.selectbox("Blood Group", ["A+","A-","B+","B-","O+","O-","AB+","AB-","Unknown"])
#             submit = st.form_submit_button("📤 Send to Hospital")

#         if submit:
#             st.success("Patient details sent to hospital ✅")
#             st.success(f"🏥 Assigned Hospital: {ROUTES[st.session_state.emergency][-1]}")
#     else:
#         st.info("Waiting for emergency activation")

#     st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st
import time
import random
import folium
from streamlit_folium import st_folium
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="QuickDoc Emergency Tracker",
    page_icon="🚑",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "route_index" not in st.session_state:
    st.session_state.route_index = 0
if "started" not in st.session_state:
    st.session_state.started = False
if "emergency" not in st.session_state:
    st.session_state.emergency = None
if "animation_frame" not in st.session_state:
    st.session_state.animation_frame = 0
if "auto_play" not in st.session_state:
    st.session_state.auto_play = True
if "alerts" not in st.session_state:
    st.session_state.alerts = []

# ---------------- ROUTES ----------------
ROUTES = {
    "Accident / Trauma": ["Lingampally", "Chandanagar", "Miyapur", "Kukatpally", "City Trauma Hospital"],
    "Cardiac Emergency": ["Lingampally", "BHEL", "KPHB", "Heart Care Hospital"],
    "Maternity": ["Lingampally", "Chandanagar", "Maternity Care Hospital"]
}

# ---------------- LOCATIONS ----------------
LOCATIONS = {
    "Home": [17.4448, 78.3719],
    "Patient": [17.4495, 78.3751],
    "Hospital": [17.4200, 78.4500]
}

# ---------------- CSS STYLING ----------------
st.markdown("""
<style>
/* MAIN APP BACKGROUND */
.stApp { 
    background: white !important; 
    color: black !important; 
}

body {
    background: white !important;
}

html {
    background: white !important;
}

/* AGGRESSIVE SIDEBAR LIGHT PINK BACKGROUND - ALL ELEMENTS */
[data-testid="stSidebar"] {
    # background: #e1bee7 !important;
    background-color: #e1bee7 !important;
}

[data-testid="stSidebar"] > * {
    # background: #e1bee7 !important;
    background-color: #e1bee7 !important;
}

/* Target all sidebar children recursively */
[data-testid="stSidebar"] div {
    background-color: #fce4ec !important;
}

[data-testid="stSidebar"] section {
    background: #e1bee7 !important;
}

/* Sidebar nav and containers */
[data-testid="stSidebarNav"] {
    background: #fce4ec !important;
}

.css-1wsmje0 {
    background: #e1bee7 !important;
}

/* Hide any background images or gradients */
[data-testid="stSidebar"]::before,
[data-testid="stSidebar"]::after {
    background: none !important;
}

/* All text in sidebar - DARK PURPLE for pink background */
[data-testid="stSidebar"] {
    color: #5e35b1 !important;
}

[data-testid="stSidebar"] * {
    color: #5e35b1 !important;
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #5e35b1 !important;
}

/* Incoming Ambulances Section - Vibrant Pink */
[data-testid="stSidebar"] div[data-testid="stVerticalBlock"]:has(> div:has(> p:has(> span:contains("Incoming")))) {
    background-color: #e1bee7 !important;
    padding: 12px !important;
    border-radius: 8px !important;
}

/* Patient Pre-Admission Section - Light Blue */
[data-testid="stSidebar"] div[data-testid="stVerticalBlock"]:has(> div:has(> p:has(> span:contains("Patient")))) {
    background: #e3f2fd !important;
    padding: 12px !important;
    border-radius: 8px !important;
}

/* Glass effect elements */
.glass {
    background: rgba(255,255,255,0.4);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.3);
}

/* Radio buttons and other elements */
div[role="radiogroup"] label { color: black !important; }
div[role="radiogroup"] p { color: black !important; }

/* Main content buttons - RED border */
.stButton > button {
    background-color: white !important;
    color: black !important;
    border: 2px solid red !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-weight: bold !important;
}
.stButton > button:hover { 
    background-color: #f5f5f5 !important; 
}

/* Sidebar buttons styling */
[data-testid="stSidebar"] .stButton > button {
    border: none !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    padding: 10px 16px !important;
}

/* Tabs styling - RED */
.stTabs [data-baseweb="tab"] {
    background: #ef4444;
    color: white;
    border-radius: 999px;
    padding: 10px 25px;
}
.stTabs [aria-selected="true"] {
    background: #dc2626 !important;
    color: white !important;
}

/* Map Full Width */
iframe { width: 100% !important; max-width: none !important; }
[data-testid="stIFrame"] { width: 100% !important; }

/* Additional sidebar background fixes */
section[data-testid="stSidebar"] {
    background-color: white !important;
}

.sidebar {
    background: white !important;
}

.sidebar-content {
    background: white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR DASHBOARD =================
st.sidebar.markdown("### 📊 Dashboard")
st.sidebar.markdown("**Hospital Emergency System**")
st.sidebar.divider()

# Control Panel
st.sidebar.markdown("#### 🎮 Control Panel")
col_alert, col_clear = st.sidebar.columns([1, 1])
with col_alert:
    if st.sidebar.button("🚨 New Alert", use_container_width=True):
        st.session_state.alerts = [
            {
                "patient": random.choice(["Ramesh", "Sita", "Arjun", "Meena", "Vikram"]),
                "blood": random.choice(["A+", "B+", "O+", "AB+", "O-"]),
                "emergency": random.choice(list(ROUTES.keys())),
                "ambulance": f"AMB-{random.randint(100,999)}",
                "eta": random.randint(3, 10)
            }
        ] + st.session_state.get("alerts", [])[:4]
        st.sidebar.success("Alert Added!")

with col_clear:
    if st.sidebar.button("🗑 Clear All", use_container_width=True):
        st.session_state.alerts = []
        st.sidebar.info("Alerts cleared!")

st.sidebar.divider()

# Incoming Ambulances
st.sidebar.markdown("#### 🚑 Incoming Ambulances")
if "alerts" not in st.session_state:
    st.session_state.alerts = []

if not st.session_state.alerts:
    st.sidebar.info("No incoming ambulances")
else:
    for i, alert in enumerate(st.session_state.alerts[:3]):
        with st.sidebar.container():
            st.markdown(f"""
            <div style="background: #f3e5f5; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #ba68c8;">
                <b>🚑 {alert.get('ambulance', 'N/A')}</b><br>
                <small>👤 {alert.get('patient', 'N/A')}</small><br>
                <small>⏱️ ETA: {alert.get('eta', 'N/A')} min</small><br>
                <small>🏥 {alert.get('emergency', 'N/A')}</small><br>
                <small>🩸 {alert.get('blood', 'N/A')}</small>
            </div>
            """, unsafe_allow_html=True)

st.sidebar.divider()

# Patient Pre-Admission
st.sidebar.markdown("#### 👤 Patient Pre-Admission")
if st.session_state.alerts:
    latest_alert = st.session_state.alerts[0]
    st.sidebar.markdown(f"""
    <div style="background: #e3f2fd; padding: 12px; border-radius: 8px; border-left: 4px solid #1976d2;">
        <b>{latest_alert.get('patient', 'N/A')}</b><br>
        <small>🩸 Blood: {latest_alert.get('blood', 'N/A')}</small><br>
        <small>🚨 Type: {latest_alert.get('emergency', 'N/A')}</small><br>
        <small>⏱️ ETA: {latest_alert.get('eta', 'N/A')} min</small>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.info("No active patient")

st.sidebar.divider()

# ================= MAIN CONTENT =================

st.markdown("<h1 style='text-align:center;'>🚑 ONE-TAP EMERGENCY & LIVE AMBULANCE TRACKING</h1>", unsafe_allow_html=True)
st.divider()

# ---------------- TABS ----------------
t1, t2, t3, t4 = st.tabs([
    "🆘 Emergency",
    "🚑 Ambulance",
    "🗺 Live Route",
    "🏥 Patient & Hospital"
])

# ================= EMERGENCY =================
with t1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🆘 Trigger Emergency")

    emergency_type = st.radio("Select Emergency Type", list(ROUTES.keys()), horizontal=True)

    if st.button("🚨 ONE-TAP EMERGENCY", use_container_width=True):
        st.session_state.started = True
        st.session_state.route_index = 0
        st.session_state.animation_frame = 0
        st.session_state.auto_play = True
        st.session_state.emergency = emergency_type
        st.success("Emergency Activated 🚨 Ambulance Dispatched")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= AMBULANCE =================
with t2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🚑 Ambulance Dispatch Status")

    if st.session_state.started:
        st.success("Nearest Ambulance Assigned")
        st.markdown(f"### 🚑 Ambulance ID: AMB-{random.randint(100,999)}")
        st.progress(70)
    else:
        st.info("No active emergency")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= LIVE ROUTE =================
def interpolate_route(start, end, steps=25):
    lat_diff = end[0] - start[0]
    lon_diff = end[1] - start[1]
    return [[start[0] + lat_diff * i / steps, start[1] + lon_diff * i / steps] for i in range(steps + 1)]

full_route = interpolate_route(LOCATIONS["Home"], LOCATIONS["Patient"], steps=20) + interpolate_route(LOCATIONS["Patient"], LOCATIONS["Hospital"], steps=25)[1:]

with t3:
    if st.session_state.started:
        frame = min(max(st.session_state.animation_frame,0), len(full_route)-1)
        current_pos = full_route[frame]
        journey_pct = int((frame / (len(full_route) - 1)) * 100)
        stage = "En route to patient" if frame < 20 else "Heading to hospital"
        next_stop = "Patient" if frame < 20 else "Hospital"

        col1, col2 = st.columns([2,1])
        with col1:
            st.markdown(f"**Stage:** {stage}")
            st.markdown(f"**Next stop:** {next_stop}")
        with col2:
            st.metric("Progress", f"{journey_pct}%")

        st.progress(journey_pct / 100)
        st.markdown("---")

        # Control buttons
        c1, c2 = st.columns([1,1])
        with c1:
            if frame == len(full_route) - 1:
                play_label = "🔁 Replay"
            else:
                play_label = "⏸ Pause" if st.session_state.auto_play else "▶ Play"

            if st.button(play_label, use_container_width=True):
                if frame == len(full_route) - 1:
                    st.session_state.animation_frame = 0
                    st.session_state.auto_play = True
                else:
                    st.session_state.auto_play = not st.session_state.auto_play
        with c2:
            frame = st.slider("Position", 0, len(full_route)-1, frame, key="ambulance_slider")
            st.session_state.animation_frame = frame
            if frame < len(full_route)-1:
                st.session_state.auto_play = False

        # Build map
        m = folium.Map(location=current_pos, zoom_start=15, tiles='CartoDB dark_matter', attr='CartoDB')
        folium.PolyLine(full_route[frame:], color="#9CA3AF", weight=4, opacity=0.45, dash_array="8,6").add_to(m)
        if frame>0:
            folium.PolyLine(full_route[:frame+1], color="#F87171", weight=6, opacity=0.95).add_to(m)
        folium.Marker(LOCATIONS["Home"], popup="🏠 Ambulance Base", icon=folium.Icon(color="blue", icon="building", prefix="fa")).add_to(m)
        folium.Marker(LOCATIONS["Patient"], popup="🏥 Patient Location", icon=folium.Icon(color="red", icon="heart", prefix="fa")).add_to(m)
        folium.Marker(LOCATIONS["Hospital"], popup="🏗️ Hospital", icon=folium.Icon(color="green", icon="hospital", prefix="fa")).add_to(m)
        folium.CircleMarker(location=current_pos, radius=18, popup=f"🚑 Ambulance {journey_pct}% Complete", color="#F97316", fill=True, fillColor="#FB923C", fillOpacity=0.95, weight=3).add_to(m)
        folium.Marker(current_pos, popup=f"🚑 Ambulance {journey_pct}% Complete", icon=folium.Icon(color="orange", icon="ambulance", prefix="fa", icon_color="white")).add_to(m)
        st_folium(m, width=1080, height=620, key="ambulance_tracker_interactive")

        if st.session_state.auto_play and frame < len(full_route)-1:
            time.sleep(0.12)
            st.session_state.animation_frame += 1
            st.experimental_rerun()
    else:
        st.info("🔔 Activate emergency to start tracking")

# ================= PATIENT INFO + FULL VOICE =================
with t4:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("🏥 Hospital Pre-Admission Form")

    if st.session_state.started:
        with st.form("details"):
            name = st.text_input("Patient Name")
            phone = st.text_input("Phone Number")
            address = st.text_area("Address")
            blood = st.selectbox("Blood Group", ["A+","A-","B+","B-","O+","O-","AB+","AB-","Unknown"])
            submit = st.form_submit_button("📤 Send to Hospital")

        if submit:
            st.success("Patient details sent to hospital ✅")
            st.success(f"🏥 Assigned Hospital: {ROUTES[st.session_state.emergency][-1]}")
    else:
        st.info("Waiting for emergency activation")

    st.markdown("</div>", unsafe_allow_html=True)

    # ================= ADVANCED VOICE ASSISTANT =================
    st.divider()
    st.subheader("🎤 Smart Voice Assistant (AI Powered)")
    st.write("*Select language, click Start, and speak when AI asks questions*")

    # Language Selection
    language = st.selectbox(
        "🌐 Select Language:",
        ["English", "Telugu", "Hindi"],
        key="voice_lang"
    )

    lang_code_map = {
        "English": "en-US",
        "Telugu": "te-IN",
        "Hindi": "hi-IN"
    }

    questions_dict = {
        "English": [
            "What is the patient name?",
            "What is the phone number?",
            "What is the address?",
            "What is the blood group?"
        ],
        "Telugu": [
            "రోగి పేరు ఏమిటి?",
            "ఫోన్ నంబర్ ఏమిటి?",
            "చిరునామా ఏమిటి?",
            "రక్త గ్రూప్ ఏమిటి?"
        ],
        "Hindi": [
            "मरीज़ का नाम क्या है?",
            "फोन नंबर क्या है?",
            "पता क्या है?",
            "ब्लड ग्रुप क्या है?"
        ]
    }

    keys_list = ["name", "phone", "address", "blood_group"]

    confirm_text = {
        "English": "Please confirm. Say YES if correct, NO if wrong.",
        "Telugu": "సరైనదైతే YES అనండి, తప్పైతే NO అనండి.",
        "Hindi": "सही है तो YES बोलिए, गलत है तो NO बोलिए।"
    }

    if st.button("🎯 Start Voice Chat", use_container_width=True):
        import streamlit.components.v1 as components
        import json
        
        lang_code_str = lang_code_map[language]
        questions_json = json.dumps(questions_dict[language])
        keys_json = json.dumps(keys_list)
        confirm_str = confirm_text[language]
        
        components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; }}
    #chat {{
        max-width: 100%;
        display: flex;
        flex-direction: column;
        gap: 10px;
        height: 400px;
        overflow-y: auto;
        padding: 15px;
        background: #fafafa;
        border-radius: 12px;
        border: 1px solid #ddd;
    }}
    
    .msg {{
        padding: 12px 15px;
        border-radius: 12px;
        max-width: 80%;
        word-wrap: break-word;
        animation: slideIn 0.3s ease-out;
    }}
    
    .ai-msg {{
        background: #e3f2fd;
        color: #1976d2;
        align-self: flex-start;
        border-left: 4px solid #1976d2;
    }}
    
    .user-msg {{
        background: #4caf50;
        color: white;
        align-self: flex-end;
        border-right: 4px solid #388e3c;
    }}
    
    .status {{
        font-size: 12px;
        color: #666;
        padding: 8px;
        text-align: center;
        font-style: italic;
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    #listening {{
        color: #f44336;
        font-weight: bold;
        animation: blink 0.8s infinite;
    }}
    
    @keyframes blink {{
        0%, 50%, 100% {{ opacity: 1; }}
        25%, 75% {{ opacity: 0.5; }}
    }}
</style>
</head>
<body>

<div id="chat"></div>
<div id="status" class="status">Ready to listen...</div>

<script>
const questions = {questions_json};
const keys = {keys_json};
const confirmText = "{confirm_str}";
let step = 0;
let data = {{}};
let lastTranscript = "";
let isSpeaking = false;
let isListening = false;
let processingTranscript = false;
let listeningTimeout = null;
let confirmationRetries = 0;
let isConversationComplete = false;
const MAX_RETRIES = 3;

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = "{lang_code_str}";
recognition.interimResults = true;
recognition.continuous = false;
recognition.maxAlternatives = 1;

const chat = document.getElementById('chat');
const statusDiv = document.getElementById('status');

function addMessage(content, type) {{
    const msgDiv = document.createElement('div');
    msgDiv.className = 'msg ' + (type === 'user' ? 'user-msg' : 'ai-msg');
    msgDiv.textContent = content;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}}

function updateStatus(text) {{
    statusDiv.innerHTML = text;
}}

function speak(text) {{
    return new Promise(resolve => {{
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = "{lang_code_str}";
        msg.rate = 0.95;
        msg.onend = () => {{
            resolve();
            if(!isConversationComplete) setTimeout(() => startListening(), 400);
        }};
        msg.onerror = () => {{
            resolve();
            if(!isConversationComplete) setTimeout(() => startListening(), 400);
        }};
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    }});
}}

async function askQuestion() {{
    if(step < questions.length) {{
        addMessage(questions[step], 'ai');
        updateStatus('🤖 AI Speaking...');
        await speak(questions[step]);
    }} else {{
        addMessage(confirmText, 'ai');
        updateStatus('🤖 AI Speaking...');
        await speak(confirmText);
    }}
}}

function startListening() {{
    if(isListening || isConversationComplete) return;
    try {{
        isListening = true;
        updateStatus('<span id="listening">🎙️ Listening...</span>');
        recognition.start();
    }} catch(e) {{
        isListening = false;
    }}
}}

function stopListening() {{
    try {{
        recognition.stop();
        isListening = false;
    }} catch(e) {{}}
}}

recognition.onstart = () => {{
    isListening = true;
    updateStatus('<span id="listening">🎙️ Listening...</span>');
}};

recognition.onresult = function(event) {{
    if(isConversationComplete) return;
    let finalTranscript = '';
    for(let i = event.resultIndex; i < event.results.length; i++) {{
        if(event.results[i].isFinal) {{
            finalTranscript += event.results[i][0].transcript;
        }}
    }}
    if(finalTranscript && finalTranscript !== lastTranscript) {{
        lastTranscript = finalTranscript;
        addMessage('👂 ' + finalTranscript, 'user');
        stopListening();
        processingTranscript = true;
        setTimeout(() => processTranscript(finalTranscript), 200);
    }}
}};

function processTranscript(finalText) {{
    finalText = finalText.toLowerCase().trim();
    if(isConversationComplete) {{
        processingTranscript = false;
        return;
    }}
    
    if(step < keys.length) {{
        data[keys[step]] = finalText;
        step++;
        updateStatus('✓ Recorded. Waiting for next...');
        setTimeout(() => {{
            lastTranscript = "";
            askQuestion();
        }}, 1200);
    }} else {{
        stopListening();
        if(finalText.includes('yes') || finalText.includes('yep') || finalText.includes('sure')) {{
            isConversationComplete = true;
            processingTranscript = false;
            addMessage('✅ Details filled successfully!', 'ai');
            updateStatus('✓ Completed');
            (async () => {{
                await speak('Details saved successfully');
            }})();
        }} else if(finalText.includes('no') || finalText.includes('wrong') || finalText.includes('nope')) {{
            addMessage('🔄 Asking again...', 'ai');
            step = 0;
            data = {{}};
            confirmationRetries = 0;
            setTimeout(() => {{
                processingTranscript = false;
                askQuestion();
            }}, 900);
        }} else {{
            confirmationRetries++;
            if(confirmationRetries >= MAX_RETRIES) {{
                isConversationComplete = true;
                addMessage('✅ Completed!', 'ai');
                updateStatus('✓ Done');
                processingTranscript = false;
                return;
            }}
            addMessage('❓ Please say YES or NO', 'ai');
            processingTranscript = false;
            setTimeout(() => {{
                lastTranscript = "";
                startListening();
            }}, 800);
        }}
    }}
}}

recognition.onerror = function(event) {{
    isListening = false;
    if(!isConversationComplete && !processingTranscript) {{
        setTimeout(() => {{
            lastTranscript = "";
            startListening();
        }}, 1200);
    }}
}};

addMessage('👋 Hello! I am your Smart Voice Assistant', 'ai');
setTimeout(() => askQuestion(), 500);
</script>

</body>
</html>
""", height=500)