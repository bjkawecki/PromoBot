# Use Case Checklists

## Buyer

| Use Case                 | Beschreibung                               | Diagramm sinnvoll? |
| ------------------------ | ------------------------------------------ | ------------------ |
| ✅ Produkt bestellen     | Klick auf Button, Daten eingeben, bezahlen | ✅ (Sequence)      |
| ✅ Bestellung bestätigen | Checkout + Info erhalten                   | ✅ (Sequence)      |
| ✅ Bestellung einsehen   | `/status` oder „Meine Bestellungen“        | ❌ (einfach)       |
| ❓ Rechnung abrufen      | PDF oder HTML-Link                         | ✅ (Flowchart)     |
| ❓ Kontakt zum Verkäufer | z. B. bei Problemen (Support-Link)         | ❌                 |

## Seller

| Use Case                   | Beschreibung                                          | Diagramm sinnvoll? |
| -------------------------- | ----------------------------------------------------- | ------------------ |
| ✅ Promo anlegen           | Produktdaten, Preis, Rabatt eingeben                  | ✅ (Flowchart)     |
| ✅ Promo posten            | Button oder Link generieren                           | ❌                 |
| ✅ Bestellungen einsehen   | Übersicht über alle Promo-Käufe                       | ✅ (Flowchart)     |
| ✅ Bestellstatus ändern    | z. B. auf „versendet“ setzen                          | ✅ (State Diagram) |
| ❓ Promo beenden           | Deaktivieren, damit Produkt nicht mehr bestellbar ist | ❌                 |
| ❓ Rückerstattung auslösen | Stripe-Rückzahlung und Status setzen                  | ✅ (Sequence)      |
| ❓ Statistik abrufen       | z. B. Verkäufe pro Promo anzeigen                     | ✅ (Flowchart)     |

## Externe Systeme (Stripe, AWS)

| Use Case                        | Beschreibung                                   | Diagramm sinnvoll? |
| ------------------------------- | ---------------------------------------------- | ------------------ |
| ✅ Stripe sendet Webhook        | Zahlung bestätigt, Bot aktualisiert Bestellung | ✅ (Sequence)      |
| ❓ Stripe sendet Rückerstattung | Bot setzt Status „erstattet“                   | ✅ (Sequence)      |
| ✅ AWS startet Infrastruktur    | Manuell oder per Event                         | ✅ (Flowchart)     |

## Admin

| Use Case                           | Beschreibung                                        | Diagramm sinnvoll? |
| ---------------------------------- | --------------------------------------------------- | ------------------ |
| Verkäufer registrieren             | Verkäufer hinzufügen: über Bot oder Web-Formular    | ✅ (Flowchart)     |
| Verkäufer deaktivieren/sperren     | Deaktivierung via Befehl                            | ❌                 |
| Alle Verkäufer einsehen            | Übersicht über alle registrierten Verkäufer         | ❌                 |
| Promo-Aktivität überwachen         | Bestellverläufe und -zahlen pro Verkäufer sehen     | ✅ (Flowchart)     |
| Webhook-Fehler prüfen              | Fehleranzeige und Logging-Möglichkeit               | ✅ (Flowchart)     |
| Verkäufer-Support leisten          | Admin-Einblick in einzelne Transaktionen            | ✅ (Sequence)      |
| Manuelles Auslösen von Prozessen   | Versandnachricht erneut senden etc.                 | ✅ (Flowchart)     |
| Fargate/Lambda starten/stoppen     | Verarbeitung anstoßen bei Bedarf                    | ✅ (Sequence)      |
| Abrechnungsdaten exportieren       | CSV-Export je Verkäufer                             | ❌                 |
| Admin-Benachrichtigungen verwalten | Regeln festlegen, wann Admins benachrichtigt werden | ❌                 |
