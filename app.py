import streamlit as st
import streamlit.components.v1 as components

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="🔴 Global Surveillance Radar + Satellite Tracker – GlobalInternet.py", layout="wide")

# ---------- AUTHENTICATION STATE ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ---------- LANGUAGE STATE ----------
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# ---------- TRANSLATIONS ----------
texts = {
    "en": {
        "app_title": "GLOBAL SURVEILLANCE RADAR + SATELLITE TRACKER",
        "login_title": "🔐 Login Required",
        "login_instruction": "Enter password to access the radar and satellite tracking system",
        "password_label": "Password",
        "login_button": "Login",
        "logout_button": "Logout",
        "incorrect_password": "Incorrect password. Hint: 20082010",
        "sidebar_company": "🌐 GlobalInternet.py",
        "sidebar_founder": "👨‍💻 Gesner Deslandes – Founder & Python Builder",
        "sidebar_phone": "📞 (509) 4738-5663",
        "sidebar_email": "✉️ deslandes78@gmail.com",
        "sidebar_website": "🌍 Visit our website",
        "radar_settings": "📡 Radar Settings",
        "radar_lat": "Radar Latitude",
        "radar_lon": "Radar Longitude",
        "max_range": "Max Range (km)",
        "demo_mode_radar": "🎲 Demo Mode (Radar)",
        "demo_mode_satellite": "🛸 Demo Mode (Satellite)",
        "data_source": "🔑 Data Source",
        "data_source_msg": "For global coverage (oceans & remote areas), enter your Flightradar24 API key.",
        "api_key_input": "Flightradar24 API Key",
        "api_key_placeholder": "Enter your API key (optional)",
        "global_active": "🌍 **Global coverage active** – you will see aircraft worldwide.",
        "opensky_active": "📡 Using OpenSky Network (regional coverage, free).",
        "demo_active": "🎮 **Demo mode active** – showing simulated aircraft.",
        "license_title": "📜 Software License",
        "license_text": """
**Proprietary Commercial Software**  
Copyright © 2025 Gesner Deslandes. All rights reserved.

This software is **licensed**, not sold.  
You may use it only after purchasing a valid license from the author.

**Unauthorized copying, distribution, or resale is strictly prohibited.**

For licensing, support, or payments:
""",
        "prisme": "📞 **Prisme Transfer** (Digicel Moncash): `(509) 4738-5663`",
        "email_contact": "📧 **Email**: `deslandes78@gmail.com`",
        "terms": "By using this software you agree to the terms above.",
        "refresh_radar": "🔄 Refresh Radar",
        "tab_radar": "📡 Radar",
        "tab_satellite": "🛰️ Satellite Tracker",
        "satellite_title": "🛰️ LIVE SATELLITE TRACKER (Real‑time positions)",
        "satellite_desc": "Current positions of the International Space Station (ISS), Hubble Space Telescope, and Tiangong space station.",
        "satellite_credit": "Data provided by wheretheiss.at API | Map: Leaflet | Built by Gesner Deslandes",
        "demo_satellite_note": "🎮 Demo mode: showing simulated satellites (GeoEye, Landsat, etc.)"
    },
    "fr": {
        "app_title": "RADAR DE SURVEILLANCE MONDIAL + TRACEUR DE SATELLITES",
        "login_title": "🔐 Connexion requise",
        "login_instruction": "Entrez le mot de passe pour accéder au radar et au traceur de satellites",
        "password_label": "Mot de passe",
        "login_button": "Connexion",
        "logout_button": "Déconnexion",
        "incorrect_password": "Mot de passe incorrect. Indice : 20082010",
        "sidebar_company": "🌐 GlobalInternet.py",
        "sidebar_founder": "👨‍💻 Gesner Deslandes – Fondateur & Constructeur Python",
        "sidebar_phone": "📞 (509) 4738-5663",
        "sidebar_email": "✉️ deslandes78@gmail.com",
        "sidebar_website": "🌍 Visitez notre site web",
        "radar_settings": "📡 Paramètres radar",
        "radar_lat": "Latitude du radar",
        "radar_lon": "Longitude du radar",
        "max_range": "Portée max (km)",
        "demo_mode_radar": "🎲 Mode démo (Radar)",
        "demo_mode_satellite": "🛸 Mode démo (Satellite)",
        "data_source": "🔑 Source de données",
        "data_source_msg": "Pour une couverture mondiale (océans et zones éloignées), entrez votre clé API Flightradar24.",
        "api_key_input": "Clé API Flightradar24",
        "api_key_placeholder": "Entrez votre clé API (optionnel)",
        "global_active": "🌍 **Couverture mondiale active** – vous verrez des aéronefs du monde entier.",
        "opensky_active": "📡 Utilisation du réseau OpenSky (couverture régionale, gratuit).",
        "demo_active": "🎮 **Mode démo actif** – simulation d'aéronefs.",
        "license_title": "📜 Licence logicielle",
        "license_text": """
**Logiciel commercial propriétaire**  
Copyright © 2025 Gesner Deslandes. Tous droits réservés.

Ce logiciel est **sous licence**, non vendu.  
Vous ne pouvez l'utiliser qu'après avoir acheté une licence valide auprès de l'auteur.

**La copie, la distribution ou la revente non autorisée est strictement interdite.**

Pour les licences, le support ou les paiements :
""",
        "prisme": "📞 **Transfert Prisme** (Moncash Digicel) : `(509) 4738-5663`",
        "email_contact": "📧 **Email** : `deslandes78@gmail.com`",
        "terms": "En utilisant ce logiciel, vous acceptez les conditions ci-dessus.",
        "refresh_radar": "🔄 Actualiser le radar",
        "tab_radar": "📡 Radar",
        "tab_satellite": "🛰️ Traceur de satellites",
        "satellite_title": "🛰️ TRACEUR DE SATELLITES EN DIRECT (positions réelles)",
        "satellite_desc": "Positions actuelles de la Station Spatiale Internationale (ISS), du télescope Hubble et de la station spatiale Tiangong.",
        "satellite_credit": "Données fournies par l'API wheretheiss.at | Carte : Leaflet | Construit par Gesner Deslandes",
        "demo_satellite_note": "🎮 Mode démo : satellites simulés (GeoEye, Landsat, etc.)"
    },
    "es": {
        "app_title": "RADAR DE VIGILANCIA GLOBAL + RASTREADOR DE SATÉLITES",
        "login_title": "🔐 Inicio de sesión requerido",
        "login_instruction": "Ingrese la contraseña para acceder al radar y al rastreador de satélites",
        "password_label": "Contraseña",
        "login_button": "Iniciar sesión",
        "logout_button": "Cerrar sesión",
        "incorrect_password": "Contraseña incorrecta. Pista: 20082010",
        "sidebar_company": "🌐 GlobalInternet.py",
        "sidebar_founder": "👨‍💻 Gesner Deslandes – Fundador & Constructor Python",
        "sidebar_phone": "📞 (509) 4738-5663",
        "sidebar_email": "✉️ deslandes78@gmail.com",
        "sidebar_website": "🌍 Visite nuestro sitio web",
        "radar_settings": "📡 Configuración del radar",
        "radar_lat": "Latitud del radar",
        "radar_lon": "Longitud del radar",
        "max_range": "Alcance máximo (km)",
        "demo_mode_radar": "🎲 Modo demostración (Radar)",
        "demo_mode_satellite": "🛸 Modo demostración (Satélite)",
        "data_source": "🔑 Fuente de datos",
        "data_source_msg": "Para cobertura global (océanos y áreas remotas), ingrese su clave API de Flightradar24.",
        "api_key_input": "Clave API de Flightradar24",
        "api_key_placeholder": "Ingrese su clave API (opcional)",
        "global_active": "🌍 **Cobertura global activa** – verá aeronaves de todo el mundo.",
        "opensky_active": "📡 Usando la red OpenSky (cobertura regional, gratuita).",
        "demo_active": "🎮 **Modo demostración activo** – aeronaves simuladas.",
        "license_title": "📜 Licencia de software",
        "license_text": """
**Software comercial propietario**  
Copyright © 2025 Gesner Deslandes. Todos los derechos reservados.

Este software tiene **licencia**, no se vende.  
Solo puede usarlo después de comprar una licencia válida del autor.

**La copia, distribución o reventa no autorizada está estrictamente prohibida.**

Para licencias, soporte o pagos:
""",
        "prisme": "📞 **Transferencia Prisme** (Moncash Digicel): `(509) 4738-5663`",
        "email_contact": "📧 **Correo electrónico**: `deslandes78@gmail.com`",
        "terms": "Al usar este software, acepta los términos anteriores.",
        "refresh_radar": "🔄 Actualizar radar",
        "tab_radar": "📡 Radar",
        "tab_satellite": "🛰️ Rastreador de satélites",
        "satellite_title": "🛰️ RASTREADOR DE SATÉLITES EN VIVO (posiciones reales)",
        "satellite_desc": "Posiciones actuales de la Estación Espacial Internacional (ISS), el telescopio Hubble y la estación espacial Tiangong.",
        "satellite_credit": "Datos proporcionados por la API wheretheiss.at | Mapa: Leaflet | Construido por Gesner Deslandes",
        "demo_satellite_note": "🎮 Modo demostración: satélites simulados (GeoEye, Landsat, etc.)"
    }
}

def _(key):
    return texts[st.session_state.lang].get(key, key)

# ---------- LANGUAGE SELECTOR ----------
def language_selector():
    lang_options = {"English": "en", "Français": "fr", "Español": "es"}
    current_lang_name = [k for k, v in lang_options.items() if v == st.session_state.lang][0]
    selected = st.sidebar.selectbox("🌐 Language / Idioma", list(lang_options.keys()), index=list(lang_options.keys()).index(current_lang_name))
    st.session_state.lang = lang_options[selected]

# ---------- SIDEBAR COMMON ----------
def sidebar_common():
    st.sidebar.markdown(f"## {_('sidebar_company')}")
    st.sidebar.markdown(f"**{_('sidebar_founder')}**")
    st.sidebar.markdown(_("sidebar_phone"))
    st.sidebar.markdown(_("sidebar_email"))
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"[{_('sidebar_website')}](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.sidebar.markdown("---")
    language_selector()

# ---------- RADAR SIDEBAR SETTINGS ----------
def radar_sidebar():
    radar_lat = st.sidebar.number_input(_("radar_lat"), value=40.7128, format="%.5f")
    radar_lon = st.sidebar.number_input(_("radar_lon"), value=-74.0060, format="%.5f")
    max_range = st.sidebar.number_input(_("max_range"), min_value=30, max_value=2000, value=500, step=50)
    demo_mode = st.sidebar.checkbox(_("demo_mode_radar"), value=False)

    st.sidebar.divider()
    st.sidebar.markdown(f"## {_('data_source')}")
    if not demo_mode:
        st.sidebar.markdown(_("data_source_msg"))
        api_key = st.sidebar.text_input(_("api_key_input"), type="password", placeholder=_("api_key_placeholder"))
        if api_key:
            st.sidebar.info(_("global_active"))
        else:
            st.sidebar.info(_("opensky_active"))
    else:
        st.sidebar.info(_("demo_active"))
        api_key = ""

    st.sidebar.divider()
    st.sidebar.markdown(f"## {_('license_title')}")
    st.sidebar.markdown(_("license_text"))
    st.sidebar.markdown(_("prisme"))
    st.sidebar.markdown(_("email_contact"))
    st.sidebar.caption(_("terms"))

    if st.sidebar.button(_("refresh_radar"), use_container_width=True):
        st.rerun()

    return radar_lat, radar_lon, max_range, api_key, demo_mode

# ---------- LOGIN PAGE ----------
def login_page():
    st.title(f"🔐 {_('login_title')}")
    st.markdown(_("login_instruction"))
    with st.form("login_form"):
        password = st.text_input(_("password_label"), type="password")
        submitted = st.form_submit_button(_("login_button"))
        if submitted:
            if password == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(_("incorrect_password"))
    sidebar_common()

# ---------- RADAR COMPONENT (fixed f-string syntax) ----------
def radar_component(radar_lat, radar_lon, max_range, api_key, demo_mode):
    demo_mode_str = "true" if demo_mode else "false"
    # Use a template with placeholders to avoid f-string conflicts
    radar_html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Radar</title>
        <style>
            * {{ box-sizing: border-box; user-select: none; }}
            body {{ background: #0a0f1e; font-family: 'Segoe UI', 'Roboto', monospace; margin: 0; padding: 20px; color: #ccd6f6; }}
            .dashboard {{ max-width: 1000px; margin: 0 auto; }}
            .radar-container {{ background: #03060c; border-radius: 32px; padding: 20px; box-shadow: 0 20px 35px rgba(0,0,0,0.5); border: 1px solid #1e3a5f; margin-bottom: 20px; }}
            canvas {{ display: block; margin: 0 auto; background: radial-gradient(circle at 30% 20%, #07121f, #010101); border-radius: 50%; box-shadow: 0 0 0 2px #0e2a3a, 0 0 0 5px #03121f; width: 100%; max-width: 550px; height: auto; cursor: crosshair; }}
            .radar-stats {{ display: flex; justify-content: space-between; margin-top: 15px; font-size: 0.8rem; font-family: monospace; flex-wrap: wrap; gap: 10px; }}
            .badge {{ background: #0f172a; padding: 5px 12px; border-radius: 40px; border-left: 3px solid #2aff9e; }}
            .report-section {{ background: #0c1220; border-radius: 24px; padding: 20px; border: 1px solid #233453; }}
            .section-title {{ font-size: 1.2rem; margin-bottom: 15px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #2a3f60; padding-bottom: 8px; }}
            .table-wrapper {{ overflow-x: auto; border-radius: 20px; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 0.8rem; }}
            th, td {{ padding: 10px 8px; text-align: left; border-bottom: 1px solid #1f2c44; }}
            th {{ background: #07101f; color: #9effcf; font-weight: 600; }}
            tr:hover {{ background: #101a2c; cursor: pointer; }}
            .selected-row {{ background: #1a3a4e !important; border-left: 3px solid #2aff9e; }}
            .report-card {{ background: #030812; border-radius: 20px; padding: 15px; margin-top: 20px; border: 1px solid #2a4a6a; font-family: monospace; }}
            .report-card h3 {{ margin: 0 0 8px 0; color: #6effb0; }}
            footer {{ text-align: center; margin-top: 25px; font-size: 0.7rem; opacity: 0.6; }}
        </style>
    </head>
    <body>
    <div class="dashboard">
        <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
            <div>
                <h1>🔴 GLOBAL SURVEILLANCE RADAR (ADS-B)</h1>
                <div class="sub">Live global tracking | Military & drone detection | Space‑based coverage</div>
                <div class="owner">🇭🇹 Owner: Gesner Deslandes | GlobalInternet.py</div>
            </div>
            <div class="badge" id="liveStatus">🟢 LOADING</div>
        </div>

        <div class="radar-container">
            <canvas id="radarCanvas" width="550" height="550" style="width:100%; max-width:550px; height:auto; aspect-ratio:1/1"></canvas>
            <div class="radar-stats">
                <span>🎯 TARGETS: <strong id="targetCount">0</strong></span>
                <span>🟢 MOVING | 🔴 STATIC | 🔫 MILITARY | 🚁 DRONE</span>
                <span>📡 LAST UPDATE: <span id="lastUpdate">--</span></span>
                <span>📐 RANGE: <span id="rangeKmDisplay">__MAX_RANGE__</span> km</span>
            </div>
        </div>

        <div class="report-section">
            <div class="section-title">
                🛸 DASHBOARD REPORT — DETECTED OBJECTS (real-time)
                <span style="font-size:0.7rem;">click any row to view detailed report</span>
            </div>
            <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                <button id="downloadAllBtn" style="background:#0f7b3e; border-color:#2aff9e; box-shadow:0 0 5px #2aff9e66;">📥 Download All Data (CSV)</button>
            </div>
            <div class="table-wrapper">
                <table id="aircraftTable">
                    <thead>
                        <tr><th>CALLSIGN / ID</th><th>TYPE</th><th>LATITUDE</th><th>LONGITUDE</th><th>ALT (m)</th><th>SPEED (m/s)</th><th>STATUS</th><th>HEADING</th>觼
                    </thead>
                    <tbody id="tableBody">
                        <tr><td colspan="8">🔄 loading radar data...<\/td>觼
                    </tbody>
                表
            </div>
            <div id="detailedReport" class="report-card">
                <h3>📋 SPECIFIC OBJECT REPORT</h3>
                <div id="reportContent">Select any flying object from the list above to generate detailed intelligence report.</div>
                <div id="downloadButtonContainer" style="margin-top: 15px;"></div>
            </div>
        </div>
        <footer>⚠️ Real ADS-B data via OpenSky Network (live mode). Demo mode shows simulated aircraft.</footer>
    </div>

    <script>
        // Audio
        let audioCtx = null;
        function playBeep() {{
            try {{
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const now = audioCtx.currentTime;
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.frequency.value = 880;
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.exponentialRampToValueAtTime(0.00001, now + 0.2);
                osc.start(now);
                osc.stop(now + 0.2);
            }} catch(e) {{ console.log("Audio not supported"); }}
        }}

        // Military/Drone classification
        const MILITARY_ICAO_PREFIXES = [
            "AE","AD","AF","3C","3E","33","34","38","39","40","43","44","45","46","48",
            "4B","4C","4D","4E","4F","50","51","52","53","54","55","56","57","58","59",
            "5A","5B","5C","5D","5E","5F","60","61","62","63","64","65","66","67","68",
            "69","6A","6B","6C","6D","6E","6F","70","71","72","73","74","75","76","77",
            "78","79","7A","7B","7C","7D","7E","7F","80","81","82","83","84","85","86",
            "87","88","89","8A","8B","8C","8D","8E","8F","90","91","92","93","94","95",
            "96","97","98","99","9A","9B","9C","9D","9E","9F","A0","A1","A2","A3","A4",
            "A5","A6","A7","A8","A9","AA","AB","AC"
        ];
        const DRONE_ICAO_PREFIXES = [
            "4CAA","4CAB","4CAC","4CAD","4CAE","4CAF","4CB0","4CB1","4CB2","4CB3","4CB4",
            "4CB5","4CB6","4CB7","4CB8","4CB9","4CBA","4CBB","4CBC","4CBD","4CBE","4CBF"
        ];

        function classifyAircraft(icao24, callsign, velocity, altitude) {{
            let isMilitary = false, isDrone = false;
            const icaoUpper = (icao24 || "").toUpperCase();
            const callsignUpper = (callsign || "").toUpperCase();
            for (let prefix of MILITARY_ICAO_PREFIXES) if (icaoUpper.startsWith(prefix)) {{ isMilitary = true; break; }}
            const milKeywords = ["AF","NAVY","ARMY","AIR FORCE","MIL","RAAF","RAF","LUFT","ARMEE"];
            if (milKeywords.some(kw => callsignUpper.includes(kw))) isMilitary = true;
            for (let prefix of DRONE_ICAO_PREFIXES) if (icaoUpper.startsWith(prefix)) {{ isDrone = true; break; }}
            const droneKeywords = ["DRONE","UAV","DRON","QUAD","HEXA","OCTO"];
            if (droneKeywords.some(kw => callsignUpper.includes(kw))) isDrone = true;
            if (!isDrone && !isMilitary && altitude !== null && altitude < 500 && velocity !== null && velocity < 30) isDrone = true;
            let typeStr = "✈️ Civilian";
            if (isMilitary) typeStr = "🔫 Military";
            else if (isDrone) typeStr = "🚁 Drone";
            return {{ isMilitary: isMilitary, isDrone: isDrone, type: typeStr }};
        }}

        // Radar parameters
        const radarLat = __RADAR_LAT__;
        const radarLon = __RADAR_LON__;
        let maxRangeKm = __MAX_RANGE__;
        let apiKey = "__API_KEY__";
        const demoMode = __DEMO_MODE__;

        const canvas = document.getElementById('radarCanvas');
        const ctx = canvas.getContext('2d');
        const targetCountSpan = document.getElementById('targetCount');
        const lastUpdateSpan = document.getElementById('lastUpdate');
        const tableBody = document.getElementById('tableBody');
        const reportDiv = document.getElementById('reportContent');
        const downloadContainer = document.getElementById('downloadButtonContainer');
        const downloadAllBtn = document.getElementById('downloadAllBtn');

        let currentAircraft = [], selectedIcao = null, refreshTimer = null, animationId = null, canvasSize = 550;
        let lastSweepAngle = 0;

        function haversine(lat1, lon1, lat2, lon2) {{
            const R = 6371;
            const dLat = (lat2 - lat1) * Math.PI/180, dLon = (lon2 - lon1) * Math.PI/180;
            const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)**2;
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        }}
        function bearing(lat1, lon1, lat2, lon2) {{
            const φ1 = lat1*Math.PI/180, φ2 = lat2*Math.PI/180, Δλ = (lon2-lon1)*Math.PI/180;
            const y = Math.sin(Δλ) * Math.cos(φ2);
            const x = Math.cos(φ1)*Math.sin(φ2) - Math.sin(φ1)*Math.cos(φ2)*Math.cos(Δλ);
            return (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
        }}

        function generateDemoAircraft() {{
            const demoList = [];
            const names = ["DEMO1","DEMO2","DEMO3","DEMO4","DEMO5","DEMO6","DEMO7","DEMO8","DEMO9","DEMO10"];
            const types = ["🔫 Military","🚁 Drone","✈️ Civilian","🔫 Military","🚁 Drone","✈️ Civilian","✈️ Civilian","🔫 Military","🚁 Drone","✈️ Civilian"];
            for (let i = 0; i < 10; i++) {{
                const dist = Math.random() * maxRangeKm;
                const brng = Math.random() * 360;
                const lat = radarLat + (dist * Math.cos(brng * Math.PI/180)) / 111;
                const lon = radarLon + (dist * Math.sin(brng * Math.PI/180)) / (111 * Math.cos(radarLat * Math.PI/180));
                const alt = Math.random() * 8000 + 100;
                const vel = Math.random() * 150;
                const heading = Math.random() * 360;
                const classification = classifyAircraft("DEMO_"+i, names[i], vel, alt);
                demoList.push({{
                    icao24: "DEMO"+i,
                    callsign: names[i],
                    lat: lat,
                    lon: lon,
                    altitude: alt,
                    velocity: vel,
                    heading: heading,
                    onGround: false,
                    verticalRate: 0,
                    distance: dist,
                    bearing: brng,
                    isMilitary: classification.isMilitary,
                    isDrone: classification.isDrone,
                    type: classification.type
                }});
            }}
            return demoList;
        }}

        async function fetchLiveAircraft() {{
            if (demoMode) return generateDemoAircraft();
            try {{
                const url = "https://opensky-network.org/api/states/all";
                const resp = await fetch(url, {{ headers: {{ "User-Agent": "Mozilla/5.0 (compatible; RadarApp/1.0)" }} }});
                if (!resp.ok) throw new Error(`HTTP ${{resp.status}}`);
                const data = await resp.json();
                const states = data.states || [];
                const aircraft = [];
                for (let s of states) {{
                    const icao24 = s[0], callsign = s[1] ? s[1].trim() : null, lon = s[5], lat = s[6];
                    if (lat === null || lon === null) continue;
                    const dist = haversine(radarLat, radarLon, lat, lon);
                    if (dist > maxRangeKm) continue;
                    const classification = classifyAircraft(icao24, callsign, s[9], s[7]);
                    aircraft.push({{
                        icao24: icao24,
                        callsign: callsign || `FLT${{icao24.slice(-4)}}`,
                        lat: lat,
                        lon: lon,
                        altitude: s[7],
                        velocity: s[9],
                        heading: s[10],
                        onGround: s[8],
                        verticalRate: s[11],
                        distance: dist,
                        bearing: bearing(radarLat, radarLon, lat, lon),
                        isMilitary: classification.isMilitary,
                        isDrone: classification.isDrone,
                        type: classification.type
                    }});
                }}
                const unique = []; const seen = new Set();
                for (let ac of aircraft) if (!seen.has(ac.icao24)) {{ seen.add(ac.icao24); unique.push(ac); }}
                return unique;
            }} catch(err) {{
                console.error(err);
                document.getElementById('liveStatus').innerHTML = "⚠️ API ERROR";
                return null;
            }}
        }}

        function drawRadar(aircraftList, nowSeconds) {{
            if (!ctx) return;
            const w = canvasSize, h = canvasSize, cx = w/2, cy = h/2, maxR = w/2 - 25;
            ctx.clearRect(0, 0, w, h);
            ctx.beginPath(); ctx.arc(cx, cy, maxR, 0, 2*Math.PI); ctx.fillStyle = '#010a14'; ctx.fill(); ctx.strokeStyle = '#2bffaa30'; ctx.stroke();
            for (let r = 0.25; r <= 1; r+=0.25) {{
                let rad = maxR * r; ctx.beginPath(); ctx.arc(cx, cy, rad, 0, 2*Math.PI); ctx.strokeStyle = '#28e6a830'; ctx.setLineDash([4,6]); ctx.stroke();
                ctx.fillStyle = '#7f9fcf'; ctx.font = "10px monospace"; ctx.fillText((maxRangeKm*r).toFixed(0)+"km", cx+rad+3, cy-3);
            }}
            ctx.setLineDash([]);
            ctx.beginPath(); ctx.moveTo(cx, cy-12); ctx.lineTo(cx, cy+12); ctx.moveTo(cx-12, cy); ctx.lineTo(cx+12, cy); ctx.strokeStyle = '#2aff9e'; ctx.stroke();
            ctx.fillStyle = '#ffffff'; ctx.font = "bold 12px monospace"; ctx.fillText("N", cx-6, cy-maxR+12);
            const testDist = 100, testBrng = 45;
            if (testDist <= maxRangeKm) {{
                const ang = testBrng * Math.PI/180, rpx = (testDist/maxRangeKm)*maxR;
                const x = cx + rpx*Math.sin(ang), y = cy - rpx*Math.cos(ang);
                ctx.beginPath(); ctx.arc(x, y, 10, 0, 2*Math.PI); ctx.fillStyle = '#ffaa44'; ctx.fill(); ctx.strokeStyle = 'white'; ctx.stroke();
                ctx.fillStyle = 'white'; ctx.font = "bold 10px monospace"; ctx.fillText("TEST", x+12, y-8);
            }}
            for (let ac of aircraftList) {{
                if (ac.distance > maxRangeKm) continue;
                const ang = ac.bearing * Math.PI/180, rpx = (ac.distance/maxRangeKm)*maxR;
                const x = cx + rpx*Math.sin(ang), y = cy - rpx*Math.cos(ang);
                let color = '#2eff9e'; if (ac.isMilitary) color = '#ff4444'; else if (ac.isDrone) color = '#ffaa44'; else if (ac.velocity !== null && ac.velocity <= 0.5) color = '#ff5555';
                ctx.beginPath(); ctx.arc(x, y, 9, 0, 2*Math.PI); ctx.fillStyle = color; ctx.fill(); ctx.strokeStyle = 'white'; ctx.stroke();
                let label = ac.callsign ? ac.callsign.trim() : (ac.icao24 ? ac.icao24.slice(-5) : "???");
                if(label.length>6) label=label.slice(0,6);
                ctx.fillStyle = 'white'; ctx.fillText(label, x+10, y-6);
                if (selectedIcao === ac.icao24) {{
                    ctx.beginPath(); ctx.arc(x, y, 13, 0, 2*Math.PI); ctx.strokeStyle = '#ffdd77'; ctx.lineWidth = 2.5; ctx.stroke();
                }}
            }}
            const sweep = (nowSeconds * 1.2) % 360, radSweep = sweep * Math.PI/180;
            if (lastSweepAngle > 350 && sweep < 10) playBeep();
            lastSweepAngle = sweep;
            ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + maxR*Math.sin(radSweep), cy - maxR*Math.cos(radSweep)); ctx.strokeStyle = '#9effcf66'; ctx.stroke();
            ctx.beginPath(); ctx.arc(cx, cy, 4, 0, 2*Math.PI); ctx.fillStyle = '#ffaa44'; ctx.fill();
        }}

        function animate() {{ drawRadar(currentAircraft, Date.now()/1000); animationId = requestAnimationFrame(animate); }}

        async function refreshRadarData() {{
            const data = await fetchLiveAircraft();
            if (!data) {{
                document.getElementById('liveStatus').innerHTML = demoMode ? "🎮 DEMO MODE" : "⚠️ API ERROR";
                return;
            }}
            document.getElementById('liveStatus').innerHTML = demoMode ? "🎮 DEMO MODE" : "🟢 LIVE DATA (OpenSky)";
            currentAircraft = data;
            targetCountSpan.innerText = currentAircraft.length;
            lastUpdateSpan.innerText = new Date().toLocaleTimeString();
            renderTable(currentAircraft);
            if (selectedIcao) {{
                const found = currentAircraft.find(ac => ac.icao24 === selectedIcao);
                if (found) generateDetailedReport(found);
                else {{ reportDiv.innerHTML = "⚠️ Selected object no longer in radar coverage."; selectedIcao = null; }}
            }}
        }}

        function renderTable(list) {{
            if (!list.length) {{ tableBody.innerHTML = '<tr><td colspan="8">✈️ No flying objects detected within radar range.脉舶'; return; }}
            let html = '';
            for (let ac of list) {{
                const moving = (ac.velocity !== null && ac.velocity > 0.5);
                html += `<tr class="${selectedIcao === ac.icao24 ? 'selected-row' : ''}" data-icao="${ac.icao24}">
                            <td>${escapeHtml(ac.callsign)}<\/td>
                            <td>${ac.type}<\/td>
                            <td>${ac.lat.toFixed(4)}<\/td>
                            <td>${ac.lon.toFixed(4)}<\/td>
                            <td>${ac.altitude !== null ? ac.altitude.toFixed(0) : 'N/A'}<\/td>
                            <td>${ac.velocity !== null ? ac.velocity.toFixed(1) : '?'}<\/td>
                            <td>${moving ? '🟢 MOVING' : '🔴 STATIC'}<\/td>
                            <td>${ac.heading !== null ? ac.heading.toFixed(0)+'°' : '---'}<\/td>
                         <\/tr>`;
            }}
            tableBody.innerHTML = html;
            document.querySelectorAll('#aircraftTable tbody tr').forEach(row => {{
                row.addEventListener('click', () => {{
                    const icao = row.getAttribute('data-icao');
                    const ac = currentAircraft.find(a => a.icao24 === icao);
                    if (ac) {{
                        selectedIcao = icao;
                        generateDetailedReport(ac);
                        document.querySelectorAll('#aircraftTable tbody tr').forEach(r => r.classList.remove('selected-row'));
                        row.classList.add('selected-row');
                    }}
                }});
            }});
        }}

        function generateDetailedReport(ac) {{
            const moving = (ac.velocity !== null && ac.velocity > 0.5);
            const speedText = ac.velocity !== null ? `${ac.velocity.toFixed(2)} m/s (${(ac.velocity*3.6).toFixed(1)} km/h)` : 'unknown';
            const altText = ac.altitude !== null ? `${ac.altitude.toFixed(1)} meters (${(ac.altitude*3.28084).toFixed(0)} ft)` : 'not reported';
            const source = demoMode ? "DEMO MODE (simulated data)" : "OpenSky Network (live ADS‑B)";
            reportDiv.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                    <div><strong>✈️ OBJECT:</strong> ${escapeHtml(ac.callsign)}</div>
                    <div><strong>🆔 ICAO24:</strong> ${ac.icao24}</div>
                    <div><strong>📍 LAT/LON:</strong> ${ac.lat.toFixed(5)}, ${ac.lon.toFixed(5)}</div>
                    <div><strong>📏 ALTITUDE:</strong> ${altText}</div>
                    <div><strong>💨 SPEED:</strong> ${speedText}</div>
                    <div><strong>🧭 HEADING:</strong> ${ac.heading !== null ? ac.heading.toFixed(1)+'°' : 'unknown'}</div>
                    <div><strong>📈 VERTICAL RATE:</strong> ${ac.verticalRate !== null ? ac.verticalRate.toFixed(1)+' m/s' : 'N/A'}</div>
                    <div><strong>⚡ STATUS:</strong> ${moving ? '🟢 MOVING' : '🔴 STATIC (low velocity)'}</div>
                    <div><strong>🛬 ON GROUND:</strong> ${ac.onGround ? 'YES (on ground)' : 'AIRBORNE'}</div>
                    <div><strong>📡 RADAR RANGE:</strong> ${maxRangeKm} km from center</div>
                    <div><strong>🛡️ CLASSIFICATION:</strong> ${ac.type}</div>
                    <div><strong>📊 DATA SOURCE:</strong> ${source}</div>
                </div>
                <hr style="border-color:#2a4f6e; margin-top:12px;">
                <div style="font-size:0.75rem;">🔍 Real ADS-B data via OpenSky Network (live mode). Demo mode uses simulated objects for testing.</div>
            `;
            const reportText = `SURVEILLANCE REPORT (${demoMode ? "DEMO" : "LIVE"})\n===================\nObject: ${ac.callsign}\nICAO24: ${ac.icao24}\nType: ${ac.type}\nLatitude: ${ac.lat.toFixed(5)}\nLongitude: ${ac.lon.toFixed(5)}\nDistance from radar: ${ac.distance.toFixed(0)} km\nAltitude: ${altText}\nSpeed: ${speedText}\nHeading: ${ac.heading !== null ? ac.heading.toFixed(1)+'°' : 'unknown'}\nVertical Rate: ${ac.verticalRate !== null ? ac.verticalRate.toFixed(1)+' m/s' : 'N/A'}\nOn Ground: ${ac.onGround ? 'YES' : 'NO'}\nData source: ${source}\nTime of report: ${new Date().toLocaleString()}`;
            downloadContainer.innerHTML = `<button id="downloadReportBtn" style="background:#0f7b3e; border-color:#2aff9e;">📥 Download Report (TXT)</button>`;
            document.getElementById('downloadReportBtn').addEventListener('click', () => {{
                const blob = new Blob([reportText], {{type: 'text/plain'}});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a'); a.href = url; a.download = `${ac.callsign}_report.txt`; a.click(); URL.revokeObjectURL(url);
            }});
        }}

        function downloadAllCSV() {{
            if (!currentAircraft.length) {{ alert("No data to download."); return; }}
            const headers = ["Callsign","Type","Latitude","Longitude","Altitude (m)","Speed (m/s)","Status","Heading","Distance (km)"];
            const rows = currentAircraft.map(ac => [
                ac.callsign, ac.type, ac.lat.toFixed(5), ac.lon.toFixed(5),
                ac.altitude !== null ? ac.altitude.toFixed(1) : "N/A",
                ac.velocity !== null ? ac.velocity.toFixed(1) : "?",
                (ac.velocity !== null && ac.velocity > 0.5) ? "MOVING" : "STATIC",
                ac.heading !== null ? ac.heading.toFixed(0)+"°" : "---",
                ac.distance.toFixed(0)
            ]);
            const csv = [headers, ...rows].map(row => row.map(cell => `"${cell}"`).join(",")).join("\n");
            const blob = new Blob([csv], {{type: "text/csv"}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href = url; a.download = `radar_data_${new Date().toISOString().slice(0,19).replace(/:/g, "-")}.csv`; a.click(); URL.revokeObjectURL(url);
        }}

        function escapeHtml(str) {{ if(!str) return ''; return str.replace(/[&<>]/g, function(m){{if(m==='&') return '&amp;'; if(m==='<') return '&lt;'; if(m==='>') return '&gt;'; return m;}}); }}

        function init() {{
            canvas.width = 550; canvas.height = 550; canvasSize = 550;
            refreshRadarData();
            refreshTimer = setInterval(() => refreshRadarData(), 60000);
        }}
        downloadAllBtn.addEventListener('click', downloadAllCSV);
        init();
        animate();
    </script>
    </body>
    </html>
    """
    # Replace placeholders
    radar_html = radar_html_template.replace("__RADAR_LAT__", str(radar_lat))
    radar_html = radar_html.replace("__RADAR_LON__", str(radar_lon))
    radar_html = radar_html.replace("__MAX_RANGE__", str(max_range))
    radar_html = radar_html.replace("__API_KEY__", api_key)
    radar_html = radar_html.replace("__DEMO_MODE__", demo_mode_str)
    components.html(radar_html, height=950, scrolling=True)

# ---------- SATELLITE TRACKER (with demo mode and list) ----------
def satellite_tracker(demo_mode_satellite):
    st.markdown(f"## {_('satellite_title')}")
    if demo_mode_satellite:
        st.info(_("demo_satellite_note"))
    else:
        st.markdown(_("satellite_desc"))
    demo_flag = "true" if demo_mode_satellite else "false"
    satellite_html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            #map {{ height: 450px; width: 100%; background: #0a0f1e; border-radius: 20px; margin-bottom: 20px; }}
            body {{ background: #0a0f1e; margin: 0; padding: 0; }}
            .info {{ text-align: center; color: #ccd6f6; font-family: monospace; margin-top: 10px; }}
            .satellite-badge {{ background: #1e3a5f; padding: 5px 12px; border-radius: 20px; display: inline-block; margin: 5px; }}
            .sat-list {{ background: #0c1220; border-radius: 20px; padding: 15px; margin-top: 20px; border: 1px solid #233453; }}
            .sat-list h3 {{ margin: 0 0 10px 0; color: #9effcf; }}
            .sat-item {{ background: #0f172a; margin: 8px 0; padding: 8px 12px; border-radius: 12px; cursor: pointer; transition: 0.2s; display: flex; justify-content: space-between; }}
            .sat-item:hover {{ background: #1a3a4e; }}
            .selected-sat {{ background: #1a3a4e; border-left: 3px solid #2aff9e; }}
            .report-panel {{ margin-top: 20px; background: #030812; border-radius: 20px; padding: 15px; border: 1px solid #2a4a6a; }}
            button {{ background: #0f7b3e; border: none; color: white; padding: 8px 16px; border-radius: 30px; cursor: pointer; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div class="sat-list">
            <h3>🛰️ DETECTED SATELLITES (click to generate report)</h3>
            <div id="satelliteList"></div>
        </div>
        <div id="reportPanel" class="report-panel">
            <h3>📋 SATELLITE REPORT</h3>
            <div id="reportContent">Select a satellite from the list to generate a detailed report.</div>
            <div id="downloadBtnContainer"></div>
        </div>
        <div class="info">
            <span class="satellite-badge">🛰️ ISS (yellow)</span>
            <span class="satellite-badge">🔭 Hubble (cyan)</span>
            <span class="satellite-badge">🌍 Tiangong (orange)</span>
            <span class="satellite-badge">🛸 Demo sats (magenta)</span>
            <p>📍 Positions update every 5 seconds | Data: wheretheiss.at (live) or simulated (demo)</p>
        </div>

        <script>
            let audioCtx = null;
            function playBeep() {{
                try {{
                    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    const now = audioCtx.currentTime;
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.frequency.value = 440;
                    gain.gain.setValueAtTime(0.08, now);
                    gain.gain.exponentialRampToValueAtTime(0.00001, now + 0.15);
                    osc.start(now);
                    osc.stop(now + 0.15);
                }} catch(e) {{}}
            }}

            const demoMode = __DEMO_MODE__;
            var map = L.map('map').setView([0, 0], 2);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> & CartoDB',
                subdomains: 'abcd',
                maxZoom: 19,
                minZoom: 2
            }}).addTo(map);
            
            var markers = {{}};
            var satelliteData = [];
            var selectedSatId = null;
            var updateInterval = null;

            function getDemoSatellites() {{
                return [
                    {{ id: "DEMO1", name: "GeoEye-1", lat: 28.6, lng: -80.6, alt: 681, vel: 7.5, type: "🌍 Earth Imaging" }},
                    {{ id: "DEMO2", name: "Landsat-9", lat: 45.0, lng: -110.0, alt: 705, vel: 7.4, type: "📸 Remote Sensing" }},
                    {{ id: "DEMO3", name: "NOAA-20", lat: -15.0, lng: -150.0, alt: 824, vel: 7.3, type: "🌦️ Weather" }},
                    {{ id: "DEMO4", name: "Starlink-1234", lat: 52.0, lng: -40.0, alt: 550, vel: 7.6, type: "📡 Communications" }},
                    {{ id: "DEMO5", name: "GPS BIIF-10", lat: 12.0, lng: 70.0, alt: 20200, vel: 3.9, type: "🛰️ Navigation" }}
                ];
            }}

            function fetchRealSatellites() {{
                return Promise.all([
                    fetch('https://api.wheretheiss.at/v1/satellites/25544').then(r => r.json()).then(data => ({{ id: "ISS", name: "ISS (International Space Station)", lat: data.latitude, lng: data.longitude, alt: data.altitude, vel: data.velocity, type: "🛰️ Manned" }})),
                    fetch('https://api.wheretheiss.at/v1/satellites/20580').then(r => r.json()).then(data => ({{ id: "HUBBLE", name: "Hubble Space Telescope", lat: data.latitude, lng: data.longitude, alt: data.altitude, vel: data.velocity, type: "🔭 Telescope" }})),
                    fetch('https://api.wheretheiss.at/v1/satellites/48274').then(r => r.json()).then(data => ({{ id: "TIANGONG", name: "Tiangong Space Station", lat: data.latitude, lng: data.longitude, alt: data.altitude, vel: data.velocity, type: "🛰️ Manned" }}))
                ]);
            }}

            function updateSatellites() {{
                if (demoMode) {{
                    satelliteData = getDemoSatellites();
                    playBeep();
                    renderSatellites();
                }} else {{
                    fetchRealSatellites().then(sats => {{
                        satelliteData = sats;
                        playBeep();
                        renderSatellites();
                    }}).catch(err => console.error("Satellite fetch error:", err));
                }}
            }}

            function renderSatellites() {{
                for (let sat of satelliteData) {{
                    if (markers[sat.id]) {{
                        markers[sat.id].setLatLng([sat.lat, sat.lng]);
                    }} else {{
                        let iconHtml = "🛸";
                        if (sat.id === "ISS") iconHtml = "🛰️";
                        else if (sat.id === "HUBBLE") iconHtml = "🔭";
                        else if (sat.id === "TIANGONG") iconHtml = "🌍";
                        markers[sat.id] = L.marker([sat.lat, sat.lng], {{
                            icon: L.divIcon({{ html: iconHtml, className: "sat-marker", iconSize: [30,30] }})
                        }}).bindPopup(`<b>${{sat.name}}</b><br>Alt: ${{sat.alt.toFixed(0)}} km<br>Vel: ${{sat.vel.toFixed(0)}} km/h`).addTo(map);
                    }}
                }}
                for (let id in markers) {{
                    if (!satelliteData.find(s => s.id === id)) {{
                        map.removeLayer(markers[id]);
                        delete markers[id];
                    }}
                }}
                const listContainer = document.getElementById('satelliteList');
                let html = '';
                for (let sat of satelliteData) {{
                    const cls = (selectedSatId === sat.id) ? "selected-sat" : "";
                    html += `<div class="sat-item ${cls}" data-id="${sat.id}">
                                <span><strong>${sat.name}</strong></span>
                                <span>📍 ${sat.lat.toFixed(2)}, ${sat.lng.toFixed(2)}</span>
                                <span>📏 ${sat.alt.toFixed(0)} km</span>
                            </div>`;
                }}
                listContainer.innerHTML = html;
                document.querySelectorAll('.sat-item').forEach(el => {{
                    el.addEventListener('click', () => {{
                        const id = el.getAttribute('data-id');
                        const sat = satelliteData.find(s => s.id === id);
                        if (sat) {{
                            selectedSatId = id;
                            generateSatelliteReport(sat);
                            document.querySelectorAll('.sat-item').forEach(i => i.classList.remove('selected-sat'));
                            el.classList.add('selected-sat');
                        }}
                    }});
                }});
            }}

            function generateSatelliteReport(sat) {{
                const source = demoMode ? "DEMO MODE (simulated)" : "wheretheiss.at API (live)";
                const reportDiv = document.getElementById('reportContent');
                reportDiv.innerHTML = `
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                        <div><strong>🛰️ NAME:</strong> ${sat.name}</div>
                        <div><strong>🆔 ID:</strong> ${sat.id}</div>
                        <div><strong>📍 LATITUDE:</strong> ${sat.lat.toFixed(5)}</div>
                        <div><strong>📍 LONGITUDE:</strong> ${sat.lng.toFixed(5)}</div>
                        <div><strong>📏 ALTITUDE:</strong> ${sat.alt.toFixed(1)} km</div>
                        <div><strong>💨 VELOCITY:</strong> ${sat.vel.toFixed(1)} km/h</div>
                        <div><strong>📡 TYPE:</strong> ${sat.type || "Satellite"}</div>
                        <div><strong>📊 DATA SOURCE:</strong> ${source}</div>
                    </div>
                    <hr style="border-color:#2a4f6e; margin-top:12px;">
                    <div style="font-size:0.75rem;">🔍 Live data from wheretheiss.at or demo simulation.</div>
                `;
                const reportText = `SATELLITE REPORT (${demoMode ? "DEMO" : "LIVE"})\n===================\nName: ${sat.name}\nID: ${sat.id}\nLatitude: ${sat.lat.toFixed(5)}\nLongitude: ${sat.lng.toFixed(5)}\nAltitude: ${sat.alt.toFixed(1)} km\nVelocity: ${sat.vel.toFixed(1)} km/h\nType: ${sat.type || "Satellite"}\nData source: ${source}\nTime of report: ${new Date().toLocaleString()}`;
                const btnContainer = document.getElementById('downloadBtnContainer');
                btnContainer.innerHTML = `<button id="downloadSatReportBtn">📥 Download Report (TXT)</button>`;
                document.getElementById('downloadSatReportBtn').addEventListener('click', () => {{
                    const blob = new Blob([reportText], {{type: 'text/plain'}});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a'); a.href = url; a.download = `${sat.name.replace(/ /g, "_")}_report.txt`; a.click(); URL.revokeObjectURL(url);
                }});
            }}

            updateSatellites();
            updateInterval = setInterval(updateSatellites, 5000);
        </script>
    </body>
    </html>
    """
    satellite_html = satellite_html_template.replace("__DEMO_MODE__", demo_flag)
    components.html(satellite_html, height=800, scrolling=False)
    st.caption(_("satellite_credit"))

# ---------- MAIN PAGE ----------
def main_page():
    sidebar_common()
    if st.sidebar.button(_("logout_button"), use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    tab1, tab2 = st.tabs([_("tab_radar"), _("tab_satellite")])
    with tab1:
        radar_lat, radar_lon, max_range, api_key, demo_mode = radar_sidebar()
        radar_component(radar_lat, radar_lon, max_range, api_key, demo_mode)
    with tab2:
        demo_sat = st.sidebar.checkbox(_("demo_mode_satellite"), value=False)
        satellite_tracker(demo_sat)

# ---------- ROUTING ----------
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
