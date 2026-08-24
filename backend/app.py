"""
K.A.R.M.A Cloud SIEM - Core Application Engine & API Gateway
Authors: Abhijeet Kumar, Kanaka C, Raghunandan T V
Project Guide: Mr. Subhash J R (Dept of Computer Science & Engineering)

Handles FastAPI REST endpoints, WebSocket real-time telemetry streaming,
honeytoken path traps, and session audit log management.
"""

import os
import asyncio
import time
import csv
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Form, Request, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel

from backend.config import PORT_API, PORT_SSH_HONEYPOT, PORT_WEB_HONEYPOT, DECOY_PORTS
from backend.database import (
    init_db, get_recent_logs, get_attackers_list, get_mitre_stats,
    get_honeytokens, get_quarantine_list, clear_all_data, get_db, get_total_attack_count
)
from backend.engine.ai_analyst import generate_ai_threat_summary, generate_single_event_ai_report
from backend.engine.csv_logger import audit_csv_logger
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
        try:
            audit_csv_logger.log_event(data)
        except Exception as e:
            print("[CSV Logger Broadcast Error]:", e)

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
async def root(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"

    # Allow Localhost Access for Admin
    if client_ip in ["127.0.0.1", "::1", "localhost"]:
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)

    # Block External Hacker IP & Trigger Honeytoken Trap
    event_data = {
        "attacker_ip": client_ip,
        "port": 8000,
        "decoy_service": "DECOY_API_KEYS",
        "attack_type": "Unauthorized SIEM Console Scan",
        "payload": f"External Host Attempted Unauthenticated Access to SIEM Console on Port 8000",
        "mitre_id": "T1078",
        "mitre_name": "Valid Accounts / Honeytoken Access",
        "mitre_tactic": "Initial Access",
        "risk_score": 90,
        "severity": "CRITICAL"
    }

    log_attack_event(**event_data)
    active_defense_engine.enforce_ip_quarantine(client_ip, "Unauthorized External Dashboard Probe")
    event_data["quarantined"] = True
    manager.sync_broadcast(event_data)

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>403 Forbidden - K.A.R.M.A Threat Deception Platform</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ background: #090d16; color: #f3f4f6; font-family: 'Plus Jakarta Sans', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
            .card {{ background: #101726; border: 1px solid #ef4444; padding: 40px; border-radius: 12px; width: 440px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            h2 {{ color: #ef4444; margin-top: 0; font-size: 20px; font-weight: 700; }}
            .status-box {{ background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); color: #ef4444; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 13px; margin-top: 20px; line-height: 1.5; }}
            .info {{ color: #9ca3af; font-size: 13px; margin-top: 15px; }}
            .attribution {{ margin-top: 24px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 12px; font-size: 11px; color: #6b7280; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🚨 403 ACCESS FORBIDDEN</h2>
            <p class="info">K.A.R.M.A Active Threat Deception Platform</p>
            <div class="status-box">
                ⚠️ UNAUTHORIZED EXTERNAL ACCESS DENIED<br>
                <span style="font-size: 11px; font-weight: normal; color: #9ca3af;">Attacker IP: {client_ip} | Quarantined by Active Defense</span>
            </div>
            <p class="info">Remote access to the SIEM Control Console is restricted. Your IP has been logged and quarantined.</p>
            <div class="attribution">
                The Oxford Evening Polytechnic • Cyber Security (Sem VI)<br>
                Guide: Mr. Subhash J R | Team: Abhijeet, Kanaka, Raghunandan
            </div>
        </div>
    </body>
    </html>
    """, status_code=403)

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
async def real_admin_authenticate(request: Request, username: str = Form(...), password: str = Form(...)):
    client_ip = request.client.host if request.client else "127.0.0.1"

    # Honeytoken Decoy Trap Trigger
    event_data = {
        "attacker_ip": client_ip,
        "port": 8000,
        "decoy_service": "DECOY_API_KEYS",
        "attack_type": "Honeytoken Credential Compromise",
        "payload": f"Attempted Production Vault Login: username='{username}' pass='{password}'",
        "mitre_id": "T1078",
        "mitre_name": "Valid Accounts / Honeytoken Compromise",
        "mitre_tactic": "Credential Access",
        "risk_score": 95,
        "severity": "CRITICAL"
    }

    log_attack_event(**event_data)
    active_defense_engine.enforce_ip_quarantine(client_ip, "Honeytoken Vault Login Trap Hit")
    event_data["quarantined"] = True
    manager.sync_broadcast(event_data)

    return JSONResponse({
        "status": "QUARANTINED",
        "error": "Honeytoken Trap Triggered",
        "message": f"Attempted Production Vault Login: username='{username}'. IP {client_ip} has been quarantined."
    }, status_code=403)

# Dedicated Honeytoken Decoy Endpoints on Port 8000
@app.get("/api/v1/auth/keys")
@app.get("/api/v1/admin/db_export")
@app.get("/secret-vault-admin-login-php")
@app.get("/admin/login")
async def honeytoken_path_trap(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    path = request.url.path

    event_data = {
        "attacker_ip": client_ip,
        "port": 8000,
        "decoy_service": "DECOY_API_KEYS",
        "attack_type": "Honeytoken Exfiltration Trap",
        "payload": f"Unauthenticated Scanner Accessed Honeytoken Endpoint: '{path}'",
        "mitre_id": "T1078",
        "mitre_name": "Valid Accounts / Honeytoken Access",
        "mitre_tactic": "Credential Access",
        "risk_score": 95,
        "severity": "CRITICAL"
    }

    log_attack_event(**event_data)
    active_defense_engine.enforce_ip_quarantine(client_ip, f"Honeytoken Path Trap Triggered: {path}")
    event_data["quarantined"] = True
    manager.sync_broadcast(event_data)

    return JSONResponse({
        "status": "QUARANTINED",
        "error": "Access Denied",
        "message": f"Honeytoken Decoy Trap Triggered on '{path}'. Incident logged & IP {client_ip} quarantined by K.A.R.M.A Active Defense Engine."
    }, status_code=403)

@app.get("/api/status")
async def get_system_status():
    total_count = get_total_attack_count()
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
            "total_attacks_logged": total_count,
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

@app.get("/api/ai-report/event/{log_id}")
async def get_single_event_ai_report_api(log_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attack_logs WHERE id = ?', (log_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Attack log event not found")

    event = dict(row)
    report = generate_single_event_ai_report(event)
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

@app.get("/api/logs/csv/list")
async def list_csv_logs():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        return []
    
    files = []
    for f in sorted(os.listdir(log_dir), reverse=True):
        if f.endswith(".csv"):
            fpath = os.path.join(log_dir, f)
            size = os.path.getsize(fpath)
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(fpath)))
            
            line_count = 0
            try:
                with open(fpath, 'r', encoding='utf-8') as cf:
                    line_count = max(0, sum(1 for _ in cf) - 1)
            except Exception:
                pass
            
            files.append({
                "filename": f,
                "size_bytes": size,
                "created_time": ctime,
                "row_count": line_count
            })
    return files

@app.get("/api/logs/csv/view/{filename}")
async def view_csv_log(filename: str):
    log_dir = "logs"
    fpath = os.path.join(log_dir, os.path.basename(filename))
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail="CSV Log File not found")

    rows = []
    with open(fpath, 'r', encoding='utf-8') as cf:
        reader = csv.DictReader(cf)
        for r in reader:
            rows.append(r)
    return {"filename": filename, "total_rows": len(rows), "rows": rows}

@app.get("/api/logs/csv/download/{filename}")
async def download_csv_log(filename: str):
    log_dir = "logs"
    fpath = os.path.join(log_dir, os.path.basename(filename))
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail="CSV Log File not found")
    return FileResponse(fpath, media_type="text/csv", filename=filename)

@app.api_route("/api/logs/csv/delete/{filename}", methods=["GET", "DELETE"])
async def delete_csv_log(filename: str):
    log_dir = "logs"
    fpath = os.path.join(log_dir, os.path.basename(filename))
    if os.path.exists(fpath):
        try:
            os.remove(fpath)
            return {"status": "SUCCESS", "message": f"Deleted CSV log file '{filename}'"}
        except Exception as e:
            return JSONResponse({"status": "ERROR", "message": str(e)}, status_code=500)
    raise HTTPException(status_code=404, detail="CSV Log File not found")

@app.post("/api/tools/phishing-eml")
async def analyze_phishing_eml_api(file: UploadFile = File(...)):
    if not file.filename.endswith(".eml") and not file.filename.endswith(".msg"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a valid .eml file.")

    content = await file.read()
    from backend.engine.phishing_analyzer import parse_and_analyze_eml
    return parse_and_analyze_eml(content, filename=file.filename)

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    manager.set_loop(loop)
    audit_csv_logger.start()
    start_sensors(manager.sync_broadcast)

@app.on_event("shutdown")
async def shutdown_event():
    audit_csv_logger.stop()
