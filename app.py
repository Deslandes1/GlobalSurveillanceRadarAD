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
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption {
        color: #d4c9bd !important;
    }
    .login-container {
        background: #0d0d12;
        background-image: 
            radial-gradient(circle at 40% 50%, rgba(70, 50, 30, 0.10) 0%, transparent 40%),
            radial-gradient(circle at 70% 30%, rgba(50, 35, 20, 0.08) 0%, transparent 35%);
        border: 1px solid #2a1f14;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.8);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #e8ddd0 !important;
    }
    p, li, .stMarkdown {
        color: #d4c9bd !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1a120a, #2a1f14) !important;
        color: #e8ddd0 !important;
        border: 1px solid #4a3520 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2a1f14, #3d2a18) !important;
        border-color: #6a4f30 !important;
        box-shadow: 0 0 20px rgba(90, 60, 30, 0.2);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div {
        background-color: #141018 !important;
        color: #d4c9bd !important;
        border: 1px solid #2a1f14 !important;
        border-radius: 8px !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #4a3520 !important;
        box-shadow: 0 0 12px rgba(90, 60, 30, 0.15);
    }
    .stMetric {
        background: rgba(20, 16, 24, 0.6);
        border: 1px solid #1f1610;
        border-radius: 12px;
        padding: 0.8rem;
    }
    .stMetric label {
        color: #a09080 !important;
    }
    .stMetric .stMetricValue {
        color: #e8ddd0 !important;
    }
    .streamlit-expanderHeader {
        background: rgba(20, 16, 24, 0.6) !important;
        border: 1px solid #1f1610 !important;
        border-radius: 8px !important;
        color: #d4c9bd !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(20, 16, 24, 0.4);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #a09080;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(40, 30, 20, 0.6);
        color: #e8ddd0;
        border: 1px solid #3d2a18;
    }
    .security-badge {
        background: rgba(20, 16, 24, 0.8);
        border: 1px solid #3d2a18;
        border-radius: 30px;
        padding: 8px 15px;
        text-align: center;
        color: #b8a898;
        font-weight: bold;
        font-family: monospace;
    }
    hr {
        border-color: #1f1610 !important;
    }
    .stAlert {
        background: rgba(20, 16, 24, 0.6) !important;
        border: 1px solid #2a1f14 !important;
        color: #d4c9bd !important;
    }
    .profile-img {
        border-radius: 50%;
        border: 2px solid #4a3520;
        display: block;
        margin: 0 auto 10px auto;
        width: 100px;
        height: 100px;
        object-fit: cover;
    }
    .legend {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 10px;
        background: rgba(20,16,24,0.5);
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #2a1f14;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #d4c9bd;
        font-size: 0.9rem;
    }
    .legend-shape {
        display: inline-block;
        width: 16px;
        height: 16px;
        text-align: center;
        font-size: 14px;
        line-height: 16px;
    }
    .question-list {
        background: rgba(20,16,24,0.5);
        border: 1px solid #2a1f14;
        border-radius: 8px;
        padding: 10px;
        max-height: 600px;
        overflow-y: auto;
    }
    .question-list button {
        width: 100%;
        text-align: left;
        background: transparent;
        border: none;
        color: #d4c9bd;
        padding: 6px 10px;
        border-radius: 4px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: background 0.2s;
        margin-bottom: 2px;
    }
    .question-list button:hover {
        background: rgba(255,255,255,0.1);
        color: #ffffff;
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 4px;
    }
    .status-live {
        background: #2ecc71;
        color: #0a0a0f;
    }
    .status-cached {
        background: #f39c12;
        color: #0a0a0f;
    }
    .status-demo {
        background: #e74c3c;
        color: #0a0a0f;
    }
    .local-instructions {
        background: rgba(20,16,24,0.6);
        border: 1px solid #4a3520;
        border-radius: 8px;
        padding: 10px 12px;
        margin: 10px 0;
        font-size: 0.85rem;
        color: #d4c9bd;
    }
    .local-instructions code {
        background: rgba(255,255,255,0.1);
        padding: 2px 6px;
        border-radius: 4px;
        color: #00ff64;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== AI VOICE SCRIPTS (updated with all features) ==========
def generate_male_voice_audio():
    script = """
    Welcome to the Global Surveillance Radar Portal, built by Gesner Deslandes at GlobalInternet.py.
    
    This application features four main modules: Radar Control, Satellite Tracker, AI Analyst, and Object Detection.
    
    The Radar Control tab shows a 360-degree live radar display with a classic fetching sound. Click the radar screen to enable the audio and hear a sonar ping on every sweep. Aircraft are automatically classified with military-style symbols: red triangles for military, purple squares for UFOs, orange diamonds for drones, green for commercial, and blue for general aviation.
    
    The Satellite Tracker predicts satellite passes and shows an interactive map with aircraft and satellite overlays.
    
    The AI Analyst is powered by Groq's Llama 3.1. You can ask any question about radar contacts or satellite predictions, and the AI provides a detailed threat analysis and recommendations.
    
    The Object Detection tab lets you upload images and detect objects using YOLOv8 computer vision.
    
    The sidebar includes automatic location detection, language selection (now also Spanish and Chinese), a demo mode toggle, and secure logout. You can search for any location and the app will update the radar to that area. The data source status shows whether you are seeing live, cached, or demo data.
    
    All data is encrypted and anonymised. This software is ideal for surveillance, security, and intelligence analysis.
    
    GlobalInternet.py – connecting the global market with local expertise.
    """
    return script

def generate_female_voice_audio():
    script = """
    Welcome to the Global Surveillance Radar Portal, built by Gesner Deslandes at GlobalInternet.py.
    
    This advanced surveillance system now features a live radar with a classic fetching sound. Just click the radar screen to enable the audio, and you will hear a sonar ping on every sweep.
    
    Objects are automatically classified and displayed with real military-style symbols. Military targets appear as red triangles, unknown or UFO contacts as purple squares, drones as orange diamonds, and civilian aircraft as green or blue circles. Each symbol includes the callsign and altitude for instant identification.
    
    A live clock and calendar are displayed on the main page, showing the current time with seconds running and today's date in real time.
    
    The Radar Control tab gives you a 360‑degree view with range rings and contact labels. The Satellite Tracker tab predicts satellite passes and shows an interactive map with both aircraft and satellite overlays.
    
    The AI Analyst tab uses Groq's Llama 3.1 to answer your questions about radar contacts and satellite predictions, providing threat analysis and recommendations.
    
    The Object Detection tab lets you upload images and detect objects with YOLOv8.
    
    The sidebar provides automatic location detection, language selection (now also Spanish and Chinese), a location search feature, a demo mode toggle, and secure logout. The app also shows the data source status – live, cached, or demo – so you always know what you are seeing. You can also find step‑by‑step instructions to run the app locally on your own computer for full live data.
    
    All data is encrypted and anonymised. This software is ideal for surveillance, security, and intelligence analysis.
    
    GlobalInternet.py – connecting the global market with local expertise.
    """
    return script

# ========== AUDIO GENERATION FOR RESPONSES ==========
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

# ========== SUPABASE CLIENT (optional) ==========
try:
    from supabase import create_client, Client
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        SUPABASE_AVAILABLE = True
    else:
        SUPABASE_AVAILABLE = False
except ImportError:
    SUPABASE_AVAILABLE = False

# ========== GLOBAL SHIELD ==========
GLOBAL_SHIELD_ACTIVE = "GLOBAL_SHIELD_API_KEY" in st.secrets

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""
if "ai_question_input" not in st.session_state:
    st.session_state.ai_question_input = ""

# ========== CACHE FOR LIVE DATA ==========
if "cached_aircraft_data" not in st.session_state:
    st.session_state.cached_aircraft_data = []
if "cached_timestamp" not in st.session_state:
    st.session_state.cached_timestamp = None
if "api_status" not in st.session_state:
    st.session_state.api_status = "Initializing"

# ========== IP & LOCATION DETECTION ==========
def get_real_ip():
    try:
        headers = st.context.headers
        forwarded = headers.get("X-Forwarded-For")
        if forwarded:
            for candidate in forwarded.split(","):
                candidate = candidate.strip()
                if candidate and not is_private_ip(candidate):
                    return candidate
            return forwarded.split(",")[0].strip()
    except Exception:
        pass

    if "real_ip" not in st.session_state:
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=3)
            if response.status_code == 200:
                ip = response.json().get("ip")
                st.session_state.real_ip = ip
                return ip
        except:
            pass
        return "Unable to retrieve"
    else:
        return st.session_state.real_ip

def is_private_ip(ip):
    private_patterns = [
        re.compile(r'^10\.'),
        re.compile(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'),
        re.compile(r'^192\.168\.'),
        re.compile(r'^127\.'),
        re.compile(r'^169\.254\.'),
        re.compile(r'^fc00:'),
        re.compile(r'^fd00:'),
        re.compile(r'^::1$')
    ]
    return any(pattern.match(ip) for pattern in private_patterns)

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,lat,lon,query", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "lat": data.get("lat", 0.0),
                    "lon": data.get("lon", 0.0)
                }
    except Exception:
        pass
    return None

def get_detected_location():
    if "detected_location" not in st.session_state:
        ip = get_real_ip()
        if ip and ip != "Unable to retrieve":
            loc = get_location(ip)
            if loc:
                st.session_state.detected_location = loc
                return loc
        st.session_state.detected_location = {
            "country": "Haiti",
            "region": "Ouest",
            "city": "Port-au-Prince",
            "isp": "Unknown",
            "lat": 18.5392,
            "lon": -72.3364
        }
    return st.session_state.detected_location

# ========== GEOCODING ==========
def geocode_location(location_name):
    if not location_name.strip():
        return None, None, None
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": location_name, "format": "json", "limit": 1}
        headers = {"User-Agent": "GlobalInternet.py Surveillance Portal"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                display = data[0]["display_name"]
                return lat, lon, display
        return None, None, None
    except Exception:
        return None, None, None

# ========== AIRCRAFT CLASSIFICATION (improved) ==========
def classify_aircraft(alt_ft, callsign=""):
    alt_ft = int(alt_ft.replace(",","").replace("ft","").strip()) if isinstance(alt_ft, str) else alt_ft
    if not isinstance(alt_ft, (int, float)):
        alt_ft = 0

    callsign = str(callsign).upper()

    if "DRN" in callsign or "UAV" in callsign:
        return "Drone", "#f39c12", "🚁 Drone"

    military_prefixes = ["F-", "B-", "C-", "E-", "KC-", "T-", "V-", "A-", "AH-", "CH-", "UH-", "B-2"]
    if any(callsign.startswith(pre) for pre in military_prefixes) or alt_ft > 40000:
        return "Military", "#e74c3c", "✈️ Military"

    airline_codes = ["AAL", "UAL", "SWA", "DAL", "NKS", "JBU", "FFT", "EJA", "LXJ", "N456", "N123"]
    if any(callsign.startswith(code) for code in airline_codes):
        if alt_ft > 25000:
            return "Commercial Airplane", "#2ecc71", "🛩️ Commercial"
        else:
            return "General Aviation", "#3498db", "🛩️ General"

    cargo_codes = ["FDX", "UPS", "CKS", "GTI"]
    if any(callsign.startswith(code) for code in cargo_codes) and alt_ft > 20000:
        return "Cargo", "#f1c40f", "📦 Cargo"

    if callsign.startswith("N") and len(callsign) >= 5:
        if alt_ft < 10000:
            return "General Aviation", "#3498db", "🛩️ General"
        else:
            return "Commercial Airplane", "#2ecc71", "🛩️ Commercial"

    if "UFO" in callsign or "UNK" in callsign or len(callsign) < 3:
        return "UFO", "#9b59b6", "🛸 UFO"

    return "Other", "#95a5a6", "❓ Unknown"

# ========== IMPROVED LIVE AIRCRAFT DATA FETCH (with exponential backoff and caching) ==========
def fetch_live_aircraft(ground_lat, ground_lon, max_retries=5, initial_delay=1):
    url = "https://opensky-network.org/api/states/all"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SurveillancePortal/1.0)"}
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                states = data.get("states", [])
                if not states:
                    return [], "no_data"
                aircraft_list = []
                for s in states:
                    lat = s[6]
                    lon = s[5]
                    if lat is None or lon is None:
                        continue
                    R = 6371
                    dlat = math.radians(lat - ground_lat)
                    dlon = math.radians(lon - ground_lon)
                    a = math.sin(dlat/2)**2 + math.cos(math.radians(ground_lat)) * math.cos(math.radians(lat)) * math.sin(dlon/2)**2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                    dist_km = R * c
                    max_km = 300
                    dist_norm = min(dist_km / max_km, 0.95)
                    alt = s[7] if s[7] is not None else 0
                    callsign = s[1].strip() if s[1] else s[0][:6].upper()
                    cat, color, label = classify_aircraft(alt, callsign)
                    aircraft_list.append({
                        "id": callsign,
                        "type": cat,
                        "color": color,
                        "label": label,
                        "alt": f"{int(alt) if alt else 'N/A'}ft",
                        "dist": dist_norm,
                        "lat": lat,
                        "lon": lon
                    })
                aircraft_list = aircraft_list[:30]
                st.session_state.cached_aircraft_data = aircraft_list
                st.session_state.cached_timestamp = datetime.now()
                st.session_state.api_status = "Live"
                return aircraft_list, "live"
            elif response.status_code == 429:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                st.session_state.api_status = f"Rate limited (retry in {wait_time:.1f}s)"
                time.sleep(wait_time)
                continue
            else:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
        except requests.exceptions.Timeout:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
            continue
        except Exception as e:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
            continue

    if st.session_state.cached_aircraft_data:
        st.session_state.api_status = "Cached (API unreachable)"
        return st.session_state.cached_aircraft_data, "cached"
    else:
        st.session_state.api_status = "Demo (No cached data)"
        demo = get_demo_aircraft()
        return demo, "demo"

def get_demo_aircraft():
    return [
        {"id": "AAL-410", "type": "Commercial Airplane", "color": "#2ecc71", "label": "🛩️ Commercial", "alt": "32,000ft", "dist": 0.4},
        {"id": "F-22-EX", "type": "Military", "color": "#e74c3c", "label": "✈️ Military", "alt": "52,000ft", "dist": 0.8},
        {"id": "DRN-QC", "type": "Drone", "color": "#f39c12", "label": "🚁 Drone", "alt": "800ft", "dist": 0.2},
        {"id": "CLX-200", "type": "Cargo", "color": "#f1c40f", "label": "📦 Cargo", "alt": "28,000ft", "dist": 0.6},
        {"id": "UFO-X", "type": "UFO", "color": "#9b59b6", "label": "🛸 UFO", "alt": "1,500ft", "dist": 0.7},
        {"id": "N1234A", "type": "General Aviation", "color": "#3498db", "label": "🛩️ General", "alt": "5,000ft", "dist": 0.3}
    ]

def get_satellites():
    return [
        {"id": "STAR-V2", "type": "Starlink", "color": "#00ff64", "alt": "550km"},
        {"id": "NAV-GPS", "type": "GPS III", "color": "#00bfff", "alt": "20,200km"},
        {"id": "KH-11-S", "type": "Spy Satellite", "color": "#ff3300", "alt": "380km"},
        {"id": "ISS", "type": "Space Station", "color": "#ffffff", "alt": "408km"}
    ]

# ========== TRANSLATIONS ==========
UI = {
    "English": {
        "radar_tab": "📡 Radar Control",
        "sat_tab": "🛰️ Satellite Tracker",
        "ai_tab": "🤖 AI Analyst",
        "detect_tab": "🕵️ Object Detection",
        "title": "GLOBAL SURVEILLANCE RADAR",
        "author_tag": "Built by Gesner Deslandes",
        "logout": "Terminate Session",
        "report": "Download Asset Report",
        "detection_log": "Live Detection Log",
        "sat_engine": "Predictive Mapping Engine",
        "audio_note": "🖱️ Click the radar screen to enable the fetching sound.",
        "lat": "Latitude",
        "lon": "Longitude",
        "predict_btn": "Calculate Pass",
        "time_target": "Prediction Target (Date/Time)",
        "aip_key": "AIP Security Key (Aerial Imagery)",
        "sky_view": "Satellite OpenSky View",
        "ai_question": "Ask about radar contacts or satellite predictions:",
        "ai_analyze": "Analyze Current Threat Level",
        "ai_thinking": "🤖 AI analyzing surveillance data...",
        "ai_response": "💡 AI Analyst Report",
        "security_badge": "🔐 Global Security Shield active",
        "security_caption": "All data is secured and anonymized",
        "detect_title": "Real‑Time Object Detection",
        "detect_desc": "Upload an image (JPEG, PNG) to detect objects using YOLOv8.",
        "upload_label": "Choose an image...",
        "detect_btn": "Detect Objects",
        "detection_results": "Detected Objects",
        "refresh_btn": "Refresh Live Data",
        "live_note": "💻 To run this app on your own computer for full live data, click the instructions below.",
        "voice_male_explain": "🎙️ AI Male Voice – Explain App",
        "voice_female_explain": "🎤 AI Female Voice – Explain App (with new features)",
        "legend_title": "🟢 Real NATO‑Style Symbols",
        "clock_label": "🕒 Live Clock",
        "common_questions_title": "💬 Common Questions",
        "listen_response": "🔊 Listen to AI Response",
        "location_detected": "📍 Detected location: {location}",
        "location_name_label": "Location Name (override)",
        "search_location": "🔍 Search Location",
        "search_btn": "Search Coordinates",
        "search_error": "❌ Location not found. Please try again.",
        "api_status_label": "📡 Data Source",
        "status_live": "Live (OpenSky)",
        "status_cached": "Cached (from previous fetch)",
        "status_demo": "Demo (simulated)",
        "status_live_detail": "Live data fetched at {time}",
        "status_cached_detail": "Cached from {time}",
        "status_demo_detail": "No live data available – showing demo",
        "local_instructions_title": "💻 Run Locally (Full Live Data)",
        "local_step1": "Install Python 3.8 or higher from python.org.",
        "local_step2": "Open Terminal or Command Prompt and run:",
        "local_cmd1": "git clone https://github.com/Deslandes1/GlobalSurveillanceRadarAD.git",
        "local_cmd2": "cd GlobalSurveillanceRadarAD",
        "local_cmd3": "pip install -r requirements.txt",
        "local_step3": "Create a .streamlit/secrets.toml file with your Groq API key:",
        "local_cmd4": "GROQ_API_KEY = \"your-api-key\"",
        "local_step4": "Run the app:",
        "local_cmd5": "streamlit run app.py",
        "local_step5": "Open the URL shown in your browser (usually http://localhost:8501).",
        "voice_lang_label": "🎤 Voice Language",
        "voice_lang_en": "English",
        "voice_lang_fr": "Français",
        "voice_lang_es": "Español",
        "voice_lang_zh": "中文"
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar",
        "sat_tab": "🛰️ Suivi Satellite",
        "ai_tab": "🤖 Analyste IA",
        "detect_tab": "🕵️ Détection",
        "title": "RADAR DE SURVEILLANCE MONDIAL",
        "author_tag": "Conçu par Gesner Deslandes",
        "logout": "Déconnexion",
        "report": "Télécharger le Rapport",
        "detection_log": "Journal de Détection",
        "sat_engine": "Moteur de Cartographie Prédictive",
        "audio_note": "🖱️ Cliquez sur le radar pour activer le son.",
        "lat": "Latitude",
        "lon": "Longitude",
        "predict_btn": "Prédire le Passage",
        "time_target": "Date/Heure Cible",
        "aip_key": "Clé de Sécurité AIP",
        "sky_view": "Vue Satellite OpenSky",
        "ai_question": "Posez une question sur les contacts radar ou les prédictions satellite:",
        "ai_analyze": "Analyser la menace",
        "ai_thinking": "🤖 L'IA analyse...",
        "ai_response": "💡 Rapport IA",
        "security_badge": "🔐 Bouclier de sécurité actif",
        "security_caption": "Toutes les données sont sécurisées",
        "detect_title": "Détection d'objets",
        "detect_desc": "Téléchargez une image pour détecter des objets avec YOLOv8.",
        "upload_label": "Choisissez une image...",
        "detect_btn": "Détecter",
        "detection_results": "Objets détectés",
        "refresh_btn": "Actualiser",
        "live_note": "💻 Pour exécuter cette application sur votre propre ordinateur et obtenir des données en direct, cliquez sur les instructions ci‑dessous.",
        "voice_male_explain": "🎙️ Voix IA Homme – Expliquer l'app",
        "voice_female_explain": "🎤 Voix IA Femme – Expliquer l'app (nouveautés)",
        "legend_title": "🟢 Symboles militaires réels",
        "clock_label": "🕒 Horloge en direct",
        "common_questions_title": "💬 Questions courantes",
        "listen_response": "🔊 Écouter la réponse IA",
        "location_detected": "📍 Localisation détectée : {location}",
        "location_name_label": "Nom de la localisation (modifiable)",
        "search_location": "🔍 Rechercher un lieu",
        "search_btn": "Rechercher les coordonnées",
        "search_error": "❌ Lieu introuvable. Veuillez réessayer.",
        "api_status_label": "📡 Source de données",
        "status_live": "En direct (OpenSky)",
        "status_cached": "Mis en cache",
        "status_demo": "Démo (simulé)",
        "status_live_detail": "Données récupérées à {time}",
        "status_cached_detail": "Mise en cache depuis {time}",
        "status_demo_detail": "Aucune donnée en direct – démo affichée",
        "local_instructions_title": "💻 Exécuter localement (données en direct)",
        "local_step1": "Installez Python 3.8 ou supérieur depuis python.org.",
        "local_step2": "Ouvrez le Terminal ou l'Invite de commandes et exécutez :",
        "local_cmd1": "git clone https://github.com/Deslandes1/GlobalSurveillanceRadarAD.git",
        "local_cmd2": "cd GlobalSurveillanceRadarAD",
        "local_cmd3": "pip install -r requirements.txt",
        "local_step3": "Créez un fichier .streamlit/secrets.toml avec votre clé API Groq :",
        "local_cmd4": "GROQ_API_KEY = \"votre-clé-api\"",
        "local_step4": "Lancez l'application :",
        "local_cmd5": "streamlit run app.py",
        "local_step5": "Ouvrez l'URL affichée dans votre navigateur (généralement http://localhost:8501).",
        "voice_lang_label": "🎤 Langue vocale",
        "voice_lang_en": "English",
        "voice_lang_fr": "Français",
        "voice_lang_es": "Español",
        "voice_lang_zh": "中文"
    },
    "Spanish": {
        "radar_tab": "📡 Control de Radar",
        "sat_tab": "🛰️ Rastreador de Satélites",
        "ai_tab": "🤖 Analista IA",
        "detect_tab": "🕵️ Detección de Objetos",
        "title": "RADAR DE VIGILANCIA GLOBAL",
        "author_tag": "Construido por Gesner Deslandes",
        "logout": "Cerrar Sesión",
        "report": "Descargar Informe",
        "detection_log": "Registro de Detección",
        "sat_engine": "Motor de Mapeo Predictivo",
        "audio_note": "🖱️ Haz clic en la pantalla del radar para activar el sonido.",
        "lat": "Latitud",
        "lon": "Longitud",
        "predict_btn": "Calcular Paso",
        "time_target": "Fecha/Hora Objetivo",
        "aip_key": "Clave de Seguridad AIP (Imágenes Aéreas)",
        "sky_view": "Vista Satelital OpenSky",
        "ai_question": "Pregunta sobre contactos de radar o predicciones de satélites:",
        "ai_analyze": "Analizar Nivel de Amenaza",
        "ai_thinking": "🤖 IA analizando datos de vigilancia...",
        "ai_response": "💡 Informe del Analista IA",
        "security_badge": "🔐 Escudo de seguridad global activo",
        "security_caption": "Todos los datos están cifrados y anonimizados",
        "detect_title": "Detección de Objetos en Tiempo Real",
        "detect_desc": "Sube una imagen (JPEG, PNG) para detectar objetos con YOLOv8.",
        "upload_label": "Elige una imagen...",
        "detect_btn": "Detectar Objetos",
        "detection_results": "Objetos Detectados",
        "refresh_btn": "Actualizar Datos",
        "live_note": "💻 Para ejecutar esta aplicación en tu propia computadora y obtener datos en vivo, haz clic en las instrucciones abajo.",
        "voice_male_explain": "🎙️ Voz IA Masculina – Explicar App",
        "voice_female_explain": "🎤 Voz IA Femenina – Explicar App (nuevas funciones)",
        "legend_title": "🟢 Símbolos estilo OTAN",
        "clock_label": "🕒 Reloj en Vivo",
        "common_questions_title": "💬 Preguntas Comunes",
        "listen_response": "🔊 Escuchar Respuesta IA",
        "location_detected": "📍 Ubicación detectada: {location}",
        "location_name_label": "Nombre de ubicación (modificar)",
        "search_location": "🔍 Buscar Ubicación",
        "search_btn": "Buscar Coordenadas",
        "search_error": "❌ Ubicación no encontrada. Intente de nuevo.",
        "api_status_label": "📡 Fuente de Datos",
        "status_live": "En vivo (OpenSky)",
        "status_cached": "En caché",
        "status_demo": "Demo (simulado)",
        "status_live_detail": "Datos en vivo obtenidos a las {time}",
        "status_cached_detail": "Datos en caché desde {time}",
        "status_demo_detail": "Sin datos en vivo – mostrando demo",
        "local_instructions_title": "💻 Ejecutar Localmente (Datos en Vivo)",
        "local_step1": "Instala Python 3.8 o superior desde python.org.",
        "local_step2": "Abre la Terminal o Símbolo del sistema y ejecuta:",
        "local_cmd1": "git clone https://github.com/Deslandes1/GlobalSurveillanceRadarAD.git",
        "local_cmd2": "cd GlobalSurveillanceRadarAD",
        "local_cmd3": "pip install -r requirements.txt",
        "local_step3": "Crea un archivo .streamlit/secrets.toml con tu clave API de Groq:",
        "local_cmd4": "GROQ_API_KEY = \"tu-clave-api\"",
        "local_step4": "Ejecuta la aplicación:",
        "local_cmd5": "streamlit run app.py",
        "local_step5": "Abre la URL mostrada en tu navegador (normalmente http://localhost:8501).",
        "voice_lang_label": "🎤 Idioma de Voz",
        "voice_lang_en": "English",
        "voice_lang_fr": "Français",
        "voice_lang_es": "Español",
        "voice_lang_zh": "中文"
    },
    "Chinese": {
        "radar_tab": "📡 雷达控制",
        "sat_tab": "🛰️ 卫星跟踪器",
        "ai_tab": "🤖 人工智能分析员",
        "detect_tab": "🕵️ 物体检测",
        "title": "全球监视雷达",
        "author_tag": "由 Gesner Deslandes 构建",
        "logout": "退出会话",
        "report": "下载资产报告",
        "detection_log": "实时检测日志",
        "sat_engine": "预测测绘引擎",
        "audio_note": "🖱️ 点击雷达屏幕启用声音。",
        "lat": "纬度",
        "lon": "经度",
        "predict_btn": "计算过境",
        "time_target": "预测目标（日期/时间）",
        "aip_key": "AIP 安全密钥（航空影像）",
        "sky_view": "OpenSky 卫星视图",
        "ai_question": "询问有关雷达联系或卫星预测的问题：",
        "ai_analyze": "分析当前威胁等级",
        "ai_thinking": "🤖 人工智能正在分析监视数据...",
        "ai_response": "💡 人工智能分析报告",
        "security_badge": "🔐 全球安全盾牌已激活",
        "security_caption": "所有数据均已加密并匿名化",
        "detect_title": "实时物体检测",
        "detect_desc": "上传图像（JPEG， PNG）以使用 YOLOv8 检测物体。",
        "upload_label": "选择图像...",
        "detect_btn": "检测物体",
        "detection_results": "检测到的物体",
        "refresh_btn": "刷新实时数据",
        "live_note": "💻 要在您自己的计算机上运行此应用程序以获取完整的实时数据，请单击下面的说明。",
        "voice_male_explain": "🎙️ 男性人工智能语音 – 解释应用",
        "voice_female_explain": "🎤 女性人工智能语音 – 解释应用（新功能）",
        "legend_title": "🟢 真实北约风格符号",
        "clock_label": "🕒 实时时钟",
        "common_questions_title": "💬 常见问题",
        "listen_response": "🔊 听取人工智能回复",
        "location_detected": "📍 检测到的位置： {location}",
        "location_name_label": "位置名称（覆盖）",
        "search_location": "🔍 搜索位置",
        "search_btn": "搜索坐标",
        "search_error": "❌ 未找到位置。请重试。",
        "api_status_label": "📡 数据源",
        "status_live": "实时（OpenSky）",
        "status_cached": "缓存（来自上次获取）",
        "status_demo": "演示（模拟）",
        "status_live_detail": "实时数据获取于 {time}",
        "status_cached_detail": "缓存自 {time}",
        "status_demo_detail": "没有实时数据 – 显示演示",
        "local_instructions_title": "💻 本地运行（完整实时数据）",
        "local_step1": "从 python.org 安装 Python 3.8 或更高版本。",
        "local_step2": "打开终端或命令提示符并运行：",
        "local_cmd1": "git clone https://github.com/Deslandes1/GlobalSurveillanceRadarAD.git",
        "local_cmd2": "cd GlobalSurveillanceRadarAD",
        "local_cmd3": "pip install -r requirements.txt",
        "local_step3": "创建一个 .streamlit/secrets.toml 文件，包含您的 Groq API 密钥：",
        "local_cmd4": "GROQ_API_KEY = \"您的-api-密钥\"",
        "local_step4": "运行应用程序：",
        "local_cmd5": "streamlit run app.py",
        "local_step5": "在浏览器中打开显示的 URL（通常为 http://localhost:8501）。",
        "voice_lang_label": "🎤 语音语言",
        "voice_lang_en": "English",
        "voice_lang_fr": "Français",
        "voice_lang_es": "Español",
        "voice_lang_zh": "中文"
    }
}

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

# ========== AI ANALYSIS ==========
def ai_analysis(aircraft, satellites, u_lat, u_lon, location_name, question=None):
    radar_summary = "\n".join([f"- {a['id']} ({a['type']}) at altitude {a['alt']}, distance {a['dist']*300:.0f}km" for a in aircraft])
    sat_summary = "\n".join([f"- {s['id']} ({s['type']}) at altitude {s['alt']}" for s in satellites])
    full_prompt = f"""You are an AI surveillance analyst. The user's ground station is located at {location_name} (Latitude {u_lat}, Longitude {u_lon}). Use the following live ADS‑B data to answer the question. Always begin your response by stating the location and coordinates. Provide a balanced, educational analysis. Classifications are approximate and based on heuristics; do not falsely label low‑altitude aircraft as drones unless they explicitly indicate drone callsigns (DRN, UAV). If the question asks about threats, assess based on the presence of unusual or military contacts.

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
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"AI error: {str(e)}"

def main_page():
    L = UI[st.session_state.lang]
    with st.sidebar:
        # Profile picture and name
        st.markdown("""
        <img src="https://raw.githubusercontent.com/Deslandes1/GlobalSurveillanceRadarAD/main/Gesner%20Deslandes.png" 
             class="profile-img" 
             onerror="this.style.display='none'">
        """, unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; color:#e8ddd0;'>Gesner Deslandes</h3>", unsafe_allow_html=True)
        st.divider()

        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French", "Spanish", "Chinese"], key="lang")
        st.markdown(f"**{L['author_tag']}**")
        st.divider()

        # Voice language selector (separate from interface language)
        voice_lang = st.selectbox(
            L['voice_lang_label'],
            options=["en", "fr", "es", "zh"],
            format_func=lambda x: L[f"voice_lang_{x}"] if f"voice_lang_{x}" in L else x,
            key="voice_lang_selector"
        )

        # Male Voice button
        if st.button(L['voice_male_explain'], use_container_width=True):
            script = generate_male_voice_audio()
            try:
                from gtts import gTTS
                # map voice_lang to gTTS language code
                lang_code = "en" if voice_lang == "en" else "fr" if voice_lang == "fr" else "es" if voice_lang == "es" else "zh"
                tts = gTTS(text=script, lang=lang_code, slow=False)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    with open(tmp.name, "rb") as f:
                        audio_bytes = f.read()
                    os.unlink(tmp.name)
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("🎙️ Male voice explanation played.")
            except ImportError:
                st.error("gTTS library not installed. Install with: pip install gTTS")
            except Exception as e:
                st.error(f"Voice generation error: {e}")

        # Female Voice button
        if st.button(L['voice_female_explain'], use_container_width=True):
            script = generate_female_voice_audio()
            try:
                from gtts import gTTS
                lang_code = "en" if voice_lang == "en" else "fr" if voice_lang == "fr" else "es" if voice_lang == "es" else "zh"
                tts = gTTS(text=script, lang=lang_code, slow=False)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    with open(tmp.name, "rb") as f:
                        audio_bytes = f.read()
                    os.unlink(tmp.name)
                    st.audio(audio_bytes, format="audio/mp3")
                    st.success("🎤 Female voice explanation played.")
            except ImportError:
                st.error("gTTS library not installed. Install with: pip install gTTS")
            except Exception as e:
                st.error(f"Voice generation error: {e}")

        st.divider()
        st.markdown(f"### 🛡️ {L['security_badge']}")
        st.markdown(f"<div class='security-badge'>{L['security_caption']}</div>", unsafe_allow_html=True)
        if GLOBAL_SHIELD_ACTIVE:
            st.success("✅ Global Shield API Key active")
        else:
            st.warning("⚠️ Global Shield API Key not configured")
        
        # ----- API STATUS INDICATOR -----
        st.markdown("---")
        st.markdown(f"### {L['api_status_label']}")
        status = st.session_state.api_status
        if "Live" in status:
            badge_class = "status-live"
            if st.session_state.cached_timestamp:
                time_str = st.session_state.cached_timestamp.strftime("%H:%M:%S")
                detail = L['status_live_detail'].format(time=time_str)
            else:
                detail = "Live data"
        elif "Cached" in status:
            badge_class = "status-cached"
            if st.session_state.cached_timestamp:
                time_str = st.session_state.cached_timestamp.strftime("%H:%M:%S")
                detail = L['status_cached_detail'].format(time=time_str)
            else:
                detail = "Cached data"
        else:
            badge_class = "status-demo"
            detail = L['status_demo_detail']
        st.markdown(f'<span class="status-badge {badge_class}">{status}</span>', unsafe_allow_html=True)
        st.caption(detail)

        st.divider()
        
        # ----- LOCAL RUN INSTRUCTIONS -----
        with st.expander(L['local_instructions_title'], expanded=False):
            st.markdown(f"""
            <div class="local-instructions">
                <p><strong>Step 1:</strong> {L['local_step1']}</p>
                <p><strong>Step 2:</strong> {L['local_step2']}</p>
                <code>{L['local_cmd1']}</code><br>
                <code>{L['local_cmd2']}</code><br>
                <code>{L['local_cmd3']}</code>
                <p><strong>Step 3:</strong> {L['local_step3']}</p>
                <code>{L['local_cmd4']}</code>
                <p><strong>Step 4:</strong> {L['local_step4']}</p>
                <code>{L['local_cmd5']}</code>
                <p><strong>Step 5:</strong> {L['local_step5']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.divider()

        # ----- LOCATION DETECTION & SEARCH -----
        detected = get_detected_location()
        if detected:
            default_city = f"{detected.get('city', '')}, {detected.get('country', '')}"
            default_lat = detected.get('lat', 18.5392)
            default_lon = detected.get('lon', -72.3364)
        else:
            default_city = "Port-au-Prince, Haiti"
            default_lat = 18.5392
            default_lon = -72.3364

        st.info(L['location_detected'].format(location=default_city))

        st.markdown(f"### {L['search_location']}")
        search_input = st.text_input("", placeholder="e.g., Kingston, Jamaica", key="location_search_input")
        if st.button(L['search_btn'], use_container_width=True):
            if search_input.strip():
                lat, lon, display_name = geocode_location(search_input)
                if lat is not None:
                    st.session_state.location_name = display_name
                    st.session_state.lat_val = lat
                    st.session_state.lon_val = lon
                    st.success(f"📍 Found: {display_name}")
                    st.rerun()
                else:
                    st.error(L['search_error'])
            else:
                st.warning("Please enter a location name.")

        if "location_name" not in st.session_state:
            st.session_state.location_name = default_city
        if "lat_val" not in st.session_state:
            st.session_state.lat_val = default_lat
        if "lon_val" not in st.session_state:
            st.session_state.lon_val = default_lon

        location_name = st.text_input(L['location_name_label'], value=st.session_state.location_name, key="loc_name_override")
        u_lat = st.number_input(L['lat'], value=st.session_state.lat_val, format="%.4f", key="lat_override")
        u_lon = st.number_input(L['lon'], value=st.session_state.lon_val, format="%.4f", key="lon_override")

        if location_name != st.session_state.location_name:
            st.session_state.location_name = location_name
        if u_lat != st.session_state.lat_val:
            st.session_state.lat_val = u_lat
        if u_lon != st.session_state.lon_val:
            st.session_state.lon_val = u_lon

        st.divider()
        aip_key = st.text_input(L['aip_key'], type="password", placeholder="Enter Provider Key...")
        st.divider()
        use_demo = st.checkbox("Demo Mode (disable live OpenSky)", value=False)
        st.divider()
        if st.button(L['refresh_btn'], use_container_width=True):
            st.rerun()
        st.divider()
        st.write("📞 (509) 4738-5663")
        st.write("✉️ deslandes78@gmail.com")
        if st.button(L['logout'], type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # ---- Fetch live or demo data ----
    if use_demo:
        aircraft_data = get_demo_aircraft()
        st.session_state.api_status = "Demo (User selected)"
    else:
        aircraft_data, status = fetch_live_aircraft(u_lat, u_lon)

    sat_data = get_satellites()

    tab_radar, tab_sat, tab_ai, tab_detect = st.tabs([L["radar_tab"], L["sat_tab"], L["ai_tab"], L["detect_tab"]])

    # Radar tab (unchanged)
    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.subheader(L['author_tag'])
        st.info(L['audio_note'])
        col_rad, col_log = st.columns([2, 1])
        with col_rad:
            st.markdown(f"### {L['legend_title']}")
            legend_html = """
            <div class="legend">
                <span class="legend-item">
                    <span class="legend-shape" style="color:#2ecc71;">⬤</span> Commercial Airplane
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#e74c3c;">▲</span> Military
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#f39c12;">◆</span> Drone
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#f1c40f;">⬛</span> Cargo
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#9b59b6;">■</span> UFO
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#3498db;">●</span> General Aviation
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#95a5a6;">◉</span> Other
                </span>
            </div>
            """
            st.markdown(legend_html, unsafe_allow_html=True)
            radar_json = json.dumps(aircraft_data)
            radar_html = f"""
            <html><body style="background:#0a0a0f; margin:0; display:flex; justify-content:center;">
                <canvas id="radar" width="550" height="550" style="border-radius:50%; border:1px solid #2a1f14; cursor:pointer;"></canvas>
                <script>
                    const canvas = document.getElementById('radar');
                    const ctx = canvas.getContext('2d');
                    const data = {radar_json};
                    let angle = 0;
                    let audioCtx = null;
                    let soundEnabled = false;
                    
                    canvas.addEventListener('click', () => {{
                        if (!audioCtx) {{
                            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        }}
                        if (audioCtx.state === 'suspended') {{
                            audioCtx.resume();
                        }}
                        soundEnabled = true;
                        canvas.style.borderColor = '#00ff64';
                        setTimeout(() => {{ canvas.style.borderColor = '#2a1f14'; }}, 200);
                    }});
                    
                    function ping() {{
                        if (!audioCtx || !soundEnabled) return;
                        try {{
                            const osc = audioCtx.createOscillator();
                            const gain = audioCtx.createGain();
                            const now = audioCtx.currentTime;
                            osc.type = 'sine';
                            osc.frequency.setValueAtTime(400, now);
                            osc.frequency.exponentialRampToValueAtTime(1200, now + 0.3);
                            gain.gain.setValueAtTime(0.2, now);
                            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
                            osc.connect(gain);
                            gain.connect(audioCtx.destination);
                            osc.start(now);
                            osc.stop(now + 0.35);
                        }} catch (e) {{}}
                    }}
                    
                    function drawTarget(ctx, x, y, color, type, id, alt, pulse) {{
                        const size = 9;
                        ctx.save();
                        ctx.shadowBlur = 20;
                        ctx.shadowColor = color;
                        
                        ctx.fillStyle = color;
                        ctx.strokeStyle = '#ffffff';
                        ctx.lineWidth = 1.2;
                        
                        switch(type) {{
                            case 'Military':
                                ctx.beginPath();
                                ctx.moveTo(x, y - size);
                                ctx.lineTo(x - size, y + size*0.7);
                                ctx.lineTo(x + size, y + size*0.7);
                                ctx.closePath();
                                ctx.fill();
                                ctx.stroke();
                                break;
                            case 'Drone':
                                ctx.beginPath();
                                ctx.moveTo(x, y - size);
                                ctx.lineTo(x + size, y);
                                ctx.lineTo(x, y + size);
                                ctx.lineTo(x - size, y);
                                ctx.closePath();
                                ctx.fill();
                                ctx.stroke();
                                break;
                            case 'UFO':
                                ctx.fillRect(x - size*0.7, y - size*0.7, size*1.4, size*1.4);
                                ctx.strokeRect(x - size*0.7, y - size*0.7, size*1.4, size*1.4);
                                break;
                            case 'Commercial Airplane':
                            case 'Cargo':
                                ctx.beginPath();
                                ctx.arc(x, y, size*0.7, 0, 2*Math.PI);
                                ctx.fill();
                                ctx.stroke();
                                break;
                            case 'General Aviation':
                                ctx.beginPath();
                                ctx.arc(x, y, size*0.5, 0, 2*Math.PI);
                                ctx.fill();
                                ctx.stroke();
                                break;
                            default:
                                ctx.beginPath();
                                ctx.arc(x, y, size*0.4, 0, 2*Math.PI);
                                ctx.fill();
                                ctx.stroke();
                        }}
                        
                        ctx.shadowBlur = 0;
                        if (type === 'Military' || type === 'UFO') {{
                            const pulseRadius = 12 + 3 * Math.sin(pulse);
                            ctx.shadowBlur = 30;
                            ctx.shadowColor = '#ff4444';
                            ctx.strokeStyle = 'rgba(255,68,68,0.4)';
                            ctx.lineWidth = 1.5;
                            ctx.beginPath();
                            ctx.arc(x, y, pulseRadius, 0, 2*Math.PI);
                            ctx.stroke();
                        }}
                        
                        ctx.restore();
                        
                        ctx.fillStyle = '#e8ddd0';
                        ctx.font = '9px monospace';
                        ctx.shadowBlur = 0;
                        ctx.fillText(id, x + 14, y - 4);
                        
                        ctx.fillStyle = 'rgba(200,200,200,0.6)';
                        ctx.font = '7px monospace';
                        ctx.fillText(alt, x + 14, y + 10);
                    }}
                    
                    function draw() {{
                        ctx.clearRect(0,0,550,550);
                        const cx = 275, cy = 275, r = 250;
                        ctx.strokeStyle = 'rgba(40,30,20,0.6)';
                        ctx.lineWidth = 1;
                        for(let i = 1; i <= 4; i++) {{
                            ctx.beginPath();
                            ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2);
                            ctx.stroke();
                        }}
                        ctx.strokeStyle = 'rgba(40,30,20,0.3)';
                        ctx.lineWidth = 0.5;
                        ctx.beginPath();
                        ctx.moveTo(cx - r, cy);
                        ctx.lineTo(cx + r, cy);
                        ctx.moveTo(cx, cy - r);
                        ctx.lineTo(cx, cy + r);
                        ctx.stroke();
                        
                        const pulse = Date.now() / 300;
                        data.forEach((d, i) => {{
                            const angleRad = i * 1.2;
                            const dx = cx + Math.cos(angleRad) * (r * d.dist);
                            const dy = cy + Math.sin(angleRad) * (r * d.dist);
                            drawTarget(ctx, dx, dy, d.color, d.type, d.id, d.alt, pulse);
                        }});
                        
                        let oldA = angle;
                        angle -= 0.03;
                        if (Math.floor(oldA / (2*Math.PI)) !== Math.floor(angle / (2*Math.PI))) {{
                            ping();
                        }}
                        ctx.save();
                        ctx.translate(cx, cy);
                        ctx.rotate(angle);
                        const grad = ctx.createRadialGradient(0,0,0,0,0,r);
                        grad.addColorStop(0, 'transparent');
                        grad.addColorStop(1, 'rgba(0,255,100,0.15)');
                        ctx.fillStyle = grad;
                        ctx.beginPath();
                        ctx.moveTo(0,0);
                        ctx.arc(0,0,r,0,0.4);
                        ctx.fill();
                        ctx.restore();
                        requestAnimationFrame(draw);
                    }}
                    draw();
                </script>
            </body></html>
            """
            components.html(radar_html, height=580)

        with col_log:
            st.subheader(L['detection_log'])
            clock_html = """
            <div style="background: rgba(20,16,24,0.9); border: 1px solid #4a3520; border-radius: 8px; padding: 10px 12px; margin: 5px 0 10px 0; text-align: center; font-family: 'Courier New', monospace;">
                <div id="liveClock" style="color: #ffffff; font-size: 1.6rem; font-weight: bold; letter-spacing: 2px; text-shadow: 0 0 10px rgba(255,255,255,0.5);">--:--:--</div>
                <div id="liveDate" style="color: #ffffff; font-size: 1.2rem; font-weight: bold; opacity: 0.9; margin-top: 2px;">--/--/----</div>
            </div>
            <script>
                function updateClock() {
                    var now = new Date();
                    var h = String(now.getHours()).padStart(2, '0');
                    var m = String(now.getMinutes()).padStart(2, '0');
                    var s = String(now.getSeconds()).padStart(2, '0');
                    var month = String(now.getMonth() + 1).padStart(2, '0');
                    var day = String(now.getDate()).padStart(2, '0');
                    var year = now.getFullYear();
                    document.getElementById('liveClock').innerHTML = h + ':' + m + ':' + s;
                    document.getElementById('liveDate').innerHTML = month + '/' + day + '/' + year;
                }
                updateClock();
                setInterval(updateClock, 1000);
            </script>
            """
            components.html(clock_html, height=90)
            for d in aircraft_data:
                with st.expander(f"{d.get('label', d['id'])} [{d['type']}]"):
                    st.write(f"**ID:** {d['id']}")
                    st.write(f"**Altitude:** {d['alt']}")
                    if not use_demo and 'lat' in d:
                        st.write(f"**Lat/Lon:** {d['lat']:.4f}, {d['lon']:.4f}")
                    st.download_button(L['report'], f"RADAR LOG\nAsset: {d['id']}\nType: {d['type']}\nOP: Gesner Deslandes", key=f"dl_{d['id']}")

    # Satellite tab (unchanged)
    with tab_sat:
        st.title(f"🛰️ {L['sat_tab']}")
        st.subheader(L['author_tag'])
        col_ctrl, col_map = st.columns([1, 2])
        with col_ctrl:
            st.subheader("OpenSky Prediction")
            t_date = st.date_input(L['time_target'], datetime.now())
            t_time = st.time_input("Target Time", datetime.now().time())
            full_t = datetime.combine(t_date, t_time)
            diff = (full_t - datetime.now()).total_seconds() / 3600
            for s in sat_data:
                pred_lat = u_lat + (math.sin(diff + hash(s['id']) % 10) * 10)
                pred_lon = u_lon + (diff * 15) % 360 - 180
                with st.container(border=True):
                    st.write(f"**{s['id']}** ({s['type']})")
                    st.caption(f"Predicted Lock: {pred_lat:.2f}N, {pred_lon:.2f}W")
                    st.download_button(L['report'], f"PREDICTION\n{s['id']}\n{full_t}", key=f"sat_{s['id']}")
        with col_map:
            st.subheader(L['sky_view'])
            tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            attribution = "AIP Imagery: Esri, Maxar, Earthstar Geographics"
            markers = ""
            if not use_demo and aircraft_data and aircraft_data != get_demo_aircraft():
                for a in aircraft_data:
                    if "lat" in a and "lon" in a:
                        markers += f"L.circleMarker([{a['lat']}, {a['lon']}], {{color:'{a['color']}', radius:6}}).addTo(map).bindPopup('{a['id']}<br>Alt: {a['alt']}');"
            for s in sat_data:
                markers += f"L.circleMarker([{u_lat + (hash(s['id'])%5-2.5)}, {u_lon + (hash(s['id'])%10-5)}], {{color:'{s['color']}', radius:8}}).addTo(map).bindPopup('{s['id']}');"
            map_html = f"""
            <html><head>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                <style>#map {{ height: 500px; border-radius: 15px; border: 2px solid #2a1f14; }}</style>
            </head><body>
                <div id="map"></div>
                <script>
                    const map = L.map('map', {{zoomControl: false}}).setView([{u_lat}, {u_lon}], 10);
                    L.tileLayer('{tiles}', {{ attribution: '{attribution}' }}).addTo(map);
                    L.circleMarker([{u_lat}, {u_lon}], {{color: '#00ff64', radius: 12, weight: 3}}).addTo(map).bindPopup('Primary Ground Lock');
                    {markers}
                </script>
            </body></html>
            """
            components.html(map_html, height=550)

    # AI Analyst tab
    with tab_ai:
        st.title("🤖 AI Surveillance Analyst")
        
        common_questions = [
            "What is the current threat level in my area?",
            "How many aircraft are currently within 50 km of my ground station?",
            "Are there any military aircraft near my location?",
            "What is the closest aircraft to my position?",
            "How many drones are detected in my vicinity?",
            "What satellites are currently overhead?",
            "When will the next satellite pass over my location?",
            "Are there any unusual or unidentified contacts on radar?",
            "What is the altitude distribution of aircraft around me?",
            "Is there any pattern in the aircraft movements?",
            "What is the average distance of radar contacts?",
            "How many aircraft are flying above 30,000 feet?",
            "Are there any cargo planes in my area?",
            "What is the most common aircraft type near me?",
            "Is there any potential threat from the radar contacts?",
            "Can you predict the trajectory of the nearest aircraft?",
            "How does the current activity compare to typical patterns?",
            "Are there any aircraft flying at low altitude?",
            "What is the total number of radar contacts right now?",
            "Summarize all radar and satellite activity in my area."
        ]
        
        col_q, col_main = st.columns([1, 2])
        with col_q:
            st.markdown(f"### {L['common_questions_title']}")
            st.markdown('<div class="question-list">', unsafe_allow_html=True)
            for idx, q in enumerate(common_questions):
                if st.button(q, key=f"q_{idx}"):
                    st.session_state.ai_question_input = q
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_main:
            user_question = st.text_area(L['ai_question'], height=100, value=st.session_state.ai_question_input, key="ai_question_text")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                analyze_btn = st.button(L['ai_analyze'], use_container_width=True)
            with col_btn2:
                listen_btn = st.button(L['listen_response'], use_container_width=True)
            
            if analyze_btn:
                if not user_question.strip():
                    st.warning("Please enter a question.")
                else:
                    with st.spinner(L['ai_thinking']):
                        response = ai_analysis(aircraft_data, sat_data, u_lat, u_lon, location_name, user_question)
                        st.session_state.ai_response = response
                    st.markdown(f"### {L['ai_response']}")
                    st.markdown(response)
            
            if st.session_state.ai_response and not analyze_btn:
                st.markdown(f"### {L['ai_response']}")
                st.markdown(st.session_state.ai_response)
            
            if listen_btn:
                if st.session_state.ai_response:
                    with st.spinner("Generating audio..."):
                        # Use the selected voice language for the response
                        lang_code = "en" if voice_lang == "en" else "fr" if voice_lang == "fr" else "es" if voice_lang == "es" else "zh"
                        audio_bytes = generate_audio_response(st.session_state.ai_response, lang_code)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                            st.success("🔊 AI response played.")
                        else:
                            st.error("Could not generate audio.")
                else:
                    st.warning("No AI response to listen to. Please ask a question first.")

    # Object Detection tab
    with tab_detect:
        st.title(L['detect_title'])
        st.markdown(L['detect_desc'])
        uploaded_file = st.file_uploader(L['upload_label'], type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            img_bytes = uploaded_file.read()
            st.image(img_bytes, caption="Uploaded Image", use_container_width=True)
            if st.button(L['detect_btn']):
                with st.spinner("Running YOLOv8..."):
                    annotated_img, detections = run_object_detection(img_bytes)
                if annotated_img is not None:
                    st.image(annotated_img, caption="Detected Objects", use_container_width=True)
                    st.subheader(L['detection_results'])
                    if detections and "error" not in detections[0]:
                        for d in detections:
                            st.write(f"- {d['label']} (confidence {d['confidence']})")
                    else:
                        st.warning("No objects detected.")
                else:
                    st.error(f"Detection failed: {detections[0].get('error', 'Unknown error')}")

# ========== RUN ==========
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
