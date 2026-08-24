# K.A.R.M.A Threat Deception Platform
## Kali Linux Penetration Testing & Honeypot Audit Guide

This guide provides step-by-step instructions to perform real-world penetration testing and adversary simulation against the **K.A.R.M.A Cloud SIEM & Threat Deception Platform** using **Kali Linux in VirtualBox**.

---

## 📋 Prerequisites & Network Setup

### 1. VirtualBox Network Configuration
To allow your Kali Linux Virtual Machine (VM) to communicate with the host Windows machine running K.A.R.M.A:
1. Open **VirtualBox** -> Select your **Kali Linux VM** -> Click **Settings**.
2. Go to **Network** -> Set **Adapter 1** to **Bridged Adapter** (select your active Wi-Fi or Ethernet adapter).
3. Start Kali Linux and open a terminal.

### 2. Identify Target & Attacker IP Addresses
- **Host Machine IP (Running K.A.R.M.A)**: Run `ipconfig` in Windows PowerShell (e.g., `10.160.142.46` or `192.168.1.50`).
- **Kali Linux VM IP**: Run `ip a` or `ifconfig` in Kali terminal (e.g., `10.160.142.99`).

> 💡 **Note**: Throughout this guide, replace `<TARGET_IP>` with your Windows Host IP address.

---

## 🚀 Module 1: Network Service Discovery & Port Reconnaissance (Nmap)

Perform active network scanning to identify open honeypot decoy ports.

### Commands to Run in Kali Terminal:

#### 1. Fast Nmap Scan on Active Decoy Ports:
```bash
nmap -sS -sV -p 21,23,8000,8080,2222,3389 <TARGET_IP>
```

#### 2. Comprehensive OS Fingerprinting & Aggressive Service Scan:
```bash
nmap -A -p 21,23,8000,8080,2222 <TARGET_IP>
```

#### Expected Results on K.A.R.M.A Dashboard:
- Real-Time Event Log Inspector records Nmap probe packets.
- Automatically mapped to **MITRE ATT&CK T1046 (Network Service Discovery)**.
- Attacker Origin World Map updates with Kali Linux IP and location marker.

---

## 🔒 Module 2: Interactive OpenSSH Shell Trapping (Port 2222)

Simulate an SSH credential brute-force attack and execute interactive post-exploitation Linux shell commands.

### Commands to Run in Kali Terminal:

#### 1. Connect to SSH Decoy Listener:
```bash
ssh root@<TARGET_IP> -p 2222
```
*(Enter any password when prompted, e.g., `admin123` or `password123`)*

#### 2. Execute Reconnaissance Commands in Fake Shell:
Once connected to the fake OpenSSH shell (`root@aegis-gateway:~#`), execute:
```bash
whoami
id
uname -a
cat /etc/passwd
ls -la
pwd
```
Type `exit` to disconnect.

#### Expected Results on K.A.R.M.A Dashboard:
- Captures exact executed hacker commands (`whoami`, `cat /etc/passwd`).
- Mapped to **MITRE ATT&CK T1059 (Command and Scripting Interpreter)**.
- Clicking **`⚡ AI Report`** on the dashboard row generates a detailed forensic report analyzing the password leak attempt!

---

## 📁 Module 3: ProFTPD File Transfer Trapping (Port 21)

Probe the FTP honeypot decoy and attempt unencrypted authentication.

### Commands to Run in Kali Terminal:

#### Option A: Using Standard FTP Client
```bash
ftp <TARGET_IP> 21
```
When prompted:
- **Name**: `root` or `admin`
- **Password**: `admin123`

Run FTP status commands:
```ftp
pwd
ls
help
quit
```

#### Option B: Using Netcat (`nc`)
```bash
nc -vn <TARGET_IP> 21
```
Type:
```text
USER root
PASS admin123
QUIT
```

#### Expected Results on K.A.R.M.A Dashboard:
- Banner output: `220 ProFTPD 1.3.5 Server Ready`.
- Traps unencrypted credentials and logs FTP commands.

---

## 📟 Module 4: Telnet Management Port Trapping (Port 23)

Simulate legacy router/switch management port probing.

### Commands to Run in Kali Terminal:
```bash
telnet <TARGET_IP> 23
```
Or using Netcat:
```bash
nc -vn <TARGET_IP> 23
```

When prompted, type:
```text
admin
cat /etc/shadow
systemctl status
exit
```

#### Expected Results on K.A.R.M.A Dashboard:
- Returns fake Linux banner prompt (`Ubuntu 22.04 LTS aegis-decoy login:`).
- Logs Telnet inputs into telemetry inspector.

---

## 🌐 Module 5: OWASP Web Application Exploit Probing (Port 8080)

Launch web application vulnerability scans and SQL Injection exploit payloads against the Web Admin Decoy.

### Commands to Run in Kali Terminal:

#### 1. SQL Injection Authentication Bypass Payload:
```bash
curl -i "http://<TARGET_IP>:8080/admin/login.php?user=' OR 1=1 --"
```

#### 2. Cross-Site Scripting (XSS) Exploit Probe:
```bash
curl -i "http://<TARGET_IP>:8080/index.php?search=<script>alert('XSS')</script>"
```

#### 3. Automated Web Scanner Probe (Nikto):
```bash
nikto -h http://<TARGET_IP>:8080
```

#### Expected Results on K.A.R.M.A Dashboard:
- Mapped to **MITRE ATT&CK T1190 (Exploit Public-Facing Application)**.
- Severity flagged as **`HIGH`** or **`CRITICAL`**.

---

## 🍯 Module 6: Port 8000 Honeytoken Decoy & Dashboard Protection Trap

Test the security controls and active honeytoken traps on Port 8000.

### Commands to Run in Kali Terminal:

#### 1. Unauthorized Remote SIEM Dashboard Access Attempt:
Attempting to open the SIEM dashboard from Kali Linux:
```bash
curl -i "http://<TARGET_IP>:8000/"
```
- **Result**: Returns `403 ACCESS FORBIDDEN`. Kali Linux IP is logged and quarantined!

#### 2. Honeytoken API Endpoint Exfiltration Probe:
```bash
curl -i "http://<TARGET_IP>:8000/api/v1/auth/keys"
```
- **Result**: Returns `403 Forbidden` honeytoken trap message.

#### 3. Honeytoken Admin Vault Credential Compromise Trap:
```bash
curl -i -X POST "http://<TARGET_IP>:8000/real-admin" \
  -d "username=admin@aegis-corp.com&password=AdminPass2026!"
```
- **Result**: Returns `🚨 HONEYTOKEN TRAP ACTIVATED`.

#### Expected Results on K.A.R.M.A Dashboard:
- Triggers **CRITICAL (95/100)** threat alert.
- Automatically invokes **K.A.R.M.A Active Defense Engine** to **QUARANTINE & BLOCK** the Kali VM IP!
- Displayed under **Quarantined Adversaries** widget.

---

## ⚡ Module 7: Automated Multi-Vector APT Attack Script

Run an automated Python script from Kali Linux to launch a multi-protocol attack campaign.

### Save and Execute Script in Kali Linux:

Create file `karma_attack_audit.py` in Kali Linux:
```python
import socket
import time
import urllib.request

target_ip = input("Enter K.A.R.M.A Target Host IP: ").strip()

print(f"\n🚀 Launching K.A.R.M.A Penetration Audit against {target_ip}...\n")

# 1. SSH Decoy Audit
print("[+] Testing SSH Decoy (Port 2222)...")
try:
    s = socket.socket()
    s.connect((target_ip, 2222))
    banner = s.recv(1024).decode('utf-8', errors='ignore')
    print(f"    Banner: {banner.strip()}")
    s.send(b"SSH-2.0-OpenSSH_8.9p1\r\n")
    time.sleep(0.5)
    s.close()
except Exception as e:
    print(f"    SSH Error: {e}")

# 2. FTP Decoy Audit
print("[+] Testing FTP Decoy (Port 21)...")
try:
    s = socket.socket()
    s.connect((target_ip, 21))
    banner = s.recv(1024).decode('utf-8', errors='ignore')
    print(f"    Banner: {banner.strip()}")
    s.send(b"USER root\r\n")
    time.sleep(0.3)
    s.send(b"PASS admin123\r\n")
    time.sleep(0.3)
    s.close()
except Exception as e:
    print(f"    FTP Error: {e}")

# 3. Web SQLi Exploit Audit
print("[+] Testing Web Decoy SQLi (Port 8080)...")
try:
    url = f"http://{target_ip}:8080/admin/login?user=' OR 1=1 --"
    req = urllib.request.urlopen(url, timeout=3)
    print(f"    Web Response Code: {req.getcode()}")
except Exception as e:
    print(f"    Web Probe Sent: {e}")

# 4. Honeytoken API Trap Audit
print("[+] Testing Honeytoken API Trap (Port 8000)...")
try:
    url = f"http://{target_ip}:8000/api/v1/auth/keys"
    req = urllib.request.urlopen(url, timeout=3)
except Exception as e:
    print(f"    Honeytoken Trap Hit (Expected 403 Forbidden): {e}")

print("\n✔ Audit completed! Check K.A.R.M.A Web Dashboard & CSV Audit Logs.\n")
```

Run in Kali terminal:
```bash
python3 karma_attack_audit.py
```

---

## 📊 Verification & Demonstration Checklist

After completing the tests, verify the following on your **K.A.R.M.A Web Dashboard** (`http://127.0.0.1:8000`):

| Test Module | Expected SIEM Output | Status |
| :--- | :--- | :---: |
| **Nmap Scan** | MITRE `T1046 Network Service Discovery` event logged | ✅ Pass |
| **SSH Shell** | Executed commands (`whoami`, `cat /etc/passwd`) captured | ✅ Pass |
| **FTP Probe** | Unencrypted credentials logged | ✅ Pass |
| **Web SQLi** | MITRE `T1190 Exploit Public-Facing App` logged | ✅ Pass |
| **Honeytoken** | MITRE `T1078 Valid Accounts` logged & IP Quarantined | ✅ Pass |
| **AI Report** | `⚡ AI Report` button generates dynamic incident analysis | ✅ Pass |
| **CSV Logs** | `logs/karma_audit_*.csv` contains all Kali attack rows | ✅ Pass |

---
*Created for **The Oxford Evening Polytechnic • Department of Computer Science & Engineering***
*Project: K.A.R.M.A Cloud SIEM & Active Cyber Deception Architecture*
