# K.A.R.M.A Cloud SIEM — Autonomous AI Threat Deception & MITRE ATT&CK Platform

**K.A.R.M.A Cloud SIEM** is an advanced, production-grade Cybersecurity project built for final year engineering/diploma defense. It integrates real-time threat deception (honeypots & honeytokens), automated MITRE ATT&CK TTP mapping, AI threat synthesis, dynamic risk scoring, autonomous IP quarantine, and a stunning futuristic Glassmorphism Dark-Mode SOC Dashboard.

---

## 🌟 Key Features

1. **Multi-Service Decoy Sensors (Honeypots):**
   - **Fake SSH Server (Port 2222):** Traps authentication brute-forcing and logs interactive shell commands.
   - **Corporate Admin Portal Decoy (Port 8080):** Traps SQL Injection, XSS, Directory Traversal, and credential stuffing.
   - **Multi-Port Probe Decoys (Ports 21, 23, 3389):** Traps port scanners (Nmap, Masscan).

2. **Honeytoken Vault:**
   - Generates decoy AWS keys (`AKIA...`), backdoor URLs (`/secret-vault-admin-login-php`), and staging credentials. Triggers instant critical severity alerts when touched.

3. **Autonomous MITRE ATT&CK Mapping:**
   - Automatically maps incoming telemetry to official MITRE techniques (`T1110`, `T1190`, `T1059`, `T1046`, `T1078`, `T1595`).

4. **AI Threat Synthesizer & Active Defense:**
   - Synthesizes raw attack streams into executive incident summaries, classifies attacker intent, computes risk scores (0-100), and automatically quarantines dangerous IPs.

5. **1-Click Built-in Attack Simulator:**
   - Allows effortless live demonstration during project defense with zero external setup.

---

## 🚀 Quickstart Guide

### Prerequisites
* Python 3.10+
* Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Start the Aegis-SOC System
Run:
```bash
python run.py
```
Open your browser and navigate to:
* **Cyber SOC Dashboard:** `http://localhost:8000`
* **Web Admin Decoy Portal:** `http://localhost:8080`

### Launch Attack Simulation for Demonstration
Inside the dashboard at `http://localhost:8000`, click **"⚡ Launch Attack Simulator"**, or run:
```bash
python -m backend.attack_simulator
```
Watch the real-time attack stream, MITRE matrix heatmap, and AI threat report populate live!
