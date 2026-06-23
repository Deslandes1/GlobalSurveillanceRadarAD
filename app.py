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

# ========== OPTIONAL: Object detection ==========
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
st.set_page_config(page_title="GlobalInternet.py | Surveillance Portal", layout="wide", page_icon="🌐")

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .stApp {background: #0a0a0f; color: #e0d5c8;}
    [data-testid="stSidebar"] {background: #0d0d12; border-right: 1px solid #2a1f14;}
    .stButton>button {background: linear-gradient(135deg, #1a120a, #2a1f14) !important; color: #e8ddd0 !important; border: 1px solid #4a3520 !important;}
    .stButton>button:hover {background: linear-gradient(135deg, #2a1f14, #3d2a18) !important;}
    .question-list button {width: 100%; text-align: left; background: transparent; border: none; color: #d4c9bd; padding: 6px 10px; border-radius: 4px;}
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

# ========== AI ANALYSIS FUNCTION ==========
def ai_analysis(aircraft, satellites, u_lat, u_lon, location_name, question=None):
    if not aircraft:
        radar_summary = "No aircraft detected within the current range."
    else:
        sorted_aircraft = sorted(aircraft, key=lambda x: x.get("distance_km", 999))
        lines = [f"- {a['id']} ({a['type']}) at altitude {a['alt']}, distance {a.get('distance_km', 'N/A'):.1f} km" 
                 for a in sorted_aircraft[:10]]
        radar_summary = "\n".join(lines)
    
    sat_summary = "\n".join([f"- {s['id']} ({s['type']}) at altitude {s['alt']}" for s in satellites])
    
    full_prompt = f"""You are an AI surveillance analyst. The user's ground station is located at {location_name} (Latitude {u_lat}, Longitude {u_lon}).
Use the following live ADS-B data to answer the question.

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
                {"role": "system", "content": "You are a precise surveillance analyst. Only use the provided data. Do not invent contacts."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2,
            max_tokens=600
        )
        response = completion.choices[0].message.content.strip()
        return response if response else "⚠️ The AI returned an empty response. Please try again."
    except Exception as e:
        return f"⚠️ AI Analysis Error: {str(e)}\n\nData Source: {st.session_state.api_status}"

# ========== VOICE FUNCTIONS (simplified) ==========
def generate_audio_response(text, lang_code="en"):
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
    except Exception:
        return None

# ========== TRANSLATIONS (shortened for space - add your full UI dict if needed) ==========
# ... Paste your full UI dictionary here if you want all languages ...

def main_page():
    L = UI[st.session_state.lang] if 'UI' in globals() else {"ai_analyze": "Analyze", "ai_thinking": "Thinking...", "ai_response": "AI Analyst Report", "ai_question": "Ask your question:"}  # fallback

    # Sidebar (you can keep your full sidebar)
    with st.sidebar:
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French", "Spanish", "Chinese"], key="lang")
        use_demo = st.checkbox("Demo Mode", value=False)
        if st.button("Refresh Data"):
            st.rerun()

    aircraft_data = get_demo_aircraft() if use_demo else []  # placeholder - replace with your fetch function
    sat_data = [{"id": "ISS", "type": "Space Station", "alt": "408km"}]
    location_name = "Port-au-Prince, Haiti"
    u_lat, u_lon = 18.5392, -72.3364

    tab_radar, tab_sat, tab_ai, tab_detect = st.tabs(["📡 Radar", "🛰️ Satellite", "🤖 AI Analyst", "🕵️ Object Detection"])

    with tab_ai:
        st.title("🤖 AI Surveillance Analyst")
        
        common_questions = [
            "What is the current threat level in my area?",
            "How many aircraft are currently within 50 km?",
            "What is the closest aircraft to my position?",
            "Are there any military aircraft nearby?",
            "Summarize all radar activity."
        ]
        
        col_q, col_main = st.columns([1, 2])
        with col_q:
            st.subheader("Common Questions")
            for idx, q in enumerate(common_questions):
                if st.button(q, key=f"q_{idx}"):
                    st.session_state.ai_question_input = q
                    st.session_state.ai_response = ""
                    st.rerun()

        with col_main:
            st.text_area(
                "Ask about radar contacts or satellite predictions:",
                height=120,
                key="ai_question_text",
                placeholder="Type your question here..."
            )
            
            col_btn1, col_btn2 = st.columns(2)
            analyze_btn = col_btn1.button("Analyze Current Threat Level", use_container_width=True, type="primary")
            listen_btn = col_btn2.button("🔊 Listen to Response", use_container_width=True)

            st.markdown("---")

            if st.session_state.ai_response:
                st.subheader("AI Analyst Report")
                st.markdown(st.session_state.ai_response)
            else:
                st.info("💡 Click **Analyze** to get an AI response based on current radar data.")

            if analyze_btn:
                question = st.session_state.get("ai_question_text", "").strip()
                if not question:
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("🤖 AI analyzing surveillance data..."):
                        response = ai_analysis(aircraft_data, sat_data, u_lat, u_lon, location_name, question)
                        st.session_state.ai_response = response
                    st.rerun()

            if listen_btn and st.session_state.ai_response:
                with st.spinner("Generating audio..."):
                    audio = generate_audio_response(st.session_state.ai_response)
                    if audio:
                        st.audio(audio, format="audio/mp3")
                    else:
                        st.error("Audio generation failed.")

# ========== RUN APP ==========
if not st.session_state.authenticated:
    st.title("GlobalInternet.py Surveillance Portal")
    pwd = st.text_input("Enter Security Key", type="password")
    if st.button("Login"):
        if pwd == "20082010":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid key")
else:
    main_page()
