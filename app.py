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
    script = """Welcome to the Global Surveillance Radar Portal..."""  # Keep your original full script
    return script  # Replace with your full original function content

def generate_female_voice_audio():
    script = """Welcome to the Global Surveillance Radar Portal..."""  # Keep your original
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

# ========== YOUR ORIGINAL FUNCTIONS (get_real_ip, fetch_live_aircraft, classify_aircraft, etc.) ==========
# Paste all your original functions here (get_real_ip, is_private_ip, get_location, geocode_location, classify_aircraft, 
# fetch_live_aircraft, get_demo_aircraft, get_satellites) - they remain unchanged.

# (For brevity in this message I didn't repeat all 300+ lines, but you should keep them exactly as in your first version)

# ========== TRANSLATIONS ==========
# Paste your full UI dictionary here (English, French, Spanish, Chinese) - unchanged

# ========== LOGIN PAGE ==========
def login_page():
    # Your original login_page code - unchanged
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""<div class="login-container">...</div>""", unsafe_allow_html=True)
        pwd = st.text_input("Enter Security Key", type="password")
        if st.button("Initialize System", key="login_btn", use_container_width=True):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Authorization")

# ========== FIXED AI ANALYSIS ==========
def ai_analysis(aircraft, satellites, u_lat, u_lon, location_name, question=None):
    if not aircraft:
        radar_summary = "No aircraft detected within the current range."
    else:
        sorted_aircraft = sorted(aircraft, key=lambda x: x.get("distance_km", 999))
        lines = [f"- {a['id']} ({a['type']}) at altitude {a['alt']}, distance {a.get('distance_km', 'N/A'):.1f} km (detected {a.get('detected_at','N/A')})" 
                for a in sorted_aircraft[:10]]
        radar_summary = "\n".join(lines)
    
    sat_summary = "\n".join([f"- {s['id']} ({s['type']}) at altitude {s['alt']}" for s in satellites])
    
    full_prompt = f"""You are an AI surveillance analyst. The user's ground station is located at {location_name} (Latitude {u_lat}, Longitude {u_lon}). 
Only report aircraft that are actually present in the list.

Ground Station: {location_name} ({u_lat}, {u_lon})

Radar Contacts:
{radar_summary}

Satellites:
{sat_summary}

Question: {question if question else "Give a threat summary"}
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
        return response if response else "⚠️ The AI returned an empty response."
    except Exception as e:
        return f"⚠️ AI Analysis Error: {str(e)}\n\nData Source: {st.session_state.api_status}"

# ========== MAIN PAGE ==========
def main_page():
    L = UI[st.session_state.lang]
    
    with st.sidebar:
        # === YOUR FULL ORIGINAL SIDEBAR CODE HERE (unchanged) ===
        # Include profile image, language selector, voice buttons, security, api status, max range, etc.
        pass  # ← Replace this comment with your full original sidebar code

    # Fetch data (your original logic)
    use_demo = st.session_state.get("use_demo", False)   # adjust if needed
    if use_demo:
        aircraft_data = get_demo_aircraft()
    else:
        aircraft_data, _ = fetch_live_aircraft(18.5392, -72.3364)
    
    sat_data = get_satellites()
    location_name = "Port-au-Prince, Haiti"
    u_lat = 18.5392
    u_lon = -72.3364

    tab_radar, tab_sat, tab_ai, tab_detect = st.tabs([L["radar_tab"], L["sat_tab"], L["ai_tab"], L["detect_tab"]])

    # Radar tab, Satellite tab, Object Detection tab → Keep exactly as in your original file

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
            "Are
