promo_bot/
│
├── main.py # Einstiegspunkt
├── config.py # Bot-Konfiguration (Token, Umgebungsvariablen)
├── commands.py # Bot-Kommandos (für BotFather & Bot-UI)
│
├── handlers/ # Alle Telegram-Handler
│ ├── buyer.py # Buyer-Flows: Bestellung, Status etc.
│ ├── seller.py # Seller-Flows: Promo anlegen, Status ändern etc.
│ └── admin.py # Admin-Funktionalität
│
├── services/ # Logik für DB, Stripe, PDF etc.
│ ├── stripe.py
│ ├── database.py
│ └── invoice.py
│
├── models/ # Datenmodelle oder Pydantic-Objekte
│ └── order.py
│
├── keyboards/ # Inline- und Reply-Keyboards
│ └── buyer_kb.py
│
├── utils/ # Hilfsfunktionen (z. B. Logging, Zeit etc.)
│ └── misc.py
│
├── middlewares/ # (Optional) z. B. Logging, Auth
│ └── auth.py
│
└── requirements.txt # Abhängigkeiten
