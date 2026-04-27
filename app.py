import streamlit as st
import json
import random
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

# --- 2. DEMO DATA GENERATOR ---
def get_radar_data(is_demo):
    if not is_demo:
        return [
            {"id": "CIV-442", "type": "Commercial", "coord": "18.5N, 72.3W", "alt": "32,000ft", "color": "#00ff64"},
            {"id": "MIL-X9", "type": "Military", "coord": "19.1N, 71.8W", "alt": "45,000ft", "color": "#ff3300"}
        ]
    else:
        # Simulated "Demo" detections across all types
        return [
            {"id": "AAL-120", "type": "Commercial Aircraft", "coord": "18.53N, 72.33W", "alt": "30,000ft", "color": "#00ff64"},
            {"id": "F-35-TAC", "type": "Military Strike", "coord": "18.90N, 72.10W", "alt": "48,000ft", "color": "#ff3300"},
            {"id": "DJI-PH4", "type": "Civilian Drone", "coord": "18.55N, 72.35W", "alt": "400ft", "color": "#ffcc00"},
            {"id": "G-STRAT", "type": "Military UAV", "coord": "19.20N, 71.50W", "alt": "65,000ft", "color": "#ff3300"},
            {"id": "CESS-172", "type": "Private Civil", "coord": "18.40N, 72.60W", "alt": "5,000ft", "color": "#00ff64"},
            {"id": "UNK-SIG", "type": "Unidentified Object", "coord": "18.72N, 72.45W", "alt": "12,000ft", "color": "#ffffff"}
        ]

# --- 3. TRANSLATION DICTIONARY ---
UI = {
    "English": {
        "radar_tab": "📡 Radar Control", "sat_tab": "🛰️ Satellite Tracker",
        "title": "GLOBAL SURVEILLANCE RADAR", "author_tag": "Built by Gesner Deslandes",
        "logout": "Terminate Session", "report": "Download Asset Report",
        "detection_log": "Live Detection Log", "sat_engine": "Satellite Mapping Engine",
        "audio_note": "Click radar to enable sonar audio.", "lat": "Latitude", "lon": "Longitude"
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar", "sat_tab": "🛰️ Suivi Satellite",
        "title": "RADAR DE SURVEILLANCE MONDIAL", "author_tag": "Conçu par Gesner Deslandes",
        "logout": "Déconnexion", "report": "Télécharger le Rapport",
        "detection_log": "Journal de Détection", "sat_engine": "Moteur de Cartographie Satellite",
        "audio_note": "Cliquez sur le radar pour activer l'audio.", "lat": "Latitude", "lon": "Longitude"
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

# --- 5. MAIN INTERFACE ---
def main_page():
    L = UI[st.session_state.lang]
    
    with st.sidebar:
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French"], key="lang")
        st.markdown(f"**👨‍💻 {L['author_tag']}**")
        st.divider()
        
        # Coordinate Target
        st.subheader("Targeting")
        u_lat = st.number_input(L['lat'], value=18.5392, format="%.4f")
        u_lon = st.number_input(L['lon'], value=-72.3364, format="%.4f")
        
        st.divider()
        demo_radar = st.checkbox("Demo Mode (Radar)", value=True, key="check_demo_r")
        demo_sat = st.checkbox("Demo Mode (Satellite)", value=True, key="check_demo_s")
        
        st.divider()
        st.write(f"📞 (509) 4738-5663")
        st.write(f"✉️ deslandes78@gmail.com")
        
        if st.button(L['logout'], key="sidebar_logout_btn", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    tab_radar, tab_sat = st.tabs([L["radar_tab"], L["sat_tab"]])

    # Current detections based on Demo status
    current_detections = get_radar_data(demo_radar)

    # --- RADAR TAB ---
    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.subheader(L['author_tag'])
        st.info(f"{L['audio_note']}")
        
        col_rad, col_log = st.columns([2, 1])
        
        with col_rad:
            # Injecting detections into JS for visual representation
            detections_json = json.dumps(current_detections)
            radar_html = r"""
            <html>
            <body style="background:#03060c; margin:0; display:flex; justify-content:center; cursor:pointer;">
                <canvas id="radar" width="550" height="550" style="border:1px solid #1e3a5f; border-radius:50%;"></canvas>
                <script>
                    const canvas = document.getElementById('radar');
                    const ctx = canvas.getContext('2d');
                    const detections = """ + detections_json + r""";
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
                        gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
                        gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.5);
                        osc.connect(gain); gain.connect(audioCtx.destination);
                        osc.start(); osc.stop(audioCtx.currentTime + 0.5);
                    }

                    function draw() {
                        ctx.clearRect(0,0,550,550);
                        const cx = 275, cy = 275, r = 250;
                        
                        // Rings
                        ctx.strokeStyle = 'rgba(30, 58, 95, 0.4)';
                        for(let i=1; i<=4; i++) {
                            ctx.beginPath(); ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2); ctx.stroke();
                        }

                        // Detections (Blips)
                        detections.forEach((d, i) => {
                            const d_x = cx + Math.cos(i) * (r * 0.6);
                            const d_y = cy + Math.sin(i) * (r * 0.6);
                            ctx.fillStyle = d.color;
                            ctx.beginPath(); ctx.arc(d_x, d_y, 4, 0, Math.PI*2); ctx.fill();
                            ctx.shadowBlur = 10; ctx.shadowColor = d.color;
                        });

                        // Sweep
                        let prevAngle = angle;
                        angle -= 0.03; 
                        if (Math.floor(prevAngle / (Math.PI*2)) !== Math.floor(angle / (Math.PI*2))) playPing();
                        
                        ctx.save();
                        ctx.translate(cx, cy); ctx.rotate(angle);
                        const g = ctx.createRadialGradient(0,0,0,0,0,r);
                        g.addColorStop(0, 'rgba(0,255,100,0)');
                        g.addColorStop(1, 'rgba(0,255,100,0.2)');
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
            for det in current_detections:
                with st.expander(f"📡 {det['id']} ({det['type']})"):
                    st.write(f"**Status:** Tracking Active")
                    st.write(f"**Altitude:** {det['alt']}")
                    st.write(f"**Loc:** {det['coord']}")
                    report = f"RADAR TRACKING LOG\nID: {det['id']}\nTYPE: {det['type']}\nALT: {det['alt']}\nOP: Gesner Deslandes"
                    st.download_button(L['report'], report, key=f"rad_{det['id']}")

    # --- SATELLITE TAB ---
    with tab_sat:
        st.title(f"🛰️ {L['sat_tab']}")
        st.subheader(L['author_tag'])
        
        col_list, col_map = st.columns([1, 2])
        
        with col_list:
            st.subheader("Simulated Orbital Assets")
            sat_list = [
                {"name": "STARLINK-V2", "owner": "SpaceX", "task": "Comms Relay"},
                {"name": "KH-11", "owner": "NRO", "task": "Imagery"},
                {"name": "SENTINEL-6", "owner": "ESA", "task": "Topography"}
            ] if demo_sat else [{"name": "ISS", "owner": "Global", "task": "Research"}]
            
            for s in sat_list:
                with st.container(border=True):
                    st.write(f"**Asset:** {s['name']}")
                    st.caption(f"Operator: {s['owner']} | Task: {s['task']}")
                    st.download_button(L['report'], f"Telemetry data for {s['name']}", key=f"dl_sat_{s['name']}")

        with col_map:
            st.subheader(L['sat_engine'])
            # Leaflet with Demo Markers
            markers_js = ""
            if demo_sat:
                markers_js = f"L.circleMarker([{u_lat + 0.1}, {u_lon + 0.1}], {{color: '#ff3300', radius: 8}}).addTo(map).bindPopup('Military Signal');"
                markers_js += f"L.circleMarker([{u_lat - 0.2}, {u_lon + 0.3}], {{color: '#00ff64', radius: 6}}).addTo(map).bindPopup('Civilian Flight');"

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
                    const map = L.map('map', {{ zoomControl: false }}).setView([{u_lat}, {u_lon}], 8);
                    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
                    L.circleMarker([{u_lat}, {u_lon}], {{ color: '#00ff64', radius: 10 }}).addTo(map).bindPopup('Primary Lock');
                    {markers_js}
                </script>
            </body>
            </html>
            """
            components.html(map_html, height=550)

# --- 6. EXECUTION ---
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
