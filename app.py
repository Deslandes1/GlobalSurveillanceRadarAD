import streamlit as st
import json
from datetime import datetime
import streamlit.components.v1 as components

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

# Data for Radar & Satellite Detections
if "radar_detections" not in st.session_state:
    st.session_state.radar_detections = [
        {"id": "SIG-01", "type": "Unidentified Aerial", "coord": "18.5N, 72.3W"},
        {"id": "SIG-09", "type": "Weather Balloon", "coord": "19.1N, 71.8W"},
        {"id": "SIG-14", "type": "Commercial Flight", "coord": "18.2N, 73.1W"}
    ]

# --- 2. TRANSLATION DICTIONARY ---
UI = {
    "English": {
        "radar_tab": "📡 Radar Control", 
        "sat_tab": "🛰️ Satellite Tracker",
        "title": "GLOBAL SURVEILLANCE RADAR", 
        "author_tag": "Built by Gesner Deslandes",
        "logout": "Terminate Session", 
        "report": "Download Asset Report",
        "detection_log": "Live Detection Log",
        "sat_engine": "Satellite Mapping Engine",
        "audio_note": "Click the radar to enable sonar audio.",
        "coord_select": "Coordinate Targeting",
        "lat": "Latitude", "lon": "Longitude"
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar", 
        "sat_tab": "🛰️ Suivi Satellite",
        "title": "RADAR DE SURVEILLANCE MONDIAL", 
        "author_tag": "Conçu par Gesner Deslandes",
        "logout": "Déconnexion", 
        "report": "Télécharger le Rapport",
        "detection_log": "Journal de Détection",
        "sat_engine": "Moteur de Cartographie Satellite",
        "audio_note": "Cliquez sur le radar pour activer l'audio sonar.",
        "coord_select": "Ciblage des Coordonnées",
        "lat": "Latitude", "lon": "Longitude"
    }
}

# --- 3. LOGIN PAGE ---
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

# --- 4. MAIN INTERFACE ---
def main_page():
    L = UI[st.session_state.lang]
    
    with st.sidebar:
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French"], key="lang")
        st.markdown(f"**👨‍💻 {L['author_tag']}**")
        st.divider()
        
        # --- NEW: LAT/LON SIDEBAR SELECTOR ---
        st.subheader(L['coord_select'])
        preset = st.selectbox("Preset Targets", ["Manual Entry", "Port-au-Prince (HQ)", "ISS Current Path", "Paris Signal"])
        
        # Map presets to values
        default_lat, default_lon = 18.53, -72.33
        if preset == "Port-au-Prince (HQ)":
            default_lat, default_lon = 18.53, -72.33
        elif preset == "ISS Current Path":
            default_lat, default_lon = 45.0, -10.0
        elif preset == "Paris Signal":
            default_lat, default_lon = 48.85, 2.35
            
        u_lat = st.number_input(L['lat'], value=default_lat, format="%.4f")
        u_lon = st.number_input(L['lon'], value=default_lon, format="%.4f")
        
        st.divider()
        demo_radar = st.checkbox("Demo Mode (Radar)", value=False, key="check_demo_r")
        demo_sat = st.checkbox("Demo Mode (Satellite)", value=False, key="check_demo_s")
        
        st.divider()
        st.write(f"📞 (509) 4738-5663")
        st.write(f"✉️ deslandes78@gmail.com")
        
        if st.button(L['logout'], key="sidebar_logout_btn", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    tab_radar, tab_sat = st.tabs([L["radar_tab"], L["sat_tab"]])

    # --- RADAR TAB ---
    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.subheader(L['author_tag'])
        st.info(f"{L['audio_note']} | Current Lock: {u_lat}, {u_lon}")
        
        col_rad, col_log = st.columns([2, 1])
        
        with col_rad:
            radar_html = r"""
            <html>
            <body style="background:#03060c; margin:0; display:flex; justify-content:center; cursor:pointer;">
                <canvas id="radar" width="550" height="550" style="border:1px solid #1e3a5f; border-radius:50%;"></canvas>
                <script>
                    const canvas = document.getElementById('radar');
                    const ctx = canvas.getContext('2d');
                    let angle = 0;
                    let audioCtx = null;
                    canvas.addEventListener('click', () => {
                        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    });
                    function playPing() {
                        if (!audioCtx) return;
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.5);
                        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                        osc.connect(gain); gain.connect(audioCtx.destination);
                        osc.start(); osc.stop(audioCtx.currentTime + 0.5);
                    }
                    function draw() {
                        ctx.clearRect(0,0,550,550);
                        const cx = 275, cy = 275, r = 250;
                        ctx.strokeStyle = 'rgba(30, 58, 95, 0.5)';
                        for(let i=1; i<=4; i++) {
                            ctx.beginPath(); ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2); ctx.stroke();
                        }
                        let prevAngle = angle;
                        angle -= 0.03; 
                        if (Math.floor(prevAngle / (Math.PI*2)) !== Math.floor(angle / (Math.PI*2))) playPing();
                        ctx.save();
                        ctx.translate(cx, cy); ctx.rotate(angle);
                        const g = ctx.createRadialGradient(0,0,0,0,0,r);
                        g.addColorStop(0, 'rgba(0,255,100,0)');
                        g.addColorStop(1, 'rgba(0,255,100,0.3)');
                        ctx.fillStyle = g;
                        ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0, r, 0, 0.4); ctx.fill();
                        ctx.restore();
                        requestAnimationFrame(draw);
                    }
                    draw();
                </script>
            </body>
            </html>
            """
            components.html(radar_html, height=580)

        with col_log:
            st.subheader(L['detection_log'])
            for det in st.session_state.radar_detections:
                with st.expander(f"📡 {det['id']}"):
                    st.write(f"**Type:** {det['type']}")
                    st.write(f"**Coordinates:** {det['coord']}")
                    report = f"RADAR REPORT\nID: {det['id']}\nOP: Gesner Deslandes\nDATE: {datetime.now()}"
                    st.download_button(L['report'], report, key=f"rad_{det['id']}")

    # --- SATELLITE TAB ---
    with tab_sat:
        st.title(f"🛰️ {L['sat_tab']}")
        st.subheader(L['author_tag'])
        
        col_list, col_map = st.columns([1, 2])
        
        with col_list:
            st.subheader("Asset Management")
            sat_assets = [{"name": "ISS", "status": "Stable"}, {"name": "HUBBLE", "status": "Active"}]
            for sat in sat_assets:
                with st.container(border=True):
                    st.write(f"**Target:** {sat['name']}")
                    sat_report = f"SATELLITE DATA LOG\nAsset: {sat['name']}\nTimestamp: {datetime.now()}\nResearcher: Gesner Deslandes"
                    st.download_button(L['report'], sat_report, key=f"dl_sat_{sat['name']}")

        with col_map:
            st.subheader(L['sat_engine'])
            # Leaflet.js with dynamic sidebar coordinates
            map_html = f"""
            <html>
            <head>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                <style>#map {{ height: 500px; border-radius: 15px; border: 2px solid #1e3a5f; }}</style>
            </head>
            <body>
                <div id="map"></div>
                <script>
                    const map = L.map('map', {{zoomControl: false}}).setView([{u_lat}, {u_lon}], 6);
                    L.tileLayer('https://{{s}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
                    L.circleMarker([{u_lat}, {u_lon}], {{color: '#00ff64', radius: 10}}).addTo(map)
                        .bindPopup('Active Lock: {u_lat}, {u_lon}').openPopup();
                </script>
            </body>
            </html>
            """
            components.html(map_html, height=550)

# --- 5. EXECUTION ---
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
