# To do

## Admin

- promos view: list
- promo view: details
- promo action: block/unblock (soft delete)
- promo action: hard delete
- seller action: block/unblock
- seller action: hard delete

## Seller

- buttons: 'Bearbeiten', 'Löschen'

- promo action: update
  - 'Bearbeiten': buttons for all fields to update
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

## Validation

- seller: create promo
- seller: update promo

## Messages

- refactor messages to src/messages/
