# K.A.R.M.A Cloud SIEM — Autonomous AI Threat Deception Platform & Security Incident Event Management

![K.A.R.M.A Cloud SIEM Banner](frontend/Project_Assets/karma_logo.png)

> **K.A.R.M.A**: **K**anaka, **A**bhijeet, **R**aghunandan — **M**onitoring Engine & **A**ctive Cyber Deception Architecture.
> 
> *"In Cybersecurity, KARMA signifies that an adversary's attack probes return directly to trap, profile, and isolate them automatically."*

---

## 🏛️ Academic Project Information

- **Institution**: The Oxford Evening Polytechnic, Bangalore, Karnataka
- **Department**: Department of Computer Science & Engineering
- **Program**: Diploma in Computer Science & Engineering (Cyber Security Major Project)
- **Course Code**: Semester VI Major Project (20CS61P)
- **Academic Year**: 2025 – 2026
- **Project Guide & Mentor**: **Mr. Subhash J R** (Lecturer, Dept of Computer Science & Engineering)

### 👥 Student Development Team
1. **Abhijeet Kumar** — *Team Lead & Core System Architect*
2. **Kanaka C** — *Security Analyst & Frontend UI/UX Engineer*
3. **Raghunandan T V** — *Backend Engineer & Threat Intelligence Specialist*

---

## ⚡ Executive Summary

**K.A.R.M.A Cloud SIEM** is an enterprise-grade Autonomous Cyber Threat Deception & Incident Response Platform designed to trap, analyze, and neutralize cyber adversaries in real time. Combining active protocol honeypots, honeytoken secret traps, automated MITRE ATT&CK TTP classification, and DeepSeek AI threat intelligence, K.A.R.M.A provides full SOC visibility across enterprise subnets.

---

## 🚀 Key Architecture & Platform Features

### 1. 🛡️ Active Multi-Protocol Honeypot Sensors
- **OpenSSH Protocol Honeypot (`Port 2222`)**: Built on Paramiko with persistent RSA host keys (`ssh_host_rsa_key`). Traps authentication brute-force attempts and records interactive bash shell commands (`whoami`, `id`, `cat /etc/passwd`), mapping them to **MITRE T1059**.
- **Web Admin Vulnerability Honeypot (`Port 8080`)**: Simulates vulnerable web applications, capturing SQL Injection (`UNION SELECT`), Cross-Site Scripting (XSS), and Path Traversal (`../../etc/passwd`).
- **Multi-Port Decoy Sensors (`Ports 21 FTP, 23 Telnet, 3389 RDP`)**: Detects early network service discovery probes (Nmap, Masscan), mapping them to **MITRE T1046**.

### 2. 🔑 Production Honeytoken Vault (`Port 8000`)
- Deploys decoy AWS access keys (`AKIA...`), database recovery URLs (`/secret-vault-admin-login-php`), and staging credentials.
- Triggers instant critical severity alerts when accessed by attackers.

### 3. 🌐 Real-Time Cloud SIEM Monitoring Console
- **Attacker Origin Geolocation World Map**: Live Leaflet.js world map rendering attacker IP locations, country flags, and threat score markers.
- **WebSockets Telemetry Dispatcher**: Low-latency event streaming directly to the browser UI.
- **Zoomable Threat Velocity Line Chart**: Features `➕`, `➖`, and `🔄 Fit` zoom controls with automatic X-axis label compression.
- **Uncapped Threat Counter**: Continuously tracks real-time attack counts across all ports.
- **CSV Session Audit Archiver**: Automatically logs session events to `logs/karma_audit_YYYY-MM-DD_HH-MM-SS.csv` with one-click preview and download capabilities.

### 4. 🧠 DeepSeek AI Threat Intelligence & MITRE ATT&CK Classifier
- Integrated with **DeepSeek AI Neural Engine** (`deepseek-chat`) to generate detailed incident response reports analyzing attacker intent, threat severity, and remediation steps.
- Automatic TTP taxonomy classification (`T1046 Network Discovery`, `T1110 Brute Force`, `T1059 Command Interpreter`, `T1190 Exploit Public App`, `T1078 Valid Accounts`).

### 5. 🧰 Built-in Cyber Toolkit
- **Password Security & Market Hasher**: Zero-storage client privacy notice, entropy calculation, GPU offline crack time estimation, and market hashes (**SHA-256**, **SHA-512**, **MD5**).
- **AI Phishing .EML Analyzer**: Drag-and-drop RFC822 MIME email parser, Return-Path domain alignment check, SPF/DKIM verification, and DeepSeek AI threat detection.

---

## 🛠️ Installation & Quickstart Guide

### Option 1: Running from Source Code (Python 3.10+)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/abhikr1436/KARMA-HoneyPot.git
   cd KARMA-HoneyPot
   ```

2. **Install Required Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the K.A.R.M.A Control Panel**:
   ```bash
   python run.py
   ```
   - **SIEM Web SOC Dashboard**: `http://localhost:8000`
   - **Web Honeypot Trap**: `http://localhost:8080`
   - **SSH Honeypot Trap**: `ssh root@<TARGET_IP> -p 2222`

---

### Option 2: Standalone Executable Package (`setup.py`)

No Python, Git, or pip installation required!

1. Compile the standalone package:
   ```bash
   python setup.py
   ```
2. Navigate to `dist/KARMA_Cloud_SIEM/` or extract `dist/KARMA_Cloud_SIEM_Standalone_v1.0.zip`.
3. Double-click **`KARMA_Cloud_SIEM.exe`** to run on any Windows PC!

---

## 🧪 Demonstration & Testing Guide

### 1. Test SSH Honeypot
Run from any terminal:
```bash
ssh root@127.0.0.1 -p 2222
```
Enter any password (e.g. `admin123`), execute commands (`whoami`, `id`, `cat /etc/passwd`), and view the captured commands live on the K.A.R.M.A Dashboard!

### 2. Test Honeytoken Vault Trap
Navigate to:
```
http://localhost:8000/secret-vault-admin-login-php
```
Watch an instant critical alert trigger on the real-time telemetry log table.

### 3. Test AI Phishing .EML Analyzer
Open **`AI Phishing .EML Analyzer`** under the `CYBER TOOLKIT` tab in the web dashboard and click `🧪 Sample .EML` to view a live DeepSeek AI forensic report!

---

## 📜 License & Copyright
Developed for **Semester VI Major Project (20CS61P)** at **The Oxford Evening Polytechnic**, Bangalore.
© 2025–2026 Team K.A.R.M.A (Abhijeet Kumar, Kanaka C, Raghunandan T V). All rights reserved.
