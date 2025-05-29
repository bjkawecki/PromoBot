import re
from urllib.parse import urlparse

from aiogram.types import Message

from keyboards.admin.manage_seller import get_retry_or_abort_keyboard

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")
TELEGRAM_USERNAME_REGEX = re.compile(r"^@?[a-zA-Z0-9_]{5,32}$")


async def validate_int(message: Message, value: str, field_name="Wert") -> int | None:
    try:
        return int(value)
    except ValueError:
        await message.answer(
            f"❌ Ungültiger {field_name}: Bitte gib eine ganze Zahl ein."
        )
        return None


async def validate_date(message: Message, value: str, field_name="Datum") -> str | None:
    from datetime import datetime

    try:
        parsed = datetime.strptime(value, "%d.%m.%Y")
        return parsed.isoformat()  # Oder return parsed für DynamoDB
    except ValueError:
        await message.answer(f"❌ Ungültiges {field_name}: Format bitte TT.MM.JJJJ.")
        return None


async def validate_email(message: Message, value: str) -> str | None:
    if EMAIL_REGEX.fullmatch(value.strip()):
        return value.strip()
    await message.answer("❌ Ungültige E-Mail-Adresse. Bitte überprüfe dein Format.")
    return None


async def validate_phone(message: Message, value: str) -> str | None:
    if PHONE_REGEX.fullmatch(value.strip()):
        return value.strip()
    await message.answer("❌ Ungültige Telefonnummer. Erlaubt: +49 123 4567890")
    return None


async def validate_telegram_user_id(message: Message, value: str) -> int | None:
    try:
        user_id = int(value)
        if user_id > 0:
            return user_id
    except ValueError:
        pass
    await message.answer(
        "❌ Ungültige Telegram-ID. Bitte gib eine gültige Zahl ein.",
        reply_markup=get_retry_or_abort_keyboard(),
    )
    return None


async def validate_telegram_username(message: Message, value: str) -> str | None:
    username = value.strip()
    if TELEGRAM_USERNAME_REGEX.fullmatch(username):
        return username if username.startswith("@") else "@" + username
    await message.answer(
        "❌ Ungültiger Telegram-Benutzername. Beispiel: @PromoBotSupport"
    )
    return None


async def validate_url(message: Message, value: str) -> str | None:
    parsed = urlparse(value)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return value
    await message.answer(
        "❌ Ungültige URL. Bitte gib einen vollständigen Link an (https://...)."
    )
    return None
