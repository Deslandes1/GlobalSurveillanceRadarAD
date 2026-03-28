import streamlit as st

st.set_page_config(page_title="🔴 Global Surveillance Radar – GlobalInternet.py", layout="centered")

with st.sidebar:
    st.markdown("## 🔴 Global Surveillance Radar")
    st.markdown("**Real‑time global aircraft tracking with military & drone detection**")
    st.markdown("---")
    st.markdown("### 📜 License")
    st.markdown("""
    **Proprietary Commercial Software**  
    Copyright © 2025 Gesner Deslandes. All rights reserved.

    This software is **licensed**, not sold.  
    Unauthorized copying, distribution, or resale is prohibited.
    """)
    st.markdown("### 💸 Purchase")
    st.markdown("""
    - **Price:** $500 USD (one‑time license)
    - Payment via **Prisme Transfer** (Digicel Moncash) to:
    📞 **(509) 4738-5663**  
    *Reference: “Radar Purchase”*
    - Email confirmation to **deslandes78@gmail.com** with your name.
    - You’ll receive the software and setup instructions within 24 hours.
    """)
    st.markdown("---")
    st.caption("© 2025 Gesner Deslandes – GlobalInternet.py")

st.title("🔴 Global Surveillance Radar")
st.markdown("**Real‑time global aircraft tracking | Military & Drone Detection**")
st.markdown("**GlobalInternet.py – Director & Python Programmer: Gesner Deslandes**")

radar_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Global Surveillance Radar – ADS-B</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
        }

        body {
            background: #0a0f1e;
            font-family: 'Segoe UI', 'Roboto', monospace;
            margin: 0;
            padding: 20px;
            color: #ccd6f6;
        }

        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            font-size: 1.7rem;
            margin: 0 0 5px 0;
            letter-spacing: 2px;
            background: linear-gradient(135deg, #2aff9e, #00c3ff);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            display: inline-block;
        }

        .sub {
            color: #8e9aaf;
            font-size: 0.8rem;
            margin-bottom: 20px;
            border-left: 3px solid #2aff9e;
            padding-left: 12px;
        }

        .owner {
            font-size: 0.8rem;
            margin-top: 5px;
            color: #9effcf;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .controls-panel {
            background: #11161fcc;
            backdrop-filter: blur(8px);
            border-radius: 24px;
            padding: 15px 20px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: flex-end;
            border: 1px solid #2a3a5a;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .input-group label {
            font-size: 0.7rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #8aa2d4;
        }

        input, button {
            background: #0b1018;
            border: 1px solid #2c3f5f;
            padding: 8px 14px;
            border-radius: 40px;
            color: white;
            font-family: monospace;
            font-weight: bold;
            transition: 0.2s;
        }

        input:focus {
            outline: none;
            border-color: #2aff9e;
            box-shadow: 0 0 8px #2aff9e66;
        }

        button {
            background: #1e2a3a;
            cursor: pointer;
        }

        button.primary {
            background: #0f7b3e;
            border-color: #2aff9e;
            box-shadow: 0 0 5px #2aff9e66;
        }

        button.primary:hover {
            background: #19a854;
            transform: scale(0.97);
        }

        .radar-container {
            background: #03060c;
            border-radius: 32px;
            padding: 20px;
            box-shadow: 0 20px 35px rgba(0,0,0,0.5);
            border: 1px solid #1e3a5f;
            margin-bottom: 20px;
        }

        canvas {
            display: block;
            margin: 0 auto;
            background: radial-gradient(circle at 30% 20%, #07121f, #010101);
            border-radius: 50%;
            box-shadow: 0 0 0 2px #0e2a3a, 0 0 0 5px #03121f;
            width: 100%;
            height: auto;
            cursor: crosshair;
        }

        .radar-stats {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 0.8rem;
            font-family: monospace;
            flex-wrap: wrap;
            gap: 10px;
        }

        .badge {
            background: #0f172a;
            padding: 5px 12px;
            border-radius: 40px;
            border-left: 3px solid #2aff9e;
        }

        .report-section {
            background: #0c1220;
            border-radius: 24px;
            padding: 20px;
            border: 1px solid #233453;
        }

        .section-title {
            font-size: 1.2rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid #2a3f60;
            padding-bottom: 8px;
        }

        .table-wrapper {
            overflow-x: auto;
            border-radius: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
        }

        th, td {
            padding: 10px 8px;
            text-align: left;
            border-bottom: 1px solid #1f2c44;
        }

        th {
            background: #07101f;
            color: #9effcf;
            font-weight: 600;
        }

        tr:hover {
            background: #101a2c;
            cursor: pointer;
        }

        .selected-row {
            background: #1a3a4e !important;
            border-left: 3px solid #2aff9e;
        }

        .report-card {
            background: #030812;
            border-radius: 20px;
            padding: 15px;
            margin-top: 20px;
            border: 1px solid #2a4a6a;
            font-family: monospace;
        }

        .report-card h3 {
            margin: 0 0 8px 0;
            color: #6effb0;
        }

        footer {
            text-align: center;
            margin-top: 25px;
            font-size: 0.7rem;
            opacity: 0.6;
        }

        @media (max-width: 700px) {
            body { padding: 12px; }
            th, td { font-size: 0.7rem; padding: 6px 4px; }
            .input-group label { font-size: 0.6rem; }
            button, input { padding: 6px 10px; }
            .owner { font-size: 0.7rem; }
        }
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

    <div class="controls-panel">
        <div class="input-group">
            <label>📍 RADAR LATITUDE</label>
            <input type="text" id="radarLat" value="40.7128" placeholder="40.7128">
        </div>
        <div class="input-group">
            <label>📍 RADAR LONGITUDE</label>
            <input type="text" id="radarLon" value="-74.0060" placeholder="-74.0060">
        </div>
        <div class="input-group">
            <label>📡 MAX RANGE (km)</label>
            <input type="number" id="maxRange" value="500" step="50" min="30" max="2000">
        </div>
        <div class="input-group">
            <label>⏱️ REFRESH (sec)</label>
            <input type="number" id="refreshSec" value="60" step="5" min="10" max="120">
        </div>
        <button class="primary" id="updateRadarBtn">🔄 UPDATE RADAR</button>
        <button id="locateMeBtn" style="background:#2a4359;">📍 MY LOCATION</button>
    </div>

    <div class="radar-container">
        <canvas id="radarCanvas" width="700" height="700" style="width:100%; max-width:700px; height:auto; aspect-ratio:1/1"></canvas>
        <div class="radar-stats">
            <span>🎯 TARGETS: <strong id="targetCount">0</strong></span>
            <span>🟢 MOVING | 🔴 STATIC | 🔫 MILITARY | 🚁 DRONE</span>
            <span>📡 LAST UPDATE: <span id="lastUpdate">--</span></span>
            <span>📐 RANGE: <span id="rangeKmDisplay">500</span> km</span>
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
    // --------------------------------------------------------------
    // CONSTANTS & CLASSIFICATION
    // --------------------------------------------------------------
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

    function classifyAircraft(icao24, callsign, velocity, altitude) {
        let isMilitary = false;
        let isDrone = false;
        const icaoUpper = (icao24 || "").toUpperCase();
        const callsignUpper = (callsign || "").toUpperCase();

        for (let prefix of MILITARY_ICAO_PREFIXES) {
            if (icaoUpper.startsWith(prefix)) { isMilitary = true; break; }
        }
        const milKeywords = ["AF","NAVY","ARMY","AIR FORCE","MIL","RAAF","RAF","LUFT","ARMEE"];
        if (milKeywords.some(kw => callsignUpper.includes(kw))) isMilitary = true;

        for (let prefix of DRONE_ICAO_PREFIXES) {
            if (icaoUpper.startsWith(prefix)) { isDrone = true; break; }
        }
        const droneKeywords = ["DRONE","UAV","DRON","QUAD","HEXA","OCTO"];
        if (droneKeywords.some(kw => callsignUpper.includes(kw))) isDrone = true;

        if (!isDrone && !isMilitary && altitude !== null && altitude < 500 && velocity !== null && velocity < 30) {
            isDrone = true;
        }

        let typeStr = "✈️ Civilian";
        if (isMilitary) typeStr = "🔫 Military";
        else if (isDrone) typeStr = "🚁 Drone";

        return { isMilitary, isDrone, type: typeStr };
    }

    // --------------------------------------------------------------
    // GLOBALS
    // --------------------------------------------------------------
    let radarCtx = null;
    let canvasSize = 700;
    let currentAircraft = [];
    let selectedIcao = null;
    let refreshTimer = null;
    let radarCenter = { lat: 40.7128, lon: -74.0060 };
    let maxRangeKm = 500;
    let refreshIntervalSec = 60;
    let animationFrameId = null;

    const radarCanvas = document.getElementById('radarCanvas');
    const targetCountSpan = document.getElementById('targetCount');
    const lastUpdateSpan = document.getElementById('lastUpdate');
    const tableBody = document.getElementById('tableBody');
    const reportDiv = document.getElementById('reportContent');
    const downloadContainer = document.getElementById('downloadButtonContainer');
    const rangeKmDisplay = document.getElementById('rangeKmDisplay');
    const radarLatInput = document.getElementById('radarLat');
    const radarLonInput = document.getElementById('radarLon');
    const maxRangeInput = document.getElementById('maxRange');
    const refreshSecInput = document.getElementById('refreshSec');
    const updateRadarBtn = document.getElementById('updateRadarBtn');
    const locateMeBtn = document.getElementById('locateMeBtn');
    const downloadAllBtn = document.getElementById('downloadAllBtn');

    // --------------------------------------------------------------
    // GEOMETRY HELPERS
    // --------------------------------------------------------------
    function haversineDistance(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2)**2 + Math.cos(lat1 * Math.PI/180) * Math.cos(lat2 * Math.PI/180) * Math.sin(dLon/2)**2;
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }

    function bearing(lat1, lon1, lat2, lon2) {
        const φ1 = lat1 * Math.PI/180;
        const φ2 = lat2 * Math.PI/180;
        const Δλ = (lon2 - lon1) * Math.PI/180;
        const y = Math.sin(Δλ) * Math.cos(φ2);
        const x = Math.cos(φ1)*Math.sin(φ2) - Math.sin(φ1)*Math.cos(φ2)*Math.cos(Δλ);
        let θ = Math.atan2(y, x);
        return (θ * 180/Math.PI + 360) % 360;
    }

    // --------------------------------------------------------------
    // DRAW RADAR (improved marker visibility)
    // --------------------------------------------------------------
    function drawRadar(aircraftList, radarLat, radarLon, maxRange, nowSeconds) {
        if (!radarCtx) return;
        const w = canvasSize, h = canvasSize;
        const centerX = w/2, centerY = h/2;
        const maxRadiusPx = w/2 - 25;

        radarCtx.clearRect(0, 0, w, h);
        radarCtx.beginPath();
        radarCtx.arc(centerX, centerY, maxRadiusPx, 0, 2*Math.PI);
        radarCtx.fillStyle = '#010a14';
        radarCtx.fill();
        radarCtx.strokeStyle = '#2bffaa30';
        radarCtx.lineWidth = 1.5;
        radarCtx.stroke();

        // range rings
        for (let r = 0.25; r <= 1; r+=0.25) {
            let radius = maxRadiusPx * r;
            radarCtx.beginPath();
            radarCtx.arc(centerX, centerY, radius, 0, 2*Math.PI);
            radarCtx.strokeStyle = '#28e6a830';
            radarCtx.setLineDash([4, 6]);
            radarCtx.stroke();
            let rangeVal = (maxRange * r).toFixed(0);
            radarCtx.font = "10px monospace";
            radarCtx.fillStyle = '#7f9fcf';
            radarCtx.fillText(rangeVal+"km", centerX + radius + 3, centerY - 3);
        }
        radarCtx.setLineDash([]);

        // crosshair & north
        radarCtx.beginPath();
        radarCtx.moveTo(centerX, centerY-12);
        radarCtx.lineTo(centerX, centerY+12);
        radarCtx.moveTo(centerX-12, centerY);
        radarCtx.lineTo(centerX+12, centerY);
        radarCtx.strokeStyle = '#2aff9e';
        radarCtx.lineWidth = 1.2;
        radarCtx.stroke();
        radarCtx.fillStyle = '#ffffff';
        radarCtx.font = "bold 12px monospace";
        radarCtx.fillText("N", centerX-6, centerY-maxRadiusPx+12);

        // draw targets
        let drawn = 0;
        for (let ac of aircraftList) {
            const dist = ac.distance;
            if (dist > maxRange) continue;
            const brng = ac.bearing;
            const angleRad = brng * Math.PI / 180;
            const radiusPx = (dist / maxRange) * maxRadiusPx;
            const x = centerX + radiusPx * Math.sin(angleRad);
            const y = centerY - radiusPx * Math.cos(angleRad);
            // colour based on classification & movement
            let color = '#2eff9e'; // civilian moving default
            if (ac.isMilitary) color = '#ff4444';
            else if (ac.isDrone) color = '#ffaa44';
            else if (ac.velocity !== null && ac.velocity <= 0.5) color = '#ff5555';
            radarCtx.beginPath();
            radarCtx.arc(x, y, 8, 0, 2*Math.PI);  // larger marker
            radarCtx.fillStyle = color;
            radarCtx.shadowBlur = 0;  // disable shadow for clarity
            radarCtx.fill();
            radarCtx.strokeStyle = 'white';
            radarCtx.lineWidth = 1;
            radarCtx.stroke();
            radarCtx.fillStyle = 'white';
            radarCtx.font = "bold 10px monospace";
            let label = ac.callsign ? ac.callsign.trim() : (ac.icao24 ? ac.icao24.slice(-5) : "???");
            if(label.length > 6) label = label.slice(0,6);
            radarCtx.fillText(label, x+10, y-6);
            if (selectedIcao === ac.icao24) {
                radarCtx.beginPath();
                radarCtx.arc(x, y, 14, 0, 2*Math.PI);
                radarCtx.strokeStyle = '#ffdd77';
                radarCtx.lineWidth = 2.5;
                radarCtx.stroke();
            }
            drawn++;
        }
        // console.log(`Drawn ${drawn} aircraft`); // uncomment to debug

        // sweep line
        const sweepAngle = (nowSeconds * 1.2) % 360;
        const radSweep = sweepAngle * Math.PI/180;
        radarCtx.beginPath();
        radarCtx.moveTo(centerX, centerY);
        const sweepX = centerX + maxRadiusPx * Math.sin(radSweep);
        const sweepY = centerY - maxRadiusPx * Math.cos(radSweep);
        radarCtx.lineTo(sweepX, sweepY);
        radarCtx.strokeStyle = '#9effcf66';
        radarCtx.lineWidth = 2;
        radarCtx.stroke();
        radarCtx.beginPath();
        radarCtx.arc(centerX, centerY, 4, 0, 2*Math.PI);
        radarCtx.fillStyle = '#ffaa44';
        radarCtx.fill();
    }

    function animate() {
        if (radarCtx) {
            const now = Date.now() / 1000;
            const lat = parseFloat(radarLatInput.value);
            const lon = parseFloat(radarLonInput.value);
            const range = parseFloat(maxRangeInput.value);
            drawRadar(currentAircraft, lat, lon, range, now);
        }
        animationFrameId = requestAnimationFrame(animate);
    }

    // --------------------------------------------------------------
    // FETCH DATA FROM OPENSKY
    // --------------------------------------------------------------
    async function fetchLiveAircraft() {
        const lat = parseFloat(radarLatInput.value);
        const lon = parseFloat(radarLonInput.value);
        const maxRange = parseFloat(maxRangeInput.value);
        if (isNaN(lat) || isNaN(lon) || isNaN(maxRange)) return null;

        try {
            const url = "https://opensky-network.org/api/states/all";
            const resp = await fetch(url, {
                headers: { "User-Agent": "Mozilla/5.0 (compatible; RadarApp/1.0)" }
            });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            const states = data.states || [];

            const aircraft = [];
            for (let s of states) {
                const icao24 = s[0];
                const callsign = s[1] ? s[1].trim() : null;
                const lonVal = s[5];
                const latVal = s[6];
                const alt = s[7];
                const velocity = s[9];
                const heading = s[10];
                if (latVal === null || lonVal === null) continue;
                const dist = haversineDistance(lat, lon, latVal, lonVal);
                if (dist > maxRange) continue;
                const brng = bearing(lat, lon, latVal, lonVal);
                const classification = classifyAircraft(icao24, callsign, velocity, alt);
                aircraft.push({
                    icao24: icao24,
                    callsign: callsign || `FLT${icao24.slice(-4)}`,
                    lat: latVal,
                    lon: lonVal,
                    altitude: alt,
                    velocity: velocity,
                    heading: heading,
                    onGround: s[8],
                    verticalRate: s[11],
                    distance: dist,
                    bearing: brng,
                    isMilitary: classification.isMilitary,
                    isDrone: classification.isDrone,
                    type: classification.type
                });
            }
            // remove duplicates
            const unique = [];
            const seen = new Set();
            for (let ac of aircraft) {
                if (!seen.has(ac.icao24)) {
                    seen.add(ac.icao24);
                    unique.push(ac);
                }
            }
            return unique;
        } catch (err) {
            console.error(err);
            document.getElementById('liveStatus').innerHTML = "⚠️ API ERROR";
            return null;
        }
    }

    // --------------------------------------------------------------
    // UPDATE UI
    // --------------------------------------------------------------
    async function refreshRadarData() {
        const aircraftData = await fetchLiveAircraft();
        if (!aircraftData) {
            document.getElementById('liveStatus').innerHTML = "⚠️ API ERROR (OpenSky)";
            return;
        }
        document.getElementById('liveStatus').innerHTML = "🟢 LIVE DATA (OpenSky)";
        currentAircraft = aircraftData;
        targetCountSpan.innerText = currentAircraft.length;
        lastUpdateSpan.innerText = new Date().toLocaleTimeString();
        renderTable(currentAircraft);
        if (selectedIcao) {
            const found = currentAircraft.find(ac => ac.icao24 === selectedIcao);
            if (found) generateDetailedReport(found);
            else {
                reportDiv.innerHTML = "⚠️ Selected object no longer in radar coverage.";
                selectedIcao = null;
            }
        }
    }

    function renderTable(aircraftList) {
        if (!aircraftList.length) {
            tableBody.innerHTML = '车脉<td colspan="8">✈️ No flying objects detected within radar range.脉舶';
            return;
        }
        let html = '';
        for (let ac of aircraftList) {
            const isMoving = (ac.velocity !== null && ac.velocity > 0.5);
            const statusLabel = isMoving ? '🟢 MOVING' : '🔴 STATIC';
            const speedVal = (ac.velocity !== null) ? ac.velocity.toFixed(1) : '?';
            const headingVal = (ac.heading !== null) ? ac.heading.toFixed(0)+'°' : '---';
            const altVal = (ac.altitude !== null) ? ac.altitude.toFixed(0) : 'N/A';
            const rowClass = (selectedIcao === ac.icao24) ? 'selected-row' : '';
            html += `<tr class="${rowClass}" data-icao="${ac.icao24}">
                            <td>${escapeHtml(ac.callsign)}<\/td>
                            <td>${ac.type}<\/td>
                            <td>${ac.lat.toFixed(4)}<\/td>
                            <td>${ac.lon.toFixed(4)}<\/td>
                            <td>${altVal}<\/td>
                            <td>${speedVal}<\/td>
                            <td>${statusLabel}<\/td>
                            <td>${headingVal}<\/td>
                        <\/tr>`;
        }
        tableBody.innerHTML = html;
        document.querySelectorAll('#aircraftTable tbody tr').forEach(row => {
            row.addEventListener('click', () => {
                const icao = row.getAttribute('data-icao');
                const aircraft = currentAircraft.find(a => a.icao24 === icao);
                if (aircraft) {
                    selectedIcao = icao;
                    generateDetailedReport(aircraft);
                    document.querySelectorAll('#aircraftTable tbody tr').forEach(r => r.classList.remove('selected-row'));
                    row.classList.add('selected-row');
                }
            });
        });
    }

    function generateDetailedReport(ac) {
        const isMoving = (ac.velocity !== null && ac.velocity > 0.5);
        let speedText = ac.velocity !== null ? `${ac.velocity.toFixed(2)} m/s (${(ac.velocity*3.6).toFixed(1)} km/h)` : 'unknown';
        let altText = ac.altitude !== null ? `${ac.altitude.toFixed(1)} meters (${(ac.altitude*3.28084).toFixed(0)} ft)` : 'not reported';
        let headingText = ac.heading !== null ? `${ac.heading.toFixed(1)}° (true)` : 'unknown';
        let verticalRate = ac.verticalRate !== null ? `${ac.verticalRate.toFixed(1)} m/s` : 'N/A';
        let onGround = ac.onGround ? 'YES (on ground)' : 'AIRBORNE';
        let callsignNice = ac.callsign ? ac.callsign : 'no callsign';
        let icao = ac.icao24;
        let lastSeen = new Date().toLocaleTimeString();

        reportDiv.innerHTML = `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                <div><strong>✈️ OBJECT:</strong> ${escapeHtml(callsignNice)}</div>
                <div><strong>🆔 ICAO24:</strong> ${icao}</div>
                <div><strong>📍 LAT/LON:</strong> ${ac.lat.toFixed(5)} , ${ac.lon.toFixed(5)}</div>
                <div><strong>📏 ALTITUDE:</strong> ${altText}</div>
                <div><strong>💨 SPEED:</strong> ${speedText}</div>
                <div><strong>🧭 HEADING:</strong> ${headingText}</div>
                <div><strong>📈 VERTICAL RATE:</strong> ${verticalRate}</div>
                <div><strong>⚡ STATUS:</strong> ${isMoving ? '🟢 MOVING' : '🔴 STATIC (low velocity)'}</div>
                <div><strong>🛬 ON GROUND:</strong> ${onGround}</div>
                <div><strong>📡 RADAR RANGE:</strong> ${maxRangeKm} km from center</div>
                <div><strong>🛡️ CLASSIFICATION:</strong> ${ac.type}</div>
            </div>
            <hr style="border-color:#2a4f6e; margin-top:12px;">
            <div style="font-size:0.75rem;">🔍 Real ADS-B data via OpenSky Network. Military detection based on ICAO hex ranges & callsigns. Drone detection includes manufacturer ICAO prefixes and heuristic low‑altitude/speed behaviour.</div>
        `;

        // Download button
        const reportText = `
SURVEILLANCE REPORT
===================
Object: ${callsignNice}
ICAO24: ${icao}
Type: ${ac.type}
Latitude: ${ac.lat.toFixed(5)}
Longitude: ${ac.lon.toFixed(5)}
Distance from radar: ${ac.distance.toFixed(0)} km
Altitude: ${altText}
Speed: ${speedText}
Heading: ${headingText}
Vertical Rate: ${verticalRate}
On Ground: ${onGround}
Time of report: ${new Date().toLocaleString()}
Data source: OpenSky Network
`;
        downloadContainer.innerHTML = `
            <button id="downloadReportBtn" style="background:#0f7b3e; border-color:#2aff9e; box-shadow:0 0 5px #2aff9e66;">📥 Download Report (TXT)</button>
        `;
        document.getElementById('downloadReportBtn').addEventListener('click', () => {
            const blob = new Blob([reportText], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${callsignNice}_report.txt`;
            a.click();
            URL.revokeObjectURL(url);
        });
    }

    // Download all aircraft as CSV
    function downloadAllCSV() {
        if (!currentAircraft.length) {
            alert("No data to download.");
            return;
        }
        const headers = ["Callsign", "Type", "Latitude", "Longitude", "Altitude (m)", "Speed (m/s)", "Status", "Heading", "Distance (km)"];
        const rows = currentAircraft.map(ac => [
            ac.callsign,
            ac.type,
            ac.lat.toFixed(5),
            ac.lon.toFixed(5),
            ac.altitude !== null ? ac.altitude.toFixed(1) : "N/A",
            ac.velocity !== null ? ac.velocity.toFixed(1) : "?",
            (ac.velocity !== null && ac.velocity > 0.5) ? "MOVING" : "STATIC",
            ac.heading !== null ? ac.heading.toFixed(0)+"°" : "---",
            ac.distance.toFixed(0)
        ]);
        const csvContent = [headers, ...rows].map(row => row.map(cell => `"${cell}"`).join(",")).join("\n");
        const blob = new Blob([csvContent], {type: "text/csv"});
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `radar_data_${new Date().toISOString().slice(0,19).replace(/:/g, "-")}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }

    function escapeHtml(str) { if(!str) return ''; return str.replace(/[&<>]/g, function(m){if(m==='&') return '&amp;'; if(m==='<') return '&lt;'; if(m==='>') return '&gt;'; return m;}); }

    // --------------------------------------------------------------
    // INITIALISATION & CONTROLS
    // --------------------------------------------------------------
    function initRadarCanvas() {
        const container = document.querySelector('.radar-container');
        const size = Math.min(container.clientWidth - 40, 700);
        radarCanvas.width = size;
        radarCanvas.height = size;
        canvasSize = size;
        radarCtx = radarCanvas.getContext('2d');
        radarCtx.shadowBlur = 0;
        refreshRadarData();
    }

    function startAutoRefresh() {
        if (refreshTimer) clearInterval(refreshTimer);
        let sec = parseInt(refreshSecInput.value);
        if (isNaN(sec)) sec = 60;
        refreshIntervalSec = Math.min(120, Math.max(10, sec));
        refreshTimer = setInterval(() => refreshRadarData(), refreshIntervalSec * 1000);
    }

    function getMyLocation() {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(pos => {
                radarLatInput.value = pos.coords.latitude.toFixed(5);
                radarLonInput.value = pos.coords.longitude.toFixed(5);
                refreshRadarData();
            }, err => alert("Location error: " + err.message));
        } else alert("Geolocation not supported");
    }

    updateRadarBtn.addEventListener('click', () => {
        if (refreshTimer) clearInterval(refreshTimer);
        startAutoRefresh();
        refreshRadarData();
    });
    locateMeBtn.addEventListener('click', getMyLocation);
    refreshSecInput.addEventListener('change', startAutoRefresh);
    maxRangeInput.addEventListener('change', () => {
        maxRangeKm = parseFloat(maxRangeInput.value);
        rangeKmDisplay.innerText = maxRangeKm;
        refreshRadarData();
    });
    downloadAllBtn.addEventListener('click', downloadAllCSV);
    window.addEventListener('resize', () => {
        setTimeout(() => {
            const container = document.querySelector('.radar-container');
            let newSize = Math.min(container.clientWidth - 40, 700);
            radarCanvas.width = newSize;
            radarCanvas.height = newSize;
            canvasSize = newSize;
        }, 100);
    });

    // initial values
    maxRangeKm = parseFloat(maxRangeInput.value);
    rangeKmDisplay.innerText = maxRangeKm;

    initRadarCanvas();
    startAutoRefresh();
    animate();
</script>
</body>
</html>
"""

st.components.v1.html(radar_html, height=1500, scrolling=True)
