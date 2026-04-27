import streamlit as st
import streamlit.components.v1 as components
import json

# --- CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="GlobalInternet.py | Surveillance & Satellite", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- TRANSLATION DICTIONARY ---
texts = {
    "English": {
        "title": "Global Surveillance Radar",
        "sat_title": "Satellite Tracker",
        "settings": "Radar Settings",
        "lat": "Radar Latitude",
        "lon": "Radar Longitude",
        "range": "Max Range (km)",
        "license": "Software License",
        "logout": "Logout",
        "refresh": "Refresh Radar",
        "demo": "Demo Mode",
        "contact": "For licensing & support:",
        "branding": "GlobalInternet.py – Founder: Gesner Deslandes"
    },
    "French": {
        "title": "Radar de Surveillance Mondial",
        "sat_title": "Suivi par Satellite",
        "settings": "Paramètres du Radar",
        "lat": "Latitude du Radar",
        "lon": "Longitude du Radar",
        "range": "Portée Max (km)",
        "license": "Licence Logicielle",
        "logout": "Déconnexion",
        "refresh": "Actualiser le Radar",
        "demo": "Mode Démo",
        "contact": "Licence et support :",
        "branding": "GlobalInternet.py – Fondateur : Gesner Deslandes"
    },
    "Spanish": {
        "title": "Radar de Vigilancia Global",
        "sat_title": "Rastreador de Satélites",
        "settings": "Ajustes del Radar",
        "lat": "Latitud del Radar",
        "lon": "Longitud del Radar",
        "range": "Rango Máximo (km)",
        "license": "Licencia de Software",
        "logout": "Cerrar sesión",
        "refresh": "Actualizar Radar",
        "demo": "Modo Demo",
        "contact": "Licencia y soporte:",
        "branding": "GlobalInternet.py – Fundador: Gesner Deslandes"
    }
}

t = texts[st.session_state.lang]

# ----------------------------------------------------------------------
# LOGIN SCREEN
# ----------------------------------------------------------------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://via.placeholder.com/150?text=GlobalInternet.py", width=100)
        st.title("Secure Access")
        password = st.text_input("Enter Access Key", type="password")
        if st.button("Login"):
            if password == "20082010":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Key")
    st.stop()

# ----------------------------------------------------------------------
# SIDEBAR & BRANDING
# ----------------------------------------------------------------------
with st.sidebar:
    st.image("https://via.placeholder.com/80?text=GI", width=60)
    st.markdown(f"### {t['branding']}")
    
    st.session_state.lang = st.selectbox("Language / Langue / Idioma", ["English", "French", "Spanish"])
    
    st.divider()
    st.markdown(f"## 📡 {t['settings']}")
    radar_lat = st.number_input(t['lat'], value=40.7128, format="%.5f")
    radar_lon = st.number_input(t['lon'], value=-74.0060, format="%.5f")
    max_range = st.number_input(t['range'], min_value=30, max_value=2000, value=500)
    
    demo_mode = st.toggle(t['demo'], value=False)
    
    st.divider()
    st.markdown(f"## 📜 {t['license']}")
    st.caption("Copyright © 2025 Gesner Deslandes. Proprietary Commercial Software.")
    st.markdown(f"**{t['contact']}**")
    st.markdown("📞 `(509) 4738-5663` (Moncash)")
    st.markdown("📧 `deslandes78@gmail.com`\n🌐 `www.globalinternet.py` (Mock)")

    if st.button(f"🔄 {t['refresh']}", use_container_width=True):
        st.rerun()
    
    if st.button(t['logout'], type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ----------------------------------------------------------------------
# RADAR COMPONENT (Counter-Clockwise + Beep + Demo)
# ----------------------------------------------------------------------
tab1, tab2 = st.tabs([f"📡 {t['title']}", f"🛰️ {t['sat_title']}"])

with tab1:
    radar_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ background: #03060c; color: #00ff41; font-family: monospace; overflow: hidden; }}
            #radarContainer {{ position: relative; width: 600px; height: 600px; margin: auto; }}
            canvas {{ border-radius: 50%; border: 2px solid #1e3a5f; }}
            .stats {{ margin-top: 10px; display: flex; justify-content: space-between; }}
        </style>
    </head>
    <body>
        <div id="radarContainer">
            <canvas id="rCanvas" width="600" height="600"></canvas>
        </div>
        <div class="stats">
            <div>MODE: {"DEMO (SIMULATED)" if demo_mode else "LIVE ADS-B"}</div>
            <div id="count">TARGETS: 0</div>
        </div>

        <script>
            const canvas = document.getElementById('rCanvas');
            const ctx = canvas.getContext('2d');
            let angle = 0;
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

            function beep() {{
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(880, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.1);
            }}

            function drawRadar() {{
                ctx.clearRect(0, 0, 600, 600);
                
                // Draw background circles
                ctx.strokeStyle = "#1e3a5f";
                for(let i=1; i<=4; i++) {{
                    ctx.beginPath();
                    ctx.arc(300, 300, i*75, 0, Math.PI*2);
                    ctx.stroke();
                }}

                // Counter-clockwise Sweep
                angle -= 0.03; 
                if (angle <= -Math.PI * 2) {{
                    angle = 0;
                    beep();
                }}

                ctx.save();
                ctx.translate(300, 300);
                ctx.rotate(angle);
                let grad = ctx.createRadialGradient(0,0,0,0,0,300);
                grad.addColorStop(0, "rgba(0, 255, 65, 0)");
                grad.addColorStop(1, "rgba(0, 255, 65, 0.4)");
                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.moveTo(0,0);
                ctx.arc(0,0, 300, 0, 0.2);
                ctx.fill();
                ctx.restore();

                requestAnimationFrame(drawRadar);
            }}
            drawRadar();
        </script>
    </body>
    </html>
    """
    components.html(radar_html, height=700)
