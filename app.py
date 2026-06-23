import streamlit as st
import json
import random
import math
import requests
import time
import base64
import os
import tempfile
from datetime import datetime
import streamlit.components.v1 as components
from groq import Groq
import pandas as pd
import re
import pytz

# ========== OPTIONAL: Object detection from uploaded images ==========
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
    except ImportError as e:
        return None, [{"error": f"Missing dependencies: {e}"}]
    except Exception as e:
        return None, [{"error": str(e)}]

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance Portal",
    layout="wide",
    page_icon="🌐"
)

# ========== CUSTOM CSS – LEOPARD BLACK THEME ==========
st.markdown("""
<style>
    .stApp {
        background: #0a0a0f;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(60, 40, 20, 0.15) 0%, transparent 25%),
            radial-gradient(circle at 70% 60%, rgba(60, 40, 20, 0.10) 0%, transparent 35%),
            radial-gradient(circle at 40% 80%, rgba(80, 50, 25, 0.12) 0%, transparent 30%),
            radial-gradient(circle at 85% 20%, rgba(40, 30, 15, 0.08) 0%, transparent 40%);
        color: #e0d5c8;
    }
    [data-testid="stSidebar"] {
        background: #0d0d12;
        background-image: 
            radial-gradient(circle at 30% 40%, rgba(70, 50, 30, 0.12) 0%, transparent 30%),
            radial-gradient(circle at 70% 70%, rgba(50, 35, 20, 0.08) 0%, transparent 35%);
        border-right: 1px solid #2a1f14;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stCaption {
        color: #d4c9bd !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1a120a, #2a1f14) !important;
        color: #e8ddd0 !important;
        border: 1px solid #4a3520 !important;
        border-radius: 8px !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2a1f14, #3d2a18) !important;
    }
    .question-list button {
        width: 100%; text-align: left; background: transparent; border: none; 
        color: #d4c9bd; padding: 6px 10px; border-radius: 4px;
    }
    .question-list button:hover {
        background: rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ========== AI VOICE SCRIPTS ==========
def generate_male_voice_audio():
    script = """
    Welcome to the Global Surveillance Radar Portal, built by Gesner Deslandes at GlobalInternet.py.
    This application features four main modules: Radar Control, Satellite Tracker, AI Analyst, and Object Detection.
    """
    return script

def generate_female_voice_audio():
    script = """
    Welcome to the Global Surveillance Radar Portal...
    """
    return script

def generate_audio_response(text, lang_code):
    try:
        from gtts import gTTS
        if not text.strip():
            return None
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(tmp_path)
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
        os.unlink(tmp_path)
        return audio_bytes
    except Exception as e:
        st.error(f"Audio generation error: {e}")
        return None

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

# ========== ALL YOUR ORIGINAL FUNCTIONS (kept unchanged) ==========
# Paste all your original functions here: get_real_ip, is_private_ip, get_location, geocode_location, classify_aircraft, 
# fetch_live_aircraft, get_demo_aircraft, get_satellites, etc.

# (Since your original file is very long, copy them from your backup into this file)

# ========== TRANSLATIONS ==========
UI = { ... }   # ← COPY YOUR FULL ORIGINAL UI DICTIONARY HERE (English, French, Spanish, Chinese)

# ========== LOGIN PAGE ==========
def login_page():
    # Your original login_page (unchanged)
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

# ========== ROBUST AI ANALYSIS ==========
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
            messages=[
                {"role": "system", "content": "You are a precise surveillance analyst. Only use the provided data."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2,
            max_tokens=600
        )
        response = completion.choices[0].message.content.strip()
        return response if response else "No response from AI."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# ========== MAIN PAGE ==========
def main_page():
    L = UI[st.session_state.lang]

    with st.sidebar:
        # === YOUR FULL ORIGINAL SIDEBAR CODE GOES HERE (copy from original file) ===
        st.markdown("<img src=...>", unsafe_allow_html=True)  # your profile image etc.
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French", "Spanish", "Chinese"], key="lang")
        # ... all your sidebar widgets, voice buttons, range slider, etc. (keep exactly as original)

    # Data fetching (your original code)
    use_demo = st.checkbox("Demo Mode (disable live OpenSky)", value=False, key="use_demo")
    if use_demo:
        aircraft_data = get_demo_aircraft()
        st.session_state.api_status = "Demo"
    else:
        aircraft_data, status = fetch_live_aircraft(18.5392, -72.3364)

    sat_data = get_satellites()
    location_name = "Port-au-Prince, Haiti"
    u_lat = 18.5392
    u_lon = -72.3364

    tab_radar, tab_sat, tab_ai, tab_detect = st.tabs([L["radar_tab"], L["sat_tab"], L["ai_tab"], L["detect_tab"]])

    # Radar tab, Satellite tab, Object Detection tab → keep your original code

    # ==================== FIXED AI ANALYST TAB ====================
    with tab_ai:
        st.title("🤖 AI Surveillance Analyst")
        
        common_questions = [
            "What is the current threat level in my area?",
            "How many aircraft are currently within 50 km of my ground station?",
            "Are there any military aircraft near my location?",
            "What is the closest aircraft to my position?",
            "How many drones are detected in my vicinity?",
            "What satellites are currently overhead?",
            "Are there any unusual or unidentified contacts on radar?",
            "Summarize all radar and satellite activity in my area."
        ]
        
        col_q, col_main = st.columns([1, 2])
        with col_q:
            st.markdown(f"### {L['common_questions_title']}")
            st.markdown('<div class="question-list">', unsafe_allow_html=True)
            for idx, q in enumerate(common_questions):
                if st.button(q, key=f"q_{idx}"):
                    st.session_state.ai_question_input = q
                    st.session_state.ai_response = ""
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_main:
            st.text_area(
                L['ai_question'],
                height=100,
                key="ai_question_text",
                placeholder="Type your question here..."
            )
            
            col_btn1, col_btn2 = st.columns(2)
            analyze_btn = col_btn1.button(L['ai_analyze'], use_container_width=True, type="primary")
            listen_btn = col_btn2.button(L['listen_response'], use_container_width=True)

            st.markdown("---")
            
            if st.session_state.ai_response:
                st.markdown(f"### {L['ai_response']}")
                st.markdown(st.session_state.ai_response)
            else:
                st.info("💡 Click 'Analyze' to get an AI response based on the current radar data.")

            if analyze_btn:
                question = st.session_state.get("ai_question_text", "").strip()
                if not question:
                    st.warning("Please enter a question.")
                else:
                    with st.spinner(L['ai_thinking']):
                        response = ai_analysis(aircraft_data, sat_data, u_lat, u_lon, location_name, question)
                        st.session_state.ai_response = response
                    st.rerun()

            if listen_btn and st.session_state.ai_response:
                lang_code = "en"
                audio_bytes = generate_audio_response(st.session_state.ai_response, lang_code)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("🔊 AI response played.")

# ========== RUN ==========
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
