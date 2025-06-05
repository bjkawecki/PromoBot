from datetime import datetime

from utils.validation import (
    validate_date,
    validate_decimal,
    validate_email,
    validate_phone,
    validate_string_length_max_50,
    validate_string_length_max_100,
    validate_stripe_account_id,
    validate_telegram_username,
    validate_url,
)

promo_status_emoji_map = {
    "active": "✅",
    "inactive": "🚫",
    "deleted": "🗑",
}


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


SELLER_FIELD_LABELS = {
    "company_name": "Unternehmensname",
    "display_name": "Anzeigename",
    "contact_name": "Ansprechpartner",
    "contact_email": "E-Mail",
    "contact_phone": "Telefonnummer",
    "Webseite": "Webseite",
    "stripe_account_id": "Stripe-Konto-ID",
}


SELLER_VALIDATOR_METHODS_MAP = {
    "company_name": validate_string_length_max_50,
    "display_name": validate_string_length_max_50,
    "contact_name": validate_string_length_max_50,
    "contact_email": validate_email,
    "contact_phone": validate_phone,
    "website": validate_url,
    "telegram_user_name": validate_telegram_username,
    "stripe_account_id": validate_stripe_account_id,
}


PROMO_FIELD_LABELS = {
    "display_name": "Name",
    "price": "Preis",
    "shipping_costs": "Versandkosten",
    "channel_id": "Ausgabekanal",
    "start_date": "Startdatum",
    "end_date": "Enddatum",
    "image": "Bild",
    "message": "Nachricht",
    "description": "Beschreibung",
}


PROMO_VALIDATOR_MAP = {
    "display_name": validate_string_length_max_50,
    "price": validate_decimal,
    "shipping_costs": validate_decimal,
    "channel_id": validate_telegram_username,
    "start_date": validate_date,
    "end_date": validate_date,
    "image": validate_url,
    "message": validate_string_length_max_50,
    "description": validate_string_length_max_100,
}


def format_new_promo(data):
    return {
        "promo_id": data.get("promo_id"),
        "seller_id": data.get("seller_id"),
        "display_name": data.get("display_name"),
        "display_message": data.get("display_message"),
        "description": data.get("description", ""),
        "price": data.get("price"),
        "shipping_costs": data.get("shipping_costs"),
        "channel_id": data.get("channel_id"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "image": data.get("image", ""),
        "promo_status": "inactive",
    }
