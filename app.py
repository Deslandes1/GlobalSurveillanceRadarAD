import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import json
import base64
from datetime import datetime

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="GlobalInternet.py Surveillance", layout="wide", page_icon="🌐")

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- 2. AUTHENTICATION GATE ---
def login_screen():
    st.markdown("<h1 style='text-align: center;'>🌐 GlobalInternet.py</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.subheader("System Access Required")
        pwd = st.text_input("Security Key", type="password")
        if st.button("Initialize System"):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Payload")

if not st.session_state.authenticated:
    login_screen()
    st.stop()

# --- 3. LANGUAGE DICTIONARY ---
UI = {
    "English": {
        "radar_tab": "📡 Radar Control",
        "sat_tab": "🛰️ Satellite Tracker",
        "settings": "System Settings",
        "demo_radar": "Demo Mode (Radar)",
        "demo_sat": "Demo Mode (Satellite)",
        "logout": "Terminate Session",
        "branding": "Built by Gesner Deslandes",
        "contact": "Contact & Support",
        "radar_title": "GLOBAL SURVEILLANCE RADAR",
        "sat_title": "ORBITAL ASSET MONITORING",
        "report_btn": "Download Asset Report",
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar",
        "sat_tab": "🛰️ Suivi Satellite",
        "settings": "Paramètres Système",
        "demo_radar": "Mode Démo (Radar)",
        "demo_sat": "Mode Démo (Satellite)",
        "logout": "Terminer la Session",
        "branding": "Conçu par Gesner Deslandes",
        "contact": "Contact & Support",
        "radar_title": "RADAR DE SURVEILLANCE MONDIAL",
        "sat_title": "SURVEILLANCE DES ACTIFS ORBITAUX",
        "report_btn": "Télécharger le Rapport",
    },
    "Spanish": {
        "radar_tab": "📡 Control de Radar",
        "sat_tab": "🛰️ Rastreador Satelital",
        "settings": "Ajustes del Sistema",
        "demo_radar": "Modo Demo (Radar)",
        "demo_sat": "Modo Demo (Satélite)",
        "logout": "Terminar Sesión",
        "branding": "Creado por Gesner Deslandes",
        "contact": "Contacto y Soporte",
        "radar_title": "RADAR DE VIGILANCIA GLOBAL",
        "sat_title": "MONITOREO DE ACTIVOS ORBITALES",
        "report_btn": "Descargar Informe de Activo",
    }
}

L = UI[st.session_state.lang]

# --- 4. SIDEBAR BRANDING & CONTROLS ---
with st.sidebar:
    st.title("🌐 GlobalInternet.py")
    st.write(f"**{L['branding']}**")
    st.divider()
    
    st.session_state.lang = st.selectbox("Language / Langue / Idioma", ["English", "French", "Spanish"])
    
    st.markdown(f"### ⚙️ {L['settings']}")
    demo_radar = st.checkbox(L['demo_radar'], value=False)
    demo_sat = st.checkbox(L['demo_sat'], value=False)
    
    st.divider()
    st.markdown(f"### 📞 {L['contact']}")
    st.write("📱 (509) 4738-5663")
    st.write("✉️ deslandes78@gmail.com")
    st.markdown("[Visit Main Site](https://globalinternet.py)")
    
    st.divider()
    if st.button(L['logout'], type="primary"):
        st.session_state.authenticated = False
        st.rerun()

# --- 5. RADAR IMPLEMENTATION (550x550, CCW, Audio) ---
def render_radar():
    st.title(L['radar_title'])
    
    # Audio Beep & Sweep JS (Using triple quotes + double braces for CSS/JS compatibility)
    radar_html = f"""
    <div id="radar-container" style="display: flex; justify-content: center; background: #000; padding: 20px; border-radius: 10px;">
        <canvas id="radarCanvas" width="550" height="550"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('radarCanvas');
        const ctx = canvas.getContext('2d');
        let angle = 0;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playBeep() {{
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.frequency.value = 880;
            gain.gain.value = 0.1;
            osc.start();
            osc.stop(audioCtx.currentTime + 0.1);
        }}

        function drawRadar() {{
            ctx.clearRect(0, 0, 550, 550);
            const cx = 275, cy = 275, r = 250;

            // Background Rings
            ctx.strokeStyle = '#004400';
            for(let i=1; i<=4; i++) {{
                ctx.beginPath();
                ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2);
                ctx.stroke();
            }}

            // Sweep (Counter-Clockwise: angle -= speed)
            angle -= 0.03;
            if (angle <= -Math.PI * 2) {{
                angle = 0;
                playBeep();
            }}

            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(angle);
            let grad = ctx.createRadialGradient(0,0,0,0,0,r);
            grad.addColorStop(0, 'rgba(0, 255, 0, 0)');
            grad.addColorStop(1, 'rgba(0, 255, 0, 0.4)');
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.moveTo(0,0);
            ctx.arc(0,0, r, 0, Math.PI/4);
            ctx.fill();
            ctx.restore();

            requestAnimationFrame(drawRadar);
        }}
        drawRadar();
    </script>
    """
    components.html(radar_html, height=600)

# --- 6. SATELLITE IMPLEMENTATION (Reports + Audio) ---
def render_satellites():
    st.title(L['sat_title'])
    
    col_map, col_list = st.columns([2, 1])
    
    # Mock data or real logic here
    assets = [
        {"name": "ISS", "lat": 51.5, "lon": -0.1, "alt": "408km", "vel": "27,600 km/h"},
        {"name": "Hubble", "lat": -10.2, "lon": 45.3, "alt": "540km", "vel": "27,300 km/h"},
    ]
    
    with col_list:
        st.subheader("Asset Registry")
        for asset in assets:
            with st.expander(f"🛰️ {asset['name']}"):
                st.write(f"Pos: {asset['lat']}, {asset['lon']}")
                st.write(f"Alt: {asset['alt']}")
                
                # Report Generation
                report_content = f"Asset: {asset['name']}\nTimestamp: {datetime.now()}\nVelocity: {asset['vel']}\nStatus: Active"
                st.download_button(
                    label=L['report_btn'],
                    data=report_content,
                    file_name=f"{asset['name']}_report.txt",
                    mime="text/plain",
                    key=asset['name']
                )

    with col_map:
        # Placeholder for Map with beep logic in JS
        st.info("Satellite Positioning Active. Syncing every 5s...")
        st.markdown("""
        <script>
            // Beep logic for every 5 seconds
            setInterval(() => {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                osc.connect(audioCtx.destination);
                osc.frequency.value = 440;
                osc.start();
                osc.stop(audioCtx.currentTime + 0.05);
            }, 5000);
        </script>
        """, unsafe_allow_html=True)

# --- 7. MAIN UI TABS ---
tab_r, tab_s = st.tabs([L["radar_tab"], L["sat_tab"]])

with tab_r:
    render_radar()

with tab_s:
    render_satellites()
