import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "aegis_soc.db")

HOST = "0.0.0.0"
PORT_API = 8000
PORT_SSH_HONEYPOT = 2222
PORT_WEB_HONEYPOT = 8080
DECOY_PORTS = [21, 23, 3389]  # FTP, Telnet, RDP decoy probes

# Threat scoring threshold for automated IP quarantine
QUARANTINE_SCORE_THRESHOLD = 75

# Default Honeytokens
DEFAULT_HONEYTOKENS = [
    {
        "token_id": "ht-aws-01",
        "name": "Decoy AWS Production Key",
        "type": "API Key",
        "token_value": "AKIAIOSFODNN7EXAMPLE_DECOY_KEY_99",
        "description": "Embedded in fake git repository leak"
    },
    {
        "token_id": "ht-admin-url",
        "name": "Secret DB Admin Portal",
        "type": "Decoy URL",
        "token_value": "/secret-vault-admin-login-php",
        "description": "Hidden hyper-link decoy in fake web portal"
    },
    {
        "token_id": "ht-ssh-key",
        "name": "Staging Server Private Key",
        "type": "Credentials",
        "token_value": "root:SuperSecretStaging2026!",
        "description": "Fake credentials in configuration file decoy"
    }
]
