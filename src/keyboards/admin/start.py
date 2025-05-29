from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_admin_keyboard():
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
                    text="📃 Verkäuferliste", callback_data="display_sellers"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📣 Promos", callback_data="display_promotions"
                )
            ],
        ]
    )
