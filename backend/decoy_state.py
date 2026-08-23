"""
Decoy State Manager for Aegis-SOC
Manages dynamic enable/disable states for Honeypots, Open Ports, and API Traps.
"""

from typing import Dict, Any
from backend.config import PORT_SSH_HONEYPOT, PORT_WEB_HONEYPOT, DECOY_PORTS

# Default Decoy Registry
DECOYS: Dict[str, Dict[str, Any]] = {
    "ssh_2222": {
        "id": "ssh_2222",
        "name": "SSH Honeypot Server",
        "type": "Protocol Honeypot",
        "port": PORT_SSH_HONEYPOT,
        "enabled": True,
        "description": "Traps SSH brute-force attempts and command probes"
    },
    "web_8080": {
        "id": "web_8080",
        "name": "Corporate Admin Portal Decoy",
        "type": "Web Honeypot",
        "port": PORT_WEB_HONEYPOT,
        "enabled": True,
        "description": "Fake web authentication portal trapping SQLi & credential harvest attempts"
    },
    "port_21": {
        "id": "port_21",
        "name": "FTP Service Decoy",
        "type": "Open Port",
        "port": 21,
        "enabled": True,
        "description": "Monitors unencrypted File Transfer Protocol scan attempts"
    },
    "port_23": {
        "id": "port_23",
        "name": "Telnet Remote Decoy",
        "type": "Open Port",
        "port": 23,
        "enabled": True,
        "description": "Traps legacy Telnet port enumeration and brute-force probes"
    },
    "port_3389": {
        "id": "port_3389",
        "name": "RDP Remote Desktop Decoy",
        "type": "Open Port",
        "port": 3389,
        "enabled": True,
        "description": "Listens for Remote Desktop Protocol connection attempts"
    },
    "api_auth_keys": {
        "id": "api_auth_keys",
        "name": "Decoy API Credentials Trap",
        "type": "API Endpoint",
        "port": 8000,
        "enabled": True,
        "description": "Fake REST endpoint `/api/v1/auth/keys` trapping unauthorized API key theft"
    },
    "api_db_export": {
        "id": "api_db_export",
        "name": "Decoy Database Export Trap",
        "type": "API Endpoint",
        "port": 8000,
        "enabled": True,
        "description": "Fake endpoint `/api/v1/admin/db_export` capturing data exfiltration attempts"
    }
}

def get_all_decoys():
    return list(DECOYS.values())

def is_decoy_enabled(decoy_id: str) -> bool:
    if decoy_id in DECOYS:
        return DECOYS[decoy_id].get("enabled", True)
    return True

def is_port_enabled(port: int) -> bool:
    for decoy in DECOYS.values():
        if decoy.get("port") == port:
            return decoy.get("enabled", True)
    return True

def toggle_decoy(decoy_id: str, enabled: bool = None) -> Dict[str, Any]:
    if decoy_id not in DECOYS:
        return {"status": "ERROR", "message": f"Decoy '{decoy_id}' not found"}
    
    if enabled is None:
        DECOYS[decoy_id]["enabled"] = not DECOYS[decoy_id]["enabled"]
    else:
        DECOYS[decoy_id]["enabled"] = bool(enabled)

    return {
        "status": "SUCCESS",
        "decoy": DECOYS[decoy_id],
        "message": f"Decoy '{DECOYS[decoy_id]['name']}' is now {'ENABLED' if DECOYS[decoy_id]['enabled'] else 'DISABLED'}"
    }

def add_custom_decoy(name: str, port: int, service_type: str, description: str = ""):
    decoy_id = f"custom_port_{port}"
    DECOYS[decoy_id] = {
        "id": decoy_id,
        "name": name,
        "type": service_type or "Custom Decoy Port",
        "port": port,
        "enabled": True,
        "description": description or f"Custom decoy listener on port {port}"
    }
    return DECOYS[decoy_id]
