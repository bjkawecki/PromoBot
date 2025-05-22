# Promo-Bot

## Idee

- Produktbasierter Promo-Bot.
- Kanalbetreiber sollen damit gezielt einzelne Produkte promoten.
- Bestellung und Bezahlung laufen direkt über Telegram.
- Statusverfolgung und Kommunikation für Käufer & Verkäufer soll eingebaut sein.

## Architektur-Übersicht

📱 Telegram Promo-Bot (Python / Node.js)
│

├─ 💬 Telegram Bot API (z. B. via aiogram / node-telegram-bot-api)

├─ 🧠 Logik / Bot-Server (z. B. mit FastAPI, Express.js oder Flask)

│ ├─ Webhook-Handler für Telegram-Events

│ ├─ Stripe-Webhook-Handler für Payment Updates

│ └─ API-Endpunkte für Status & Rechnung

├─ 🗃️ Datenbank (z. B. SQLite oder PostgreSQL bei Bedarf)

│ ├─ Nutzer, Bestellungen, Produkte, Kanäle

├─ 💳 Zahlungsanbieter (z. B. Stripe via Telegram Bot Payments)

└─ 📤 E-Mail-Service (z. B. SMTP, Mailjet, Resend) für Rechnungen

## Bot-Flow: Beispiel produkt anlegen → bestellen → bezahlen → status

### Für Verkäufer (Kanalbetreiber):

/verknüpfen_meinen_shop

- "Bitte gib deinen Shop-Namen ein:"

/produkt_anlegen

- "Name des Produkts?"
- "Beschreibung?"
- "Normalpreis?"
- "Rabattpreis (für Telegram)?"
- "Bild-Link oder Bild hochladen"
- "Maximale Anzahl Bestellungen?"
- "Gültig bis (optional)?"
- Bot generiert Link/Button:
  t.me/PromoBestellBot?start=produkt123

### Für Käufer:

1. Klickt auf den Button im Kanal:

- t.me/PromoBestellBot?start=produkt123

2. Bot fragt:

- „Möchtest du Wolkenatlas zum Sonderpreis kaufen?“
- „Gib deine E-Mail ein:“
- „Lieferadresse?“
- „Zahlung jetzt abschließen?“ → Telegram-Zahlung mit Stripe

3. Nach erfolgreicher Zahlung:

- Bot: „Vielen Dank! Deine Bestellung wurde aufgenommen.“
- Rechnung wird gesendet
- Command: /meine_bestellungen

### Käufer-Commands:

- /meine_bestellungen Liste der Bestellungen mit Status
- /status <id> Details einer Bestellung
- /rechnung <id> PDF erneut erhalten

### Verkäufer-Commands (Admin):

- /meine_bestellungen Alle Bestellungen für seine Produkte
- /status <id> Status ansehen
- /versendet <id> Status aktualisieren + Käufer benachrichtigen
- /export_bestellungen CSV-Link oder Google Sheet-Anbindung

## Sicherheit & Auth

- Admins = Telegram-IDs der Kanalbetreiber
- Zugriff auf Bestellungen nur über:
  - Telegram ID verknüpft mit Bestellung (Käufer)
  - Telegram ID verknüpft mit Produkt (Verkäufer)

## AWS-basierte Architektur für deinen Telegram Promo-Bot

### Überblick

- 📱 Telegram User
- 🤖 Telegram Bot API → API Gateway
- 🧠 Lambda Functions
- 🗃️ Amazon DynamoDB
- 💳 Stripe (Payments)
  📧 SES (E-Mails mit Rechnung)

### AWS-Komponenten im Detail

| Komponente               | Zweck                                            | Preis                             | Alternative              |
| ------------------------ | ------------------------------------------------ | --------------------------------- | ------------------------ |
| **Lambda**               | Bot-Logik, Webhooks, Admin-Aktionen              | Nur für Aufrufe bezahlen          | EC2 (aber teurer)        |
| **API Gateway**          | Schnittstelle für Telegram & Stripe-Webhooks     | sehr günstig                      | ALB (komplizierter)      |
| **DynamoDB**             | Speicherung von Produkten, Bestellungen, Nutzern | Kostenloser Kontingent nutzbar    | PostgreSQL (RDS, teurer) |
| **Stripe**               | Bezahlung (Telegram Bot Payments)                | Transaktionsbasiert               | PayPal, LemonSqueezy     |
| **Amazon SES**           | E-Mail-Versand (z. B. Rechnung als PDF)          | 62.000 Mails/Monat frei (aus EC2) | Mailgun, Resend          |
| **S3**                   | Speicherung von Rechnungspdfs / Bildern          | sehr günstig                      | Firebase Storage         |
| **Cognito** _(optional)_ | Verkäufer-Login in Web-Dashboard                 | kostenlos im kleinen Umfang       | Auth0                    |

### Konkrete Bot-Ablauf-Beispiele mit AWS-Komponenten

#### Webhook-Verarbeitung (Telegram, Stripe)

- Telegram-Bot
  → registrierter Webhook
  → API Gateway
  → ruft Lambda handle_bot_event auf
- Lambda verarbeitet z. B. /bestellen produkt123
  → schreibt Daten in DynamoDB
  → erstellt Stripe Payment Link (oder Telegram Bot Payment mit Stripe)
  → gibt Antwort via Telegram zurück

### 💾 DynamoDB – Tabellenstruktur

**Tabelle: Products**

| Partition Key | Sort Key    | Weitere Daten             |
| ------------- | ----------- | ------------------------- |
| `PRODUCT#123` | `METADATA`  | Name, Preis, Rabatt, etc. |
| `PRODUCT#123` | `ORDER#456` | Bestellung zu Produkt     |

**Tabelle: Users**
| Partition Key | Sort Key | E-Mail, Adresse, Telegram-ID |
| ------------- | ----------- | ---------------------------- |
| `USER#789` | `PROFILE` | ... |
| `USER#789` | `ORDER#456` | Verknüpfung zu Bestellung |

## Rechnung versenden (SES + S3)

Nach erfolgreicher Zahlung:

1. Lambda handle_payment_success wird über Stripe Webhook ausgelöst
2. Erstellt Rechnung (PDF mit fpdf oder reportlab)
3. Speichert PDF in S3: invoices/order456.pdf
4. Sendet E-Mail via SES:
   „Hier ist Ihre Rechnung zu Bestellung 456...“

## Admin-Funktionen für Verkäufer (Bot oder Mini-App)

Du kannst per Telegram-Bot auch Verkäufer bedienen:

- /meine_bestellungen
- /versendet 1234
- /export → CSV-Datei aus DynamoDB generieren

Oder als Web-Mini-App:

- Telegram Login Button → Login über Telegram ID
- Zeigt Produkte und Bestellungen dieses Verkäufers

## Laufende Kosten (realistisch für Einzelentwickler)

| Dienst            | Kosten / Monat (bei wenigen Bestellungen) |
| ----------------- | ----------------------------------------- |
| Lambda            | \$0 (innerhalb Free Tier)                 |
| API Gateway       | \~\$1–2 (abhängig von Aufrufen)           |
| DynamoDB          | \$0–1 (bei <= 25 GB und geringem Traffic) |
| SES (Rechnungen)  | \$0 (aus Lambda bis 62k Mails/Monat)      |
| S3 (PDFs, Bilder) | \$0–0.5                                   |
| Stripe            | Transaktionsgebühr (abhängig von Land)    |

Gesamt: < 5–10 € monatlich bei geringen Nutzerzahlen.

Hier ist eine **Marketing-freundliche Vorteils-Liste**, mit der du **Verkäufer/Kanalbetreiber überzeugen** kannst, deinen Telegram Promo-Bot zu nutzen:

---

## 💡 Vorteile für Verkäufer: Telegram Promo-Bot als Verkaufs-Tool

### 1. **Mehr Umsatz durch Sofort-Käufe**

> Mach aus Aufmerksamkeit direkt Umsatz – mit einem Button direkt im Post.

- Nutzer kaufen _ohne die App zu verlassen_
- Impulskäufe steigen durch einfache Bestellung

---

### 2. **Direkter Draht zu loyalen Followern**

> Du verkaufst direkt an die Menschen, die deinen Kanal abonniert haben – ohne Streuverluste.

- Kein Algorithmus, keine Anzeigenkosten
- Maximale Sichtbarkeit im Kanal

---

### 3. **Persönlicher Verkauf im Messenger**

> Kunden fühlen sich betreut – nicht wie in einem anonymen Webshop.

- Interaktive Bestellstrecke per Chat
- Käufer können Fragen stellen oder Hilfe anfordern

---

### 4. **Sonderaktionen & Rabatte nur für Abonnenten**

> Belohne deine Telegram-Follower mit exklusiven Rabatten.

- Promo-Produkte nur über Bot bestellbar
- Rabatt-Aktionen schnell aufsetzen

---

### 5. **Schnelle Bestellung – kein Checkout-Wahnsinn**

> Kein Account-Zwang, kein Passwort, keine App-Downloads.

- Käufer geben nur das Nötigste an
- Telegram-Zahlung oder Stripe-Link – sofort bezahlbar

---

### 📦 6. **Einfaches Bestell-Management für dich**

> Du wirst über jede Bestellung benachrichtigt und kannst alles im Bot verwalten.

- Übersicht über alle Bestellungen
- Bestellung als "versendet" markieren mit einem Klick

---

### 7. **Automatische Rechnungserstellung**

> Käufer erhalten direkt eine rechtskonforme Rechnung – ohne Aufwand für dich.

- Rechnung per Mail oder Telegram
- Ideal für Buchhaltung und Rückfragen

---

### 8. **Wiederkaufsrate steigern mit Bestell-Historie**

> Kunden sehen im Bot ihre alten Bestellungen – und bestellen schnell erneut.

- Erhöht Vertrauen & Convenience
- Ideal für Abo-Produkte oder Serienkäufe

---

### 9. **Einfacher Start – kein Tech-Wissen nötig**

> Du brauchst keinen Webshop, keine eigene Website, kein technisches Setup.

- Produkt im Bot anlegen → Bestell-Link erzeugen
- Sofort verwendbar in deinem Telegram-Kanal

---

### 10. **Keine Fixkosten – nur bei echten Verkäufen**

> Keine Abo-Gebühren oder laufenden Kosten. Du zahlst nur Stripe-Gebühren.

- Ideal für kleine Kanäle oder Nischenprodukte
- Starten ohne Risiko
