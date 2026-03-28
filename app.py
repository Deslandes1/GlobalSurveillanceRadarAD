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
    <title>Radar</title>
    <style>
        * { box-sizing: border-box; user-select: none; }
        body {
            background: #0a0f1e;
            font-family: monospace;
            margin: 0;
            padding: 20px;
            color: #ccd6f6;
        }
        .dashboard { max-width: 1000px; margin: 0 auto; }
        .controls-panel {
            background: #11161fcc;
            border-radius: 24px;
            padding: 15px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: flex-end;
            border: 1px solid #2a3a5a;
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
            padding: 6px 12px;
            border-radius: 40px;
            color: white;
            font-family: monospace;
            font-weight: bold;
        }
        button {
            background: #1e2a3a;
            cursor: pointer;
        }
        button.primary {
            background: #0f7b3e;
            border-color: #2aff9e;
        }
        .radar-container {
            background: #03060c;
            border-radius: 32px;
            padding: 20px;
            border: 1px solid #1e3a5f;
            margin-bottom: 20px;
            text-align: center;
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
        .table-wrapper {
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #1f2c44;
        }
        th {
            background: #07101f;
            color: #9effcf;
        }
        tr:hover {
            background: #101a2c;
            cursor: pointer;
        }
        .selected-row {
            background: #1a3a4e !important;
        }
        .report-card {
            background: #030812;
            border-radius: 20px;
            padding: 15px;
            margin-top: 20px;
            border: 1px solid #2a4a6a;
        }
        footer {
            text-align: center;
            margin-top: 25px;
            font-size: 0.7rem;
            opacity: 0.6;
        }
    </style>
</head>
<body>
<div class="dashboard">
    <div style="display: flex; justify-content: space-between; align-items: baseline;">
        <div>
            <h1>🔴 GLOBAL SURVEILLANCE RADAR</h1>
            <div class="sub">Live tracking | Military & Drone Detection</div>
            <div class="owner">🇭🇹 Owner: Gesner Deslandes | GlobalInternet.py</div>
        </div>
        <div class="badge" id="liveStatus">🟢 LIVE DATA</div>
    </div>

    <div class="controls-panel">
        <div class="input-group">
            <label>📍 RADAR LATITUDE</label>
            <input type="text" id="radarLat" value="40.7128">
        </div>
        <div class="input-group">
            <label>📍 RADAR LONGITUDE</label>
            <input type="text" id="radarLon" value="-74.0060">
        </div>
        <div class="input-group">
            <label>📡 MAX RANGE (km)</label>
            <input type="number" id="maxRange" value="500" step="50" min="30" max="2000">
        </div>
        <div class="input-group">
            <label>⏱️ REFRESH (sec)</label>
            <input type="number" id="refreshSec" value="60" step="5" min="10" max="120">
        </div>
        <button class="primary" id="updateRadarBtn">🔄 UPDATE</button>
        <button id="locateMeBtn">📍 MY LOCATION</button>
        <button id="downloadAllBtn">📥 Download CSV</button>
    </div>

    <div class="radar-container">
        <canvas id="radarCanvas" width="600" height="600"></canvas>
        <div class="radar-stats">
            <span>🎯 TARGETS: <strong id="targetCount">0</strong></span>
            <span>📡 LAST UPDATE: <span id="lastUpdate">--</span></span>
            <span>📐 RANGE: <span id="rangeKmDisplay">500</span> km</span>
        </div>
    </div>

    <div class="report-section">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="section-title">🛸 DETECTED OBJECTS (click row)</div>
        </div>
        <div class="table-wrapper">
            <table id="aircraftTable">
                <thead><tr><th>CALLSIGN</th><th>TYPE</th><th>LAT</th><th>LON</th><th>ALT(m)</th><th>SPEED(m/s)</th><th>STATUS</th><th>HEADING</th></tr></thead>
                <tbody id="tableBody"><tr><td colspan="8">Loading...</td></tr></tbody>
            </table>
        </div>
        <div id="detailedReport" class="report-card">
            <h3>📋 DETAILED REPORT</h3>
            <div id="reportContent">Select an aircraft</div>
            <div id="downloadButtonContainer"></div>
        </div>
    </div>
    <footer>Data: OpenSky Network | Military detection by ICAO prefix / callsign | Drone detection by ICAO + low altitude/speed</footer>
</div>

<script>
    // --------------------------------------------------------------
    // Simple helper: distance and bearing
    // --------------------------------------------------------------
    function haversine(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)**2;
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }
    function bearing(lat1, lon1, lat2, lon2) {
        const φ1 = lat1 * Math.PI/180, φ2 = lat2 * Math.PI/180;
        const Δλ = (lon2 - lon1) * Math.PI/180;
        const y = Math.sin(Δλ) * Math.cos(φ2);
        const x = Math.cos(φ1)*Math.sin(φ2) - Math.sin(φ1)*Math.cos(φ2)*Math.cos(Δλ);
        let θ = Math.atan2(y, x);
        return (θ * 180 / Math.PI + 360) % 360;
    }

    // --------------------------------------------------------------
    // DOM elements
    // --------------------------------------------------------------
    const canvas = document.getElementById('radarCanvas');
    const ctx = canvas.getContext('2d');
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
    const liveStatus = document.getElementById('liveStatus');

    let currentAircraft = [];
    let selectedIcao = null;
    let refreshTimer = null;
    let animationId = null;

    // --------------------------------------------------------------
    // Classification (simplified)
    // --------------------------------------------------------------
    const MIL_PREFIXES = ["AE","AD","AF","3C","3E","33","34","38","39","40","43","44","45","46","48","4B","4C","4D","4E","4F","50","51","52","53","54","55","56","57","58","59","5A","5B","5C","5D","5E","5F","60","61","62","63","64","65","66","67","68","69","6A","6B","6C","6D","6E","6F","70","71","72","73","74","75","76","77","78","79","7A","7B","7C","7D","7E","7F","80","81","82","83","84","85","86","87","88","89","8A","8B","8C","8D","8E","8F","90","91","92","93","94","95","96","97","98","99","9A","9B","9C","9D","9E","9F","A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","AA","AB","AC"];
    const DRONE_PREFIXES = ["4CAA","4CAB","4CAC","4CAD","4CAE","4CAF","4CB0","4CB1","4CB2","4CB3","4CB4","4CB5","4CB6","4CB7","4CB8","4CB9","4CBA","4CBB","4CBC","4CBD","4CBE","4CBF"];

    function classify(icao, callsign, velocity, altitude) {
        let military = false, drone = false;
        const icaoU = (icao || "").toUpperCase();
        const callsignU = (callsign || "").toUpperCase();
        if (MIL_PREFIXES.some(p => icaoU.startsWith(p))) military = true;
        if (["AF","NAVY","ARMY","AIR FORCE","MIL","RAAF","RAF","LUFT","ARMEE"].some(kw => callsignU.includes(kw))) military = true;
        if (DRONE_PREFIXES.some(p => icaoU.startsWith(p))) drone = true;
        if (["DRONE","UAV","DRON","QUAD","HEXA","OCTO"].some(kw => callsignU.includes(kw))) drone = true;
        if (!drone && !military && altitude !== null && altitude < 500 && velocity !== null && velocity < 30) drone = true;
        let type = "✈️ Civilian";
        if (military) type = "🔫 Military";
        else if (drone) type = "🚁 Drone";
        return { military, drone, type };
    }

    // --------------------------------------------------------------
    // Fetch data from OpenSky
    // --------------------------------------------------------------
    async function fetchAircraft() {
        const lat = parseFloat(radarLatInput.value);
        const lon = parseFloat(radarLonInput.value);
        const maxRange = parseFloat(maxRangeInput.value);
        if (isNaN(lat) || isNaN(lon) || isNaN(maxRange)) return [];

        try {
            const resp = await fetch("https://opensky-network.org/api/states/all", {
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
                const vel = s[9];
                const hdg = s[10];
                if (latVal === null || lonVal === null) continue;
                const dist = haversine(lat, lon, latVal, lonVal);
                if (dist > maxRange) continue;
                const brng = bearing(lat, lon, latVal, lonVal);
                const cls = classify(icao24, callsign, vel, alt);
                aircraft.push({
                    icao24, callsign: callsign || `FLT${icao24.slice(-4)}`,
                    lat: latVal, lon: lonVal, altitude: alt, velocity: vel, heading: hdg,
                    onGround: s[8], verticalRate: s[11], distance: dist, bearing: brng,
                    isMilitary: cls.military, isDrone: cls.drone, type: cls.type
                });
            }
            // remove duplicates by icao24
            const unique = [];
            const seen = new Set();
            for (let a of aircraft) {
                if (!seen.has(a.icao24)) {
                    seen.add(a.icao24);
                    unique.push(a);
                }
            }
            return unique;
        } catch (err) {
            console.error("Fetch error:", err);
            liveStatus.innerHTML = "⚠️ API ERROR";
            return null;
        }
    }

    // --------------------------------------------------------------
    // Draw radar (always includes a test marker)
    // --------------------------------------------------------------
    function drawRadar(aircraft, radarLat, radarLon, maxRange, timestamp) {
        if (!ctx) return;
        const w = canvas.width, h = canvas.height;
        const centerX = w/2, centerY = h/2;
        const maxRadius = Math.min(w,h)/2 - 25;
        ctx.clearRect(0, 0, w, h);
        // outer circle
        ctx.beginPath();
        ctx.arc(centerX, centerY, maxRadius, 0, 2*Math.PI);
        ctx.fillStyle = '#010a14';
        ctx.fill();
        ctx.strokeStyle = '#2bffaa30';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        // rings
        for (let r = 0.25; r <= 1; r+=0.25) {
            let radius = maxRadius * r;
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2*Math.PI);
            ctx.strokeStyle = '#28e6a830';
            ctx.setLineDash([4,6]);
            ctx.stroke();
            ctx.font = "10px monospace";
            ctx.fillStyle = '#7f9fcf';
            ctx.fillText((maxRange*r).toFixed(0)+"km", centerX+radius+3, centerY-3);
        }
        ctx.setLineDash([]);
        // crosshair
        ctx.beginPath();
        ctx.moveTo(centerX, centerY-12);
        ctx.lineTo(centerX, centerY+12);
        ctx.moveTo(centerX-12, centerY);
        ctx.lineTo(centerX+12, centerY);
        ctx.strokeStyle = '#2aff9e';
        ctx.lineWidth = 1.2;
        ctx.stroke();
        ctx.fillStyle = '#ffffff';
        ctx.fillText("N", centerX-6, centerY-maxRadius+12);

        // Test marker (orange dot at 100 km, 45°)
        const testDist = 100;
        const testBrng = 45;
        if (testDist <= maxRange) {
            const rad = testBrng * Math.PI/180;
            const rPx = (testDist / maxRange) * maxRadius;
            const x = centerX + rPx * Math.sin(rad);
            const y = centerY - rPx * Math.cos(rad);
            ctx.beginPath();
            ctx.arc(x, y, 10, 0, 2*Math.PI);
            ctx.fillStyle = '#ffaa44';
            ctx.fill();
            ctx.strokeStyle = 'white';
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.fillStyle = 'white';
            ctx.font = "bold 10px monospace";
            ctx.fillText("TEST", x+12, y-8);
        }

        // Real aircraft
        let drawn = 0;
        for (let ac of aircraft) {
            const dist = ac.distance;
            if (dist > maxRange) continue;
            const brng = ac.bearing;
            const rad = brng * Math.PI/180;
            const rPx = (dist / maxRange) * maxRadius;
            const x = centerX + rPx * Math.sin(rad);
            const y = centerY - rPx * Math.cos(rad);
            let color = '#2eff9e';
            if (ac.isMilitary) color = '#ff4444';
            else if (ac.isDrone) color = '#ffaa44';
            else if (ac.velocity !== null && ac.velocity <= 0.5) color = '#ff5555';
            ctx.beginPath();
            ctx.arc(x, y, 9, 0, 2*Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.strokeStyle = 'white';
            ctx.lineWidth = 1;
            ctx.stroke();
            ctx.fillStyle = 'white';
            ctx.font = "bold 10px monospace";
            let label = ac.callsign ? ac.callsign.slice(0,6) : "?";
            ctx.fillText(label, x+10, y-6);
            if (selectedIcao === ac.icao24) {
                ctx.beginPath();
                ctx.arc(x, y, 13, 0, 2*Math.PI);
                ctx.strokeStyle = '#ffdd77';
                ctx.lineWidth = 2.5;
                ctx.stroke();
            }
            drawn++;
        }

        // sweep line
        const sweepAngle = (timestamp * 1.2) % 360;
        const radSweep = sweepAngle * Math.PI/180;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        const sweepX = centerX + maxRadius * Math.sin(radSweep);
        const sweepY = centerY - maxRadius * Math.cos(radSweep);
        ctx.lineTo(sweepX, sweepY);
        ctx.strokeStyle = '#9effcf66';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(centerX, centerY, 4, 0, 2*Math.PI);
        ctx.fillStyle = '#ffaa44';
        ctx.fill();

        // debug text
        ctx.font = "12px monospace";
        ctx.fillStyle = "#9effcf";
        ctx.fillText(`DRAWN: ${drawn} / ${aircraft.length}`, 15, 25);
    }

    function animate() {
        const now = Date.now() / 1000;
        const lat = parseFloat(radarLatInput.value);
        const lon = parseFloat(radarLonInput.value);
        const range = parseFloat(maxRangeInput.value);
        drawRadar(currentAircraft, lat, lon, range, now);
        animationId = requestAnimationFrame(animate);
    }

    // --------------------------------------------------------------
    // Table and report
    // --------------------------------------------------------------
    function renderTable(aircraft) {
        if (!aircraft.length) {
            tableBody.innerHTML = '<tr><td colspan="8">No aircraft in range</td></tr>';
            return;
        }
        let html = '';
        for (let ac of aircraft) {
            const moving = (ac.velocity !== null && ac.velocity > 0.5);
            const rowClass = (selectedIcao === ac.icao24) ? 'selected-row' : '';
            html += `<tr class="${rowClass}" data-icao="${ac.icao24}">
                        <td>${escapeHtml(ac.callsign)}</td>
                        <td>${ac.type}</td>
                        <td>${ac.lat.toFixed(4)}</td>
                        <td>${ac.lon.toFixed(4)}</td>
                        <td>${ac.altitude !== null ? ac.altitude.toFixed(0) : 'N/A'}</td>
                        <td>${ac.velocity !== null ? ac.velocity.toFixed(1) : '?'}</td>
                        <td>${moving ? '🟢 MOVING' : '🔴 STATIC'}</td>
                        <td>${ac.heading !== null ? ac.heading.toFixed(0)+'°' : '---'}</td>
                     </tr>`;
        }
        tableBody.innerHTML = html;
        document.querySelectorAll('#aircraftTable tbody tr').forEach(row => {
            row.addEventListener('click', () => {
                const icao = row.getAttribute('data-icao');
                const ac = aircraft.find(a => a.icao24 === icao);
                if (ac) {
                    selectedIcao = icao;
                    generateReport(ac);
                    document.querySelectorAll('#aircraftTable tbody tr').forEach(r => r.classList.remove('selected-row'));
                    row.classList.add('selected-row');
                }
            });
        });
    }

    function generateReport(ac) {
        const moving = (ac.velocity !== null && ac.velocity > 0.5);
        const speedText = ac.velocity !== null ? `${ac.velocity.toFixed(2)} m/s (${(ac.velocity*3.6).toFixed(1)} km/h)` : 'unknown';
        const altText = ac.altitude !== null ? `${ac.altitude.toFixed(1)} m (${(ac.altitude*3.28084).toFixed(0)} ft)` : 'unknown';
        const headingText = ac.heading !== null ? `${ac.heading.toFixed(1)}°` : 'unknown';
        const verticalRate = ac.verticalRate !== null ? `${ac.verticalRate.toFixed(1)} m/s` : 'N/A';
        const onGround = ac.onGround ? 'YES' : 'NO';
        reportDiv.innerHTML = `
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                <div><b>Object:</b> ${escapeHtml(ac.callsign)}</div>
                <div><b>ICAO24:</b> ${ac.icao24}</div>
                <div><b>Lat/Lon:</b> ${ac.lat.toFixed(5)}, ${ac.lon.toFixed(5)}</div>
                <div><b>Altitude:</b> ${altText}</div>
                <div><b>Speed:</b> ${speedText}</div>
                <div><b>Heading:</b> ${headingText}</div>
                <div><b>Vertical rate:</b> ${verticalRate}</div>
                <div><b>Status:</b> ${moving ? 'MOVING' : 'STATIC'}</div>
                <div><b>On ground:</b> ${onGround}</div>
                <div><b>Range:</b> ${ac.distance.toFixed(0)} km</div>
                <div><b>Type:</b> ${ac.type}</div>
            </div>
        `;
        const reportText = `
SURVEILLANCE REPORT
===================
Object: ${ac.callsign}
ICAO24: ${ac.icao24}
Type: ${ac.type}
Latitude: ${ac.lat.toFixed(5)}
Longitude: ${ac.lon.toFixed(5)}
Distance: ${ac.distance.toFixed(0)} km
Altitude: ${altText}
Speed: ${speedText}
Heading: ${headingText}
Vertical Rate: ${verticalRate}
On Ground: ${onGround}
Time: ${new Date().toLocaleString()}
`;
        downloadContainer.innerHTML = `<button id="reportDownloadBtn" style="background:#0f7b3e;">📥 Download Report (TXT)</button>`;
        document.getElementById('reportDownloadBtn').onclick = () => {
            const blob = new Blob([reportText], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${ac.callsign}_report.txt`;
            a.click();
            URL.revokeObjectURL(url);
        };
    }

    function downloadAllCSV() {
        if (!currentAircraft.length) {
            alert("No data");
            return;
        }
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
        const blob = new Blob([csv], {type: 'text/csv'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `radar_${new Date().toISOString().slice(0,19).replace(/:/g, '-')}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }

    function escapeHtml(s) { return s.replace(/[&<>]/g, function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[m];}); }

    // --------------------------------------------------------------
    // Refresh data
    // --------------------------------------------------------------
    async function refreshData() {
        liveStatus.innerHTML = "🟢 FETCHING...";
        const data = await fetchAircraft();
        if (data !== null) {
            currentAircraft = data;
            targetCountSpan.innerText = currentAircraft.length;
            lastUpdateSpan.innerText = new Date().toLocaleTimeString();
            renderTable(currentAircraft);
            liveStatus.innerHTML = "🟢 LIVE DATA";
            if (selectedIcao) {
                const found = currentAircraft.find(a => a.icao24 === selectedIcao);
                if (found) generateReport(found);
                else {
                    reportDiv.innerHTML = "Object no longer in range";
                    selectedIcao = null;
                }
            }
        } else {
            liveStatus.innerHTML = "⚠️ API ERROR";
        }
    }

    function startAutoRefresh() {
        if (refreshTimer) clearInterval(refreshTimer);
        let sec = parseInt(refreshSecInput.value);
        if (isNaN(sec)) sec = 60;
        refreshTimer = setInterval(refreshData, sec * 1000);
    }

    function getMyLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(pos => {
                radarLatInput.value = pos.coords.latitude.toFixed(5);
                radarLonInput.value = pos.coords.longitude.toFixed(5);
                refreshData();
            }, err => alert("Location error: " + err.message));
        } else alert("Geolocation not supported");
    }

    // --------------------------------------------------------------
    // Initialisation
    // --------------------------------------------------------------
    function resizeCanvas() {
        const container = document.querySelector('.radar-container');
        const size = Math.min(container.clientWidth - 40, 600);
        canvas.width = size;
        canvas.height = size;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    refreshData();
    startAutoRefresh();
    animate();

    updateRadarBtn.onclick = () => {
        if (refreshTimer) clearInterval(refreshTimer);
        startAutoRefresh();
        refreshData();
    };
    locateMeBtn.onclick = getMyLocation;
    downloadAllBtn.onclick = downloadAllCSV;
    maxRangeInput.onchange = () => {
        rangeKmDisplay.innerText = maxRangeInput.value;
        refreshData();
    };
    rangeKmDisplay.innerText = maxRangeInput.value;
</script>
</body>
</html>
"""

st.components.v1.html(radar_html, height=1200, scrolling=True)
