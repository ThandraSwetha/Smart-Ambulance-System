# 🚑 Smart Ambulance Dispatch System

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
- **Vercel**: Configuration included in `vercel.json`.
- **Streamlit Community Cloud**: Connect your GitHub repository for instant hosting.

## 👥 Authors
- **Thandra Swetha** - Project Lead & Core Developer

---
*Built with ❤️ for emergency response efficiency.*
