"""
Main FastAPI Server & WebSockets Telemetry Dispatcher for Aegis-SOC
"""

import os
import asyncio
import time
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel

from backend.config import PORT_API, PORT_SSH_HONEYPOT, PORT_WEB_HONEYPOT, DECOY_PORTS
from backend.database import (
    init_db, get_recent_logs, get_attackers_list, get_mitre_stats,
    get_honeytokens, get_quarantine_list, clear_all_data, get_db
)
from backend.engine.ai_analyst import generate_ai_threat_summary
from backend.engine.active_defense import active_defense_engine
from backend.honeytokens import create_honeytoken
from backend.sensors.ssh_honeypot import SSHHoneypotServer
from backend.sensors.web_honeypot import WebHoneypotServer, set_web_broadcast_callback
from backend.sensors.raw_decoy import RawDecoyServer
from backend.decoy_state import get_all_decoys, toggle_decoy, is_decoy_enabled, add_custom_decoy
from backend.database import log_attack_event
from backend.engine.mitre_mapper import map_payload_to_mitre
from backend.engine.threat_score import calculate_event_risk
import threading

app = FastAPI(title="Aegis-SOC Threat Deception Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.loop = None

    def set_loop(self, loop):
        self.loop = loop

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_json(self, data: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(data)
            except Exception:
                self.disconnect(connection)

    def sync_broadcast(self, data: dict):
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.broadcast_json(data), self.loop)

manager = ConnectionManager()

# Data Models
class QuarantineRequest(BaseModel):
    ip: str
    action: str  # "BLOCK" or "UNBLOCK"
    reason: str = "Admin Intervention"

class HoneytokenRequest(BaseModel):
    name: str
    type: str

class DecoyToggleRequest(BaseModel):
    id: str
    enabled: bool = None

class DecoyAddRequest(BaseModel):
    name: str
    port: int
    service_type: str = "Custom Decoy"
    description: str = ""

# API Routes
@app.get("/")
async def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"status": "Aegis-SOC API Running", "dashboard": "Frontend index.html not found"})

@app.get("/real-admin", response_class=HTMLResponse)
async def real_admin_login():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Aegis Production Vault - Secure Login</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body { background: #090d16; color: #f3f4f6; font-family: 'Plus Jakarta Sans', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: #101726; border: 1px solid rgba(255,255,255,0.08); padding: 36px; border-radius: 12px; width: 380px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            .brand { text-align: center; margin-bottom: 24px; }
            .brand h2 { color: #10b981; margin: 0; font-size: 20px; font-weight: 700; }
            .brand p { font-size: 12px; color: #9ca3af; margin-top: 4px; }
            .form-group { margin-bottom: 18px; }
            label { display: block; margin-bottom: 6px; font-size: 12px; color: #9ca3af; font-weight: 500; }
            input { width: 100%; padding: 10px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1); background: #090d16; color: #fff; box-sizing: border-box; font-size: 13px; }
            input:focus { outline: none; border-color: #10b981; }
            button { width: 100%; padding: 11px; border-radius: 6px; border: none; background: #10b981; color: #060911; font-weight: 700; cursor: pointer; font-size: 14px; transition: all 0.2s; }
            button:hover { background: #059669; }
            .creds-hint { background: rgba(16, 185, 129, 0.05); border: 1px dashed rgba(16, 185, 129, 0.3); padding: 12px; border-radius: 6px; font-size: 11px; color: #10b981; margin-top: 20px; text-align: center; line-height: 1.5; }
            .attribution { margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 12px; font-size: 10px; color: #6b7280; text-align: center; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="brand">
                <h2>🔒 Aegis Production Vault</h2>
                <p>Authenticated Corporate Portal (Port 8000)</p>
            </div>
            <form method="POST" action="/real-admin">
                <div class="form-group">
                    <label>Admin ID / Email</label>
                    <input type="text" name="username" value="admin@aegis-corp.com" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="Enter Password" required>
                </div>
                <button type="submit">Log In to Production</button>
            </form>
            <div class="creds-hint">
                <strong>Demo Access Credentials:</strong><br>
                User: <code>admin@aegis-corp.com</code><br>
                Pass: <code>AdminPass2026!</code>
            </div>
            <div class="attribution">
                The Oxford Evening Polytechnic • Cyber Security (Sem VI)<br>
                Guide: Mr. Subhash J R | Team: Abhijeet, Kanaka, Raghunandan
            </div>
        </div>
    </body>
    </html>
    """)

@app.post("/real-admin", response_class=HTMLResponse)
async def real_admin_authenticate(username: str = Form(...), password: str = Form(...)):
    if username == "admin@aegis-corp.com" and password == "AdminPass2026!":
        return HTMLResponse("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Aegis Secure Production Portal</title>
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>
                body { background: #090d16; color: #f3f4f6; font-family: 'Plus Jakarta Sans', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                .card { background: #101726; border: 1px solid #10b981; padding: 40px; border-radius: 12px; width: 440px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
                h2 { color: #10b981; margin-top: 0; font-size: 20px; font-weight: 700; }
                .status-box { background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); color: #10b981; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 14px; margin-top: 20px; line-height: 1.5; }
                .info { color: #9ca3af; font-size: 13px; margin-top: 15px; }
                a { color: #10b981; text-decoration: none; display: inline-block; margin-top: 20px; font-size: 12px; font-weight: 600; }
                .attribution { margin-top: 24px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 12px; font-size: 11px; color: #6b7280; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🔒 Genuine Production Vault</h2>
                <p class="info">Authenticated Employee Session (Port 8000)</p>
                <div class="status-box">
                    ✔ AUTHORIZED ACCESS GRANTED<br>
                    <span style="font-size: 11px; font-weight: normal; color: #9ca3af;">User: admin@aegis-corp.com | Encrypted TLS 1.3</span>
                </div>
                <p class="info">Welcome, Authorized Administrator. All core production modules online.</p>
                <a href="/real-admin">← Log Out</a>

                <div class="attribution">
                    <strong>The Oxford Evening Polytechnic</strong> (Sem VI)<br>
                    Project Guide: <strong>Mr. Subhash J R</strong><br>
                    Team: Abhijeet Kumar, Kanaka C, Raghunandan T V
                </div>
            </div>
        </body>
        </html>
        """)
    else:
        return HTMLResponse("""
        <script>
            alert('Invalid Credentials! Access Denied.');
            window.location.href = '/real-admin';
        </script>
        """, status_code=401)

@app.get("/api/status")
async def get_system_status():
    logs = get_recent_logs(100)
    attackers = get_attackers_list()
    quarantined = get_quarantine_list()
    tokens = get_honeytokens()
    all_decoys = get_all_decoys()
    active_count = sum(1 for d in all_decoys if d.get("enabled"))

    return {
        "platform": "Aegis-SOC Threat Deception",
        "status": "ONLINE",
        "active_honeypots": [
            {"name": d["name"], "port": d["port"], "status": "ACTIVE" if d.get("enabled") else "DISABLED"}
            for d in all_decoys
        ],
        "metrics": {
            "total_attacks_logged": len(logs),
            "unique_attackers": len(attackers),
            "quarantined_ips": len(quarantined),
            "active_honeytokens": len(tokens),
            "active_decoys": active_count,
            "total_decoys": len(all_decoys)
        }
    }

@app.get("/api/logs")
async def get_logs(limit: int = 50):
    return get_recent_logs(limit)

@app.get("/api/attackers")
async def get_attackers():
    return get_attackers_list()

@app.get("/api/mitre")
async def get_mitre():
    return get_mitre_stats()

@app.get("/api/honeytokens")
async def get_tokens():
    return get_honeytokens()

@app.post("/api/honeytokens/create")
async def add_honeytoken(req: HoneytokenRequest):
    return create_honeytoken(req.name, req.type)

@app.get("/api/quarantine")
async def get_quarantine():
    return get_quarantine_list()

@app.post("/api/quarantine/toggle")
async def toggle_quarantine(req: QuarantineRequest):
    if req.action.upper() == "BLOCK":
        active_defense_engine.manual_quarantine(req.ip, req.reason)
        msg = f"IP {req.ip} added to quarantine."
    else:
        active_defense_engine.manual_unblock(req.ip)
        msg = f"IP {req.ip} unblocked."
    return {"status": "SUCCESS", "message": msg}

@app.get("/api/ai-report/{ip}")
async def get_ai_report(ip: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attack_logs WHERE attacker_ip = ? ORDER BY id DESC', (ip,))
    logs = [dict(r) for r in cursor.fetchall()]
    cursor.execute('SELECT * FROM attackers WHERE ip = ?', (ip,))
    attacker_row = cursor.fetchone()
    attacker_profile = dict(attacker_row) if attacker_row else {}
    conn.close()

    report = generate_ai_threat_summary(ip, logs, attacker_profile)
    return report

@app.post("/api/simulator/launch")
async def launch_simulator():
    from backend.attack_simulator import run_full_attack_scenario
    threading.Thread(target=run_full_attack_scenario, daemon=True).start()
    return {"status": "SUCCESS", "message": "Attack simulation launched!"}

@app.post("/api/reset")
async def reset_data():
    clear_all_data()
    return {"status": "SUCCESS", "message": "System telemetry reset cleanly."}

@app.get("/api/decoys")
async def list_decoys():
    return get_all_decoys()

@app.post("/api/decoys/toggle")
async def toggle_decoy_status(req: DecoyToggleRequest):
    return toggle_decoy(req.id, req.enabled)

@app.post("/api/decoys/add")
async def create_custom_decoy(req: DecoyAddRequest):
    return add_custom_decoy(req.name, req.port, req.service_type, req.description)

# Decoy API Trap Endpoints
@app.get("/api/v1/auth/keys")
async def decoy_api_auth_keys(request: Request):
    if not is_decoy_enabled("api_auth_keys"):
        return JSONResponse({"status": "error", "message": "Endpoint disabled"}, status_code=404)
    
    client_ip = request.client.host if request.client else "127.0.0.1"
    payload = "Attempted API Key Harvesting / Exfiltration"
    mitre = map_payload_to_mitre("DECOY_API", "api_key_harvesting", payload)
    score, severity = calculate_event_risk(mitre['risk_score'])
    
    log_id = log_attack_event(
        attacker_ip=client_ip,
        port=8000,
        decoy_service="DECOY_API_KEYS",
        attack_type="Unauthenticated API Key Probe",
        payload=payload,
        mitre_id=mitre['mitre_id'],
        mitre_name=mitre['mitre_name'],
        mitre_tactic=mitre['mitre_tactic'],
        risk_score=score,
        severity=severity
    )
    
    from backend.database import get_geo_info
    geo = get_geo_info(client_ip)
    quarantined, _ = active_defense_engine.process_event(client_ip, score, mitre['mitre_name'])
    
    manager.sync_broadcast({
        "id": log_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "attacker_ip": client_ip,
        "port": 8000,
        "decoy_service": "DECOY_API_KEYS",
        "attack_type": "Unauthenticated API Key Probe",
        "payload": payload,
        "mitre_id": mitre['mitre_id'],
        "mitre_name": mitre['mitre_name'],
        "mitre_tactic": mitre['mitre_tactic'],
        "risk_score": score,
        "severity": severity,
        "quarantined": quarantined,
        "country": geo['country'],
        "city": geo['city'],
        "lat": geo['lat'],
        "lng": geo['lng'],
        "flag": geo['flag']
    })
    return JSONResponse({"error": "Unauthorized", "message": "Honeytoken trigger recorded"}, status_code=401)

@app.get("/api/v1/admin/db_export")
async def decoy_api_db_export(request: Request):
    if not is_decoy_enabled("api_db_export"):
        return JSONResponse({"status": "error", "message": "Endpoint disabled"}, status_code=404)
    
    client_ip = request.client.host if request.client else "127.0.0.1"
    payload = "Attempted Unauthorized Database Dump / Exfiltration"
    mitre = map_payload_to_mitre("DECOY_API", "database_dump", payload)
    score, severity = calculate_event_risk(mitre['risk_score'])
    
    log_id = log_attack_event(
        attacker_ip=client_ip,
        port=8000,
        decoy_service="DECOY_API_DB_EXPORT",
        attack_type="Rogue DB Export Attempt",
        payload=payload,
        mitre_id=mitre['mitre_id'],
        mitre_name=mitre['mitre_name'],
        mitre_tactic=mitre['mitre_tactic'],
        risk_score=score,
        severity=severity
    )
    
    from backend.database import get_geo_info
    geo = get_geo_info(client_ip)
    quarantined, _ = active_defense_engine.process_event(client_ip, score, mitre['mitre_name'])
    
    manager.sync_broadcast({
        "id": log_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "attacker_ip": client_ip,
        "port": 8000,
        "decoy_service": "DECOY_API_DB_EXPORT",
        "attack_type": "Rogue DB Export Attempt",
        "payload": payload,
        "mitre_id": mitre['mitre_id'],
        "mitre_name": mitre['mitre_name'],
        "mitre_tactic": mitre['mitre_tactic'],
        "risk_score": score,
        "severity": severity,
        "quarantined": quarantined,
        "country": geo['country'],
        "city": geo['city'],
        "lat": geo['lat'],
        "lng": geo['lng'],
        "flag": geo['flag']
    })
    return JSONResponse({"error": "Forbidden", "message": "Honeytoken trigger recorded"}, status_code=403)

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def start_sensors(broadcast_cb):
    # Initialize SQLite Database
    init_db()

    # Set Web Callback
    set_web_broadcast_callback(broadcast_cb)

    # Start SSH Decoy
    ssh_server = SSHHoneypotServer(port=PORT_SSH_HONEYPOT, broadcast_callback=broadcast_cb)
    ssh_server.start()

    # Start Web Admin Decoy
    web_server = WebHoneypotServer(port=PORT_WEB_HONEYPOT)
    web_server.start()

    # Start Raw Port Scan Decoy
    raw_server = RawDecoyServer(ports=DECOY_PORTS, broadcast_callback=broadcast_cb)
    raw_server.start()

    print("[Aegis-SOC Engine] All decoy sensors initialized & running!")

@app.post("/api/tester/launch")
async def launch_tester():
    try:
        import threading
        from backend.tester_gui import launch_tester_gui
        threading.Thread(target=launch_tester_gui, daemon=True).start()
        return JSONResponse({"status": "SUCCESS", "message": "Tester/Attacker Suite Desktop Window Opened"})
    except Exception as e:
        return JSONResponse({"status": "ERROR", "message": str(e)}, status_code=500)

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    manager.set_loop(loop)
    start_sensors(manager.sync_broadcast)
