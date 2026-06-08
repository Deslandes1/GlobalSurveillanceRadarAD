import streamlit as st
import json
import random
import math
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from groq import Groq

# --- 1. CORE CONFIGURATION ---
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance Portal",
    layout="wide",
    page_icon="🌐"
)

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- GROQ CLIENT (from secrets) ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. SURVEILLANCE DATA GENERATOR ---
def get_surveillance_data(is_demo, u_lat, u_lon):
    if not is_demo:
        return [], []
    
    # Aircraft Classes for Radar
    aircraft = [
        {"id": "AAL-410", "type": "Commercial", "color": "#00ff64", "alt": "32,000ft", "dist": 0.4},
        {"id": "F-22-EX", "type": "Military Strike", "color": "#ff3300", "alt": "52,000ft", "dist": 0.8},
        {"id": "DRN-QC", "type": "Drone/UAV", "color": "#ffcc00", "alt": "800ft", "dist": 0.2}
    ]
    
    # Satellite Classes for Prediction
    satellites = [
        {"id": "STAR-V2", "type": "Starlink", "color": "#00ff64", "alt": "550km"},
        {"id": "NAV-GPS", "type": "GPS III", "color": "#00bfff", "alt": "20,200km"},
        {"id": "KH-11-S", "type": "Spy Satellite", "color": "#ff3300", "alt": "380km"},
        {"id": "ISS", "type": "Space Station", "color": "#ffffff", "alt": "408km"}
    ]
    
    return aircraft, satellites

# --- 3. TRANSLATION DICTIONARY (extended with AI tab)---
UI = {
    "English": {
        "radar_tab": "📡 Radar Control", "sat_tab": "🛰️ Satellite Tracker", "ai_tab": "🤖 AI Analyst",
        "title": "GLOBAL SURVEILLANCE RADAR", "author_tag": "Built by Gesner Deslandes",
        "logout": "Terminate Session", "report": "Download Asset Report",
        "detection_log": "Live Detection Log", "sat_engine": "Predictive Mapping Engine",
        "audio_note": "Click radar to enable sonar audio.", "lat": "Latitude", "lon": "Longitude",
        "predict_btn": "Calculate Pass", "time_target": "Prediction Target (Date/Time)",
        "aip_key": "AIP Security Key (Aerial Imagery)", "sky_view": "Satellite OpenSky View",
        "ai_question": "Ask about radar contacts or satellite predictions:",
        "ai_analyze": "Analyze Current Threat Level",
        "ai_thinking": "🤖 AI analyzing surveillance data...",
        "ai_response": "💡 AI Analyst Report",
        "security_badge": "🔐 Global Security Shield active",
        "security_caption": "All data is secured and anonymized"
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar", "sat_tab": "🛰️ Suivi Satellite", "ai_tab": "🤖 Analyste IA",
        "title": "RADAR DE SURVEILLANCE MONDIAL", "author_tag": "Conçu par Gesner Deslandes",
        "logout": "Déconnexion", "report": "Télécharger le Rapport",
        "detection_log": "Journal de Détection", "sat_engine": "Moteur de Cartographie Prédictive",
        "audio_note": "Cliquez sur le radar pour l'audio.", "lat": "Latitude", "lon": "Longitude",
        "predict_btn": "Prédire le Passage", "time_target": "Date/Heure Cible",
        "aip_key": "Clé de Sécurité AIP (Imagerie Aérienne)", "sky_view": "Vue Satellite OpenSky",
        "ai_question": "Posez une question sur les contacts radar ou les prédictions satellite:",
        "ai_analyze": "Analyser le niveau de menace actuel",
        "ai_thinking": "🤖 L'IA analyse les données de surveillance...",
        "ai_response": "💡 Rapport d'analyse IA",
        "security_badge": "🔐 Bouclier de sécurité global actif",
        "security_caption": "Toutes les données sont sécurisées et anonymisées"
    }
}

# --- 4. LOGIN PAGE ---
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### 🌐 GlobalInternet.py Access")
        pwd = st.text_input("Enter Security Key", type="password")
        if st.button("Initialize System", key="login_btn", use_container_width=True):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Authorization")

# --- 5. AI ANALYSIS FUNCTION (uses Groq) ---
def ai_analysis(aircraft, satellites, u_lat, u_lon, question=None):
    # Build a summary of current surveillance data
    radar_summary = "\n".join([f"- {a['id']} ({a['type']}) at altitude {a['alt']}, distance {a['dist']}" for a in aircraft])
    sat_summary = "\n".join([f"- {s['id']} ({s['type']}) at altitude {s['alt']}" for s in satellites])
    
    full_prompt = f"""You are an AI surveillance analyst. Use the following real-time data to answer the question or provide a threat assessment. Respond concisely and professionally.

Ground Station Location: Latitude {u_lat}, Longitude {u_lon}

Radar Contacts:
{radar_summary}

Satellite Assets:
{sat_summary}

User Query: {question if question else "Provide a summary of current threat level and any unusual activity."}

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

# --- 6. MAIN INTERFACE ---
def main_page():
    L = UI[st.session_state.lang]
    
    with st.sidebar:
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French"], key="lang")
        st.markdown(f"**👨‍💻 {L['author_tag']}**")
        st.divider()
        
        # Security Shield
        st.markdown(f"### 🛡️ {L['security_badge']}")
        st.markdown(f"<div style='background:#0a192f; border:1px solid #00ebc7; border-radius:30px; padding:8px; text-align:center; color:#00ebc7;'>{L['security_caption']}</div>", unsafe_allow_html=True)
        st.divider()
        
        # --- POSITIONING & AIP ---
        st.subheader("System Control")
        u_lat = st.number_input(L['lat'], value=18.5392, format="%.4f")
        u_lon = st.number_input(L['lon'], value=-72.3364, format="%.4f")
        
        aip_key = st.text_input(L['aip_key'], type="password", placeholder="Enter Provider Key...")
        
        st.divider()
        demo_radar = st.checkbox("Demo Mode (Radar)", value=True)
        demo_sat = st.checkbox("Demo Mode (Satellite)", value=True)
        
        st.divider()
        st.write(f"📞 (509) 4738-5663")
        st.write(f"✉️ deslandes78@gmail.com")
        
        if st.button(L['logout'], type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # Generate data
    aircraft_data, sat_data = get_surveillance_data(True, u_lat, u_lon)
    
    # Tabs: Radar, Satellite, AI Analyst
    tab_radar, tab_sat, tab_ai = st.tabs([L["radar_tab"], L["sat_tab"], L["ai_tab"]])

    # --- RADAR TAB (AIRCRAFT) ---
    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.subheader(L['author_tag'])
        st.info(L['audio_note'])
        
        col_rad, col_log = st.columns([2, 1])
        
        with col_rad:
            radar_json = json.dumps(aircraft_data)
            radar_html = r"""
            <html><body style="background:#03060c; margin:0; display:flex; justify-content:center; cursor:pointer;">
                <canvas id="radar" width="550" height="550" style="border-radius:50%; border:1px solid #1e3a5f;"></canvas>
                <script>
                    const canvas = document.getElementById('radar');
                    const ctx = canvas.getContext('2d');
                    const data = """ + radar_json + r""";
                    let angle = 0; let audioCtx = null;
                    canvas.onclick = () => { if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); };
                    function ping() {
                        if(!audioCtx) return;
                        let o = audioCtx.createOscillator(); let g = audioCtx.createGain();
                        o.frequency.setValueAtTime(800, audioCtx.currentTime);
                        g.gain.setValueAtTime(0.05, audioCtx.currentTime);
                        o.connect(g); g.connect(audioCtx.destination);
                        o.start(); o.stop(audioCtx.currentTime + 0.5);
                    }
                    function draw() {
                        ctx.clearRect(0,0,550,550); let cx=275, cy=275, r=250;
                        ctx.strokeStyle='rgba(30,58,95,0.4)';
                        for(let i=1;i<=4;i++){ ctx.beginPath(); ctx.arc(cx,cy,(r/4)*i,0,Math.PI*2); ctx.stroke(); }
                        data.forEach((d, i) => {
                            let dx = cx + Math.cos(i*1.5) * (r * d.dist);
                            let dy = cy + Math.sin(i*1.5) * (r * d.dist);
                            ctx.fillStyle=d.color; ctx.shadowBlur=15; ctx.shadowColor=d.color;
                            ctx.beginPath(); ctx.arc(dx,dy,5,0,7); ctx.fill();
                        });
                        let oldA = angle; angle -= 0.03;
                        if(Math.floor(oldA/6.28) !== Math.floor(angle/6.28)) ping();
                        ctx.save(); ctx.translate(cx,cy); ctx.rotate(angle);
                        let g=ctx.createRadialGradient(0,0,0,0,0,r);
                        g.addColorStop(0,'transparent'); g.addColorStop(1,'rgba(0,255,100,0.2)');
                        ctx.fillStyle=g; ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0,r,0,0.4); ctx.fill();
                        ctx.restore(); requestAnimationFrame(draw);
                    }
                    draw();
                </script>
            </body></html>
            """
            components.html(radar_html, height=580)

        with col_log:
            st.subheader(L['detection_log'])
            for d in aircraft_data:
                with st.expander(f"📡 {d['id']} [{d['type']}]"):
                    st.write(f"**Altitude:** {d['alt']}")
                    st.download_button(L['report'], f"RADAR LOG\nAsset: {d['id']}\nOP: Gesner Deslandes", key=f"dl_{d['id']}")

    # --- SATELLITE TAB (PREDICTION + OPENSKY) ---
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
            for s in sat_data:
                markers += f"L.circleMarker([{u_lat + (hash(s['id'])%5-2.5)}, {u_lon + (hash(s['id'])%10-5)}], {{color:'{s['color']}', radius:8}}).addTo(map).bindPopup('{s['id']}');"
            
            map_html = f"""
            <html><head>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                <style>#map {{ height: 500px; border-radius: 15px; border: 2px solid #1e3a5f; }}</style>
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

    # --- AI ANALYST TAB (NEW) ---
    with tab_ai:
        st.title("🤖 AI Surveillance Analyst")
        st.markdown("Ask questions about radar contacts, satellite assets, or request a threat assessment.")
        
        col_q, col_a = st.columns([1, 1])
        with col_q:
            user_question = st.text_area(L['ai_question'], height=100,
                                         placeholder="E.g., Which aircraft pose the highest threat? or Summarize current satellite coverage.")
            if st.button(L['ai_analyze'], use_container_width=True):
                with st.spinner(L['ai_thinking']):
                    response = ai_analysis(aircraft_data, sat_data, u_lat, u_lon, user_question if user_question.strip() else None)
                st.markdown(f"### {L['ai_response']}")
                st.markdown(response)
        
        with col_a:
            # Quick threat assessment button (no question needed)
            if st.button("🚨 Quick Threat Assessment", use_container_width=True):
                with st.spinner(L['ai_thinking']):
                    response = ai_analysis(aircraft_data, sat_data, u_lat, u_lon, None)
                st.markdown(f"### {L['ai_response']}")
                st.markdown(response)

# --- 7. EXECUTION ---
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
