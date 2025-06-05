def format_promo_details(promo: object):
    promo_status_map = {
        "active": "✅ Aktiv",
        "inactive": "🚫 Inaktiv",
        "deleted": "🗑 Gelöscht",
    }
    promo_status = promo_status_map[promo.get("promo_status")]
    return (
        f"<b>🔎 Promo Details</b>\n\n"
        f"<b>{promo.get('display_name')}</b>\n\n"
        f"<b>Status:</b> {promo_status}\n"
        f"<b>Preis:</b> {promo.get('price')} €\n"
        f"<b>Versandkosten:</b> {promo.get('shipping_costs')} €\n"
        f"<b>Ausgabekanal:</b> {promo.get('channel_id')}\n"
        f"<b>Startdatum:</b> {promo.get('start_date')}\n"
        f"<b>Enddatum:</b> {promo.get('end_date')}\n"
        f"<b>Nachricht:</b>\n{promo.get('display_message')}\n\n"
        f"<b>Beschreibung:</b>\n{promo.get('description')}\n\n"
        f"<b>{'🚫 Promo ist blockiert. Für mehr Informationen wende dich an den Kundenservice.' if promo.get('blocked', False) else ''}</b>"
    )


def confirm_soft_delete_promo_message(display_name: str) -> str:
    return f"❗️Bist du sicher, dass du die Promo <b>'{display_name}'</b> als 'gelöscht' markieren willst?"


PROMO_LIST_MENU = "<b>📢 Promo-Menü</b>\n\nWähle eine Promo aus:"
PROMO_NOT_FOUND = "❌ Promo nicht gefunden."
