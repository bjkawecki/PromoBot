from datetime import datetime


def format_datetime(iso_timestamp):
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    return dt.strftime("%d.%m.%Y")


def create_initial_seller_data(telegram_id: int, username: str = "") -> dict:
    return {
        "telegram_user_id": telegram_id,
        "username": username,
        "business_name": "",
        "contact_email": "",
        "display_name": "",
    }


def is_seller_registered(seller: dict) -> bool:
    required = ["business_name", "display_name", "contact_email"]
    return all(seller.get(k) for k in required)


def escape_markdown_v2(text: str) -> str:
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{c}" if c in escape_chars else c for c in text)
