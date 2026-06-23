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
</style>
""", unsafe_allow_html=True)

# ========== GROQ CLIENT ==========
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Missing Groq API key.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ========== SESSION STATE ==========
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "lang" not in st.session_state: st.session_state.lang = "English"
if "ai_response" not in st.session_state: st.session_state.ai_response = ""
if "ai_question_input" not in st.session_state: st.session_state.ai_question_input = ""
if "cached_aircraft_data" not in st.session_state: st.session_state.cached_aircraft_data = []
if "cached_timestamp" not in st.session_state: st.session_state.cached_timestamp = None
if "api_status" not in st.session_state: st.session_state.api_status = "Initializing"

# ========== TRANSLATIONS ==========
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
    },
    "French": {}, "Spanish": {}, "Chinese": {}
}  # Replace with your full original UI if needed

# ========== AI ANALYSIS ==========
def ai_analysis(aircraft, satellites, u_lat, u_lon, location_name, question=None):
    if not aircraft:
        radar_summary = "No aircraft detected within the current range."
    else:
        sorted_aircraft = sorted(aircraft, key=lambda x: x.get("distance_km", 999))
        lines = [f"- {a['id']} ({a['type']}) at altitude {a['alt']}, distance {a.get('distance_km', 'N/A'):.1f} km" for a in sorted_aircraft[:10]]
        radar_summary = "\n".join(lines)
    
    sat_summary = "\n".join([f"- {s['id']} ({s['type']}) at altitude {s['alt']}" for s in satellites])
    
    full_prompt = f"""You are an AI surveillance analyst. Ground station: {location_name} ({u_lat}, {u_lon}).

Radar Contacts:
{radar_summary}

Satellites:
{sat_summary}

Question: {question}
Answer:"""

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "Be precise. Use only provided data."},
                      {"role": "user", "content": full_prompt}],
            temperature=0.2,
            max_tokens=600
        )
        return completion.choices[0].message.content.strip() or "No response."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

def generate_audio_response(text, lang_code="en"):
    try:
        from gtts import gTTS
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(tmp_path)
        with open(tmp_path, "rb") as f:
            return f.read()
        os.unlink(tmp_path)
    except:
        return None

# ========== LOGIN ==========
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        pwd = st.text_input("Enter Security Key", type="password")
        if st.button("Initialize System"):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid key")

# ========== MAIN PAGE ==========
def main_page():
    L = UI.get(st.session_state.lang, UI["English"])

    with st.sidebar:
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French", "Spanish
