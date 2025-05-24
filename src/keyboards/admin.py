from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Dashboard", callback_data="admin_dashboard")]
        ]
    )
