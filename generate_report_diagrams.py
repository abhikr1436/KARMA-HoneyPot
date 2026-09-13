"""
Generates high-resolution, professional diagrams for the Capstone Project Report (Format-9):
1. fig_architecture_block.png - High-Level System Architecture Block Diagram
2. fig_dfd_level0.png - Data Flow Diagram Level 0 (Context Level)
3. fig_dfd_level1.png - Data Flow Diagram Level 1 (Subsystems Level)
4. fig_call_graph.png - Sequence / Call Diagram of Telemetry & Threat Classification
5. fig_wbs_hierarchy.png - WBS Visual Tree Hierarchy
6. fig_state_machine.png - Sensor State Transition Machine
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = r"d:\DIPLOMA\SEM-VI\Project\Software\frontend\Project_Assets"
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# -------------------------------------------------------------
# 1. System Architecture Block Diagram
# -------------------------------------------------------------
def make_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 96, "K.A.R.M.A — HIGH-LEVEL SYSTEM ARCHITECTURE BLOCK DIAGRAM", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
    
    # Layer 1: Adversary / External Network
    rect_ext = patches.FancyBboxPatch((3, 68), 20, 22, boxstyle="round,pad=1.5", 
                                      ec="#ef4444", fc="#fee2e2", lw=2)
    ax.add_patch(rect_ext)
    ax.text(13, 85, "ADVERSARY &\nRECON PROBES", ha='center', va='center', fontsize=10, fontweight='bold', color='#991b1b')
    ax.text(13, 76, "• Port Scanners (Nmap)\n• SSH Brute Force\n• Web SQLi / XSS\n• Honeytoken Access", ha='center', va='center', fontsize=8, color='#7f1d1d')
    
    # Arrow to Sensors
    ax.annotate('', xy=(27, 79), xytext=(23, 79), arrowprops=dict(facecolor='#ef4444', edgecolor='#ef4444', width=2, headwidth=8))
    
    # Layer 2: Deception Sensors
    rect_sensor = patches.FancyBboxPatch((27, 45), 24, 45, boxstyle="round,pad=1.5", 
                                         ec="#3b82f6", fc="#eff6ff", lw=2)
    ax.add_patch(rect_sensor)
    ax.text(39, 85, "DECEPTION SENSORS LAYER", ha='center', va='center', fontsize=10, fontweight='bold', color='#1e40af')
    ax.text(39, 74, "SSH Sensor (Port 2222)\n• Paramiko Virtual Shell\n• RSA Key Persistence", ha='center', va='center', fontsize=8, color='#1e3a8a')
    ax.text(39, 61, "Web Decoy (Port 8080)\n• OWASP Trap Engine\n• Fake Admin Portal", ha='center', va='center', fontsize=8, color='#1e3a8a')
    ax.text(39, 49, "Raw TCP (Ports 21/23/3389)\n• FTP/Telnet/RDP Decoys\n• Honeytoken Vault (/keys)", ha='center', va='center', fontsize=8, color='#1e3a8a')

    # Arrow to Backend Event Bus
    ax.annotate('', xy=(55, 67), xytext=(51, 67), arrowprops=dict(facecolor='#3b82f6', edgecolor='#3b82f6', width=2, headwidth=8))

    # Layer 3: Core Backend & Analysis
    rect_core = patches.FancyBboxPatch((55, 30), 22, 60, boxstyle="round,pad=1.5", 
                                       ec="#8b5cf6", fc="#f5f3ff", lw=2)
    ax.add_patch(rect_core)
    ax.text(66, 85, "CORE PIPELINE & ENGINE", ha='center', va='center', fontsize=10, fontweight='bold', color='#5b21b6')
    ax.text(66, 75, "FastAPI & Uvicorn ASGI\n• Async Event Queue\n• REST Endpoints", ha='center', va='center', fontsize=8, color='#4c1d95')
    ax.text(66, 62, "MITRE ATT&CK Engine\n• Automated TTP Mapper\n• Pattern Signature Rules", ha='center', va='center', fontsize=8, color='#4c1d95')
    ax.text(66, 49, "Threat Scorer (0-100)\n• Dynamic Risk Weighting\n• Isolation Threshold (75+)", ha='center', va='center', fontsize=8, color='#4c1d95')
    ax.text(66, 36, "SQLite3 Database (WAL)\n• Event History & IP Logs\n• Active Quarantine List", ha='center', va='center', fontsize=8, color='#4c1d95')

    # Arrow to AI & Frontend
    ax.annotate('', xy=(81, 75), xytext=(77, 75), arrowprops=dict(facecolor='#10b981', edgecolor='#10b981', width=2, headwidth=8))
    ax.annotate('', xy=(81, 45), xytext=(77, 45), arrowprops=dict(facecolor='#0284c7', edgecolor='#0284c7', width=2, headwidth=8))

    # Layer 4A: DeepSeek AI Engine
    rect_ai = patches.FancyBboxPatch((81, 63), 16, 27, boxstyle="round,pad=1.5", 
                                    ec="#10b981", fc="#ecfdf5", lw=2)
    ax.add_patch(rect_ai)
    ax.text(89, 85, "DEEPSEEK AI COPILOT", ha='center', va='center', fontsize=9, fontweight='bold', color='#065f46')
    ax.text(89, 74, "• Model: deepseek-chat\n• Live Telemetry Context\n• Tier-3 SOC Reasoning\n• Phishing .EML Analyzer", ha='center', va='center', fontsize=7.5, color='#047857')

    # Layer 4B: Presentation SIEM & Launcher
    rect_ui = patches.FancyBboxPatch((81, 20), 16, 38, boxstyle="round,pad=1.5", 
                                    ec="#0284c7", fc="#f0f9ff", lw=2)
    ax.add_patch(rect_ui)
    ax.text(89, 53, "PRESENTATION LAYER", ha='center', va='center', fontsize=9, fontweight='bold', color='#075985')
    ax.text(89, 44, "• Web SIEM Dashboard\n• Leaflet World Map (ESRI)\n• Chart.js Live Graphs\n• Dual-Mode AI Chat\n• Cyber Toolkit Hasher\n• Tkinter Launcher GUI", ha='center', va='center', fontsize=7.5, color='#0369a1')

    # Active Defense Loop
    ax.annotate('Active Quarantine (HTTP 403 / Dropped)', xy=(13, 67), xytext=(55, 33),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.4", color="#dc2626", lw=2, ls='--'))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig_architecture_block.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# -------------------------------------------------------------
# 2. DFD Level 0 (Context Diagram)
# -------------------------------------------------------------
def make_dfd_level0():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 94, "FIGURE 2.3: DATA FLOW DIAGRAM (DFD LEVEL 0 — CONTEXT DIAGRAM)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # External Entity: Attacker
    rect_att = patches.Rectangle((5, 40), 18, 24, ec='#ef4444', fc='#fee2e2', lw=2)
    ax.add_patch(rect_att)
    ax.text(14, 52, "EXTERNAL ENTITY:\nCYBER ATTACKER", ha='center', va='center', fontsize=9, fontweight='bold', color='#991b1b')

    # Central Process: K.A.R.M.A Platform
    circle_p0 = patches.Circle((50, 52), 16, ec='#3b82f6', fc='#eff6ff', lw=2.5)
    ax.add_patch(circle_p0)
    ax.text(50, 55, "PROCESS 0.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#1d4ed8')
    ax.text(50, 48, "K.A.R.M.A System\nDeception & SIEM", ha='center', va='center', fontsize=8.5, color='#1e40af')

    # External Entity: Security Analyst
    rect_user = patches.Rectangle((77, 40), 18, 24, ec='#10b981', fc='#ecfdf5', lw=2)
    ax.add_patch(rect_user)
    ax.text(86, 52, "EXTERNAL ENTITY:\nSOC ANALYST", ha='center', va='center', fontsize=9, fontweight='bold', color='#065f46')

    # Arrows Attacker -> System
    ax.annotate('Attacks, Probes, Payloads', xy=(34, 56), xytext=(23, 56),
                arrowprops=dict(facecolor='#ef4444', edgecolor='#ef4444', width=1.5, headwidth=6), fontsize=8, color='#991b1b', ha='center', va='bottom')
    ax.annotate('Deceptive Responses / Banners', xy=(23, 46), xytext=(34, 46),
                arrowprops=dict(facecolor='#3b82f6', edgecolor='#3b82f6', width=1.5, headwidth=6), fontsize=8, color='#1d4ed8', ha='center', va='top')

    # Arrows System -> Analyst
    ax.annotate('Real-Time Telemetry & Alerts', xy=(77, 56), xytext=(66, 56),
                arrowprops=dict(facecolor='#10b981', edgecolor='#10b981', width=1.5, headwidth=6), fontsize=8, color='#047857', ha='center', va='bottom')
    ax.annotate('Quarantine Commands / Inquiries', xy=(66, 46), xytext=(77, 46),
                arrowprops=dict(facecolor='#8b5cf6', edgecolor='#8b5cf6', width=1.5, headwidth=6), fontsize=8, color='#6d28d9', ha='center', va='top')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig_dfd_level0.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# -------------------------------------------------------------
# 3. Call Graph / Sequence Flowchart
# -------------------------------------------------------------
def make_call_sequence():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 95, "FIGURE 3.4: END-TO-END TELEMETRY & AI COPILOT SEQUENCE FLOW", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # Lifelines
    actors = ["Attacker", "Sensors (SSH/Web)", "MITRE / Scorer", "Database", "WebSocket Bus", "DeepSeek AI", "SIEM Console"]
    xs = [10, 24, 38, 52, 66, 80, 94]
    
    for x, name in zip(xs, actors):
        # Box header
        rect = patches.FancyBboxPatch((x-6, 82), 12, 7, boxstyle="round,pad=0.5", ec="#475569", fc="#f1f5f9", lw=1.5)
        ax.add_patch(rect)
        ax.text(x, 85.5, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1e293b')
        # Dashed line
        ax.plot([x, x], [10, 82], color='#cbd5e1', linestyle='--', lw=1)

    # Step arrows
    steps = [
        (10, 24, 76, "1. Attack Probe (Port 2222/8080)", "#ef4444"),
        (24, 38, 70, "2. Emit Event Telemetry (JSON)", "#3b82f6"),
        (38, 38, 64, "3. Classify MITRE & Score (0-100)", "#8b5cf6"),
        (38, 52, 58, "4. Persist Record (SQLite WAL)", "#64748b"),
        (38, 66, 52, "5. Broadcast Event Packet", "#0284c7"),
        (66, 94, 46, "6. Real-Time Stream to Client", "#0284c7"),
        (94, 80, 38, "7. Operator Query AI Copilot", "#10b981"),
        (80, 52, 32, "8. Ingest Live SIEM DB Snapshot", "#64748b"),
        (80, 94, 24, "9. Render SOC Analysis & Playbook", "#10b981"),
        (38, 10, 16, "10. Active Quarantine Block (HTTP 403)", "#dc2626")
    ]

    for x1, x2, y, label, col in steps:
        if x1 == x2:
            # Self call
            ax.annotate('', xy=(x1+3, y-2), xytext=(x1, y),
                        arrowprops=dict(facecolor=col, edgecolor=col, width=1, headwidth=5))
            ax.text(x1+4, y-1, label, fontsize=7, color=col, va='center')
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(facecolor=col, edgecolor=col, width=1.2, headwidth=6))
            mid_x = (x1 + x2) / 2
            ax.text(mid_x, y + 1.8, label, fontsize=7.5, color=col, ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig_call_graph.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# -------------------------------------------------------------
# 4. WBS Hierarchy Tree
# -------------------------------------------------------------
def make_wbs_diagram():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 95, "FIGURE 2.1: WORK BREAKDOWN STRUCTURE (WBS) HIERARCHICAL TREE", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # Root
    rect_root = patches.FancyBboxPatch((35, 78), 30, 10, boxstyle="round,pad=1", ec="#1e3a8a", fc="#dbeafe", lw=2)
    ax.add_patch(rect_root)
    ax.text(50, 83, "K.A.R.M.A PLATFORM (1.0)\nDeception & SIEM System", ha='center', va='center', fontsize=9, fontweight='bold', color='#1e3a8a')

    # Level 2 nodes
    l2_nodes = [
        ("WP 1.0: Planning &\nArchitecture", 12, "#e0e7ff", "#3730a3"),
        ("WP 2.0: Backend &\nDatabase Layer", 27, "#ede9fe", "#5b21b6"),
        ("WP 3.0: Honeypot &\nDecoy Sensors", 42, "#fce7f3", "#9d174d"),
        ("WP 4.0: MITRE &\nActive Defense", 58, "#fee2e2", "#991b1b"),
        ("WP 5.0: AI Copilot &\nCyber Toolkit", 73, "#ecfdf5", "#065f46"),
        ("WP 6.0: Frontend SIEM\n& Testing", 88, "#e0f2fe", "#075985")
    ]

    for title, x, fc, tc in l2_nodes:
        # Arrow from root
        ax.plot([50, 50, x, x], [78, 68, 68, 56], color='#64748b', lw=1.5)
        rect = patches.FancyBboxPatch((x-6.5, 44), 13, 12, boxstyle="round,pad=0.8", ec=tc, fc=fc, lw=1.5)
        ax.add_patch(rect)
        ax.text(x, 50, title, ha='center', va='center', fontsize=7.5, fontweight='bold', color=tc)

    # Sample sub-tasks below
    tasks = [
        (12, ["• Scope (F1)", "• WBS (F2)", "• Schedule (F3)"]),
        (27, ["• SQLite Schema", "• FastAPI Engine", "• WS Gateway"]),
        (42, ["• SSH Honeypot", "• Web Decoy", "• Raw TCP Traps"]),
        (58, ["• TTP Rules", "• Threat Scorer", "• IP Quarantine"]),
        (73, ["• DeepSeek API", "• EML Forensics", "• Zero-Storage"]),
        (88, ["• Leaflet Map", "• Chart.js Trends", "• 10 Test Cases"])
    ]

    for x, sub in tasks:
        ax.plot([x, x], [44, 34], color='#94a3b8', lw=1, linestyle=':')
        rect_sub = patches.Rectangle((x-6.5, 16), 13, 18, ec='#cbd5e1', fc='#f8fafc', lw=1)
        ax.add_patch(rect_sub)
        y_text = 30
        for s in sub:
            ax.text(x-5.5, y_text, s, fontsize=6.8, color='#334155')
            y_text -= 5

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig_wbs_hierarchy.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

if __name__ == "__main__":
    make_architecture_diagram()
    make_dfd_level0()
    make_call_sequence()
    make_wbs_diagram()
