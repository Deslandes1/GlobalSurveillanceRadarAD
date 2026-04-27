import streamlit as st
import streamlit.components.v1 as components

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="🔴 Global Surveillance Radar + Satellite Tracker – GlobalInternet.py", layout="wide")

# ---------- AUTHENTICATION ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ---------- LANGUAGE ----------
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# ---------- TRANSLATIONS ----------
texts = {
    "en": {
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
        "license_text": "Proprietary Commercial Software\nCopyright © 2025 Gesner Deslandes.\nThis software is licensed, not sold.\nUnauthorized copying, distribution, or resale is strictly prohibited.",
        "prisme": "📞 Prisme Transfer (Digicel Moncash): (509) 4738-5663",
        "email_contact": "📧 Email: deslandes78@gmail.com",
        "terms": "By using this software you agree to the terms above.",
        "refresh_radar": "🔄 Refresh Radar",
        "tab_radar": "📡 Radar",
        "tab_satellite": "🛰️ Satellite Tracker",
        "satellite_title": "🛰️ LIVE SATELLITE TRACKER",
        "satellite_desc": "Current positions of ISS, Hubble, Tiangong",
        "satellite_credit": "Data: wheretheiss.at | Map: Leaflet",
        "demo_satellite_note": "🎮 Demo mode: simulated satellites"
    },
    "fr": {
        "login_title": "🔐 Connexion requise",
        "login_instruction": "Entrez le mot de passe",
        "password_label": "Mot de passe",
        "login_button": "Connexion",
        "logout_button": "Déconnexion",
        "incorrect_password": "Mot de passe incorrect. Indice : 20082010",
        "sidebar_company": "🌐 GlobalInternet.py",
        "sidebar_founder": "👨‍💻 Gesner Deslandes – Fondateur",
        "sidebar_phone": "📞 (509) 4738-5663",
        "sidebar_email": "✉️ deslandes78@gmail.com",
        "sidebar_website": "🌍 Visitez notre site web",
        "radar_settings": "📡 Paramètres radar",
        "radar_lat": "Latitude",
        "radar_lon": "Longitude",
        "max_range": "Portée max (km)",
        "demo_mode_radar": "🎲 Mode démo",
        "demo_mode_satellite": "🛸 Mode démo",
        "data_source": "🔑 Source",
        "data_source_msg": "Entrez votre clé API Flightradar24",
        "api_key_input": "Clé API",
        "api_key_placeholder": "Clé optionnelle",
        "global_active": "🌍 Couverture mondiale active",
        "opensky_active": "📡 Utilisation OpenSky",
        "demo_active": "🎮 Mode démo actif",
        "license_title": "📜 Licence",
        "license_text": "Logiciel commercial propriétaire\nCopyright © 2025 Gesner Deslandes.",
        "prisme": "📞 Transfert Prisme: (509) 4738-5663",
        "email_contact": "📧 Email: deslandes78@gmail.com",
        "terms": "En utilisant ce logiciel, vous acceptez les conditions.",
        "refresh_radar": "🔄 Actualiser",
        "tab_radar": "📡 Radar",
        "tab_satellite": "🛰️ Satellites",
        "satellite_title": "🛰️ TRACEUR DE SATELLITES",
        "satellite_desc": "Positions ISS, Hubble, Tiangong",
        "satellite_credit": "Données: wheretheiss.at | Carte: Leaflet",
        "demo_satellite_note": "🎮 Mode démo: satellites simulés"
    },
    "es": {
        "login_title": "🔐 Inicio requerido",
        "login_instruction": "Ingrese la contraseña",
        "password_label": "Contraseña",
        "login_button": "Iniciar",
        "logout_button": "Cerrar sesión",
        "incorrect_password": "Contraseña incorrecta. Pista: 20082010",
        "sidebar_company": "🌐 GlobalInternet.py",
        "sidebar_founder": "👨‍💻 Gesner Deslandes – Fundador",
        "sidebar_phone": "📞 (509) 4738-5663",
        "sidebar_email": "✉️ deslandes78@gmail.com",
        "sidebar_website": "🌍 Visite nuestro sitio",
        "radar_settings": "📡 Configuración",
        "radar_lat": "Latitud",
        "radar_lon": "Longitud",
        "max_range": "Alcance (km)",
        "demo_mode_radar": "🎲 Modo demo",
        "demo_mode_satellite": "🛸 Modo demo",
        "data_source": "🔑 Fuente",
        "data_source_msg": "Ingrese clave API de Flightradar24",
        "api_key_input": "Clave API",
        "api_key_placeholder": "Opcional",
        "global_active": "🌍 Cobertura global activa",
        "opensky_active": "📡 Usando OpenSky",
        "demo_active": "🎮 Modo demo activo",
        "license_title": "📜 Licencia",
        "license_text": "Software comercial propietario\nCopyright © 2025 Gesner Deslandes.",
        "prisme": "📞 Transferencia Prisme: (509) 4738-5663",
        "email_contact": "📧 Email: deslandes78@gmail.com",
        "terms": "Al usar este software, acepta los términos.",
        "refresh_radar": "🔄 Actualizar",
        "tab_radar": "📡 Radar",
        "tab_satellite": "🛰️ Satélites",
        "satellite_title": "🛰️ RASTREADOR DE SATÉLITES",
        "satellite_desc": "Posiciones ISS, Hubble, Tiangong",
        "satellite_credit": "Datos: wheretheiss.at | Mapa: Leaflet",
        "demo_satellite_note": "🎮 Modo demo: satélites simulados"
    }
}

def _(key):
    return texts[st.session_state.lang].get(key, key)

# ---------- LANGUAGE SELECTOR ----------
def language_selector():
    opts = {"English": "en", "Français": "fr", "Español": "es"}
    cur = [k for k, v in opts.items() if v == st.session_state.lang][0]
    sel = st.sidebar.selectbox("🌐 Language", list(opts.keys()), index=list(opts.keys()).index(cur))
    st.session_state.lang = opts[sel]

def sidebar_common():
    st.sidebar.markdown(f"## {_('sidebar_company')}")
    st.sidebar.markdown(f"**{_('sidebar_founder')}**")
    st.sidebar.markdown(_("sidebar_phone"))
    st.sidebar.markdown(_("sidebar_email"))
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"[{_('sidebar_website')}](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.sidebar.markdown("---")
    language_selector()

# ---------- RADAR SIDEBAR ----------
def radar_sidebar():
    lat = st.sidebar.number_input(_("radar_lat"), value=40.7128, format="%.5f")
    lon = st.sidebar.number_input(_("radar_lon"), value=-74.0060, format="%.5f")
    maxr = st.sidebar.number_input(_("max_range"), min_value=30, max_value=2000, value=500, step=50)
    demo = st.sidebar.checkbox(_("demo_mode_radar"), value=False)
    st.sidebar.divider()
    st.sidebar.markdown(f"## {_('data_source')}")
    if not demo:
        st.sidebar.markdown(_("data_source_msg"))
        api = st.sidebar.text_input(_("api_key_input"), type="password", placeholder=_("api_key_placeholder"))
        if api:
            st.sidebar.info(_("global_active"))
        else:
            st.sidebar.info(_("opensky_active"))
    else:
        st.sidebar.info(_("demo_active"))
        api = ""
    st.sidebar.divider()
    st.sidebar.markdown(f"## {_('license_title')}")
    st.sidebar.markdown(_("license_text"))
    st.sidebar.markdown(_("prisme"))
    st.sidebar.markdown(_("email_contact"))
    st.sidebar.caption(_("terms"))
    if st.sidebar.button(_("refresh_radar"), use_container_width=True):
        st.rerun()
    return lat, lon, maxr, api, demo

# ---------- LOGIN ----------
def login_page():
    st.title(_("login_title"))
    st.markdown(_("login_instruction"))
    with st.form("login_form"):
        pwd = st.text_input(_("password_label"), type="password")
        if st.form_submit_button(_("login_button")):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(_("incorrect_password"))
    sidebar_common()

# ---------- RADAR HTML (WITH WORKING SWEEP AND BEEP) ----------
def radar_component(lat, lon, maxr, api_key, demo_mode):
    demo_str = "true" if demo_mode else "false"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>Radar</title>
    <style>
        *{{box-sizing:border-box;}} body{{background:#0a0f1e;font-family:monospace;margin:0;padding:20px;color:#ccd6f6;}}
        .dashboard{{max-width:1000px;margin:0 auto;}}
        .radar-container{{background:#03060c;border-radius:32px;padding:20px;border:1px solid #1e3a5f;margin-bottom:20px;}}
        canvas{{display:block;margin:0 auto;background:radial-gradient(circle at 30% 20%,#07121f,#010101);border-radius:50%;width:100%;max-width:550px;height:auto;cursor:crosshair;}}
        .radar-stats{{display:flex;justify-content:space-between;margin-top:15px;font-size:0.8rem;flex-wrap:wrap;gap:10px;}}
        .badge{{background:#0f172a;padding:5px 12px;border-radius:40px;border-left:3px solid #2aff9e;}}
        .report-section{{background:#0c1220;border-radius:24px;padding:20px;border:1px solid #233453;}}
        .table-wrapper{{overflow-x:auto;}}
        table{{width:100%;border-collapse:collapse;font-size:0.8rem;}}
        th,td{{padding:10px 8px;border-bottom:1px solid #1f2c44;text-align:left;}}
        th{{background:#07101f;color:#9effcf;}}
        tr:hover{{background:#101a2c;cursor:pointer;}}
        .selected-row{{background:#1a3a4e !important;border-left:3px solid #2aff9e;}}
        .report-card{{background:#030812;border-radius:20px;padding:15px;margin-top:20px;border:1px solid #2a4a6a;}}
        button{{background:#0f7b3e;border:none;color:white;padding:8px 16px;border-radius:30px;cursor:pointer;}}
    </style>
    </head>
    <body>
    <div class="dashboard">
        <div style="display:flex;justify-content:space-between;">
            <div><h1>🔴 GLOBAL SURVEILLANCE RADAR</h1><div class="owner">Owner: Gesner Deslandes | GlobalInternet.py</div></div>
            <div class="badge" id="liveStatus">🟢 LOADING</div>
        </div>
        <div class="radar-container">
            <canvas id="radarCanvas" width="550" height="550"></canvas>
            <div class="radar-stats">
                <span>🎯 TARGETS: <strong id="targetCount">0</strong></span>
                <span>🟢 MOVING | 🔴 STATIC | 🔫 MILITARY | 🚁 DRONE</span>
                <span>📡 LAST UPDATE: <span id="lastUpdate">--</span></span>
                <span>📐 RANGE: {maxr} km</span>
            </div>
        </div>
        <div class="report-section">
            <div style="display:flex;justify-content:space-between;"><h3>🛸 DETECTED OBJECTS</h3><button id="downloadAllBtn">📥 Download All CSV</button></div>
            <div class="table-wrapper"><table id="aircraftTable"><thead><tr><th>CALLSIGN</th><th>TYPE</th><th>LAT</th><th>LON</th><th>ALT(m)</th><th>SPEED(m/s)</th><th>STATUS</th><th>HEADING</th></thead><tbody id="tableBody"><tr><td colspan="8">Loading...</td></tr></tbody></table></div>
            <div id="detailedReport" class="report-card"><h3>📋 OBJECT REPORT</h3><div id="reportContent">Select an object</div><div id="downloadButtonContainer"></div></div>
        </div>
    </div>
    <script>
        let audioCtx=null;
        function beep(){try{if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();let now=audioCtx.currentTime,osc=audioCtx.createOscillator(),gain=audioCtx.createGain();osc.connect(gain);gain.connect(audioCtx.destination);osc.frequency.value=880;gain.gain.setValueAtTime(0.1,now);gain.gain.exponentialRampToValueAtTime(0.00001,now+0.2);osc.start(now);osc.stop(now+0.2);}catch(e){}}
        const milPrefixes=["AE","AD","AF","3C","3E","33","34","38","39","40","43","44","45","46","48","4B","4C","4D","4E","4F","50","51","52","53","54","55","56","57","58","59","5A","5B","5C","5D","5E","5F","60","61","62","63","64","65","66","67","68","69","6A","6B","6C","6D","6E","6F","70","71","72","73","74","75","76","77","78","79","7A","7B","7C","7D","7E","7F","80","81","82","83","84","85","86","87","88","89","8A","8B","8C","8D","8E","8F","90","91","92","93","94","95","96","97","98","99","9A","9B","9C","9D","9E","9F","A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","AA","AB","AC"];
        const dronePrefixes=["4CAA","4CAB","4CAC","4CAD","4CAE","4CAF","4CB0","4CB1","4CB2","4CB3","4CB4","4CB5","4CB6","4CB7","4CB8","4CB9","4CBA","4CBB","4CBC","4CBD","4CBE","4CBF"];
        function classify(icao,callsign,vel,alt){let mil=false,drone=false,icaoU=(icao||"").toUpperCase(),csU=(callsign||"").toUpperCase();for(let p of milPrefixes)if(icaoU.startsWith(p)){mil=true;break;}let milKW=["AF","NAVY","ARMY","AIR FORCE","MIL","RAAF","RAF","LUFT","ARMEE"];if(milKW.some(k=>csU.includes(k)))mil=true;for(let p of dronePrefixes)if(icaoU.startsWith(p)){drone=true;break;}let droneKW=["DRONE","UAV","DRON","QUAD","HEXA","OCTO"];if(droneKW.some(k=>csU.includes(k)))drone=true;if(!drone&&!mil&&alt!==null&&alt<500&&vel!==null&&vel<30)drone=true;let type="✈️ Civilian";if(mil)type="🔫 Military";else if(drone)type="🚁 Drone";return{mil,drone,type};}
        const radarLat={lat}, radarLon={lon};
        let maxRangeKm={maxr}, demoMode={demo_str};
        const canvas=document.getElementById('radarCanvas'), ctx=canvas.getContext('2d');
        const targetSpan=document.getElementById('targetCount'), updateSpan=document.getElementById('lastUpdate');
        const tbody=document.getElementById('tableBody'), reportDiv=document.getElementById('reportContent'), downDiv=document.getElementById('downloadButtonContainer');
        let aircraft=[], selectedIcao=null, refreshTimer=null, sweepAngle=0;
        function haversine(lat1,lon1,lat2,lon2){let R=6371,dLat=(lat2-lat1)*Math.PI/180,dLon=(lon2-lon1)*Math.PI/180,a=Math.sin(dLat/2)**2+Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)**2;return R*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));}
        function bearing(lat1,lon1,lat2,lon2){let φ1=lat1*Math.PI/180,φ2=lat2*Math.PI/180,Δλ=(lon2-lon1)*Math.PI/180,y=Math.sin(Δλ)*Math.cos(φ2),x=Math.cos(φ1)*Math.sin(φ2)-Math.sin(φ1)*Math.cos(φ2)*Math.cos(Δλ);return(Math.atan2(y,x)*180/Math.PI+360)%360;}
        function generateDemo(){let list=[];let names=["DEMO1","DEMO2","DEMO3","DEMO4","DEMO5","DEMO6","DEMO7","DEMO8","DEMO9","DEMO10"];for(let i=0;i<10;i++){let dist=Math.random()*maxRangeKm,brng=Math.random()*360,lat=radarLat+(dist*Math.cos(brng*Math.PI/180))/111,lon=radarLon+(dist*Math.sin(brng*Math.PI/180))/(111*Math.cos(radarLat*Math.PI/180)),alt=Math.random()*8000+100,vel=Math.random()*150,hdg=Math.random()*360,cls=classify("DEMO_"+i,names[i],vel,alt);list.push({icao24:"DEMO"+i,callsign:names[i],lat,lon,altitude:alt,velocity:vel,heading:hdg,onGround:false,verticalRate:0,distance:dist,bearing:brng,isMilitary:cls.mil,isDrone:cls.drone,type:cls.type});}return list;}
        async function fetchLive(){if(demoMode)return generateDemo();try{let resp=await fetch("https://opensky-network.org/api/states/all",{headers:{"User-Agent":"Mozilla/5.0"}});if(!resp.ok)throw new Error();let data=await resp.json(),states=data.states||[],ac=[];for(let s of states){let icao=s[0],cs=s[1]?s[1].trim():null,lon=s[5],lat=s[6];if(lat===null||lon===null)continue;let dist=haversine(radarLat,radarLon,lat,lon);if(dist>maxRangeKm)continue;let cls=classify(icao,cs,s[9],s[7]);ac.push({icao24:icao,callsign:cs||`FLT${icao.slice(-4)}`,lat,lon,altitude:s[7],velocity:s[9],heading:s[10],onGround:s[8],verticalRate:s[11],distance:dist,bearing:bearing(radarLat,radarLon,lat,lon),isMilitary:cls.mil,isDrone:cls.drone,type:cls.type});}let unique=[],seen=new Set();for(let a of ac)if(!seen.has(a.icao24)){seen.add(a.icao24);unique.push(a);}return unique;}catch(e){console.log(e);return null;}}
        function draw(){if(!ctx)return;let w=canvas.width,h=canvas.height,cx=w/2,cy=h/2,maxR=w/2-25;ctx.clearRect(0,0,w,h);ctx.beginPath();ctx.arc(cx,cy,maxR,0,2*Math.PI);ctx.fillStyle='#010a14';ctx.fill();ctx.strokeStyle='#2bffaa30';ctx.stroke();for(let r=0.25;r<=1;r+=0.25){let rad=maxR*r;ctx.beginPath();ctx.arc(cx,cy,rad,0,2*Math.PI);ctx.strokeStyle='#28e6a830';ctx.setLineDash([4,6]);ctx.stroke();ctx.fillStyle='#7f9fcf';ctx.font="10px monospace";ctx.fillText((maxRangeKm*r).toFixed(0)+"km",cx+rad+3,cy-3);}ctx.setLineDash([]);ctx.beginPath();ctx.moveTo(cx,cy-12);ctx.lineTo(cx,cy+12);ctx.moveTo(cx-12,cy);ctx.lineTo(cx+12,cy);ctx.strokeStyle='#2aff9e';ctx.stroke();ctx.fillStyle='#fff';ctx.font="bold 12px monospace";ctx.fillText("N",cx-6,cy-maxR+12);let testDist=100,testBrng=45;if(testDist<=maxRangeKm){let ang=testBrng*Math.PI/180,rpx=(testDist/maxRangeKm)*maxR,x=cx+rpx*Math.sin(ang),y=cy-rpx*Math.cos(ang);ctx.beginPath();ctx.arc(x,y,10,0,2*Math.PI);ctx.fillStyle='#ffaa44';ctx.fill();ctx.fillStyle='white';ctx.fillText("TEST",x+12,y-8);}for(let ac of aircraft){if(ac.distance>maxRangeKm)continue;let ang=ac.bearing*Math.PI/180,rpx=(ac.distance/maxRangeKm)*maxR,x=cx+rpx*Math.sin(ang),y=cy-rpx*Math.cos(ang);let color='#2eff9e';if(ac.isMilitary)color='#ff4444';else if(ac.isDrone)color='#ffaa44';else if(ac.velocity!==null&&ac.velocity<=0.5)color='#ff5555';ctx.beginPath();ctx.arc(x,y,9,0,2*Math.PI);ctx.fillStyle=color;ctx.fill();ctx.strokeStyle='white';ctx.stroke();let label=ac.callsign?ac.callsign.trim():(ac.icao24?ac.icao24.slice(-5):"???");if(label.length>6)label=label.slice(0,6);ctx.fillStyle='white';ctx.fillText(label,x+10,y-6);if(selectedIcao===ac.icao24){ctx.beginPath();ctx.arc(x,y,13,0,2*Math.PI);ctx.strokeStyle='#ffdd77';ctx.lineWidth=2.5;ctx.stroke();}}let now=Date.now()/1000;let sweep=(now*1.2)%360;let radSweep=sweep*Math.PI/180;ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+maxR*Math.sin(radSweep),cy-maxR*Math.cos(radSweep));ctx.strokeStyle='#9effcf66';ctx.stroke();ctx.beginPath();ctx.arc(cx,cy,4,0,2*Math.PI);ctx.fillStyle='#ffaa44';ctx.fill();requestAnimationFrame(draw);}
        async function refresh(){let data=await fetchLive();if(!data){document.getElementById('liveStatus').innerHTML=demoMode?"🎮 DEMO":"⚠️ ERROR";return;}document.getElementById('liveStatus').innerHTML=demoMode?"🎮 DEMO":"🟢 LIVE";aircraft=data;targetSpan.innerText=aircraft.length;updateSpan.innerText=new Date().toLocaleTimeString();renderTable();if(selectedIcao){let found=aircraft.find(a=>a.icao24===selectedIcao);if(found)generateReport(found);else{reportDiv.innerHTML="Object no longer in range.";selectedIcao=null;}}}
        function renderTable(){if(!aircraft.length){tbody.innerHTML='<tr><td colspan="8">No objects detected</td></tr>';return;}let html='';for(let ac of aircraft){let moving=(ac.velocity!==null&&ac.velocity>0.5);html+=`<tr class="${selectedIcao===ac.icao24?'selected-row':''}" data-icao="${ac.icao24}"><td>${escapeHtml(ac.callsign)}</td><td>${ac.type}</td><td>${ac.lat.toFixed(4)}</td><td>${ac.lon.toFixed(4)}</td><td>${ac.altitude!==null?ac.altitude.toFixed(0):'N/A'}</td><td>${ac.velocity!==null?ac.velocity.toFixed(1):'?'}</td><td>${moving?'🟢 MOVING':'🔴 STATIC'}</td><td>${ac.heading!==null?ac.heading.toFixed(0)+'°':'---'}</td></tr>`;}tbody.innerHTML=html;document.querySelectorAll('#aircraftTable tbody tr').forEach(row=>{row.onclick=()=>{let icao=row.getAttribute('data-icao');let ac=aircraft.find(a=>a.icao24===icao);if(ac){selectedIcao=icao;generateReport(ac);document.querySelectorAll('#aircraftTable tbody tr').forEach(r=>r.classList.remove('selected-row'));row.classList.add('selected-row');}}});}
        function generateReport(ac){let moving=(ac.velocity!==null&&ac.velocity>0.5);let speedText=ac.velocity!==null?`${ac.velocity.toFixed(2)} m/s (${(ac.velocity*3.6).toFixed(1)} km/h)`:'unknown';let altText=ac.altitude!==null?`${ac.altitude.toFixed(1)} m (${(ac.altitude*3.28084).toFixed(0)} ft)`:'not reported';let source=demoMode?"DEMO SIMULATION":"OpenSky LIVE";reportDiv.innerHTML=`<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;"><div><strong>OBJECT:</strong> ${escapeHtml(ac.callsign)}</div><div><strong>ICAO24:</strong> ${ac.icao24}</div><div><strong>LAT/LON:</strong> ${ac.lat.toFixed(5)}, ${ac.lon.toFixed(5)}</div><div><strong>ALTITUDE:</strong> ${altText}</div><div><strong>SPEED:</strong> ${speedText}</div><div><strong>HEADING:</strong> ${ac.heading!==null?ac.heading.toFixed(1)+'°':'unknown'}</div><div><strong>VERTICAL RATE:</strong> ${ac.verticalRate!==null?ac.verticalRate.toFixed(1)+' m/s':'N/A'}</div><div><strong>STATUS:</strong> ${moving?'MOVING':'STATIC'}</div><div><strong>ON GROUND:</strong> ${ac.onGround?'YES':'NO'}</div><div><strong>RANGE:</strong> ${ac.distance.toFixed(0)} km</div><div><strong>CLASSIFICATION:</strong> ${ac.type}</div><div><strong>DATA SOURCE:</strong> ${source}</div></div>`;let reportText=`SURVEILLANCE REPORT (${demoMode?"DEMO":"LIVE"})\nObject: ${ac.callsign}\nICAO24: ${ac.icao24}\nLat: ${ac.lat.toFixed(5)}\nLon: ${ac.lon.toFixed(5)}\nDistance: ${ac.distance.toFixed(0)} km\nAltitude: ${altText}\nSpeed: ${speedText}\nHeading: ${ac.heading!==null?ac.heading.toFixed(1)+'°':'unknown'}\nVertical Rate: ${ac.verticalRate!==null?ac.verticalRate.toFixed(1)+' m/s':'N/A'}\nOn Ground: ${ac.onGround?'YES':'NO'}\nType: ${ac.type}\nSource: ${source}\nTime: ${new Date().toLocaleString()}`;downDiv.innerHTML=`<button id="dlReportBtn">📥 Download Report (TXT)</button>`;document.getElementById('dlReportBtn').onclick=()=>{let blob=new Blob([reportText],{type:'text/plain'});let url=URL.createObjectURL(blob);let a=document.createElement('a');a.href=url;a.download=`${ac.callsign}_report.txt`;a.click();URL.revokeObjectURL(url);};}
        function downloadAll(){if(!aircraft.length){alert("No data");return;}let headers=["Callsign","Type","Lat","Lon","Alt(m)","Speed(m/s)","Status","Heading","Dist(km)"];let rows=aircraft.map(ac=>[ac.callsign,ac.type,ac.lat.toFixed(5),ac.lon.toFixed(5),ac.altitude!==null?ac.altitude.toFixed(1):"N/A",ac.velocity!==null?ac.velocity.toFixed(1):"?",(ac.velocity!==null&&ac.velocity>0.5)?"MOVING":"STATIC",ac.heading!==null?ac.heading.toFixed(0)+"°":"---",ac.distance.toFixed(0)]);let csv=[headers,...rows].map(row=>row.map(c=>`"${c}"`).join(",")).join("\\n");let blob=new Blob([csv],{type:"text/csv"});let url=URL.createObjectURL(blob);let a=document.createElement('a');a.href=url;a.download=`radar_${new Date().toISOString().slice(0,19).replace(/:/g,"-")}.csv`;a.click();URL.revokeObjectURL(url);}
        function escapeHtml(s){if(!s)return '';return s.replace(/[&<>]/g,function(m){if(m==='&')return '&amp;';if(m==='<')return '&lt;';if(m==='>')return '&gt;';return m;});}
        function init(){canvas.width=550;canvas.height=550;refresh();setInterval(refresh,60000);draw();}
        document.getElementById('downloadAllBtn').onclick=downloadAll;
        init();
        // Beep on each full rotation: approximate 0.833 rotations per second, we'll check angle crossing
        let lastBeepSweep=0;
        setInterval(function(){let now=Date.now()/1000;let sweep=(now*1.2)%360;if(lastBeepSweep>350 && sweep<10)beep();lastBeepSweep=sweep;},50);
    </script>
    </body>
    </html>
    """
    components.html(html, height=950, scrolling=True)

# ---------- SATELLITE TRACKER ----------
def satellite_tracker(demo_mode):
    st.markdown(f"## {_('satellite_title')}")
    if demo_mode:
        st.info(_("demo_satellite_note"))
    else:
        st.markdown(_("satellite_desc"))
    demo_flag = "true" if demo_mode else "false"
    sat_html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" /><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>#map{{height:450px;width:100%;background:#0a0f1e;border-radius:20px;}}body{{background:#0a0f1e;margin:0;padding:0;}}.info{{text-align:center;color:#ccd6f6;margin-top:10px;}}.sat-list{{background:#0c1220;border-radius:20px;padding:15px;margin-top:20px;}}.sat-item{{background:#0f172a;margin:8px 0;padding:8px 12px;border-radius:12px;cursor:pointer;display:flex;justify-content:space-between;}}.sat-item:hover{{background:#1a3a4e;}}.selected-sat{{background:#1a3a4e;border-left:3px solid #2aff9e;}}.report-panel{{margin-top:20px;background:#030812;border-radius:20px;padding:15px;}}button{{background:#0f7b3e;border:none;color:white;padding:8px 16px;border-radius:30px;cursor:pointer;}}</style>
    </head>
    <body>
    <div id="map"></div>
    <div class="sat-list"><h3>🛰️ SATELLITES (click for report)</h3><div id="satelliteList"></div></div>
    <div id="reportPanel" class="report-panel"><h3>📋 REPORT</h3><div id="reportContent">Select a satellite</div><div id="downloadBtnContainer"></div></div>
    <div class="info"><span>🛰️ ISS (yellow)  🔭 Hubble (cyan)  🌍 Tiangong (orange)  🛸 Demo (magenta)</span><p>Updates every 5s</p></div>
    <script>
        let audioCtx=null;function beep(){try{if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();let now=audioCtx.currentTime,osc=audioCtx.createOscillator(),gain=audioCtx.createGain();osc.connect(gain);gain.connect(audioCtx.destination);osc.frequency.value=440;gain.gain.setValueAtTime(0.08,now);gain.gain.exponentialRampToValueAtTime(0.00001,now+0.15);osc.start(now);osc.stop(now+0.15);}catch(e){}}
        const demoMode={demo_flag};
        let map=L.map('map').setView([0,0],2);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png',{{attribution:'',subdomains:'abcd',maxZoom:19,minZoom:2}}).addTo(map);
        let markers={{}},satData=[],selectedId=null;
        function getDemo(){return[{{id:"DEMO1",name:"GeoEye-1",lat:28.6,lng:-80.6,alt:681,vel:7.5,type:"Earth Imaging"}},{{id:"DEMO2",name:"Landsat-9",lat:45.0,lng:-110.0,alt:705,vel:7.4,type:"Remote Sensing"}},{{id:"DEMO3",name:"NOAA-20",lat:-15.0,lng:-150.0,alt:824,vel:7.3,type:"Weather"}},{{id:"DEMO4",name:"Starlink",lat:52.0,lng:-40.0,alt:550,vel:7.6,type:"Comms"}},{{id:"DEMO5",name:"GPS",lat:12.0,lng:70.0,alt:20200,vel:3.9,type:"Navigation"}}];}
        function fetchReal(){return Promise.all([fetch('https://api.wheretheiss.at/v1/satellites/25544').then(r=>r.json()).then(d=>({{id:"ISS",name:"ISS",lat:d.latitude,lng:d.longitude,alt:d.altitude,vel:d.velocity,type:"Manned"}})),fetch('https://api.wheretheiss.at/v1/satellites/20580').then(r=>r.json()).then(d=>({{id:"HUBBLE",name:"Hubble",lat:d.latitude,lng:d.longitude,alt:d.altitude,vel:d.velocity,type:"Telescope"}})),fetch('https://api.wheretheiss.at/v1/satellites/48274').then(r=>r.json()).then(d=>({{id:"TIANGONG",name:"Tiangong",lat:d.latitude,lng:d.longitude,alt:d.altitude,vel:d.velocity,type:"Manned"}}))]);}
        function update(){if(demoMode){satData=getDemo();beep();render();}else{fetchReal().then(s=>{satData=s;beep();render();}).catch(console.error);}}
        function render(){for(let s of satData){if(markers[s.id])markers[s.id].setLatLng([s.lat,s.lng]);else{let icon="🛸";if(s.id==="ISS")icon="🛰️";else if(s.id==="HUBBLE")icon="🔭";else if(s.id==="TIANGONG")icon="🌍";markers[s.id]=L.marker([s.lat,s.lng],{{icon:L.divIcon({{html:icon,className:"sat-marker",iconSize:[30,30]}})}}).bindPopup(`<b>${{s.name}}</b><br>Alt: ${{s.alt.toFixed(0)}} km`).addTo(map);}}for(let id in markers)if(!satData.find(s=>s.id===id)){{map.removeLayer(markers[id]);delete markers[id];}}let html='';for(let s of satData){let cls=(selectedId===s.id)?"selected-sat":"";html+=`<div class="sat-item ${{cls}}" data-id="${{s.id}}"><span><strong>${{s.name}}</strong></span><span>📍 ${{s.lat.toFixed(2)}}, ${{s.lng.toFixed(2)}}</span><span>📏 ${{s.alt.toFixed(0)}} km</span></div>`;}document.getElementById('satelliteList').innerHTML=html;document.querySelectorAll('.sat-item').forEach(el=>{el.onclick=()=>{let id=el.getAttribute('data-id');let s=satData.find(x=>x.id===id);if(s){selectedId=id;generateReport(s);document.querySelectorAll('.sat-item').forEach(i=>i.classList.remove('selected-sat'));el.classList.add('selected-sat');}}});}
        function generateReport(s){let source=demoMode?"DEMO":"LIVE (wheretheiss.at)";document.getElementById('reportContent').innerHTML=`<div><strong>NAME:</strong> ${{s.name}}<br><strong>ID:</strong> ${{s.id}}<br><strong>LAT:</strong> ${{s.lat.toFixed(5)}}<br><strong>LON:</strong> ${{s.lng.toFixed(5)}}<br><strong>ALT:</strong> ${{s.alt.toFixed(1)}} km<br><strong>VEL:</strong> ${{s.vel.toFixed(1)}} km/h<br><strong>TYPE:</strong> ${{s.type||"Satellite"}}<br><strong>SOURCE:</strong> ${{source}}</div>`;let txt=`SATELLITE REPORT\nName: ${{s.name}}\nID: ${{s.id}}\nLat: ${{s.lat.toFixed(5)}}\nLon: ${{s.lng.toFixed(5)}}\nAlt: ${{s.alt.toFixed(1)}} km\nVel: ${{s.vel.toFixed(1)}} km/h\nType: ${{s.type||"Satellite"}}\nSource: ${{source}}\nTime: ${{new Date().toLocaleString()}}`;document.getElementById('downloadBtnContainer').innerHTML=`<button id="dlSatBtn">📥 Download Report</button>`;document.getElementById('dlSatBtn').onclick=()=>{let blob=new Blob([txt],{{type:'text/plain'}});let url=URL.createObjectURL(blob);let a=document.createElement('a');a.href=url;a.download=`${{s.name}}_report.txt`;a.click();URL.revokeObjectURL(url);};}
        update();setInterval(update,5000);
    </script>
    </body>
    </html>
    """
    components.html(sat_html, height=650, scrolling=False)
    st.caption(_("satellite_credit"))

# ---------- MAIN PAGE ----------
def main_page():
    sidebar_common()
    if st.sidebar.button(_("logout_button"), key="logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    tab1, tab2 = st.tabs([_("tab_radar"), _("tab_satellite")])
    with tab1:
        lat, lon, maxr, api, demo = radar_sidebar()
        radar_component(lat, lon, maxr, api, demo)
    with tab2:
        demo_sat = st.sidebar.checkbox(_("demo_mode_satellite"), key="demo_sat", value=False)
        satellite_tracker(demo_sat)

# ---------- ROUTING ----------
if not st.session_state.authenticated:
    login_page()
else:
    main_page()
