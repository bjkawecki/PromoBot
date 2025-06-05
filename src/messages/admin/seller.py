from utils.misc import format_datetime

ADD_NEW_SELLER_MESSAGE = (
    "Neuen Verkäufer hinzufügen\n\n"
    "Bitte gib die <b>Telegram-Nutzer-ID</b> des neuen Verkäufers an:"
)


def format_seller_info(seller: dict):
    seller_status = seller.get("seller_status")
    seller_status_map = {
        "active": "✅ Aktiv",
        "inactive": "🚫 Deaktiviert",
    }
    seller_status = seller_status_map[seller.get("seller_status", "active")]
    return (
        f"<b>Status:</b> {seller_status}\n\n"
        f"Nutzername: {seller.get('username', '–')}\n"
        f"Telegram-ID: {seller.get('telegram_user_id', '-')}\n"
        f"Unternehmen: {seller.get('company_name', '-')}\n"
        f"Anzeigename: {seller.get('display_name', '-')}\n"
        f"Ansprechperson: {seller.get('contact_name', '-')}\n"
        f"E-Mail: {seller.get('contact_email', '-')}\n"
        f"Telefon: {seller.get('contact_phone', '-')}\n"
        f"Webseite: {seller.get('website', '-')}\n"
        f"Stripe-Konto-ID: {seller.get('stripe_account_id', '–')}\n"
        f"Registriert: {'Ja' if seller.get('is_registered') else 'Nein'}\n"
        f"Hinzugefügt: {format_datetime(seller.get('created_at'))}"
    )


def seller_not_found_answer(telegram_id: int) -> str:
    return f"❌ Verkäufer mit ID {telegram_id} nicht gefunden."


ADMIN_SELLERS_MENU = "<b>👔 Verkäufer-Menü</b>"
NO_REGISTERED_SELLERS = "❌ Es sind noch keine Verkäufer registriert."
CHOOSE_SELLER = "Wähle einen Verkäufer aus:"
SELLER_NOT_FOUND = "❌ Verkäufer nicht gefunden."
NO_SELLER_PROMOS = "❌ Verkäufer hat noch keine Promos erstellt."


def confirm_toggle_user_message(action: str, seller_info: str):
    return (
        "❗️<b>Bist du sicher, dass du den folgenden Verkäufer "
        f"{'aktivieren' if action == 'activate' else 'deaktivieren'} möchtest?</b>\n\n"
        f"{seller_info}"
    )


def confirm_seller_toggle_answer(seller_status):
    return (
        "✅ Verkäufer wurde aktiviert."
        if seller_status == "active"
        else "🚫 Verkäufer wurde deaktiviert."
    )


def confirm_saved_seller_answer(telegram_user_id):
    return (
        f"✅ Neuer Verkäufer mit Telegram-User-ID {telegram_user_id} wurde gespeichert."
    )
