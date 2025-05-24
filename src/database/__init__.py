import json

# --- Rollen aus JSON-Datei laden (für Entwicklung) ---
with open("src/database/roles.json") as f:
    ROLE_MAP = json.load(f)
