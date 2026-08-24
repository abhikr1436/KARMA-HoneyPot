"""
K.A.R.M.A SQLite Database Engine & Geolocation Mapping Layer
Manages threat logs, attacker IP profiles, MITRE ATT&CK statistics, and honeytoken tracking.
"""

import sqlite3
import json
import ipaddress
from datetime import datetime
from backend.config import DB_PATH, DEFAULT_HONEYTOKENS

# Mock IP Geolocation Database for Demonstration Variety
IP_GEO_MAP = {
    "185.220.101.5": {"country": "Germany", "city": "Frankfurt", "lat": 50.1109, "lng": 8.6821, "flag": "🇩🇪"},
    "45.33.32.156": {"country": "United States", "city": "California", "lat": 37.7749, "lng": -122.4194, "flag": "🇺🇸"},
    "198.51.100.42": {"country": "Japan", "city": "Tokyo", "lat": 35.6762, "lng": 139.6503, "flag": "🇯🇵"},
    "103.21.244.0": {"country": "India", "city": "Bengaluru", "lat": 12.9716, "lng": 77.5946, "flag": "🇮🇳"}
}

def get_geo_info(ip):
    if ip in IP_GEO_MAP:
        return IP_GEO_MAP[ip]

    # Automatically map all Private / Local LAN IP addresses (10.x.x.x, 192.168.x.x, 172.16.x.x, 127.x.x.x)
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            return {
                "country": "India (Local Network)",
                "city": "Bengaluru",
                "lat": 12.9716,
                "lng": 77.5946,
                "flag": "🇮🇳"
            }
    except Exception:
        pass

    # Fallback simulation generator for unmapped external public IPs
    h = hash(ip)
    lats = [55.7558, 48.8566, 51.5074, -33.8688, 39.9042]
    lngs = [37.6173, 2.3522, -0.1278, 151.2093, 116.4074]
    countries = ["Russia", "France", "United Kingdom", "Australia", "China"]
    flags = ["🇷🇺", "🇫🇷", "🇬🇧", "🇦🇺", "🇨🇳"]
    idx = abs(h) % len(lats)
    return {
        "country": countries[idx],
        "city": "Capital Region",
        "lat": lats[idx],
        "lng": lngs[idx],
        "flag": flags[idx]
    }

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attack_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            attacker_ip TEXT NOT NULL,
            port INTEGER NOT NULL,
            decoy_service TEXT NOT NULL,
            attack_type TEXT NOT NULL,
            payload TEXT,
            mitre_id TEXT,
            mitre_name TEXT,
            mitre_tactic TEXT,
            risk_score INTEGER NOT NULL,
            severity TEXT NOT NULL,
            country TEXT,
            city TEXT,
            lat REAL,
            lng REAL,
            flag TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attackers (
            ip TEXT PRIMARY KEY,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            total_attempts INTEGER DEFAULT 1,
            max_risk_score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'MONITORING',
            services_targeted TEXT,
            country TEXT,
            city TEXT,
            lat REAL,
            lng REAL,
            flag TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS honeytokens (
            token_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            token_value TEXT NOT NULL,
            status TEXT DEFAULT 'ACTIVE',
            created_at TEXT NOT NULL,
            hit_count INTEGER DEFAULT 0,
            last_hit_ip TEXT,
            last_hit_time TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quarantine_list (
            ip TEXT PRIMARY KEY,
            quarantined_at TEXT NOT NULL,
            reason TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            status TEXT DEFAULT 'ACTIVE'
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM honeytokens')
    if cursor.fetchone()[0] == 0:
        now = datetime.now().isoformat()
        for ht in DEFAULT_HONEYTOKENS:
            cursor.execute('''
                INSERT INTO honeytokens (token_id, name, type, token_value, status, created_at)
                VALUES (?, ?, ?, ?, 'ACTIVE', ?)
            ''', (ht['token_id'], ht['name'], ht['type'], ht['token_value'], now))

    # Auto Migration for Geo Columns if existing DB schema is older
    try:
        cursor.execute("ALTER TABLE attack_logs ADD COLUMN country TEXT")
        cursor.execute("ALTER TABLE attack_logs ADD COLUMN city TEXT")
        cursor.execute("ALTER TABLE attack_logs ADD COLUMN lat REAL")
        cursor.execute("ALTER TABLE attack_logs ADD COLUMN lng REAL")
        cursor.execute("ALTER TABLE attack_logs ADD COLUMN flag TEXT")
    except Exception:
        pass

    try:
        cursor.execute("ALTER TABLE attackers ADD COLUMN country TEXT")
        cursor.execute("ALTER TABLE attackers ADD COLUMN city TEXT")
        cursor.execute("ALTER TABLE attackers ADD COLUMN lat REAL")
        cursor.execute("ALTER TABLE attackers ADD COLUMN lng REAL")
        cursor.execute("ALTER TABLE attackers ADD COLUMN flag TEXT")
    except Exception:
        pass

    conn.commit()
    conn.close()

def log_attack_event(attacker_ip, port, decoy_service, attack_type, payload, mitre_id, mitre_name, mitre_tactic, risk_score, severity):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    geo = get_geo_info(attacker_ip)

    cursor.execute('''
        INSERT INTO attack_logs (timestamp, attacker_ip, port, decoy_service, attack_type, payload, mitre_id, mitre_name, mitre_tactic, risk_score, severity, country, city, lat, lng, flag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (now, attacker_ip, port, decoy_service, attack_type, payload, mitre_id, mitre_name, mitre_tactic, risk_score, severity, geo['country'], geo['city'], geo['lat'], geo['lng'], geo['flag']))

    cursor.execute('SELECT total_attempts, max_risk_score, services_targeted FROM attackers WHERE ip = ?', (attacker_ip,))
    row = cursor.fetchone()

    if row:
        attempts = row['total_attempts'] + 1
        max_score = max(row['max_risk_score'], risk_score)
        try:
            services = set(json.loads(row['services_targeted'] or "[]"))
        except Exception:
            services = set()
        services.add(decoy_service)
        services_str = json.dumps(list(services))

        cursor.execute('''
            UPDATE attackers
            SET last_seen = ?, total_attempts = ?, max_risk_score = ?, services_targeted = ?
            WHERE ip = ?
        ''', (now, attempts, max_score, services_str, attacker_ip))
    else:
        services_str = json.dumps([decoy_service])
        cursor.execute('''
            INSERT INTO attackers (ip, first_seen, last_seen, total_attempts, max_risk_score, status, services_targeted, country, city, lat, lng, flag)
            VALUES (?, ?, ?, 1, ?, 'MONITORING', ?, ?, ?, ?, ?, ?)
        ''', (attacker_ip, now, now, risk_score, services_str, geo['country'], geo['city'], geo['lat'], geo['lng'], geo['flag']))

    conn.commit()
    log_id = cursor.lastrowid
    conn.close()
    return log_id

def get_total_attack_count():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM attack_logs')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_recent_logs(limit=1000):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attack_logs ORDER BY id DESC LIMIT ?', (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_attackers_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM attackers ORDER BY max_risk_score DESC, total_attempts DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_mitre_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT mitre_id, mitre_name, mitre_tactic, COUNT(*) as hit_count, MAX(risk_score) as max_score
        FROM attack_logs
        WHERE mitre_id IS NOT NULL AND mitre_id != ''
        GROUP BY mitre_id, mitre_name, mitre_tactic
        ORDER BY hit_count DESC
    ''')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_honeytokens():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM honeytokens ORDER BY hit_count DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def record_honeytoken_hit(token_id, ip_address):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        UPDATE honeytokens
        SET hit_count = hit_count + 1, last_hit_ip = ?, last_hit_time = ?
        WHERE token_id = ? OR token_value = ?
    ''', (ip_address, now, token_id, token_id))
    conn.commit()
    conn.close()

def add_to_quarantine(ip, reason, risk_score):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        INSERT OR REPLACE INTO quarantine_list (ip, quarantined_at, reason, risk_score, status)
        VALUES (?, ?, ?, ?, 'ACTIVE')
    ''', (ip, now, reason, risk_score))
    cursor.execute("UPDATE attackers SET status = 'QUARANTINED' WHERE ip = ?", (ip,))
    conn.commit()
    conn.close()

def remove_from_quarantine(ip):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quarantine_list WHERE ip = ?", (ip,))
    cursor.execute("UPDATE attackers SET status = 'MONITORING' WHERE ip = ?", (ip,))
    conn.commit()
    conn.close()

def get_quarantine_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quarantine_list ORDER BY quarantined_at DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def clear_all_data():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM attack_logs')
    cursor.execute('DELETE FROM attackers')
    cursor.execute('DELETE FROM quarantine_list')
    cursor.execute('UPDATE honeytokens SET hit_count = 0, last_hit_ip = NULL, last_hit_time = NULL')
    conn.commit()
    conn.close()
