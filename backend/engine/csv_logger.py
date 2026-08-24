"""
CSV SIEM Audit Logger for K.A.R.M.A Cloud SIEM
Automatically creates timestamped CSV log files on server startup (logs/karma_audit_YYYY-MM-DD_HH-MM-SS.csv),
logs all incoming attack telemetry in real-time with immediate flushing,
and safely saves and closes on server shutdown.
"""

import os
import csv
import time
from datetime import datetime

class AuditCsvLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.file_path = None
        self.file_handle = None
        self.csv_writer = None
        self.is_active = False

    def start(self):
        try:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

            timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"karma_audit_{timestamp_str}.csv"
            self.file_path = os.path.join(self.log_dir, filename)

            self.file_handle = open(self.file_path, mode="w", newline="", encoding="utf-8")
            self.csv_writer = csv.writer(self.file_handle, quoting=csv.QUOTE_MINIMAL, escapechar="\\")

            # Write Standard CSV Header
            headers = [
                "Log_ID",
                "Timestamp",
                "Attacker_IP",
                "Country",
                "City",
                "Target_Service",
                "Port",
                "Attack_Type",
                "Executed_Payload",
                "MITRE_ID",
                "MITRE_Name",
                "Severity",
                "Risk_Score",
                "Action_Taken"
            ]
            self.csv_writer.writerow(headers)
            self.file_handle.flush()
            self.is_active = True
            print(f"[CSV Audit Logger] Session log initialized: {self.file_path}")
        except Exception as e:
            print(f"[CSV Audit Logger Error] Failed to initialize CSV logger: {e}")

    def log_event(self, event):
        if not self.is_active or not self.csv_writer:
            return

        try:
            payload_str = str(event.get("payload", "")).replace("\n", " ").replace("\r", " ")
            row = [
                event.get("id", ""),
                event.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%S")),
                event.get("attacker_ip", ""),
                event.get("country", ""),
                event.get("city", ""),
                event.get("decoy_service", ""),
                event.get("port", ""),
                event.get("attack_type", ""),
                payload_str,
                event.get("mitre_id", ""),
                event.get("mitre_name", ""),
                event.get("severity", ""),
                event.get("risk_score", 0),
                "Quarantined / Isolated" if event.get("quarantined") else "Monitored"
            ]
            self.csv_writer.writerow(row)
            self.file_handle.flush() # Immediate flush so no data is lost on crash/exit
        except Exception as e:
            print(f"[CSV Audit Logger Error] Failed to write event to CSV: {e}")

    def stop(self):
        if self.file_handle:
            try:
                self.file_handle.flush()
                self.file_handle.close()
                print(f"[CSV Audit Logger] Session log saved and closed cleanly: {self.file_path}")
            except Exception as e:
                print(f"[CSV Audit Logger Error] Error closing CSV log file: {e}")
            finally:
                self.is_active = False

# Global instance for app import
audit_csv_logger = AuditCsvLogger()
