import streamlit as st
import json
import math
import requests
import time
import os
import tempfile
from datetime import datetime
import streamlit.components.v1 as components
from groq import Groq
import re
import pytz

# ========== OBJECT DETECTION ==========
def run_object_detection(image_bytes):
    try:
        from ultralytics import YOLO
        import cv2
        model = YOLO("yolov8n.pt")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name
        results = model(tmp_path)
        os.unlink(tmp_path)
        img = cv2.imread(tmp_path)
        if img is None:
            return None, [{"error": "Could not read image"}]
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    detections.append({"label": label, "confidence": f"{conf:.2f}", "bbox": (x1, y1, x2, y2)})
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, f"{label} {conf:.2f}", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img_rgb, detections
    except Exception as e:
        return None, [{"error": str(e)}]

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance Portal",
    layout="wide",
    page_icon="🌐"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .stApp {background: #0a0a0f; color: #e0d5c8;}
    [data-testid="stSidebar"] {background: #0d0d12; border-right: 1px solid #2a1f14;}
    .stButton>button {background: linear-gradient(135deg, #1a120a, #2a1f14) !important; color: #e8ddd0 !important;}
    .question-list button {width: 100%; text-align: left; background: transparent; border: none; color: #d4c9bd; padding: 6px 10px;}
    .question-list button:hover {background: rgba(255,255,255,0.1);}
</style>
""", unsafe_allow_html=True)

# ========== GROQ CLIENT ==========
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ========== SESSION STATE ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""
if "ai_question_input" not in st.session_state:
    st.session_state.ai_question_input = ""
if "cached_aircraft_data" not in st.session_state:
    st.session_state.cached_aircraft_data = []
if "cached_timestamp" not in st.session_state:
    st.session_state.cached_timestamp = None
if "api_status" not in st.session_state:
    st.session_state.api_status = "Initializing"

# ========== TRANSLATIONS (UI) ==========
# Paste your full original UI dictionary here
UI = {
    "English": {
        "radar_tab": "📡 Radar Control",
        "sat_tab": "🛰️ Satellite Tracker",
        "ai_tab": "🤖 AI Analyst",
        "detect_tab": "🕵️ Object Detection",
        "ai_question": "Ask about radar contacts or satellite predictions:",
        "ai_analyze": "Analyze Current Threat Level",
        "ai_thinking": "🤖 AI analyzing surveillance data...",
        "ai_response": "💡 AI Analyst Report",
        "common_questions_title": "💬 Common Questions",
        "listen_response": "🔊 Listen to AI Response",
        # Add the rest of your keys from the original file
    },
    "French": {}, "Spanish": {}, "Chinese": {}  # Fill with your original translations
}

# ========== AI ANALYSIS ==========
def ai_analysis(aircraft, satellites, u_lat, u_lon, location_name, question=None):
    if not aircraft:
        radar_summary = "No aircraft detected within the current range."
    else:
        sorted_aircraft = sorted(aircraft, key=lambda x: x.get("distance_km", 999))
        lines = [f"- {a['id']} ({a['type']}) at altitude {a['alt']}, distance {a.get('distance_km', 'N/A'):.1f} km" for a in sorted_aircraft[:10]]
        radar_summary = "\n".join(lines)
    
    sat_summary = "\n".join([f"- {s['id']} ({s['type']}) at altitude {s['alt']}" for s in satellites])
    
    full_prompt = f"""You are an AI surveillance analyst.
Ground Station: {location_name} ({u_lat}, {u_lon})

Radar Contacts:
{radar_summary}

Satellites:
{sat_summary}

Question: {question}
Answer:"""
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a precise surveillance analyst. Only use the provided data."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2,
            max_tokens=600
        )
        return completion.choices[0].message.content.strip() or "No response generated."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# ========== LOGIN ==========
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <h2 style="text-align:center; color:#e8ddd0;">🌐 GlobalInternet.py Access</h2>
            <p style="text-align:center; color:#a09080;">Secure Surveillance Portal</p>
        </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("Enter Security Key", type="password")
        if st.button("Initialize System", key="login_btn", use_container_width=True):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Authorization")

# ========== MAIN PAGE ==========
def main_page():
    L = UI.get(st.session_state.lang, UI["English"])

    with st.sidebar:
        # === YOUR ORIGINAL SIDEBAR CODE ===
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French", "Spanish", "Chinese"], key="lang")
        use_demo = st.checkbox("Demo Mode (disable live OpenSky)", value=False)
        if st.button("Refresh Live Data", use_container_width=True):
            st.rerun()
        # Add the rest of your sidebar (voice buttons, range, status, etc.)

    # Data Fetching (add your original fetch_live_aircraft logic here)
    if use_demo:
        aircraft_data = []  # replace with get_demo_aircraft()
    else:
        aircraft_data = []  # replace with your fetch function

    sat_data = [{"id": "ISS", "type": "Space Station", "alt": "408km"}]
    location_name = "Port-au-Prince, Haiti"
    u_lat = 18.5392
    u_lon = -72.3364

    tab_radar, tab_sat, tab_ai, tab_detect = st.tabs([L.get("radar_tab", "Radar"), L.get("sat_tab", "Satellite"), L.get("ai_tab", "AI Analyst"), L.get("detect_tab", "Detection")])

    # Radar, Satellite, Object Detection tabs - keep your original code here

    # FIXED AI ANALYST TAB
    with tab_ai:
        st.title("🤖 AI Surveillance Analyst")
        
        common_questions = [
            "What is the current threat level in my area?",
            "How many aircraft are currently within 50 km of my ground station?",
            "Are there any military aircraft near my location?",
            "What is the closest aircraft to my position?",
            "How many drones are detected in my vicinity?",
            "Summarize all radar and satellite activity in my area."
        ]
        
        col_q, col_main = st.columns([1, 2])
        with col_q:
            st.markdown(f"### {L.get('common_questions_title', 'Common Questions')}")
            st.markdown('<div class="question-list">', unsafe_allow_html=True)
            for idx, q in enumerate(common_questions):
                if st.button(q, key=f"q_{idx}"):
                    st.session_state.ai_question_input = q
                    st.session_state.ai_response = ""
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_main:
            st.text_area(
                L.get('ai_question', 'Ask your question:'),
                height=120,
                key="ai_question_text",
                placeholder="Type your question here..."
            )
            
            col_btn1, col_btn2 = st.columns(2)
            analyze_btn = col_btn1.button(L.get('ai_analyze', 'Analyze Current Threat Level'), use_container_width=True, type="primary")
            listen_btn = col_btn2.button(L.get('listen_response', 'Listen to AI Response'), use_container_width=True)

            st.markdown("---")
            
            if st.session_state.ai_response:
                st.markdown(f"### {L.get('ai_response', 'AI Analyst Report')}")
                st.markdown(st.session_state.ai_response)
            else:
                st.info("💡 Click 'Analyze' to get an AI response based on the current radar data.")

            if analyze_btn:
                question = st.session_state.get("ai_question_text", "").strip()
                if not question:
                    st.warning("Please enter a question.")
                else:
                    with st.spinner(L.get('ai_thinking', 'AI analyzing...')):
                        response = ai_analysis(aircraft_data, sat_data, u_lat, u_lon, location_name, question)
                        st.session_state.ai_response = response
                    st.rerun()

            if listen_btn and st.session_state.ai_response:
                audio_bytes = None  # Add generate_audio_response call
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")

# ========== RUN ==========
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
