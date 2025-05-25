from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Verkäufer hinzufügen",
                    callback_data="add_seller",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📃 Verkäufer anzeigen", callback_data="display_sellers"
                )
            ],
        ]
    )
