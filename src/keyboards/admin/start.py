from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👔 Verkäufer", callback_data="admin_sellers_menu"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📣 Promos", callback_data="admin_promotions_menu"
                )
            ],
            [InlineKeyboardButton(text="📊 Statistik", callback_data="admin_stats")],
        ]
    )
