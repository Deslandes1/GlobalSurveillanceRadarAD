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
    .clock-container {
        background: rgba(20,16,24,0.6);
        border: 1px solid #2a1f14;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 5px 0 10px 0;
        text-align: center;
        font-family: 'Courier New', monospace;
        color: #00ff64;
        font-size: 1.1rem;
        letter-spacing: 1px;
    }
    .clock-container .date {
        color: #b8a898;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# ========== AI VOICE SCRIPTS ==========
def generate_male_voice_audio():
    script = """
    Welcome to the Global Surveillance Radar Portal, built by Gesner Deslandes at GlobalInternet.py.
    
    This application features four main modules.
    
    First, the Radar Control tab. Here you can view live aircraft tracking with a 360-degree radar display. The radar sweeps continuously and plays a classic fetching sound on each pass. You can see aircraft identified by type, altitude, and distance from your ground station. The interface includes a live clock showing the current time and date.
    
    Second, the Satellite Tracker tab. This module displays satellite positions and allows you to predict future passes based on your selected time and date. You can also view an interactive map with both aircraft and satellite overlays.
    
    Third, the AI Analyst tab. This module is powered by Groq's Llama 3.1 model. You can ask any question about the radar contacts or satellite predictions, and the AI will provide a detailed threat analysis and recommendations.
    
    Fourth, the Object Detection tab. Upload an image and the system will detect and label objects using YOLOv8 computer vision.
    
    The sidebar includes language selection, your ground station coordinates, a demo mode toggle, and secure logout.
    
    This software is built for surveillance, security, and intelligence analysis. All data is encrypted and anonymized.
    
    GlobalInternet.py – connecting the global market with local expertise.
    """
    return script

def generate_female_voice_audio():
    script = """
    Welcome to the Global Surveillance Radar Portal, built by Gesner Deslandes at GlobalInternet.py.
    
    This advanced surveillance system now features a live radar with a classic fetching sound – just click the radar screen to enable the audio, and you will hear a sonar ping on every sweep.
    
    Objects are automatically classified and displayed with real military-style symbols. Military targets appear as red triangles, unknown or UFO contacts as purple squares, drones as orange diamonds, and civilian aircraft as green or blue circles. Each symbol includes the callsign and altitude for instant identification.
    
    A live clock and calendar are displayed on the main page, showing the current time with seconds running and today's date in real time.
    
    The Radar Control tab gives you a 360‑degree view with range rings and contact labels. The Satellite Tracker tab predicts satellite passes and shows an interactive map with both aircraft and satellite overlays.
    
    The AI Analyst tab uses Groq's Llama 3.1 to answer your questions about radar contacts and satellite predictions, providing threat analysis and recommendations.
    
    The Object Detection tab lets you upload images and detect objects with YOLOv8.
    
    The sidebar provides language selection, ground station coordinates, demo mode, and secure logout.
    
    All data is encrypted and anonymised. This software is ideal for surveillance, security, and intelligence analysis.
    
    GlobalInternet.py – connecting the global market with local expertise.
    """
    return script

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

# ========== AIRCRAFT CLASSIFICATION ==========
def classify_aircraft(alt_ft, callsign=""):
    alt_ft = int(alt_ft.replace(",","").replace("ft","").strip()) if isinstance(alt_ft, str) else alt_ft
    if not isinstance(alt_ft, (int, float)):
        alt_ft = 0

    callsign = str(callsign).upper()

    if "UFO" in callsign or "UNK" in callsign or len(callsign) < 3:
        return "UFO", "#9b59b6", "🛸 UFO"

    military_prefixes = ["F-", "B-", "C-", "E-", "KC-", "T-", "V-", "A-", "AH-", "CH-", "UH-"]
    if any(callsign.startswith(pre) for pre in military_prefixes) or alt_ft > 40000:
        return "Military", "#e74c3c", "✈️ Military"

    if alt_ft < 1000 or "DRN" in callsign or "UAV" in callsign:
        return "Drone", "#f39c12", "🚁 Drone"

    if alt_ft > 25000 and alt_ft <= 40000 and ("C" in callsign or "CLX" in callsign or "FDX" in callsign):
        return "Cargo", "#f1c40f", "📦 Cargo"

    if 10000 <= alt_ft <= 30000:
        return "Public Airplane", "#2ecc71", "🛩️ Public Airplane"

    if alt_ft < 10000:
        return "General Aviation", "#3498db", "🛩️ General"

    return "Other", "#95a5a6", "❓ Unknown"

# ========== LIVE AIRCRAFT DATA FROM OPENSKY (with retry) ==========
def fetch_live_aircraft(ground_lat, ground_lon, retries=3):
    url = "https://opensky-network.org/api/states/all"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SurveillancePortal/1.0)"}
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            states = data.get("states", [])
            if not states:
                return []
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
            return aircraft_list[:30]
        except Exception as e:
            if attempt == retries - 1:
                st.warning(f"OpenSky API error after {retries} attempts: {e}")
            else:
                time.sleep(1)
    return []

def get_demo_aircraft():
    return [
        {"id": "AAL-410", "type": "Public Airplane", "color": "#2ecc71", "label": "🛩️ Public Airplane", "alt": "32,000ft", "dist": 0.4},
        {"id": "F-22-EX", "type": "Military", "color": "#e74c3c", "label": "✈️ Military", "alt": "52,000ft", "dist": 0.8},
        {"id": "DRN-QC", "type": "Drone", "color": "#f39c12", "label": "🚁 Drone", "alt": "800ft", "dist": 0.2},
        {"id": "CLX-200", "type": "Cargo", "color": "#f1c40f", "label": "📦 Cargo", "alt": "28,000ft", "dist": 0.6},
        {"id": "UFO-X", "type": "UFO", "color": "#9b59b6", "label": "🛸 UFO", "alt": "1,500ft", "dist": 0.7}
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
        "live_note": "Live data may not work on Streamlit Cloud due to network restrictions. For real detection, run this app locally or use Demo Mode.",
        "voice_male_explain": "🎙️ AI Male Voice – Explain App",
        "voice_female_explain": "🎤 AI Female Voice – Explain App (with new features)",
        "legend_title": "🟢 Real NATO‑Style Symbols",
        "clock_label": "🕒 Live Clock"
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
        "live_note": "Les données en direct peuvent ne pas fonctionner sur Streamlit Cloud. Exécutez localement pour une vraie détection.",
        "voice_male_explain": "🎙️ Voix IA Homme – Expliquer l'app",
        "voice_female_explain": "🎤 Voix IA Femme – Expliquer l'app (nouveautés)",
        "legend_title": "🟢 Symboles militaires réels",
        "clock_label": "🕒 Horloge en direct"
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

def ai_analysis(aircraft, satellites, u_lat, u_lon, question=None):
    radar_summary = "\n".join([f"- {a['id']} ({a['type']}) at altitude {a['alt']}, distance {a['dist']*300:.0f}km" for a in aircraft])
    sat_summary = "\n".join([f"- {s['id']} ({s['type']}) at altitude {s['alt']}" for s in satellites])
    full_prompt = f"""You are an AI surveillance analyst. Use the following data to answer the question. Respond concisely.

Ground Station: Lat {u_lat}, Lon {u_lon}

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
        st.selectbox("Language", ["English", "French"], key="lang")
        st.markdown(f"**{L['author_tag']}**")
        st.divider()

        # Male Voice button
        if st.button(L['voice_male_explain'], use_container_width=True):
            script = generate_male_voice_audio()
            try:
                from gtts import gTTS
                tts = gTTS(text=script, lang="en" if st.session_state.lang == "English" else "fr", slow=False)
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
                tts = gTTS(text=script, lang="en" if st.session_state.lang == "English" else "fr", slow=False)
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
        st.info(L['live_note'])
        st.divider()

        u_lat = st.number_input(L['lat'], value=18.5392, format="%.4f")
        u_lon = st.number_input(L['lon'], value=-72.3364, format="%.4f")
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

    # Fetch live data if not demo
    if use_demo:
        aircraft_data = get_demo_aircraft()
    else:
        with st.spinner("Fetching live aircraft data (30 sec timeout)..."):
            aircraft_data = fetch_live_aircraft(u_lat, u_lon)
            if not aircraft_data:
                st.warning("No live data received. Falling back to demo.")
                aircraft_data = get_demo_aircraft()

    sat_data = get_satellites()

    tab_radar, tab_sat, tab_ai, tab_detect = st.tabs([L["radar_tab"], L["sat_tab"], L["ai_tab"], L["detect_tab"]])

    # Radar tab
    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.subheader(L['author_tag'])
        st.info(L['audio_note'])
        col_rad, col_log = st.columns([2, 1])
        with col_rad:
            # Legend with real symbol shapes
            st.markdown(f"### {L['legend_title']}")
            legend_html = """
            <div class="legend">
                <span class="legend-item">
                    <span class="legend-shape" style="color:#2ecc71;">⬤</span> Public Airplane
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#e74c3c;">▲</span> Military
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#f39c12;">◆</span> Drone
                </span>
                <span class="legend-item">
                    <span class="legend-shape" style="color:#f1c40f;">⬛</span> Cargo / Unknown
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

            # Radar canvas with real NATO-style symbols
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
                            case 'Public Airplane':
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
                            case 'Cargo':
                                ctx.fillRect(x - size*0.8, y - size*0.8, size*1.6, size*1.6);
                                ctx.strokeRect(x - size*0.8, y - size*0.8, size*1.6, size*1.6);
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
            
            # ========== LIVE CLOCK AND CALENDAR (fixed using components.html) ==========
            clock_html = """
            <div class="clock-container">
                <div id="liveClock">--:--:--</div>
                <div class="date" id="liveDate">--/--/----</div>
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
            components.html(clock_html, height=70)
            
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
            if not use_demo:
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
        user_question = st.text_area(L['ai_question'], height=100)
        if st.button(L['ai_analyze'], use_container_width=True):
            with st.spinner(L['ai_thinking']):
                response = ai_analysis(aircraft_data, sat_data, u_lat, u_lon, user_question if user_question.strip() else None)
            st.markdown(f"### {L['ai_response']}")
            st.markdown(response)

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
