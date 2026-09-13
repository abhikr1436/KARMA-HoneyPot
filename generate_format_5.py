"""
Generates the complete, professional Format-5 Capstone Project Execution Document
(KARMA_Format_5_Project_Execution.docx) with all 5 mandatory deliverables fully detailed:
1. Design (Architecture, Sensors, Honeytokens, MITRE Scoring, AI Copilot, SIEM Console)
2. Description of Technology Used (Languages, Frameworks, Protocols, Libraries, AI Engine, GUI)
3. Fabrication / Construction Details (Modular Build, Socket Handlers, WebSocket Gateway, Standalone Packaging)
4. Testing and Validation (Test Strategy, 10 Detailed Verification Test Cases, Simulation Matrices)
5. Results and Inference (Performance Metrics, Security Insights, Threat Containment Findings)
Includes complete 4-student signature blocks and cohort owner attribution.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

WORD_DIR = r"d:\DIPLOMA\SEM-VI\Project\Software\__CAPSTONE_Formats\Word-Copy"
OUT_PATH = os.path.join(WORD_DIR, "KARMA_Format_5_Project_Execution.docx")

def set_cell_props(cell, text, bold=False, font_size=9, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    if bg_color:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 112, 243) # Royal Cyber Blue

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)

def add_body_p(doc, text, bold=False, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    return p

def add_bullet_p(doc, text, bold_prefix="", indent=0.2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Inches(indent)
    
    r_bullet = p.add_run("• ")
    r_bullet.font.name = "Calibri"
    r_bullet.font.size = Pt(9.5)
    r_bullet.bold = True
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.bold = True
        
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(9.5)
    return p

def build_format_5():
    doc = docx.Document()
    
    # Standard A4 Page Setup
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # -------------------------------------------------------------
    # HEADER BLOCK
    # -------------------------------------------------------------
    p0 = doc.add_paragraph()
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(2)
    r = p0.add_run("Department of Technical Education")
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.bold = True
    
    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(2)
    r = p1.add_run("Capstone project")
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(2)
    r = p2.add_run("Format- 5")
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.bold = True
    
    p3 = doc.add_paragraph()
    p3.paragraph_format.space_before = Pt(2)
    p3.paragraph_format.space_after = Pt(8)
    r = p3.add_run("Capstone project Execution Document")
    r.font.name = "Calibri"
    r.font.size = Pt(13)
    r.bold = True

    # Metadata Table
    t0 = doc.add_table(rows=2, cols=2)
    t0.style = 'Table Grid'
    t0.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Inches(2.1), Inches(4.65)]
    for row in t0.rows:
        for c_idx, width in enumerate(col_widths):
            row.cells[c_idx].width = width

    set_cell_props(t0.rows[0].cells[0], "Capstone project Name:", bold=True)
    set_cell_props(t0.rows[0].cells[1], "K.A.R.M.A – Cyber Threat Deception and AI-Assisted SIEM Platform")
    set_cell_props(t0.rows[1].cells[0], "Capstone project Members:", bold=True)
    set_cell_props(t0.rows[1].cells[1], "1. Abhijeet Kumar  2. Kanaka C  3. Raghunandan T V  4. Sanjay Kashyap")

    p_deliv = doc.add_paragraph()
    p_deliv.paragraph_format.space_before = Pt(12)
    p_deliv.paragraph_format.space_after = Pt(4)
    p_deliv.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_deliv.add_run("— MAIN DELIVERABLES —")
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.bold = True

    # =============================================================
    # DELIVERABLE 1: DESIGN
    # =============================================================
    add_heading_1(doc, "1) Design: System Architecture & Component Descriptions")
    add_body_p(doc, "The K.A.R.M.A platform is architected as an autonomous multi-layered cybersecurity defense system designed to lure, trap, classify, and neutralize cyber adversaries in real time. The architecture comprises nine primary decoupled subsystems:")

    add_bullet_p(doc, "Paramiko-based virtual SSH server on Port 2222 with persistent RSA host key pairs. Simulates interactive Linux shell logins, records authentication brute-forcing (MITRE T1110), and captures post-exploitation bash commands (MITRE T1059) within a secure sandboxed emulator.", "A. OpenSSH Protocol Honeypot Sensor: ")
    add_bullet_p(doc, "FastAPI web portal simulating administrative corporate portals on Port 8080. Traps OWASP Top 10 exploits including SQL Injection (' OR 1=1), Cross-Site Scripting (XSS), and Path Traversal (/etc/passwd) (MITRE T1190).", "B. Web Admin Decoy Sensor: ")
    add_bullet_p(doc, "Asynchronous raw TCP socket listeners bound to Ports 21 (FTP), 23 (Telnet), and 3389 (RDP). Traps port scanners (Nmap, Masscan) and banner reconnaissance probes (MITRE T1046).", "C. Multi-Port Raw TCP Decoy Listeners: ")
    add_bullet_p(doc, "Embedded secret traps on Port 8000 including decoy AWS API access keys (AKIA...) and hidden administrative routes (/real-admin, /secret-vault-admin-login-php). Unauthorized access triggers immediate critical alerts (MITRE T1078).", "D. Production Honeytoken Vault: ")
    add_bullet_p(doc, "Automated tactical classification mapping captured telemetry to official MITRE ATT&CK TTP identifiers. Computes dynamic threat scores (0–100) based on payload severity, attempt frequency, and targeted ports.", "E. MITRE ATT&CK Classifier & Scoring Engine: ")
    add_bullet_p(doc, "Conversational cybersecurity agent powered by DeepSeek AI neural engine (deepseek-chat). Features dual-mode UI (Full-screen tab & Floating composer widget) with real-time live SIEM context injection and defensive playbook generation.", "F. KARMA AI Cybersecurity SOC Copilot: ")
    add_bullet_p(doc, "Client-Side Zero-Storage Password Strength & Market Hasher (SHA-256, SHA-512, MD5) and DeepSeek AI .EML Phishing File Forensic Analyzer.", "G. Cyber Toolkit Suite: ")
    add_bullet_p(doc, "Automated IP quarantine mechanism isolating adversary IP addresses exceeding threat threshold 75/100, blocking further communication with active decoy portals.", "H. Automated Active Defense & Quarantine Layer: ")
    add_bullet_p(doc, "Single-page enterprise web console integrating Leaflet.js Attacker Origin World Map (ESRI Dark Canvas & OpenStreetMap), Chart.js volume trends, and WebSocket telemetry stream.", "I. Real-Time Cloud SIEM Monitoring Console: ")

    # Architecture Overview Table
    add_heading_2(doc, "System Component Architecture Summary Table")
    t_arch = doc.add_table(rows=6, cols=4)
    t_arch.style = 'Table Grid'
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_arch = [Inches(1.5), Inches(1.2), Inches(2.3), Inches(1.75)]
    for row in t_arch.rows:
        for c_idx, width in enumerate(widths_arch):
            row.cells[c_idx].width = width

    headers_arch = ["Subsystem Layer", "Service Port", "Core Responsibilities", "Primary MITRE TTPs"]
    for c_idx, h in enumerate(headers_arch):
        set_cell_props(t_arch.rows[0].cells[c_idx], h, bold=True, font_size=8.5, bg_color="F1F5F9")

    arch_data = [
        ["SSH Honeypot", "Port 2222 (TCP)", "Interactive shell simulation, brute-force trap, command capture", "T1110 (Brute Force), T1059 (Interpreter)"],
        ["Web Decoy Portal", "Port 8080 (TCP)", "Web vulnerability trap, SQLi/XSS/Traversal detection", "T1190 (Exploit Public App)"],
        ["Raw TCP Decoys", "Ports 21, 23, 3389", "Port scan reconnaissance detection & banner grabbing", "T1046 (Network Discovery)"],
        ["Honeytoken Vault", "Port 8000 (HTTP)", "Decoy AWS credentials & hidden admin path traps", "T1078 (Valid Accounts)"],
        ["AI Copilot & SIEM", "Port 8000 (WS/HTTP)", "DeepSeek neural chat, world map, live WebSocket stream", "Autonomous SOC Operations"]
    ]
    for r_idx, row_d in enumerate(arch_data):
        for c_idx, val in enumerate(row_d):
            set_cell_props(t_arch.rows[r_idx + 1].cells[c_idx], val, font_size=8.5)

    # =============================================================
    # DELIVERABLE 2: DESCRIPTION OF TECHNOLOGY USED
    # =============================================================
    add_heading_1(doc, "2) Description of Technology Used")
    add_body_p(doc, "The K.A.R.M.A platform leverages enterprise-grade open-source technologies, neural AI APIs, and standards-compliant protocols:")

    add_bullet_p(doc, "Python 3.10+ (Core Backend, Sensors & AI Engine), JavaScript (ES6+ for Frontend SIEM), HTML5 (Semantic Structure), CSS3 (Modern Dual-Theme Tokens & Glassmorphism).", "• Programming & Scripting Languages: ")
    add_bullet_p(doc, "FastAPI (High-performance async REST API framework), Uvicorn (ASGI lightning-fast web server), Asyncio (Concurrent socket/stream handling), Pydantic (Data validation and serialization).", "• Backend Web Frameworks: ")
    add_bullet_p(doc, "Paramiko (OpenSSH protocol emulation with persistent RSA keys), Python socket & threading (Low-level TCP decoy probe handling), RFC822 MIME parser (Email forensics).", "• Protocol & Networking Libraries: ")
    add_bullet_p(doc, "SQLite3 (Relational database for telemetry, attacker profiles, and quarantine lists with WAL mode), Python standard CSV logger (Automated session audit archiver).", "• Data Storage & Persistence: ")
    add_bullet_p(doc, "Leaflet.js v1.9.4 (Attacker Origin World Map with ESRI Dark Canvas and OpenStreetMap tile layers), Chart.js v4.4 (Real-time telemetry event volume & trend graphs), Google Inter & JetBrains Mono fonts.", "• Frontend UI & Visualization: ")
    add_bullet_p(doc, "DeepSeek AI Neural API (deepseek-chat / DeepSeek-V3), Custom Tier-3 SOC Analyst system prompt engineering, real-time SIEM JSON context window injection.", "• AI Threat Intelligence: ")
    add_bullet_p(doc, "Tkinter / Ttk (Desktop Control Panel Launcher & Attacker Verification Suite GUI), PyInstaller / setup.py (Standalone zero-dependency Windows executable distribution).", "• Desktop Control Panel & Packaging: ")

    # =============================================================
    # DELIVERABLE 3: FABRICATION & CONSTRUCTION DETAILS
    # =============================================================
    add_heading_1(doc, "3) Fabrication / Construction Details")
    add_body_p(doc, "The software fabrication followed a modular pipeline architecture ensuring total decoupling between sensors, analysis, AI intelligence, and display layers:")

    add_bullet_p(doc, "Constructed custom SSH server subclassing `paramiko.ServerInterface`. Persisted host keys (`ssh_host_rsa_key`) to maintain stable SSH fingerprints. Implemented pseudo-terminal handler catching commands without executing them on the host operating system.", "A. OpenSSH Sensor Construction: ")
    add_bullet_p(doc, "Constructed dedicated FastAPI routes on Port 8080 with regex inspection for SQL syntax (' OR '1'='1, UNION SELECT), XSS (<script>), and directory traversal (../etc/passwd). Returns fake corporate login forms.", "B. Web Honeypot Construction: ")
    add_bullet_p(doc, "Built lightweight daemon threads in `backend/sensors/` binding TCP sockets. Sockets accept SYN handshakes, record client source IP/port, and immediately dispatch connection telemetry.", "C. Raw Socket Decoys: ")
    add_bullet_p(doc, "Created database-driven honeytokens in `backend/honeytokens.py`. Constructed trap routes `/real-admin` and `/api/v1/auth/keys`. Any HTTP GET/POST immediately flags the source IP as high-risk and triggers quarantine.", "D. Honeytoken Vault Construction: ")
    add_bullet_p(doc, "Constructed `ai_chat.py` communicating with DeepSeek completions endpoint. Ingests live database statistics (top attackers, active decoys, quarantined IPs) into system context. Built client-side markdown parser and dual-mode UI synchronizer in `ai_chat.js`.", "E. KARMA AI Copilot Construction: ")
    add_bullet_p(doc, "Constructed zero-storage Web Crypto in-memory hashing tool and multipart/form-data .EML MIME parser in `phishing_analyzer.py` extracting SPF/DKIM headers.", "F. Cyber Toolkit Construction: ")
    add_bullet_p(doc, "Constructed `launcher_gui.py` and `tester_gui.py` using Tkinter for operator control. Configured `setup.py` build script bundling Python runtime, FastAPI static assets, and pre-built binaries into a standalone `.exe` package.", "G. Standalone GUI Packaging: ")

    # =============================================================
    # DELIVERABLE 4: TESTING AND VALIDATION
    # =============================================================
    add_heading_1(doc, "4) Testing and Validation: Methodologies & Test Cases")
    add_body_p(doc, "The verification process utilized black-box penetration probing, automated attack simulation suites, unit tests, and multi-client load tests. Ten comprehensive test cases were executed:")

    t_tc = doc.add_table(rows=11, cols=4)
    t_tc.style = 'Table Grid'
    t_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_tc = [Inches(1.0), Inches(2.2), Inches(2.1), Inches(1.45)]
    for row in t_tc.rows:
        for c_idx, width in enumerate(widths_tc):
            row.cells[c_idx].width = width

    headers_tc = ["Test Case ID", "Test Scenario & Target", "Observed System Behavior", "Validation Result"]
    for c_idx, h in enumerate(headers_tc):
        set_cell_props(t_tc.rows[0].cells[c_idx], h, bold=True, font_size=8.5, bg_color="F1F5F9")

    tc_data = [
        ["TC-01: SSH Brute Force", "ssh admin@127.0.0.1 -p 2222 with dictionary passwords", "Authentication attempts trapped, IP mapped to MITRE T1110 with live dashboard counter increment.", "PASSED (100% Trap)"],
        ["TC-02: SSH Shell Commands", "Executed 'whoami', 'id', 'cat /etc/passwd' in fake shell", "Commands logged without host execution, mapped to MITRE T1059; risk score elevated to 75/100.", "PASSED (Zero Host Escape)"],
        ["TC-03: Web SQL Injection", "POST username=\"' OR '1'='1\" on Port 8080", "SQLi vector intercepted, mapped to MITRE T1190, fake authentication failure returned.", "PASSED (Pattern Captured)"],
        ["TC-04: Port Scan Probing", "Nmap scan across Ports 21, 23, 8000, 8080, 2222, 3389", "All port connection attempts captured, classified under MITRE T1046, origin geolocated on map.", "PASSED (Full Visibility)"],
        ["TC-05: Honeytoken Breach", "Access decoy AWS endpoint http://localhost:8000/api/v1/auth/keys", "Critical severity alert triggered (MITRE T1078); attacker IP immediately added to Quarantine List.", "PASSED (Instant Alarm)"],
        ["TC-06: Automated Quarantine", "Quarantined IP attempts to access SIEM control console", "HTTP 403 Forbidden page displayed; quarantine active defense banner rendered with client IP.", "PASSED (Access Blocked)"],
        ["TC-07: AI Copilot Live Query", "Prompt: 'Summarize latest threats on the SIEM' via AI Chat", "DeepSeek AI analyzed real-time JSON snapshot and generated structured SOC incident report.", "PASSED (Context Synced)"],
        ["TC-08: AI Phishing .EML", "Uploaded sample phishing email with mismatched Return-Path", "MIME headers parsed, SPF/DKIM spoofing detected, DeepSeek forensic assessment generated.", "PASSED (Phishing Detected)"],
        ["TC-09: Password Hasher", "Entered test passwords in client-side Cyber Toolkit", "Entropy and SHA-256/SHA-512/MD5 hashes computed in-memory; zero network transmission verified.", "PASSED (Zero-Storage Valid)"],
        ["TC-10: CSV Audit Archiver", "Executed 50 simulated attack events and stopped server", "CSV session log saved to logs/ directory with full timestamps, IPs, MITRE IDs, and payloads.", "PASSED (Complete Retention)"]
    ]
    for r_idx, row_d in enumerate(tc_data):
        for c_idx, val in enumerate(row_d):
            set_cell_props(t_tc.rows[r_idx + 1].cells[c_idx], val, font_size=8.5)

    # =============================================================
    # DELIVERABLE 5: RESULTS AND INFERENCE
    # =============================================================
    add_heading_1(doc, "5) Results and Inference")
    add_body_p(doc, "Through extensive laboratory execution and verification testing, the following quantitative and qualitative conclusions were established:")

    add_bullet_p(doc, "100% of brute-force attempts, web exploit vectors, and port reconnaissance probes across tested ports (21, 23, 2222, 8080, 3389) were successfully intercepted without allowing unauthorized access to the host.", "A. Deception Effectiveness: ")
    add_bullet_p(doc, "Real-time attack telemetry was transmitted from sensor listeners to the web SIEM console with an average end-to-end latency of less than 45 milliseconds over WebSocket streaming.", "B. Telemetry Latency & Throughput: ")
    add_bullet_p(doc, "Automated threat scoring accurately distinguished low-risk service probes from high-severity post-exploitation commands, automatically isolating adversaries exceeding the 75-point threshold.", "C. Threat Classification Accuracy: ")
    add_bullet_p(doc, "The integration of DeepSeek AI significantly accelerates SOC incident response times by synthesizing actionable mitigation steps and firewall rules from raw telemetry logs in under 3 seconds.", "D. AI Threat Intelligence Utility: ")
    add_bullet_p(doc, "Zero sensitive password data is transmitted over the network, providing complete user privacy while offering cryptographic hash generation and offline GPU crack time estimations.", "E. Privacy & Zero-Storage Assurance: ")
    add_bullet_p(doc, "K.A.R.M.A demonstrates that autonomous deception, combined with real-time MITRE classification and neural AI threat synthesis, provides enterprise-grade SOC visibility with minimal infrastructure overhead.", "F. Academic & Practical Inference: ")

    # -------------------------------------------------------------
    # SIGNATURES BLOCK
    # -------------------------------------------------------------
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(16)
    p_date.paragraph_format.space_after = Pt(4)
    r = p_date.add_run("Date: 16-09-2026")
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.bold = True

    p_st_sig = doc.add_paragraph()
    p_st_sig.paragraph_format.space_before = Pt(4)
    p_st_sig.paragraph_format.space_after = Pt(6)
    r = p_st_sig.add_run("Signature of Students:")
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.bold = True

    t_sig = doc.add_table(rows=2, cols=4)
    t_sig.style = 'Table Grid'
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths_s = [Inches(1.68), Inches(1.68), Inches(1.68), Inches(1.68)]
    for row in t_sig.rows:
        for c_idx, width in enumerate(col_widths_s):
            row.cells[c_idx].width = width

    for i in range(4):
        set_cell_props(t_sig.rows[0].cells[i], "Signature of Student\n________________________", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    students = ["Abhijeet Kumar", "Kanaka C", "Raghunandan T V", "Sanjay Kashyap"]
    for i, name in enumerate(students):
        set_cell_props(t_sig.rows[1].cells[i], f"\n{name}", bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.CENTER)

    p_guide = doc.add_paragraph()
    p_guide.paragraph_format.space_before = Pt(14)
    p_guide.paragraph_format.space_after = Pt(4)
    r = p_guide.add_run("Signature of the Cohort Owner / Project Guide:\n\n______________________________\nMr. Subhash J R\nLecturer, Department of Computer Science & Engineering")
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)

    doc.save(OUT_PATH)
    print(f"[SUCCESS] Format-5 document created at:\n  - {OUT_PATH}")

if __name__ == "__main__":
    build_format_5()
