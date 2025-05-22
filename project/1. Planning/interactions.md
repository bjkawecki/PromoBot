# Interaktionen

## Käufer

| Interaktion               | Beschreibung                                            |
| ------------------------- | ------------------------------------------------------- |
| **/start**                | Begrüßung, Infos zur Nutzung des Bots                   |
| **Produkt ansehen**       | Über Inline-Button oder Link aus einem Kanalpost        |
| **Produktdaten anzeigen** | Name, Bild, Preis, Rabatt, Beschreibung                 |
| **Bestellung starten**    | Klick auf „Jetzt bestellen“                             |
| **Daten eingeben**        | Name, Adresse, ggf. E-Mail für Rechnung                 |
| **Bezahlmethode wählen**  | Stripe oder andere Zahlungsanbieter                     |
| **Bestellung bestätigen** | Zusammenfassung prüfen und Kauf auslösen                |
| **Bestätigung erhalten**  | Kauf abgeschlossen, Info mit Status + optional Rechnung |
| **/status** oder Button   | Übersicht über eigene Bestellungen                      |
| **Rechnung abrufen**      | PDF oder Link nachträglich abrufen                      |
| **Support kontaktieren**  | Kontakt-Link oder Nachricht an Verkäufer senden         |

## Verkäufer

| Interaktion                 | Beschreibung                                                |
| --------------------------- | ----------------------------------------------------------- |
| **/start**                  | Begrüßung, Erklärung der Funktionen für Verkäufer           |
| **/promo_neu**              | Neue Promo-Aktion anlegen: Produkt, Preis, Rabatt, Laufzeit |
| **/promo_liste**            | Übersicht aktiver und abgelaufener Aktionen                 |
| **Promo posten**            | Inline-Button für Telegram-Kanal erzeugen                   |
| **/bestellungen**           | Aktionen-Liste → Käufe pro Aktion anzeigen                  |
| **Bestellung ansehen**      | Details zu einzelner Bestellung: Käuferdaten, Zeit, Status  |
| **Status ändern**           | z. B. Bestellung als „versendet“ markieren                  |
| **Promo deaktivieren**      | Nicht mehr bestellbar machen                                |
| **Rückerstattung auslösen** | Stripe-Refund und Status setzen                             |
| **/statistik**              | Verkäufe und Umsätze pro Promo-Aktion (optional)            |

## Admin

| Interaktion                 | Beschreibung                                             |
| --------------------------- | -------------------------------------------------------- |
| **/add_seller**             | Neuen Verkäufer registrieren                             |
| **/sellers**                | Liste aller Verkäufer anzeigen                           |
| **/errors**                 | Stripe/Webhook-Fehler prüfen                             |
| **/export**                 | CSV-Export der Verkäufe (z. B. pro Monat)                |
| **Fargate starten/stoppen** | Infrastruktur bei Bedarf manuell aktivieren/deaktivieren |
