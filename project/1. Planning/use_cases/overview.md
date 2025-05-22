# Überblick

## **Haupt-Use Cases**

### 1. **Kanalbetreiber startet eine Telegram-Promo für ein Produkt**

- Ziel: Ein Produkt aus dem eigenen Webshop direkt im Telegram-Kanal bewerben.
- Ablauf:

  - Betreiber hinterlegt Produktinformationen beim Promo-Bot (Name, Preis, Rabatt, URL, Bild, etc.).
  - Der Bot generiert einen Telegram-kompatiblen Bestell-Link oder -Button.
  - Betreiber fügt diesen Button in einen Kanalpost ein.

---

### 2. **Nutzer klickt im Telegram-Post auf „Jetzt bestellen“**

- Ziel: Als Kanalabonnent ein rabattiertes Produkt direkt in Telegram kaufen.
- Ablauf:

  - Nutzer klickt auf den Button → Bot leitet zu einem Konversationsablauf.
  - Der Bot fragt nacheinander relevante Daten ab:

    - Vorname, Nachname
    - Lieferadresse
    - E-Mail (für Rechnung)

  - Bot zeigt Produktvorschau und fragt: „Kauf bestätigen?“
  - Nach Bestätigung wird Stripe-Checkout geöffnet.
  - Nach erfolgreicher Zahlung: Bestätigung durch den Bot + Bestellübersicht.

---

### 3. **Nutzer möchte seine Bestellung und deren Status einsehen**

- Ziel: Überblick über Bestellungen, z. B. ob die Ware versendet wurde.
- Ablauf:

  - Nutzer gibt `/status` ein oder klickt auf „Meine Bestellungen“.
  - Bot listet alle Bestellungen auf:

    - Produktname, Datum, Status (z. B. „bezahlt“, „versendet“, „storniert“)

---

### 4. **Verkäufer erhält eine Bestellung und verwaltet den Status**

- Ziel: Bestellungen empfangen und manuell abwickeln.
- Ablauf:

  - Verkäufer bekommt bei neuer Bestellung eine Nachricht vom Bot (mit Käuferdaten).
  - Über einen `/orders`-Befehl oder einen privaten Bot-Kanal sieht er alle aktuellen Bestellungen.
  - Verkäufer kann den Status ändern, z. B. auf „Versendet“ oder „Storniert“.
  - Der Käufer wird bei Statusänderung benachrichtigt.

---

### 5. **Verkäufer startet oder beendet eine Promo-Kampagne**

- Ziel: Promo-Aktion nur zu bestimmten Zeitpunkten aktiv schalten.
- Ablauf:

  - Verkäufer ruft `/newpromo` auf und gibt Produktdaten ein.
  - Bot gibt Button-Code zum Einfügen im Kanal zurück.
  - Verkäufer kann die Promo später mit `/stoppromo` deaktivieren.

---

## 🔄 **Zusammengefasste Ablauf-Logik (Textform)**

### Ablauf 1: Bestellung aus Telegram-Post

1. Kanalbetreiber erstellt ein Promo-Angebot über den Bot.
2. Bot generiert einen Inline-Button für Telegram-Post.
3. Nutzer klickt auf den Button → Telegram-Dialog startet.
4. Bot fragt Adresse, Name, E-Mail ab.
5. Bot zeigt Übersicht → Nutzer bestätigt.
6. Stripe Checkout wird geöffnet.
7. Nach Zahlung: Webhook benachrichtigt Bot.
8. Bot speichert Bestellung und sendet Bestätigung.
9. Verkäufer wird benachrichtigt.
10. Käufer kann `/status` verwenden.

---

### Ablauf 2: Bestellstatus-Änderung durch Verkäufer

1. Verkäufer ruft `/orders` auf oder öffnet Admin-Dashboard.
2. Wählt eine Bestellung aus.
3. Ändert Status z. B. auf „Versendet“.
4. Bot informiert den Käufer automatisch.
