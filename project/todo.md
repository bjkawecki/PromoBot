# Start-Plan

## **1. Anwendungs-Design & Flows festlegen**

- Was genau kann der Bot (MVP)?
  → Beispiel: Produkt anzeigen, kaufen, Status abrufen
- Welche Akteure?
  → Kanalbetreiber, Käufer
- Welche Befehle?
  → `/start`, `/status`, `/meine_bestellungen`, `/hilfe`, `/produkt_anlegen`

🔹 _Ziel: Übersichtliche Liste aller Abläufe & Befehle (Use Case Map)_

---

## **2. Lokale Bot-Entwicklung starten**

**Entwicklungsstack wählen:**

| Sprache | Framework                            |
| ------- | ------------------------------------ |
| Python  | `aiogram` oder `python-telegram-bot` |
| Node.js | `node-telegram-bot-api`              |
| Go      | `telebot`, `tgbot`                   |

Ich empfehle **Python + aiogram** für schnellen Start + AWS Lambda-Kompatibilität.

🔹 _Ziel: Bot kann auf `/start` und `/status` antworten_

---

## **3. Datenmodell planen (Produkte, Bestellungen, Nutzer)**

Starte einfach:

- Produkte: ID, Name, Preis, Rabatt
- Bestellungen: ID, Nutzer, Produkt, Status, Zahlung
- Nutzer: Telegram-ID, E-Mail, Adresse

🔹 _Ziel: Minimal-Datenmodell in DynamoDB (oder lokal SQLite für Start)_

---

## **4. Bezahlfluss aufbauen**

- Stripe-Integration vorbereiten
- Telegram Bot Payments oder klassischer Payment-Link
- Webhook-Endpunkt definieren (später via AWS API Gateway + Lambda)

🔹 _Ziel: Bezahlung mit Stripe einmal lokal durchspielen_

---

## **5. Rechnung per Mail senden (SES oder SMTP)**

- PDF-Rechnung generieren (lokal testen)
- E-Mail-Versand testen mit z. B. Amazon SES Sandbox oder Mailtrap

---

## **6. Webhooks produktionsbereit machen (AWS Gateway + Lambda)**

- Bot erhält Events via `POST /bot-webhook`
- Stripe ruft `POST /stripe-webhook` auf

---

## **7. Telegram-Commands mit @BotFather registrieren**

- `/start`, `/status`, `/meine_bestellungen`, `/hilfe`

---

## Fazit: Erste sinnvolle Schritte

| Schritt                                    | Zweck                           |
| ------------------------------------------ | ------------------------------- |
| ✅ Flows + Features definieren             | Klarheit über das MVP           |
| ✅ Bot lokal starten (`/start`, `/status`) | Grundgerüst prüfen              |
| ✅ Beispielprodukt + Bestellung speichern  | Datenmodell testen              |
| ✅ Stripe-Zahlung integrieren              | Ende-zu-Ende-Zahlung            |
| ✅ Webhook-Architektur aufbauen            | für späteres Deployment         |
| ✅ SES-E-Mail-Versand testen               | für Rechnung & Benachrichtigung |

---
