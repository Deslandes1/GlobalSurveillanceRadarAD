import streamlit as st
import streamlit.components.v1 as components
import json
import base64

# --- INITIAL CONFIGURATION ---
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance & Satellite", 
    layout="wide",
    page_icon="📡"
)

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- TRANSLATIONS DICTIONARY ---
t_dict = {
    "English": {
        "title": "GLOBAL SURVEILLANCE RADAR",
        "sat_title": "SATELLITE TRACKER",
        "founder": "Founder & Python Builder: Gesner Deslandes",
        "settings": "Radar Settings",
        "lat": "Radar Latitude",
        "lon": "Radar Longitude",
        "range": "Max Range (km)",
        "demo_radar": "Demo Mode (Radar)",
        "demo_sat": "Demo Mode (Satellite)",
        "license": "Software License",
        "contact": "Licensing & Support",
        "logout": "Logout",
        "refresh": "Refresh System",
        "details": "DETAILED REPORT",
        "download": "Download Report",
        "download_all": "Download All CSV",
        "sat_refresh": "Refreshes every 5s"
    },
    "French": {
        "title": "RADAR DE SURVEILLANCE MONDIAL",
        "sat_title": "SUIVI SATELLITE",
        "founder": "Fondateur et Développeur Python : Gesner Deslandes",
        "settings": "Paramètres Radar",
        "lat": "Latitude Radar",
        "lon": "Longitude Radar",
        "range": "Portée Max (km)",
        "demo_radar": "Mode Démo (Radar)",
        "demo_sat": "Mode Démo (Satellite)",
        "license": "Licence Logicielle",
        "contact": "Licence et Support",
        "logout": "Déconnexion",
        "refresh": "Actualiser le Système",
        "details": "RAPPORT DÉTAILLÉ",
        "download": "Télécharger le Rapport",
        "download_all": "Télécharger tout (CSV)",
        "sat_refresh": "S'actualise toutes les 5s"
    },
    "Spanish": {
        "title": "RADAR DE VIGILANCIA GLOBAL",
        "sat_title": "RASTREADOR DE SATÉLITES",
        "founder": "Fundador y Desarrollador Python: Gesner Deslandes",
        "settings": "Ajustes del Radar",
        "lat": "Latitud del Radar",
        "lon": "Longitud del Radar",
        "range": "Rango Máximo (km)",
        "demo_radar": "Modo Demo (Radar)",
        "demo_sat": "Modo Demo (Satelital)",
        "license": "Licencia de Software",
        "contact": "Licencia y Soporte",
        "logout": "Cerrar sesión",
        "refresh": "Refrescar Sistema",
        "details": "INFORME DETALLADO",
        "download": "Descargar Informe",
        "download_all": "Descargar todo (CSV)",
        "sat_refresh": "Actualiza cada 5s"
    }
}

# ----------------------------------------------------------------------
# 1. LOGIN SCREEN
# ----------------------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("### 🌐 GlobalInternet.py Access")
        password = st.text_input("Enter System Password", type="password")
        if st.button("Access System", use_container_width=True):
            if password == "20082010":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Password")
    st.stop()

# ----------------------------------------------------------------------
# 2. SIDEBAR & BRANDING
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌐 GlobalInternet.py")
    st.selectbox("Language / Langue / Idioma", ["English", "French", "Spanish"], key="lang")
    t = t_dict[st.session_state.lang]
    
    st.caption(f"👨‍💻 {t['founder']}")
    st.divider()
    
    st.markdown(f"### 📡 {t['settings']}")
    radar_lat = st.number_input(t['lat'], value=18.5333, format="%.5f") # Default Haiti
    radar_lon = st.number_input(t['lon'], value=-72.3333, format="%.5f")
    max_range = st.number_input(t['range'], value=500)
    
    demo_radar = st.checkbox(t['demo_radar'], value=False)
    demo_sat = st.checkbox(t['demo_sat'], value=False)
    
    st.divider()
    st.markdown(f"### 📞 {t['contact']}")
    st.write("**(509) 4738-5663**")
    st.write("deslandes78@gmail.com")
    st.markdown("[Visit Website](https://globalinternet.py)")
    
    st.divider()
    if st.button(t['logout'], type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ----------------------------------------------------------------------
# 3. MAIN UI TABS
# ----------------------------------------------------------------------
tab_radar, tab_sat = st.tabs([f"📡 {t['title']}", f"🛰️ {t['sat_title']}"])

with tab_radar:
    st.title(f"🔴 {t['title']}")
    # Radar Canvas logic (550x550, CCW sweep, Beep)
    # We use a raw string for JS to avoid curly brace issues
    radar_js = """
    <script>
        const canvasSize = 550;
        const center = canvasSize / 2;
        const radius = center - 20;
        let angle = 0;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function beep() {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.frequency.value = 800; gain.gain.value = 0.05;
            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
        }

        function drawRadar() {
            const canvas = document.getElementById('radarCanvas');
            if(!canvas) return;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0,0,canvasSize,canvasSize);
            
            // Rings
            ctx.strokeStyle = '#1e3a5f';
            for(let i=1; i<=4; i++) {
                ctx.beginPath(); ctx.arc(center, center, (radius/4)*i, 0, Math.PI*2); ctx.stroke();
            }

            // CCW Sweep
            angle -= 0.02; 
            if(angle <= -Math.PI*2) { angle = 0; beep(); }
            
            ctx.save();
            ctx.translate(center, center);
            ctx.rotate(angle);
            const grad = ctx.createRadialGradient(0,0,0,0,0,radius);
            grad.addColorStop(0, 'rgba(0,255,100,0)');
            grad.addColorStop(1, 'rgba(0,255,100,0.3)');
            ctx.fillStyle = grad;
            ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0, radius, 0, 0.4); ctx.fill();
            ctx.restore();
            
            requestAnimationFrame(drawRadar);
        }
    </script>
    """
    
    radar_html = f"""
    <div style="background:#0a0f1e; padding:20px; border-radius:20px; text-align:center;">
        <canvas id="radarCanvas" width="550" height="550" style="background:#03060c; border-radius:50%; border:2px solid #1e3a5f;"></canvas>
    </div>
    {radar_js}
    <script>drawRadar();</script>
    """
    components.html(radar_html, height=600)
    st.button(t['download_all'])

with tab_sat:
    st.title(f"🛰️ {t['sat_title']}")
    
    col_map, col_list = st.columns([2, 1])
    
    with col_map:
        # Simplified Leaflet Map integration
        map_html = """
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <div id="map" style="height: 500px; border-radius:15px; border:1px solid #1e3a5f;"></div>
        <script>
            const map = L.map('map', {zoomControl: false}).setView([20, 0], 2);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png').addTo(map);
            
            // Beep on refresh simulation
            const satAudio = new (window.AudioContext || window.webkitAudioContext)();
            setInterval(() => {
                const osc = satAudio.createOscillator();
                const g = satAudio.createGain();
                osc.connect(g); g.connect(satAudio.destination);
                osc.frequency.value = 1200; g.gain.value = 0.02;
                osc.start(); osc.stop(satAudio.currentTime + 0.05);
            }, 5000);
        </script>
        """
        components.html(map_html, height=520)
        st.caption(f"📡 {t['sat_refresh']}")

    with col_list:
        st.subheader("Target Assets")
        sats = ["ISS", "HUBBLE", "TIANGONG"] if not demo_sat else ["GeoEye-1", "Landsat-9", "NOAA-20", "Starlink", "GPS-III"]
        
        for s in sats:
            with st.expander(f"🛰️ {s}"):
                st.write(f"**Type:** {'Commercial' if demo_sat else 'Scientific'}")
                st.write("**Alt:** 420km | **Vel:** 27,600km/h")
                st.button(t['download'], key=f"dl_{s}")

# --- LICENSE FOOTER ---
st.divider()
st.markdown(f"### 📜 {t['license']}")
st.caption("Proprietary Commercial Software. Copyright © 2026 Gesner Deslandes. All rights reserved.")
