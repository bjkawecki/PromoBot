from datetime import datetime

from utils.validation import (
    validate_email,
    validate_phone,
    validate_string_length_max_50,
    validate_stripe_account_id,
    validate_telegram_user_id,
    validate_telegram_username,
    validate_url,
)


def format_datetime(iso_timestamp):
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    return dt.strftime("%d.%m.%Y")


def create_initial_seller_data(telegram_id: int, username: str = "") -> dict:
    return {
        "telegram_user_id": telegram_id,
        "username": username,
        "company_name": "",
        "contact_email": "",
        "display_name": "",
    }


def is_seller_registered(seller: dict) -> bool:
    required = ["company_name", "display_name", "contact_email"]
    return all(seller.get(k) for k in required)


def escape_markdown_v2(text: str) -> str:
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{c}" if c in escape_chars else c for c in text)


FIELD_LABELS = {
    "company_name": "Unternehmensname",
    "display_name": "Anzeigename",
    "contact_name": "Ansprechpartner",
    "contact_email": "E-Mail",
    "contact_phone": "Telefonnummer",
    "website": "Webseite",
    "stripe_account_id": "Stripe-Konto-ID",
}


VALIDATOR_LABELS = {
    "company_name": validate_string_length_max_50,
    "display_name": validate_string_length_max_50,
    "contact_name": validate_string_length_max_50,
    "contact_email": validate_email,
    "contact_phone": validate_phone,
    "website": validate_url,
    "telegram_user_name": validate_telegram_username,
    "stripe_account_id": validate_stripe_account_id,
}


def get_seller_info(seller: object):
    return (
        f"Nutzername: {seller.get('username', '–')}\n"
        f"Telegram-ID: {seller.get('telegram_user_id', '-')}\n"
        f"Unternehmen: {seller.get('company_name', '-')}\n"
        f"Anzeigename: {seller.get('display_name', '-')}\n"
        f"Ansprechperson: {seller.get('contact_name', '-')}\n"
        f"E-Mail: {seller.get('contact_email', '-')}\n"
        f"Telefon: {seller.get('contact_phone', '-')}\n"
        f"website: {seller.get('website', '-')}\n"
        f"Stripe-Konto-ID: {seller.get('stripe_account_id', '–')}\n"
        f"Aktiv: {'Ja' if seller.get('active') else 'Nein'}\n"
        f"Registriert: {'Ja' if seller.get('is_registered') else 'Nein'}\n"
        f"Hinzugefügt: {format_datetime(seller.get('created_at'))}"
    )
