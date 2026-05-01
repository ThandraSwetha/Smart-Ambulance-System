# import streamlit as st
# import streamlit.components.v1 as components
# import json

# st.set_page_config(page_title="Smart Ambulance Voice Bot", layout="centered")

# st.title("🚑 Smart Ambulance Voice Assistant")
# st.write("Select your language, then click mic and speak after AI asks.")

# # -------- LANGUAGE SELECTION --------
# language = st.selectbox(
#     "Select Language",
#     ["English", "Telugu", "Hindi"]
# )

# lang_code = {
#     "English": "en-US",
#     "Telugu": "te-IN",
#     "Hindi": "hi-IN"
# }

# questions_dict = {
#     "English": [
#         "What is the patient name?",
#         "What is the phone number?",
#         "What is the address?",
#         "What is the blood group?"
#     ],
#     "Telugu": [
#         "రోగి పేరు ఏమిటి?",
#         "ఫోన్ నంబర్ ఏమిటి?",
#         "చిరునామా ఏమిటి?",
#         "రక్త గ్రూప్ ఏమిటి?"
#     ],
#     "Hindi": [
#         "मरीज़ का नाम क्या है?",
#         "फोन नंबर क्या है?",
#         "पता क्या है?",
#         "ब्लड ग्रुप क्या है?"
#     ]
# }

# keys = ["name", "phone", "address", "blood_group"]

# confirm_text = {
#     "English": "Please confirm. Say YES if correct, NO if wrong.",
#     "Telugu": "సరైనదైతే YES అనండి, తప్పైతే NO అనండి.",
#     "Hindi": "सही है तो YES बोलिए, गलत है तो NO बोलिए।"
# }

# if st.button("🎤 Start Voice Chat"):
#     components.html(f"""
# <!DOCTYPE html>
# <html>
# <body>

# <div id="chat" style="max-width:420px;margin:auto;font-family:Arial;"></div>

# <script>
# const questions = {json.dumps(questions_dict[language])};
# const keys = {json.dumps(keys)};
# const confirmText = "{confirm_text[language]}";
# let step = 0;
# let data = {{}};
# let currentUsrMsgDiv = null;

# // Always-on speech recognition
# const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
# const recognition = new SpeechRecognition();
# recognition.lang = "{lang_code[language]}";
# recognition.interimResults = true;
# recognition.continuous = true;

# // Add chat message
# function addMessage(content, type) {{
#     const chat = document.getElementById('chat');
#     const msgDiv = document.createElement('div');
#     msgDiv.style.padding = '10px';
#     msgDiv.style.margin = '10px 0';
#     msgDiv.style.borderRadius = '20px';
#     msgDiv.style.maxWidth = '75%';
#     msgDiv.style.wordWrap = 'break-word';
#     if (type === 'user') {{
#         msgDiv.style.background = '#4CAF50';
#         msgDiv.style.color = 'white';
#         msgDiv.style.marginLeft = 'auto';
#     }} else {{
#         msgDiv.style.background = '#f1f1f1';
#         msgDiv.style.color = 'black';
#         msgDiv.style.marginRight = 'auto';
#     }}
#     msgDiv.innerText = content;
#     chat.appendChild(msgDiv);
#     chat.scrollTop = chat.scrollHeight;
#     return msgDiv;
# }}

# // Speak helper
# function speak(text) {{
#     return new Promise(resolve => {{
#         const msg = new SpeechSynthesisUtterance(text);
#         msg.lang = "{lang_code[language]}";
#         msg.rate = 0.9;
#         msg.onend = resolve;
#         window.speechSynthesis.speak(msg);
#     }});
# }}

# // Ask next question
# async function askQuestion() {{
#     if(step < questions.length) {{
#         addMessage(questions[step], 'ai');
#         await speak(questions[step]);
#     }} else {{
#         addMessage(confirmText, 'ai');
#         await speak(confirmText);
#     }}
# }}

# // Handle recognition results instantly
# recognition.onresult = function(event) {{
#     let interimTranscript = '';
#     for(let i = event.resultIndex; i < event.results.length; i++) {{
#         const transcript = event.results[i][0].transcript;
#         if(event.results[i].isFinal) {{
#             addFinalTranscript(transcript);
#         }} else {{
#             interimTranscript += transcript;
#             if(!currentUsrMsgDiv) {{
#                 currentUsrMsgDiv = addMessage(interimTranscript,'user');
#             }} else {{
#                 currentUsrMsgDiv.innerText = interimTranscript;
#             }}
#         }}
#     }}
# }};

# // Final transcript processing
# function addFinalTranscript(finalText) {{
#     if(currentUsrMsgDiv) {{
#         currentUsrMsgDiv.innerText = finalText;
#         currentUsrMsgDiv = null;
#     }} else {{
#         addMessage(finalText, 'user');
#     }}

#     if(step < keys.length) {{
#         data[keys[step]] = finalText;
#         step++;
#         askQuestion(); // Ask next immediately
#     }} else {{
#         if(finalText.toLowerCase().includes('yes')) {{
#             addMessage("🚑 Details have been sent to Hospital", 'ai');
#             fetch("/hospital", {{
#                 method:"POST",
#                 headers:{{"Content-Type":"application/json"}},
#                 body: JSON.stringify(data)
#             }});
#         }} else {{
#             step = 0;
#             data = {{}};
#             askQuestion(); // Restart if NO
#         }}
#     }}
# }}

# // Handle errors
# recognition.onerror = function() {{
#     addMessage("⚠️ Could not hear clearly, please speak again.", 'ai');
# }}

# // Start everything
# recognition.start();
# askQuestion();
# </script>

# </body>
# </html>
# """, height=700)
import streamlit as st
import streamlit.components.v1 as components
import json
from auth import login, signup
from dashboards import user_dashboard, hospital_dashboard, admin_dashboard

st.set_page_config(page_title="Smart Ambulance Dispatch System", layout="wide")

# 🎨 FULL WHITE UI + BUTTON FIX
st.markdown("""
<style>
html, body, .stApp {
    background-color: white !important;
    color: black !important;
}

/* Card */
.main-box {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

/* 🔘 BUTTON WHITE */
.stButton > button {
    background-color: white !important;
    color: black !important;
    border: 2px solid #ccc !important;
    border-radius: 8px !important;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #f5f5f5 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🚑 Smart Ambulance Voice Assistant")

st.markdown("<div class='main-box'>", unsafe_allow_html=True)
st.write("Speak clearly after each question. The system will wait for your response.")

# -------- LANGUAGE --------
language = st.selectbox("Select Language", ["English", "Telugu", "Hindi"])

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

success_msg = {
    "English": "✅ Patient details successfully sent to hospital.",
    "Telugu": "✅ రోగి వివరాలు ఆసుపత్రికి విజయవంతంగా పంపించబడ్డాయి.",
    "Hindi": "✅ मरीज़ की जानकारी अस्पताल को सफलतापूर्वक भेज दी गई है।"
}

if st.button("🎤 Start Voice Assistant"):
    components.html(f"""
<!DOCTYPE html>
<html>
<body style="background:white;font-family:Arial;">

<div id="chat" style="max-width:450px;margin:auto;"></div>

<script>
const questions = {json.dumps(questions_dict[language])};
const keys = {json.dumps(keys)};
const successMsg = "{success_msg[language]}";

let step = 0;
let data = {{}};
let retryCount = 0;
const MAX_RETRY = 2;

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

// 🔢 UPDATED NUMBER HANDLING
function convertWordsToNumbers(text) {{
    const map = {{
        "zero":"0","one":"1","two":"2","three":"3","four":"4",
        "five":"5","six":"6","seven":"7","eight":"8","nine":"9"
    }};

    // If already numbers → clean and return
    if (/^\\d+$/.test(text.replace(/\\s/g, ""))) {{
        return text.replace(/\\D/g, "");
    }}

    // Convert words → digits
    return text.toLowerCase().split(" ")
        .map(w => map[w] !== undefined ? map[w] : "")
        .join("");
}}

// 💬 Chat UI
function addMessage(content, type) {{
    const chat = document.getElementById('chat');
    const msg = document.createElement('div');

    msg.style.padding = "10px";
    msg.style.margin = "10px 0";
    msg.style.borderRadius = "15px";
    msg.style.maxWidth = "75%";

    if(type === "user") {{
        msg.style.background = "#4CAF50";
        msg.style.color = "white";
        msg.style.marginLeft = "auto";
    }} else {{
        msg.style.background = "#f1f1f1";
        msg.style.color = "black";
    }}

    msg.innerText = content;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}}

// 🔊 Speak
function speak(text) {{
    return new Promise(resolve => {{
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = "{lang_code[language]}";
        utter.rate = 0.85;
        utter.onend = resolve;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utter);
    }});
}}

// 🎯 Ask Question
async function askQuestion() {{
    let question = questions[step];
    addMessage(question, "ai");
    await speak(question);
    setTimeout(() => listen(), 600);
}}

// 🎤 Listen
function listen() {{
    const recognition = new SpeechRecognition();
    recognition.lang = "{lang_code[language]}";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.start();

    recognition.onresult = function(event) {{
        retryCount = 0;
        let text = event.results[0][0].transcript.trim();
        handleAnswer(text);
    }};

    recognition.onerror = function() {{
        retryCount++;
        if(retryCount <= MAX_RETRY) {{
            addMessage("⚠️ Please repeat.", "ai");
            setTimeout(() => listen(), 1000);
        }} else {{
            addMessage("❌ Too many failed attempts.", "ai");
        }}
    }};
}}

// 🧠 VALIDATION (TEST FRIENDLY)
function validateInput(key, value) {{
    if(key === "phone") {{
        let cleaned = convertWordsToNumbers(value);
        return cleaned.length >= 3 && cleaned.length <= 10;
    }}
    if(key === "blood_group") {{
        return /(A|B|AB|O)[+-]/i.test(value);
    }}
    return value.length > 0;
}}

// 🧠 Handle Answer
function handleAnswer(answer) {{
    addMessage(answer, "user");

    let key = keys[step];

    if(!validateInput(key, answer)) {{
        addMessage("⚠️ Invalid input. Try again.", "ai");
        setTimeout(() => listen(), 800);
        return;
    }}

    if(key === "phone") {{
        data[key] = convertWordsToNumbers(answer);
    }} else {{
        data[key] = answer;
    }}

    step++;

    if(step < questions.length) {{
        askQuestion();
    }} else {{
        finishProcess();
    }}
}}

// ✅ Finish
async function finishProcess() {{
    addMessage("🔄 Processing...", "ai");
    await speak("Processing your details");

    fetch("/hospital", {{
        method: "POST",
        headers: {{"Content-Type":"application/json"}},
        body: JSON.stringify(data)
    }});

    setTimeout(async () => {{
        addMessage(successMsg, "ai");
        await speak(successMsg);
        addMessage("🚑 Help is on the way!", "ai");
    }}, 1000);
}}

askQuestion();
</script>

</body>
</html>
""", height=700)

st.markdown("</div>", unsafe_allow_html=True)

# -------- SESSION STATE --------
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

# -------- MAIN APP LOGIC --------
if st.session_state.user is None:
    # Show login/signup
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        login()
    
    with col2:
        st.subheader("New User?")
        signup()
else:
    # User is logged in - show dashboard based on role
    st.divider()
    
    # Logout button
    if st.button("🔌 Logout"):
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()
    
    # Route to appropriate dashboard
    if st.session_state.role == "user":
        user_dashboard()
    elif st.session_state.role == "hospital":
        hospital_dashboard()
    elif st.session_state.role == "admin":
        admin_dashboard()