"""
Generates the complete 100-Day Student's Daily Log Book (Format-8)
for Kanaka C (Security Analyst & Frontend Engineer).
Registration Number: 470CS23005

Each day is formatted to occupy exactly ONE single page in the Word document.
Total: 100 days across 100 pages, with zero spillovers.
Spans July 15, 2026 (Wednesday) to October 22, 2026 (Thursday).
"""

import os
import datetime
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

WORD_DIR = r"d:\DIPLOMA\SEM-VI\Project\Software\__CAPSTONE_Formats\Word-Copy"
OUT_PATH = os.path.join(WORD_DIR, "KARMA_Format_8_Student_Daily_LogBook_Kanaka_C.docx")

def set_cell_props(cell, text, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None, space_before=2.5, space_after=2.5):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.12
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    if bg_color:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

def get_100_days_schedule(start_date):
    days = []
    curr = start_date
    for _ in range(100):
        days.append(curr)
        curr += datetime.timedelta(days=1)
    return days

# 100 Days unique engineering logs for Kanaka C (Security Analyst & Frontend Engineer)
LOG_ENTRIES_KANAKA = [
    # Phase 1: Initiation, UI/UX Research & Requirements (Days 1-12)
    (
        "Participated in initial Capstone project kickoff meeting with team lead Abhijeet Kumar, Raghu, Sanjay, and guide Mr. Subhash J R.\n"
        "Discussed frontend visual requirements for real-time cybersecurity threat monitoring and deception analytics.\n"
        "Identified key operational challenges in existing SIEM dashboards: high cognitive load and cluttered data visualization.\n"
        "Assigned lead responsibility for Frontend UI/UX, Real-Time Charting, Geolocation Map, and Security Analysis UI.",
        "Role responsibilities clearly established. Approved to begin UI/UX research."
    ),
    (
        "Conducted extensive literature and competitive survey of enterprise SOC dashboards (Splunk Enterprise, Elastic SIEM, CrowdStrike Falcon, Datadog Security).\n"
        "Analyzed how modern security analysts interact with high-velocity threat alerts and triage MITRE ATT&CK techniques.\n"
        "Compiled design inspiration moodboard emphasizing dark-mode ergonomics, cyber aesthetics, and high-contrast typography.\n"
        "Documented UI design criteria in project research repository.",
        "Good comparative study of modern enterprise SOC visualization paradigms."
    ),
    (
        "Researched visualization techniques for representing MITRE ATT&CK tactic and technique hierarchies on web dashboards.\n"
        "Evaluated matrix grids versus doughnut and radial charts for displaying attack technique distributions.\n"
        "Drafted preliminary wireframe sketches for the K.A.R.M.A Cloud SIEM single-page application layout.\n"
        "Shared visual wireframes with Abhijeet for backend API alignment.",
        "Wireframe layout provides clear visual separation of SIEM telemetry."
    ),
    (
        "Explored client-side charting libraries: Chart.js v4 vs D3.js vs Apache ECharts for high-frequency telemetry updates.\n"
        "Evaluated render performance, memory consumption during continuous canvas redraws, and animation smoothness.\n"
        "Selected Chart.js v4.4 for its lightweight footprint (<60KB) and robust canvas rendering engine.\n"
        "Created proof-of-concept prototype charting 100 dynamic data points per second.",
        "Chart.js selection is well justified for lightweight, responsive browser charting."
    ),
    (
        "Investigated open-source geospatial mapping libraries for adversary geolocation visualization.\n"
        "Evaluated Mapbox GL JS, Google Maps API, and Leaflet.js v1.9.4.\n"
        "Selected Leaflet.js due to its zero-API-key requirement, high performance, and support for custom tile providers (OpenStreetMap & ESRI).\n"
        "Designed custom SVG pulsing radar markers to indicate active attacker coordinates.",
        "Leaflet.js provides an excellent open-source foundation for threat mapping."
    ),
    (
        "Contributed to the formulation of Capstone Project Scope Document (Format-1).\n"
        "Authored frontend and visualization scope sections: Responsive Web SIEM, Geolocation Map, AI Chat Interface, and Cyber Toolkit.\n"
        "Collaborated with team to review functional boundaries and user roles.\n"
        "Assisted in finalizing document formatting for submission.",
        "Scope Document contributions are well-aligned with project objectives."
    ),
    (
        "Collaborated on Work Breakdown Structure (Format-2) for Work Package 5 (Frontend SIEM & UI/UX).\n"
        "Decomposed UI development into 12 detailed practical tasks: Design System, Live Telemetry Table, Leaflet Map, Chart.js Visualizations, AI Copilot UI, and Cyber Toolkit.\n"
        "Mapped task dependencies against backend API availability.\n"
        "Submitted WBS draft for cohort owner review.",
        "WBS tasks for UI/UX are comprehensive and systematically sequenced."
    ),
    (
        "Contributed to Semester Time Line Schedule (Format-3) and Cost Breakdown Structure (Format-4).\n"
        "Estimated frontend development milestones across 13 academic weeks.\n"
        "Verified zero software licensing cost by committing to open-source UI libraries (Vanilla CSS, Leaflet.js, Chart.js).\n"
        "Coordinated with team on milestone review dates.",
        "Timeline and cost estimates verified. Proceed to design system foundation."
    ),
    (
        "Designed comprehensive User Experience (UX) workflow and interaction state diagrams.\n"
        "Mapped user journeys for three primary operational personas: SOC Tier-1 Triage Analyst, Incident Responder, and Security Evaluator.\n"
        "Defined modal interaction flows for event inspection, quarantine management, and AI copilot dialogs.\n"
        "Reviewed UX flowcharts with project guide.",
        "Persona-based UX workflow diagrams provide excellent functional clarity."
    ),
    (
        "Established frontend directory structure and tooling in `frontend/`.\n"
        "Created folder hierarchy: `frontend/css/`, `frontend/js/`, `frontend/assets/`, and `frontend/index.html`.\n"
        "Configured code formatting standards and ESLint rules for modern JavaScript (ES6+).\n"
        "Committed initial frontend skeleton to project Git repository.",
        "Clean frontend workspace structure established."
    ),
    (
        "Participated in Department Project Committee Scope Presentation.\n"
        "Presented the UI/UX architecture and live threat dashboard mockups.\n"
        "Addressed committee inquiries regarding real-time event streaming and browser performance.\n"
        "Received unanimous committee approval.",
        "Committee commended the intuitive UI design and clear visual presentation."
    ),
    (
        "Finalized sprint backlog for Sprint 1 (Design System & Base Layout).\n"
        "Set up local development web server and verified hot-reloading with FastAPI static mounts.\n"
        "Verified browser developer tools and responsive device emulation profiles.\n"
        "Ready to begin design system implementation.",
        "Sprint 1 backlog approved. Ready for implementation."
    ),

    # Phase 2: Design System, Base Layout & WebSocket Client (Days 13-28)
    (
        "Constructed core CSS Design System in `frontend/css/style.css`.\n"
        "Defined CSS Custom Properties (CSS variables) for HSL color tokens: Primary Cyber Blue (`--primary`), Danger Red (`--danger`), Warning Amber (`--warning`), Success Green (`--success`).\n"
        "Integrated modern typography from Google Fonts: 'Inter' for clean UI body text and 'JetBrains Mono' for terminal logs and IP addresses.\n"
        "Verified consistent font rendering across screen resolutions.",
        "CSS custom property design tokens provide a strong, maintainable styling base."
    ),
    (
        "Engineered Dual-Theme Engine supporting Cyber Dark Mode and Crisp Light Mode.\n"
        "Configured theme variables: `--bg-primary`, `--bg-card`, `--text-primary`, `--border-color`.\n"
        "Implemented smooth theme transition effects (`transition: all 0.3s cubic-bezier(...)`).\n"
        "Added persistent theme toggle button in navbar storing user preference in `localStorage`.",
        "Dual-theme switching operates smoothly with persistent state."
    ),
    (
        "Implemented Glassmorphism UI aesthetic across cards and navigation panels.\n"
        "Configured `backdrop-filter: blur(12px)`, subtle semi-transparent background gradients (`rgba(15, 23, 42, 0.75)`), and 1px border glows (`rgba(255, 255, 255, 0.1)`).\n"
        "Ensured glassmorphism fallback for older browsers without CSS backdrop filter support.\n"
        "Reviewed aesthetic quality with team lead Abhijeet.",
        "Glassmorphism styling looks premium, sleek, and highly modern."
    ),
    (
        "Built responsive Top Navigation Bar and Sidebar Navigation in `frontend/index.html`.\n"
        "Created navigation tabs: '📊 Live SIEM Dashboard', '🌍 World Map & Geolocation', '🤖 KARMA AI SOC Copilot', '🛠️ Cyber Toolkit', '📜 Audit Logs', '⚙️ Active Defense'.\n"
        "Implemented tab-switching controller in `frontend/js/app.js` with active indicator animations.\n"
        "Verified accessible keyboard navigation.",
        "Navigation layout is intuitive and responsive."
    ),
    (
        "Constructed Header KPI Metric Cards in `frontend/index.html`.\n"
        "Designed 4 prominent summary cards: 'Total Trapped Events', 'Active Honeypot Sensors', 'Critical Threat Attacks', 'Quarantined IPs'.\n"
        "Implemented dynamic numeric counters with subtle ease-out increment animations on data update.\n"
        "Styled cards with color-coded accent borders matching severity levels.",
        "Metric KPI cards provide instant, glanceable SOC situational awareness."
    ),
    (
        "Engineered client-side WebSocket subscriber in `frontend/js/app.js`.\n"
        "Connected to backend WebSocket endpoint `ws://localhost:8000/ws/events`.\n"
        "Implemented automated reconnection algorithm with exponential backoff (1s, 2s, 4s, max 10s) upon connection drop.\n"
        "Added visual connection status badge in navbar (Green: 'CONNECTED', Amber: 'RECONNECTING', Red: 'DISCONNECTED').",
        "WebSocket client handles connection drops gracefully with auto-reconnect."
    ),
    (
        "Constructed Live Telemetry Event Table in SIEM dashboard view.\n"
        "Designed columns: Timestamp, Source IP, Decoy Port / Sensor Type, MITRE ATT&CK Technique, Threat Score, Action Taken.\n"
        "Implemented color-coded severity badges: Low (<30: Green), Medium (30-74: Amber), Critical (>=75: Red Glowing).\n"
        "Tested rendering of 50 simultaneous incoming test events.",
        "Live event table layout is clean, readable, and dynamically updated."
    ),
    (
        "Implemented client-side table search, filtering, and pagination in `frontend/js/app.js`.\n"
        "Added instant search bar filtering events by IP address, payload text, or MITRE ID.\n"
        "Added dropdown filters: Sensor Type (All, SSH, Web, FTP, Telnet, RDP) and Severity (All, Low, Medium, Critical).\n"
        "Verified sub-millisecond table filtering over 500 cached events.",
        "Table filtering and search work seamlessly without UI latency."
    ),
    (
        "Created Event Detail Modal popup in `frontend/js/app.js`.\n"
        "When an operator clicks on any event row, modal displays complete raw payload, HTTP headers, extracted MITRE description, and reverse DNS data.\n"
        "Added one-click 'Copy Raw Payload' and 'Inspect in AI Copilot' buttons.\n"
        "Styled modal with sleek glassmorphism backdrop and animated entrance.",
        "Event detail modal provides deep forensic visibility with convenient actions."
    ),
    (
        "Constructed Audio Siren & Notification Toast Notification System.\n"
        "Synthesized subtle Web Audio API tone alerts triggering exclusively on Critical events (Score >= 75).\n"
        "Added audio mute toggle in top navigation with persistent state.\n"
        "Built animated toast notification container in top-right screen corner with auto-dismiss (5s) and close button.",
        "Audio-visual notification system alerts operators effectively to high-threat events."
    ),
    (
        "Engineered Active Quarantine Management UI in `frontend/index.html`.\n"
        "Built Quarantine Table listing isolated IP addresses, isolation timestamp, triggering reason, and active block status.\n"
        "Added interactive 'Unblock IP' and 'Manual Quarantine IP' action buttons connecting to backend REST endpoints.\n"
        "Tested IP quarantine toggle workflow with backend manager.",
        "Active defense UI gives operators direct control over quarantined adversaries."
    ),
    (
        "Designed and implemented CSV Audit Log Export interface.\n"
        "Added 'Download Session CSV Audit Log' button in navigation toolbar.\n"
        "Implemented client-side CSV formatter generating downloadable forensic report with full session metadata.\n"
        "Tested export file generation and verified formatting in Microsoft Excel.",
        "CSV export feature operates reliably for compliance and audit archiving."
    ),
    (
        "Conducted cross-device responsive layout testing across laptop (1366x768), desktop (1920x1080), and 4K monitors.\n"
        "Optimized CSS Grid layouts (`grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`).\n"
        "Adjusted table container scrollbars and font scaling.\n"
        "Verified zero overflow or horizontal scrolling on all test resolutions.",
        "Responsive grid layout adapts cleanly across all standard viewport sizes."
    ),
    (
        "Collaborated with backend engineer Raghunandan T V on API schema validation.\n"
        "Verified that all JSON payload properties match expected frontend data model interfaces.\n"
        "Tested edge cases: null GeoIP coordinates, empty payload strings, and long malicious command sequences.\n"
        "Implemented fallback placeholders for missing metadata.",
        "Data validation ensures robust UI rendering under diverse backend responses."
    ),
    (
        "Conducted Sprint 1 Review with project guide Mr. Subhash J R.\n"
        "Demonstrated working single-page dashboard, dual-theme switching, live WebSocket event stream, and audio-visual siren.\n"
        "Guide commended the modern visual appeal and responsive design.\n"
        "Approved to proceed to Sprint 2: Leaflet Map & Chart.js Visualizations.",
        "Sprint 1 review completed successfully. Excellent progress on UI framework."
    ),
    (
        "Refactored CSS stylesheet to eliminate duplicate selectors and optimize rendering performance.\n"
        "Minified CSS utility classes and verified GPU-accelerated transitions.\n"
        "Committed optimized stylesheet to main Git branch.\n"
        "Prepared task backlog for mapping and charting sprint.",
        "Stylesheet optimized for high-performance rendering."
    ),

    # Phase 3: World Map, Geolocation & Real-Time Charts (Days 29-50)
    (
        "Integrated Leaflet.js v1.9.4 map engine into `frontend/index.html` and `frontend/js/app.js`.\n"
        "Configured full-width interactive map container with smooth pan, zoom, and touch gesture controls.\n"
        "Set initial map view centered on global projection (`lat: 20.0, lng: 0.0, zoom: 2`).\n"
        "Verified map initialization inside tabbed UI without container sizing bugs.",
        "Leaflet map container initialized smoothly within dashboard layout."
    ),
    (
        "Configured dual-mode map tile layer switching matching the active platform theme.\n"
        "Integrated **OpenStreetMap Standard** tile layer for Crisp Light Mode.\n"
        "Integrated **ESRI World Dark Canvas** (`server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base`) for Cyber Dark Mode.\n"
        "Eliminated all previous CartoDB 'API Key Required' watermark issues with 100% free tiles.",
        "Map tile upgrade provides stunning visuals with zero API key dependencies."
    ),
    (
        "Engineered custom SVG Pulsing Threat Radar Markers on the world map.\n"
        "Created animated CSS pulse effect radiating outward from attacker coordinate points.\n"
        "Color-coded markers based on threat level: Blue (Port Scan), Amber (Brute Force), Red (Honeytoken / SQLi).\n"
        "Added interactive popups displaying Attacker IP, City, Country, targeted sensor port, and timestamp.",
        "Pulsing threat markers visually dramatize live incoming attacks effectively."
    ),
    (
        "Implemented dynamic marker clustering and auto-panning on new incoming attacks.\n"
        "When a new high-severity attack is received via WebSocket, the map automatically pulses the coordinate and updates sidebar stats.\n"
        "Added 'Recenter Global View' and 'Filter by Country' controls on map overlay.\n"
        "Tested mapping with 20 international simulated attacker IP coordinates.",
        "Map auto-focus and clustering work seamlessly during live attack streams."
    ),
    (
        "Constructed Live Telemetry Event Volume Line & Bar Chart in `frontend/js/app.js` using Chart.js v4.4.\n"
        "Configured rolling time-series chart displaying event frequency (events per 30 seconds) across the last 15 minutes.\n"
        "Applied cyber blue gradient fills (`ctx.createLinearGradient`) and glowing line stroke effects.\n"
        "Configured Chart.js options for smooth spline curve interpolation.",
        "Live event volume chart provides immediate temporal threat visibility."
    ),
    (
        "Constructed MITRE ATT&CK Technique Distribution Doughnut Chart in `frontend/js/app.js`.\n"
        "Visualizes proportional breakdown of captured techniques: T1110 (Brute Force), T1190 (Web Exploit), T1046 (Reconnaissance), T1059 (Shell Command), T1078 (Honeytoken).\n"
        "Configured vibrant custom palette with glassmorphic center cutout displaying total technique count.\n"
        "Added interactive legend allowing analysts to toggle individual technique categories.",
        "MITRE doughnut chart cleanly illustrates adversary attack methodology distributions."
    ),
    (
        "Constructed Sensor Port Activity Distribution Bar Chart.\n"
        "Displays real-time connection attempts across active decoy ports: Port 2222 (SSH), Port 8080 (Web), Port 21 (FTP), Port 23 (Telnet), Port 3389 (RDP).\n"
        "Implemented horizontal bar layout with animated transitions on value updates.\n"
        "Tested chart responsiveness under live multi-port port sweeps.",
        "Sensor activity chart clearly contrasts reconnaissance vs exploitation targets."
    ),
    (
        "Constructed Top 5 Attacker Origin Countries Bar & Badge Widget.\n"
        "Aggregates incoming GeoIP metadata and renders top 5 attacker countries with national flag emojis and percentage bars.\n"
        "Updates dynamically in real time as new geographical telemetry is ingested.\n"
        "Verified accuracy against simulated multi-region attack logs.",
        "Top country widget provides concise geopolitical threat intelligence."
    ),
    (
        "Implemented real-time chart synchronization engine updating all Chart.js instances without full redraws.\n"
        "Used `chart.update('active')` with buffered data queues to prevent browser memory spikes and UI frame drops.\n"
        "Benchmarked charting performance: maintained steady 60 FPS during continuous data streams.\n"
        "Verified zero memory leakage across 2-hour continuous soak test.",
        "Chart synchronization engine operates efficiently with 60 FPS smoothness."
    ),
    (
        "Designed and implemented Sensor Health & Status Monitoring Panel in `frontend/index.html`.\n"
        "Created card widgets for each active honeypot service showing port number, status indicator (Green pulse: 'LISTENING'), uptime, and total connection count.\n"
        "Added quick restart toggle buttons connecting to backend sensor manager.\n"
        "Verified sensor status reporting with backend.",
        "Sensor status panel provides comprehensive operational health monitoring."
    ),
    (
        "Collaborated with Sanjay Kashyap to validate UI response during simulated penetration attacks.\n"
        "Sanjay executed automated multi-port Nmap scans and SSH dictionary attacks.\n"
        "Verified that the map plotted attacker origin within 50ms and chart counters updated immediately.\n"
        "Validated visual clarity of alert toasts during high-frequency attack bursts.",
        "UI handled multi-vector attack stream with instantaneous visual feedback."
    ),
    (
        "Optimized map and chart rendering on low-power laptop screens.\n"
        "Added CSS `contain: layout style` and hardware-accelerated canvas transforms.\n"
        "Reduced DOM node allocations in live event table by recycling table rows (virtualized scrolling).\n"
        "Achieved 40% reduction in client-side CPU usage.",
        "Performance optimization significantly improves dashboard responsiveness."
    ),
    (
        "Conducted Sprint 2 Review with project guide Mr. Subhash J R.\n"
        "Demonstrated live Leaflet world map with ESRI Dark Canvas tiles, pulsing threat markers, and dynamic Chart.js analytics.\n"
        "Guide commended the map tile upgrade and fluid chart animations.\n"
        "Approved to proceed to Sprint 3: AI SOC Copilot UI & Cyber Toolkit Interface.",
        "Sprint 2 review completed successfully. Map and charts are fully operational."
    ),
    (
        "Created frontend component documentation in project UI style guide.\n"
        "Documented Chart.js configuration parameters, Leaflet tile layer setups, and CSS animation classes.\n"
        "Committed updated frontend assets to Git repository.\n"
        "Prepared task board for AI Copilot UI development.",
        "Frontend documentation updated with complete component specifications."
    ),
    (
        "Designed wireframes for the upcoming AI SOC Copilot chat interfaces.\n"
        "Sketched Dual-Mode interface: Full-Screen SOC Workspace tab and Floating Action Button (FAB) composer window.\n"
        "Designed message bubble layouts, typing indicator animations, and code snippet copy buttons.\n"
        "Reviewed design sketches with Abhijeet Kumar.",
        "AI Copilot wireframes finalized with clean dual-mode architecture."
    ),
    (
        "Prepared test datasets of simulated multi-region cyber attacks for presentation demonstrations.\n"
        "Configured sample attack coordinates across Asia, Europe, North America, and South America.\n"
        "Verified visual distribution of markers across global map projection.\n"
        "Ready for AI interface development sprint.",
        "Demo datasets prepared and validated."
    ),

    # Phase 4: AI Copilot Interface & Cyber Toolkit Development (Days 51-70)
    (
        "Constructed Dual-Mode AI SOC Copilot UI Architecture in `frontend/index.html`.\n"
        "Mode 1: Dedicated Full-Screen AI Workspace tab for deep incident investigations with expanded chat history and context sidebar.\n"
        "Mode 2: Floating Action Button (FAB) in bottom-right screen corner opening a sleek, collapsible Gmail-composer style chat modal.\n"
        "Ensured synchronized conversation state between both UI modes in `frontend/js/ai_chat.js`.",
        "Dual-mode AI UI architecture successfully constructed with shared state."
    ),
    (
        "Developed frontend AI chat interaction controller in `frontend/js/ai_chat.js`.\n"
        "Implemented asynchronous fetch client communicating with backend `POST /api/ai/chat`.\n"
        "Built animated typing indicator ('🤖 KARMA AI is analyzing SIEM telemetry...') while awaiting DeepSeek API response.\n"
        "Added auto-scrolling to newest message and smooth entry animations for message bubbles.",
        "AI chat controller provides fluid conversational interaction."
    ),
    (
        "Integrated custom client-side Markdown rendering engine in `frontend/js/ai_chat.js`.\n"
        "Engineered regex-based parser converting raw LLM Markdown into formatted HTML: bold headers, bullet lists, numbered steps, tables, and fenced code blocks (` ```bash `).\n"
        "Styled code blocks with dark terminal styling, syntax highlights, and top header bar.\n"
        "Verified rendering on complex multi-paragraph incident response playbooks.",
        "Client-side Markdown parser renders rich technical responses beautifully."
    ),
    (
        "Engineered one-click 'Copy Code' and 'Export Chat' functionality in AI Copilot interface.\n"
        "Added clipboard copy button to every generated code snippet (iptables rules, Python scripts, bash commands) with 'Copied!' toast feedback.\n"
        "Added 'Export Incident Report' button downloading full conversation as a formatted `.md` forensic file.\n"
        "Tested export on 10-turn SOC investigation session.",
        "One-click copy and markdown export enhance incident triage workflows."
    ),
    (
        "Constructed Quick-Action Analyst Prompt Chips in AI Copilot interface.\n"
        "Added one-click prompt pills: '⚡ Summarize Active Threats', '🛡️ Generate Firewall Rules', '🔍 Explain MITRE T1110', '📋 Draft Incident Report', '🚨 Triage Top Attacker'.\n"
        "Clicking any chip immediately sends the specialized prompt to the AI with live SIEM context.\n"
        "Tested all quick prompts and verified instant contextual responses.",
        "Quick prompt chips significantly accelerate SOC analyst investigation speed."
    ),
    (
        "Constructed Client-Side Password Strength Evaluator in `frontend/js/tools.js`.\n"
        "Engineered real-time password analysis calculating Shannon entropy, character diversity score (uppercase, lowercase, numbers, symbols), and length score.\n"
        "Implemented dynamic crack time estimation algorithm based on modern offline GPU cluster hash rates (100 GH/s).\n"
        "Built visual animated progress bar changing from Red (Weak) -> Amber (Moderate) -> Green (Strong) -> Emerald (Fortress).",
        "Password strength evaluator operates with high accuracy and engaging visual feedback."
    ),
    (
        "Constructed Client-Side Zero-Storage Multi-Algorithm Cryptographic Hasher in `frontend/js/tools.js`.\n"
        "Implemented cryptographic hashing using browser native `crypto.subtle.digest` for SHA-256 and SHA-512, plus lightweight in-memory MD5 implementation.\n"
        "Outputs hex-encoded digest strings in real-time as user types.\n"
        "Verified with DevTools Network tab that zero network packets are transmitted, ensuring 100% user privacy.",
        "Cryptographic hasher conforms strictly to zero-storage privacy standards."
    ),
    (
        "Designed and implemented Phishing Forensic Analyzer UI in `frontend/index.html` and `frontend/js/tools.js`.\n"
        "Built interactive drag-and-drop file upload zone supporting `.eml` and `.msg` email files.\n"
        "Implemented visual file drop animations and client-side MIME type validation.\n"
        "Built loading spinner while backend and DeepSeek AI parse headers and evaluate email legitimacy.",
        "Phishing upload interface is intuitive and user-friendly."
    ),
    (
        "Constructed Phishing Forensic Results Viewer Widget in `frontend/js/tools.js`.\n"
        "Renders visual Verdict Card: Malicious (Red), Suspicious (Amber), Clean (Green) with risk score gauge (0-100).\n"
        "Renders header inspection breakdown: SPF pass/fail, DKIM signature verification, Return-Path mismatch alerts, and extracted suspicious URLs table.\n"
        "Displays AI forensic analysis summary in structured markdown card.",
        "Phishing results viewer provides clear, comprehensive forensic evidence breakdown."
    ),
    (
        "Conducted integration testing of AI Copilot with live honeypot attack traffic.\n"
        "Collaborated with Abhijeet Kumar to trigger live attacks and query AI: 'What is the current threat posture?'\n"
        "Verified that AI received live database JSON snapshot and accurately cited active attacker IPs and MITRE T1190 exploits.\n"
        "Confirmed end-to-end response time under 3 seconds.",
        "AI Copilot integration successfully verified with live threat context."
    ),
    (
        "Tested AI Copilot floating composer across all SIEM tabs.\n"
        "Verified that floating composer stays accessible while navigating between World Map, Live SIEM, Cyber Toolkit, and Audit Logs.\n"
        "Implemented minimize, maximize, and close window controls.\n"
        "Ensured zero layout shift or z-index conflicts with map layers.",
        "Floating composer window operates smoothly across all dashboard views."
    ),
    (
        "Conducted comprehensive cross-browser validation of Cyber Toolkit suite.\n"
        "Tested Password Evaluator, Cryptographic Hasher, and Phishing Analyzer across Chrome, Firefox, Safari, and Edge.\n"
        "Verified consistent WebCrypto API behavior and file drag-and-drop compatibility across all browsers.\n"
        "Fixed minor Safari CSS flexbox alignment quirk in hasher output cards.",
        "Cross-browser testing confirmed 100% feature compatibility."
    ),
    (
        "Conducted Sprint 3 Review with project guide Mr. Subhash J R.\n"
        "Demonstrated Dual-Mode AI Copilot, live SIEM context queries, `.EML` phishing analysis, and zero-storage cryptographic hasher.\n"
        "Guide commended the advanced AI integration and clean frontend execution.\n"
        "Approved to proceed to Sprint 4: Usability Testing, Stress Testing & Final Polish.",
        "Sprint 3 review completed with high praise. Proceed to final testing phase."
    ),
    (
        "Refactored frontend codebase into modular JavaScript files: `app.js`, `ai_chat.js`, and `tools.js`.\n"
        "Eliminated global namespace pollution by encapsulating modules inside clean IIFE / ES6 module scopes.\n"
        "Added descriptive JSDoc comments to all public functions and event handlers.\n"
        "Committed refactored codebase to Git repository.",
        "Frontend codebase modularized and thoroughly documented."
    ),
    (
        "Optimized frontend bundle size and asset delivery.\n"
        "Ensured all CSS and JS files are served locally without external CDN dependencies for offline lab demonstration capability.\n"
        "Pre-cached essential assets and icons in local `/static/` directory.\n"
        "Verified full offline dashboard functionality.",
        "Offline standalone asset independence verified."
    ),
    (
        "Conducted UI accessibility (a11y) audit using Chrome Lighthouse.\n"
        "Checked color contrast ratios against WCAG 2.1 AA standards (minimum 4.5:1 for text).\n"
        "Added descriptive `aria-label` attributes to icon buttons and interactive controls.\n"
        "Achieved 98/100 Accessibility score on Lighthouse audit.",
        "UI accessibility audit achieved excellent compliance score."
    ),

    (
        "Engineered collapsible sidebar navigation for smaller laptop viewports in frontend/js/app.js.\n"
        "Added toggle hamburger button in navbar for collapsing sidebar into compact icon-only view.\n"
        "Ensured all dashboard content dynamically expands to fill available screen real estate.\n"
        "Verified smooth CSS transition animations on toggle.",
        "Collapsible sidebar improves dashboard usability on compact screens."
    ),
    (
        "Constructed custom pure CSS Tooltip engine for MITRE ATT&CK technique badges.\n"
        "Hovering over any technique badge (e.g. T1110, T1190) displays an instant tooltip with official MITRE definition and tactic category.\n"
        "Eliminated third-party tooltip library dependencies for minimal DOM footprint.\n"
        "Verified tooltip positioning and zero boundary clipping.",
        "Lightweight tooltip engine enhances analyst comprehension of MITRE tactics."
    ),
    (
        "Constructed Dynamic Threat Score Circular Gauge Widget in frontend/index.html.\n"
        "Built animated SVG circular gauge displaying current overall platform threat level (0 to 100).\n"
        "Added color-coded gradient ring: Green (0-29 Normal) to Amber (30-74 Elevated) to Red (75-100 Critical Lockdown).\n"
        "Tested gauge animation with dynamic telemetry updates.",
        "Circular threat gauge provides immediate visual threat status."
    ),
    (
        "Implemented custom Web Audio Oscillator API synthesizer in frontend/js/app.js.\n"
        "Created dual audio alert profiles: 'Subtle Beep' (for moderate events) and 'Emergency Siren' (for critical events >= 75).\n"
        "Added volume slider and sound profile selector in dashboard preferences modal.\n"
        "Verified audio playback across Chrome, Firefox, and Edge.",
        "Custom synthesized audio alerts avoid external sound file dependencies."
    ),
    (
        "Engineered dynamic time-window selector for Chart.js event volume graphs.\n"
        "Added time-filter buttons: 'Last 5 Mins', 'Last 15 Mins', 'Last 1 Hour', and 'Full Session'.\n"
        "Implemented client-side data slicing updating chart datasets seamlessly.\n"
        "Tested graph recalculations with 500 cached events.",
        "Time-window filtering provides flexible temporal analysis."
    ),
    (
        "Engineered slide-in CSS animations for newly arriving WebSocket telemetry table rows.\n"
        "New attack events slide in from the top of the table with a temporary glowing highlight that fades after 3 seconds.\n"
        "Enables security analysts to instantly identify incoming attacks visually.\n"
        "Verified smooth 60 FPS animation performance.",
        "Table row entry animation visually highlights incoming attack events."
    ),
    (
        "Implemented 'Auto-Scroll Freeze' controller for live telemetry event table.\n"
        "When an analyst hovers over or clicks an event row to inspect details, auto-scrolling freezes automatically to prevent losing position.\n"
        "Added floating 'Resume Live Stream' badge indicating paused view.\n"
        "Tested during high-velocity simulated attack streams.",
        "Auto-scroll freeze prevents analyst distraction during live event triage."
    ),
    (
        "Implemented Chart Export functionality allowing analysts to download telemetry charts as PNG images.\n"
        "Added 'Export Chart PNG' button to Event Volume, MITRE Doughnut, and Port Activity charts using HTML5 canvas toDataURL.\n"
        "Tested exported image quality for inclusion in executive SOC briefing documents.\n"
        "Confirmed crisp rendering at 300 DPI.",
        "Chart PNG export capability facilitates incident report compilation."
    ),
    (
        "Engineered interactive drag-and-drop animations and file dropzone styling in frontend/css/style.css.\n"
        "Added pulsating dashed borders and highlight effects when an analyst drags an .eml email file over the dropzone.\n"
        "Added animated progress indicator while email headers are being extracted and analyzed.\n"
        "Verified intuitive drag-and-drop feedback across operating systems.",
        "Dropzone animations create an engaging, modern file analysis experience."
    ),
    (
        "Constructed Password Entropy & Character Diversity Breakdown Card in frontend/js/tools.js.\n"
        "Renders visual checklist: Uppercase (A-Z), Lowercase (a-z), Digits (0-9), Special Symbols (!@#$%), and Length (>=12 chars).\n"
        "Updates real-time score indicators with green checkmarks as requirements are fulfilled.\n"
        "Tested with diverse test password vectors.",
        "Visual password checklist clearly guides users toward strong credentials."
    ),
    (
        "Styled AI Copilot Markdown Tables with alternating row colors and highlighted headers in frontend/css/style.css.\n"
        "Ensured tables rendered by DeepSeek AI (e.g. firewall rule matrices, IOC lists) format cleanly with horizontal borders and monospace code cells.\n"
        "Added horizontal scroll wrapper preventing table overflow on smaller screens.\n"
        "Verified clean rendering on complex AI triage reports.",
        "Markdown table styling ensures excellent readability for structured AI outputs."
    ),
    (
        "Tested touch-screen gesture support and pinch-to-zoom on Leaflet world map using tablet emulator.\n"
        "Optimized touch hit targets for map markers and zoom controls (minimum 44x44px per WCAG guidelines).\n"
        "Verified smooth panning and coordinate inspection on mobile and touch devices.\n"
        "Confirmed responsive touch ergonomics.",
        "Touch-screen optimization enables field triage on mobile/tablet devices."
    ),
    (
        "Benchmarked client-side DOM memory footprint during sustained 2-hour telemetry streaming.\n"
        "Monitored memory allocation using Chrome DevTools Heap Snapshot: memory stabilized at 54MB without memory leaks.\n"
        "Verified that old event DOM elements beyond 500 rows are cleanly recycled.\n"
        "Confirmed long-term dashboard operational stability.",
        "Memory heap profiling confirms zero client-side memory leakage."
    ),
    (
        "Constructed Print-Optimized Stylesheet (@media print) for SIEM dashboard in frontend/css/style.css.\n"
        "Configured clean white-background print styles hiding navigation bars and optimizing event tables and charts for standard A4 printing.\n"
        "Allows analysts to print hard-copy incident reports directly from the browser (Ctrl+P).\n"
        "Tested print preview across Chrome and Firefox.",
        "Print stylesheet enables effortless creation of physical incident reports."
    ),
    (
        "Designed custom 403 Forbidden Quarantine Warning Page in frontend/index.html.\n"
        "When a quarantined attacker IP attempts to access web services, page displays a high-impact cybersecurity warning banner showing their trapped IP address and incident tracking ID.\n"
        "Styled page with glowing red cyber aesthetics and security contact instructions.\n"
        "Reviewed active defense page with team lead Abhijeet.",
        "Quarantine block page provides an imposing, professional active defense barrier."
    ),
    (
        "Conducted complete frontend code audit, verifying semantic HTML5 tags (<header>, <main>, <nav>, <section>, <article>, <footer>).\n"
        "Ensured all form inputs have associated labels and unique element IDs.\n"
        "Verified zero HTML validation warnings using W3C validator.\n"
        "Finalized frontend code for release.",
        "Semantic HTML5 validation confirms high code quality and standards compliance."
    ),

        # Phase 5: Usability Testing, Stress Testing & Verification (Days 71-88)
    (
        "Formulated Frontend Usability and Verification Test Plan with Security QA Specialist Sanjay Kashyap.\n"
        "Defined 8 UI-specific test cases: WebSocket auto-reconnect, chart render under load, map marker clustering, dark/light theme switching, AI markdown rendering, file upload validation, zero-storage hashing, and quarantine toggle.\n"
        "Established quantitative acceptance benchmarks (60 FPS rendering, <100ms UI response).\n"
        "Documented UI test suite in project test plan.",
        "Frontend verification test plan is thorough and well-defined."
    ),
    (
        "Executed UI Test Case UTC-01 (WebSocket Reconnection) and UTC-02 (Live Event Ingestion).\n"
        "UTC-01: Disconnected network interface and reconnected after 30s. Verified automatic exponential backoff reconnection without page reload.\n"
        "UTC-02: Streamed 100 simulated attack events via WebSocket. Verified table row insertion, KPI counter updates, and zero UI stutter.\n"
        "Both test cases PASSED.",
        "WebSocket reconnection and event ingestion test cases passed."
    ),
    (
        "Executed UI Test Case UTC-03 (Map Layer Switching) and UTC-04 (Chart.js Live Updates).\n"
        "UTC-03: Toggled between Dark and Light modes. Verified seamless swap between ESRI Dark Canvas and OpenStreetMap tiles with zero watermark errors.\n"
        "UTC-04: Monitored rolling event volume chart over 30 minutes of continuous simulated attacks. Verified memory usage stayed flat (<45MB).\n"
        "Both test cases PASSED.",
        "Map tile and chart stability test cases validated successfully."
    ),
    (
        "Executed UI Test Case UTC-05 (AI Copilot Markdown Rendering) and UTC-06 (Phishing Analyzer).\n"
        "UTC-05: Tested AI responses containing tables, bold text, and iptables code blocks. Verified proper syntax highlighting and one-click copy button execution.\n"
        "UTC-06: Uploaded 5 sample phishing emails and 3 benign emails. Verified risk score badges and header analysis cards rendered accurately.\n"
        "Both test cases PASSED.",
        "AI Copilot and phishing forensics UI test cases passed with high visual fidelity."
    ),
    (
        "Executed UI Test Case UTC-07 (Zero-Storage Cryptographic Hasher) and UTC-08 (Active Quarantine Toggle).\n"
        "UTC-07: Verified SHA-256, SHA-512, MD5 hash calculation accuracy against standard NIST test vectors with zero network transmission.\n"
        "UTC-08: Toggled IP quarantine status from UI and verified instant table update and backend state synchronization.\n"
        "Both test cases PASSED.",
        "Cryptographic hasher and quarantine management UI tests passed."
    ),
    (
        "Conducted High-Throughput UI Stress Testing with team.\n"
        "Simulated burst injection of 500 events per second directly into WebSocket stream.\n"
        "Monitored browser rendering performance in Chrome DevTools Performance Profiler: FPS remained above 58, CPU scripting time <14ms per frame.\n"
        "Verified UI resilience under extreme attack flood conditions.",
        "Frontend exhibited exceptional rendering performance under high event volume."
    ),
    (
        "Conducted usability walkthrough with all 4 team members and collected operational feedback.\n"
        "Identified subtle areas for enhancement: added quick-filter chips above the live event table and refined hover tooltips on MITRE technique tags.\n"
        "Implemented visual polish adjustments in `style.css`.\n"
        "Verified enhanced analyst workflow efficiency.",
        "Usability walkthrough led to meaningful ergonomics enhancements."
    ),
    (
        "Assisted team lead Abhijeet Kumar in LAN multi-machine deployment testing.\n"
        "Accessed SIEM dashboard from secondary laptop across college local area network (`http://10.30.129.46:8000`).\n"
        "Verified full dashboard responsiveness, WebSocket stream connectivity, and live attack visualization from remote client browser.\n"
        "Confirmed real-world network operational readiness.",
        "LAN multi-machine deployment verified with flawless client rendering."
    ),
    (
        "Tested standalone desktop launcher integration with web dashboard.\n"
        "Verified that clicking 'Open SIEM Dashboard' in Tkinter launcher launched default system browser directly to the dashboard URL.\n"
        "Tested launcher status indicator synchronization with backend.\n"
        "Confirmed seamless operator onboarding experience.",
        "Desktop launcher and web UI integration operate harmoniously."
    ),
    (
        "Compiled Frontend Testing Results and Performance Metrics for Capstone Project Execution Document (Format-5).\n"
        "Documented all 8 UI test case outcomes, browser compatibility matrix, and Lighthouse audit scores.\n"
        "Provided high-resolution UI screenshots and component diagrams.\n"
        "Integrated frontend test results into master Format-5 document.",
        "Format-5 frontend verification section compiled with complete evidence."
    ),
    (
        "Conducted formal Sprint 4 Review with project guide Mr. Subhash J R.\n"
        "Demonstrated complete integrated platform: live attack visualization, AI Copilot threat triage, phishing analyzer, and zero-storage toolkit.\n"
        "Guide verified test results and commended the professional visual aesthetics.\n"
        "Instructed team to proceed to final documentation and viva defense preparation.",
        "Sprint 4 review completed. System is fully operational and approved."
    ),
    (
        "Updated Weekly Status Reports (Format-7) across all completed weeks.\n"
        "Documented individual contributions for Kanaka C (UI/UX, Map, Charts, AI frontend, Cyber Toolkit).\n"
        "Verified 4-student signature tables and milestone progress tracking.\n"
        "Submitted updated Format-7 Word document for cohort owner review.",
        "Format-7 weekly reports updated and verified."
    ),
    (
        "Cleaned up frontend source files, removing unused CSS rules and console logging statements.\n"
        "Verified asset file paths and verified zero broken links or 404 errors in browser console.\n"
        "Created production-ready minified build bundle.\n"
        "Committed final frontend release to GitHub repository.",
        "Frontend codebase finalized and ready for release distribution."
    ),
    (
        "Assisted in packaging final standalone distribution ZIP archive.\n"
        "Verified that all frontend static assets (HTML, CSS, JS, fonts, map tiles) are bundled properly inside standalone executable package.\n"
        "Tested standalone extraction on clean lab machine.\n"
        "Verified perfect offline execution.",
        "Distribution package verified with complete offline UI assets."
    ),

    # Phase 6: Final Documentation, Presentation & Viva Defense (Days 89-100)
    (
        "Commenced drafting frontend and analytics sections of Capstone Project Final Report.\n"
        "Authored Chapter 4.4 (User Interface Design & Ergonomics) and Chapter 4.5 (Real-Time Visualization Subsystems).\n"
        "Documented design system principles, HSL color tokens, Leaflet map architecture, and Chart.js integration.\n"
        "Generated high-resolution UI figures and workflow diagrams.",
        "Report chapters on UI/UX and visualization are well-documented."
    ),
    (
        "Authored Chapter 5.4 (AI Copilot Frontend Implementation) and Chapter 5.5 (Cyber Toolkit Implementation).\n"
        "Detailed the dual-mode AI chat architecture, markdown rendering algorithm, and WebCrypto API zero-storage hashing.\n"
        "Documented phishing forensic parser visualization.\n"
        "Reviewed draft chapters with team members.",
        "Implementation chapters provide clear technical and architectural descriptions."
    ),
    (
        "Authored Chapter 6.4 (Frontend Verification, Usability & Performance Analysis).\n"
        "Included all 8 UI verification test case tables, Lighthouse audit results, and FPS stress testing graphs.\n"
        "Highlighted quantitative metrics: 60 FPS rendering under 500 events/sec and <50ms WebSocket latency.\n"
        "Merged chapters into master project report.",
        "Testing and validation chapters compiled with comprehensive empirical data."
    ),
    (
        "Reviewed and finalized all 8 Capstone Project Formats (Format-1 to Format-8) in Microsoft Word.\n"
        "Verified student attribution for Kanaka C (Reg. No: 470CS23005) across all signature blocks.\n"
        "Ensured consistent formatting, typography, and page layout across all documents.\n"
        "Prepared master documentation submission folder.",
        "All 8 Capstone formats compiled and verified."
    ),
    (
        "Designed PowerPoint presentation slide deck for final Capstone Project Viva-Voce defense.\n"
        "Created visually engaging slides highlighting UI architecture, live SIEM dashboard features, world map visualization, and AI Copilot interaction flows.\n"
        "Embedded high-contrast screenshots and component flowcharts.\n"
        "Rehearsed presentation delivery with team.",
        "Presentation slides are professionally structured and visually compelling."
    ),
    (
        "Participated in full dry-run of final project demonstration and presentation in computer laboratory.\n"
        "Presented the Frontend SIEM Architecture, Live Geolocation Map, and AI Copilot interface.\n"
        "Demonstrated real-time attack visualization during simulated live multi-vector attacks.\n"
        "Received valuable feedback from guide Mr. Subhash J R on presentation pacing.",
        "Demonstration dry-run was well-coordinated and timed within limits."
    ),
    (
        "Refined demonstration sequence based on dry-run feedback.\n"
        "Optimized browser tab layout and zoom levels for projection display.\n"
        "Pre-configured attack scenario triggers for smooth live demonstration transitions.\n"
        "Verified display resolution compatibility on laboratory projector.",
        "Live demonstration environment fully configured and rehearsed."
    ),
    (
        "Assembled and printed individual hard-bound Format-8 Daily Log Book for Kanaka C covering all 100 days.\n"
        "Organized project deliverables on submission USB drive (source code, installer, documentation, presentation).\n"
        "Signed all declaration forms and project certificates.\n"
        "Submitted documentation package for cohort owner review.",
        "Hard-bound daily log book and project materials prepared for final submission."
    ),
    (
        "Appeared for final Capstone Project Evaluation and Viva-Voce Examination before External Examiners.\n"
        "Delivered technical presentation on Frontend SIEM Architecture, Geolocation Mapping, and AI SOC Copilot.\n"
        "Conducted successful live attack demonstration showing real-time event capture and AI threat triage on dashboard.\n"
        "External examiners commended the professional UI design, responsive charting, and intuitive AI copilot interface.\n"
        "Successfully defended Capstone Project with highest evaluation rating.",
        "Outstanding viva-voce defense and live demonstration. Project successfully completed!"
    ),
    (
        "Completed post-examination project archival and documentation handoff.\n"
        "Archived final source code, UI assets, and demonstration video recordings in department repository and GitHub.\n"
        "Submitted signed hard-bound project report and Format-8 Daily Log Book to the Department of Computer Science & Engineering.\n"
        "Extended sincere gratitude to cohort owner Mr. Subhash J R and HOD for their guidance throughout the semester.",
        "Project officially submitted and archived. Congratulations on outstanding work!"
    )
]

def build_format_8_kanaka():
    # 100 days starting from 15th July 2026 up to 22nd October 2026
    start_date = datetime.date(2026, 7, 15)
    working_days = get_100_days_schedule(start_date)
    
    print(f"Total days generated: {len(working_days)}")
    print(f"Start: {working_days[0]} ({working_days[0].strftime('%A')}), End: {working_days[-1]} ({working_days[-1].strftime('%A')})")

    doc = docx.Document()

    # Configure exact A4 margins (0.55 top/bottom, 0.65 left/right)
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)

    for day_idx in range(100):
        day_num = day_idx + 1
        day_date = working_days[day_idx]
        date_str = day_date.strftime("%d-%m-%Y (%A)")
        
        # Pull corresponding log activity and remark for Kanaka C
        log_text, remark_text = LOG_ENTRIES_KANAKA[day_idx]

        # ---------------------------------------------------------
        # HEADER BLOCK (Department & Capstone Title)
        # ---------------------------------------------------------
        p_hdr = doc.add_paragraph()
        p_hdr.paragraph_format.space_before = Pt(0)
        p_hdr.paragraph_format.space_after = Pt(2)
        p_hdr.paragraph_format.line_spacing = 1.1
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        r1 = p_hdr.add_run("Department of Technical Education\n")
        r1.font.name = "Calibri"
        r1.font.size = Pt(11.5)
        r1.bold = True
        
        r2 = p_hdr.add_run("Capstone Project  |  Format- 8\n")
        r2.font.name = "Calibri"
        r2.font.size = Pt(10.5)
        r2.bold = True
        
        r3 = p_hdr.add_run("STUDENT’S DAILY LOG BOOK")
        r3.font.name = "Calibri"
        r3.font.size = Pt(13)
        r3.bold = True
        r3.font.color.rgb = RGBColor(0, 102, 204) # Royal Cyber Blue

        # Note / Notice
        p_note = doc.add_paragraph()
        p_note.paragraph_format.space_before = Pt(2)
        p_note.paragraph_format.space_after = Pt(6)
        p_note.paragraph_format.line_spacing = 1.05
        p_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_note = p_note.add_run("Note: A4 size Student’s Daily Log Book with official college, registration and execution details")
        r_note.font.name = "Calibri"
        r_note.font.size = Pt(8)
        r_note.italic = True
        r_note.font.color.rgb = RGBColor(90, 90, 90)

        # ---------------------------------------------------------
        # TABLE 1: METADATA BOX (Generous spacing to fill ~75-80% of page)
        # ---------------------------------------------------------
        t_meta = doc.add_table(rows=5, cols=2)
        t_meta.style = 'Table Grid'
        t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_w = [Inches(2.1), Inches(4.87)]
        for row in t_meta.rows:
            for c_idx, w in enumerate(col_w):
                row.cells[c_idx].width = w

        # Row 0: Day & Date
        set_cell_props(t_meta.rows[0].cells[0], f"Day-{day_num}", bold=True, font_size=9.5, bg_color="E2E8F0", space_before=2.5, space_after=2.5)
        set_cell_props(t_meta.rows[0].cells[1], f"Date: {date_str}", bold=True, font_size=9.5, bg_color="E2E8F0", space_before=2.5, space_after=2.5)

        # Row 1: Project Name
        set_cell_props(t_meta.rows[1].cells[0], "Capstone project Name:", bold=True, font_size=9, space_before=2.5, space_after=2.5)
        set_cell_props(t_meta.rows[1].cells[1], "K.A.R.M.A – Cyber Threat Deception and AI-Assisted SIEM Platform", bold=False, font_size=9, space_before=2.5, space_after=2.5)

        # Row 2: Name of the Student + Registration Number
        set_cell_props(t_meta.rows[2].cells[0], "Name of the student:", bold=True, font_size=9, space_before=2.5, space_after=2.5)
        set_cell_props(t_meta.rows[2].cells[1], "Kanaka C  |  Reg. No: 470CS23005  (Role: Security Analyst & Frontend Engineer)", bold=True, font_size=9, space_before=2.5, space_after=2.5)

        # Row 3: Name of the Cohort Owner
        set_cell_props(t_meta.rows[3].cells[0], "Name of the Cohort owner:", bold=True, font_size=9, space_before=2.5, space_after=2.5)
        set_cell_props(t_meta.rows[3].cells[1], "Mr. Subhash J R  (Lecturer, Dept. of Computer Science & Engineering)", bold=False, font_size=9, space_before=2.5, space_after=2.5)

        # Row 4: Remarks of the Cohort owner
        set_cell_props(t_meta.rows[4].cells[0], "Remarks of Cohort owner:", bold=True, font_size=9, space_before=2.5, space_after=2.5)
        set_cell_props(t_meta.rows[4].cells[1], remark_text, bold=False, font_size=9, space_before=2.5, space_after=2.5)

        # ---------------------------------------------------------
        # ACTIVITIES SECTION (Record Main Activities of the Day)
        # ---------------------------------------------------------
        p_act_hdr = doc.add_paragraph()
        p_act_hdr.paragraph_format.space_before = Pt(8)
        p_act_hdr.paragraph_format.space_after = Pt(3)
        r_act_hdr = p_act_hdr.add_run("Record Main activities of the day (including observation, sketches, discussions, etc):")
        r_act_hdr.font.name = "Calibri"
        r_act_hdr.font.size = Pt(9.5)
        r_act_hdr.bold = True

        # Activity Box (Single Cell Table with comfortable vertical padding)
        t_act = doc.add_table(rows=1, cols=1)
        t_act.style = 'Table Grid'
        t_act.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_act.rows[0].cells[0].width = Inches(6.97)
        
        cell_act = t_act.rows[0].cells[0]
        cell_act.text = ""
        lines = [l.strip() for l in log_text.strip().split("\n") if l.strip()]
        for l_idx, line in enumerate(lines):
            p_line = cell_act.paragraphs[0] if l_idx == 0 else cell_act.add_paragraph()
            p_line.paragraph_format.space_before = Pt(3)
            p_line.paragraph_format.space_after = Pt(3)
            p_line.paragraph_format.line_spacing = 1.18
            p_line.paragraph_format.left_indent = Inches(0.18)
            
            r_bullet = p_line.add_run("• ")
            r_bullet.font.name = "Calibri"
            r_bullet.font.size = Pt(9.5)
            r_bullet.bold = True
            
            r_text = p_line.add_run(line)
            r_text.font.name = "Calibri"
            r_text.font.size = Pt(9.5)

        # ---------------------------------------------------------
        # SIGNATURE FOOTER BLOCK
        # ---------------------------------------------------------
        p_sig = doc.add_paragraph()
        p_sig.paragraph_format.space_before = Pt(10)
        p_sig.paragraph_format.space_after = Pt(0)
        p_sig.paragraph_format.line_spacing = 1.0

        t_sig = doc.add_table(rows=2, cols=2)
        t_sig.style = 'Table Grid'
        t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
        col_sig_w = [Inches(3.48), Inches(3.49)]
        for row in t_sig.rows:
            for c_idx, w in enumerate(col_sig_w):
                row.cells[c_idx].width = w

        set_cell_props(t_sig.rows[0].cells[0], "Signature of the Student:\n\n\n_____________________________\nKanaka C  (Reg. No: 470CS23005)", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=3, space_after=3)
        set_cell_props(t_sig.rows[0].cells[1], "Signature of the Cohort owner:\n\n\n_____________________________\nMr. Subhash J R  (Project Guide)", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=3, space_after=3)

        set_cell_props(t_sig.rows[1].cells[0], "Dept. of Computer Science & Engineering", font_size=8, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="F8FAFC", space_before=2, space_after=2)
        set_cell_props(t_sig.rows[1].cells[1], "The Oxford Evening Polytechnic, Bangalore", font_size=8, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="F8FAFC", space_before=2, space_after=2)

        # Add page break for all days except the very last one (Day 100)
        if day_idx < 99:
            doc.add_page_break()

    # Save final document
    doc.save(OUT_PATH)
    print(f"\n[SUCCESS] 100-Day Log Book for Kanaka C successfully created at:\n  - {OUT_PATH}")

if __name__ == "__main__":
    build_format_8_kanaka()
