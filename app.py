import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

# --- 1. BOOTSTRAP & SESSION STATE ---
# We set this first to prevent any "Fragment" or configuration errors.
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance Suite",
    layout="wide",
    page_icon="🌐"
)

# Initialize critical state keys to prevent KeyErrors on first load
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- 2. TRANSLATION ENGINE ---
# Every language must contain every key to prevent app crashes.
UI = {
    "English": {
        "radar_tab": "📡 Radar Control",
        "sat_tab": "🛰️ Satellite Tracker",
        "title": "GLOBAL SURVEILLANCE RADAR",
        "subtitle": "Built by Gesner Deslandes",
        "settings": "System Settings",
        "demo_r": "Demo Mode (Radar)",
        "demo_s": "Demo Mode (Satellite)",
        "logout": "Terminate Session",
        "report": "Download Asset Report",
        "contact": "Contact & Support",
        "license": "Proprietary Commercial License"
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar",
        "sat_tab": "🛰️ Suivi Satellite",
        "title": "RADAR DE SURVEILLANCE MONDIAL",
        "subtitle": "Conçu par Gesner Deslandes",
        "settings": "Paramètres Système",
        "demo_r": "Mode Démo (Radar)",
        "demo_s": "Mode Démo (Satellite)",
        "logout": "Terminer la Session",
        "report": "Télécharger le Rapport",
        "contact": "Contact & Support",
        "license": "Licence Commerciale Propriétaire"
    },
    "Spanish": {
        "radar_tab": "📡 Control de Radar",
        "sat_tab": "🛰️ Rastreador Satelital",
        "title": "RADAR DE VIGILANCIA GLOBAL",
        "subtitle": "Construido por Gesner Deslandes",
        "settings": "Ajustes del Sistema",
        "demo_r": "Modo Demo (Radar)",
        "demo_s": "Modo Demo (Satélite)",
        "logout": "Terminar Sesión",
        "report": "Descargar Informe de Activo",
        "contact": "Contacto y Soporte",
        "license": "Licencia Comercial Propietaria"
    }
}

# --- 3. SECURITY GATE ---
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### 🌐 GlobalInternet.py Access")
        pwd = st.text_input("Enter System Security Key", type="password")
        if st.button("Initialize System", use_container_width=True):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Security Payload")
    st.stop()

# --- 4. SIDEBAR IDENTITY & CONTROLS ---
with st.sidebar:
    st.title("🌐 GlobalInternet.py")
    # Using key="lang" ensures the selectbox is wired directly to session_state
    st.selectbox("Language / Langue / Idioma", ["English", "French", "Spanish"], key="lang")
    
    # We define L *after* the selectbox to ensure it uses the updated state
    L = UI[st.session_state.lang]
    
    st.markdown(f"**👨‍💻 Gesner Deslandes**")
    st.caption("Founder & Python Systems Builder")
    st.divider()
    
    st.markdown(f"### ⚙️ {L['settings']}")
    demo_radar = st.checkbox(L['demo_r'], value=False)
    demo_sat = st.checkbox(L['demo_s'], value=False)
    
    st.divider()
    st.markdown(f"### 📞 {L['contact']}")
    st.write("📱 **(509) 4738-5663**")
    st.write("✉️ **deslandes78@gmail.com**")
    st.markdown("[Visit Systems Portal](https://globalinternet.py)")
    
    st.divider()
    if st.button(L['logout'], type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- 5. COMPONENT: RADAR (CCW, 550px, Audio) ---
def render_radar_ui():
    st.title(f"🔴 {L['title']}")
    st.subheader(L['subtitle'])
    
    # Using double braces {{ }} to protect JS code from Python f-string parsing
    radar_html = f"""
    <div style="background:#03060c; padding:20px; border-radius:20px; display:flex; justify-content:center; flex-direction:column; align-items:center;">
        <canvas id="surveillanceRadar" width="550" height="550" style="border:1px solid #1e3a5f; border-radius:50%; background:#000;"></canvas>
        <div style="margin-top:10px; color:#00ff41; font-family:monospace; font-size:12px;">SCANNING ACTIVE... CCW DIRECTION</div>
    </div>
    <script>
        const canvas = document.getElementById('surveillanceRadar');
        const ctx = canvas.getContext('2d');
        let angle = 0;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playScanBeep() {{
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.frequency.value = 800; gain.gain.value = 0.05;
            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
        }}

        function draw() {{
            ctx.clearRect(0,0,550,550);
            const cx = 275, cy = 275, r = 250;
            
            // Draw Background Rings
            ctx.strokeStyle = '#1e3a5f';
            ctx.lineWidth = 1;
            for(let i=1; i<=4; i++) {{
                ctx.beginPath(); ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2); ctx.stroke();
            }}

            // Update Angle (CCW: minus operator)
            angle -= 0.025;
            if(angle <= -Math.PI * 2) {{ 
                angle = 0; 
                playScanBeep(); 
            }}

            // Draw Sweep Gradient
            ctx.save();
            ctx.translate(cx, cy); ctx.rotate(angle);
            const grad = ctx.createRadialGradient(0,0,0,0,0,r);
            grad.addColorStop(0, 'rgba(0,255,100,0)');
            grad.addColorStop(1, 'rgba(0,255,100,0.3)');
            ctx.fillStyle = grad;
            ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0,0, r, 0, 0.4); ctx.fill();
            ctx.restore();

            // Built-by Watermark on Canvas
            ctx.fillStyle = "rgba(0, 255, 65, 0.4)";
            ctx.font = "10px Monospace";
            ctx.fillText("Built by Gesner Deslandes | GlobalInternet.py", 320, 535);

            requestAnimationFrame(draw);
        }}
        draw();
    </script>
    """
    components.html(radar_html, height=620)

# --- 6. COMPONENT: SATELLITE (Reports, Demo Mode) ---
def render_satellite_ui():
    st.title(f"🛰️ {L['sat_tab']}")
    
    col_map, col_list = st.columns([2.2, 1])
    
    with col_list:
        st.subheader("Asset Registry")
        # Logic: Switch asset list based on demo mode
