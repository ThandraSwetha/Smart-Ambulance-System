# 🚑 Smart Ambulance Dispatch System

**🔗 [Live Demo: smart-ambulance-system.streamlit.app](https://smart-ambulance-system-v6jqcu2cezf4nxvf5zkhc4.streamlit.app/)**

A real-time emergency response platform featuring an AI-powered voice assistant, live ambulance tracking, and a comprehensive hospital dashboard. Designed to streamline emergency triage and reduce response times.

## 🚀 Features

### 🎙️ AI Voice Assistant
- **Interactive Triage**: Automated emergency assessment using browser-native Speech Recognition and Synthesis.
- **Multi-Language Support**: Full support for **English**, **Telugu**, and **Hindi**.
- **Real-Time Feedback**: Professional pulse visualization and status updates during voice interaction.

### 🗺️ Live Ambulance Tracking
- **Interactive Maps**: Real-time visualization of ambulance movement from base to patient to hospital.
- **Dynamic Routing**: Smooth path interpolation using Folium and custom animation logic.
- **Live Metrics**: ETA and progress tracking for critical oversight.

### 🏥 Hospital Command Center
- **Pre-Admission Triage**: Instant transmission of patient vitals and emergency details from the field to the ER.
- **Emergency Queue**: Sidebar dashboard for managing multiple incoming ambulances and severity levels.
- **Status Updates**: Real-time alerts for new emergencies and hospital assignments.

---

## ✅ System Integration Details

### 1. **Sidebar Dashboard**
   - **Emergency Control Panel** - Quick action buttons
   - **Incoming Ambulances** - Real-time ambulance tracking display
   - **Live View** - Emergency status monitoring
   - **Patient Pre-Admission** - Quick form entry in sidebar
   - Interactive menu navigation with dynamic content

### 2. **Enhanced AI Voice Assistant (Tab 4)**
   - **Multi-Language Support**: English, Telugu, Hindi
   - **Smart Extraction**: Auto-fills form fields from voice recognition
   - **Text-to-Speech**: Confirm information with spoken feedback
   - **Interactive Voice Chat**: Full conversation mode (ready to use)

### 📋 Tab Descriptions

- **Tab 1: 🆘 Emergency**: Select type and activate with one tap.
- **Tab 2: 🚑 Ambulance**: View ID, distance, ETA, and progress.
- **Tab 3: 🗺 Live Route**: Animated Folium map with playback controls and position slider.
- **Tab 4: 🎤 Voice Assistant**: Multi-language AI voice triage with auto-fill form capabilities.

---

## 🔧 How to Use

### **Start Emergency:**
1. Click **🚨 Emergency** button in sidebar OR Tab 1.
2. Select emergency type.
3. Click **ONE-TAP EMERGENCY ACTIVATION**.

### **Use Voice Assistant:**
1. Go to **Tab 4: 🎤 Voice Assistant**.
2. Select language.
3. Click **🚀 START INTERACTIVE SESSION**.
4. Speak your answer clearly after the AI finishes speaking.
5. Form auto-fills with recognized data.

### **Track Live Route:**
1. Activate emergency first.
2. Go to **Tab 3: 🗺 Live Route**.
3. Use **Play/Pause** or **Position Slider** to control animation.

---

## 🛠️ Tech Stack
- **Frontend/Backend**: [Streamlit](https://streamlit.io/)
- **Mapping**: [Folium](https://python-visualization.github.io/folium/) & [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium)
- **Voice Engine**: Browser Web Speech API (SpeechRecognition & SpeechSynthesis)
- **Styling**: Custom CSS and HTML Components for a premium glassmorphism UI.

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ThandraSwetha/Smart-Ambulance-System.git
   cd Smart-Ambulance-System
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run test.py
   ```

## 🌐 Deployment

The project is configured for deployment on:
- **Streamlit Community Cloud**: [Recommended] Connect your GitHub repository for instant hosting.
- **Vercel**: Configuration included in `vercel.json`.

## 👥 Authors
- **Thandra Swetha** - Project Lead & Core Developer
