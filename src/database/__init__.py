import json

from config import DB_URL

# --- Rollen aus JSON-Datei laden (für Entwicklung) ---
with open(DB_URL) as f:
    db_data = json.load(f)
