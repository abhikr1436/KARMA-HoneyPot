"""
Generates the Hand-Writable Notebook Edition of Continuous Internal Evaluation - CIE - II
File: __CAPSTONE_Formats/CIE/CIE-II.docx

Tailored specifically for writing down into an academic bluebook/notebook with pen:
1. Page 1: Official Header & Assessment Rubric Question Table ONLY, followed by clean Page Break.
2. Page 2 onwards: Clear, concise, point-by-point answers to all 8 questions.
3. No complex image screenshots (cannot be drawn on paper).
4. Includes a simple, clean, hand-drawable Block Diagram (boxes & arrows) that a student can easily draw with a pen and ruler.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

OUT_DIR = r"d:\DIPLOMA\SEM-VI\Project\Software\__CAPSTONE_Formats\CIE"
OUT_PATH = os.path.join(OUT_DIR, "CIE-II.docx")

def set_cell(cell, text, bold=False, font_size=10, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None, space_before=2, space_after=2):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.bold = bold
    r.font.name = "Times New Roman"
    r.font.size = Pt(font_size)
    if bg_color:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

def add_q_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 51, 153)
    return p

def add_sub_title(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    return p

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    return p

def add_bullet_point(doc, text, bold_pre="", indent=0.3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Inches(indent)
    
    rb = p.add_run("• ")
    rb.font.name = "Times New Roman"
    rb.font.size = Pt(11)
    rb.bold = True
    
    if bold_pre:
        rp = p.add_run(bold_pre)
        rp.font.name = "Times New Roman"
        rp.font.size = Pt(11)
        rp.bold = True
        
    rt = p.add_run(text)
    rt.font.name = "Times New Roman"
    rt.font.size = Pt(11)
    return p

def build_cie_document():
    doc = docx.Document()

    # Standard A4 Page Setup
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    # =============================================================
    # PAGE 1: QUESTION PAPER / EVALUATION RUBRIC ONLY
    # =============================================================
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(2)
    r = p_hdr.add_run("DEPARTMENT OF TECHNICAL EDUCATION\nGOVERNMENT OF KARNATAKA\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

    r = p_hdr.add_run("THE OXFORD EVENING POLYTECHNIC, BENGALURU\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 51, 102)

    r = p_hdr.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True

    r = p_hdr.add_run("SIXTH SEMESTER DIPLOMA — CAPSTONE PROJECT (20CS61P)\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    # Question Rubric Table (Exact reproduction of user's screenshot)
    t_rubric = doc.add_table(rows=3, cols=3)
    t_rubric.style = 'Table Grid'
    t_rubric.alignment = WD_TABLE_ALIGNMENT.CENTER
    w_rb = [Inches(1.0), Inches(4.67), Inches(1.0)]
    for row in t_rubric.rows:
        for c_idx, w in enumerate(w_rb):
            row.cells[c_idx].width = w

    # Row 0: Header Banner
    cell_top = t_rubric.rows[0].cells[0]
    cell_top.merge(t_rubric.rows[0].cells[1])
    cell_top.merge(t_rubric.rows[0].cells[2])
    set_cell(cell_top, "Continuous Internal Evaluation- CIE - II conducted at the end of 8th week", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="E2E8F0")

    # Row 1: Subheaders
    set_cell(t_rubric.rows[1].cells[0], "Sl No", bold=True, font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="F1F5F9")
    set_cell(t_rubric.rows[1].cells[1], "Assessment of parameter", bold=True, font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="F1F5F9")
    set_cell(t_rubric.rows[1].cells[2], "Marks", bold=True, font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="F1F5F9")

    # Row 2: Questions & Marks
    set_cell(t_rubric.rows[2].cells[0], "1", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)

    q_text = "Capstone project Details:\n\n" \
             "   •  Description of Technology Used\n" \
             "   •  Details of Hardware devices\n" \
             "   •  Details of software products\n" \
             "   •  Programming languages\n" \
             "   •  Descriptions of the components in the system\n" \
             "   •  Component diagrams and required design if any\n" \
             "   •  Construction or Fabrication details\n" \
             "   •  Any other information needed to execute the capstone project"
    set_cell(t_rubric.rows[2].cells[1], q_text, bold=True, font_size=10)
    set_cell(t_rubric.rows[2].cells[2], "80", bold=True, font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Total Row
    row_tot = t_rubric.add_row()
    for c_idx, w in enumerate(w_rb):
        row_tot.cells[c_idx].width = w
    set_cell(row_tot.cells[0], "", font_size=10)
    set_cell(row_tot.cells[1], "Total", bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.RIGHT)
    set_cell(row_tot.cells[2], "80", bold=True, font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="E2E8F0")

    # Student Identification & Guide Info
    p_info = doc.add_paragraph()
    p_info.paragraph_format.space_before = Pt(16)
    p_info.paragraph_format.space_after = Pt(4)
    r = p_info.add_run("Candidate & Evaluation Identification:")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    t_meta = doc.add_table(rows=6, cols=3)
    t_meta.style = 'Table Grid'
    t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    w_m = [Inches(0.6), Inches(4.07), Inches(2.0)]
    for row in t_meta.rows:
        for c_idx, w in enumerate(w_m):
            row.cells[c_idx].width = w

    set_cell(t_meta.rows[0].cells[0], "Project Title:", bold=True, font_size=9.5)
    t_meta.rows[0].cells[1].merge(t_meta.rows[0].cells[2])
    set_cell(t_meta.rows[0].cells[1], "K.A.R.M.A – Cyber Threat Deception and AI-Assisted SIEM Platform", bold=True, font_size=10, bg_color="F8FAFC")

    set_cell(t_meta.rows[1].cells[0], "Sl.", bold=True, font_size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="F1F5F9")
    set_cell(t_meta.rows[1].cells[1], "Candidate Name & Role", bold=True, font_size=9.5, bg_color="F1F5F9")
    set_cell(t_meta.rows[1].cells[2], "Registration / USN No.", bold=True, font_size=9.5, bg_color="F1F5F9", align=WD_ALIGN_PARAGRAPH.CENTER)

    students = [
        ("1", "ABHIJEET KUMAR (Team Lead & Core Architect)", "470CS24701"),
        ("2", "KANAKA C (Security Analyst & Frontend Engineer)", "470CS23005"),
        ("3", "RAGHUNANDAN T V (Backend Engineer & Threat Intelligence)", "470CS23010"),
        ("4", "SANJAY KASHYAP (Security QA & Penetration Testing Specialist)", "470CS23015")
    ]
    for r_idx, (sl, name, usn) in enumerate(students):
        set_cell(t_meta.rows[r_idx+2].cells[0], sl, font_size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell(t_meta.rows[r_idx+2].cells[1], name, font_size=9.5)
        set_cell(t_meta.rows[r_idx+2].cells[2], usn, font_size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    p_guide = doc.add_paragraph()
    p_guide.paragraph_format.space_before = Pt(8)
    p_guide.paragraph_format.space_after = Pt(8)
    r = p_guide.add_run("Project Guide / Cohort Owner: Mr. Subhash J R (Lecturer, Dept. of CSE)\nEvaluation Timeline: End of 8th Week (16-09-2026)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.bold = True

    p_note = doc.add_paragraph()
    p_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_note.paragraph_format.space_before = Pt(16)
    r = p_note.add_run("— PLEASE TURN OVER FOR COMPLETE ANSWERS TO ALL 8 PARAMETERS —")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.bold = True
    r.italic = True
    r.font.color.rgb = RGBColor(100, 100, 100)

    # FORCE CLEAN PAGE BREAK AFTER PAGE 1
    doc.add_page_break()

    # =============================================================
    # PAGE 2 ONWARDS: COMPLETE, HAND-WRITABLE ANSWERS
    # =============================================================
    p_ans_hdr = doc.add_paragraph()
    p_ans_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ans_hdr.paragraph_format.space_before = Pt(0)
    p_ans_hdr.paragraph_format.space_after = Pt(12)
    r = p_ans_hdr.add_run("ANSWERS TO CIE-II ASSESSMENT PARAMETERS")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True
    r.underline = True

    # -------------------------------------------------------------
    # QUESTION 1: DESCRIPTION OF TECHNOLOGY USED
    # -------------------------------------------------------------
    add_q_heading(doc, "1. Description of Technology Used")
    add_body_p(doc, "K.A.R.M.A is a cyber threat deception and Security Information and Event Management (SIEM) platform designed to lure, detect, classify, and neutralize cyber adversaries in real time. The key technologies used are:")

    add_bullet_point(doc, "Simulates genuine vulnerable services (SSH, Web, FTP, Telnet, RDP) to trap unauthorized reconnaissance and exploits safely in memory.", "1. Cyber Deception (Honeypot Technology): ")
    add_bullet_point(doc, "Built using Python FastAPI and Uvicorn ASGI server, handling hundreds of concurrent connection probes asynchronously without blocking.", "2. Asynchronous Event-Driven Architecture: ")
    add_bullet_point(doc, "Full-duplex WebSocket channels stream incoming attack events instantly to the web dashboard with sub-45ms latency.", "3. Real-Time WebSocket Streaming: ")
    add_bullet_point(doc, "Automatically maps observed attacker payloads and commands to official MITRE Enterprise TTP identifiers (T1110, T1059, T1046, T1190, T1078).", "4. MITRE ATT&CK Threat Classification: ")
    add_bullet_point(doc, "Powered by the DeepSeek-V3 neural engine (`deepseek-chat`). Ingests live database statistics to generate incident triage reports and firewall rules.", "5. Artificial Intelligence (DeepSeek AI): ")
    add_bullet_point(doc, "Integrated Leaflet.js with free ESRI Dark Canvas and OpenStreetMap tile layers, resolving attacker coordinates via GeoIP.", "6. Interactive Geospatial Mapping: ")
    add_bullet_point(doc, "Browser Web Crypto API calculates SHA-256, SHA-512, and MD5 hashes in client memory with zero server transmission, guaranteeing 100% user privacy.", "7. Zero-Storage Cryptographic Toolkit: ")

    # -------------------------------------------------------------
    # QUESTION 2: DETAILS OF HARDWARE DEVICES
    # -------------------------------------------------------------
    add_q_heading(doc, "2. Details of Hardware Devices")
    add_body_p(doc, "K.A.R.M.A runs on standard commodity computer hardware without needing expensive server racks. The physical hardware specifications used are:")

    add_bullet_point(doc, "Intel Core i5-1135G7 (4 Cores, 8 Threads @ 2.40 GHz up to 4.20 GHz). Handles FastAPI server, socket daemons, and database queries.", "1. Host Processor (CPU): ")
    add_bullet_point(doc, "16 GB DDR4 @ 3200 MHz. Maintains in-memory WebSocket queues, GeoIP cache, and virtual terminal shell buffers.", "2. System Memory (RAM): ")
    add_bullet_point(doc, "512 GB NVMe M.2 SSD. Provides high read/write speeds for SQLite database transactions and CSV audit logs.", "3. Primary Storage: ")
    add_bullet_point(doc, "Gigabit Ethernet (10/100/1000 Mbps RJ45) + Intel Wi-Fi 6 AX201 (802.11ax). Binds decoy listener ports on local LAN IP (e.g. 10.30.129.46).", "4. Network Interface Cards: ")
    add_bullet_point(doc, "Secondary laptop (Intel Core i3, 8GB RAM, Kali Linux / Windows). Used to run Nmap port sweeps, Hydra password attacks, and curl exploit tests.", "5. Attacker Simulation Machine: ")
    add_bullet_point(doc, "All decoy services run in user space in Python memory (`shell=False`). Physical host hardware, SSD controllers, and operating system kernels remain completely safe.", "6. Hardware Safety Isolation: ")

    # -------------------------------------------------------------
    # QUESTION 3: DETAILS OF SOFTWARE PRODUCTS
    # -------------------------------------------------------------
    add_q_heading(doc, "3. Details of Software Products")
    add_body_p(doc, "The software stack consists of standard open-source products, database engines, and AI APIs:")

    add_bullet_point(doc, "Windows 10/11 Pro 64-bit (Host development platform) and Ubuntu 22.04 LTS (Emulated guest system).", "1. Operating Systems: ")
    add_bullet_point(doc, "Python 3.10+ standard distribution with asyncio, socket, and threading libraries.", "2. Programming Runtime: ")
    add_bullet_point(doc, "FastAPI v0.110 (Async web framework) and Uvicorn v0.28 (High-speed ASGI web server).", "3. Backend Web Server: ")
    add_bullet_point(doc, "Paramiko v3.4 (OpenSSH protocol emulation with persistent 2048-bit RSA host keys).", "4. SSH Library: ")
    add_bullet_point(doc, "SQLite3 with Write-Ahead Logging (WAL Mode) for high-speed concurrent database writes.", "5. Database Engine: ")
    add_bullet_point(doc, "DeepSeek AI REST API (`deepseek-chat`) for live threat reasoning and .EML email phishing forensics.", "6. AI Neural Engine: ")
    add_bullet_point(doc, "Leaflet.js v1.9.4 (World Map) and Chart.js v4.4 (Live event volume and doughnut charts).", "7. Frontend UI Libraries: ")
    add_bullet_point(doc, "Python Tkinter/Ttk (Control panel) and PyInstaller v6.4 (Standalone .exe packager).", "8. Desktop GUI & Packaging: ")

    # -------------------------------------------------------------
    # QUESTION 4: PROGRAMMING LANGUAGES
    # -------------------------------------------------------------
    add_q_heading(doc, "4. Programming Languages")
    add_body_p(doc, "The system is implemented using four core programming languages:")

    add_bullet_point(doc, "Used for core backend logic, multi-sensor socket daemons, Paramiko SSH server, SQLite database queries, MITRE regex classification, threat scoring formula, DeepSeek AI API integration, and the Tkinter desktop launcher.", "1. Python 3.10+: ")
    add_bullet_point(doc, "Used for single-page dashboard interactivity (app.js), consuming real-time WebSocket telemetry, rendering Leaflet.js world map coordinates, animating Chart.js event graphs, and client-side Web Crypto API hashing.", "2. JavaScript (ES6+): ")
    add_bullet_point(doc, "Used for semantic layout structure, modal dialogs, navigation tabs, KPI metric cards, and drag-and-drop email file upload zones.", "3. HTML5: ")
    add_bullet_point(doc, "Used for the custom design system tokens (HSL colors), Glassmorphism effects (backdrop-filter: blur), responsive CSS Grid layouts, and the Cyber Dark / Crisp Light theme engine.", "4. CSS3: ")
    add_bullet_point(doc, "Used for relational database tables (`events`, `attacker_profiles`, `quarantine`), index creation, and fast parameterized queries.", "5. SQL (SQLite): ")

    # -------------------------------------------------------------
    # QUESTION 5: DESCRIPTIONS OF THE COMPONENTS IN THE SYSTEM
    # -------------------------------------------------------------
    add_q_heading(doc, "5. Descriptions of the Components in the System")
    add_body_p(doc, "The platform consists of nine modular subsystems:")

    add_bullet_point(doc, "Virtual SSH server on Port 2222 with RSA host keys. Simulates Linux bash login, traps brute-force passwords (MITRE T1110), and logs interactive commands (`whoami`, `cat /etc/passwd`) safely without host execution (MITRE T1059).", "1. OpenSSH Honeypot (Port 2222): ")
    add_bullet_point(doc, "Simulated corporate web login portal on Port 8080. Evaluates input requests against regex patterns to trap SQL Injection, XSS, and Path Traversal attacks (MITRE T1190).", "2. Web Admin Decoy (Port 8080): ")
    add_bullet_point(doc, "Asynchronous raw TCP daemon sockets on Ports 21 (FTP), 23 (Telnet), and 3389 (RDP). Traps Nmap port scans and banner grabs (MITRE T1046).", "3. Raw TCP Decoy Listeners: ")
    add_bullet_point(doc, "Decoy AWS API keys (`AKIA...`) and hidden canary routes (`/real-admin`, `/api/v1/auth/keys`). Any access attempt immediately triggers a critical alert (Threat Score: 100/100, MITRE T1078).", "4. Production Honeytoken Vault: ")
    add_bullet_point(doc, "Rule-based signature engine that maps captured raw attack payloads directly to official MITRE Enterprise technique IDs.", "5. MITRE ATT&CK Classifier: ")
    add_bullet_point(doc, "Calculates threat scores (0–100) based on sensor weight, payload maliciousness, and attack frequency. Categories: Low (<30), Medium (30–74), Critical (>=75).", "6. Dynamic Threat Scorer: ")
    add_bullet_point(doc, "Automatically isolates adversary IPs with threat scores >= 75, blocking further access with a custom HTTP 403 deception banner.", "7. Active Defense Quarantine: ")
    add_bullet_point(doc, "AI assistant using DeepSeek API. Ingests live database statistics to generate incident reports and firewall rules. Also analyzes uploaded `.eml` phishing email headers.", "8. KARMA AI SOC Copilot: ")
    add_bullet_point(doc, "Responsive single-page web dashboard with Leaflet world map, Chart.js trends, live event tables, and Tkinter desktop launcher GUI.", "9. Cloud SIEM Dashboard: ")

    # -------------------------------------------------------------
    # QUESTION 6: COMPONENT DIAGRAMS AND REQUIRED DESIGN
    # (SIMPLE HAND-DRAWABLE SCHEMATIC FOR PEN & RULER)
    # -------------------------------------------------------------
    add_q_heading(doc, "6. Component Diagrams and Required Design")
    add_body_p(doc, "Below is the simple block diagram representing the complete system architecture, designed to be easily drawn in a notebook using a pen and ruler:")

    add_sub_title(doc, "K.A.R.M.A System Architecture Block Diagram (Hand-Drawable Schema):")

    diagram_text = """
+-------------------------------------------------------------------------------+
|                           CYBER ATTACKER / SCANNER                            |
|                  (Nmap, Hydra Brute-Force, Web SQLi, Canary Probes)           |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                       MULTI-PROTOCOL DECEPTION SENSORS                        |
|  +--------------------+  +--------------------+  +-------------------------+  |
|  |   Port 2222: SSH   |  |   Port 8080: Web   |  | Ports 21, 23, 3389: TCP |  |
|  |  (Paramiko Shell)  |  |  (OWASP SQLi Trap) |  |   (FTP / Telnet / RDP)  |  |
|  +--------------------+  +--------------------+  +-------------------------+  |
|               +--------------------------------------------+                  |
|               |  Port 8000: Honeytokens (/real-admin, AWS) |                  |
|               +--------------------------------------------+                  |
+-------------------------------------------------------------------------------+
                                      |
                                      v (Raw Telemetry: IP, Port, Payload)
+-------------------------------------------------------------------------------+
|                   CORE PROCESSING PIPELINE & INTELLIGENCE                     |
|                                                                               |
|   1. MITRE ATT&CK Classifier   -->  Maps to TTPs (T1110, T1059, T1190, T1046) |
|   2. Dynamic Threat Scorer     -->  Calculates Risk Score (0 - 100)           |
|   3. Active Defense Quarantine -->  Blocks Attacker IP if Score >= 75 (HTTP 403)
|   4. SQLite Database (WAL)     -->  Stores Events, Attacker Profiles & Logs   |
|   5. WebSocket Event Bus       -->  Pushes Real-Time Event Stream (<45ms)     |
+-------------------------------------------------------------------------------+
                     |                                       |
                     v                                       v
+------------------------------------+   +--------------------------------------+
|        DEEPSEEK AI ENGINE          |   |       PRESENTATION & SIEM UI         |
|  • Model: deepseek-chat            |   |  • Leaflet.js Attacker World Map     |
|  • Ingests Live SIEM DB Snapshot   |   |  • Chart.js Live Attack Graphs       |
|  • Generates SOC Playbooks & Rules |   |  • Dual-Mode AI Copilot Chat Window  |
|  • Analyzes .EML Phishing Forensics|   |  • Zero-Storage Password Hasher Tool |
+------------------------------------+   +--------------------------------------+
"""

    p_diag = doc.add_paragraph()
    p_diag.paragraph_format.space_before = Pt(4)
    p_diag.paragraph_format.space_after = Pt(8)
    p_diag.paragraph_format.line_spacing = 1.0
    r_diag = p_diag.add_run(diagram_text)
    r_diag.font.name = "Courier New"
    r_diag.font.size = Pt(8)
    r_diag.bold = True

    add_body_p(doc, "How to draw this in your notebook:")
    add_bullet_point(doc, "Draw a top box for 'Attacker' with downward arrows.", "Step 1: ")
    add_bullet_point(doc, "Draw a wide box for 'Deception Sensors' containing 4 sub-boxes: SSH (2222), Web (8080), Raw TCP (21/23/3389), and Honeytokens (8000).", "Step 2: ")
    add_bullet_point(doc, "Draw a middle box for 'Core Engine' listing MITRE Classifier, Threat Scorer (0-100), Active Quarantine, SQLite Database, and WebSocket Bus.", "Step 3: ")
    add_bullet_point(doc, "Draw two bottom boxes: 'DeepSeek AI Engine' on the left and 'Web SIEM Dashboard' on the right, connected by downward arrows.", "Step 4: ")

    # -------------------------------------------------------------
    # QUESTION 7: CONSTRUCTION OR FABRICATION DETAILS
    # -------------------------------------------------------------
    add_q_heading(doc, "7. Construction or Fabrication Details")
    add_body_p(doc, "The software was constructed through modular steps:")

    add_bullet_point(doc, "Created `backend/sensors/ssh_sensor.py` subclassing `paramiko.ServerInterface`. Generated a 2048-bit RSA key (`ssh_host_rsa_key`) to keep host fingerprint constant. Traps passwords and logs shell commands in memory.", "1. SSH Honeypot: ")
    add_bullet_point(doc, "Created `backend/sensors/web_sensor.py` on Port 8080. Added regex scanners checking for SQL injection (`' OR '1'='1`), XSS (`<script>`), and directory traversal (`../../etc/passwd`).", "2. Web Honeypot: ")
    add_bullet_point(doc, "Created daemon threads in `backend/sensors/raw_tcp_sensor.py` binding raw sockets on Ports 21, 23, and 3389. Sockets accept handshakes, log IP/port, and send fake banners.", "3. Raw TCP Sockets: ")
    add_bullet_point(doc, "Created `backend/honeytokens.py` seeding routes `/real-admin` and `/api/v1/auth/keys`. Any HTTP request triggers immediate quarantine.", "4. Honeytoken Vault: ")
    add_bullet_point(doc, "Built `backend/engine/websocket_manager.py` using Python `asyncio` to broadcast newly logged attack events to browser clients in real time.", "5. WebSocket Manager: ")
    add_bullet_point(doc, "Created `backend/engine/ai_chat.py` communicating with DeepSeek API. Pulls live database metrics and inserts them into system prompts for accurate incident response.", "6. DeepSeek AI Copilot: ")
    add_bullet_point(doc, "Created `launcher_gui.py` using Python Tkinter for one-click startup and compiled standalone package using PyInstaller in `setup.py`.", "7. GUI Launcher: ")

    # -------------------------------------------------------------
    # QUESTION 8: ANY OTHER INFORMATION NEEDED TO EXECUTE
    # -------------------------------------------------------------
    add_q_heading(doc, "8. Any Other Information Needed to Execute the Capstone Project")
    add_body_p(doc, "Essential setup, startup steps, and test demonstration commands:")

    add_sub_title(doc, "A. System Prerequisites:")
    add_bullet_point(doc, "Operating System: Windows 10/11 or Linux Ubuntu 20.04+ (64-bit).")
    add_bullet_point(doc, "Python Environment: Python 3.10+ installed with pip.")
    add_bullet_point(doc, "Web Browser: Google Chrome, Microsoft Edge, or Mozilla Firefox.")

    add_sub_title(doc, "B. Step-by-Step Execution Commands:")
    add_bullet_point(doc, "Step 1 (Install Dependencies): `pip install -r requirements.txt`")
    add_bullet_point(doc, "Step 2 (Set AI Key): `set DEEPSEEK_API_KEY=<your_deepseek_api_key>`")
    add_bullet_point(doc, "Step 3 (Run Application): `python run.py` (Launches desktop GUI and starts all sensors)")
    add_bullet_point(doc, "Step 4 (Access SIEM Web Dashboard): Open browser to `http://localhost:8000/`")

    add_sub_title(doc, "C. Verification Attack Commands for Viva Demonstration:")
    add_bullet_point(doc, "Test SSH Trap: `ssh admin@localhost -p 2222` -> enter password -> run `whoami`, `cat /etc/passwd`")
    add_bullet_point(doc, "Test Web Trap: Open browser to `http://localhost:8080/` -> input username `' OR '1'='1`")
    add_bullet_point(doc, "Test Port Scan: `nmap -sS -p 21,23,8080,2222,3389 localhost`")
    add_bullet_point(doc, "Test Honeytoken: Open browser to `http://localhost:8000/api/v1/auth/keys` -> observe instant IP quarantine")

    # Final Signatures
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(24)
    p_sig.paragraph_format.space_after = Pt(4)
    r = p_sig.add_run("Student Signatures:\n\n"
                      "1. Abhijeet Kumar: __________________        2. Kanaka C: __________________\n\n"
                      "3. Raghunandan T V: __________________       4. Sanjay Kashyap: __________________\n\n\n"
                      "Signature of Cohort Owner / Guide: __________________     Date: 16-09-2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.bold = True

    doc.save(OUT_PATH)
    print(f"\n[SUCCESS] Notebook-Friendly CIE-II Word Document created at:\n  - {OUT_PATH}")

if __name__ == "__main__":
    build_cie_document()
