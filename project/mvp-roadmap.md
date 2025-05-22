# Telegram Promo-Bot – MVP Roadmap

| Phase | Aufgabe                                                    | Priorität | Aufwand (Tage) | Kommentar                                      |
| ----- | ---------------------------------------------------------- | --------- | -------------- | ---------------------------------------------- |
| **1** | Use Cases + Ablauflogik skizzieren                         | Hoch      | 0.5            | Z. B. mit Excalidraw oder Miro                 |
| **1** | Stripe-Account einrichten + Webhook-URL testen             | Hoch      | 0.5            | Testdaten aktivieren                           |
| **2** | Lokale Projektstruktur aufsetzen (aiogram, Docker etc.)    | Hoch      | 1              | Minimales Setup mit `/start` und einem Handler |
| **2** | DynamoDB oder PostgreSQL vorbereiten                       | Mittel    | 1              | Z. B. für Bestellungen, Nutzer, Status         |
| **3** | Produkteingabe vom Verkäufer (simple JSON/API)             | Hoch      | 1              | Noch kein UI nötig                             |
| **3** | Inline-Button im Post generieren                           | Hoch      | 1              | Mit `InlineKeyboardMarkup`                     |
| **3** | Nutzer-Interaktion: Daten erfassen (Name, Adresse, E-Mail) | Hoch      | 1.5            | FSM/Dialogstruktur in aiogram                  |
| **3** | Stripe Checkout Session erzeugen                           | Hoch      | 1.5            | Session-URL zurückgeben                        |
| **3** | Stripe Webhook empfangen + Bestellung speichern            | Hoch      | 1.5            | Fargate/Webhook-Test                           |
| **3** | `/status`-Befehl für Nutzer (Käufe + Status)               | Mittel    | 1              | Übersicht als Textnachricht                    |
| **3** | Admin-Benachrichtigung bei Bestellung                      | Mittel    | 0.5            | Verkäufer erhält Telegram-Message              |
| **4** | Admin-/Verkäufer-Sicht: `/orders`, Status ändern           | Mittel    | 1              | Zunächst CLI oder Bot-Command                  |
| **4** | Rechnung per Mail oder PDF-Link (optional)                 | Niedrig   | 1              | z. B. via PDFKit + S3                          |
| **4** | Deployment via ECS Fargate (Start per CLI oder Button)     | Mittel    | 2              | Optional mit Admin-Trigger oder API            |
| **5** | Logging & Monitoring einbauen (CloudWatch, Alerts)         | Mittel    | 1              | Für Stripe-Fehler, Webhook-Ausfälle etc.       |
