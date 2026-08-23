"""
AI Threat Synthesizer & Autonomous SOC Analyst
Analyzes raw attack events and generates executive incident reports, intent classification, and remediation steps.
"""

def generate_ai_threat_summary(attacker_ip, logs, attacker_profile):
    if not logs:
        return {
            "summary": "No telemetry recorded for this IP address yet.",
            "intent": "UNKNOWN",
            "threat_level": "LOW",
            "recommendations": ["Maintain standard perimeter monitoring."]
        }

    total_events = len(logs)
    services_hit = list(set(l['decoy_service'] for l in logs))
    mitre_ids = list(set(l['mitre_id'] for l in logs if l['mitre_id']))
    max_risk = max((l['risk_score'] for l in logs), default=0)

    # Classify Intent
    if "T1078" in mitre_ids or "HONEYTOKEN" in services_hit:
        intent = "Targeted Credential Exploitation / Exfiltration"
        summary = (f"CRITICAL INCIDENT: Attacker from {attacker_ip} triggered a high-value Honeytoken (Decoy Credential/URL). "
                   f"This indicates active lateral movement or post-reconnaissance access attempt using decoy tokens.")
        threat_level = "CRITICAL"
        remediations = [
            "Immediately isolate associated host network interface.",
            "Revoke compromised credential signatures & rotate active session keys.",
            "Automated IP Quarantine enforced by Aegis-SOC Active Defense."
        ]
    elif "T1059" in mitre_ids:
        intent = "Arbitrary Command Execution / Interactive Shell Compromise"
        summary = (f"HIGH SEVERITY: Attacker connected to SSH Decoy and attempted interactive shell commands. "
                   f"Captured commands include reconnaissance tools (whoami, id, cat /etc/passwd).")
        threat_level = "CRITICAL" if max_risk >= 85 else "HIGH"
        remediations = [
            "Block IP address at gateway firewall / IPTables.",
            "Audit internal Linux user accounts for unauthorized key additions.",
            "Enforce strict multi-factor authentication (MFA)."
        ]
    elif "T1190" in mitre_ids:
        intent = "Web Application Vulnerability Exploitation (OWASP Top 10)"
        summary = (f"HIGH SEVERITY: Attacker launched SQL Injection / Web Application exploit payloads against Web Admin Decoy. "
                   f"Pattern demonstrates automated web vulnerability scanner or targeted exploit script.")
        threat_level = "HIGH"
        remediations = [
            "Deploy Web Application Firewall (WAF) filtering rules.",
            "Block IP {attacker_ip} across public web endpoints.",
            "Inspect web access logs for secondary payloads."
        ]
    elif "T1110" in mitre_ids:
        intent = "Automated Brute-Force Authentication Attack"
        summary = (f"MEDIUM-HIGH SEVERITY: Attacker launched repeated authentication attempts against decoy authentication interfaces. "
                   f"Recorded {total_events} failed login attempts across services: {', '.join(services_hit)}.")
        threat_level = "HIGH" if total_events > 10 else "MEDIUM"
        remediations = [
            "Enable Fail2Ban / IP rate limiting on public SSH and Login portals.",
            "Disallow password-based SSH logins in favor of SSH keys."
        ]
    else:
        intent = "Reconnaissance & Network Port Probing"
        summary = (f"LOW-MEDIUM SEVERITY: Attacker probed decoy network services ({', '.join(services_hit)}). "
                   f"Consistent with automated network port scanners (e.g., Nmap, Masscan).")
        threat_level = "MEDIUM" if max_risk >= 50 else "LOW"
        remediations = [
            "Filter unused external inbound ports at boundary router.",
            "Monitor IP for escalation or payload execution attempts."
        ]

    # Dynamic AI Executive Synthesis Report
    report = {
        "attacker_ip": attacker_ip,
        "threat_level": threat_level,
        "max_risk_score": max_risk,
        "total_events": total_events,
        "intent_classification": intent,
        "summary": summary,
        "targeted_services": services_hit,
        "mitre_techniques": mitre_ids,
        "recommendations": remediations,
        "ai_verdict": f"Aegis AI recommends immediate {'QUARANTINE' if threat_level in ['CRITICAL', 'HIGH'] else 'CONTINUOUS MONITORING'} for IP {attacker_ip}."
    }

    return report
