import streamlit as st
import json
import random
from datetime import datetime, timedelta
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

# --- 2. ADVANCED DATA GENERATOR ---
def get_simulated_assets(is_demo, lat_base, lon_base):
    if not is_demo:
        return []
    
    # Categories of satellites with simulated offsets for prediction
    categories = [
        {"id": "SL-5122", "type": "Starlink (Comms)", "color": "#00ff64", "alt": "550km"},
        {"id": "NAV-GPS", "type": "GPS Block III", "color": "#00bfff", "alt": "20,200km"},
        {"id": "KH-11", "type": "Keyhole (Spy)", "color": "#ff3300", "alt": "350km"},
        {"id": "NOAA-19", "type": "Weather/Met", "color": "#ffcc00", "alt": "870km"},
        {"id": "ISS", "type": "Space Station", "color": "#ffffff", "alt": "408km"}
    ]
    
    assets = []
    for i, cat in enumerate(categories):
        # Create simulated paths based on current location
        assets.append({
            "id": cat["id"],
            "type": cat["type"],
            "lat": lat_base + (math_offset := random.uniform(-5, 5)),
            "lon": lon_base + random.uniform(-10, 10),
            "alt": cat["alt"],
            "color": cat["color"],
            "velocity": random.uniform(7.5, 7.8) # km/s for LEO
        })
    return assets

# --- 3. TRANSLATION DICTIONARY ---
UI = {
    "English": {
        "radar_tab": "📡 Radar Control", "sat_tab": "🛰️ Satellite Tracker",
        "title": "GLOBAL SURVEILLANCE RADAR", "author_tag": "Built by Gesner Deslandes",
        "logout": "Terminate Session", "report": "Download Asset Report",
        "detection_log": "Live Detection Log", "sat_engine": "Predictive Mapping Engine",
        "audio_note": "Click radar to enable sonar audio.", "lat": "Latitude", "lon": "Longitude",
        "predict_btn": "Predict Next Pass", "time_target": "Target Date/Time"
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar", "sat_tab": "🛰️ Suivi Satellite",
        "title": "RADAR DE SURVEILLANCE MONDIAL", "author_tag": "Conçu par Gesner Deslandes",
        "logout": "Déconnexion", "report": "Télécharger le Rapport",
        "detection_log": "Journal de Détection", "sat_engine": "Moteur de Cartographie Prédictive",
        "audio_note": "Cliquez sur le radar pour l'audio.", "lat": "Latitude", "lon": "Longitude",
        "predict_btn": "Prédire le Passage", "time_target": "Date/Heure Cible"
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
        
        st.subheader("System Configuration")
        u_lat = st.number_input(L['lat'], value=18.5392, format="%.4f")
        u_lon = st.number_input(L['lon'], value=-72.3364, format="%.4f")
        
        st.divider()
        demo_radar = st.checkbox("Demo Mode (Radar)", value=True)
        demo_sat = st.checkbox("Demo Mode (Satellite)", value=True)
        
        st.divider()
        st.write(f"📞 (509) 4738-5663")
        st.write(f"✉️ deslandes78@gmail.com")
        
        if st.button(L['logout'], type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    tab_radar, tab_sat = st.tabs([L["radar_tab"], L["sat_tab"]])

    # --- RADAR TAB (AIRCRAFT/UAV) ---
    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.subheader(L['author_tag'])
        
        col_rad, col_log = st.columns([2, 1])
        
        with col_rad:
            # Simulation of aircraft (Commercial, Military, Drones)
            aircraft = [
                {"id": "AAL-102", "type": "Commercial", "color": "#00ff64", "alt": "32k ft"},
                {"id": "F22-SPT", "type": "Military", "color": "#ff3300", "alt": "55k ft"},
                {"id": "MQ9-DRN", "type": "Drone/UAV", "color": "#ffcc00", "alt": "15k ft"}
            ] if demo_radar else []
            
            radar_json = json.dumps(aircraft)
            radar_html = r"""
            <html><body style="background:#03060c; margin:0; display:flex; justify-content:center; cursor:pointer;">
                <canvas id="radar" width="500" height="500" style="border-radius:50%; border:1px solid #1e3a5f;"></canvas>
                <script>
                    const canvas = document.getElementById('radar');
                    const ctx = canvas.getContext('2d');
                    const data = """ + radar_json + r""";
                    let angle = 0; let audioCtx = null;
                    canvas.onclick = () => { if(!audioCtx) audioCtx = new AudioContext(); };
                    function ping() {
                        if(!audioCtx) return;
                        let o = audioCtx.createOscillator(); let g = audioCtx.createGain();
                        o.frequency.setValueAtTime(800, audioCtx.currentTime);
                        g.gain.setValueAtTime(0.05, audioCtx.currentTime);
                        o.connect(g); g.connect(audioCtx.destination);
                        o.start(); o.stop(audioCtx.currentTime + 0.3);
                    }
                    function draw() {
                        ctx.clearRect(0,0,500,500); let cx=250, cy=250, r=240;
                        ctx.strokeStyle='rgba(30,58,95,0.4)';
                        for(let i=1;i<=4;i++){ ctx.beginPath(); ctx.arc(cx,cy,(r/4)*i,0,Math.PI*2); ctx.stroke(); }
                        data.forEach((d, i) => {
                            ctx.fillStyle=d.color; ctx.beginPath(); ctx.arc(cx+Math.cos(i)*150, cy+Math.sin(i)*150, 5, 0, 7); ctx.fill();
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
            components.html(radar_html, height=520)

    # --- SATELLITE TAB (PREDICTION & TRACKING) ---
    with tab_sat:
        st.title(f"🛰️ {L['sat_tab']}")
        st.subheader(L['author_tag'])
        
        col_ctrl, col_map = st.columns([1, 2])
        
        with col_ctrl:
            st.subheader("Prediction Logic")
            target_date = st.date_input(L['time_target'], datetime.now())
            target_time = st.time_input("Target Time", datetime.now().time())
            
            # Simulated Calculation
            full_target = datetime.combine(target_date, target_time)
            st.write(f"Calculating trajectories for: `{full_target}`")
            
            sat_assets = get_simulated_assets(demo_sat, u_lat, u_lon)
            
            for s in sat_assets:
                with st.expander(f"🛰️ {s['id']} | {s['type']}"):
                    st.write(f"**Alt:** {s['alt']}")
                    # Simple simulation: move satellite based on time difference
                    diff_hours = (full_target - datetime.now()).total_seconds() / 3600
                    future_lat = s['lat'] + (diff_hours * 2) # Mock orbital drift
                    future_lon = s['lon'] + (diff_hours * 15) # Mock Earth rotation factor
                    
                    st.success(f"Predicted Pass: {future_lat:.2f}N, {future_lon:.2f}W")
                    st.download_button(L['report'], f"PREDICTION REPORT\nAsset: {s['id']}\nTime: {full_target}\nLoc: {future_lat}, {future_lon}\nLead: Gesner Deslandes", key=s['id'])

        with col_map:
            # Mapping future markers
            markers_js = ""
            for s in sat_assets:
                # Add current and predicted path markers
                markers_js += f"L.circleMarker([{s['lat']}, {s['lon']}], {{color: '{s['color']}', radius: 8}}).addTo(map).bindPopup('Current: {s['id']}');"
            
            map_html = f"""
            <html><head>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                <style>#map {{ height: 500px; border-radius: 15px; border: 2px solid #1e3a5f; }}</style>
            </head><body>
                <div id="map"></div>
                <script>
                    const map = L.map('map', {{zoomControl: false}}).setView([{u_lat}, {u_lon}], 3);
                    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
                    {markers_js}
                </script>
            </body></html>
            """
            components.html(map_html, height=550)

# --- 6. EXECUTION ---
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
