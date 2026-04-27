import streamlit as st
import streamlit.components.v1 as components
import base64

# --- CONFIGURATION ---
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance & Satellite", 
    layout="wide",
    page_icon="🔴"
)

# 1. Initialize session state keys immediately
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# 2. Define Translations
texts = {
    "English": {
        "title": "GLOBAL SURVEILLANCE RADAR",
        "subtitle": "Built by Gesner Deslandes",
        "sat_title": "LIVE SATELLITE TRACKER",
        "settings": "Radar Settings",
        "lat": "Radar Latitude",
        "lon": "Radar Longitude",
        "range": "Max Range (km)",
        "demo_radar": "Demo Mode (Radar)",
        "demo_sat": "Demo Mode (Satellite)",
        "license": "Software License",
        "logout": "Logout",
        "refresh": "Refresh System",
        "report": "Generate Satellite Report",
        "tabs": ["📡 Radar", "🛰️ Satellite Tracker"]
    },
    "French": {
        "title": "RADAR DE SURVEILLANCE MONDIAL",
        "subtitle": "Conçu par Gesner Deslandes",
        "sat_title": "SUIVI SATELLITE EN DIRECT",
        "settings": "Paramètres Radar",
        "lat": "Latitude Radar",
        "lon": "Longitude Radar",
        "range": "Portée Max (km)",
        "demo_radar": "Mode Démo (Radar)",
        "demo_sat": "Mode Démo (Satellite)",
        "license": "Licence Logicielle",
        "logout": "Déconnexion",
        "refresh": "Actualiser le Système",
        "report": "Générer Rapport Satellite",
        "tabs": ["📡 Radar", "🛰️ Suivi Satellite"]
    },
    "Spanish": {
        "title": "RADAR DE VIGILANCIA GLOBAL",
        "subtitle": "Construido por Gesner Deslandes",
        "sat_title": "RASTREADOR DE SATÉLITES",
        "settings": "Ajustes del Radar",
        "lat": "Latitud del Radar",
        "lon": "Longitud del Radar",
        "range": "Rango Máximo (km)",
        "demo_radar": "Modo Demo (Radar)",
        "demo_sat": "Modo Demo (Satelital)",
        "license": "Licencia de Software",
        "logout": "Cerrar sesión",
        "refresh": "Refrescar Sistema",
        "report": "Generar Informe Satelital",
        "tabs": ["📡 Radar", "🛰️ Rastreador Satelital"]
    }
}

# ----------------------------------------------------------------------
# LOGIN SCREEN
# ----------------------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("## 🔐 Secure Access Required")
        st.info("GlobalInternet.py - Proprietary Surveillance Suite")
        password = st.text_input("Access Key", type="password")
        if st.button("Authorize Access", use_container_width=True):
            if password == "20082010":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Security Key")
    st.stop()

# ----------------------------------------------------------------------
# SIDEBAR (Identity & Branding)
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌐 GlobalInternet.py")
    st.selectbox("Language / Langue / Idioma", ["English", "French", "Spanish"], key="lang")
    
    t = texts[st.session_state.lang]
    
    st.markdown(f"**👨‍💻 Gesner Deslandes**")
    st.caption("Founder & Python Builder")
    st.divider()
    
    st.markdown(f"### 📡 {t['settings']}")
    radar_lat = st.number_input(t['lat'], value=18.5333, format="%.5f")
    radar_lon = st.number_input(t['lon'], value=-72.3333, format="%.5f")
    max_range = st.number_input(t['range'], min_value=30, max_value=2000, value=500)
    
    demo_radar = st.checkbox(t['demo_radar'], value=False)
    demo_sat = st.checkbox(t['demo_sat'], value=False)
    
    st.divider()
    st.markdown("### 📞 Contact Details")
    st.write("**(509) 4738-5663**")
    st.write("deslandes78@gmail.com")
    st.markdown("[GlobalInternet.py Official](https://globalinternet.py)")
    
    st.divider()
    if st.button(t['logout'], type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ----------------------------------------------------------------------
# MAIN UI
# ----------------------------------------------------------------------
tab1, tab2 = st.tabs(t['tabs'])

with tab1:
    st.title(f"🔴 {t['title']}")
    st.subheader(f"{t['subtitle']}")
    
    # Radar HTML Component (550x550, CCW Sweep, Beep)
    radar_html = f"""
    <div style="background:#0a0f1e; padding:20px; border-radius:20px; text-align:center;">
        <canvas id="radarCanvas" width="550" height="550" style="background:#03060c; border-radius:50%; border:1px solid #1e3a5f;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('radarCanvas');
        const ctx = canvas.getContext('2d');
        let angle = 0;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function beep() {{
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.frequency.value = 880; gain.gain.value = 0.05;
            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
        }}

        function draw() {{
            ctx.clearRect(0,0,550,550);
            const cx = 275, cy = 275, r = 250;
            
            // CCW Sweep
            angle -= 0.02; 
            if(angle <= -Math.PI * 2) {{ angle = 0; beep(); }}

            // Rings
            ctx.strokeStyle = '#1e3a5f';
            for(let i=1; i<=4; i++) {{
                ctx.beginPath(); ctx.arc(cx, cy, (r/4)*i, 0, 7); ctx.stroke();
            }}

            // Sweep Line
            ctx.save();
            ctx.translate(cx, cy); ctx.rotate(angle);
            const grad = ctx.createRadialGradient(0,0,0,0,0,r);
            grad.addColorStop(0, 'rgba(0,255,100,0)');
            grad.addColorStop(1, 'rgba(0,255,100,0.3)');
            ctx.fillStyle = grad;
            ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0, r, 0, 0.4); ctx.fill();
            ctx.restore();
            
            // Watermark
            ctx.fillStyle = "rgba(0, 255, 100, 0.5)";
            ctx.font = "10px Monospace";
            ctx.fillText("Built by Gesner Deslandes", 380, 530);

            requestAnimationFrame(draw);
        }}
        draw();
    </script>
    """
    components.html(radar_html, height=600)

with tab2:
    st.title(f"🛰️ {t['sat_title']}")
    
    col_map, col_list = st.columns([2, 1])
    
    with col_list:
        st.write("### Target Assets")
        # Clickable Asset Logic
        if demo_sat:
            assets = ["GeoEye-1", "Landsat-9", "NOAA-20", "Starlink-V2", "GPS-III"]
        else:
            assets = ["ISS", "HUBBLE", "TIANGONG"]
            
        for asset in assets:
            if st.button(f"🔍 {asset}", use_container_width=True):
                data = f"Name: {asset}\\nType: Surveillance\\nAlt: 415km\\nVel: 7.6km/s"
                st.download_button(t['report'], data, file_name=f"{asset}_report.txt")
    
    with col_map:
        # Map Refresh with sound
        map_html = """
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <div id="map" style="height: 500px; border-radius:15px; background:#03060c;"></div>
        <script>
            const map = L.map('map', {zoomControl: false}).setView([20, 0], 2);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png').addTo(map);
            
            const audio = new AudioContext();
            setInterval(() => {
                const o = audio.createOscillator();
                const g = audio.createGain();
                o.connect(g); g.connect(audio.destination);
                o.frequency.value = 1200; g.gain.value = 0.02;
                o.start(); o.stop(audio.currentTime + 0.05);
            }, 5000);
        </script>
        """
        components.html(map_html, height=520)

# --- FOOTER ---
st.divider()
st.caption(f"© 2026 GlobalInternet.py | {t['license']}")
