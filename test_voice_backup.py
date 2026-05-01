import streamlit as st
import streamlit.components.v1 as components
import time
import random
import folium
from streamlit_folium import st_folium
import json

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="QuickDoc Emergency Tracker",
    page_icon="🚑",
    layout="wide"
)

# ============ SESSION STATE ============
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

# ============ ROUTES ============
ROUTES = {
    "Accident / Trauma": ["Lingampally", "Chandanagar", "Miyapur", "Kukatpally", "City Trauma Hospital"],
    "Cardiac Emergency": ["Lingampally", "BHEL", "KPHB", "Heart Care Hospital"],
    "Maternity": ["Lingampally", "Chandanagar", "Maternity Care Hospital"]
}

# ============ LOCATIONS ============
LOCATIONS = {
    "Home": [17.4448, 78.3719],
    "Patient": [17.4495, 78.3751],
    "Hospital": [17.4200, 78.4500]
}

# ============ SIDEBAR - HOSPITAL DASHBOARD (from form.py) ============
with st.sidebar:
    st.markdown("""
<div style="text-align:center; margin-bottom: 0.8rem;">
    <h2 style="margin:0; font-size:1.8rem; color:#111111;">🏥 Dashboard</h2>
    <p style="margin:0.5rem 0 0; color:#4b5563; font-size:0.9rem;">Hospital Emergency System</p>
</div>
""", unsafe_allow_html=True)
    st.divider()

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

    # Control Panel
    st.markdown("### 🎛️ Control Panel")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 New Alert", use_container_width=True):
            st.session_state.alerts.insert(0, generate_emergency())
            st.rerun()
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.alerts = []
            st.rerun()

    st.divider()

    # Incoming Ambulances
    st.markdown("### 🚑 Incoming Ambulances")
    if not st.session_state.alerts:
        st.info("No incoming emergencies")
    else:
        for alert in st.session_state.alerts:
            st.markdown(f"""
            <div style="background: #f8d5ff; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                <b>🚨 {alert['emergency']}</b><br>
                <small>👤 {alert['patient']}</small><br>
                <small>🚑 {alert['ambulance']}</small><br>
                <small>⏳ ETA: {alert['eta']} min | 🩸 {alert['blood']}</small>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Pre-Admission Form
    st.markdown("### 📋 Patient Pre-Admission")
    if st.session_state.alerts:
        p = st.session_state.alerts[0]
        st.markdown(f"""
        <div style="background: rgba(200,230,255,0.5); padding: 12px; border-radius: 8px;">
            <b>👤 {p['patient']}</b><br>
            <small>🚨 {p['emergency']}</small><br>
            <small>🩸 {p['blood']}</small><br>
            <small>🚑 {p['ambulance']} (ETA {p['eta']} min)</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Waiting for ambulance")

# ============ CSS STYLING ============
st.markdown("""
<style>
.stApp { background: white; color: black; }

.glass {
    background: rgba(255,255,255,0.4);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.3);
}

div[role="radiogroup"] label { color: black !important; }
div[role="radiogroup"] p { color: black !important; }

.stButton > button {
    background-color: white !important;
    color: black !important;
    border: 2px solid red !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-weight: bold !important;
}
.stButton > button:hover { background-color: #f5f5f5 !important; }

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

iframe { width: 100% !important; max-width: none !important; }
[data-testid="stIFrame"] { width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("<h1 style='text-align:center;'>🚑 ONE-TAP EMERGENCY & LIVE AMBULANCE TRACKING</h1>", unsafe_allow_html=True)
st.divider()

# ============ TABS ============
t1, t2, t3, t4 = st.tabs([
    "🆘 Emergency",
    "🚑 Ambulance",
    "🗺 Live Route",
    "🏥 Patient & Hospital"
])

# ============ TAB 1: EMERGENCY ============
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

# ============ TAB 2: AMBULANCE ============
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

# ============ TAB 3: LIVE ROUTE ============
def interpolate_route(start, end, steps=25):
    lat_diff = end[0] - start[0]
    lon_diff = end[1] - start[1]
    return [[start[0] + lat_diff * i / steps, start[1] + lon_diff * i / steps] for i in range(steps + 1)]

full_route = interpolate_route(LOCATIONS["Home"], LOCATIONS["Patient"], steps=20) + interpolate_route(LOCATIONS["Patient"], LOCATIONS["Hospital"], steps=25)[1:]

with t3:
    if st.session_state.started:
        st.markdown("<div style='display:flex; align-items:center; justify-content:space-between; gap:20px;'><div><h3 style='margin:0;'>🗺 Live Ambulance Tracking</h3></div></div>", unsafe_allow_html=True)
        
        frame = st.session_state.animation_frame
        if frame < 0:
            frame = 0
        elif frame >= len(full_route):
            frame = len(full_route) - 1

        current_pos = full_route[frame]
        journey_pct = int((frame / (len(full_route) - 1)) * 100)
        stage = "En route to patient" if frame < 20 else "Heading to hospital"
        next_stop = "Patient" if frame < 20 else "Hospital"

        summary_col1, summary_col2, summary_col3 = st.columns([2, 1, 1])
        with summary_col1:
            st.markdown(f"**Stage:** {stage}  ")
            st.markdown(f"**Next stop:** {next_stop}  ")
        with summary_col2:
            st.metric("Progress", f"{journey_pct}%")
        with summary_col3:
            st.metric("Status", "In Transit" if journey_pct < 100 else "Arrived")

        st.progress(journey_pct / 100)
        st.markdown("---")

        control_col1, control_col2 = st.columns([1,1])
        with control_col1:
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
        with control_col2:
            frame = st.slider("Position", 0, len(full_route)-1, frame, key="ambulance_slider")
            st.session_state.animation_frame = frame
            if frame < len(full_route) - 1:
                st.session_state.auto_play = False

        # Build map
        m = folium.Map(
            location=current_pos,
            zoom_start=15,
            tiles='CartoDB dark_matter',
            attr='CartoDB'
        )

        # Future route (dashed grey)
        folium.PolyLine(
            full_route[frame:],
            color="#9CA3AF",
            weight=4,
            opacity=0.45,
            dash_array="8,6"
        ).add_to(m)

        # Traveled route (moving red)
        if frame > 0:
            folium.PolyLine(
                full_route[:frame+1],
                color="#F87171",
                weight=6,
                opacity=0.95
            ).add_to(m)

        folium.Marker(
            LOCATIONS["Home"],
            popup="<b>🏠 Ambulance Base</b>",
            tooltip="Ambulance Base",
            icon=folium.Icon(color="blue", icon="building", prefix="fa")
        ).add_to(m)

        folium.Marker(
            LOCATIONS["Patient"],
            popup="<b>🏥 Patient Location</b>",
            tooltip="Patient Location",
            icon=folium.Icon(color="red", icon="heart", prefix="fa")
        ).add_to(m)

        folium.Marker(
            LOCATIONS["Hospital"],
            popup="<b>🏗️ Hospital</b>",
            tooltip="Hospital",
            icon=folium.Icon(color="green", icon="hospital", prefix="fa")
        ).add_to(m)

        folium.CircleMarker(
            location=current_pos,
            radius=18,
            popup=f"<b>🚑 Ambulance</b><br>{journey_pct}% Complete",
            tooltip="Ambulance",
            color="#F97316",
            fill=True,
            fillColor="#FB923C",
            fillOpacity=0.95,
            weight=3
        ).add_to(m)

        folium.Marker(
            current_pos,
            popup=f"<b>🚑 Ambulance</b><br>{journey_pct}% Complete",
            icon=folium.Icon(color="orange", icon="ambulance", prefix="fa", icon_color="white")
        ).add_to(m)

        st_folium(m, width=1080, height=620, key="ambulance_tracker_interactive")

        if st.session_state.auto_play and frame < len(full_route) - 1:
            time.sleep(0.12)
            st.session_state.animation_frame += 1
            st.rerun()
    else:
        st.info("🔔 Activate emergency to start tracking")

# ============ TAB 4: PATIENT & HOSPITAL + VOICE ASSISTANT ============
with t4:
    st.markdown("""
    <style>
    div[data-testid="stForm"] {
        background-color: white !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid #ddd !important;
    }

    div[data-testid="stForm"] input,
    div[data-testid="stForm"] textarea {
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] {
        background-color: white !important;
        color: black !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] * {
        background-color: white !important;
        color: black !important;
    }

    div[data-testid="stForm"] label {
        color: black !important;
        font-weight: 500;
    }

    div[data-testid="stForm"] button {
        background-color: white !important;
        color: black !important;
        border: 2px solid #ccc !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }

    div[data-testid="stForm"] button:hover {
        background-color: #f5f5f5 !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

    # ============ VOICE ASSISTANT FROM UI.PY ============
    st.divider()
    st.subheader("🎤 Smart Ambulance Voice Assistant")

    # Language Selection
    language = st.selectbox(
        "Select Language",
        ["English", "Telugu", "Hindi"]
    )

    lang_code = {
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

    keys = ["name", "phone", "address", "blood_group"]

    confirm_text = {
        "English": "Please confirm. Say YES if correct, NO if wrong.",
        "Telugu": "సరైనదైతే YES అనండి, తప్పైతే NO అనండి.",
        "Hindi": "सही है तो YES बोलिए, गलत है तो NO बोलिए।"
    }

    if st.button("🎯 Start Voice Chat"):
        components.html(f"""
<!DOCTYPE html>
<html>
<body>

<div id="chat" style="max-width:420px;margin:auto;font-family:Arial;"></div>

<script>
const questions = {json.dumps(questions_dict[language])};
const keys = {json.dumps(keys)};
const confirmText = "{confirm_text[language]}";
let step = 0;
let data = {{}};
let currentUsrMsgDiv = null;

// Always-on speech recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = "{lang_code[language]}";
recognition.interimResults = true;
recognition.continuous = true;

// Add chat message
function addMessage(content, type) {{
    const chat = document.getElementById('chat');
    const msgDiv = document.createElement('div');
    msgDiv.style.padding = '10px';
    msgDiv.style.margin = '10px 0';
    msgDiv.style.borderRadius = '20px';
    msgDiv.style.maxWidth = '75%';
    msgDiv.style.wordWrap = 'break-word';
    if (type === 'user') {{
        msgDiv.style.background = '#4CAF50';
        msgDiv.style.color = 'white';
        msgDiv.style.marginLeft = 'auto';
    }} else {{
        msgDiv.style.background = '#f1f1f1';
        msgDiv.style.color = 'black';
        msgDiv.style.marginRight = 'auto';
    }}
    msgDiv.innerText = content;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
    return msgDiv;
}}

// Speak helper
function speak(text) {{
    return new Promise(resolve => {{
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = "{lang_code[language]}";
        msg.rate = 0.9;
        msg.onend = resolve;
        window.speechSynthesis.speak(msg);
    }});
}}

// Ask next question
async function askQuestion() {{
    if(step < questions.length) {{
        addMessage(questions[step], 'ai');
        await speak(questions[step]);
    }} else {{
        addMessage(confirmText, 'ai');
        await speak(confirmText);
    }}
}}

// Handle recognition results instantly
recognition.onresult = function(event) {{
    let interimTranscript = '';
    for(let i = event.resultIndex; i < event.results.length; i++) {{
        const transcript = event.results[i][0].transcript;
        if(event.results[i].isFinal) {{
            addFinalTranscript(transcript);
        }} else {{
            interimTranscript += transcript;
            if(!currentUsrMsgDiv) {{
                currentUsrMsgDiv = addMessage(interimTranscript,'user');
            }} else {{
                currentUsrMsgDiv.innerText = interimTranscript;
            }}
        }}
    }}
}};

// Final transcript processing
function addFinalTranscript(finalText) {{
    if(currentUsrMsgDiv) {{
        currentUsrMsgDiv.innerText = finalText;
        currentUsrMsgDiv = null;
    }} else {{
        addMessage(finalText, 'user');
    }}

    if(step < keys.length) {{
        data[keys[step]] = finalText;
        step++;
        askQuestion(); // Ask next immediately
    }} else {{
        if(finalText.toLowerCase().includes('yes')) {{
            addMessage("🚑 Details have been sent to Hospital", 'ai');
            fetch("/hospital", {{
                method:"POST",
                headers:{{"Content-Type":"application/json"}},
                body: JSON.stringify(data)
            }});
        }} else {{
            step = 0;
            data = {{}};
            askQuestion(); // Restart if NO
        }}
    }}
}}

// Handle errors
recognition.onerror = function() {{
    addMessage("⚠️ Could not hear clearly, please speak again.", 'ai');
}}

// Start everything
recognition.start();
askQuestion();
</script>

</body>
</html>
""", height=700)
