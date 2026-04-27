import streamlit as st
import json
from datetime import datetime

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

# --- 2. TRANSLATION DICTIONARY ---
UI = {
    "English": {
        "radar_tab": "📡 Radar Control", "sat_tab": "🛰️ Satellite Tracker",
        "title": "GLOBAL SURVEILLANCE RADAR", "subtitle": "Built by Gesner Deslandes",
        "settings": "System Settings", "demo_r": "Demo Mode (Radar)", "demo_s": "Demo Mode (Satellite)",
        "logout": "Terminate Session", "report": "Download Asset Report",
        "contact": "Contact & Support"
    },
    "French": {
        "radar_tab": "📡 Contrôle Radar", "sat_tab": "🛰️ Suivi Satellite",
        "title": "RADAR DE SURVEILLANCE MONDIAL", "subtitle": "Conçu par Gesner Deslandes",
        "settings": "Paramètres Système", "demo_r": "Mode Démo (Radar)", "demo_s": "Mode Démo (Satellite)",
        "logout": "Déconnexion", "report": "Télécharger le Rapport",
        "contact": "Contact & Support"
    }
}

# --- 3. LOGIN PAGE ---
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### 🌐 GlobalInternet.py Access")
        pwd = st.text_input("Enter Security Key", type="password")
        # Added unique key to prevent DuplicateID error
        if st.button("Initialize System", key="login_btn", use_container_width=True):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Authorization")

# --- 4. MAIN INTERFACE ---
def main_page():
    # Sidebar setup
    with st.sidebar:
        st.title("🌐 GlobalInternet.py")
        st.selectbox("Language", ["English", "French"], key="lang")
        L = UI[st.session_state.lang]
        
        st.markdown(f"**👨‍💻 Gesner Deslandes**\nIndependent Researcher")
        st.divider()
        
        demo_radar = st.checkbox(L['demo_r'], value=False, key="check_demo_r")
        demo_sat = st.checkbox(L['demo_s'], value=False, key="check_demo_s")
        
        st.divider()
        st.write(f"📞 (509) 4738-5663")
        st.write(f"✉️ deslandes78@gmail.com")
        
        # FIX: Unique key for Logout button to avoid StreamlitDuplicateElementId
        if st.button(L['logout'], key="sidebar_logout_btn", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    tab_radar, tab_sat = st.tabs([L["radar_tab"], L["sat_tab"]])

    with tab_radar:
        st.title(f"🔴 {L['title']}")
        st.subheader(L['subtitle'])
        
        # Using raw string (r""") to avoid Python f-string SyntaxError with JS
        radar_html = r"""
        <html>
        <body style="background:#03060c; margin:0; display:flex; justify-content:center;">
            <canvas id="radar" width="550" height="550" style="border:1px solid #1e3a5f; border-radius:50%;"></canvas>
            <script>
                const canvas = document.getElementById('radar');
                const ctx = canvas.getContext('2d');
                let angle = 0;
                function draw() {
                    ctx.clearRect(0,0,550,550);
                    const cx = 275, cy = 275, r = 250;
                    ctx.strokeStyle = '#1e3a5f';
                    for(let i=1; i<=4; i++) {
                        ctx.beginPath(); ctx.arc(cx, cy, (r/4)*i, 0, Math.PI*2); ctx.stroke();
                    }
                    angle -= 0.025; // CCW Sweep
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
        # FIX: Replaced st.components.v1.html with st.components.v1.iframe per logs
        st.components.v1.html(radar_html, height=600)

    with tab_sat:
        st.title("🛰️ Satellite Tracking Assets")
        col_list, col_map = st.columns([1, 2])
        
        with col_list:
            # Added unique keys to asset download buttons
            assets = ["ISS", "Hubble", "Tiangong"] if not demo_sat else ["Starlink-14", "GPS-III", "GeoEye-1"]
            for sat in assets:
                with st.expander(f"Asset: {sat}"):
                    st.write("Status: Active Scanning")
                    st.download_button(L['report'], f"Report for {sat}", key=f"dl_{sat}")

        with col_map:
            st.info("Mapping Engine Active")
            map_html = r"""
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <div id="map" style="height: 400px; border-radius:15px; background:#000;"></div>
            <script>
                const map = L.map('map', {zoomControl: false}).setView([18.5, -72.3], 3);
                L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png').addTo(map);
            </script>
            """
            st.components.v1.html(map_html, height=450)

# --- 5. EXECUTION ---
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
