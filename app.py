import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance & Satellite", 
    layout="wide", 
    page_icon="🌐"
)

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- 2. SECURITY GATE ---
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### 🌐 GlobalInternet.py Access")
        pwd = st.text_input("Enter Security Key", type="password")
        if st.button("Initialize System", use_container_width=True):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Authorization")
    st.stop()

# --- 3. TRANSLATIONS ---
UI = {
    "English": {
        "radar_tab": "📡 Radar", "sat_tab": "🛰️ Satellite",
        "title": "GLOBAL SURVEILLANCE RADAR", "subtitle": "Built by Gesner Deslandes",
        "settings": "System Settings", "demo_r": "Demo Mode (Radar)", "demo_s": "Demo Mode (Satellite)",
        "logout": "Terminate Session", "report": "Download Asset Report",
        "contact": "Contact & Support", "license": "Proprietary License"
    },
    "French": {
        "radar_tab": "📡 Radar", "sat_tab": "🛰️ Satellite",
        "title": "RADAR DE SURVEILLANCE MONDIAL", "subtitle": "Conçu par Gesner Deslandes",
        "settings": "Paramètres Système", "demo_r": "Mode Démo (Radar)", "demo_s": "Mode Démo (Satellite)",
        "logout": "Déconnexion", "report": "Télécharger le Rapport",
        "contact": "Contact & Support", "license": "Licence Propriétaire"
    },
    "Spanish": {
        "radar_tab": "📡 Radar", "sat_tab": "🛰️ Satélite",
        "title": "RADAR DE VIGILANCIA GLOBAL", "subtitle": "Construido por Gesner Deslandes",
        "settings": "Ajustes del Sistema", "demo_r": "Modo Demo (Radar)", "demo_s": "Modo Demo (Satélite)",
        "logout": "Cerrar Sesión", "report": "Descargar Informe",
        "contact": "Contacto y Soporte", "license": "Licencia Propietaria"
    }
}

# --- 4. SIDEBAR & BRANDING ---
with st.sidebar:
    st.title("🌐 GlobalInternet.py")
    st.selectbox("Language / Langue / Idioma", ["English", "French", "Spanish"], key="lang")
    L = UI[st.session_state.lang] # Current translation object
    
    st.markdown(f"**👨‍💻 Gesner Deslandes**")
    st.caption("Founder & Python Builder")
    st.divider()
    
    st.markdown(f"### ⚙️ {L['settings']}")
    demo_radar = st.checkbox(L['demo_r'], value=False)
    demo_sat = st.checkbox(L['demo_s'], value=False)
    
    st.divider()
    st.markdown(f"### 📞 {L['contact']}")
    st.write("📱 (509) 4738-5663")
    st.write("✉️ deslandes78@gmail.com")
    
    st.divider()
    if st.button(L['logout'], type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- 5. MAIN INTERFACE ---
tab_radar, tab_sat = st.tabs([L["radar_tab"], L["sat_tab"]])

with tab_radar:
    st.title(f"🔴 {L['title']}")
    st.subheader(L['subtitle'])
    
    # 550x550 Radar | CCW Sweep | Audio Beep
    radar_html = f"""
    <div style="background:#03060c; padding:20px; border-radius:20px; display:flex; justify-content:center;">
        <canvas id="rCanvas" width="550" height="550" style="border:1px solid #1e3a5f; border-radius:50%;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('rCanvas');
        const ctx = canvas.getContext('2d');
        let angle = 0;
        const audio = new (window.AudioContext || window.webkitAudioContext)();

        function beep() {{
            const osc = audio.createOscillator();
            const gain = audio.createGain();
            osc.connect(gain); gain.connect(audio.destination);
            osc.frequency.value = 900; gain.gain.value = 0.03;
            osc.start(); osc.stop(audio.currentTime + 0.1);
        }}

        function draw() {{
            ctx.clearRect(0,0,550,550);
            const cx = 275, cy = 275, r = 250;
            
            // Background Rings
            ctx.strokeStyle = '#1e3a5f';
            for(let i=1; i<=4; i++) {{
                ctx.beginPath(); ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2); ctx.stroke();
            }}

            // CCW Sweep (Minus operator)
            angle -= 0.025;
            if(angle <= -Math.PI * 2) {{ angle = 0; beep(); }}

            ctx.save();
            ctx.translate(cx, cy); ctx.rotate(angle);
            const grad = ctx.createRadialGradient(0,0,0,0,0,r);
            grad.addColorStop(0, 'rgba(0,255,100,0)');
            grad.addColorStop(1, 'rgba(0,255,100,0.3)');
            ctx.fillStyle = grad;
            ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0, r, 0, 0.4); ctx.fill();
            ctx.restore();

            requestAnimationFrame(draw);
        }}
        draw();
    </script>
    """
    components.html(radar_html, height=600)

with tab_sat:
    st.title(f"🛰️ {L['sat_title']}")
    
    col_map, col_list = st.columns([2, 1])
    
    with col_list:
        st.subheader("Target Assets")
        # Asset logic: Real or Demo
        assets = [
            {"id": "ISS", "type": "Scientific", "alt": "408km"},
            {"id": "Hubble", "type": "Telescope", "alt": "540km"},
            {"id": "Tiangong", "type": "Scientific", "alt": "385km"}
        ] if not demo_sat else [
            {"id": "Starlink-14", "type": "Comm", "alt": "550km"},
            {"id": "GPS-III", "type": "Nav", "alt": "20200km"},
            {"id": "GeoEye-1", "type": "Imagery", "alt": "680km"}
        ]
        
        for sat in assets:
            with st.expander(f"🛰️ {sat['id']}"):
                st.write(f"**Type:** {sat['type']} | **Alt:** {sat['alt']}")
                report_data = f"Asset: {sat['id']}\\nType: {sat['type']}\\nAlt: {sat['alt']}\\nGenerated: {datetime.now()}"
                st.download_button(L['report'], report_data, file_name=f"{sat['id']}_report.txt", key=sat['id'])

    with col_map:
        # Dark Leaflet Map + 5s Beep
        map_html = """
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <div id="map" style="height: 500px; border-radius:15px; border:1px solid #1e3a5f;"></div>
        <script>
            const map = L.map('map', {zoomControl: false}).setView([20, 0], 2);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png').addTo(map);
            
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            setInterval(() => {
                const o = audioCtx.createOscillator();
                const g = audioCtx.createGain();
                o.connect(g); g.connect(audioCtx.destination);
                o.frequency.value = 1100; g.gain.value = 0.02;
                o.start(); o.stop(audioCtx.currentTime + 0.05);
            }, 5000);
        </script>
        """
        components.html(map_html, height=520)

# --- 6. FOOTER ---
st.divider()
st.caption(f"Copyright © 2026 GlobalInternet.py | {L['license']}")
