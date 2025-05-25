from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.admin import admin_keyboard
from keyboards.buyer import buyer_keyboard
from keyboards.seller import seller_keyboard


def get_back_to_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Abbrechen", callback_data="back_to_start"),
            ],
        ]
    )


def get_role_keyboard(role: str) -> InlineKeyboardMarkup:
    if role == "admin":
        return admin_keyboard
    elif role == "seller":
        return seller_keyboard
    else:
        return buyer_keyboard
