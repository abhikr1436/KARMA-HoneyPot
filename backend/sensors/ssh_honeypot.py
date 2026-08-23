"""
Fake SSH Decoy Sensor for Aegis-SOC
Traps SSH authentication attempts and logs interactive command telemetry.
"""

import socket
import threading
import time
from backend.config import PORT_SSH_HONEYPOT
from backend.engine.mitre_mapper import map_payload_to_mitre
from backend.engine.threat_score import calculate_event_risk
from backend.database import log_attack_event
from backend.engine.active_defense import active_defense_engine

# Global instance reference for stopping
_ssh_honeypot_instance = None

FAKE_SHELL_RESPONSES = {
    "whoami": "root\r\n",
    "id": "uid=0(root) gid=0(root) groups=0(root)\r\n",
    "uname -a": "Linux aegis-soc-gateway 5.15.0-76-generic #83-Ubuntu SMP x86_64 GNU/Linux\r\n",
    "ls": "bin  boot  etc  home  lib  opt  root  sys  tmp  var\r\n",
    "ls -l": "total 32\r\ndrwxr-xr-x 2 root root 4096 Aug 23 12:00 bin\r\ndrwxr-xr-x 12 root root 4096 Aug 23 12:00 etc\r\n-rw------- 1 root root 1024 Aug 23 12:00 id_rsa\r\n-rw-r--r-- 1 root root  512 Aug 23 12:00 config.json\r\n",
    "cat /etc/passwd": "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nadmin:x:1000:1000:AegisAdmin:/home/admin:/bin/bash\r\n",
    "cat /etc/shadow": "root:$6$vUaZ4mN...:19200:0:99999:7:::\r\nadmin:$6$xKw9L1...:19200:0:99999:7:::\r\n",
    "cat /etc/issue": "Ubuntu 22.04.3 LTS \\n \\l\r\n",
    "pwd": "/root\r\n",
    "hostname": "aegis-soc-gateway\r\n",
}

class SSHHoneypotServer:
    def __init__(self, host="0.0.0.0", port=PORT_SSH_HONEYPOT, broadcast_callback=None):
        global _ssh_honeypot_instance
        self.host = host
        self.port = port
        self.broadcast_callback = broadcast_callback
        self.running = False
        self.server_socket = None
        _ssh_honeypot_instance = self

    def start(self):
        from backend.decoy_state import is_decoy_enabled
        if not is_decoy_enabled("ssh_2222"):
            print(f"[SSH Decoy Sensor] SSH Honeypot (Port {self.port}) is DISABLED in launcher config. Skipping socket bind.")
            return

        self.running = True
        thread = threading.Thread(target=self._run_server, daemon=True)
        thread.start()

    def _run_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"[SSH Decoy Sensor] Listening on port {self.port}...")

            while self.running:
                try:
                    client_sock, client_addr = self.server_socket.accept()
                    client_ip = client_addr[0]
                    threading.Thread(target=self._handle_client, args=(client_sock, client_ip), daemon=True).start()
                except Exception:
                    break
        except Exception as e:
            print(f"[SSH Decoy Sensor] Socket error on port {self.port}: {e}")

    def _handle_client(self, client_sock, client_ip):
        try:
            # Send fake SSH Banner
            banner = b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1\r\n"
            client_sock.sendall(banner)
            client_sock.settimeout(6.0)

            # Prompt simulation loop
            client_sock.sendall(b"root@aegis-gateway:~# ")

            while self.running:
                data = client_sock.recv(1024)
                if not data:
                    break

                raw_cmd = data.decode('utf-8', errors='ignore').strip()
                if not raw_cmd:
                    continue

                if raw_cmd.lower() in ["exit", "quit"]:
                    client_sock.sendall(b"logout\r\n")
                    break

                payload_info = f"SSH Executed Command: '{raw_cmd}'"

                # Map executed command to MITRE TTP
                mitre_key = "ssh_command_execution"
                if "cat /etc" in raw_cmd or "shadow" in raw_cmd or "passwd" in raw_cmd:
                    mitre_key = "credential_access"
                elif "whoami" in raw_cmd or "id" in raw_cmd or "uname" in raw_cmd:
                    mitre_key = "system_discovery"

                mitre = map_payload_to_mitre("SSH_HONEYPOT", mitre_key, payload_info)
                score, severity = calculate_event_risk(mitre['risk_score'])

                # Log to DB
                log_id = log_attack_event(
                    attacker_ip=client_ip,
                    port=self.port,
                    decoy_service="SSH_HONEYPOT",
                    attack_type="SSH Command Execution / Probe",
                    payload=payload_info,
                    mitre_id=mitre['mitre_id'],
                    mitre_name=mitre['mitre_name'],
                    mitre_tactic=mitre['mitre_tactic'],
                    risk_score=score,
                    severity=severity
                )

                from backend.database import get_geo_info
                geo = get_geo_info(client_ip)

                # Active Defense Check
                quarantined, q_msg = active_defense_engine.process_event(client_ip, score, mitre['mitre_name'])

                # Broadcast via WebSocket
                if self.broadcast_callback:
                    self.broadcast_callback({
                        "id": log_id,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "attacker_ip": client_ip,
                        "port": self.port,
                        "decoy_service": "SSH_HONEYPOT",
                        "attack_type": "SSH Command Execution / Probe",
                        "payload": payload_info,
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

                # Determine fake shell response
                cmd_lower = raw_cmd.lower()
                response = FAKE_SHELL_RESPONSES.get(cmd_lower)
                if not response:
                    response = f"bash: {raw_cmd.split()[0]}: command not found\r\n"

                client_sock.sendall(response.encode('utf-8') + b"root@aegis-gateway:~# ")

            client_sock.close()
        except Exception:
            try:
                client_sock.close()
            except Exception:
                pass

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass

def stop_ssh_sensor():
    global _ssh_honeypot_instance
    if _ssh_honeypot_instance:
        _ssh_honeypot_instance.stop()
