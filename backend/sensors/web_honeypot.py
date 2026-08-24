"""
K.A.R.M.A Web Application Honeypot Sensor (Port 8080)
Simulates vulnerability web services, traps SQL Injection, XSS, and Path Traversal probes.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn
import threading
import time
from backend.config import PORT_WEB_HONEYPOT
from backend.engine.mitre_mapper import map_payload_to_mitre
from backend.engine.threat_score import calculate_event_risk
from backend.database import log_attack_event, record_honeytoken_hit
from backend.engine.active_defense import active_defense_engine

web_decoy_app = FastAPI(title="Corporate Admin Portal Decoy")
broadcast_cb = None

def set_web_broadcast_callback(cb):
    global broadcast_cb
    broadcast_cb = cb

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aegis Corporate Vault - Admin Authentication</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .login-box { background: #1e293b; padding: 40px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5); width: 340px; }
        h2 { margin-top: 0; color: #38bdf8; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 6px; font-size: 14px; color: #94a3b8; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 12px; border-radius: 6px; border: none; background: #0284c7; color: white; font-weight: bold; cursor: pointer; font-size: 15px; }
        button:hover { background: #0369a1; }
        .notice { font-size: 11px; color: #64748b; margin-top: 20px; text-align: center; }
        a { color: #0284c7; text-decoration: none; font-size: 12px; display: block; margin-top: 15px; text-align: center; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Aegis Vault Portal</h2>
        <form method="POST" action="/login">
            <div class="form-group">
                <label>Username / Email</label>
                <input type="text" name="username" placeholder="admin@aegis-corp.internal" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="••••••••" required>
            </div>
            <button type="submit">Authenticate</button>
        </form>
        <a href="/secret-vault-admin-login-php">Backdoor Recovery Console (Legacy)</a>
        <div class="notice">Restricted Access. All activity logged & monitored.</div>
    </div>
</body>
</html>
"""

def process_web_attack(client_ip, path, method, payload):
    from backend.decoy_state import is_decoy_enabled
    if not is_decoy_enabled("web_8080"):
        return

    # Check for Honeytoken URL hit
    is_honeytoken = "secret-vault-admin" in path or "AKIAIOSF" in payload
    if is_honeytoken:
        record_honeytoken_hit("ht-admin-url", client_ip)
        attack_type = "Honeytoken Compromise"
        service = "HONEYTOKEN"
    else:
        attack_type = "Web Vulnerability Probe"
        service = "WEB_HONEYPOT"

    mitre = map_payload_to_mitre(service, attack_type, payload or path)
    score, severity = calculate_event_risk(mitre['risk_score'])

    log_id = log_attack_event(
        attacker_ip=client_ip,
        port=PORT_WEB_HONEYPOT,
        decoy_service="WEB_HONEYPOT",
        attack_type=attack_type,
        payload=f"[{method}] Path: {path} | Data: {payload}",
        mitre_id=mitre['mitre_id'],
        mitre_name=mitre['mitre_name'],
        mitre_tactic=mitre['mitre_tactic'],
        risk_score=score,
        severity=severity
    )

    from backend.database import get_geo_info
    geo = get_geo_info(client_ip)

    quarantined, _ = active_defense_engine.process_event(client_ip, score, mitre['mitre_name'])

    if broadcast_cb:
        broadcast_cb({
            "id": log_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "attacker_ip": client_ip,
            "port": PORT_WEB_HONEYPOT,
            "decoy_service": "WEB_HONEYPOT",
            "attack_type": attack_type,
            "payload": f"[{method}] {path} | Payload: {payload}",
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

@web_decoy_app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    process_web_attack(client_ip, request.url.path, "GET", str(request.query_params))
    return HTML_TEMPLATE

@web_decoy_app.get("/secret-vault-admin-login-php", response_class=HTMLResponse)
async def get_honeytoken(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    process_web_attack(client_ip, request.url.path, "GET", "Honeytoken URL Triggered")
    return "<h1 style='color:red; font-family:sans-serif; text-align:center;'>403 Access Denied - Security Alert Triggered</h1>"

@web_decoy_app.post("/login")
async def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    payload = f"user={username} & pass={password}"
    process_web_attack(client_ip, "/login", "POST", payload)
    return HTMLResponse(content="<script>alert('Invalid Authentication Credentials'); window.location.href='/';</script>")

@web_decoy_app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, full_path: str):
    client_ip = request.client.host if request.client else "127.0.0.1"
    process_web_attack(client_ip, f"/{full_path}", request.method, str(request.query_params))
    return HTMLResponse(content="<h1>404 Not Found</h1>", status_code=404)

# Global reference for stopping
_web_honeypot_instance = None

class WebHoneypotServer:
    def __init__(self, host="0.0.0.0", port=PORT_WEB_HONEYPOT):
        global _web_honeypot_instance
        self.host = host
        self.port = port
        self.server = None
        _web_honeypot_instance = self

    def start(self):
        from backend.decoy_state import is_decoy_enabled
        if not is_decoy_enabled("web_8080"):
            print(f"[Web Decoy Sensor] Web Admin Decoy (Port {self.port}) is DISABLED in launcher config. Skipping socket bind.")
            return

        config = uvicorn.Config(web_decoy_app, host=self.host, port=self.port, log_level="error")
        self.server = uvicorn.Server(config)
        thread = threading.Thread(target=self.server.run, daemon=True)
        thread.start()
        print(f"[Web Decoy Sensor] Listening on port {self.port}...")

    def stop(self):
        if self.server:
            self.server.should_exit = True

def stop_web_sensor():
    global _web_honeypot_instance
    if _web_honeypot_instance:
        _web_honeypot_instance.stop()
