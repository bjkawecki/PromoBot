# To do

## Admin

- promos view: list, emphasize status
- promo view: details with buttons "Blockieren/Freigeben", "Löschen", "Endgültig löschen"
  - damit eine Promo gelöscht werden kann, muss es den Status "deleted" haben
- promo action: hard delete

## Seller

- help/FAQ:
  - welche Promo Felder man updaten darf
  - Leitfaden für das Erstellen von Promo: Am besten Texte vorbereiten und dann Copy-Paste

## middleware

- seller: check
  - is active
  - is blocked
- promo: check
  - is active
  - is blocked
  - date is between start_date and end_date

## Refactor

- move text messages to src/messages, check for redundancy
