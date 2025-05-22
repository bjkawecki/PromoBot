# Planphasen

## **1. Planung & Spezifikation**

### Ziel: Minimale, funktionale MVP-Version (nicht gleich alles bauen)

**Was du brauchst:**

- Klare **Use Cases**: z. B. "Nutzer klickt Button → Bestellt Produkt"
- Liste der **Interaktionen** (z. B. `/start`, Produkt anzeigen, Daten abfragen, Bestellung bestätigen)
- Entscheidung über **Zahlungsanbieter** (Stripe empfohlen)
- Entscheidung über **Speicherlösung** (z. B. DynamoDB oder PostgreSQL)

**Tipp:** Halte alle Abläufe in **Ablaufdiagrammen oder Sequenzdiagrammen** fest (z. B. mit Excalidraw oder Mermaid).

---

## **2. Technische Architektur & Setup**

### Ziel: Infrastruktur vorbereiten, bevor du die Logik baust

**ToDos:**

- Telegram Bot erstellen (mit BotFather) und Token sichern
- Git-Repo aufsetzen
- Projektstruktur vorbereiten (z. B. mit `aiogram`)
- AWS Setup:

  - ECR für Container
  - DynamoDB (falls NoSQL reicht)
  - Stripe-API-Key einbinden
  - ggf. S3 für Rechnungsspeicherung

**Tipp:** Lokale Entwicklung mit Docker und **ngrok** oder **AWS API Gateway** für Webhook-Tests.

---

## **3. MVP-Entwicklung (inkrementell)**

### Ziel: Schnell einen nutzbaren Kern bauen – dann erweitern

**Entwicklungsschritte (vorschlag):**

1. **Bot-Grundstruktur mit aiogram**
2. **Webhook-Empfang & Routing**
3. **/start-Befehl und Produktansicht mit Inline-Button**
4. **Bestellvorgang:**

   - Nutzer gibt Daten an
   - Stripe Checkout Session

5. **Webhook-Endpunkt für Zahlungsbestätigung**
6. **Speicherung der Bestellung + Status**
7. **/status-Befehl für Nutzer**
8. **Admin-Benachrichtigung per Message**

**Tools:**

- `aiogram` für Bot-Logik
- `pydantic` für Validierung
- `Stripe-Python` SDK
- `boto3` für DynamoDB (wenn AWS-native)

---

## **4. Deployment & Wartung**

### Ziel: Automatisiert, kosteneffizient und sicher betreiben

**Empfehlung:**

- Code als Docker-Image packen
- Deployment via ECS Fargate (per Knopfdruck bei Bedarf)
- Logging z. B. mit CloudWatch
- Stripe Webhook über API Gateway oder ALB weiterleiten
- Nutzung tracken (z. B. mit einer "Verwendung"-Tabelle)

**Tipp:** Automatisierter Task-Start (z. B. via Admin-Button oder Trigger in deinem System)

---

## ✅ **Zusammengefasst:**

| Phase       | Ziel                             | Tools                     |
| ----------- | -------------------------------- | ------------------------- |
| Planung     | Use Cases, Abläufe klären        | Diagramme, Checklisten    |
| Architektur | Setup von AWS + APIs             | Telegram, AWS, Stripe     |
| Entwicklung | MVP zuerst, dann iterativ        | aiogram, Stripe, DynamoDB |
| Deployment  | Günstig und skalierbar betreiben | ECS Fargate, Docker, ALB  |

---

Wenn du möchtest, kann ich dir auch:

- Einen **Roadmap-Plan als Tabelle** mit Prioritäten und Aufwand machen
- Eine **Projektstruktur als Code-Template** vorschlagen
- Eine **Teststrategie** für Webhooks und Bot-Verhalten definieren

Sag einfach Bescheid, womit du starten willst.
