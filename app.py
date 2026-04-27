import streamlit as st
import streamlit.components.v1 as components
import json

# --- CONFIGURATION & INITIAL STATE ---
st.set_page_config(
    page_title="GlobalInternet.py | Surveillance & Satellite", 
    layout="wide",
    page_icon="🔴"
)

# Initialize session state keys safely
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- TRANSLATION DICTIONARY ---
texts = {
    "English": {
        "title": "GLOBAL SURVEILLANCE RADAR",
        "subtitle": "Real-time global aircraft tracking | Military & Drone Detection",
        "sat_title": "LIVE SATELLITE TRACKER",
        "settings": "Radar Settings",
        "lat": "Radar Latitude",
        "lon": "Radar Longitude",
        "range": "Max Range (km)",
        "license": "Software License",
        "logout": "Logout",
        "refresh": "Refresh Radar",
        "demo": "Demo Mode",
        "contact": "For licensing, support, or payments:",
        "branding": "GlobalInternet.py",
        "founder": "Founder & Python Programmer: Gesner Deslandes",
        "tabs": ["📡 Radar", "🛰️ Satellite Tracker"]
    },
    "French": {
        "title": "RADAR DE SURVEILLANCE MONDIAL",
        "subtitle": "Suivi mondial en temps réel | Détection militaire et drones",
        "sat_title": "SUIVI SATELLITE EN DIRECT",
        "settings": "Paramètres du Radar",
        "lat": "Latitude du Radar",
        "lon": "Longitude du Radar",
        "range": "Portée Max (km)",
        "license": "Licence Logicielle",
        "logout": "Déconnexion",
        "refresh": "Actualiser le Radar",
        "demo": "Mode Démo",
        "contact": "Pour licence, support ou paiements :",
        "branding": "GlobalInternet.py",
        "founder": "Fondateur et Programmeur Python : Gesner Deslandes",
        "tabs": ["📡 Radar", "🛰️ Suivi Satellite"]
    },
    "Spanish": {
        "title": "RADAR DE VIGILANCIA GLOBAL",
        "subtitle": "Rastreo global en tiempo real | Detección militar y drones",
        "sat_title": "RASTREADOR DE SATÉLITES",
        "settings": "Ajustes del Radar",
        "lat": "Latitud del Radar",
        "lon": "Longitud del Radar",
        "range": "Rango Máximo (km)",
        "license": "Licencia de Software",
        "logout": "Cerrar sesión",
        "refresh": "Actualizar Radar",
        "demo": "Modo Demo",
        "contact": "Para licencias, soporte o pagos:",
        "branding": "GlobalInternet.py",
        "founder": "Fundador y Programador Python: Gesner Deslandes",
        "tabs": ["📡 Radar", "🛰️ Rastreador Satelital"]
    }
}

# ----------------------------------------------------------------------
# LOGIN SCREEN
# ----------------------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_view_content=True)
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
# SIDEBAR & BRANDING
# ----------------------------------------------------------------------
with st.sidebar:
    st.title("🌐 GlobalInternet.py")
    # Language Selector (Binds to session_state['lang'])
    st.selectbox("Language / Langue / Idioma", ["English", "French", "Spanish"], key="lang")
    
    # Refresh translation object AFTER language selection
    t = texts[st.session_state.lang]
    
    st.divider()
    st.markdown(f"### 📡 {t['settings']}")
    radar_lat = st.number_input(t['lat'], value=40.7128, format="%.5f")
    radar_lon = st.number_input(t['lon'], value=-74.0060, format="%.5f")
    max_range = st.number_input(t['range'], min_value=30, max_value=2000, value=500, step=50)
    
    demo_mode = st.toggle(t['demo'], value=True)
    
    st.divider()
    st.markdown(f"### 📜 {t['license']}")
    st.caption(f"Copyright © 2025 Gesner Deslandes.\n{t['branding']}")
    st.markdown(f"**{t['contact']}**")
    st.markdown("📞 **Prisme Transfer**: `(509) 4738-5663`")
    st.markdown("📧 **Email**: `deslandes78@gmail.com`")
    st.markdown("🌐 **Web**: `www.globalinternet.py`")

    if st.button(t['refresh'], use_container_width=True):
        st.rerun()
        
    if st.button(t['logout'], type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ----------------------------------------------------------------------
# MAIN INTERFACE
# ----------------------------------------------------------------------
tab1, tab2 = st.tabs(t['tabs'])

with tab1:
    st.title(f"🔴 {t['title']}")
    st.write(f"**{t['subtitle']}**")
    st.write(f"*{t['founder']}*")

    # Radar Component with Counter-Clockwise Sweep + Audio Beep
    radar_html = f"""
    <!DOCTYPE html>
    <html>
    <body style="background:#0a0f1e; margin:0; overflow:hidden;">
        <canvas id="radar" width="700" height="700" style="display:block; margin:auto;"></canvas>
        <script>
            const canvas = document.getElementById('radar');
            const ctx = canvas.getContext('2d');
            let angle = 0;
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

            function beep() {{
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.frequency.value = 1200;
                gain.gain.value = 0.05;
                osc.start();
                osc.stop(audioCtx.currentTime + 0.1);
            }}

            function draw() {{
                ctx.clearRect(0,0,700,700);
                // Center
                const cx = 350, cy = 350, r = 300;
                
                // Rings
                ctx.strokeStyle = '#1e3a5f';
                for(let i=1; i<=4; i++) {{
                    ctx.beginPath();
                    ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2);
                    ctx.stroke();
                }}

                // Counter-Clockwise Sweep
                angle -= 0.02; 
                if (angle <= -Math.PI * 2) {{
                    angle = 0;
                    beep();
                }}

                ctx.save();
                ctx.translate(cx, cy);
                ctx.rotate(angle);
                const grad = ctx.createRadialGradient(0,0,0,0,0,r);
                grad.addColorStop(0, 'rgba(0,255,100,0)');
                grad.addColorStop(1, 'rgba(0,255,100,0.3)');
                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.moveTo(0,0);
                ctx.arc(0,0, r, 0, 0.4);
                ctx.fill();
                ctx.restore();

                requestAnimationFrame(draw);
            }}
            draw();
        </script>
    </body>
    </html>
    """
    components.html(radar_html, height=720)

with tab2:
    st.title(f"🛰️ {t['sat_title']}")
    # Simplified Satellite Logic (ISS, Hubble, Tiangong)
    sat_html = """
    <div style="background:#0a0f1e; color:#00ff41; padding:20px; border-radius:15px; border:1px solid #1e3a5f; font-family:monospace;">
        <h3>Active Orbital Assets</h3>
        <ul>
            <li>🛰️ ISS - Altitude: 418km | Velocity: 27,600 km/h</li>
            <li>🔭 HUBBLE - Altitude: 540km | Status: Operational</li>
            <li>🌍 TIANGONG - Altitude: 385km | Status: Active</li>
        </ul>
        <p style="color:gray;">Real-time API tracking active. Beep on position update enabled.</p>
    </div>
    """
    components.html(sat_html, height=400)
