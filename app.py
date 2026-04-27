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

# Data for Radar Detections
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
        "subtitle": "Built by Gesner Deslandes",
        "logout": "Terminate Session", 
        "report": "Download Asset Report",
        "detection_log": "Live Detection Log",
        "audio_note": "Click the radar to enable sonar audio."
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar", 
        "sat_tab": "🛰️ Suivi Satellite",
        "title": "RADAR DE SURVEILLANCE MONDIAL", 
        "subtitle": "Conçu par Gesner Deslandes",
        "logout": "Déconnexion", 
        "report": "Télécharger le Rapport",
        "detection_log": "Journal de Détection",
        "audio_note": "Cliquez sur le radar pour activer l'audio sonar."
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
    with st.sidebar:
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French"], key="lang")
        L = UI[st.session_state.lang]
        
        st.markdown(f"**👨‍💻 Gesner Deslandes**\nIndependent Researcher")
        st.divider()
        
        st.checkbox(L.get('demo_r', 'Demo Radar'), value=False, key="check_demo_r")
        st.checkbox(L.get('demo_s', 'Demo Sat'), value=False, key="check_demo_s")
        
        st.divider()
        st.write(f"📞 (509) 4738-5663")
        st.write(f"✉️ deslandes78@gmail.com")
        
        if st.button(L['logout'], key="sidebar_logout_btn", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    tab_radar, tab_sat = st.tabs([L["radar_tab"], L["sat_tab"]])

    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.info(L['audio_note'])
        
        col_rad, col_log = st.columns([2, 1])
        
        with col_rad:
            # INTEGRATED RADAR WITH SYNCED AUDIO PING
            radar_html = r"""
            <html>
            <body style="background:#03060c; margin:0; display:flex; flex-direction:column; align-items:center; cursor:pointer;">
                <canvas id="radar" width="550" height="550" style="border:1px solid #1e3a5f; border-radius:50%;"></canvas>
                <script>
                    const canvas = document.getElementById('radar');
                    const ctx = canvas.getContext('2d');
                    let angle = 0;
                    let audioCtx = null;

                    // Initialize Audio on first click (Browser security requirement)
                    canvas.addEventListener('click', () => {
                        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    });

                    function playPing() {
                        if (!audioCtx) return;
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.5);
                        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.5);
                    }

                    function draw() {
                        ctx.clearRect(0,0,550,550);
                        const cx = 275, cy = 275, r = 250;
                        
                        // Draw static grid
                        ctx.strokeStyle = 'rgba(30, 58, 95, 0.5)';
                        for(let i=1; i<=4; i++) {
                            ctx.beginPath(); ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2); ctx.stroke();
                        }

                        // Update Angle
                        let prevAngle = angle;
                        angle -= 0.03; 
                        
                        // Trigger sound when sweep passes the "12 o'clock" position
                        if (Math.floor(prevAngle / (Math.PI*2)) !== Math.floor(angle / (Math.PI*2))) {
                            playPing();
                        }

                        // Draw Sweep
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

    with tab_sat:
        st.title("🛰️ Satellite Tracking Assets")
        # (Satellite logic remains consistent)
        st.info("Satellite Tracking Module Online")

# --- 5. EXECUTION ---
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
