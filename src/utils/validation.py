import io
import re
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

from aiogram.types import Message
from PIL import Image

from keyboards.common import get_abort_keyboard

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")
TELEGRAM_USERNAME_REGEX = re.compile(r"^@?[a-zA-Z0-9_]{5,32}$")
STRIPE_ACCOUNT_ID_REGEX = re.compile(r"^acct_[a-zA-Z0-9]{24}$")


def is_valid_length(value: str, min_length: int = 0, max_length: int = 100) -> bool:
    return min_length <= len(value.strip()) <= max_length


async def validate_string_length_max_50(
    message: Message, value: str, field_name="Wert"
) -> str | None:
    try:
        if is_valid_length(value, min_length=3, max_length=10):
            return value
    except ValueError:
        await message.answer(
            "❌ Ungültiger Wert. Eingabe muss zwischen 3 und 50 Zeichen lang sein.\n\n"
            "Bitte versuche es erneut:",
            get_abort_keyboard(),
        )


async def validate_string_length_max_100(
    message: Message, value: str, field_name="Wert"
) -> str | None:
    try:
        if is_valid_length(value, min_length=3, max_length=100):
            return value
    except ValueError:
        await message.answer(
            "❌ Ungültiger Wert. Eingabe muss zwischen 3 und 100 Zeichen lang sein.\n\n"
            "Bitte versuche es erneut:",
            get_abort_keyboard(),
        )


async def validate_int(message: Message, value: str, field_name="Wert") -> int | None:
    try:
        return int(value)
    except ValueError:
        await message.answer(
            f"❌ Ungültiger {field_name}: Bitte gib eine ganze Zahl ein:",
            reply_markup=get_abort_keyboard(),
        )
        return None


async def validate_decimal(
    message: Message, value: str, field_name="Wert"
) -> Decimal | None:
    value = value.strip()

    # Format: Nur Zahlen mit optionalem Komma und genau 2 Nachkommastellen
    if not re.fullmatch(r"\d{1,5},\d{2}", value):
        await message.answer(
            f"❌ Ungültige Eingabe für {field_name}: Bitte gib eine Zahl mit zwei Nachkommastellen ein, getrennt durch ein Komma (z. B. 19,99).",
            reply_markup=get_abort_keyboard(),
        )
        return None

    # Komma in Punkt umwandeln für Decimal
    normalized = value.replace(",", ".")

    try:
        number = Decimal(normalized)
        return number
    except InvalidOperation:
        await message.answer(
            f"❌ Fehler beim Verarbeiten der Eingabe von {field_name}. Bitte gib einen gültigen Wert wie 12,99 ein.",
            reply_markup=get_abort_keyboard(),
        )
        return None


async def validate_date(message: Message, value: str, field_name="Datum") -> str | None:
    from datetime import datetime

    try:
        parsed = datetime.strptime(value, "%d.%m.%Y")
        return parsed.isoformat()  # Oder return parsed für DynamoDB
    except ValueError:
        await message.answer(
            f"❌ Ungültiges {field_name}: Format bitte TT.MM.JJJJ:",
            reply_markup=get_abort_keyboard(),
        )
        return None


async def validate_email(message: Message, value: str) -> str | None:
    if EMAIL_REGEX.fullmatch(value.strip()):
        return value.strip()
    await message.answer(
        "❌ Ungültige E-Mail-Adresse. Bitte überprüfe dein Format:",
        reply_markup=get_abort_keyboard(),
    )
    return None


async def validate_phone(message: Message, value: str) -> str | None:
    if PHONE_REGEX.fullmatch(value.strip()):
        return value.strip()
    await message.answer(
        "❌ Ungültige Telefonnummer. Erlaubt: +49 123 4567890:",
        reply_markup=get_abort_keyboard(),
    )
    return None


async def validate_telegram_user_id(message: Message, value: str) -> int | None:
    try:
        user_id = int(value)
        if user_id > 0:
            return user_id
    except ValueError:
        pass
    await message.answer(
        "❌ Ungültige Telegram-ID.\n\nBitte versuche es erneut:",
        reply_markup=get_abort_keyboard(),
    )
    return None


async def validate_telegram_username(
    message: Message, value: str, field_name="Telegram-Benutzername"
) -> str | None:
    username = value.strip()
    if TELEGRAM_USERNAME_REGEX.fullmatch(username):
        return username if username.startswith("@") else "@" + username
    await message.answer(
        f"❌ Ungültiger Wert für {field_name}. Bitte gib einen gültigen Wert im Format '@PromoBot' ein, der zwischen 5 und 32 Zeichen lang ist:",
        reply_markup=get_abort_keyboard(),
    )
    return None


async def validate_url(message: Message, value: str) -> str | None:
    parsed = urlparse(value)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return value
    await message.answer(
        "❌ Ungültige URL. Bitte gib einen vollständigen Link an (https://...):",
        reply_markup=get_abort_keyboard(),
    )
    return None


def validate_and_resize_image(
    file_bytes: bytes, max_width=1280, max_height=720
) -> bytes:
    with Image.open(io.BytesIO(file_bytes)) as img:
        if img.width > max_width or img.height > max_height:
            img.thumbnail((max_width, max_height))
        buf = io.BytesIO()
        img.save(buf, format=img.format)
        return buf.getvalue()


async def validate_stripe_account_id(message: Message, value: str) -> str | None:
    if STRIPE_ACCOUNT_ID_REGEX.fullmatch(value.strip()):
        return value.strip()

    await message.answer(
        "❌ Ungültige Stripe-Account-ID.\n\n"
        "Bitte gib eine ID im Format `acct_...` ein:",
        reply_markup=get_abort_keyboard(),
    )
    return None
