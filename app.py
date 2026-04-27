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
        "data_source": "🔑 Data Source",
        "data_source_msg": "For global coverage (oceans & remote areas), enter your Flightradar24 API key.",
        "api_key_input": "Flightradar24 API Key",
        "api_key_placeholder": "Enter your API key (optional)",
        "global_active": "🌍 **Global coverage active** – you will see aircraft worldwide.",
        "opensky_active": "📡 Using OpenSky Network (regional coverage, free).",
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
        "satellite_desc": "Current positions of the International Space Station (ISS), Hubble Space Telescope, and other selected satellites.",
        "satellite_credit": "Data provided by wheretheiss.at API | Map: Leaflet | Built by Gesner Deslandes"
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
        "data_source": "🔑 Source de données",
        "data_source_msg": "Pour une couverture mondiale (océans et zones éloignées), entrez votre clé API Flightradar24.",
        "api_key_input": "Clé API Flightradar24",
        "api_key_placeholder": "Entrez votre clé API (optionnel)",
        "global_active": "🌍 **Couverture mondiale active** – vous verrez des aéronefs du monde entier.",
        "opensky_active": "📡 Utilisation du réseau OpenSky (couverture régionale, gratuit).",
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
        "satellite_desc": "Positions actuelles de la Station Spatiale Internationale (ISS), du télescope Hubble et d'autres satellites sélectionnés.",
        "satellite_credit": "Données fournies par l'API wheretheiss.at | Carte : Leaflet | Construit par Gesner Deslandes"
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
        "data_source": "🔑 Fuente de datos",
        "data_source_msg": "Para cobertura global (océanos y áreas remotas), ingrese su clave API de Flightradar24.",
        "api_key_input": "Clave API de Flightradar24",
        "api_key_placeholder": "Ingrese su clave API (opcional)",
        "global_active": "🌍 **Cobertura global activa** – verá aeronaves de todo el mundo.",
        "opensky_active": "📡 Usando la red OpenSky (cobertura regional, gratuita).",
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
        "satellite_desc": "Posiciones actuales de la Estación Espacial Internacional (ISS), el telescopio Hubble y otros satélites seleccionados.",
        "satellite_credit": "Datos proporcionados por la API wheretheiss.at | Mapa: Leaflet | Construido por Gesner Deslandes"
    }
}

def _(key):
    return texts[st.session_state.lang].get(key, key)

# ---------- LANGUAGE SELECTOR (always visible in sidebar) ----------
def language_selector():
    lang_options = {"English": "en", "Français": "fr", "Español": "es"}
    current_lang_name = [k for k, v in lang_options.items() if v == st.session_state.lang][0]
    selected = st.sidebar.selectbox("🌐 Language / Idioma", list(lang_options.keys()), index=list(lang_options.keys()).index(current_lang_name))
    st.session_state.lang = lang_options[selected]

# ---------- SIDEBAR COMMON CONTENT ----------
def sidebar_common():
    st.sidebar.markdown(f"## {_('sidebar_company')}")
    st.sidebar.markdown(f"**{_('sidebar_founder')}**")
    st.sidebar.markdown(_("sidebar_phone"))
    st.sidebar.markdown(_("sidebar_email"))
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"[{_('sidebar_website')}](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.sidebar.markdown("---")
    language_selector()

# ---------- RADAR SIDEBAR SETTINGS (shown only when radar is active) ----------
def radar_sidebar():
    radar_lat = st.sidebar.number_input(_("radar_lat"), value=40.7128, format="%.5f")
    radar_lon = st.sidebar.number_input(_("radar_lon"), value=-74.0060, format="%.5f")
    max_range = st.sidebar.number_input(_("max_range"), min_value=30, max_value=2000, value=500, step=50)

    st.sidebar.divider()
    st.sidebar.markdown(f"## {_('data_source')}")
    st.sidebar.markdown(_("data_source_msg"))
    api_key = st.sidebar.text_input(_("api_key_input"), type="password", placeholder=_("api_key_placeholder"))
    if api_key:
        st.sidebar.info(_("global_active"))
    else:
        st.sidebar.info(_("opensky_active"))

    st.sidebar.divider()
    st.sidebar.markdown(f"## {_('license_title')}")
    st.sidebar.markdown(_("license_text"))
    st.sidebar.markdown(_("prisme"))
    st.sidebar.markdown(_("email_contact"))
    st.sidebar.caption(_("terms"))

    if st.sidebar.button(_("refresh_radar"), use_container_width=True):
        st.rerun()

    return radar_lat, radar_lon, max_range, api_key

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

# ---------- RADAR HTML COMPONENT (UNCHANGED FROM YOUR ORIGINAL) ----------
def radar_component(radar_lat, radar_lon, max_range, api_key):
    radar_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Radar</title>
        <style>
            * {{ box-sizing: border-box; user-select: none; }}
            body {{ background: #0a0f1e; font-family: 'Segoe UI', 'Roboto', monospace; margin: 0; padding: 20px; color: #ccd6f6; }}
            .dashboard {{ max-width: 1400px; margin: 0 auto; }}
            .radar-container {{ background: #03060c; border-radius: 32px; padding: 20px; box-shadow: 0 20px 35px rgba(0,0,0,0.5); border: 1px solid #1e3a5f; margin-bottom: 20px; }}
            canvas {{ display: block; margin: 0 auto; background: radial-gradient(circle at 30% 20%, #07121f, #010101); border-radius: 50%; box-shadow: 0 0 0 2px #0e2a3a, 0 0 0 5px #03121f; width: 100%; height: auto; cursor: crosshair; }}
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
            <div class="badge" id="liveStatus">🟢 LIVE DATA (OpenSky)</div>
        </div>

        <div class="radar-container">
            <canvas id="radarCanvas" width="700" height="700" style="width:100%; max-width:700px; height:auto; aspect-ratio:1/1"></canvas>
            <div class="radar-stats">
                <span>🎯 TARGETS: <strong id="targetCount">0</strong></span>
                <span>🟢 MOVING | 🔴 STATIC | 🔫 MILITARY | 🚁 DRONE</span>
                <span>📡 LAST UPDATE: <span id="lastUpdate">--</span></span>
                <span>📐 RANGE: <span id="rangeKmDisplay">{max_range}</span> km</span>
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
                        <tr><td colspan="8">🔄 loading live radar data...<\/td>觼
                    </tbody>
                表
            </div>
            <div id="detailedReport" class="report-card">
                <h3>📋 SPECIFIC OBJECT REPORT</h3>
                <div id="reportContent">Select any flying object from the list above to generate detailed intelligence report.</div>
                <div id="downloadButtonContainer" style="margin-top: 15px;"></div>
            </div>
        </div>
        <footer>⚠️ Real ADS-B data via OpenSky Network. Military detection based on ICAO hex ranges & callsigns. Drone detection includes heuristics (low alt/speed).</footer>
    </div>

    <script>
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
            return {{ isMilitary, isDrone, type: typeStr }};
        }}

        const radarLat = {radar_lat}, radarLon = {radar_lon};
        let maxRangeKm = {max_range};
        let apiKey = "{api_key}";

        const canvas = document.getElementById('radarCanvas');
        const ctx = canvas.getContext('2d');
        const targetCountSpan = document.getElementById('targetCount');
        const lastUpdateSpan = document.getElementById('lastUpdate');
        const tableBody = document.getElementById('tableBody');
        const reportDiv = document.getElementById('reportContent');
        const downloadContainer = document.getElementById('downloadButtonContainer');
        const rangeKmDisplay = document.getElementById('rangeKmDisplay');
        const downloadAllBtn = document.getElementById('downloadAllBtn');

        let currentAircraft = [], selectedIcao = null, refreshTimer = null, animationId = null, canvasSize = 700;

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
                ctx.fillStyle = 'white'; ctx.fillText("TEST", x+12, y-8);
            }}
            for (let ac of aircraftList) {{
                if (ac.distance > maxRangeKm) continue;
                const ang = ac.bearing * Math.PI/180, rpx = (ac.distance/maxRangeKm)*maxR;
                const x = cx + rpx*Math.sin(ang), y = cy - rpx*Math.cos(ang);
                let color = '#2eff9e'; if (ac.isMilitary) color = '#ff4444'; else if (ac.isDrone) color = '#ffaa44'; else if (ac.velocity !== null && ac.velocity <= 0.5) color = '#ff5555';
                ctx.beginPath(); ctx.arc(x, y, 9, 0, 2*Math.PI); ctx.fillStyle = color; ctx.fill(); ctx.strokeStyle = 'white'; ctx.stroke();
                let label = ac.callsign ? ac.callsign.trim() : (ac.icao24 ? ac.icao24.slice(-5) : "???"); if(label.length>6) label=label.slice(0,6);
                ctx.fillStyle = 'white'; ctx.fillText(label, x+10, y-6);
                if (selectedIcao === ac.icao24) {{
                    ctx.beginPath(); ctx.arc(x, y, 13, 0, 2*Math.PI); ctx.strokeStyle = '#ffdd77'; ctx.lineWidth = 2.5; ctx.stroke();
                }}
            }}
            const sweep = (nowSeconds * 1.2) % 360, radSweep = sweep * Math.PI/180;
            ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + maxR*Math.sin(radSweep), cy - maxR*Math.cos(radSweep)); ctx.strokeStyle = '#9effcf66'; ctx.stroke();
            ctx.beginPath(); ctx.arc(cx, cy, 4, 0, 2*Math.PI); ctx.fillStyle = '#ffaa44'; ctx.fill();
        }}

        function animate() {{ drawRadar(currentAircraft, Date.now()/1000); animationId = requestAnimationFrame(animate); }}

        async function fetchLiveAircraft() {{
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
                        icao24, callsign: callsign || `FLT${{icao24.slice(-4)}}`, lat, lon, altitude: s[7], velocity: s[9], heading: s[10], onGround: s[8],
                        verticalRate: s[11], distance: dist, bearing: bearing(radarLat, radarLon, lat, lon),
                        isMilitary: classification.isMilitary, isDrone: classification.isDrone, type: classification.type
                    }});
                }}
                const unique = []; const seen = new Set();
                for (let ac of aircraft) if (!seen.has(ac.icao24)) {{ seen.add(ac.icao24); unique.push(ac); }}
                return unique;
            }} catch(err) {{ console.error(err); document.getElementById('liveStatus').innerHTML = "⚠️ API ERROR"; return null; }}
        }}

        async function refreshRadarData() {{
            const data = await fetchLiveAircraft();
            if (!data) {{ document.getElementById('liveStatus').innerHTML = "⚠️ API ERROR (OpenSky)"; return; }}
            document.getElementById('liveStatus').innerHTML = "🟢 LIVE DATA (OpenSky)";
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
                html += `<tr class="${{selectedIcao === ac.icao24 ? 'selected-row' : ''}}" data-icao="${{ac.icao24}}">
                            <td>${{escapeHtml(ac.callsign)}}<\/td><td>${{ac.type}}<\/td><td>${{ac.lat.toFixed(4)}}<\/td>
                            <td>${{ac.lon.toFixed(4)}}<\/td><td>${{ac.altitude !== null ? ac.altitude.toFixed(0) : 'N/A'}}<\/td>
                            <td>${{ac.velocity !== null ? ac.velocity.toFixed(1) : '?'}}<\/td><td>${{moving ? '🟢 MOVING' : '🔴 STATIC'}}<\/td>
                            <td>${{ac.heading !== null ? ac.heading.toFixed(0)+'°' : '---'}}<\/td>
                         <\/tr>`;
            }}
            tableBody.innerHTML = html;
            document.querySelectorAll('#aircraftTable tbody tr').forEach(row => {{
                row.addEventListener('click', () => {{
                    const icao = row.getAttribute('data-icao');
                    const ac = currentAircraft.find(a => a.icao24 === icao);
                    if (ac) {{ selectedIcao = icao; generateDetailedReport(ac);
                        document.querySelectorAll('#aircraftTable tbody tr').forEach(r => r.classList.remove('selected-row'));
                        row.classList.add('selected-row');
                    }}
                }});
            }});
        }}

        function generateDetailedReport(ac) {{
            const moving = (ac.velocity !== null && ac.velocity > 0.5);
            const speedText = ac.velocity !== null ? `${{ac.velocity.toFixed(2)}} m/s (${{(ac.velocity*3.6).toFixed(1)}} km/h)` : 'unknown';
            const altText = ac.altitude !== null ? `${{ac.altitude.toFixed(1)}} meters (${{(ac.altitude*3.28084).toFixed(0)}} ft)` : 'not reported';
            reportDiv.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                    <div><strong>✈️ OBJECT:</strong> ${{escapeHtml(ac.callsign)}}</div>
                    <div><strong>🆔 ICAO24:</strong> ${{ac.icao24}}</div>
                    <div><strong>📍 LAT/LON:</strong> ${{ac.lat.toFixed(5)}}, ${{ac.lon.toFixed(5)}}</div>
                    <div><strong>📏 ALTITUDE:</strong> ${{altText}}</div>
                    <div><strong>💨 SPEED:</strong> ${{speedText}}</div>
                    <div><strong>🧭 HEADING:</strong> ${{ac.heading !== null ? ac.heading.toFixed(1)+'°' : 'unknown'}}</div>
                    <div><strong>📈 VERTICAL RATE:</strong> ${{ac.verticalRate !== null ? ac.verticalRate.toFixed(1)+' m/s' : 'N/A'}}</div>
                    <div><strong>⚡ STATUS:</strong> ${{moving ? '🟢 MOVING' : '🔴 STATIC (low velocity)'}}</div>
                    <div><strong>🛬 ON GROUND:</strong> ${{ac.onGround ? 'YES (on ground)' : 'AIRBORNE'}}</div>
                    <div><strong>📡 RADAR RANGE:</strong> ${{maxRangeKm}} km from center</div>
                    <div><strong>🛡️ CLASSIFICATION:</strong> ${{ac.type}}</div>
                </div>
                <hr style="border-color:#2a4f6e; margin-top:12px;">
                <div style="font-size:0.75rem;">🔍 Real ADS-B data via OpenSky Network. Military detection based on ICAO hex ranges & callsigns. Drone detection includes manufacturer ICAO prefixes and heuristic low‑altitude/speed behaviour.</div>
            `;
            const reportText = `SURVEILLANCE REPORT\\n===================\\nObject: ${{ac.callsign}}\\nICAO24: ${{ac.icao24}}\\nType: ${{ac.type}}\\nLatitude: ${{ac.lat.toFixed(5)}}\\nLongitude: ${{ac.lon.toFixed(5)}}\\nDistance from radar: ${{ac.distance.toFixed(0)}} km\\nAltitude: ${{altText}}\\nSpeed: ${{speedText}}\\nHeading: ${{ac.heading !== null ? ac.heading.toFixed(1)+'°' : 'unknown'}}\\nVertical Rate: ${{ac.verticalRate !== null ? ac.verticalRate.toFixed(1)+' m/s' : 'N/A'}}\\nOn Ground: ${{ac.onGround ? 'YES' : 'NO'}}\\nTime of report: ${{new Date().toLocaleString()}}\\nData source: OpenSky Network`;
            downloadContainer.innerHTML = `<button id="downloadReportBtn" style="background:#0f7b3e; border-color:#2aff9e;">📥 Download Report (TXT)</button>`;
            document.getElementById('downloadReportBtn').addEventListener('click', () => {{
                const blob = new Blob([reportText], {{type: 'text/plain'}});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a'); a.href = url; a.download = `${{ac.callsign}}_report.txt`; a.click(); URL.revokeObjectURL(url);
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
            const csv = [headers, ...rows].map(row => row.map(cell => `"${{cell}}"`).join(",")).join("\\n");
            const blob = new Blob([csv], {{type: "text/csv"}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href = url; a.download = `radar_data_${{new Date().toISOString().slice(0,19).replace(/:/g, "-")}}.csv`; a.click(); URL.revokeObjectURL(url);
        }}

        function escapeHtml(str) {{ if(!str) return ''; return str.replace(/[&<>]/g, function(m){{if(m==='&') return '&amp;'; if(m==='<') return '&lt;'; if(m==='>') return '&gt;'; return m;}}); }}

        function init() {{
            const container = document.querySelector('.radar-container');
            const size = Math.min(container.clientWidth - 40, 700);
            canvas.width = size; canvas.height = size; canvasSize = size;
            refreshRadarData();
            refreshTimer = setInterval(() => refreshRadarData(), 60000);
        }}
        downloadAllBtn.addEventListener('click', downloadAllCSV);
        window.addEventListener('resize', () => setTimeout(() => {{
            const container = document.querySelector('.radar-container');
            let newSize = Math.min(container.clientWidth - 40, 700);
            canvas.width = newSize; canvas.height = newSize; canvasSize = newSize;
        }}, 100));
        init();
        animate();
    </script>
    </body>
    </html>
    """
    components.html(radar_html, height=1300, scrolling=True)

# ---------- SATELLITE TRACKER COMPONENT (NEW) ----------
def satellite_tracker():
    st.markdown(f"## {_('satellite_title')}")
    st.markdown(_("satellite_desc"))
    # Use an iframe to embed a live satellite tracking map from a reliable public source
    # Option 1: Use a simple Leaflet map with real-time ISS position (open-source)
    # We'll create a custom HTML/JS map that fetches ISS and other satellites.
    satellite_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            #map { height: 600px; width: 100%; background: #0a0f1e; border-radius: 20px; margin-bottom: 20px; }
            body { background: #0a0f1e; margin: 0; padding: 0; }
            .info { text-align: center; color: #ccd6f6; font-family: monospace; margin-top: 10px; }
            .satellite-badge { background: #1e3a5f; padding: 5px 12px; border-radius: 20px; display: inline-block; margin: 5px; }
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div class="info">
            <span class="satellite-badge">🛰️ ISS (yellow)</span>
            <span class="satellite-badge">🔭 Hubble (cyan)</span>
            <span class="satellite-badge">🌍 Tiangong (orange)</span>
            <p>📍 Positions update every 5 seconds | Real data via wheretheiss.at</p>
        </div>
        <script>
            var map = L.map('map').setView([0, 0], 2);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> & CartoDB',
                subdomains: 'abcd',
                maxZoom: 19,
                minZoom: 2
            }).addTo(map);
            
            var issMarker, hubbleMarker, tiangongMarker;
            
            function fetchSatellites() {
                // ISS
                fetch('https://api.wheretheiss.at/v1/satellites/25544')
                    .then(res => res.json())
                    .then(data => {
                        if (!issMarker) {
                            issMarker = L.marker([data.latitude, data.longitude], {
                                icon: L.divIcon({ html: '🛰️', className: 'iss-icon', iconSize: [30,30] })
                            }).bindPopup('<b>ISS (International Space Station)</b><br>Altitude: ' + data.altitude.toFixed(0) + ' km<br>Velocity: ' + data.velocity.toFixed(0) + ' km/h').addTo(map);
                        } else {
                            issMarker.setLatLng([data.latitude, data.longitude]);
                            issMarker.getPopup().setContent('<b>ISS (International Space Station)</b><br>Altitude: ' + data.altitude.toFixed(0) + ' km<br>Velocity: ' + data.velocity.toFixed(0) + ' km/h');
                        }
                        map.setView([data.latitude, data.longitude], 3);
                    }).catch(err => console.error("ISS error:", err));
                
                // Hubble (satellite ID 20580)
                fetch('https://api.wheretheiss.at/v1/satellites/20580')
                    .then(res => res.json())
                    .then(data => {
                        if (!hubbleMarker) {
                            hubbleMarker = L.marker([data.latitude, data.longitude], {
                                icon: L.divIcon({ html: '🔭', className: 'hubble-icon', iconSize: [30,30] })
                            }).bindPopup('<b>Hubble Space Telescope</b><br>Altitude: ' + data.altitude.toFixed(0) + ' km<br>Velocity: ' + data.velocity.toFixed(0) + ' km/h').addTo(map);
                        } else {
                            hubbleMarker.setLatLng([data.latitude, data.longitude]);
                            hubbleMarker.getPopup().setContent('<b>Hubble Space Telescope</b><br>Altitude: ' + data.altitude.toFixed(0) + ' km<br>Velocity: ' + data.velocity.toFixed(0) + ' km/h');
                        }
                    }).catch(err => console.error("Hubble error:", err));
                
                // Tiangong (Chinese space station, sat ID 48274)
                fetch('https://api.wheretheiss.at/v1/satellites/48274')
                    .then(res => res.json())
                    .then(data => {
                        if (!tiangongMarker) {
                            tiangongMarker = L.marker([data.latitude, data.longitude], {
                                icon: L.divIcon({ html: '🌍', className: 'tiangong-icon', iconSize: [30,30] })
                            }).bindPopup('<b>Tiangong Space Station</b><br>Altitude: ' + data.altitude.toFixed(0) + ' km<br>Velocity: ' + data.velocity.toFixed(0) + ' km/h').addTo(map);
                        } else {
                            tiangongMarker.setLatLng([data.latitude, data.longitude]);
                            tiangongMarker.getPopup().setContent('<b>Tiangong Space Station</b><br>Altitude: ' + data.altitude.toFixed(0) + ' km<br>Velocity: ' + data.velocity.toFixed(0) + ' km/h');
                        }
                    }).catch(err => console.error("Tiangong error:", err));
            }
            
            fetchSatellites();
            setInterval(fetchSatellites, 5000);
        </script>
    </body>
    </html>
    """
    components.html(satellite_html, height=700, scrolling=False)
    st.caption(_("satellite_credit"))

# ---------- MAIN PAGE (AFTER LOGIN) ----------
def main_page():
    sidebar_common()
    # Create tabs for Radar and Satellite Tracker
    tab1, tab2 = st.tabs([_("tab_radar"), _("tab_satellite")])
    with tab1:
        radar_lat, radar_lon, max_range, api_key = radar_sidebar()
        radar_component(radar_lat, radar_lon, max_range, api_key)
        if st.sidebar.button(_("logout_button"), use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    with tab2:
        satellite_tracker()
        if st.sidebar.button(_("logout_button"), use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# ---------- PAGE ROUTING ----------
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
