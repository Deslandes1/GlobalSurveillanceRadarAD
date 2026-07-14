import streamlit as st
import json
import random
import math
import requests
import time
import base64
import os
import tempfile
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from groq import Groq
import pandas as pd
import re
import pytz

# ========== SATELLITE TRACKING WITH REAL TLE DATA ==========
try:
    from skyfield.api import load, EarthSatellite
    from skyfield.timelib import Time
    SKYFIELD_AVAILABLE = True
except ImportError:
    SKYFIELD_AVAILABLE = False

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance Portal – Haiti & DR",
    layout="wide",
    page_icon="🌐"
)

# ========== CUSTOM CSS – LEOPARD BLACK THEME + BRIGHT WHITE TEXT ==========
st.markdown("""
<style>
    .stApp {
        background: #0a0a0f;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(60, 40, 20, 0.15) 0%, transparent 25%),
            radial-gradient(circle at 70% 60%, rgba(60, 40, 20, 0.10) 0%, transparent 35%),
            radial-gradient(circle at 40% 80%, rgba(80, 50, 25, 0.12) 0%, transparent 30%),
            radial-gradient(circle at 85% 20%, rgba(40, 30, 15, 0.08) 0%, transparent 40%);
        color: #ffffff;
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
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    div[data-baseweb="select"] ul {
        background-color: #1a1a2e !important;
    }
    div[data-baseweb="select"] ul li {
        color: #ffffff !important;
        background-color: #1a1a2e !important;
    }
    div[data-baseweb="select"] ul li:hover {
        background-color: #2a1f14 !important;
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
    .login-container h2, .login-container p {
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, p, li, .stMarkdown, .stCaption, label, .stTextInput, .stSelectbox, .stTextArea, .stButton, .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        color: #ffffff !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1a120a, #2a1f14) !important;
        color: #ffffff !important;
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
        color: #ffffff !important;
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
        color: #ffffff !important;
    }
    .stMetric .stMetricValue {
        color: #ffffff !important;
    }
    .streamlit-expanderHeader {
        background: rgba(20, 16, 24, 0.6) !important;
        border: 1px solid #1f1610 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
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
        color: #ffffff;
        border: 1px solid #3d2a18;
    }
    .security-badge {
        background: rgba(20, 16, 24, 0.8);
        border: 1px solid #3d2a18;
        border-radius: 30px;
        padding: 8px 15px;
        text-align: center;
        color: #ffffff;
        font-weight: bold;
        font-family: monospace;
    }
    hr {
        border-color: #1f1610 !important;
    }
    .stAlert {
        background: rgba(20, 16, 24, 0.6) !important;
        border: 1px solid #2a1f14 !important;
        color: #ffffff !important;
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
        color: #ffffff;
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
        color: #ffffff;
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
        color: #ffffff;
    }
    .local-instructions code {
        background: rgba(255,255,255,0.1);
        padding: 2px 6px;
        border-radius: 4px;
        color: #00ff64;
        font-size: 0.8rem;
    }
    iframe {
        background-color: #0a0a0f !important;
        border: 1px solid #2a1f14 !important;
        border-radius: 10px !important;
    }
    .flight-tracker-container {
        background: rgba(10, 10, 15, 0.9);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #2a1f14;
    }
    .main-title h1 {
        color: #ffffff !important;
    }
    .main-title p {
        color: #ffffff !important;
    }
    .chat-message {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
        color: #ffffff !important;
    }
    .email-log {
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid #4a3520;
        padding: 10px;
        margin: 5px 0;
        font-family: monospace;
        font-size: 0.9rem;
        color: #ffffff !important;
    }
    .warning-box {
        background: rgba(255, 193, 7, 0.15);
        border-left: 4px solid #ffc107;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: #ffffff !important;
    }
    .stInfo, .stSuccess, .stWarning, .stError {
        color: #ffffff !important;
    }
    .stSelectbox label, .stTextInput label, .stTextArea label, .stNumberInput label, .stDateInput label, .stTimeInput label {
        color: #ffffff !important;
    }
    .stMarkdown a {
        color: #00bfff !important;
    }
    .stMarkdown a:hover {
        color: #87ceeb !important;
    }
    .stDownloadButton button {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== AI VOICE SCRIPTS ==========
def generate_male_voice_audio():
    script = """
    Welcome to the Global Surveillance Radar Portal, now covering Haiti and the Dominican Republic airspace and the Caribbean Sea. Built by Gesner Deslandes at GlobalInternet.py.
    
    This application features six main modules: Radar Control, Satellite Tracker, AI Analyst, Flight Tracker, Maritime Detection, and Live World Cup.
    
    The Radar Control tab shows a 360-degree live radar display. Aircraft are automatically classified with military-style symbols: red triangles for military, purple squares for UFOs, orange diamonds for drones, green for commercial, and blue for general aviation. Ships appear as squares with colors indicating military (red) or cargo (yellow) vessels.
    
    The Maritime Detection tab lists all vessels within range, including military ships and cargo vessels in the Caribbean.
    
    The Satellite Tracker predicts satellite passes and shows an interactive map with aircraft, ships, and satellite overlays.
    
    The AI Analyst is powered by Groq's Llama 3.1. Ask about radar contacts, satellite predictions, or maritime threats.
    
    The Flight Tracker tab provides real-time flight delay information powered by FlightAware.
    
    The Live World Cup tab features an embedded free live stream from a third-party provider.
    
    GlobalInternet.py – connecting the global market with local expertise.
    """
    return script

def generate_female_voice_audio():
    script = """
    Welcome to the Global Surveillance Radar Portal, now covering Haiti and the Dominican Republic airspace and the Caribbean Sea. Built by Gesner Deslandes at GlobalInternet.py.
    
    This advanced surveillance system features a live radar with a classic fetching sound. Click the radar screen to enable the audio, and you will hear a sonar ping on every sweep.
    
    Objects are automatically classified and displayed with real military-style symbols. Military targets appear as red triangles, unknown or UFO contacts as purple squares, drones as orange diamonds, civilian aircraft as green or blue circles, and ships as squares.
    
    The Maritime Detection tab provides real-time information on vessels in Caribbean waters, including military ships, cargo, and tankers.
    
    The Satellite Tracker tab predicts satellite passes and shows an interactive map.
    
    The AI Analyst tab uses Groq's Llama 3.1 to answer your questions.
    
    The Flight Tracker tab displays real-time flight delay information from FlightAware.
    
    The Live World Cup tab features an embedded free live stream.
    
    GlobalInternet.py – connecting the global market with local expertise.
    """
    return script

# ========== AUDIO GENERATION ==========
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

# ========== SUPABASE (optional) ==========
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

# ========== SATELLITE CACHE ==========
if "satellite_tle_cache" not in st.session_state:
    st.session_state.satellite_tle_cache = None
if "satellite_cache_time" not in st.session_state:
    st.session_state.satellite_cache_time = None
if "satellite_positions" not in st.session_state:
    st.session_state.satellite_positions = None
if "satellite_error" not in st.session_state:
    st.session_state.satellite_error = False

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

# ========== AIRCRAFT CLASSIFICATION ==========
def classify_aircraft(alt_ft, callsign=""):
    alt_ft = int(alt_ft.replace(",","").replace("ft","").strip()) if isinstance(alt_ft, str) else alt_ft
    if not isinstance(alt_ft, (int, float)):
        alt_ft = 0

    callsign = str(callsign).upper()

    drone_keywords = ["UAV", "DRN", "DRONE", "QUAD", "HEX", "OCTO", "RQ", "MQ", 
                      "EAGLE", "SHADOW", "PREDATOR", "REAPER", "GLOBAL", "HAWK", "PHANTOM"]
    if any(keyword in callsign for keyword in drone_keywords):
        if alt_ft < 1000:
            return "Low Altitude Drone", "#ff6b35", "🛸 Drone (Low)"
        elif alt_ft > 15000:
            return "High Altitude Drone", "#ff00ff", "🛸 Drone (High)"
        else:
            return "Drone", "#ff9900", "🛸 Drone"

    military_prefixes = ["F-", "B-", "C-", "E-", "KC-", "T-", "V-", "A-", "AH-", "CH-", "UH-", "B-2"]
    if any(callsign.startswith(pre) for pre in military_prefixes) or alt_ft > 40000:
        return "Military", "#e74c3c", "✈️ Military"

    airline_codes = ["AAL", "UAL", "SWA", "DAL", "NKS", "JBU", "FFT", "EJA", "LXJ", "N456", "N123", "TAM", "LATAM", "GOL", "AZU", "VRG"]
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

# ========== LIVE AIRCRAFT FETCH ==========
def fetch_live_aircraft(ground_lat, ground_lon):
    max_range = st.session_state.get("max_range", 500)  # increased default to 500 km
    haiti_tz = pytz.timezone('America/Port-au-Prince')
    
    if st.session_state.cached_aircraft_data and st.session_state.cached_timestamp:
        age = (datetime.now() - st.session_state.cached_timestamp).total_seconds()
        if age < 60:
            st.session_state.api_status = "Cached (recent)"
            return st.session_state.cached_aircraft_data, "cached"
    
    url = "https://opensky-network.org/api/states/all"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SurveillancePortal/1.0)"}
    
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                states = data.get("states", [])
                if not states:
                    st.session_state.api_status = "Live (No aircraft detected)"
                    if st.session_state.cached_aircraft_data:
                        return st.session_state.cached_aircraft_data, "cached"
                    time.sleep(0.5)
                    continue
                
                aircraft_list = []
                now_str = datetime.now(haiti_tz).strftime("%Y-%m-%d %I:%M:%S %p")
                for s in states:
                    lat = s[6]
                    lon = s[5]
                    if lat is None or lon is None:
                        continue
                    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                        continue
                    R = 6371
                    dlat = math.radians(lat - ground_lat)
                    dlon = math.radians(lon - ground_lon)
                    a = math.sin(dlat/2)**2 + math.cos(math.radians(ground_lat)) * math.cos(math.radians(lat)) * math.sin(dlon/2)**2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                    dist_km = R * c
                    if dist_km > max_range:
                        continue
                    alt = s[7] if s[7] is not None else 0
                    if alt < -1000 or alt > 60000:
                        continue
                    callsign = s[1].strip() if s[1] else s[0][:6].upper()
                    if not callsign or len(callsign) < 2:
                        continue
                    if callsign in ["N/A", "UNKNOWN", "-----", "0", "NA"]:
                        continue
                    cat, color, label = classify_aircraft(alt, callsign)
                    aircraft_list.append({
                        "id": callsign,
                        "type": cat,
                        "color": color,
                        "label": label,
                        "alt": f"{int(alt) if alt else 'N/A'}ft",
                        "dist": min(dist_km / max_range, 0.95),
                        "distance_km": round(dist_km, 1),
                        "lat": lat,
                        "lon": lon,
                        "verified": False,
                        "detected_at": now_str
                    })
                
                if aircraft_list:
                    aircraft_list = sorted(aircraft_list, key=lambda x: x["distance_km"])[:20]
                    st.session_state.cached_aircraft_data = aircraft_list
                    st.session_state.cached_timestamp = datetime.now()
                    st.session_state.api_status = "Live"
                    return aircraft_list, "live"
                else:
                    st.session_state.api_status = "Live (No aircraft within range)"
                    return st.session_state.cached_aircraft_data or [], "cached"
            elif response.status_code == 429:
                wait = (2 ** attempt) * 0.5
                time.sleep(wait)
                continue
            else:
                time.sleep(0.5)
                continue
        except Exception:
            time.sleep(0.5)
            continue
    
    if st.session_state.cached_aircraft_data:
        st.session_state.api_status = "Cached (Live unavailable – retrying)"
        return st.session_state.cached_aircraft_data, "cached"
    else:
        st.session_state.api_status = "Demo (No cached data – waiting for signal)"
        demo = get_demo_aircraft()
        return demo, "demo"

def get_demo_aircraft():
    haiti_tz = pytz.timezone('America/Port-au-Prince')
    now_str = datetime.now(haiti_tz).strftime("%Y-%m-%d %I:%M:%S %p")
    return [
        {"id": "HAI001", "type": "Commercial Airplane", "color": "#2ecc71", "label": "🛩️ Commercial", "alt": "32,000ft", "dist": 0.3, "distance_km": 120, "detected_at": now_str},
        {"id": "DR-DRONE", "type": "Drone", "color": "#ff9900", "label": "🛸 Drone", "alt": "1,200ft", "dist": 0.2, "distance_km": 80, "detected_at": now_str},
        {"id": "N1234A", "type": "General Aviation", "color": "#3498db", "label": "🛩️ General", "alt": "5,000ft", "dist": 0.4, "distance_km": 160, "detected_at": now_str}
    ]

# ========== MARITIME DETECTION – AISSTREAM WITH CARIBBEAN BOUNDING BOX ==========

def parse_aisstream_vessels(vessels_data, ground_lat, ground_lon):
    """Parse vessels from aisstream.io response into unified format"""
    max_range = st.session_state.get("max_range", 500)
    haiti_tz = pytz.timezone('America/Port-au-Prince')
    now_str = datetime.now(haiti_tz).strftime("%Y-%m-%d %I:%M:%S %p")
    vessels = []
    
    for v in vessels_data:
        lat = v.get("latitude")
        lon = v.get("longitude")
        if lat is None or lon is None:
            continue
        
        # Distance
        R = 6371
        dlat = math.radians(lat - ground_lat)
        dlon = math.radians(lon - ground_lon)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(ground_lat)) * math.cos(math.radians(lat)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        dist_km = R * c
        if dist_km > max_range:
            continue
        
        # Type classification
        ship_type = v.get("shipType", "Unknown")
        ship_type_lower = str(ship_type).lower()
        mmsi = str(v.get("mmsi", ""))
        
        if 'military' in ship_type_lower or 'navy' in ship_type_lower or 'warship' in ship_type_lower:
            vessel_type = "Military Ship"; color = "#e74c3c"; label = "⚓ Military Ship"
        elif 'tanker' in ship_type_lower or 'oil' in ship_type_lower:
            vessel_type = "Tanker"; color = "#00bfff"; label = "⛽ Tanker"
        elif 'cargo' in ship_type_lower or 'container' in ship_type_lower or 'freight' in ship_type_lower:
            vessel_type = "Cargo Ship"; color = "#f1c40f"; label = "🚢 Cargo"
        elif 'fishing' in ship_type_lower:
            vessel_type = "Fishing Vessel"; color = "#2ecc71"; label = "🎣 Fishing"
        elif 'passenger' in ship_type_lower or 'cruise' in ship_type_lower:
            vessel_type = "Passenger Ship"; color = "#9b59b6"; label = "🛳️ Passenger"
        else:
            vessel_type = "Other Vessel"; color = "#95a5a6"; label = "🚢 Other"
        
        vessels.append({
            "id": v.get("callsign", str(v.get("mmsi", "Unknown"))),
            "type": vessel_type,
            "color": color,
            "label": label,
            "alt": "0ft",
            "dist": min(dist_km / max_range, 0.95),
            "distance_km": round(dist_km, 1),
            "lat": lat,
            "lon": lon,
            "verified": True,
            "detected_at": now_str
        })
    return vessels

def fetch_live_ships(ground_lat, ground_lon):
    """
    Fetch real vessel data from aisstream.io using the provided API key.
    Key hardcoded as fallback; can also be set in secrets as AISSTREAM_API_KEY.
    """
    ais_key = st.secrets.get("AISSTREAM_API_KEY")
    if not ais_key:
        ais_key = "e8622757a267cc06fb9ad0126d52ad519d784039"  # fallback, replace with your own
    
    if not ais_key:
        st.warning("⚠️ No AISStream API key found. Using demo ship data.")
        return get_demo_ships()
    
    # Caribbean bounding box covering Haiti and DR: lon min, lat min, lon max, lat max
    url = "https://api.aisstream.io/v1/vessels"
    headers = {"X-API-Key": ais_key}
    params = {"bbox": "-75,17,-68,20"}  # covers Hispaniola and surrounding waters
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            vessels = data.get("vessels", [])
            if vessels:
                parsed = parse_aisstream_vessels(vessels, ground_lat, ground_lon)
                if parsed:
                    st.success(f"🟢 Retrieved {len(parsed)} vessels from AISStream")
                    return parsed
            else:
                st.warning("⚠️ No vessels found in the Caribbean area.")
                return get_demo_ships()
        elif r.status_code == 401:
            st.error("❌ AISStream API key is invalid or expired. Please check your key.")
            return get_demo_ships()
        elif r.status_code == 429:
            st.warning("⏳ AISStream rate limit exceeded. Please try again later.")
            return get_demo_ships()
        else:
            st.warning(f"⚠️ AISStream returned status {r.status_code}. Using demo data.")
            return get_demo_ships()
    except requests.exceptions.Timeout:
        st.warning("⏳ AISStream request timed out. Using demo data.")
        return get_demo_ships()
    except requests.exceptions.ConnectionError:
        st.warning("🌐 Could not connect to AISStream. Using demo data.")
        return get_demo_ships()
    except Exception as e:
        st.warning(f"⚠️ Error fetching vessel data: {str(e)}. Using demo data.")
        return get_demo_ships()

def get_demo_ships():
    """Generate demo ship data for testing when API is unavailable."""
    ground_lat = st.session_state.get("lat_override", 18.5392)
    ground_lon = st.session_state.get("lon_override", -72.3364)
    
    demo_ships = [
        {"id": "CARIB-01", "type": "Cargo Ship", "color": "#f1c40f", "label": "🚢 Cargo", "lat": 18.5, "lon": -69.5},
        {"id": "TANKER-2", "type": "Tanker", "color": "#00bfff", "label": "⛽ Tanker", "lat": 19.0, "lon": -71.0},
        {"id": "FISH-03", "type": "Fishing Vessel", "color": "#2ecc71", "label": "🎣 Fishing", "lat": 18.8, "lon": -72.0},
        {"id": "PASS-04", "type": "Passenger Ship", "color": "#9b59b6", "label": "🛳️ Passenger", "lat": 18.2, "lon": -68.5},
        {"id": "NAVY-05", "type": "Military Ship", "color": "#e74c3c", "label": "⚓ Military Ship", "lat": 19.5, "lon": -70.5},
    ]
    
    # Calculate distances from ground station
    for ship in demo_ships:
        lat = ship["lat"]
        lon = ship["lon"]
        R = 6371
        dlat = math.radians(lat - ground_lat)
        dlon = math.radians(lon - ground_lon)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(ground_lat)) * math.cos(math.radians(lat)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        dist_km = R * c
        ship["distance_km"] = round(dist_km, 1)
        ship["dist"] = min(dist_km / st.session_state.get("max_range", 500), 0.95)
        ship["detected_at"] = datetime.now(pytz.timezone('America/Port-au-Prince')).strftime("%Y-%m-%d %I:%M:%S %p")
        ship["alt"] = "0ft"
    
    return demo_ships

# ========== SATELLITE TRACKING ==========
@st.cache_data(ttl=21600)
def fetch_tle_from_celestrak(catnr, timeout=10, retries=2):
    urls = [
        f"https://celestrak.org/NORAD/elements/gp.php?CATNR={catnr}&FORMAT=TLE",
        f"https://celestrak.com/NORAD/elements/gp.php?CATNR={catnr}&FORMAT=TLE",
        f"http://celestrak.org/NORAD/elements/gp.php?CATNR={catnr}&FORMAT=TLE",
    ]
    for attempt in range(retries):
        for url in urls:
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    lines = response.text.strip().split('\n')
                    if len(lines) >= 3:
                        return lines[1].strip(), lines[2].strip()
                time.sleep(1)
            except Exception:
                continue
    return None, None

def get_satellite_tle():
    if not SKYFIELD_AVAILABLE:
        return None
    
    if st.session_state.satellite_tle_cache and st.session_state.satellite_cache_time:
        age = (datetime.now() - st.session_state.satellite_cache_time).total_seconds()
        if age < 21600:
            return st.session_state.satellite_tle_cache
    
    satellites_catalog = {
        "ISS": 25544,
        "NAV-GPS": 46825,
        "STAR-V2": 44713,
        "KH-11-S": 37348,
    }
    satellite_names = {
        "ISS": "ISS (ZARYA)",
        "NAV-GPS": "GPS III-6",
        "STAR-V2": "Starlink-1007",
        "KH-11-S": "USA-224 (KH-11)"
    }
    tle_data = {}
    for sat_id, catnr in satellites_catalog.items():
        line1, line2 = fetch_tle_from_celestrak(catnr)
        if line1 and line2:
            tle_data[sat_id] = {
                "name": satellite_names.get(sat_id, f"Satellite {catnr}"),
                "line1": line1,
                "line2": line2
            }
    if tle_data:
        st.session_state.satellite_tle_cache = tle_data
        st.session_state.satellite_cache_time = datetime.now()
        st.session_state.satellite_error = False
        return tle_data
    else:
        st.session_state.satellite_error = True
        return None

def compute_satellite_positions(target_time, ground_lat, ground_lon):
    if not SKYFIELD_AVAILABLE:
        return None
    tle_data = get_satellite_tle()
    if not tle_data:
        return None
    try:
        ts = load.timescale()
        t = ts.utc(target_time.year, target_time.month, target_time.day,
                   target_time.hour, target_time.minute, target_time.second)
        positions = []
        color_map = {
            "STAR-V2": "#00ff64",
            "NAV-GPS": "#00bfff",
            "KH-11-S": "#ff3300",
            "ISS": "#ffffff"
        }
        for sat_id, data in tle_data.items():
            satellite = EarthSatellite(data["line1"], data["line2"], data["name"], ts)
            geocentric = satellite.at(t)
            subpoint = geocentric.subpoint()
            lat = subpoint.latitude.degrees
            lon = subpoint.longitude.degrees
            alt_km = subpoint.elevation.km
            positions.append({
                "id": sat_id,
                "type": "Satellite",
                "name": data["name"],
                "color": color_map.get(sat_id, "#ffffff"),
                "lat": lat,
                "lon": lon,
                "alt": f"{alt_km:.0f}km" if alt_km > 0 else "N/A",
                "detected_at": target_time.strftime("%Y-%m-%d %I:%M:%S %p")
            })
        return positions
    except Exception:
        st.session_state.satellite_error = True
        return None

def get_satellite_data(u_lat, u_lon):
    if st.session_state.satellite_positions and st.session_state.satellite_cache_time:
        age = (datetime.now() - st.session_state.satellite_cache_time).total_seconds()
        if age < 3600:
            return st.session_state.satellite_positions
    if SKYFIELD_AVAILABLE:
        target_time = datetime.now()
        positions = compute_satellite_positions(target_time, u_lat, u_lon)
        if positions:
            st.session_state.satellite_positions = positions
            st.session_state.satellite_error = False
            return positions
        else:
            st.session_state.satellite_error = True
            return None
    else:
        st.session_state.satellite_error = True
        return None

# ========== TRANSLATIONS (abridged for brevity) ==========
UI = {
    "English": {
        "radar_tab": "📡 Radar Control",
        "sat_tab": "🛰️ Satellite Tracker",
        "ai_tab": "🤖 AI Analyst",
        "detect_tab": "✈️ Flight Tracker",
        "maritime_tab": "🚢 Maritime Detection",
        "worldcup_tab": "⚽ Live World Cup",
        "title": "GLOBAL SURVEILLANCE RADAR – HAITI & DR",
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
        "ai_question": "Ask about radar contacts, satellite predictions, or maritime activity:",
        "ai_analyze": "Analyze Current Threat Level",
        "ai_thinking": "🤖 AI analyzing surveillance data...",
        "ai_response": "💡 AI Analyst Report",
        "security_badge": "🔐 Global Security Shield active",
        "security_caption": "All data is secured and anonymized",
        "flight_tracker_title": "✈️ Live Flight Tracker",
        "flight_tracker_desc": "Real-time flight delay information powered by FlightAware",
        "maritime_title": "🚢 Maritime Detection – Caribbean",
        "maritime_desc": "List of vessels within range, including military and cargo ships.",
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
        "voice_lang_zh": "中文",
        "verify_flight": "🔍 Verify a Specific Flight",
        "verify_flight_hint": "Enter a flight number (e.g., AAL674) to check its current status on FlightAware.",
        "flight_id": "Flight ID",
        "check_flight_btn": "🔍 Check Flight",
        "example_flight": "✈️ Example: AAL674",
        "track_flight_on": "🔗 Click here to track **{}** on FlightAware",
        "fr24_link": "✈️ Also check on Flightradar24: [Link]({})",
        "enter_flight": "Please enter a flight ID.",
        "worldcup_title": "🏆 FIFA World Cup 2026 – Live Stream (FREE)",
        "worldcup_desc": "Watch every match live for free via the embedded stream.",
        "stream_note": "ℹ️ Stream provided by a third-party site."
    },
    # Other languages omitted for brevity
}

def t(key):
    return UI[st.session_state.lang].get(key, key)

# ========== AI ANALYSIS ==========
def ai_analysis(aircraft, ships, satellites, u_lat, u_lon, location_name, question=None):
    if not aircraft and not ships:
        radar_summary = "No aircraft or ships detected within the current range."
    else:
        sorted_aircraft = sorted(aircraft, key=lambda x: x["distance_km"]) if aircraft else []
        sorted_ships = sorted(ships, key=lambda x: x["distance_km"]) if ships else []
        lines = []
        for a in sorted_aircraft[:10]:
            lines.append(f"- {a['id']} ({a['type']}) at altitude {a['alt']}, distance {a['distance_km']:.1f} km (detected {a['detected_at']})")
        for s in sorted_ships[:10]:
            lines.append(f"- {s['id']} ({s['type']}) at distance {s['distance_km']:.1f} km (detected {s['detected_at']})")
        radar_summary = "\n".join(lines)
    
    sat_summary = "\n".join([f"- {s['id']} ({s['name']}) at altitude {s['alt']}, position {s['lat']:.2f}N, {s['lon']:.2f}W" for s in satellites]) if satellites else "No satellite data available."
    
    full_prompt = f"""You are an AI surveillance analyst. The ground station is located at {location_name} (Latitude {u_lat}, Longitude {u_lon}). 
Use the following live ADS-B and AIS data to answer the question. 
CRITICAL: Only report contacts actually present in the list. Do not invent.
If no data, state that clearly.
Be concise and factual.

Ground Station: {location_name} ({u_lat}, {u_lon})

Radar Contacts:
{radar_summary}

Satellites (for context):
{sat_summary}

Question: {question if question else "Give a threat summary including both air and maritime assets"}
Answer:"""
    
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a precise surveillance analyst. Only use provided data. Do not invent contacts."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2,
            max_tokens=600
        )
        response = completion.choices[0].message.content.strip()
        if not response:
            response = "⚠️ AI returned an empty response."
        return response
    except Exception as e:
        return f"⚠️ AI error: {str(e)}\n\nCheck your Groq API key and try again."

# ========== LOGIN PAGE ==========
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <h2 style="text-align:center; color:#e8ddd0;">🌐 GlobalInternet.py Access</h2>
            <p style="text-align:center; color:#a09080;">Secure Surveillance Portal – Haiti & DR</p>
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
    L = UI[st.session_state.lang]
    with st.sidebar:
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

        voice_lang = st.selectbox(
            L['voice_lang_label'],
            options=["en", "fr", "es", "zh"],
            format_func=lambda x: L[f"voice_lang_{x}"] if f"voice_lang_{x}" in L else x,
            key="voice_lang_selector"
        )

        if st.button(L['voice_male_explain'], use_container_width=True):
            script = generate_male_voice_audio()
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
                    st.success("🎙️ Male voice explanation played.")
            except ImportError:
                st.error("gTTS library not installed. Install with: pip install gTTS")
            except Exception as e:
                st.error(f"Voice generation error: {e}")

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
            status_text = "Live"
        elif "Cached" in status:
            badge_class = "status-cached"
            if st.session_state.cached_timestamp:
                time_str = st.session_state.cached_timestamp.strftime("%H:%M:%S")
                detail = L['status_cached_detail'].format(time=time_str)
            else:
                detail = "Cached data"
            status_text = "Cached"
        else:
            badge_class = "status-demo"
            detail = L['status_demo_detail']
            status_text = "Demo"
        st.markdown(f'<span class="status-badge {badge_class}">{status_text}</span>', unsafe_allow_html=True)
        st.caption(detail)

        st.divider()
        
        st.markdown("### 📡 Max Detection Range")
        max_range = st.slider(
            "Distance from ground station (km)",
            min_value=50,
            max_value=800,
            value=500,  # changed default to 500 km for better Haiti coverage
            step=10,
            key="max_range",
            help="Adjust to cover Haiti and the Dominican Republic."
        )
        st.caption(f"Current range: **{max_range} km**")
        st.divider()
        
        st.markdown("### 🔄 Auto-Refresh")
        refresh_interval = st.selectbox(
            "Refresh every:",
            ["5 seconds", "10 seconds", "15 seconds", "30 seconds", "Manual only"],
            index=1
        )
        if refresh_interval != "Manual only":
            seconds = int(refresh_interval.split()[0])
            st.caption(f"Auto-refreshing every {seconds} seconds")
        else:
            st.caption("Manual refresh only")
        
        st.divider()
        
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

        st.markdown("### 📍 Fixed Location")
        st.info("**Port-au-Prince, Haiti** (18.5392, -72.3364)")
        st.caption("Radar covers Haiti and the Dominican Republic.")
        
        location_name = "Port-au-Prince, Haiti"
        u_lat = 18.5392
        u_lon = -72.3364

        st.markdown("---")
        st.markdown("#### Override (optional)")
        location_name_override = st.text_input("Location Name (override)", value=location_name, key="loc_name_override")
        u_lat_override = st.number_input("Latitude", value=u_lat, format="%.4f", key="lat_override")
        u_lon_override = st.number_input("Longitude", value=u_lon, format="%.4f", key="lon_override")
        
        # ---- NEW: Reset to Haiti Defaults button ----
        if st.button("🔄 Reset to Haiti Defaults", use_container_width=True):
            # We need to update the session state keys for the override inputs
            st.session_state.loc_name_override = "Port-au-Prince, Haiti"
            st.session_state.lat_override = 18.5392
            st.session_state.lon_override = -72.3364
            st.session_state.max_range = 500
            st.rerun()
        
        if location_name_override != location_name or u_lat_override != u_lat or u_lon_override != u_lon:
            location_name = location_name_override
            u_lat = u_lat_override
            u_lon = u_lon_override
            st.caption("Using custom location override.")
        else:
            st.caption("Using default Port-au-Prince, Haiti.")

        st.divider()
        aip_key = st.text_input(L['aip_key'], type="password", placeholder="Enter Provider Key...")
        st.divider()
        use_demo = st.checkbox("Demo Mode (disable live OpenSky & Maritime)", value=False)
        st.divider()
        if st.button(L['refresh_btn'], use_container_width=True):
            st.rerun()
        st.divider()
        
        # ---- Maritime API test button ----
        with st.expander("🔍 Test Maritime API"):
            if st.button("Run Diagnostic"):
                with st.spinner("Testing AISStream..."):
                    ais_key = st.secrets.get("AISSTREAM_API_KEY")
                    if not ais_key:
                        ais_key = "e8622757a267cc06fb9ad0126d52ad519d784039"
                    if not ais_key:
                        st.warning("No AISStream key available.")
                    else:
                        try:
                            r = requests.get("https://api.aisstream.io/v1/vessels", 
                                             headers={"X-API-Key": ais_key}, 
                                             params={"bbox": "-75,17,-68,20"}, timeout=10)
                            st.write(f"Status: {r.status_code}")
                            st.text(r.text[:1000])
                        except Exception as e:
                            st.error(f"Error: {e}")

        st.write("📞 (509) 4738-5663")
        st.write("✉️ deslandes78@gmail.com")
        if st.button(L['logout'], type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # ---- Fetch aircraft data ----
    if use_demo:
        aircraft_data, _ = get_demo_aircraft(), "demo"
        st.session_state.api_status = "Demo (User selected)"
    else:
        aircraft_data, status = fetch_live_aircraft(u_lat, u_lon)
        if status == "cached" and aircraft_data:
            st.info("📡 Using cached data (live refresh in progress)")
        elif status == "demo":
            st.warning("📡 No live signal yet. Waiting for OpenSky data...")

    # ---- Fetch maritime data ----
    if use_demo:
        ships_data = get_demo_ships()
        st.info("🚢 Using demo ship data (Demo Mode enabled)")
    else:
        ships_data = fetch_live_ships(u_lat, u_lon)

    # ---- Satellite data ----
    sat_data = []

    # ---- TABS ----
    tab_radar, tab_sat, tab_ai, tab_detect, tab_maritime, tab_worldcup = st.tabs([
        L["radar_tab"], 
        L["sat_tab"], 
        L["ai_tab"], 
        L["detect_tab"],
        L["maritime_tab"],
        L["worldcup_tab"]
    ])

    # ========== RADAR TAB ==========
    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.subheader(L['author_tag'])
        st.info(L['audio_note'])
        
        all_contacts = aircraft_data + ships_data
        if all_contacts:
            close_contacts = [c for c in all_contacts if "distance_km" in c and c["distance_km"] <= 100]
            if close_contacts:
                closest = min(close_contacts, key=lambda x: x["distance_km"])
                st.success(f"🛩️ Closest contact: **{closest['id']}** – {closest['type']} – {closest['distance_km']:.1f} km away")
            else:
                st.info("ℹ️ No contacts detected within 100 km of your location.")
        else:
            st.info("ℹ️ No contacts detected.")
        
        col_rad, col_log = st.columns([2, 1])
        with col_rad:
            st.markdown(f"### {L['legend_title']}")
            legend_html = """
            <div class="legend">
                <span class="legend-item"><span class="legend-shape" style="color:#2ecc71;">⬤</span> Commercial Airplane</span>
                <span class="legend-item"><span class="legend-shape" style="color:#e74c3c;">▲</span> Military Aircraft</span>
                <span class="legend-item"><span class="legend-shape" style="color:#ff6b35;">◆</span> Drone (Low)</span>
                <span class="legend-item"><span class="legend-shape" style="color:#ff00ff;">◆</span> Drone (High)</span>
                <span class="legend-item"><span class="legend-shape" style="color:#ff9900;">◆</span> Drone (Mid)</span>
                <span class="legend-item"><span class="legend-shape" style="color:#f1c40f;">⬛</span> Cargo</span>
                <span class="legend-item"><span class="legend-shape" style="color:#e74c3c;">⬜</span> Military Ship</span>
                <span class="legend-item"><span class="legend-shape" style="color:#f1c40f;">⬜</span> Cargo Ship</span>
                <span class="legend-item"><span class="legend-shape" style="color:#00bfff;">⬜</span> Tanker</span>
                <span class="legend-item"><span class="legend-shape" style="color:#9b59b6;">■</span> UFO</span>
                <span class="legend-item"><span class="legend-shape" style="color:#3498db;">●</span> General Aviation</span>
                <span class="legend-item"><span class="legend-shape" style="color:#95a5a6;">◉</span> Other</span>
            </div>
            """
            st.markdown(legend_html, unsafe_allow_html=True)
            radar_json = json.dumps(all_contacts)
            radar_html = f"""
            <html><body style="background:#0a0a0f; margin:0; display:flex; justify-content:center;">
                <canvas id="radar" width="550" height="550" style="border-radius:50%; border:2px solid #4a8aff; cursor:pointer; box-shadow:0 0 30px rgba(74,138,255,0.3);"></canvas>
                <script>
                    const canvas = document.getElementById('radar');
                    const ctx = canvas.getContext('2d');
                    const data = {radar_json};
                    let angle = 0;
                    let audioCtx = null;
                    let soundEnabled = false;
                    let alertPlayed = false;
                    
                    canvas.addEventListener('click', () => {{
                        if (!audioCtx) {{
                            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        }}
                        if (audioCtx.state === 'suspended') {{
                            audioCtx.resume();
                        }}
                        soundEnabled = true;
                        canvas.style.borderColor = '#00ff64';
                        canvas.style.boxShadow = '0 0 40px rgba(0,255,100,0.5)';
                        setTimeout(() => {{ 
                            canvas.style.borderColor = '#4a8aff';
                            canvas.style.boxShadow = '0 0 30px rgba(74,138,255,0.3)';
                        }}, 300);
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
                    
                    function playAlert() {{
                        if (!audioCtx) return;
                        try {{
                            const osc = audioCtx.createOscillator();
                            const gain = audioCtx.createGain();
                            const now = audioCtx.currentTime;
                            osc.type = 'square';
                            osc.frequency.setValueAtTime(880, now);
                            osc.frequency.exponentialRampToValueAtTime(660, now + 0.25);
                            gain.gain.setValueAtTime(0.12, now);
                            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
                            osc.connect(gain);
                            gain.connect(audioCtx.destination);
                            osc.start(now);
                            osc.stop(now + 0.35);
                        }} catch (e) {{}}
                    }}
                    
                    function drawTarget(ctx, x, y, color, type, id, alt, pulse, distance, isShip) {{
                        const size = 9;
                        ctx.save();
                        ctx.shadowBlur = 25;
                        ctx.shadowColor = color;
                        ctx.fillStyle = color;
                        ctx.strokeStyle = '#ffffff';
                        ctx.lineWidth = 1.5;
                        
                        if (isShip) {{
                            ctx.fillRect(x - size*0.8, y - size*0.8, size*1.6, size*1.6);
                            ctx.strokeRect(x - size*0.8, y - size*0.8, size*1.6, size*1.6);
                        }} else if (type.includes('Drone')) {{
                            ctx.beginPath();
                            ctx.moveTo(x, y - size);
                            ctx.lineTo(x + size, y);
                            ctx.lineTo(x, y + size);
                            ctx.lineTo(x - size, y);
                            ctx.closePath();
                            ctx.fill();
                            ctx.stroke();
                        }} else if (type === 'Military') {{
                            ctx.beginPath();
                            ctx.moveTo(x, y - size);
                            ctx.lineTo(x - size, y + size*0.7);
                            ctx.lineTo(x + size, y + size*0.7);
                            ctx.closePath();
                            ctx.fill();
                            ctx.stroke();
                        }} else if (type === 'UFO') {{
                            ctx.fillRect(x - size*0.7, y - size*0.7, size*1.4, size*1.4);
                            ctx.strokeRect(x - size*0.7, y - size*0.7, size*1.4, size*1.4);
                        }} else {{
                            ctx.beginPath();
                            ctx.arc(x, y, size*0.6, 0, 2*Math.PI);
                            ctx.fill();
                            ctx.stroke();
                        }}
                        ctx.shadowBlur = 0;
                        ctx.restore();
                        
                        ctx.fillStyle = '#ffffff';
                        ctx.font = 'bold 10px monospace';
                        ctx.shadowBlur = 0;
                        ctx.fillText(id, x + 14, y - 4);
                        ctx.fillStyle = 'rgba(220,220,220,0.8)';
                        ctx.font = '8px monospace';
                        ctx.fillText(alt || '', x + 14, y + 10);
                        ctx.fillStyle = 'rgba(200,200,200,0.5)';
                        ctx.font = '7px monospace';
                        ctx.fillText(distance + 'km', x + 14, y + 20);
                    }}
                    
                    function draw() {{
                        ctx.clearRect(0,0,550,550);
                        const bgGrad = ctx.createRadialGradient(275,275,50,275,275,280);
                        bgGrad.addColorStop(0, 'rgba(20,40,80,0.35)');
                        bgGrad.addColorStop(0.5, 'rgba(10,20,50,0.25)');
                        bgGrad.addColorStop(1, 'rgba(0,0,0,0.5)');
                        ctx.fillStyle = bgGrad;
                        ctx.fillRect(0,0,550,550);
                        
                        const cx = 275, cy = 275, r = 250;
                        ctx.strokeStyle = 'rgba(100,200,255,0.6)';
                        ctx.lineWidth = 1.2;
                        for(let i = 1; i <= 4; i++) {{
                            ctx.beginPath();
                            ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2);
                            ctx.stroke();
                        }}
                        ctx.strokeStyle = 'rgba(0,255,200,0.5)';
                        ctx.lineWidth = 1;
                        ctx.setLineDash([5,5]);
                        ctx.beginPath();
                        ctx.moveTo(cx - r, cy);
                        ctx.lineTo(cx + r, cy);
                        ctx.moveTo(cx, cy - r);
                        ctx.lineTo(cx, cy + r);
                        ctx.stroke();
                        ctx.setLineDash([]);
                        
                        const pulse = Date.now() / 300;
                        data.forEach((d, i) => {{
                            const angleRad = i * 0.8 + 0.1;
                            const dx = cx + Math.cos(angleRad) * (r * (d.dist || 0.5));
                            const dy = cy + Math.sin(angleRad) * (r * (d.dist || 0.5));
                            const dist = d.distance_km ? d.distance_km.toFixed(0) : 'N/A';
                            const isShip = d.type.includes('Ship') || d.type.includes('Tanker');
                            drawTarget(ctx, dx, dy, d.color, d.type, d.id, d.alt || '', pulse, dist, isShip);
                        }});
                        
                        if (data.length > 0) {{
                            if (!alertPlayed) {{
                                playAlert();
                                alertPlayed = true;
                            }}
                        }} else {{
                            alertPlayed = false;
                        }}
                        
                        let oldA = angle;
                        angle -= 0.03;
                        if (Math.floor(oldA / (2*Math.PI)) !== Math.floor(angle / (2*Math.PI))) {{
                            ping();
                        }}
                        ctx.save();
                        ctx.translate(cx, cy);
                        ctx.rotate(angle);
                        const grad = ctx.createRadialGradient(0,0,0,0,0,r);
                        grad.addColorStop(0, 'rgba(0,255,180,0.15)');
                        grad.addColorStop(0.5, 'rgba(0,200,255,0.2)');
                        grad.addColorStop(1, 'rgba(0,150,255,0.3)');
                        ctx.fillStyle = grad;
                        ctx.beginPath();
                        ctx.moveTo(0,0);
                        ctx.arc(0,0,r,0,0.5);
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
            <div style="background: rgba(20,16,24,0.9); border: 1px solid #4a3520; border-radius: 8px; padding: 10px 12px; text-align: center; font-family: 'Courier New', monospace;">
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
            for d in all_contacts:
                with st.expander(f"{d.get('label', d['id'])} [{d['type']}]"):
                    st.write(f"**ID:** {d['id']}")
                    if 'alt' in d:
                        st.write(f"**Altitude:** {d['alt']}")
                    st.write(f"**Distance:** {d['distance_km']:.1f} km")
                    st.write(f"**Detected at:** {d.get('detected_at', 'N/A')}")
                    if not use_demo and 'lat' in d:
                        st.write(f"**Lat/Lon:** {d['lat']:.4f}, {d['lon']:.4f}")
                    report_data = f"RADAR LOG\nAsset: {d['id']}\nType: {d['type']}\nDistance: {d['distance_km']:.1f} km\nDetected at: {d.get('detected_at', 'N/A')}\nOP: Gesner Deslandes"
                    st.download_button(L['report'], report_data, key=f"dl_{d['id']}")

    # Satellite tab (unchanged)
    with tab_sat:
        st.title(f"🛰️ {L['sat_tab']}")
        st.subheader(L['author_tag'])
        
        if not SKYFIELD_AVAILABLE:
            st.error("❌ Skyfield library is not installed. Please install it with: pip install skyfield")
        else:
            with st.spinner("🛰️ Fetching real-time satellite positions from Celestrak..."):
                sat_data = get_satellite_data(u_lat, u_lon)
            
            if st.session_state.satellite_error or sat_data is None or len(sat_data) == 0:
                st.error("❌ Unable to fetch real-time satellite data from Celestrak. Please check your internet connection and try again.")
                if st.button("🔄 Retry Satellite Fetch"):
                    st.session_state.satellite_tle_cache = None
                    st.session_state.satellite_cache_time = None
                    st.session_state.satellite_positions = None
                    st.session_state.satellite_error = False
                    st.rerun()
                st.info("ℹ️ Satellite positions will appear here once the TLE data is successfully retrieved.")
            else:
                st.success("✅ Real-time satellite positions successfully loaded from Celestrak (TLE)")
                col_ctrl, col_map = st.columns([1, 2])
                with col_ctrl:
                    st.subheader("Live Satellite Positions")
                    st.caption("Positions calculated from real TLE data (updated every 6 hours)")
                    for s in sat_data:
                        with st.container(border=True):
                            st.write(f"**{s['id']}** ({s['name']})")
                            st.caption(f"Position: {s['lat']:.2f}°N, {s['lon']:.2f}°W")
                            st.caption(f"Altitude: {s['alt']}")
                            st.caption(f"Updated: {s['detected_at']}")
                
                with col_map:
                    st.subheader(L['sky_view'])
                    tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                    attribution = "AIP Imagery: Esri, Maxar, Earthstar Geographics"
                    markers = ""
                    if not use_demo and aircraft_data and aircraft_data != get_demo_aircraft():
                        for a in aircraft_data:
                            if "lat" in a and "lon" in a:
                                markers += f"L.circleMarker([{a['lat']}, {a['lon']}], {{color:'{a['color']}', radius:6}}).addTo(map).bindPopup('✈️ {a['id']}<br>Alt: {a['alt']}<br>Dist: {a['distance_km']:.1f}km');"
                    for s in ships_data:
                        if "lat" in s and "lon" in s:
                            markers += f"L.circleMarker([{s['lat']}, {s['lon']}], {{color:'{s['color']}', radius:8, weight:2}}).addTo(map).bindPopup('🚢 {s['id']}<br>Type: {s['type']}<br>Dist: {s['distance_km']:.1f}km');"
                    for s in sat_data:
                        markers += f"L.circleMarker([{s['lat']}, {s['lon']}], {{color:'{s['color']}', radius:10, weight:2}}).addTo(map).bindPopup('🛰️ {s['id']}<br>{s['name']}<br>Alt: {s['alt']}');"
                    map_html = f"""
                    <html><head>
                        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                        <style>#map {{ height: 500px; border-radius: 15px; border: 2px solid #2a1f14; }}</style>
                    </head><body>
                        <div id="map"></div>
                        <script>
                            const map = L.map('map', {{zoomControl: false}}).setView([{u_lat}, {u_lon}], 8);
                            L.tileLayer('{tiles}', {{ attribution: '{attribution}' }}).addTo(map);
                            L.circleMarker([{u_lat}, {u_lon}], {{color: '#00ff64', radius: 12, weight: 3}}).addTo(map).bindPopup('📍 Ground Station');
                            {markers}
                        </script>
                    </body></html>
                    """
                    components.html(map_html, height=550)

    # AI Analyst tab
    with tab_ai:
        st.title("🤖 AI Surveillance Analyst")
        
        common_questions = [
            "What is the current threat level in Haiti/DR?",
            "How many aircraft are within 200 km of Port-au-Prince?",
            "Are there any military ships in the Caribbean?",
            "What is the closest contact to my location?",
            "How many drones are detected?",
            "What satellites are currently overhead?",
            "Summarize all radar, maritime, and satellite activity.",
            "Is there any unusual or unidentified contact?",
            "What is the average distance of all contacts?",
            "Are there any cargo ships near the Mona Passage?",
            "What is the total number of aircraft and ships?",
            "Predict the trajectory of the nearest aircraft.",
            "How does current activity compare to typical patterns?",
            "Are there any low-altitude threats?",
            "Provide a combined threat assessment."
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
            user_question = st.text_area(
                L['ai_question'],
                height=100,
                value=st.session_state.ai_question_input,
                key="ai_question_text"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                analyze_btn = st.button(L['ai_analyze'], use_container_width=True)
            with col_btn2:
                listen_btn = st.button(L['listen_response'], use_container_width=True)
            
            if not st.session_state.ai_response:
                st.info("💡 Click 'Analyze' to get an AI response based on the current radar data.")
            else:
                st.markdown(f"### {L['ai_response']}")
                st.markdown(st.session_state.ai_response)
            
            if analyze_btn:
                if not user_question.strip():
                    st.warning("Please enter a question.")
                else:
                    with st.spinner(L['ai_thinking']):
                        sat_data = get_satellite_data(u_lat, u_lon)
                        if sat_data is None:
                            sat_data = []
                        response = ai_analysis(aircraft_data, ships_data, sat_data, u_lat, u_lon, location_name, user_question)
                        st.session_state.ai_response = response
                    st.rerun()
            
            if listen_btn:
                if st.session_state.ai_response:
                    with st.spinner("Generating audio..."):
                        lang_code = "en" if voice_lang == "en" else "fr" if voice_lang == "fr" else "es" if voice_lang == "es" else "zh"
                        audio_bytes = generate_audio_response(st.session_state.ai_response, lang_code)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                            st.success("🔊 AI response played.")
                        else:
                            st.error("Could not generate audio.")
                else:
                    st.warning("No AI response to listen to. Please ask a question first.")

    # Flight Tracker tab
    with tab_detect:
        st.title(L['flight_tracker_title'])
        st.markdown(L['flight_tracker_desc'])

        st.markdown(f"### {L['verify_flight']}")
        st.markdown(L['verify_flight_hint'])

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            flight_id = st.text_input(L['flight_id'], placeholder="e.g., AAL674 or AA674", key="flight_check_input")
        with col2:
            check_btn = st.button(L['check_flight_btn'], use_container_width=True)
        with col3:
            st.markdown(f"[{L['example_flight']}](https://hi.flightaware.com/live/flight/AAL674)", unsafe_allow_html=True)

        if check_btn and flight_id:
            clean_id = flight_id.strip().upper()
            fa_link = f"https://hi.flightaware.com/live/flight/{clean_id}"
            fr_link = f"https://www.flightradar24.com/{clean_id}"
            st.markdown(L['track_flight_on'].format(clean_id, fa_link))
            st.info(L['fr24_link'].format(fr_link))
        elif check_btn:
            st.warning(L['enter_flight'])

        st.markdown("---")

        st.markdown("### 📋 Current Airport Delay Reports")
        st.markdown("""
        - **Toussaint Louverture Int'l (MTPP)**: departure delays avg 45m due to weather.
        - **Las Américas Int'l (MDSD)**: arrival delays avg 30m.
        - **Miami Int'l (KMIA)**: departure delays avg 1h 15m.
        - **Newark Liberty (KEWR)**: departure delays avg 42m.
        - **Boston Logan (KBOS)**: departure delays avg 48m (decreasing).
        - **Dallas-Fort Worth (KDFW)**: departure delays 46m to 1h (increasing) due to weather.
        - **Chicago Midway (KMDW)**: departure delays avg 41m (increasing).
        - **London Gatwick (EGKK)**: arrival delays avg 33m (decreasing).
        - **John F Kennedy (KJFK)**: departure delays 31m to 45m (increasing) due to traffic volume.
        """)

        st.markdown("---")
        st.components.v1.iframe(
            "https://embed.flightaware.com/commercial/integrated/web/delay_map_fullpage.rvt",
            height=600,
            scrolling=True
        )

    # ========== MARITIME TAB ==========
    with tab_maritime:
        st.title(L['maritime_title'])
        st.markdown(L['maritime_desc'])

        if ships_data:
            st.success(f"🟢 **{len(ships_data)}** vessels detected within range.")
            for ship in ships_data:
                with st.container(border=True):
                    cols = st.columns([1, 3, 1])
                    with cols[0]:
                        st.markdown(f"**{ship['id']}**")
                        st.caption(ship['type'])
                    with cols[1]:
                        st.markdown(f"Distance: **{ship['distance_km']:.1f} km**")
                        if 'lat' in ship and 'lon' in ship:
                            st.caption(f"Lat: {ship['lat']:.4f}, Lon: {ship['lon']:.4f}")
                        st.caption(f"Detected: {ship['detected_at']}")
                    with cols[2]:
                        st.markdown(f"<span style='color:{ship['color']}; font-size:2rem;'>{ship.get('label', '🚢')}</span>", unsafe_allow_html=True)
        else:
            st.info("No ships detected within range. Adjust range or check data source.")

    # World Cup tab
    with tab_worldcup:
        st.title(L['worldcup_title'])
        st.markdown(L['worldcup_desc'])

        stream1_url = "https://futbol-libres.su/eventos.html?r=aHR0cHM6Ly9sYXRhbXZpZHpzLm9yZy9jYW5hbC5waHA/c3RyZWFtPXRlbGVtdW5kb3VzYQ=="
        stream2_url = "https://futbol-libres.su/eventos.html?r=aHR0cHM6Ly9sYXRhbXZpZHpzLm9yZy9jYW5hbC5waHA/c3RyZWFtPWRzcG9ydHM="

        sub_tab1, sub_tab2 = st.tabs(["📺 Stream #1 (Main)", "⚽ Live WorldCup 2026 #2"])

        with sub_tab1:
            st.components.v1.iframe(stream1_url, height=600, scrolling=True)
            st.caption("📺 Live soccer stream – watch the 2026 World Cup matches for free.")

        with sub_tab2:
            st.components.v1.iframe(stream2_url, height=600, scrolling=True)
            st.caption("⚽ Alternative live stream – enjoy the matches via the second feed.")

        st.markdown("---")
        st.info(L['stream_note'])

# ========== RUN ==========
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
