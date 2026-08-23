"""
Automated Attack Simulator for Aegis-SOC Live Demonstrations
Simulates realistic cyber attack traffic (SSH Brute Force, Web SQLi, Honeytoken leaks, Port Scans).
"""

import socket
import urllib.request
import urllib.parse
import time
import random
from backend.config import PORT_SSH_HONEYPOT, PORT_WEB_HONEYPOT, DECOY_PORTS

TARGET_IP = "127.0.0.1"

# Simulated Attacker IPs for demonstration variety
ATTACKER_IPS = [
    "192.168.1.105",
    "10.0.4.12",
    "185.220.101.5",  # Tor Exit Node sample
    "45.33.32.156",   # Nmap scanner sample
    "198.51.100.42"   # External test IP
]

def simulate_ssh_brute_force():
    print("[Attack Simulator] Launching SSH Brute-Force Attack (T1110)...")
    passwords = ["admin123", "root2026", "password", "toor", "123456", "supersecret"]
    attacker_ip = random.choice(ATTACKER_IPS)

    for pwd in passwords[:4]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((TARGET_IP, PORT_SSH_HONEYPOT))
            # Read banner
            s.recv(1024)
            # Send fake SSH auth string
            auth_str = f"SSH-2.0-OpenSSH_8.9 | User: root Pass: {pwd}\r\n".encode()
            s.sendall(auth_str)
            s.close()
            time.sleep(0.3)
        except Exception as e:
            print(f"[Attack Simulator] SSH attack connect error: {e}")

def simulate_web_sqli_attack():
    print("[Attack Simulator] Launching Web SQL Injection & OWASP Top 10 Attack (T1190)...")
    payloads = [
        ("admin' OR '1'='1", "password123"),
        ("<script>alert('XSS_Exfiltration')</script>", "testpass"),
        ("SELECT * FROM users WHERE id=1 UNION SELECT 1,2,@@version--", "sqli_pass"),
        ("../../../etc/passwd", "path_traversal")
    ]

    for user, pwd in payloads:
        try:
            data = urllib.parse.urlencode({'username': user, 'password': pwd}).encode('utf-8')
            req = urllib.request.Request(f"http://{TARGET_IP}:{PORT_WEB_HONEYPOT}/login", data=data)
            with urllib.request.urlopen(req, timeout=2) as resp:
                _ = resp.read()
            time.sleep(0.3)
        except Exception as e:
            print(f"[Attack Simulator] Web attack request sent (handled by decoy): {e}")

def simulate_honeytoken_breach():
    print("[Attack Simulator] Triggering Honeytoken Compromise (T1078)...")
    try:
        url = f"http://{TARGET_IP}:{PORT_WEB_HONEYPOT}/secret-vault-admin-login-php"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as resp:
            _ = resp.read()
    except Exception as e:
        print(f"[Attack Simulator] Honeytoken trigger request sent: {e}")

def simulate_port_scan():
    print("[Attack Simulator] Launching Port Scanning Reconnaissance (T1046)...")
    ports = [PORT_SSH_HONEYPOT, PORT_WEB_HONEYPOT] + DECOY_PORTS
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((TARGET_IP, p))
            s.close()
            time.sleep(0.2)
        except Exception:
            pass

def run_full_attack_scenario():
    print("=== STARTING AEGIS-SOC LIVE ATTACK DEMONSTRATION ===")
    simulate_port_scan()
    time.sleep(1)
    simulate_ssh_brute_force()
    time.sleep(1)
    simulate_web_sqli_attack()
    time.sleep(1)
    simulate_honeytoken_breach()
    print("=== ATTACK DEMONSTRATION COMPLETED ===")

if __name__ == "__main__":
    run_full_attack_scenario()
